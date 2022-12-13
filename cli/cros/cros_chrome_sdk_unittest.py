# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module tests the cros image command."""

import copy
import json
import os
import shutil
import threading
from unittest import mock

from chromite.third_party.gn_helpers import gn_helpers

from chromite.cli import command_unittest
from chromite.cli.cros import cros_chrome_sdk
from chromite.lib import cache
from chromite.lib import chromite_config
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import gs_unittest
from chromite.lib import osutils
from chromite.lib import partial_mock


# pylint: disable=protected-access


class MockChromeSDKCommand(command_unittest.MockCommand):
  """Mock out the build command."""
  TARGET = 'chromite.cli.cros.cros_chrome_sdk.ChromeSDKCommand'
  TARGET_CLASS = cros_chrome_sdk.ChromeSDKCommand
  COMMAND = 'chrome-sdk'
  ATTRS = ('_SetupEnvironment',) + command_unittest.MockCommand.ATTRS

  def __init__(self, *args, **kwargs):
    command_unittest.MockCommand.__init__(self, *args, **kwargs)
    self.env = None

  def _SetupEnvironment(self, *args, **kwargs):
    env = self.backup['_SetupEnvironment'](*args, **kwargs)
    self.env = copy.deepcopy(env)
    return env


class ParserTest(cros_test_lib.MockTempDirTestCase):
  """Test the parser."""
  def testNormal(self):
    """Tests that our example parser works normally."""
    with MockChromeSDKCommand(
        ['--board', SDKFetcherMock.BOARD],
        base_args=['--cache-dir', str(self.tempdir)]) as bootstrap:
      self.assertEqual(bootstrap.inst.options.board, SDKFetcherMock.BOARD)
      self.assertEqual(bootstrap.inst.options.cache_dir, str(self.tempdir))

  def testVersion(self):
    """Tests that a platform version is allowed."""
    VERSION = '1234.0.0'
    with MockChromeSDKCommand(
        ['--board', SDKFetcherMock.BOARD, '--version', VERSION]) as parser:
      self.assertEqual(parser.inst.options.version, VERSION)

  def testFullVersion(self):
    """Tests that a full version is allowed."""
    FULL_VERSION = 'R56-1234.0.0'
    with MockChromeSDKCommand(
        ['--board', SDKFetcherMock.BOARD, '--version', FULL_VERSION]) as parser:
      self.assertEqual(parser.inst.options.version, FULL_VERSION)


def _GSCopyMock(_self, path, dest, **_kwargs):
  """Used to simulate a GS Copy operation."""
  with osutils.TempDir() as tempdir:
    local_path = os.path.join(tempdir, os.path.basename(path))
    osutils.Touch(local_path)
    shutil.move(local_path, dest)


def _DependencyMockCtx(f):
  """Attribute that ensures dependency PartialMocks are started.

  Since PartialMock does not support nested mocking, we need to first call
  stop() on the outer level PartialMock (which is passed in to us).  We then
  re-start() the outer level upon exiting the context.
  """
  def new_f(self, *args, **kwargs):
    if not self.entered:
      try:
        self.entered = True
        # Temporarily disable outer GSContext mock before starting our mock.
        # TODO(rcui): Generalize this attribute and include in partial_mock.py.
        for emock in self.external_mocks:
          emock.stop()

        with self.gs_mock:
          return f(self, *args, **kwargs)
      finally:
        self.entered = False
        for emock in self.external_mocks:
          emock.start()
    else:
      return f(self, *args, **kwargs)
  return new_f


