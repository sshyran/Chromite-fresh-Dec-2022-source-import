# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test service.

Handles test related functionality.
"""
import json
import logging
import os
import shutil
import traceback
from typing import Dict, Iterable, List, NamedTuple, Optional, TYPE_CHECKING

from chromite.cbuildbot import commands
from chromite.lib import autotest_util
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.lib import path_util
from chromite.lib import portage_util
from chromite.utils import code_coverage_util


if TYPE_CHECKING:
  from chromite.lib import build_target_lib
  from chromite.lib import chroot_lib
  from chromite.lib import goma_lib
  from chromite.lib import sysroot_lib
  from chromite.lib.parser import package_info

CHROMITE_UTILS_PATH = 'chromite/utils/data'
COVERAGE_BOARD_OWNERSHIP_JSON = 'code_coverage_board_ownership.json'


class Error(Exception):
  """The module's base error class."""


class NoFilesError(Error):
  """When there are no files to archive."""


class BuildTargetUnitTestResult(object):
  """Result value object."""

  def __init__(self, return_code: int,
               failed_pkgs: Optional[Iterable['package_info.PackageInfo']]):
    """Init method.

    Args:
      return_code: The return code from the command execution.
      failed_pkgs: List of packages whose tests failed.
    """
    self.return_code = return_code
    self.failed_pkgs = failed_pkgs or []

  @property
  def success(self):
    return self.return_code == 0 and len(self.failed_pkgs) == 0


def BuildTargetUnitTest(build_target: 'build_target_lib.BuildTarget',
                        packages: Optional[List[str]] = None,
                        blocklist: Optional[List[str]] = None,
                        was_built: bool = True,
                        code_coverage: bool = False,
                        testable_packages_optional: bool = False,
                        filter_only_cros_workon: bool = False
                       ) -> BuildTargetUnitTestResult:
  """Run the ebuild unit tests for the target.

  Args:
    build_target: The build target.
    packages: Packages to be tested. If none, uses all testable packages.
    blocklist: Tests to skip.
    was_built: Whether packages were built.
    code_coverage: Whether to produce code coverage data.
    testable_packages_optional: Whether to allow no testable packages to be
      found.
    filter_only_cros_workon: Whether to filter out non-cros_workon packages from
      input package list.

  Returns:
    BuildTargetUnitTestResult
  """
  cros_build_lib.AssertInsideChroot()
  # TODO(saklein) Refactor commands.RunUnitTests to use this/the API.
  # TODO(crbug.com/960805) Move cros_run_unit_tests logic here.
  cmd = ['cros_run_unit_tests']

  if build_target.is_host():
    cmd.extend(['--host'])
  else:
    cmd.extend(['--board', build_target.name])

  if packages:
    cmd.extend(['--packages', ' '.join(packages)])

  if blocklist:
    cmd.extend(['--skip-packages', ' '.join(blocklist)])

  if filter_only_cros_workon:
    cmd.append('--filter-only-cros-workon')

  if testable_packages_optional:
    cmd.append('--no-testable-packages-ok')

  if not was_built:
    cmd.append('--assume-empty-sysroot')

  extra_env = {}
  if code_coverage:
    use_flags = os.environ.get('USE', '').split()
    if 'coverage' not in use_flags:
      use_flags.append('coverage')
    extra_env['USE'] = ' '.join(use_flags)

  # Set up the failed package status file.
  with osutils.TempDir() as tempdir:
    extra_env[constants.CROS_METRICS_DIR_ENVVAR] = tempdir

    result = cros_build_lib.run(
        cmd,
        extra_env=extra_env,
        check=False)

    failed_pkgs = portage_util.ParseDieHookStatusFile(tempdir)

  return BuildTargetUnitTestResult(result.returncode, failed_pkgs)


