# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""The test service unit tests."""

import json
import os
import shutil
from typing import List
from unittest import mock

from chromite.api.gen.chromiumos import common_pb2
from chromite.cbuildbot import commands
from chromite.lib import autotest_util
from chromite.lib import build_target_lib
from chromite.lib import chroot_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import goma_lib
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import sysroot_lib
from chromite.lib.parser import package_info
from chromite.service import test
from chromite.service.test import GatherCodeCoverageLlvmJsonFileResult
from chromite.utils import code_coverage_util


class PartialDict:
  """Used as key value matcher in a mocked call."""

  def __init__(self, key, value):
    self.key = key
    self.value = value

  def __eq__(self, other):
    return other[self.key] == self.value


class BuildTargetUnitTestResultTest(cros_test_lib.TestCase):
  """BuildTargetUnitTestResult tests."""

  def testSuccess(self):
    """Test success case."""
    result = test.BuildTargetUnitTestResult(0, None)
    self.assertTrue(result.success)

  def testPackageFailure(self):
    """Test packages failed."""
    # Supposed to be CPVs, but not actually necessary at the moment.
    packages = ['a', 'b']
    # Should have a non-zero return code when packages fail.
    result = test.BuildTargetUnitTestResult(1, packages)
    self.assertFalse(result.success)
    # Make sure failed packages alone are enough.
    result = test.BuildTargetUnitTestResult(0, packages)
    self.assertFalse(result.success)

  def testScriptFailure(self):
    """Test non-package failure."""
    # Should have a non-zero return code when packages fail.
    result = test.BuildTargetUnitTestResult(1, None)
    self.assertFalse(result.success)


class BuildTargetUnitTestTest(cros_test_lib.RunCommandTempDirTestCase):
  """BuildTargetUnitTest tests."""

  def setUp(self):
    self.board = 'board'
    self.build_target = build_target_lib.BuildTarget(self.board)

  def testSuccess(self):
    """Test simple success case."""
    result = test.BuildTargetUnitTest(self.build_target)

    self.assertCommandContains(['cros_run_unit_tests', '--board', self.board])
    self.assertTrue(result.success)

  def testHost(self):
    """Test host target."""
    host_build_target = build_target_lib.BuildTarget('')
    result = test.BuildTargetUnitTest(host_build_target)

    self.assertCommandContains(['cros_run_unit_tests', '--host'])
    self.assertTrue(result.success)

  def testPackages(self):
    """Test the packages argument."""
    packages = ['foo/bar', 'cat/pkg']
    test.BuildTargetUnitTest(self.build_target, packages=packages)
    self.assertCommandContains(['--packages', 'foo/bar cat/pkg'])

  def testBlocklist(self):
    """Test the blocklist argument."""
    blocklist = ['foo/bar', 'cat/pkg']
    test.BuildTargetUnitTest(self.build_target, blocklist=blocklist)
    self.assertCommandContains(['--skip-packages', 'foo/bar cat/pkg'])

  def testTestablePackagesOptional(self):
    """Test the testable packages optional argument."""
    test.BuildTargetUnitTest(self.build_target, testable_packages_optional=True)
    self.assertCommandContains(['--no-testable-packages-ok'])

  def testFilterOnlyCrosWorkon(self):
    """Test the filter packages argument."""
    test.BuildTargetUnitTest(self.build_target, filter_only_cros_workon=True)
    self.assertCommandContains(['--filter-only-cros-workon'])

  def testFailure(self):
    """Test non-zero return code and failed package handling."""
    packages = ['foo/bar', 'cat/pkg']
    pkgs = [package_info.parse(p) for p in packages]
    self.PatchObject(portage_util, 'ParseDieHookStatusFile', return_value=pkgs)
    expected_rc = 1
    self.rc.SetDefaultCmdResult(returncode=expected_rc)

    result = test.BuildTargetUnitTest(self.build_target)

    self.assertFalse(result.success)
    self.assertEqual(expected_rc, result.return_code)
    self.assertCountEqual(pkgs, result.failed_pkgs)

  def testCodeCoverage(self):
    """Test adding use flags for coverage when requested."""
    self.PatchObject(os, 'environ', new={})
    result = test.BuildTargetUnitTest(self.build_target, code_coverage=True)

    self.assertCommandContains(['cros_run_unit_tests', '--board', self.board],
                               extra_env=PartialDict('USE', 'coverage'))
    self.assertTrue(result.success)

  def testCodeCoverageExistingFlags(self):
    """Test adding use flags for coverage when existing flags."""
    self.PatchObject(os, 'environ', new={'USE': 'foo bar'})
    result = test.BuildTargetUnitTest(self.build_target, code_coverage=True)

    self.assertCommandContains(['cros_run_unit_tests', '--board', self.board],
                               extra_env=PartialDict('USE', 'foo bar coverage'))
    self.assertTrue(result.success)

  def testCodeCoverageExistingCoverageFlag(self):
    """Test adding use flags for coverage when already has coverage flag."""
    self.PatchObject(os, 'environ', new={'USE': 'coverage bar'})
    result = test.BuildTargetUnitTest(self.build_target, code_coverage=True)

    self.assertCommandContains(['cros_run_unit_tests', '--board', self.board],
                               extra_env=PartialDict('USE', 'coverage bar'))
    self.assertTrue(result.success)