class SDKFetcherMock(partial_mock.PartialMock):
  """Provides mocking functionality for SDKFetcher."""

  TARGET = 'chromite.cli.cros.cros_chrome_sdk.SDKFetcher'
  ATTRS = ('__init__', 'GetFullVersion', '_GetMetadata', '_UpdateTarball',
           '_GetManifest', 'UpdateDefaultVersion', '_GetTarballCacheKey',
           '_GetBuildReport', '_HasInternalConfig')

  FAKE_METADATA = """
{
  "boards": ["eve"],
  "cros-version": "25.3543.2",
  "metadata-version": "1",
  "bot-hostname": "build82-m2.golo.chromium.org",
  "bot-config": "eve-release",
  "toolchain-tuple": ["i686-pc-linux-gnu"],
  "toolchain-url": "2013/01/%(target)s-2013.01.23.003823.tar.xz",
  "sdk-version": "2013.01.23.003823"
}"""
  FAKE_BUILD_REPORT = """
{
  "sdkVersion": "2013.01.23.003823",
  "toolchainUrl": "2013/01/%(target)s-2013.01.23.003823.tar.xz",
  "toolchains": ["i686-pc-linux-gnu"]
}
"""

  BOARD = 'eve'
  # These are boards that Lacros is currently supporting.
  # Specifically, *-crostoolchain.gni files need to be generated for them.
  BOARDS = ['amd64-generic', 'arm-generic', 'arm64-generic']
  VERSION = '4567.8.9'

  def __init__(self, external_mocks=None):
    """Initializes the mock.

    Args:
      external_mocks: A list of already started PartialMock/patcher instances.
        stop() will be called on each element every time execution enters one of
        our the mocked out methods, and start() called on it once execution
        leaves the mocked out method.
    """
    partial_mock.PartialMock.__init__(self)
    self.external_mocks = external_mocks or []
    self.entered = False
    self.gs_mock = gs_unittest.GSContextMock()
    self.gs_mock.SetDefaultCmdResult()
    self.env = None
    self.tarball_cache_key_map = {}
    self.tarball_fetch_lock = threading.Lock()

  @_DependencyMockCtx
  def _HasInternalConfig(self, inst, *args, **kwargs):
    self.gs_mock.SetDefaultCmdResult()
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex(f'ls .*gs://{constants.RELEASE_GS_BUCKET}'),
        side_effect=gs.GSCommandError('some ACL error'))
    return self.backup['_HasInternalConfig'](inst, *args, **kwargs)

  @_DependencyMockCtx
  def _target__init__(self, inst, *args, **kwargs):
    self.backup['__init__'](inst, *args, **kwargs)
    if not inst.cache_base.startswith('/tmp'):
      raise AssertionError('For testing, SDKFetcher cache_dir needs to be a '
                           'dir under /tmp')

  @_DependencyMockCtx
  def UpdateDefaultVersion(self, inst, *_args, **_kwargs):
    inst._SetDefaultVersion(self.VERSION)
    return self.VERSION, True

  @_DependencyMockCtx
  def _UpdateTarball(self, inst, *args, **kwargs):
    # The mocks here can fall off in the middle of the test unreliably, likely
    # due to a race condition when running _UpdateTarball across multiple
    # threads. So lock around the mocks to avoid.
    with self.tarball_fetch_lock:
      with mock.patch.object(gs.GSContext, 'Copy', autospec=True,
                             side_effect=_GSCopyMock):
        with mock.patch.object(cache, 'Untar'):
          return self.backup['_UpdateTarball'](inst, *args, **kwargs)

  @_DependencyMockCtx
  def GetFullVersion(self, _inst, version):
    return 'R26-%s' % version

  @_DependencyMockCtx
  def _GetMetadata(self, inst, *args, **kwargs):
    self.gs_mock.SetDefaultCmdResult()
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/%s' % constants.METADATA_JSON),
        stdout=self.FAKE_METADATA)
    return self.backup['_GetMetadata'](inst, *args, **kwargs)

  @_DependencyMockCtx
  def _GetBuildReport(self, inst, *args, **kwargs):
    self.gs_mock.SetDefaultCmdResult()
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/%s' % constants.BUILD_REPORT_JSON),
        stdout=self.FAKE_BUILD_REPORT)
    return self.backup['_GetBuildReport'](inst, *args, **kwargs)

  @_DependencyMockCtx
  def _GetManifest(self, _inst, _version):
    return {
        'packages': {
            'app-emulation/qemu': [['3.0.0', {}]],
            'chromeos-base/tast-cmd': [['1.2.3', {}]],
            'chromeos-base/tast-remote-tests-cros': [['7.8.9', {}]],
            'sys-firmware/seabios': [['1.11.0', {}]]
        }
    }

  @_DependencyMockCtx
  def _GetTarballCacheKey(self, _inst, component, _url):
    return (os.path.join(
        component,
        self.tarball_cache_key_map.get(component, 'some-fake-hash')),)


