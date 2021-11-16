# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Uprev Chrome OS LTS kernel.

Update Chrome OS manifest commit ids to the latest LTS commit ids used in
kernel repo.

Assumptions:
  1. The user has a full chromiumos checkout.
  2. XML structure follows //project/{name|path|revision}.
  3. Kernel repos have name="chromiumos/third_party/kernel".
  4. Each kernel repo revision is unique.
"""

import datetime
import logging
import os
from pathlib import Path
import re
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import uri_lib


def _parse_iso_date_str(date_str: str) -> datetime.datetime:
  """Transform ISO date string into a datetime.

  Args:
    date_str: ISO date string.

  Returns:
    A datetime object representing the same time as date_str.
  """
  try:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
  except TypeError:
    return None


class LtsKernelUprev():
  """Class to represent upreving LTS kernels."""

  KERNEL_PROJECT_NAME = 'chromiumos/third_party/kernel'

  def __init__(self, release_milestone: str, buildroot: Path):
    """Initialize the LtsKernelUprev class.

    Args:
      release_milestone: Milestone to use for LTS kernel uprev.
      buildroot: Path to chromiumos checkout.
    """
    self.release_milestone = release_milestone
    self.buildroot = buildroot
    self.kernel_repo_path = buildroot / 'src/third_party/kernel'
    self.manifest_repo_path = buildroot / 'manifest-internal'
    self.full_manifest_path = self.manifest_repo_path / 'full.xml'

  def get_branch_name(self) -> str:
    """Determine branch stem using the kernel repo path and release milestone.

    Returns:
      The stem of branches in the kernel repo which contain the release
      milestone, or '' if no milestone branches are found.
    """
    kernel_upstream_path = self.kernel_repo_path / 'upstream'
    release_branches = cros_build_lib.run(
        [
            'git',
            'for-each-ref',
            '--format',
            '%(refname:lstrip=-1)',
            f'refs/remotes/cros/release-{self.release_milestone}-*',
        ],
        capture_output=True,
        encoding='utf-8',
        cwd=kernel_upstream_path).stdout.splitlines()
    return self._get_branch_stem(release_branches)

  def _get_branch_stem(self, branches: List[str]) -> str:
    """Determine branch stem given a list of branches.

    Args:
      branches: All branches containing the release milestone (e.g. ['remotes/
        cros/release-R96-14268.B-chromeos-4.4', 'remotes/cros/release-R96-14268.
        B-chromeos-5.10']).

    Returns:
      The stem of branches in the kernel repo which contain the release
      milestone (e.g. 'release-R96-14268.B-chromeos-').
    """
    # Select any branch because they all share the same prefix.
    try:
      branch = branches[0].strip()
    except IndexError:
      return None
    # Remove remote prefix.
    branch = os.path.basename(branch)
    # Find and remove the kernel version.
    branch_kernel_version = branch.split('-')[-1]
    branch_stem = branch.replace(branch_kernel_version, '')
    return branch_stem

  def find_new_kernel_commit_ids(
      self, branch_stem: str, manifest_tree: ET.ElementTree) -> Dict[str, str]:
    """Determine latest commit id for each kernel repo.

    Args:
      branch_stem: The stem of branches for the release milestone.
      manifest_tree: Representation of manifest XML hierarchy.

    Returns:
      Mapping of strings to find -> replace in XML manifest.
    """
    replace_mapping = {}
    for kernel_element in manifest_tree.getroot().findall('.//project'):
      if kernel_element.attrib['name'] == self.KERNEL_PROJECT_NAME:
        kernel_path = self.buildroot / kernel_element.attrib['path']
        orig_kernel_version = os.path.basename(kernel_path)
        # Remove first 'v' from repo kernel version (e.g. v5.10) to get
        # branch-style kernel version (e.g. 5.10).
        kernel_version = orig_kernel_version.replace('v', '', 1)
        branch_name = f'{branch_stem}{kernel_version}'
        if not os.path.exists(kernel_path):
          logging.warning('Could not find "%s". Skipping.', kernel_path)
          continue

        try:
          branch_tag = cros_build_lib.run(
              ['git', 'describe', f'remotes/cros/{branch_name}'],
              capture_output=True,
              encoding='utf-8',
              cwd=kernel_path).stdout.strip()
        except cros_build_lib.RunCommandError as e:
          logging.warning(
              'No tag in "%s" for branch "remotes/cros/%s: %s". Skipping.',
              kernel_path, branch_name, e)
          continue

        if not branch_tag:
          logging.warning('No branch found for "%s": "%s"', kernel_path,
                          branch_name)
          continue

        branch_commit_id = git.GetGitRepoRevision(
            kernel_path, branch=branch_tag)
        orig_rev = kernel_element.attrib['revision']
        kernel_element.attrib['revision'] = branch_commit_id
        if orig_rev != branch_commit_id:
          orig_date_str = self.get_commit_date(kernel_path, orig_rev)
          new_date_str = self.get_commit_date(kernel_path, branch_commit_id)
          replace_mapping[orig_kernel_version] = {
              'original_revision': orig_rev,
              'new_revision': branch_commit_id,
              'original_date_str': orig_date_str,
              'new_date_str': new_date_str,
          }
          logging.info('Version %s: replace "%s" with "%s"', kernel_version,
                       orig_rev, branch_commit_id)
    return replace_mapping

  def get_commit_date(self, kernel_repo: str, commit_id: str) -> str:
    """Determine date of a given commit.

    Args:
      kernel_repo: Path to repo containing commit id.
      commit_id: Unique id representing a commit in kernel_repo.

    Returns:
      Date of commit.
    """
    if not git.IsSHA1(commit_id):
      logging.warning(
          'Error checking date of "%s": not a valid SHA1, skipping.', commit_id)
      return None
    cmd = [
        'git',
        'show',
        '--no-patch',
        '--no-notes',
        '--pretty=%cd',
        '--date=iso',
        commit_id,
    ]
    return cros_build_lib.run(
        cmd, capture_output=True, encoding='utf-8',
        cwd=kernel_repo).stdout.strip('\n')

  def remove_invalid_revisions(self, replace_mapping: Dict[str, str]):
    """Remove commit id revisions that are invalid by modifying dict.

    Revisions are invalid if the replacement commit id occurred before the
    original commit id.

    Args:
      replace_mapping: Mapping from original to new commit id.
    """
    invalid_revisions = []
    for kernel_version, revisions in replace_mapping.items():
      orig_date_str = revisions['original_date_str']
      new_date_str = revisions['new_date_str']
      orig_date = _parse_iso_date_str(orig_date_str)
      new_date = _parse_iso_date_str(new_date_str)
      if orig_date and new_date and orig_date > new_date:
        kernel_path = self.kernel_repo_path / kernel_version
        logging.warning(
            'Skipping "%s": commit id "%s" (%s) more recent than new commit id '
            '"%s" (%s)', kernel_path, revisions['original_revision'],
            orig_date_str, revisions['new_revision'], new_date_str)
        invalid_revisions.append(kernel_version)
    for rev in invalid_revisions:
      del replace_mapping[rev]

  def pretty_update_xml(self, replace_mapping: Dict[str, str],
                        full_manifest_path: str):
    """Use replace_mapping to update manifest XML retaining formatting.

    Args:
      replace_mapping: Mapping of strings to find -> replace in XML manifest.
      full_manifest_path: Path to XML manifest.
    """
    manifest_str = osutils.ReadFile(full_manifest_path)
    for revisions in replace_mapping.values():
      orig_str = f'revision="{revisions["original_revision"]}"'
      new_str = f'revision="{revisions["new_revision"]}"'
      manifest_str = manifest_str.replace(orig_str, new_str)
    osutils.WriteFile(full_manifest_path, manifest_str)

  def create_cl(self, commit_message: str) -> str:
    """Create and upload a CL in the manifest repo.

    Args:
      commit_message: CL commit message.

    Returns:
      URI of uploaded CL.
    """
    try:
      git.AddPath(self.full_manifest_path)
      git.Commit(self.manifest_repo_path, commit_message)
      git_stdout = git.UploadCL(
          self.manifest_repo_path, 'cros-internal', 'main',
          capture_output=True).stdout
      return uri_lib.ShortenUri(git.GetUrlFromRemoteOutput(git_stdout))
    except cros_build_lib.RunCommandError as e:
      cros_build_lib.Die(f'Error creating CL: {e}')


def get_parser() -> commandline.ArgumentParser:
  """Creates the argparse parser.

  Returns:
    Argument parser.
  """
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument(
      '--release', required=True, help='Release milestone, e.g. R96')
  parser.add_argument(
      '--buildroot',
      default=constants.SOURCE_ROOT,
      type='path',
      help='Path to chromiumos checkout')
  return parser


def parse_args(argv: List[str]) -> commandline.ArgumentNamespace:
  """Parse and validate CLI arguments.

  Args:
    argv: Arguments passed via CLI.

  Returns:
    Validated argument namespace.
  """
  parser = get_parser()
  options = parser.parse_args(argv)
  if not re.match(r'^R[0-9]+$', options.release):
    cros_build_lib.Die(
        'Please provide a release milestone of the format R[release number] '
        'e.g. R96')
  options.buildroot = Path(options.buildroot)
  options.Freeze()
  return options


def main(argv: List[str]) -> Optional[int]:
  options = parse_args(argv)
  lts = LtsKernelUprev(options.release, options.buildroot)

  # Determine branch stem based on kernel repo and release milestone.
  logging.info('Using release "%s" and chromiumos checkout at "%s"',
               lts.release_milestone, lts.buildroot)
  # Ensure kernel refs are up-to-date.
  git.RunGit(lts.kernel_repo_path / 'upstream', ['fetch', 'cros'])
  branch_stem = lts.get_branch_name()
  if not branch_stem:
    cros_build_lib.Die(
        f'Could not determine a branch stem for repo "{lts.kernel_repo_path}" '
        f'and release "{lts.release_milestone}".')
  logging.info('Using branch stem "%s"', branch_stem)

  # Ensure manifest repo is up-to-date.
  git.SyncPushBranch(lts.manifest_repo_path, 'cros-internal',
                     'refs/remotes/cros-internal/main')
  git.RunGit(lts.manifest_repo_path, ['fetch', 'cros-internal'])

  # Read manifest XML.
  try:
    manifest_tree = ET.parse(lts.full_manifest_path)
  except ET.ParseError as e:
    cros_build_lib.Die(f'Error parsing XML: {e}')

  # Find new commit ids for each kernel repo, ensuring they are newer than the
  # existing commit ids.
  replace_mapping = lts.find_new_kernel_commit_ids(branch_stem, manifest_tree)
  lts.remove_invalid_revisions(replace_mapping)

  # Using built-in XML functionality causes formatting changes.
  # Use string.replace to preserve formatting.
  lts.pretty_update_xml(replace_mapping, lts.full_manifest_path)

  # If available, add date details for manifest commit id changes to give
  # context in the CL.
  commit_details = ''
  for kernel_version, revs in replace_mapping.items():
    if revs['original_date_str'] and revs['new_date_str']:
      commit_details += (
          f'\nKernel {kernel_version}: Replaced commit id from '
          f'"{revs["original_date"]}" with commit id from "revs["new_date"]"')
  commit_message = f"""LTS: update kernel commit ids for LTS branches

This CL was created automatically. For more details see go/
chromeos-lts-kernel-uprev.
{commit_details}

BUG=None
TEST=CQ"""

  uploaded_cl_uri = lts.create_cl(commit_message)
  if uploaded_cl_uri:
    logging.info('Successfully uploaded CL: %s', uploaded_cl_uri)