def BundleHwqualTarball(board: str, version: str, chroot: 'chroot_lib.Chroot',
                        sysroot: 'sysroot_lib.Sysroot',
                        result_path: str) -> Optional[str]:
  """Build the hwqual tarball.

  Args:
    board: The board name.
    version: The version string to use for the image.
    chroot: Chroot where the tests were run.
    sysroot: The sysroot where the tests were run.
    result_path: The directory where the archive should be created.

  Returns:
    The output path or None.
  """
  # Create an autotest.tar.bz2 file to pass to archive_hwqual

  # archive_basedir is the base directory where the archive commands are run.
  # We want the folder containing the board's autotest folder.
  archive_basedir = chroot.full_path(sysroot.path,
                                     constants.AUTOTEST_BUILD_PATH)
  archive_basedir = os.path.dirname(archive_basedir)

  if not os.path.exists(archive_basedir):
    logging.warning('%s does not exist, not creating hwqual', archive_basedir)
    return None

  with chroot.tempdir() as autotest_bundle_dir:
    if not autotest_util.AutotestTarballBuilder(archive_basedir,
                                                autotest_bundle_dir):
      logging.warning('could not create autotest bundle, not creating hwqual')
      return None

    image_dir = image_lib.GetLatestImageLink(board)
    ssh_private_key = os.path.join(image_dir, constants.TEST_KEY_PRIVATE)

    output_tag = 'chromeos-hwqual-%s-%s' % (board, version)

    script_dir = os.path.join(constants.SOURCE_ROOT, 'src', 'platform',
                              'crostestutils')
    cmd = [
        os.path.join(script_dir, 'archive_hwqual'), '--from',
        autotest_bundle_dir, '--to', result_path, '--image_dir', image_dir,
        '--ssh_private_key', ssh_private_key, '--output_tag', output_tag
    ]

    cros_build_lib.run(cmd)

  artifact_path = os.path.join(result_path, '%s.tar.bz2' % output_tag)
  if not os.path.exists(artifact_path):
    return None
  return artifact_path


def DebugInfoTest(sysroot_path: str) -> bool:
  """Run the debug info tests.

  Args:
    sysroot_path: The sysroot being tested.

  Returns:
    True iff all tests passed, False otherwise.
  """
  cmd = ['debug_info_test', os.path.join(sysroot_path, 'usr/lib/debug')]
  result = cros_build_lib.run(cmd, enter_chroot=True, check=False)

  return result.returncode == 0


def ChromiteUnitTest() -> bool:
  """Run chromite unittests.

  Returns:
    True iff all tests passed, False otherwise.
  """
  cmd = [
      os.path.join(constants.CHROMITE_DIR, 'run_tests'),
      constants.CHROMITE_DIR,
  ]
  result = cros_build_lib.run(cmd, check=False)
  return result.returncode == 0


def RulesCrosUnitTest() -> bool:
  """Run rules_cros unittests.

  Returns:
    True iff all tests passed, False otherwise.
  """
  cmd = [
      os.path.join(constants.RULES_CROS_PATH, 'run_tests.sh'),
  ]
  result = cros_build_lib.run(cmd, enter_chroot=True, check=False)

  return result.returncode == 0


def SimpleChromeWorkflowTest(sysroot_path: str, build_target_name: str,
                             chrome_root: str,
                             goma: Optional['goma_lib.Goma']) -> None:
  """Execute SimpleChrome workflow tests

  Args:
    sysroot_path: The sysroot path for testing Chrome.
    build_target_name: Board build target
    chrome_root: Path to Chrome source root.
    goma: Goma object or None.
  """
  board_dir = 'out_%s' % build_target_name

  out_board_dir = os.path.join(chrome_root, board_dir, 'Release')
  use_goma = goma is not None
  extra_args = []

  with osutils.TempDir(prefix='chrome-sdk-cache') as tempdir:
    sdk_cmd = _InitSimpleChromeSDK(tempdir, build_target_name, sysroot_path,
                                   chrome_root, use_goma)

    if goma:
      extra_args.extend(['--nostart-goma', '--gomadir', goma.linux_goma_dir])

    _BuildChrome(sdk_cmd, chrome_root, out_board_dir, goma)
    _TestDeployChrome(sdk_cmd, out_board_dir)
    _VMTestChrome(build_target_name, sdk_cmd)


def _InitSimpleChromeSDK(tempdir: str, build_target_name: str,
                         sysroot_path: str, chrome_root: str,
                         use_goma: bool) -> commands.ChromeSDK:
  """Create ChromeSDK object for executing 'cros chrome-sdk' commands.

  Args:
    tempdir: Tempdir for command execution.
    build_target_name: Board build target.
    sysroot_path: Sysroot for Chrome to use.
    chrome_root: Path to Chrome.
    use_goma: Whether to use goma.

  Returns:
    A ChromeSDK object.
  """
  extra_args = ['--cwd', chrome_root, '--sdk-path', sysroot_path]
  cache_dir = os.path.join(tempdir, 'cache')

  sdk_cmd = commands.ChromeSDK(
      constants.SOURCE_ROOT,
      build_target_name,
      chrome_src=chrome_root,
      goma=use_goma,
      extra_args=extra_args,
      cache_dir=cache_dir)
  return sdk_cmd