class DebugInfoTestTest(cros_test_lib.RunCommandTestCase):
  """DebugInfoTest tests."""

  def testSuccess(self):
    """Test command success."""
    self.assertTrue(test.DebugInfoTest('/sysroot/path'))
    self.assertCommandContains(
        ['debug_info_test', '/sysroot/path/usr/lib/debug'])

  def testFailure(self):
    """Test command failure."""
    self.rc.SetDefaultCmdResult(returncode=1)
    self.assertFalse(test.DebugInfoTest('/sysroot/path'))


class SimpleChromeWorkflowTestTest(cros_test_lib.MockTempDirTestCase):
  """Unit tests for SimpleChromeWorkflowTest."""

  def setUp(self):
    self.chrome_root = '/path/to/chrome/root'
    self.sysroot_path = '/chroot/path/sysroot/path'
    self.build_target = 'board'

    self.goma_mock = self.PatchObject(goma_lib, 'Goma')

    self.chrome_sdk_run_mock = self.PatchObject(commands.ChromeSDK, 'Run')

    # SimpleChromeTest workflow creates directories based on objects that are
    # mocked for this test, so patch osutils.WriteFile
    self.write_mock = self.PatchObject(osutils, 'WriteFile')

    self.PatchObject(cros_build_lib, 'CmdToStr', return_value='CmdToStr value')
    self.PatchObject(shutil, 'copy2')

  def testSimpleChromeWorkflowTest(self):
    goma_test_dir = os.path.join(self.tempdir, 'goma_test_dir')
    goma_test_json_string = os.path.join(self.tempdir, 'goma_json_string.txt')
    chromeos_goma_dir = os.path.join(self.tempdir, 'chromeos_goma_dir')
    goma_config = common_pb2.GomaConfig(
        goma_dir=goma_test_dir, goma_client_json=goma_test_json_string)
    osutils.SafeMakedirs(goma_test_dir)
    osutils.SafeMakedirs(chromeos_goma_dir)
    osutils.Touch(goma_test_json_string)
    goma = goma_lib.Goma(
        goma_config.goma_dir,
        goma_config.goma_client_json,
        stage_name='BuildApiTestSimpleChrome',
        chromeos_goma_dir=chromeos_goma_dir)

    mock_goma_log_dir = os.path.join(self.tempdir, 'goma_log_dir')
    osutils.SafeMakedirs(mock_goma_log_dir)
    goma.goma_log_dir = mock_goma_log_dir

    # For this test, we avoid running test._VerifySDKEnvironment because use of
    # other mocks prevent creating the SDK dir that _VerifySDKEnvironment checks
    # for
    self.PatchObject(test, '_VerifySDKEnvironment')

    self.PatchObject(os.path, 'exists', return_value=True)

    ninja_cmd = self.PatchObject(
        commands.ChromeSDK, 'GetNinjaCommand', return_value='ninja command')

    test.SimpleChromeWorkflowTest(self.sysroot_path, self.build_target,
                                  self.chrome_root, goma)
    # Verify ninja_cmd calls.
    ninja_calls = [mock.call(), mock.call(debug=False)]
    ninja_cmd.assert_has_calls(ninja_calls)

    # Verify calls with args to chrome_sdk_run made by service/test.py.
    gn_dir = os.path.join(self.chrome_root, 'buildtools/linux64/gn')
    board_out_dir = os.path.join(self.chrome_root, 'out_board/Release')

    self.chrome_sdk_run_mock.assert_any_call(['gclient', 'runhooks'])
    self.chrome_sdk_run_mock.assert_any_call(['true'])
    self.chrome_sdk_run_mock.assert_any_call([
        'bash', '-c',
        ('%s gen "%s" --args="$GN_ARGS"' % (gn_dir, board_out_dir))
    ])
    self.chrome_sdk_run_mock.assert_any_call(['env', '--null'],
                                             run_args=mock.ANY)
    self.chrome_sdk_run_mock.assert_any_call('ninja command', run_args=mock.ANY)

    # Create expected paths from constants so that the tests work inside or
    # outside the SDK.
    deploy_chrome_path = os.path.join(constants.SOURCE_ROOT,
                                      constants.CHROMITE_BIN_SUBDIR,
                                      'deploy_chrome')
    image_dir_symlink = image_lib.GetLatestImageLink(self.build_target)
    image_path = os.path.join(image_dir_symlink, constants.VM_IMAGE_BIN)

    self.chrome_sdk_run_mock.assert_any_call([
        deploy_chrome_path, '--build-dir', board_out_dir, '--staging-only',
        '--staging-dir', mock.ANY
    ])
    self.chrome_sdk_run_mock.assert_any_call([
        'cros_run_test', '--copy-on-write', '--deploy', '--board=board',
        ('--image-path=%s' % (image_path)), '--build-dir=out_board/Release'
    ])

    # Verify goma mock was started and stopped.
    # TODO(crbug/1065172): Invalid assertions that had previously been mocked.
    # self.goma_mock.Start.assert_called_once()
    # self.goma_mock.Stop.assert_called_once()