class RunThroughTest(cros_test_lib.MockTempDirTestCase,
                     cros_test_lib.LoggingTestCase):
  """Run the script with most things mocked out."""

  VERSION_KEY = (SDKFetcherMock.BOARD, SDKFetcherMock.VERSION,
                 constants.CHROME_SYSROOT_TAR)

  FAKE_ENV = {
      'GN_ARGS': 'target_sysroot="/path/to/sysroot" is_clang=false',
      'AR': 'x86_64-cros-linux-gnu-ar',
      'AS': 'x86_64-cros-linux-gnu-as',
      'CXX': 'x86_64-cros-linux-gnu-clang++',
      'CC': 'x86_64-cros-linux-gnu-clang',
      'LD': 'x86_64-cros-linux-gnu-clang++',
      'NM': 'x86_64-cros-linux-gnu-nm',
      'RANLIB': 'x86_64-cros-linux-gnu-ranlib',
      'READELF': 'x86_64-cros-linux-gnu-readelf',
      'CFLAGS': '-O2',
      'CXXFLAGS': '-O2',
  }

  def SetupCommandMock(self, many_boards=False, extra_args=None,
                       default_cache_dir=False):

    cmd_args = ['--chrome-src', self.chrome_src_dir, 'true']
    if many_boards:
      cmd_args += ['--boards', ':'.join(SDKFetcherMock.BOARDS), '--no-shell']
    else:
      cmd_args += ['--board', SDKFetcherMock.BOARD]
    if extra_args:
      cmd_args.extend(extra_args)
    # --no-shell drops gni files in //build/args/chromeos/.
    # reclient configs are also dropped here regardless of --no-shell or not.
    osutils.SafeMakedirs(
        os.path.join(self.chrome_root, 'src', 'build', 'args', 'chromeos'))

    base_args = (None if default_cache_dir else
                 ['--cache-dir', str(self.tempdir)])
    self.cmd_mock = MockChromeSDKCommand(cmd_args, base_args=base_args)
    self.StartPatcher(self.cmd_mock)
    self.cmd_mock.UnMockAttr('Run')

  def SourceEnvironmentMock(self, path, *_args, **_kwargs):
    if str(path).endswith('environment'):
      return copy.deepcopy(self.FAKE_ENV)
    return {}

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    self.sdk_mock = self.StartPatcher(SDKFetcherMock(
        external_mocks=[self.rc_mock]))

    # This needs to occur before initializing MockChromeSDKCommand.
    self.bashrc = self.tempdir / 'bashrc'
    self.PatchObject(chromite_config, 'CHROME_SDK_BASHRC', new=self.bashrc)

    self.PatchObject(osutils, 'SourceEnvironment',
                     autospec=True, side_effect=self.SourceEnvironmentMock)
    self.rc_mock.AddCmdResult(cros_chrome_sdk.ChromeSDKCommand.GOMACC_PORT_CMD,
                              stdout='8088')

    # Initialized by SetupCommandMock.
    self.cmd_mock = None

    # Set up a fake Chrome src/ directory
    self.chrome_root = os.path.join(self.tempdir, 'chrome_root')
    self.chrome_src_dir = os.path.join(self.chrome_root, 'src')
    osutils.SafeMakedirs(self.chrome_src_dir)
    osutils.Touch(os.path.join(self.chrome_root, '.gclient'))
    osutils.SafeMakedirs(os.path.join(self.chrome_src_dir, 'chrome'))
    osutils.WriteFile(
        os.path.join(self.chrome_src_dir, 'chrome', 'VERSION'), 'MAJOR=123')

  @property
  def cache(self):
    return self.cmd_mock.inst.sdk.tarball_cache

  def testIt(self):
    """Test a runthrough of the script."""
    self.PatchObject(cros_chrome_sdk.ChromeSDKCommand, '_GomaDir',
                     side_effect=['XXXX'])
    self.SetupCommandMock()
    with cros_test_lib.LoggingCapturer() as logs:
      self.cmd_mock.inst.Run()
      self.AssertLogsContain(logs, 'Goma:', inverted=True)

  def testManyBoards(self):
    """Test a runthrough when multiple boards are specified via --boards."""
    self.SetupCommandMock(many_boards=True)
    self.cmd_mock.inst.ProcessOptions(
        self.cmd_mock.parser, self.cmd_mock.inst.options)
    self.cmd_mock.inst.Run()
    for board in SDKFetcherMock.BOARDS:
      board_arg_file = os.path.join(
          self.chrome_src_dir, 'build/args/chromeos/%s.gni' % board)
      self.assertExists(board_arg_file)
      board_crostoolchain_arg_file = os.path.join(
          self.chrome_src_dir,
          'build/args/chromeos/%s-crostoolchain.gni' % board)
      self.assertNotExists(board_crostoolchain_arg_file)

  def testManyBoardsLacros(self):
    """Test a runthrough when multiple boards are specified via --boards."""
    self.SetupCommandMock(many_boards=True,
                          extra_args=['--is-lacros', '--version=1234.0.0'])
    lkgm_file = os.path.join(self.chrome_src_dir, constants.PATH_TO_CHROME_LKGM)
    osutils.Touch(lkgm_file, makedirs=True)
    osutils.WriteFile(lkgm_file, '5678.0.0')

    self.cmd_mock.inst.ProcessOptions(
        self.cmd_mock.parser, self.cmd_mock.inst.options)
    self.cmd_mock.inst.Run()
    for board in SDKFetcherMock.BOARDS:
      board_arg_file = os.path.join(
          self.chrome_src_dir, 'build/args/chromeos/%s.gni' % board)
      self.assertNotExists(board_arg_file)
      board_crostoolchain_arg_file = os.path.join(
          self.chrome_src_dir,
          'build/args/chromeos/%s-crostoolchain.gni' % board)
      self.assertExists(board_crostoolchain_arg_file)
      with open(board_crostoolchain_arg_file) as f:
        self.assertIn('cros_sdk_version = "5678.0.0"', f.read())

  def testManyBoardsBrokenArgs(self):
    """Tests that malformed args.gn files will be fixed in --boards."""
    self.SetupCommandMock(many_boards=True)
    for board in SDKFetcherMock.BOARDS:
      gn_args_file = os.path.join(
          self.chrome_src_dir, 'out_%s' % board, 'Release', 'args.gn')
      osutils.WriteFile(gn_args_file, 'foo\nbar', makedirs=True)

    self.cmd_mock.inst.ProcessOptions(
        self.cmd_mock.parser, self.cmd_mock.inst.options)
    self.cmd_mock.inst.Run()

    for board in SDKFetcherMock.BOARDS:
      gn_args_file = os.path.join(
          self.chrome_src_dir, 'out_%s' % board, 'Release', 'args.gn')
      self.assertTrue(osutils.ReadFile(gn_args_file).startswith('import'))

  def testErrorCodePassthrough(self):
    """Test that error codes are passed through."""
    self.SetupCommandMock()
    with cros_test_lib.LoggingCapturer():
      self.rc_mock.AddCmdResult(partial_mock.ListRegex('-- true'),
                                returncode=5)
      returncode = self.cmd_mock.inst.Run()
      self.assertEqual(returncode, 5)

  def testEmptyMetadata(self):
    """Tests the use of build_report.json when metadata.json is empty."""
    sdk_dir = os.path.join(self.tempdir, 'sdk_dir')
    osutils.SafeMakedirs(sdk_dir)
    osutils.WriteFile(os.path.join(sdk_dir, constants.METADATA_JSON), '{}')
    osutils.WriteFile(os.path.join(sdk_dir, constants.BUILD_REPORT_JSON),
                      SDKFetcherMock.FAKE_BUILD_REPORT)
    self.SetupCommandMock(extra_args=['--sdk-path', sdk_dir])
    with cros_test_lib.LoggingCapturer():
      self.cmd_mock.inst.Run()

  def testLocalSDKPath(self):
    """Fetch components from a local --sdk-path."""
    sdk_dir = os.path.join(self.tempdir, 'sdk_dir')
    osutils.SafeMakedirs(sdk_dir)
    osutils.WriteFile(os.path.join(sdk_dir, constants.METADATA_JSON),
                      SDKFetcherMock.FAKE_METADATA)
    osutils.WriteFile(os.path.join(sdk_dir, constants.BUILD_REPORT_JSON),
                      SDKFetcherMock.FAKE_BUILD_REPORT)
    self.SetupCommandMock(extra_args=['--sdk-path', sdk_dir])
    with cros_test_lib.LoggingCapturer():
      self.cmd_mock.inst.Run()

  def testGomaError(self):
    """We print an error message when GomaError is raised."""
    self.SetupCommandMock()
    with cros_test_lib.LoggingCapturer() as logs:
      self.PatchObject(cros_chrome_sdk.ChromeSDKCommand, '_SetupGoma',
                       side_effect=cros_chrome_sdk.GomaError())
      self.cmd_mock.inst.Run()
      self.AssertLogsContain(logs, 'Goma:')

  def testSpecificComponent(self):
    """Tests that SDKFetcher.Prepare() handles |components| param properly."""
    sdk = cros_chrome_sdk.SDKFetcher(os.path.join(self.tempdir),
                                     SDKFetcherMock.BOARD)
    components = [constants.BASE_IMAGE_TAR, constants.CHROME_SYSROOT_TAR]
    with sdk.Prepare(components=components) as ctx:
      for c in components:
        self.assertExists(ctx.key_map[c].path)
      for c in [constants.IMAGE_SCRIPTS_TAR, constants.CHROME_ENV_TAR]:
        self.assertFalse(c in ctx.key_map)

  def testExceptionDuringUpdateTarball(self):
    """Tests that an exception thrown in _UpdateTarball is surfaced.

    _UpdateTarball is ran across multiple threads. This test ensures an
    exception raised in one of those threads is surfaced to the caller.
    """
    self.SetupCommandMock()
    with mock.patch.object(cache.CacheReference, 'SetDefault',
                           side_effect=ValueError('uh oh')):
      with self.assertRaises(ValueError):
        self.cmd_mock.inst.Run()

  @staticmethod
  def FindInPath(paths, endswith):
    for path in paths.split(':'):
      if path.endswith(endswith):
        return True
    return False

  def testGomaInPath(self):
    """Verify that we do indeed add Goma to the PATH."""
    self.PatchObject(cros_chrome_sdk.ChromeSDKCommand, '_GomaDir',
                     side_effect=['XXXX'])
    self.SetupCommandMock()
    self.cmd_mock.inst.Run()

    self.assertIn('use_goma = true', self.cmd_mock.env['GN_ARGS'])

  def testNoGoma(self):
    """Verify that we do not add Goma to the PATH."""
    self.SetupCommandMock(extra_args=['--nogoma'])
    self.cmd_mock.inst.Run()

    self.assertIn('use_goma = false', self.cmd_mock.env['GN_ARGS'])

  def testUseRBE(self):
    """Verify that we do not add Goma to the PATH."""
    self.SetupCommandMock(extra_args=['--use-remoteexec'])
    self.cmd_mock.inst.Run()

    self.assertIn('use_goma = false', self.cmd_mock.env['GN_ARGS'])
    self.assertIn('use_remoteexec = true', self.cmd_mock.env['GN_ARGS'])
    wrapper_path = os.path.join(
        self.chrome_root, 'src', 'build', 'args', 'chromeos',
        'rewrapper_%s' % SDKFetcherMock.BOARD)
    self.assertIn('rbe_cros_cc_wrapper = "%s"' % wrapper_path,
                  self.cmd_mock.env['GN_ARGS'])

  def testUseRBELacros(self):
    """Verify that we do not add Goma to the PATH."""
    self.SetupCommandMock(extra_args=['--use-remoteexec',
                                      '--is-lacros', '--version=1234.0.0'])
    lkgm_file = os.path.join(self.chrome_src_dir, constants.PATH_TO_CHROME_LKGM)
    osutils.Touch(lkgm_file, makedirs=True)
    osutils.WriteFile(lkgm_file, '5678.0.0')

    self.cmd_mock.inst.Run()

    self.assertIn('use_goma = false', self.cmd_mock.env['GN_ARGS'])
    self.assertIn('use_remoteexec = true', self.cmd_mock.env['GN_ARGS'])
    wrapper_path = os.path.join(
        self.chrome_root, 'src', 'build', 'args', 'chromeos',
        'rewrapper_%s' % SDKFetcherMock.BOARD)
    self.assertIn('rbe_cros_cc_wrapper = "%s"' % wrapper_path,
                  self.cmd_mock.env['GN_ARGS'])

  def testGnArgsStalenessCheckNoMatch(self):
    """Verifies the GN args are checked for staleness with a mismatch."""
    with cros_test_lib.LoggingCapturer() as logs:
      out_dir = 'out_%s' % SDKFetcherMock.BOARD
      build_label = 'Release'
      gn_args_file_dir = os.path.join(self.chrome_src_dir, out_dir, build_label)
      gn_args_file_path = os.path.join(gn_args_file_dir, 'args.gn')
      osutils.SafeMakedirs(gn_args_file_dir)
      osutils.WriteFile(gn_args_file_path, 'foo = "no match"')

      self.SetupCommandMock()
      self.cmd_mock.inst.Run()

      self.AssertLogsContain(logs, 'Stale args.gn file')

  def testGnArgsStalenessCheckMatch(self):
    """Verifies the GN args are checked for staleness with a match."""
    with cros_test_lib.LoggingCapturer() as logs:
      self.SetupCommandMock()
      self.cmd_mock.inst.Run()

      out_dir = 'out_%s' % SDKFetcherMock.BOARD
      build_label = 'Release'
      gn_args_file_dir = os.path.join(self.chrome_src_dir, out_dir, build_label)
      gn_args_file_path = os.path.join(gn_args_file_dir, 'args.gn')

      osutils.SafeMakedirs(gn_args_file_dir)
      osutils.WriteFile(gn_args_file_path, self.cmd_mock.env['GN_ARGS'])

      self.cmd_mock.inst.Run()

      self.AssertLogsContain(logs, 'Stale args.gn file', inverted=True)

  def testGnArgsStalenessExtraArgs(self):
    """Verifies the GN extra args regenerate gn."""
    with cros_test_lib.LoggingCapturer() as logs:
      self.SetupCommandMock(
          extra_args=['--gn-extra-args=dcheck_always_on=true'])
      self.cmd_mock.inst.Run()

      out_dir = 'out_%s' % SDKFetcherMock.BOARD
      build_label = 'Release'
      gn_args_file_dir = os.path.join(self.chrome_src_dir, out_dir, build_label)
      gn_args_file_path = os.path.join(gn_args_file_dir, 'args.gn')

      osutils.SafeMakedirs(gn_args_file_dir)
      gn_args_dict = gn_helpers.FromGNArgs(self.cmd_mock.env['GN_ARGS'])
      osutils.WriteFile(gn_args_file_path, gn_helpers.ToGNString(gn_args_dict))

      self.cmd_mock.inst.Run()

      self.AssertLogsContain(logs, 'Stale args.gn file', inverted=True)

  def testChromiumOutDirSet(self):
    """Verify that CHROMIUM_OUT_DIR is set."""
    self.SetupCommandMock()
    self.cmd_mock.inst.Run()

    out_dir = os.path.join(self.chrome_src_dir, 'out_%s' % SDKFetcherMock.BOARD)

    self.assertEqual(out_dir, self.cmd_mock.env['CHROMIUM_OUT_DIR'])

  @mock.patch('chromite.lib.gclient.LoadGclientFile')
  def testInternalGclientSpec(self, mock_gclient_load):
    """Verify that the SDK exits with an error if the gclient spec is wrong."""
    self.SetupCommandMock(extra_args=['--internal'])

    # Simple Chrome should exit with an error if "--internal" is passed and
    # "checkout_src_internal" isn't present in the .gclient file.
    mock_gclient_load.return_value = [{
        'url': 'https://chromium.googlesource.com/chromium/src.git',
        'custom_deps': {},
        'custom_vars': {},
    }]
    with self.assertRaises(cros_build_lib.DieSystemExit):
      self.cmd_mock.inst.Run()

    # With "checkout_src_internal" set, Simple Chrome should run without error.
    mock_gclient_load.return_value = [{
        'url': 'https://chromium.googlesource.com/chromium/src.git',
        'custom_deps': {},
        'custom_vars': {
            'checkout_src_internal': True
        },
    }]
    self.cmd_mock.inst.Run()

  def testClearSDKCache(self):
    """Verifies cache directories are removed with --clear-sdk-cache."""
    # Ensure we have checkout type GCLIENT.
    self.PatchObject(os, 'getcwd', return_value=self.chrome_root)

    # Use the default cache location.
    self.SetupCommandMock(extra_args=['--clear-sdk-cache'],
                          default_cache_dir=True)
    chrome_cache = os.path.join(self.chrome_src_dir, 'build/cros_cache')
    self.assertNotExists(chrome_cache)

    self.cmd_mock.inst.Run()
    self.assertExists(chrome_cache)

  def testSeabiosDownload(self):
    """Verify _CreateSeabiosFWSymlinks.

    Create qemu/seabios directory structure with expected symlinks,
    break the symlinks, and verify that they get fixed.
    """
    qemu_share = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/app-emulation/qemu/some-fake-hash/usr/share')
    seabios_share = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/sys-firmware/seabios/some-fake-hash/usr/share')

    # Create qemu subdirectories.
    for share_dir in ['qemu', 'seabios', 'seavgabios']:
      os.makedirs(os.path.join(qemu_share, share_dir))

    def _CreateLink(share, bios_dir, bios):
      src_file = os.path.join(share, bios_dir, bios)
      dest_file = os.path.join(share, 'qemu', bios)
      osutils.Touch(src_file, makedirs=True)
      rel_path = os.path.relpath(src_file, os.path.dirname(dest_file))
      os.symlink(rel_path, dest_file)

    def _VerifyLinks(broken):
      """Verfies that the links are |broken|."""
      qemu_share_dir = os.path.join(qemu_share, 'qemu')
      for link in os.listdir(qemu_share_dir):
        full_link = os.path.join(qemu_share_dir, link)
        self.assertTrue(os.path.islink(full_link))
        self.assertNotEqual(os.path.exists(full_link), broken)

    # Create qemu links.
    for bios in ['bios.bin', 'bios256k.bin']:
      _CreateLink(qemu_share, 'seabios', bios)
    for bios in ['vgabios-vmware.bin', 'vgabios-virtio.bin',
                 'vgabios-stdvga.bin', 'vgabios-qxl.bin',
                 'vgabios-cirrus.bin', 'vgabios.bin']:
      _CreateLink(qemu_share, 'seavgabios', bios)

    # Move the seabios/seavgabios directories into the seabios package, which
    # breaks the links.
    for bios_dir in ['seabios', 'seavgabios']:
      shutil.move(os.path.join(qemu_share, bios_dir),
                  os.path.join(seabios_share, bios_dir))
    _VerifyLinks(broken=True)

    # Run the command and verify the links get fixed.
    self.SetupCommandMock(extra_args=['--download-vm'])
    self.cmd_mock.inst.Run()
    _VerifyLinks(broken=False)

  def testSymlinkCache(self):
    """Ensures the symlink cache contains valid links to the tarball cache."""
    self.SetupCommandMock()
    self.cmd_mock.inst.Run()

    board, version, _ = self.VERSION_KEY
    toolchain_dir = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/target_toolchain/some-fake-hash')
    sysroot_dir = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/sysroot_chromeos-base_chromeos-chrome.tar.xz/'
        'some-fake-hash')
    self.assertExists(toolchain_dir)
    self.assertExists(sysroot_dir)
    toolchain_link = os.path.join(
        self.tempdir,
        'chrome-sdk/symlinks/%s+%s+target_toolchain' % (board, version))
    sysroot_link = os.path.join(
        self.tempdir,
        'chrome-sdk/symlinks/%s+%s+sysroot_chromeos-base_chromeos-'
        'chrome.tar.xz' % (board, version))
    self.assertTrue(os.path.islink(toolchain_link))
    self.assertTrue(os.path.islink(sysroot_link))
    self.assertEqual(os.path.realpath(toolchain_link), toolchain_dir)
    self.assertEqual(os.path.realpath(sysroot_link), sysroot_dir)

  def testSymlinkCacheToolchainOverride(self):
    """Ensures that the SDK picks up an overridden component."""
    sdk = cros_chrome_sdk.SDKFetcher(os.path.join(self.tempdir),
                                     SDKFetcherMock.BOARD)
    board, version, _ = self.VERSION_KEY
    toolchain_link = os.path.join(
        self.tempdir,
        'chrome-sdk/symlinks/%s+%s+target_toolchain' % (board, version))
    components = [sdk.TARGET_TOOLCHAIN_KEY]

    toolchain_url_1 = 'some-fake-gs-path-1'
    toolchain_dir_1 = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/target_toolchain/',
        toolchain_url_1)
    toolchain_url_2 = 'some-fake-gs-path-2'
    toolchain_dir_2 = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/target_toolchain/',
        toolchain_url_2)
    nacl_toolchain_dir = os.path.join(
        self.tempdir,
        'chrome-sdk/tarballs/arm32_toolchain_for_nacl_helper/')

    # Prepare the cache using 'toolchain_url_1'.
    self.sdk_mock.tarball_cache_key_map = {
        sdk.TARGET_TOOLCHAIN_KEY: toolchain_url_1
    }
    with sdk.Prepare(components, toolchain_url=toolchain_url_1):
      self.assertEqual(toolchain_dir_1, os.path.realpath(toolchain_link))
      self.assertExists(toolchain_dir_1)
      self.assertNotExists(toolchain_dir_2)

    # Prepare the cache with 'toolchain_url_2' and make sure the active symlink
    # points to it and that 'toolchain_url_1' is still present.
    self.sdk_mock.tarball_cache_key_map = {
        sdk.TARGET_TOOLCHAIN_KEY: toolchain_url_2
    }
    with sdk.Prepare(components, toolchain_url=toolchain_url_2):
      self.assertEqual(toolchain_dir_2, os.path.realpath(toolchain_link))
      self.assertExists(toolchain_dir_2)
      self.assertExists(toolchain_dir_1)

    # Test that arm32 toolchain is fetched for NaCl for arm64.
    with sdk.Prepare(components, toolchain_url=toolchain_url_2,
                     target_tc='aarch64-cros-linux-gnu'):
      self.assertExists(nacl_toolchain_dir)

