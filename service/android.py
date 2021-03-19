# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for performing Android uprev."""

import os
import re
import time

from chromite.lib import constants
from chromite.lib import cros_logging as logging
from chromite.lib import gs


def IsBuildIdValid(bucket_url, build_branch, build_id):
  """Checks that a specific build_id is valid.

  Looks for that build_id for all builds. Confirms that the subpath can
  be found and that the zip file is present in that subdirectory.

  Args:
    bucket_url: URL of Android build gs bucket
    build_branch: branch of Android builds
    build_id: A string. The Android build id number to check.

  Returns:
    Returns subpaths dictionary if build_id is valid.
    None if the build_id is not valid.
  """
  targets = constants.ANDROID_BRANCH_TO_BUILD_TARGETS[build_branch]
  gs_context = gs.GSContext()
  subpaths_dict = {}
  for build, (target, _) in targets.items():
    build_dir = f'{build_branch}-linux-{target}'
    build_id_path = os.path.join(bucket_url, build_dir, build_id)

    # Find name of subpath.
    try:
      subpaths = gs_context.List(build_id_path)
    except gs.GSNoSuchKey:
      logging.warning(
          'Directory [%s] does not contain any subpath, ignoring it.',
          build_id_path)
      return None
    if len(subpaths) > 1:
      logging.warning(
          'Directory [%s] contains more than one subpath, ignoring it.',
          build_id_path)
      return None

    subpath_dir = subpaths[0].url.rstrip('/')
    subpath_name = os.path.basename(subpath_dir)

    # Look for a zipfile ending in the build_id number.
    try:
      gs_context.List(subpath_dir)
    except gs.GSNoSuchKey:
      logging.warning(
          'Did not find a file for build id [%s] in directory [%s].',
          build_id, subpath_dir)
      return None

    # Record subpath for the build.
    subpaths_dict[build] = subpath_name

  # If we got here, it means we found an appropriate build for all platforms.
  return subpaths_dict


def GetLatestBuild(bucket_url, build_branch):
  """Searches the gs bucket for the latest green build.

  Args:
    bucket_url: URL of Android build gs bucket
    build_branch: branch of Android builds

  Returns:
    Tuple of (latest version string, subpaths dictionary)
    If no latest build can be found, returns None, None
  """
  targets = constants.ANDROID_BRANCH_TO_BUILD_TARGETS[build_branch]
  gs_context = gs.GSContext()
  common_build_ids = None
  # Find builds for each target.
  for target, _ in targets.values():
    build_dir = f'{build_branch}-linux-{target}'
    base_path = os.path.join(bucket_url, build_dir)
    build_ids = []
    for gs_result in gs_context.List(base_path):
      # Remove trailing slashes and get the base name, which is the build_id.
      build_id = os.path.basename(gs_result.url.rstrip('/'))
      if not build_id.isdigit():
        logging.warning('Directory [%s] does not look like a valid build_id.',
                        gs_result.url)
        continue
      build_ids.append(build_id)

    # Update current list of builds.
    if common_build_ids is None:
      # First run, populate it with the first platform.
      common_build_ids = set(build_ids)
    else:
      # Already populated, find the ones that are common.
      common_build_ids.intersection_update(build_ids)

  if common_build_ids is None:
    logging.warning('Did not find a build_id common to all platforms.')
    return None, None

  # Otherwise, find the most recent one that is valid.
  for build_id in sorted(common_build_ids, key=int, reverse=True):
    subpaths = IsBuildIdValid(bucket_url, build_branch, build_id)
    if subpaths:
      return build_id, subpaths

  # If not found, no build_id is valid.
  logging.warning('Did not find a build_id valid on all platforms.')
  return None, None


def _GetArcBasename(build, basename):
  """Tweaks filenames between Android bucket and ARC++ bucket.

  Android builders create build artifacts with the same name for -user and
  -userdebug builds, which breaks the android-container ebuild (b/33072485).
  When copying the artifacts from the Android bucket to the ARC++ bucket some
  artifacts will be renamed from the usual pattern
  *cheets_${ARCH}-target_files-S{VERSION}.zip to
  cheets_${BUILD_NAME}-target_files-S{VERSION}.zip which will typically look
  like cheets_(${LABEL})*${ARCH}_userdebug-target_files-S{VERSION}.zip.

  Args:
    build: the build being mirrored, e.g. 'X86', 'ARM', 'X86_USERDEBUG'.
    basename: the basename of the artifact to copy.

  Returns:
    The basename of the destination.
  """
  if build not in constants.ARC_BUILDS_NEED_ARTIFACTS_RENAMED:
    return basename
  if basename in constants.ARC_ARTIFACTS_RENAME_NOT_NEEDED:
    return basename
  to_discard, sep, to_keep = basename.partition('-')
  if not sep:
    logging.error(('Build %s: Could not find separator "-" in artifact'
                   ' basename %s'), build, basename)
    return basename
  if 'cheets_' in to_discard:
    return 'cheets_%s-%s' % (build.lower(), to_keep)
  elif 'bertha_' in to_discard:
    return 'bertha_%s-%s' % (build.lower(), to_keep)
  logging.error('Build %s: Unexpected artifact basename %s',
                build, basename)
  return basename