class BundleCodeCoverageLlvmJsonTest(cros_test_lib.MockTempDirTestCase):
  """BundleCodeCoverageLlvmJson Tests."""

  def setUp(self):
    """Set up the class for tests."""
    chroot_dir = os.path.join(self.tempdir, 'chroot')
    osutils.SafeMakedirs(chroot_dir)
    osutils.SafeMakedirs(os.path.join(chroot_dir, 'tmp'))
    self.chroot = chroot_lib.Chroot(chroot_dir)

    sysroot_path = os.path.join(chroot_dir, 'build', 'board')
    osutils.SafeMakedirs(sysroot_path)
    self.sysroot = sysroot_lib.Sysroot(sysroot_path)

    self.output_dir = os.path.join(self.tempdir, 'output')

  def testGatherCodeCoverageLlvmJsonFileIsCalled1Time(self):
    """Verify GatherCodeCoverageLlvmJsonFile is called on each file."""
    GatherCodeCoverageLlvmJsonFile_mock = self.PatchObject(
        test, 'GatherCodeCoverageLlvmJsonFile', return_value=None)

    test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot, self.output_dir)
    GatherCodeCoverageLlvmJsonFile_mock.assert_called_once()

  def testReturnNoneWhenGatherCodeCoverageLlvmJsonFileReturnsNone(self):
    """Test returns None when no coverage files were found."""
    self.PatchObject(test, 'GatherCodeCoverageLlvmJsonFile', return_value=None)

    result = test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot,
                                             self.output_dir)
    self.assertIsNone(result)

  def testCreateTarballIsCalled1Time(self):
    """Test that CreateTarball is called once."""
    gather_result = GatherCodeCoverageLlvmJsonFileResult({})
    self.PatchObject(
        test, 'GatherCodeCoverageLlvmJsonFile', return_value=gather_result)
    self.PatchObject(code_coverage_util, 'ExtractFilenames', return_value=[])
    self.PatchObject(
        code_coverage_util, 'GenerateZeroCoverageLlvm', return_value={})
    self.PatchObject(
        code_coverage_util, 'MergeLLVMCoverageJson', return_value={})
    self.PatchObject(
        code_coverage_util, 'GetLLVMCoverageWithFilesExcluded', return_value={})

    create_tarball_result = cros_build_lib.CompletedProcess(returncode=1)
    CreateTarball_mock = self.PatchObject(
        cros_build_lib, 'CreateTarball', return_value=create_tarball_result)

    test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot, self.output_dir)
    CreateTarball_mock.assert_called_once()

  def testGenerateZeroCoverageLlvmCalled1Time(self):
    """Test that GenerateZeroCoverageLlvm is called once."""
    gather_result = GatherCodeCoverageLlvmJsonFileResult({})
    self.PatchObject(
        test, 'GatherCodeCoverageLlvmJsonFile', return_value=gather_result)
    self.PatchObject(code_coverage_util, 'ExtractFilenames', return_value=[])
    self.PatchObject(
        code_coverage_util, 'GetLLVMCoverageWithFilesExcluded', return_value={})

    self.PatchObject(
        code_coverage_util, 'GenerateZeroCoverageLlvm', return_value={})
    self.PatchObject(
        code_coverage_util, 'MergeLLVMCoverageJson', return_value={})

    GenerateZeroCoverageLlvm_mock = self.PatchObject(
        code_coverage_util, 'GenerateZeroCoverageLlvm')

    test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot, self.output_dir)

    GenerateZeroCoverageLlvm_mock.assert_called_once()

  def testShouldReturnNoneWhenCreateTarballFails(self):
    """Test that None is returned when CreateTarball fails."""
    gather_result = GatherCodeCoverageLlvmJsonFileResult({})
    self.PatchObject(
        test, 'GatherCodeCoverageLlvmJsonFile', return_value=gather_result)

    create_tarball_result = cros_build_lib.CompletedProcess(returncode=1)
    self.PatchObject(
        cros_build_lib, 'CreateTarball', return_value=create_tarball_result)

    result = test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot,
                                             self.output_dir)
    self.assertIsNone(result)

  def testShouldReturnPathToTarballOnSuccess(self):
    """Test that the path to the tarball is returned on success."""
    gather_result = GatherCodeCoverageLlvmJsonFileResult({})
    self.PatchObject(
        test, 'GatherCodeCoverageLlvmJsonFile', return_value=gather_result)
    self.PatchObject(code_coverage_util, 'ExtractFilenames', return_value=[])
    self.PatchObject(
        code_coverage_util, 'GenerateZeroCoverageLlvm', return_value={})
    self.PatchObject(
        code_coverage_util, 'MergeLLVMCoverageJson', return_value={})
    self.PatchObject(
        code_coverage_util, 'GetLLVMCoverageWithFilesExcluded', return_value={})

    create_tarball_result = cros_build_lib.CompletedProcess(returncode=0)
    self.PatchObject(
        cros_build_lib, 'CreateTarball', return_value=create_tarball_result)

    result = test.BundleCodeCoverageLlvmJson(self.chroot, self.sysroot,
                                             self.output_dir)

    self.assertEqual(
        os.path.join(self.output_dir,
                     constants.CODE_COVERAGE_LLVM_JSON_SYMBOLS_TAR), result)