class GomaTest(cros_test_lib.MockTempDirTestCase,
               cros_test_lib.LoggingTestCase):
  """Test Goma setup functionality."""

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    self.cmd_mock = MockChromeSDKCommand(
        ['--board', SDKFetcherMock.BOARD, 'true'],
        base_args=['--cache-dir', str(self.tempdir)])
    self.StartPatcher(self.cmd_mock)

  def VerifyGomaError(self):
    self.assertRaises(cros_chrome_sdk.GomaError, self.cmd_mock.inst._SetupGoma)

  def testNoGomaPort(self):
    """We print an error when gomacc is not returning a port."""
    self.rc_mock.AddCmdResult(
        cros_chrome_sdk.ChromeSDKCommand.GOMACC_PORT_CMD)
    self.VerifyGomaError()

  def testGomaccError(self):
    """We print an error when gomacc exits with nonzero returncode."""
    self.rc_mock.AddCmdResult(
        cros_chrome_sdk.ChromeSDKCommand.GOMACC_PORT_CMD, returncode=1)
    self.VerifyGomaError()

  def testSetupError(self):
    """We print an error when we can't fetch Goma."""
    self.rc_mock.AddCmdResult(
        cros_chrome_sdk.ChromeSDKCommand.GOMACC_PORT_CMD, returncode=1)
    self.VerifyGomaError()

  def testGomaStart(self):
    """Test that we start Goma if it's not already started."""
    # Duplicate return values.
    self.PatchObject(cros_chrome_sdk.ChromeSDKCommand, '_GomaDir',
                     side_effect=['XXXX'])
    self.PatchObject(cros_chrome_sdk.ChromeSDKCommand, '_GomaPort',
                     side_effect=['XXXX', 'XXXX'])
    goma_dir, goma_port = self.cmd_mock.inst._SetupGoma()
    self.assertEqual(goma_port, 'XXXX')
    self.assertTrue(bool(goma_dir))