def _VerifySDKEnvironment(out_board_dir: str) -> None:
  """Make sure the SDK environment is set up properly.

  Args:
    out_board_dir: Output SDK dir for board.
  """
  if not os.path.exists(out_board_dir):
    raise AssertionError('%s not created!' % out_board_dir)
  logging.info('ARGS.GN=\n%s',
               osutils.ReadFile(os.path.join(out_board_dir, 'args.gn')))


def _BuildChrome(sdk_cmd: commands.ChromeSDK, chrome_root: str,
                 out_board_dir: str, goma: Optional['goma_lib.Goma']) -> None:
  """Build Chrome with SimpleChrome environment.

  Args:
    sdk_cmd: sdk_cmd to run cros chrome-sdk commands.
    chrome_root: Path to Chrome.
    out_board_dir: Path to board directory.
    goma: Goma object or None
  """
  # Validate fetching of the SDK and setting everything up.
  sdk_cmd.Run(['true'])

  sdk_cmd.Run(['gclient', 'runhooks'])

  # Generate args.gn and ninja files.
  gn_cmd = os.path.join(chrome_root, 'buildtools', 'linux64', 'gn')
  gn_gen_cmd = '%s gen "%s" --args="$GN_ARGS"' % (gn_cmd, out_board_dir)
  sdk_cmd.Run(['bash', '-c', gn_gen_cmd])

  _VerifySDKEnvironment(out_board_dir)

  if goma:
    # If goma is enabled, start goma compiler_proxy here, and record
    # several information just before building Chrome is started.
    goma.Start()
    extra_env = goma.GetExtraEnv()
    ninja_env_path = os.path.join(goma.goma_log_dir, 'ninja_env')
    sdk_cmd.Run(['env', '--null'],
                run_args={
                    'extra_env': extra_env,
                    'stdout': ninja_env_path
                })
    osutils.WriteFile(os.path.join(goma.goma_log_dir, 'ninja_cwd'), sdk_cmd.cwd)
    osutils.WriteFile(
        os.path.join(goma.goma_log_dir, 'ninja_command'),
        cros_build_lib.CmdToStr(sdk_cmd.GetNinjaCommand()))
  else:
    extra_env = None

  result = None
  try:
    # Build chromium.
    result = sdk_cmd.Ninja(run_args={'extra_env': extra_env})
  finally:
    # In teardown, if goma is enabled, stop the goma compiler proxy,
    # and record/copy some information to log directory, which will be
    # uploaded to the goma's server in a later stage.
    if goma:
      goma.Stop()
      ninja_log_path = os.path.join(chrome_root, sdk_cmd.GetNinjaLogPath())
      if os.path.exists(ninja_log_path):
        shutil.copy2(ninja_log_path, os.path.join(goma.goma_log_dir,
                                                  'ninja_log'))
      if result:
        osutils.WriteFile(
            os.path.join(goma.goma_log_dir, 'ninja_exit'),
            str(result.returncode))


def _TestDeployChrome(sdk_cmd: commands.ChromeSDK, out_board_dir: str) -> None:
  """Test SDK deployment.

  Args:
    sdk_cmd: sdk_cmd to run cros chrome-sdk commands.
    out_board_dir: Path to board directory.
  """
  with osutils.TempDir(prefix='chrome-sdk-stage') as tempdir:
    # Use the TOT deploy_chrome.
    script_path = os.path.join(constants.SOURCE_ROOT,
                               constants.CHROMITE_BIN_SUBDIR, 'deploy_chrome')
    sdk_cmd.Run([
        script_path, '--build-dir', out_board_dir, '--staging-only',
        '--staging-dir', tempdir
    ])
    # Verify chrome is deployed.
    chromepath = os.path.join(tempdir, 'chrome')
    if not os.path.exists(chromepath):
      raise AssertionError(
          'deploy_chrome did not run successfully! Searched %s' % (chromepath))


def _VMTestChrome(board: str, sdk_cmd: commands.ChromeSDK) -> None:
  """Run cros_run_test.

  Args:
    board: The name of the board.
    sdk_cmd: sdk_cmd to run cros chrome-sdk commands.
  """
  image_dir_symlink = image_lib.GetLatestImageLink(board)
  image_path = os.path.join(image_dir_symlink, constants.VM_IMAGE_BIN)

  # Run VM test for boards where we've built a VM.
  if image_path and os.path.exists(image_path):
    sdk_cmd.VMTest(image_path)