class GatherCodeCoverageLlvmJsonFileTest(cros_test_lib.MockTempDirTestCase):
  """GatherCodeCoverageLlvmJsonFile Tests."""

  def getCodeCoverageLlvmContents(self,
                                  filenames: List[str],
                                  version='1',
                                  file_type='llvm.coverage.json.export') -> str:
    """Helper for generating the contents of an llvm code coverage file."""
    return json.dumps({
        'data': [{
            'files': [{
                'filename': x
            } for x in filenames]
        }],
        'version': version,
        'type': file_type
    })

  def writeCodeCoverageLlvm(self, filename, content: str = None):
    """Helper to write a code coverage file."""
    if content is None:
      content = self.getCodeCoverageLlvmContents(['a.txt'])

    osutils.WriteFile(filename, content=content, mode='w', makedirs=True)

  def testJoinedFilePathsMatchesNumFilesProcessed(self):
    """Test that all coverage files are found."""
    input_dir = os.path.join(self.tempdir, 'input')
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/coverage.json'))
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/b/c/coverage.json'))
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/b/c/d/coverage.json'))
    self.writeCodeCoverageLlvm(
        os.path.join(input_dir, 'a/b/c/d/e/coverage.json'))

    coverage_json = test.GatherCodeCoverageLlvmJsonFile(input_dir)
    all_files = coverage_json['data'][0]['files']
    self.assertEqual(len(all_files), 4)

  def testCallsGetLlvmJsonCoverageDataIfValidForEachFile(self):
    """Test that GetLlvmJsonCoverageDataIfValid is called on each file."""
    get_llvm_json_coverage_data_if_valid_mock = self.PatchObject(
        code_coverage_util, 'GetLlvmJsonCoverageDataIfValid', return_value=None)

    input_dir = os.path.join(self.tempdir, 'input')
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/coverage.json'))
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/b/c/coverage.json'))
    self.writeCodeCoverageLlvm(os.path.join(input_dir, 'a/b/c/d/coverage.json'))
    self.writeCodeCoverageLlvm(
        os.path.join(input_dir, 'a/b/c/d/e/coverage.json'))

    test.GatherCodeCoverageLlvmJsonFile(input_dir)
    self.assertEqual(get_llvm_json_coverage_data_if_valid_mock.call_count, 4)

  def testWritesCombinedFileToOutputDir(self):
    """Test that all contents of valid files are combined into the output."""

    input_dir = os.path.join(self.tempdir, 'input')
    self.writeCodeCoverageLlvm(
        os.path.join(input_dir, 'a/src2/coverage.json'),
        self.getCodeCoverageLlvmContents(['/src2/a.txt', '/src2/b.txt']))
    self.writeCodeCoverageLlvm(
        os.path.join(input_dir, 'a/firmware/coverage.json'),
        self.getCodeCoverageLlvmContents(['/firmware/c.txt']))
    self.writeCodeCoverageLlvm(
        os.path.join(input_dir, 'a/invalid/invalid.json'), 'INVALID')

    coverage_json = test.GatherCodeCoverageLlvmJsonFile(input_dir)
    all_files = coverage_json['data'][0]['files']

    # Verify the contents of each valid file appear in the output.
    self.assertEqual(3, len(all_files))
    self.assertEqual(
        1, len([x for x in all_files if x['filename'] == '/src2/a.txt']))
    self.assertEqual(
        1, len([x for x in all_files if x['filename'] == '/src2/b.txt']))
    self.assertEqual(
        1, len([x for x in all_files if x['filename'] == '/firmware/c.txt']))

  def testShouldEmptyCoverageIfPathDoesNotExists(self):
    """Test empty coverage returned when path does not exist."""

    coverage_json = test.GatherCodeCoverageLlvmJsonFile('/invalid/path')
    all_files = coverage_json['data'][0]['files']
    self.assertEqual(0, len(all_files))