class HasInternalConfigTest(cros_test_lib.MockTempDirTestCase):
  """Tests the various GS calls in _HasInternalConfig()."""

  def setUp(self):
    self.src_dir = os.path.join(self.tempdir, 'src')
    osutils.SafeMakedirs(os.path.join(self.src_dir, 'chrome'))
    self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
    self.gs_mock.SetDefaultCmdResult()
    self.cache_dir = os.path.join(self.tempdir, 'cache')

    self.sdk = cros_chrome_sdk.SDKFetcher(
        self.cache_dir, SDKFetcherMock.BOARD,
        chrome_src=self.src_dir,
        use_external_config=True)

  def testNotAuthed(self):
    """Covers the case when the initial ls of the release bucket fails."""
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex(f'ls .*gs://{constants.RELEASE_GS_BUCKET}'),
        side_effect=gs.GSCommandError('some ACL error'))
    self.assertFalse(self.sdk._HasInternalConfig(self.cache_dir))

  def testFoundInToTConfig(self):
    """Covers the case when the board is found in the ToT file."""
    osutils.WriteFile(
        os.path.join(self.src_dir, 'chrome', 'VERSION'), 'MAJOR=123')
    # No 'ls' results should make it fallback to using the ToT file.
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('ls .*gs://{constants.RELEASE_GS_BUCKET}'),
        stdout='')

    # Check against the top-level 'boards' key.
    config_contents = json.dumps({
        'boards': [
            {
                'name': SDKFetcherMock.BOARD,
                'configs': [
                    {
                        'builder': 'RELEASE',
                    }
                ],
            }
        ]
    })
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/build_config.ToT.json'),
        stdout=config_contents)
    self.assertTrue(self.sdk._HasInternalConfig(self.cache_dir))

    # Check against the top-level 'reference_board_unified_builds' key.
    config_contents = json.dumps({
        'reference_board_unified_builds': [
            {
                'name': SDKFetcherMock.BOARD,
                'builder': 'RELEASE',
            }
        ]
    })
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/build_config.ToT.json'),
        stdout=config_contents)
    self.assertTrue(self.sdk._HasInternalConfig(self.cache_dir))

  def testFoundInBranchConfig(self):
    """Covers the case when the board is found in a branch file."""
    osutils.WriteFile(
        os.path.join(self.src_dir, 'chrome', 'VERSION'), 'MAJOR=123')
    branch_config_file = 'build_config.release-R123-12345.B.json'
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex(f'ls .*gs://{constants.RELEASE_GS_BUCKET}'),
        stdout=f'gs://{constants.RELEASE_GS_BUCKET}/{branch_config_file}')
    config_contents = json.dumps({
        'reference_board_unified_builds': [
            {
                'name': SDKFetcherMock.BOARD,
                'builder': 'RELEASE',
            }
        ]
    })
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex(
            f'cat .*gs://{constants.RELEASE_GS_BUCKET}/{branch_config_file}'),
        stdout=config_contents)
    # Our board was listed in the branch file, so should return True.
    self.assertTrue(self.sdk._HasInternalConfig(self.cache_dir))

  def testNotFoundInConfig(self):
    """Covers the case when the board is not found in a config file."""
    osutils.WriteFile(
        os.path.join(self.src_dir, 'chrome', 'VERSION'), 'MAJOR=123')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('ls .*gs://{constants.RELEASE_GS_BUCKET}'),
        stdout='')
    config_contents = json.dumps({
        'boards': [
            {
                'name': 'not-our-board',
                'builder': 'RELEASE',
            }
        ]
    })
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/build_config.ToT.json'),
        stdout=config_contents)
    # Our board wasn't listed in the ToT file, so should return False.
    self.assertFalse(self.sdk._HasInternalConfig(self.cache_dir))


