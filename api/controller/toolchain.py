# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Toolchain-related operations."""

import collections
import logging
import os
from pathlib import Path
import re

from chromite.api import controller
from chromite.api import faux
from chromite.api import validate
from chromite.api.controller import controller_util
from chromite.api.gen.chromite.api import toolchain_pb2
from chromite.api.gen.chromite.api.artifacts_pb2 import PrepareForBuildResponse
from chromite.api.gen.chromiumos.builder_config_pb2 import BuilderConfig
from chromite.lib import chroot_util
from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import toolchain_util


if cros_build_lib.IsInsideChroot():
  # Only used for linting in chroot and requires yaml which is only in chroot
  from chromite.scripts import tricium_cargo_clippy
  from chromite.scripts import tricium_clang_tidy


_Handlers = collections.namedtuple('_Handlers', ['name', 'prepare', 'bundle'])
_TOOLCHAIN_ARTIFACT_HANDLERS = {
    BuilderConfig.Artifacts.UNVERIFIED_CHROME_LLVM_ORDERFILE:
        _Handlers('UnverifiedChromeLlvmOrderfile',
                  toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.VERIFIED_CHROME_LLVM_ORDERFILE:
        _Handlers('VerifiedChromeLlvmOrderfile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.CHROME_CLANG_WARNINGS_FILE:
        _Handlers('ChromeClangWarningsFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.UNVERIFIED_LLVM_PGO_FILE:
        _Handlers('UnverifiedLlvmPgoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.UNVERIFIED_CHROME_BENCHMARK_AFDO_FILE:
        _Handlers('UnverifiedChromeBenchmarkAfdoFile',
                  toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.CHROME_DEBUG_BINARY:
        _Handlers('ChromeDebugBinary', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.UNVERIFIED_CHROME_BENCHMARK_PERF_FILE:
        _Handlers('UnverifiedChromeBenchmarkPerfFile',
                  toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.VERIFIED_CHROME_BENCHMARK_AFDO_FILE:
        _Handlers('VerifiedChromeBenchmarkAfdoFile',
                  toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.UNVERIFIED_KERNEL_CWP_AFDO_FILE:
        _Handlers('UnverifiedKernelCwpAfdoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.VERIFIED_KERNEL_CWP_AFDO_FILE:
        _Handlers('VerifiedKernelCwpAfdoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.UNVERIFIED_CHROME_CWP_AFDO_FILE:
        _Handlers('UnverifiedChromeCwpAfdoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.VERIFIED_CHROME_CWP_AFDO_FILE:
        _Handlers('VerifiedChromeCwpAfdoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.VERIFIED_RELEASE_AFDO_FILE:
        _Handlers('VerifiedReleaseAfdoFile', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.TOOLCHAIN_WARNING_LOGS:
        _Handlers('ToolchainWarningLogs', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.CHROME_AFDO_PROFILE_FOR_ANDROID_LINUX:
        _Handlers('ChromeAFDOProfileForAndroidLinux',
                  toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.CLANG_CRASH_DIAGNOSES:
        _Handlers('ClangCrashDiagnoses', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
    BuilderConfig.Artifacts.COMPILER_RUSAGE_LOG:
        _Handlers('CompilerRusageLogs', toolchain_util.PrepareForBuild,
                  toolchain_util.BundleArtifacts),
}

_TOOLCHAIN_COMMIT_HANDLERS = {
    BuilderConfig.Artifacts.VERIFIED_KERNEL_CWP_AFDO_FILE:
        'VerifiedKernelCwpAfdoFile'
}

TIDY_BASE_DIR = Path('/tmp/linting_output/clang-tidy')


def _GetProfileInfoDict(profile_info):
  """Convert profile_info to a dict.

  Args:
    profile_info (ArtifactProfileInfo): The artifact profile_info.

  Returns:
    A dictionary containing profile info.
  """
  ret = {}
  which = profile_info.WhichOneof('artifact_profile_info')
  if which:
    value = getattr(profile_info, which)
    # If it is a message, then use the contents of the message.  This works as
    # long as simple types do not have a 'DESCRIPTOR' attribute. (And protobuf
    # messages do.)
    if getattr(value, 'DESCRIPTOR', None):
      ret.update({k.name: v for k, v in value.ListFields()})
    else:
      ret[which] = value
  return ret


# TODO(crbug/1031213): When @faux is expanded to have more than success/failure,
# this should be changed.
@faux.all_empty
@validate.require('artifact_types')
# Note: chroot and sysroot are unspecified the first time that the build_target
# recipe calls PrepareForBuild.  The second time, they are specified.  No
# validation check because "all" values are valid.
@validate.validation_complete
def PrepareForBuild(input_proto, output_proto, _config):
  """Prepare to build toolchain artifacts.

  The handlers (from _TOOLCHAIN_ARTIFACT_HANDLERS above) are called with:
      artifact_name (str): name of the artifact type.
      chroot (chroot_lib.Chroot): chroot.  Will be None if the chroot has not
          yet been created.
      sysroot_path (str): sysroot path inside the chroot (e.g., /build/atlas).
          Will be an empty string if the sysroot has not yet been created.
      build_target_name (str): name of the build target (e.g., atlas).  Will be
          an empty string if the sysroot has not yet been created.
      input_artifacts ({(str) name:[str gs_locations]}): locations for possible
          input artifacts.  The handler is expected to know which keys it should
          be using, and ignore any keys that it does not understand.
      profile_info ({(str) name: (str) value}) Dictionary containing profile
          information.

  They locate and modify any ebuilds and/or source required for the artifact
  being created, then return a value from toolchain_util.PrepareForBuildReturn.

  This function sets output_proto.build_relevance to the result.

  Args:
    input_proto (PrepareForToolchainBuildRequest): The input proto
    output_proto (PrepareForToolchainBuildResponse): The output proto
    _config (api_config.ApiConfig): The API call config.
  """
  if input_proto.chroot.path:
    chroot = controller_util.ParseChroot(input_proto.chroot)
  else:
    chroot = None

  input_artifacts = collections.defaultdict(list)
  for art in input_proto.input_artifacts:
    item = _TOOLCHAIN_ARTIFACT_HANDLERS.get(art.input_artifact_type)
    if item:
      input_artifacts[item.name].extend(
          ['gs://%s' % str(x) for x in art.input_artifact_gs_locations])

  profile_info = _GetProfileInfoDict(input_proto.profile_info)

  results = set()
  sysroot_path = input_proto.sysroot.path
  build_target = input_proto.sysroot.build_target.name
  for artifact_type in input_proto.artifact_types:
    # Unknown artifact_types are an error.
    handler = _TOOLCHAIN_ARTIFACT_HANDLERS[artifact_type]
    if handler.prepare:
      results.add(
          handler.prepare(handler.name, chroot, sysroot_path, build_target,
                          input_artifacts, profile_info))

  # Translate the returns from the handlers we called.
  #   If any NEEDED => NEEDED
  #   elif any UNKNOWN => UNKNOWN
  #   elif any POINTLESS => POINTLESS
  #   else UNKNOWN.
  if toolchain_util.PrepareForBuildReturn.NEEDED in results:
    output_proto.build_relevance = PrepareForBuildResponse.NEEDED
  elif toolchain_util.PrepareForBuildReturn.UNKNOWN in results:
    output_proto.build_relevance = PrepareForBuildResponse.UNKNOWN
  elif toolchain_util.PrepareForBuildReturn.POINTLESS in results:
    output_proto.build_relevance = PrepareForBuildResponse.POINTLESS
  else:
    output_proto.build_relevance = PrepareForBuildResponse.UNKNOWN
  return controller.RETURN_CODE_SUCCESS


# TODO(crbug/1031213): When @faux is expanded to have more than success/failure,
# this should be changed.
@faux.all_empty
@validate.require('chroot.path', 'output_dir', 'artifact_types')
@validate.exists('output_dir')
@validate.validation_complete
def BundleArtifacts(input_proto, output_proto, _config):
  """Bundle valid toolchain artifacts.

  The handlers (from _TOOLCHAIN_ARTIFACT_HANDLERS above) are called with:
      artifact_name (str): name of the artifact type
      chroot (chroot_lib.Chroot): chroot
      sysroot_path (str): sysroot path inside the chroot (e.g., /build/atlas),
          or None.
      chrome_root (str): path to chrome root. (e.g., /b/s/w/ir/k/chrome)
      build_target_name (str): name of the build target (e.g., atlas), or None.
      output_dir (str): absolute path where artifacts are being bundled.
        (e.g., /b/s/w/ir/k/recipe_cleanup/artifactssptfMU)
      profile_info ({(str) name: (str) value}) Dictionary containing profile
          information.

  Note: the actual upload to GS is done by CI, not here.

  Args:
    input_proto (BundleToolchainRequest): The input proto
    output_proto (BundleToolchainResponse): The output proto
    _config (api_config.ApiConfig): The API call config.
  """
  chroot = controller_util.ParseChroot(input_proto.chroot)

  profile_info = _GetProfileInfoDict(input_proto.profile_info)

  output_path = Path(input_proto.output_dir)

  for artifact_type in input_proto.artifact_types:
    if artifact_type not in _TOOLCHAIN_ARTIFACT_HANDLERS:
      logging.error('%s not understood', artifact_type)
      return controller.RETURN_CODE_UNRECOVERABLE

    handler = _TOOLCHAIN_ARTIFACT_HANDLERS[artifact_type]
    if not handler or not handler.bundle:
      logging.warning('%s does not have a handler with a bundle function.',
                      artifact_type)
      continue

    artifacts = handler.bundle(handler.name, chroot, input_proto.sysroot.path,
                               input_proto.sysroot.build_target.name,
                               input_proto.output_dir, profile_info)
    if not artifacts:
      continue

    # Filter out artifacts that do not exist or are empty.
    usable_artifacts = []
    for artifact in artifacts:
      artifact_path = output_path / artifact
      if not artifact_path.exists():
        logging.warning('%s is not in the output directory.', artifact)
      elif not artifact_path.stat().st_size:
        logging.warning('%s is empty.', artifact)
      else:
        usable_artifacts.append(artifact)

    if not usable_artifacts:
      logging.warning('No usable artifacts for artifact type %s', artifact_type)
      continue

    # Add all usable artifacts.
    art_info = output_proto.artifacts_info.add()
    art_info.artifact_type = artifact_type
    for artifact in usable_artifacts:
      art_info.artifacts.add().path = artifact


def _GetUpdatedFilesResponse(_input_proto, output_proto, _config):
  """Add successful status to the faux response."""
  file_info = output_proto.updated_files.add()
  file_info.path = '/any/modified/file'
  output_proto.commit_message = 'Commit message'


@faux.empty_error
@faux.success(_GetUpdatedFilesResponse)
@validate.require('uploaded_artifacts')
@validate.validation_complete
def GetUpdatedFiles(input_proto, output_proto, _config):
  """Use uploaded artifacts to update some updates in a chromeos checkout.

  The function will call toolchain_util.GetUpdatedFiles using the type of
  uploaded artifacts to make some changes in a checkout, and return the list
  of change files together with commit message.
     updated_artifacts: A list of UpdatedArtifacts type which contains a tuple
        of artifact info and profile info.
  Note: the actual creation of the commit is done by CI, not here.

  Args:
    input_proto (GetUpdatedFilesRequest): The input proto
    output_proto (GetUpdatedFilesResponse): The output proto
    _config (api_config.ApiConfig): The API call config.
  """
  commit_message = ''
  for artifact in input_proto.uploaded_artifacts:
    artifact_type = artifact.artifact_info.artifact_type
    if artifact_type not in _TOOLCHAIN_COMMIT_HANDLERS:
      logging.error('%s not understood', artifact_type)
      return controller.RETURN_CODE_UNRECOVERABLE
    artifact_name = _TOOLCHAIN_COMMIT_HANDLERS[artifact_type]
    if artifact_name:
      assert len(artifact.artifact_info.artifacts) == 1, (
          'Only one file to update per each artifact')
      updated_files, message = toolchain_util.GetUpdatedFiles(
          artifact_name, artifact.artifact_info.artifacts[0].path,
          _GetProfileInfoDict(artifact.profile_info))
      for f in updated_files:
        file_info = output_proto.updated_files.add()
        file_info.path = f

      commit_message += message + '\n'
    output_proto.commit_message = commit_message
    # No commit footer is added for now. Can add more here if needed


@faux.all_empty
@validate.exists('sysroot.path')
@validate.require('packages')
@validate.validation_complete
def EmergeWithLinting(input_proto, output_proto, _config):
  """Emerge packages with linter features enabled and retrieves all findings.

  Args:
    input_proto (LinterRequest): The nput proto with package and sysroot info.
    output_proto (LinterResponse): The output proto where findings are stored.
    _config (api_config.ApiConfig): The API call config (unused).
  """
  packages = [
      f'{package.category}/{package.package_name}'
      for package in input_proto.packages]

  # rm any existing lints from clang tidy
  osutils.RmDir(TIDY_BASE_DIR, ignore_missing=True, sudo=True)
  osutils.SafeMakedirs(TIDY_BASE_DIR, 0o777, sudo=True)

  # rm any existing temporary portage files from builds of affected packages:
  # this is required to make sure lints are always regenerated
  for package in packages:
    cache_files_dir = f'{input_proto.sysroot.path}/var/cache/portage/{package}'
    osutils.RmDir(cache_files_dir, ignore_missing=True)

  emerge_cmd = chroot_util.GetEmergeCommand(input_proto.sysroot.path)
  cros_build_lib.sudo_run(
      emerge_cmd + packages,
      preserve_env=True,
      extra_env={
          'ENABLE_RUST_CLIPPY': 1,
          'WITH_TIDY': 'tricium',
          'FEATURES': 'noclean'
      }
  )

  # FIXME(b/195056381): default git-repo should be replaced with logic in
  # build_linters recipe to detect the repo path for applied patches.
  # As of 01-05-21 only platform2 is supported so this value works temporarily.
  git_repo_path = '/mnt/host/source/src/platform2/'

  linter_findings = _fetch_clippy_lints(git_repo_path)
  linter_findings.extend(_fetch_tidy_lints(git_repo_path))

  if input_proto.filter_modified:
    linter_findings = _filter_linter_findings(linter_findings, git_repo_path)

  output_proto.findings.extend(linter_findings)


LINTER_CODES = {
    'clang_tidy': toolchain_pb2.LinterFinding.CLANG_TIDY,
    'cargo_clippy': toolchain_pb2.LinterFinding.CARGO_CLIPPY
}


def _filter_linter_findings(findings, git_repo_path):
  """Filters findings to keep only those concerning modified lines."""
  new_findings = []
  new_lines = _get_added_lines({git_repo_path: 'HEAD'})
  for finding in findings:
    for loc in finding.locations:
      for (addition_start, addition_end) in new_lines.get(loc.filepath, set()):
        if addition_start <= loc.line_start < addition_end:
          new_findings.append(finding)
  return new_findings


def _get_added_lines(git_repos):
  """Parses the lines with additions from fit diff for the provided repos.

  Args:
    git_repos: a dictionary mapping repo paths to hashes for `git diff`

  Returns:
    A dictionary mapping modified filepaths to sets of tuples where each
    tuple is a (start_line, end_line) pair noting which lines were modified.
    Note that start_line is inclusive, and end_line is exclusive.
  """
  new_lines = {}
  file_path_pattern = re.compile(r'^\+\+\+ b/(?P<file_path>.*)$')
  position_pattern = re.compile(
      r'^@@ -\d+(?:,\d+)? \+(?P<line_num>\d+)(?:,(?P<lines_added>\d+))? @@')
  for git_repo, git_hash in git_repos.items():
    cmd = f'git -C {git_repo} diff -U0 {git_hash}^...{git_hash}'
    diff = cros_build_lib.run(cmd, capture_output=True, shell=True,
                              encoding='utf-8').output
    current_file = ''
    for line in diff.splitlines():
      file_path_match = re.match(file_path_pattern, str(line))
      if file_path_match:
        current_file = file_path_match.group('file_path')
        continue
      position_match = re.match(position_pattern, str(line))
      if position_match:
        if current_file not in new_lines:
          new_lines[current_file] = set()
        line_num = int(position_match.group('line_num'))
        line_count = position_match.group('lines_added')
        line_count = int(line_count) if line_count is not None else 1
        new_lines[current_file].add((line_num, line_num + line_count))
  return new_lines


def _fetch_clippy_lints(git_repo_path):
  """Get lints created by Cargo Clippy during emerge."""
  lints_dir = '/tmp/cargo_clippy'
  findings = tricium_cargo_clippy.parse_files(lints_dir, git_repo_path)
  findings = tricium_cargo_clippy.filter_diagnostics(findings)
  findings_protos = []
  for finding in findings:
    location_protos = []
    for location in finding.locations:
      location_protos.append(
          toolchain_pb2.LinterFindingLocation(
              filepath=location.file_path,
              line_start=location.line_start,
              line_end=location.line_end
          )
      )
    findings_protos.append(
        toolchain_pb2.LinterFinding(
            message=finding.message,
            locations=location_protos,
            linter=LINTER_CODES['cargo_clippy']
        )
    )
  return findings_protos


def _fetch_tidy_lints(git_repo_path):
  """Get lints created by Clang Tidy during emerge."""

  def resolve_file_path(file_path):
    # Remove git repo from prefix
    file_path = re.sub('^' + git_repo_path, '/', str(file_path))
    # Remove ebuild work directories from prefix
    # Such as: "**/<package>-9999/work/<package>-9999/"
    #      or: "**/<package>-0.24.52-r9/work/<package>-0.24.52/"
    return re.sub(r'(.*/)?([^/]+)-[^/]+/work/[^/]+/+', '', file_path)

  lints = set()
  for filename in os.listdir(TIDY_BASE_DIR):
    if filename.endswith('.json'):
      invocation_result = tricium_clang_tidy.parse_tidy_invocation(
          TIDY_BASE_DIR / filename)
      meta, complaints = invocation_result
      assert not meta.exit_code, (
          f'Invoking clang-tidy on {meta.lint_target} with flags '
          f'{meta.invocation} exited with code {meta.exit_code}; '
          f'output:\n{meta.stdstreams}')
      lints.update(complaints)
  return [
      toolchain_pb2.LinterFinding(
          message=lint.message,
          locations=[
              toolchain_pb2.LinterFindingLocation(
                  filepath=resolve_file_path(lint.file_path),
                  line_start=lint.line_number,
                  line_end=lint.line_number
              )
          ],
          linter=LINTER_CODES['clang_tidy']
      )
      for lint in tricium_clang_tidy.filter_tidy_lints(None, None, lints)
  ]