class FindMetadataTestCase(cros_test_lib.MockTestCase):
  """Test case for functions to find metadata files."""

  build_target_name = 'coral'
  sysroot_path = '/build/coral'
  chroot_path = '/usr/chroot'

  expected_autotest_metadata_file = (
      '/usr/chroot/build/coral/usr/local/build/autotest/autotest_metadata.pb')
  expected_tast_local_metadata_file = (
      '/usr/chroot/build/coral/usr/share/tast/metadata/local/cros.pb')
  expected_tast_local_private_metadata_file = (
      '/usr/chroot/build/coral/build/share/tast/metadata/local/crosint.pb')
  expected_tast_remote_metadata_file = (
      '/usr/chroot/usr/share/tast/metadata/remote/cros.pb')

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=False)
    self.sysroot = sysroot_lib.Sysroot(self.sysroot_path)
    self.chroot = chroot_lib.Chroot(self.chroot_path)
    self.PatchObject(cros_build_lib, 'AssertOutsideChroot')

  def testFindAllMetadataFiles(self):
    """Test case for Sysroot.FindAllMetadataFiles."""
    actual = test.FindAllMetadataFiles(self.chroot, self.sysroot)
    expected = [
        self.expected_autotest_metadata_file,
        self.expected_tast_local_metadata_file,
        self.expected_tast_local_private_metadata_file,
        self.expected_tast_remote_metadata_file,
    ]
    self.assertEqual(sorted(actual), sorted(expected))