class VersionTest(cros_test_lib.MockTempDirTestCase,
                  cros_test_lib.LoggingTestCase):
  """Tests the determination of which SDK version to use."""

  VERSION = '3543.0.0'
  FULL_VERSION = 'R55-%s' % VERSION
  RECENT_VERSION_MISSING = '3542.0.0'
  RECENT_VERSION_FOUND = '3541.0.0'
  FULL_VERSION_RECENT = 'R55-%s' % RECENT_VERSION_FOUND
  NON_CANARY_VERSION = '3543.2.1'
  FULL_VERSION_NON_CANARY = 'R55-%s' % NON_CANARY_VERSION
  BOARD = 'eve'

  VERSION_BASE = ('gs://chromeos-image-archive/%s-release/LATEST-%s'
                  % (BOARD, VERSION))

  CAT_ERROR = 'CommandException: No URLs matched %s' % VERSION_BASE
  LS_ERROR = 'CommandException: One or more URLs matched no objects.'

  def setUp(self):
    self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
    self.gs_mock.SetDefaultCmdResult()
    self.sdk_mock = self.StartPatcher(SDKFetcherMock(
        external_mocks=[self.gs_mock]))

    os.environ.pop(cros_chrome_sdk.SDKFetcher.SDK_VERSION_ENV, None)
    self.sdk = cros_chrome_sdk.SDKFetcher(
        os.path.join(self.tempdir, 'cache'), self.BOARD)

  def testUpdateDefaultChromeVersion(self):
    """We pick up the right LKGM version from the Chrome tree."""
    dir_struct = [
        'gclient_root/.gclient'
    ]
    cros_test_lib.CreateOnDiskHierarchy(self.tempdir, dir_struct)
    gclient_root = os.path.join(self.tempdir, 'gclient_root')
    self.PatchObject(os, 'getcwd', return_value=gclient_root)

    lkgm_file = os.path.join(gclient_root, 'src', constants.PATH_TO_CHROME_LKGM)
    osutils.Touch(lkgm_file, makedirs=True)
    osutils.WriteFile(lkgm_file, self.VERSION)

    self.sdk_mock.UnMockAttr('UpdateDefaultVersion')
    self.sdk.UpdateDefaultVersion()
    self.assertEqual(self.sdk.GetDefaultVersion(),
                     self.VERSION)

  def testFullVersionFromFullVersion(self):
    """Test that a fully specified version is allowed."""
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        stdout=self.FULL_VERSION)
    self.assertEqual(
        self.FULL_VERSION,
        self.sdk.GetFullVersion(self.FULL_VERSION))

  def testFullVersionFromPlatformVersion(self):
    """Test full version calculation from the platform version."""
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        stdout=self.FULL_VERSION)
    self.assertEqual(
        self.FULL_VERSION,
        self.sdk.GetFullVersion(self.VERSION))

  def _SetupMissingVersions(self):
    """Version & Version-1 are missing, but Version-2 exists."""
    def _RaiseGSNoSuchKey(*_args, **_kwargs):
      raise gs.GSNoSuchKey('file does not exist')
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        side_effect=_RaiseGSNoSuchKey)
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex(
            'cat .*/LATEST-%s' % self.RECENT_VERSION_MISSING),
        side_effect=_RaiseGSNoSuchKey)
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.RECENT_VERSION_FOUND),
        stdout=self.FULL_VERSION_RECENT)

  def testNoFallbackVersion(self):
    """Test that all versions are checked before raising an exception."""
    def _RaiseGSNoSuchKey(*_args, **_kwargs):
      raise gs.GSNoSuchKey('file does not exist')

    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-*'),
        side_effect=_RaiseGSNoSuchKey)
    self.sdk.fallback_versions = 2000000
    with cros_test_lib.LoggingCapturer() as logs:
      self.assertRaises(cros_chrome_sdk.MissingSDK, self.sdk.GetFullVersion,
                        self.VERSION)
    self.AssertLogsContain(logs, 'LATEST-1.0.0')
    self.AssertLogsContain(logs, 'LATEST--1.0.0', inverted=True)

  def testFallbackVersions(self):
    """Test full version calculation with various fallback version counts."""
    self._SetupMissingVersions()
    for version in range(6):
      self.sdk.fallback_versions = version
      # _SetupMissingVersions mocks the result of 3 files.
      # The file ending with LATEST-3.0.0 is the only one that would pass.
      if version < 3:
        self.assertRaises(cros_chrome_sdk.MissingSDK, self.sdk.GetFullVersion,
                          self.VERSION)
      else:
        self.assertEqual(
            self.FULL_VERSION_RECENT,
            self.sdk.GetFullVersion(self.VERSION))

  def testFullVersionCaching(self):
    """Test full version calculation and caching."""
    def RaiseException(*_args, **_kwargs):
      raise Exception('boom')

    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        stdout=self.FULL_VERSION)
    self.assertEqual(
        self.FULL_VERSION,
        self.sdk.GetFullVersion(self.VERSION))
    # Test that we access the cache on the next call, rather than checking GS.
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        side_effect=RaiseException)
    self.assertEqual(
        self.FULL_VERSION,
        self.sdk.GetFullVersion(self.VERSION))
    # Test that we access GS again if the board is changed.
    self.sdk.board += '2'
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.VERSION),
        stdout=self.FULL_VERSION + '2')
    self.assertEqual(
        self.FULL_VERSION + '2',
        self.sdk.GetFullVersion(self.VERSION))

  def testNoLatestVersion(self):
    """We raise an exception when there is no recent latest version."""
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-*'),
        stdout='', stderr=self.CAT_ERROR, returncode=1)
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('ls .*%s' % self.VERSION),
        stdout='', stderr=self.LS_ERROR, returncode=1)
    self.assertRaises(cros_chrome_sdk.MissingSDK, self.sdk.GetFullVersion,
                      self.VERSION)

  def testNonCanaryFullVersion(self):
    """Test full version calculation for a non canary version."""
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.NON_CANARY_VERSION),
        stdout=self.FULL_VERSION_NON_CANARY)
    self.assertEqual(
        self.FULL_VERSION_NON_CANARY,
        self.sdk.GetFullVersion(self.NON_CANARY_VERSION))

  def testNonCanaryNoLatestVersion(self):
    """We raise an exception when there is no matching latest non canary."""
    self.sdk_mock.UnMockAttr('GetFullVersion')
    self.gs_mock.AddCmdResult(
        partial_mock.ListRegex('cat .*/LATEST-%s' % self.NON_CANARY_VERSION),
        stdout='', stderr=self.CAT_ERROR, returncode=1)
    # Set any other query to return a valid version, but we don't expect that
    # to occur for non canary versions.
    self.gs_mock.SetDefaultCmdResult(stdout=self.FULL_VERSION_NON_CANARY)
    self.assertRaises(cros_chrome_sdk.MissingSDK, self.sdk.GetFullVersion,
                      self.NON_CANARY_VERSION)

  def testDefaultEnvBadBoard(self):
    """We don't use the version in the environment if board doesn't match."""
    os.environ[cros_chrome_sdk.SDKFetcher.SDK_VERSION_ENV] = self.VERSION
    self.assertNotEqual(self.VERSION, self.sdk_mock.VERSION)
    self.assertEqual(self.sdk.GetDefaultVersion(), None)

  def testDefaultEnvGoodBoard(self):
    """We use the version in the environment if board matches."""
    sdk_version_env = cros_chrome_sdk.SDKFetcher.SDK_VERSION_ENV
    os.environ[sdk_version_env] = self.VERSION
    os.environ[cros_chrome_sdk.SDKFetcher.SDK_BOARD_ENV] = self.BOARD
    self.assertEqual(self.sdk.GetDefaultVersion(), self.VERSION)