def _GetZeroCoverageDirectories(
    build_target: 'build_target_lib.BuildTarget') -> List[str]:
  """Get the list of directories to generate zero coverage for.

  Args:
    build_target: The build target we want to choose directories for.

  Returns:
    List of directories that we should generate zero coverage for.
  """
  # TODO(b/244365763): Get this mapping dynamically instead of the static json.
  owners_path = os.path.join(
      constants.SOURCE_ROOT, CHROMITE_UTILS_PATH, COVERAGE_BOARD_OWNERSHIP_JSON)
  if not os.path.exists(owners_path):
    raise ValueError('Coverage boards ownership json does not'
                     f'exists {owners_path}')

  content = osutils.ReadFile(owners_path)
  owners_json = json.loads(content)
  if not owners_json:
    raise ValueError(f'Could not read board ownership json {owners_path}')

  if owners_json[build_target] is None:
    raise ValueError(f'No ownership data found for {build_target}'
                     f'at {owners_path}')

  dirs = [
      os.path.join(constants.SOURCE_ROOT, d)
      for d in owners_json[build_target]]
  return dirs

def BundleCodeCoverageLlvmJson(build_target: 'build_target_lib.BuildTarget',
                               chroot: 'chroot_lib.Chroot',
                               sysroot_class: 'sysroot_lib.Sysroot',
                               output_dir: str) -> Optional[str]:
  """Bundle code coverage llvm json into a tarball for importing into GCE.

  Args:
    build_target: The build target.
    chroot: The chroot class used for these artifacts.
    sysroot_class: The sysroot class used for these artifacts.
    output_dir: The path to write artifacts to.

  Returns:
    A string path to the output code_coverage.tar.xz artifact, or None.
  """

  try:
    base_path = chroot.full_path(sysroot_class.path)

    # Gather all LLVM compiler generated coverage data into single coverage.json
    coverage_dir = os.path.join(base_path, 'build/coverage_data')
    coverage_dir = path_util.FromChrootPath(coverage_dir)

    llvm_generated_cov_json = GatherCodeCoverageLlvmJsonFile(
        coverage_dir)

    llvm_generated_cov_json = (
        code_coverage_util.GetLLVMCoverageWithFilesExcluded(
            llvm_generated_cov_json,
            constants.ZERO_COVERAGE_EXCLUDE_FILES_SUFFIXES))
    search_directory = os.path.join(base_path,
                                    'var/lib/chromeos/package-artifacts')
    search_directory = path_util.FromChrootPath(search_directory)
    path_mapping = code_coverage_util.GatherPathMapping(search_directory)

    cleaned_cov_json = code_coverage_util.CleanLlvmFileNames(
        coverage_json=llvm_generated_cov_json,
        source_root=constants.SOURCE_ROOT,
        path_mapping_list=path_mapping)

    code_coverage_util.LogLlvmCoverageJsonInformation(
        cleaned_cov_json,
        'LLVM generated coverage after files cleaned:')

    # Generate zero coverage for all src files, excluding those which are
    # already present in cleaned_cov_json.
    files_with_cov = code_coverage_util.ExtractFilenames(
        cleaned_cov_json)
    zero_coverage_json = code_coverage_util.GenerateZeroCoverageLlvm(
        # TODO(b/227649725): Input path_to_src_directories and language specific
        # src_file_extensions and exclude_line_prefixes from GetArtifact API
        path_to_src_directories=_GetZeroCoverageDirectories(
            build_target=build_target),
        src_file_extensions=constants.ZERO_COVERAGE_FILE_EXTENSIONS_TO_PROCESS,
        exclude_line_prefixes=constants.ZERO_COVERAGE_EXCLUDE_LINE_PREFIXES,
        exclude_files=files_with_cov,
        exclude_files_suffixes=constants.ZERO_COVERAGE_EXCLUDE_FILES_SUFFIXES,
        src_prefix_path=constants.SOURCE_ROOT)

    code_coverage_util.LogLlvmCoverageJsonInformation(
        zero_coverage_json,
        'Zero coverage files:')

    # Merge generated zero coverage data and
    # llvm compiler generated coverage data.
    merged_coverage_json = code_coverage_util.MergeLLVMCoverageJson(
        cleaned_cov_json, zero_coverage_json)
    code_coverage_util.LogLlvmCoverageJsonInformation(
        merged_coverage_json,
        'merged_coverage_json:')
    with osutils.TempDir() as dest_tmpdir:
      osutils.WriteFile(
          os.path.join(dest_tmpdir, constants.CODE_COVERAGE_LLVM_FILE_NAME),
          json.dumps(merged_coverage_json))

      tarball_path = os.path.join(output_dir,
                                  constants.CODE_COVERAGE_LLVM_JSON_SYMBOLS_TAR)
      result = cros_build_lib.CreateTarball(tarball_path, dest_tmpdir)
      if result.returncode != 0:
        logging.error('Error (%d) when creating tarball %s from %s',
                      result.returncode, tarball_path, dest_tmpdir)
        return None
      return tarball_path

  except Exception as e:
    logging.error(traceback.format_exc())
    logging.error('BundleCodeCoverageLlvmJson failed %s', e)
    return None