class BundleHwqualTarballTest(cros_test_lib.MockTempDirTestCase):
  """BundleHwqualTarball tests."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=False)
    # Create the chroot and sysroot instances.
    self.chroot_path = os.path.join(self.tempdir, 'chroot_dir')
    self.chroot = chroot_lib.Chroot(path=self.chroot_path)
    self.sysroot_path = os.path.join(self.chroot_path, 'sysroot_dir')
    self.sysroot = sysroot_lib.Sysroot(self.sysroot_path)
    osutils.SafeMakedirs(self.sysroot_path)

    # Create the output directory.
    self.output_dir = os.path.join(self.tempdir, 'output_dir')
    osutils.SafeMakedirs(self.output_dir)

  def testNoArchiveDir(self):
    """Test a run when the archive dir does not exist."""
    self.assertIsNone(
        test.BundleHwqualTarball('foo', 'bar', self.chroot, self.sysroot,
                                 self.output_dir))

  def testAutotestUtilFailure(self):
    """Test a run when autotest_util fails to bundle autotest."""
    archive_dir = self.chroot.full_path(self.sysroot.path,
                                        constants.AUTOTEST_BUILD_PATH)
    osutils.SafeMakedirs(archive_dir)

    self.PatchObject(autotest_util, 'AutotestTarballBuilder', return_value=None)
    self.assertIsNone(
        test.BundleHwqualTarball('foo', 'bar', self.chroot, self.sysroot,
                                 self.output_dir))

  def testSuccess(self):
    """Test a successful multiple version run."""
    archive_dir = self.chroot.full_path(self.sysroot.path,
                                        constants.AUTOTEST_BUILD_PATH)
    osutils.SafeMakedirs(archive_dir)

    bundle_tmp_path = 'tmp/path/'
    self.PatchObject(osutils.TempDir, '__enter__', return_value=bundle_tmp_path)
    self.PatchObject(
        autotest_util, 'AutotestTarballBuilder', return_value=bundle_tmp_path)

    image_dir = 'path/to/image/'
    self.PatchObject(image_lib, 'GetLatestImageLink', return_value=image_dir)

    script_dir = os.path.join(constants.SOURCE_ROOT, 'src', 'platform',
                              'crostestutils')
    ssh_private_key = os.path.join(image_dir, constants.TEST_KEY_PRIVATE)

    run_mock = self.PatchObject(cros_build_lib, 'run')
    # Fake artifact placement.
    env_file = os.path.join(self.output_dir, 'chromeos-hwqual-foo-bar.tar.bz2')
    osutils.Touch(env_file)

    created = test.BundleHwqualTarball('foo', 'bar', self.chroot, self.sysroot,
                                       self.output_dir)
    run_mock.assert_called_with([
        os.path.join(script_dir, 'archive_hwqual'), '--from', bundle_tmp_path,
        '--to', self.output_dir, '--image_dir', image_dir, '--ssh_private_key',
        ssh_private_key, '--output_tag', 'chromeos-hwqual-foo-bar'
    ],)
    self.assertStartsWith(created, self.output_dir)