class PathVerifyTest(cros_test_lib.MockTempDirTestCase,
                     cros_test_lib.LoggingTestCase):
  """Tests user_rc PATH validation and warnings."""

  def testPathVerifyWarnings(self):
    """Test the user rc PATH verification codepath."""
    def SourceEnvironmentMock(*_args, **_kwargs):
      return {
          'PATH': ':'.join([os.path.dirname(p) for p in abs_paths]),
      }

    self.PatchObject(osutils, 'SourceEnvironment',
                     side_effect=SourceEnvironmentMock)
    file_list = (
        'goma/goma_ctl.py',
        'clang/clang',
        'chromite/parallel_emerge',
    )
    abs_paths = [os.path.join(self.tempdir, relpath) for relpath in file_list]
    for p in abs_paths:
      osutils.Touch(p, makedirs=True, mode=0o755)

    with cros_test_lib.LoggingCapturer() as logs:
      cros_chrome_sdk.ChromeSDKCommand._VerifyGoma(None)
      cros_chrome_sdk.ChromeSDKCommand._VerifyChromiteBin(None)

    for msg in ['managed Goma', 'default Chromite']:
      self.AssertLogsMatch(logs, msg)


class ClearOldItemsTest(cros_test_lib.MockTempDirTestCase,
                        cros_test_lib.LoggingTestCase):
  """Tests SDKFetcher.ClearOldItems() behavior."""

  def setUp(self):
    """Sets up a temporary symlink & tarball cache."""
    self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
    self.gs_mock.SetDefaultCmdResult()

    self.sdk_fetcher = cros_chrome_sdk.SDKFetcher(
        self.tempdir, None, use_external_config=True)

  def testBrokenSymlinkCleared(self):
    """Adds a broken symlink and ensures it gets removed."""
    osutils.Touch(os.path.join(self.tempdir, 'some-file'))
    valid_link_ref = self.sdk_fetcher.symlink_cache.Lookup('some-valid-link')
    with valid_link_ref:
      self.sdk_fetcher._UpdateCacheSymlink(
          valid_link_ref, os.path.join(self.tempdir, 'some-file'))

    broken_link_ref = self.sdk_fetcher.symlink_cache.Lookup('some-broken-link')
    with broken_link_ref:
      self.sdk_fetcher._UpdateCacheSymlink(
          broken_link_ref, '/some/invalid/file')

    # Broken symlink should exist before the ClearOldItems() call, and be
    # removed after.
    self.assertTrue(valid_link_ref.Exists())
    self.assertTrue(broken_link_ref.Exists())
    cros_chrome_sdk.SDKFetcher.ClearOldItems(self.tempdir)
    self.assertTrue(valid_link_ref.Exists())
    self.assertFalse(broken_link_ref.Exists())