class GatherCodeCoverageLlvmJsonFileResult(NamedTuple):
  """Class containing result data of GatherCodeCoverageLlvmJsonFile."""
  coverage_json: Dict


def GatherCodeCoverageLlvmJsonFile(path: str):
  """Locate code coverage llvm json files in |path|.

   This function locates all the coverage llvm json files and merges them
   into one file, in the correct llvm json format.

  Args:
    path: The input path to walk.

  Returns:
    Code coverage json llvm format.
  """
  joined_file_paths = []
  coverage_data = []
  if not os.path.exists(path):
    # Builder might only build packages that does not have
    # unit test setup,therefore there will be no
    # coverage_data to gather.
    logging.info('The path does not exists %s. Returning empty coverage.',
                 path)
    return code_coverage_util.CreateLlvmCoverageJson(coverage_data)
  if not os.path.isdir(path):
    raise ValueError('The path is not a directory: ', path)

  for root, _, files in os.walk(path):
    for f in files:
      # Make sure the file contents match the llvm json format.
      path_to_file = os.path.join(root, f)
      file_data = code_coverage_util.GetLlvmJsonCoverageDataIfValid(
          path_to_file)
      if file_data is None:
        continue

      # Copy over data from this file.
      joined_file_paths.append(path_to_file)
      for datum in file_data['data']:
        for file_data in datum['files']:
          coverage_data.append(file_data)

  return code_coverage_util.CreateLlvmCoverageJson(coverage_data)


def FindAllMetadataFiles(chroot: 'chroot_lib.Chroot',
                         sysroot: 'sysroot_lib.Sysroot') -> List[str]:
  """Find the full paths to all test metadata paths."""
  # Right now there's no use case for this function inside the chroot.
  # If it's useful, we could make the chroot param optional to run in the SDK.
  cros_build_lib.AssertOutsideChroot()
  return [
      _FindAutotestMetadataFile(chroot, sysroot),
      _FindTastLocalMetadataFile(chroot, sysroot),
      _FindTastLocalPrivateMetadataFile(chroot, sysroot),
      _FindTastRemoteMetadataFile(chroot),
  ]


def _FindAutotestMetadataFile(chroot: 'chroot_lib.Chroot',
                              sysroot: 'sysroot_lib.Sysroot') -> str:
  """Find the full path to the Autotest test metadata file.

  This file is installed during the chromeos-base/autotest ebuild.
  """
  return chroot.full_path(
      sysroot.Path('usr', 'local', 'build', 'autotest', 'autotest_metadata.pb'))


def _FindTastLocalMetadataFile(chroot: 'chroot_lib.Chroot',
                               sysroot: 'sysroot_lib.Sysroot') -> str:
  """Find the full path to the Tast local test metadata file.

  This file is installed during the tast-bundle eclass.
  """
  return chroot.full_path(
      sysroot.Path('usr', 'share', 'tast', 'metadata', 'local', 'cros.pb'))


def _FindTastLocalPrivateMetadataFile(chroot: 'chroot_lib.Chroot',
                                      sysroot: 'sysroot_lib.Sysroot') -> str:
  """Find the full path to the Tast local private test metadata file.

  This file is installed during the tast-bundle eclass.
  """
  return chroot.full_path(
      sysroot.Path('build', 'share', 'tast', 'metadata', 'local', 'crosint.pb'))


def _FindTastRemoteMetadataFile(chroot: 'chroot_lib.Chroot') -> str:
  """Find the full path to the Tast remote test metadata file.

  This file is installed during the tast-bundle eclass.
  """
  return chroot.full_path('usr', 'share', 'tast', 'metadata', 'remote',
                          'cros.pb')
