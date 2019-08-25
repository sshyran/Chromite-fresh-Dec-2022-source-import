# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test service.

Handles test related functionality.
"""
import json
import logging
import os
import re
import shutil
from typing import Dict, Iterable, List, NamedTuple, Optional, TYPE_CHECKING

from chromite.cbuildbot import commands
from chromite.lib import autotest_util
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import failures_lib
from chromite.lib import image_lib
from chromite.lib import moblab_vm
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.utils import code_coverage_util


if TYPE_CHECKING:
  from chromite.lib import build_target_lib
  from chromite.lib import chroot_lib
  from chromite.lib import goma_lib
  from chromite.lib import sysroot_lib
  from chromite.lib.parser import package_info


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
                        chroot: Optional['chroot_lib.Chroot'],
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
    chroot: The chroot where the tests are running if this function is executed
      from outside the SDK.
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

  extra_env = chroot.env if chroot else {}

  if code_coverage:
    use_flags = extra_env.get('USE', '').split()
    if 'coverage' not in use_flags:
      use_flags.append('coverage')
    extra_env['USE'] = ' '.join(use_flags)

  tmpdir_ctx_mgr = chroot.tempdir if chroot else osutils.TempDir
  # Set up the failed package status file.
  with tmpdir_ctx_mgr() as tempdir:
    extra_env[constants.CROS_METRICS_DIR_ENVVAR] = (
        chroot.chroot_path(tempdir) if chroot else tempdir)

    result = cros_build_lib.run(
        cmd,
        enter_chroot=True,
        extra_env=extra_env,
        chroot_args=chroot.get_enter_args() if chroot else None,
        check=False)

    failed_pkgs = portage_util.ParseDieHookStatusFile(tempdir)

  return BuildTargetUnitTestResult(result.returncode, failed_pkgs)


def BuildTargetUnitTestTarball(chroot: 'chroot_lib.Chroot',
                               sysroot: 'sysroot_lib.Sysroot',
                               result_path: str) -> Optional[str]:
  """Build the unittest tarball.

  Args:
    chroot: Chroot where the tests were run.
    sysroot: The sysroot where the tests were run.
    result_path: The directory where the archive should be created.

  Returns:
    The tarball path or None.
  """
  tarball = 'unit_tests.tar'
  tarball_path = os.path.join(result_path, tarball)

  cwd = chroot.full_path(sysroot.path, constants.UNITTEST_PKG_PATH)

  if not os.path.exists(cwd):
    return None

  result = cros_build_lib.CreateTarball(
      tarball_path,
      cwd,
      chroot=chroot.path,
      compression=cros_build_lib.COMP_NONE,
      check=False)

  return tarball_path if result.returncode == 0 else None


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


def CreateMoblabVm(workspace_dir: str, chroot_dir: str,
                   image_dir: str) -> moblab_vm.MoblabVm:
  """Create the moblab VMs.

  Assumes that image_dir is in exactly the state it was after building
  a test image and then converting it to a VM image.

  Args:
    workspace_dir: Workspace for the moblab VM.
    chroot_dir: Directory containing the chroot for the moblab VM.
    image_dir: Directory containing the VM image.

  Returns:
    The resulting VM.
  """
  vms = moblab_vm.MoblabVm(workspace_dir, chroot_dir=chroot_dir)
  vms.Create(image_dir, dut_image_dir=image_dir, create_vm_images=False)
  return vms


def PrepareMoblabVmImageCache(vms: moblab_vm.MoblabVm, builder: str,
                              payload_dirs: List[str]) -> str:
  """Preload the given payloads into the moblab VM image cache.

  Args:
    vms: The Moblab VM.
    builder: The builder path, used to name the cache dir.
    payload_dirs: List of payload directories to load.

  Returns:
    Absolute path to the image cache path.
  """
  with vms.MountedMoblabDiskContext() as disk_dir:
    image_cache_root = os.path.join(disk_dir, 'static/prefetched')
    # If by any chance this path exists, the permission bits are surely
    # nonsense, since 'moblab' user doesn't exist on the host system.
    osutils.RmDir(image_cache_root, ignore_missing=True, sudo=True)

    image_cache_dir = os.path.join(image_cache_root, builder)
    osutils.SafeMakedirsNonRoot(image_cache_dir)
    for payload_dir in payload_dirs:
      osutils.CopyDirContents(payload_dir, image_cache_dir, allow_nonempty=True)

  image_cache_rel_dir = image_cache_dir[len(disk_dir):].strip('/')
  return os.path.join('/', 'mnt/moblab', image_cache_rel_dir)


def RunMoblabVmTest(chroot: 'chroot_lib.Chroot', vms: moblab_vm.MoblabVm,
                    builder: str, image_cache_dir: str,
                    results_dir: str) -> None:
  """Run Moblab VM tests.

  Args:
    chroot: The chroot in which to run tests.
    builder: The builder path, used to find artifacts on GS.
    vms: The Moblab VMs to test.
    image_cache_dir: Path to artifacts cache.
    results_dir: Path to output test results.
  """
  with vms.RunVmsContext():
    # TODO(evanhernandez): Move many of these arguments to test config.
    test_args = [
        # moblab in VM takes longer to bring up all upstart services on first
        # boot than on physical machines.
        'services_init_timeout_m=10',
        'target_build="%s"' % builder,
        'test_timeout_hint_m=90',
        'clear_devserver_cache=False',
        'image_storage_server="%s"' % (image_cache_dir.rstrip('/') + '/'),
    ]
    cros_build_lib.run(
        [
            'test_that',
            '--no-quickmerge',
            '--results_dir',
            results_dir,
            '-b',
            'moblab-generic-vm',
            'localhost:%s' % vms.moblab_ssh_port,
            'moblab_DummyServerNoSspSuite',
            '--args',
            ' '.join(test_args),
        ],
        enter_chroot=True,
        chroot_args=chroot.get_enter_args(),
    )


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


def ValidateMoblabVmTest(results_dir: str) -> None:
  """Determine if the VM test passed or not.

  Args:
    results_dir: Path to directory containing test_that results.

  Raises:
    failures_lib.TestFailure: If dummy_PassServer did not run or failed.
  """
  log_file = os.path.join(results_dir, 'debug', 'test_that.INFO')
  if not os.path.isfile(log_file):
    raise failures_lib.TestFailure('Found no test_that logs at %s' % log_file)

  log_file_contents = osutils.ReadFile(log_file)
  if not re.match(r'dummy_PassServer\s*\[\s*PASSED\s*]', log_file_contents):
    raise failures_lib.TestFailure('Moblab run_suite succeeded, but did '
                                   'not successfully run dummy_PassServer.')


def BundleCodeCoverageLlvmJson(chroot: 'chroot_lib.Chroot',
                               sysroot_class: 'sysroot_lib.Sysroot',
                               output_dir: str) -> Optional[str]:
  """Bundle code coverage llvm json into a tarball for importing into GCE.

  Args:
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
    llvm_generated_cov_json = GatherCodeCoverageLlvmJsonFile(
        paths=[coverage_dir])
    llvm_generated_cov_json = (
        code_coverage_util.GetLLVMCoverageWithFilesExcluded(
            llvm_generated_cov_json,
            constants.ZERO_COVERAGE_EXCLUDE_FILES_SUFFIXES))

    # Generate zero coverage for all src files, excluding those which are
    # already present in llvm_generated_cov_json
    files_with_cov = code_coverage_util.ExtractFilenames(
        llvm_generated_cov_json)
    zero_coverage_json = code_coverage_util.GenerateZeroCoverageLlvm(
        # TODO(b/227649725): Input path_to_src_directories and language specific
        # src_file_extensions and exclude_line_prefixes from GetArtifact API
        path_to_src_directories=[
            os.path.join(constants.SOURCE_ROOT, 'src/platform/'),
            os.path.join(constants.SOURCE_ROOT, 'src/platform2/')
        ],
        src_file_extensions=constants.ZERO_COVERAGE_FILE_EXTENSIONS_TO_PROCESS,
        exclude_line_prefixes=constants.ZERO_COVERAGE_EXCLUDE_LINE_PREFIXES,
        exclude_files=files_with_cov,
        exclude_files_suffixes=constants.ZERO_COVERAGE_EXCLUDE_FILES_SUFFIXES,
        src_prefix_path=constants.SOURCE_ROOT)
    # Merge generated zero coverage data and
    # llvm compiler generated coverage data.
    merged_coverage_json = code_coverage_util.MergeLLVMCoverageJson(
        llvm_generated_cov_json, zero_coverage_json)

    with chroot.tempdir() as dest_tmpdir:
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
    logging.error('BundleCodeCoverageLlvmJson failed %s', e)
    return None


class GatherCodeCoverageLlvmJsonFileResult(NamedTuple):
  """Class containing result data of GatherCodeCoverageLlvmJsonFile."""
  coverage_json: Dict


def GatherCodeCoverageLlvmJsonFile(paths: List[str]):
  """Locate code coverage llvm json files in |paths|.

   This function locates all the coverage llvm json files and merges them
   into one file, in the correct llvm json format.

  Args:
    paths: A list of input paths to walk.

  Returns:
    Code coverage json llvm format.
  """
  joined_file_paths = []
  coverage_data = []
  for p in paths:
    if not os.path.exists(p):
      raise NoFilesError('The path did not exist: ', p)

    if not os.path.isdir(p):
      raise ValueError('The path is not a directory: ', p)

    for root, _, files in os.walk(p):
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