def CopyToArcBucket(android_bucket_url, build_branch, build_id, subpaths,
                    arc_bucket_url, acls):
  """Copies from source Android bucket to ARC++ specific bucket.

  Copies each build to the ARC bucket eliminating the subpath.
  Applies build specific ACLs for each file.

  Args:
    android_bucket_url: URL of Android build gs bucket
    build_branch: branch of Android builds
    build_id: A string. The Android build id number to check.
    subpaths: Subpath dictionary for each build to copy.
    arc_bucket_url: URL of the target ARC build gs bucket
    acls: ACLs dictionary for each build to copy.
  """
  targets = constants.ANDROID_BRANCH_TO_BUILD_TARGETS[build_branch]
  gs_context = gs.GSContext()
  for build, subpath in subpaths.items():
    target, pattern = targets[build]
    build_dir = f'{build_branch}-linux-{target}'
    android_dir = os.path.join(android_bucket_url, build_dir, build_id, subpath)
    arc_dir = os.path.join(arc_bucket_url, build_dir, build_id)

    # Copy all target files from android_dir to arc_dir, setting ACLs.
    for targetfile in gs_context.List(android_dir):
      if re.search(pattern, targetfile.url):
        basename = os.path.basename(targetfile.url)
        arc_path = os.path.join(arc_dir, _GetArcBasename(build, basename))
        acl = acls[build]
        needs_copy = True
        retry_count = 2

        # Retry in case race condition when several boards trying to copy the
        # same resource
        while True:
          # Check a pre-existing file with the original source.
          if gs_context.Exists(arc_path):
            if (gs_context.Stat(targetfile.url).hash_crc32c !=
                gs_context.Stat(arc_path).hash_crc32c):
              logging.warning('Removing incorrect file %s', arc_path)
              gs_context.Remove(arc_path)
            else:
              logging.info('Skipping already copied file %s', arc_path)
              needs_copy = False

          # Copy if necessary, and set the ACL unconditionally.
          # The Stat() call above doesn't verify the ACL is correct and
          # the ChangeACL should be relatively cheap compared to the copy.
          # This covers the following caes:
          # - handling an interrupted copy from a previous run.
          # - rerunning the copy in case one of the googlestorage_acl_X.txt
          #   files changes (e.g. we add a new variant which reuses a build).
          if needs_copy:
            logging.info('Copying %s -> %s (acl %s)',
                         targetfile.url, arc_path, acl)
            try:
              gs_context.Copy(targetfile.url, arc_path, version=0)
            except gs.GSContextPreconditionFailed as error:
              if not retry_count:
                raise error
              # Retry one more time after a short delay
              logging.warning('Will retry copying %s -> %s',
                              targetfile.url, arc_path)
              time.sleep(5)
              retry_count = retry_count - 1
              continue
          gs_context.ChangeACL(arc_path, acl_args_file=acl)
          break


def MirrorArtifacts(android_bucket_url, android_build_branch, arc_bucket_url,
                    acls, version=None):
  """Mirrors artifacts from Android bucket to ARC bucket.

  First, this function identifies which build version should be copied,
  if not given. Please see GetLatestBuild() and IsBuildIdValid() for details.

  On build version identified, then copies target artifacts to the ARC bucket,
  with setting ACLs.

  Args:
    android_bucket_url: URL of Android build gs bucket
    android_build_branch: branch of Android builds
    arc_bucket_url: URL of the target ARC build gs bucket
    acls: ACLs dictionary for each build to copy.
    version: (optional) A string. The Android build id number to check.
        If not passed, detect latest good build version.

  Returns:
    Mirrored version.
  """
  if version:
    subpaths = IsBuildIdValid(android_bucket_url, android_build_branch, version)
    if not subpaths:
      logging.error('Requested build %s is not valid', version)
  else:
    version, subpaths = GetLatestBuild(android_bucket_url, android_build_branch)

  CopyToArcBucket(android_bucket_url, android_build_branch, version, subpaths,
                  arc_bucket_url, acls)

  return version


def MakeAclDict(package_dir):
  """Creates a dictionary of acl files for each build type.

  Args:
    package_dir: The path to where the package acl files are stored.

  Returns:
    Returns acls dictionary.
  """
  return dict(
      (k, os.path.join(package_dir, v))
      for k, v in constants.ARC_BUCKET_ACLS.items()
  )
