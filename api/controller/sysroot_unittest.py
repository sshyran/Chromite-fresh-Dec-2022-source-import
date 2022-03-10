# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sysroot controller tests."""

import datetime
import os

from chromite.api import api_config
from chromite.api import controller
from chromite.api.controller import controller_util
from chromite.api.controller import sysroot as sysroot_controller
from chromite.api.gen.chromite.api import sysroot_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import binpkg
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.lib import sysroot_lib
from chromite.lib.parser import package_info
from chromite.service import sysroot as sysroot_service


class CreateTest(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Create function tests."""

  def _InputProto(self, build_target=None, profile=None, replace=False,
                  current=False, package_indexes=None):
    """Helper to build and input proto instance."""
    proto = sysroot_pb2.SysrootCreateRequest()
    if build_target:
      proto.build_target.name = build_target
    if profile:
      proto.profile.name = profile
    if replace:
      proto.flags.replace = replace
    if current:
      proto.flags.chroot_current = current
    if package_indexes:
      proto.package_indexes.extend(package_indexes)

    return proto

  def _OutputProto(self):
    """Helper to build output proto instance."""
    return sysroot_pb2.SysrootCreateResponse()

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'Create')

    board = 'board'
    profile = None
    force = False
    upgrade_chroot = True
    in_proto = self._InputProto(build_target=board, profile=profile,
                                replace=force, current=not upgrade_chroot)
    sysroot_controller.Create(in_proto, self._OutputProto(),
                              self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'Create')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.Create(request, response, self.mock_call_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_SUCCESS, rc)

  def testMockError(self):
    """Sanity check that a mock error does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'Create')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.Create(request, response, self.mock_error_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_UNRECOVERABLE, rc)

  def testArgumentValidation(self):
    """Test the input argument validation."""
    # Error when no name provided.
    in_proto = self._InputProto()
    out_proto = self._OutputProto()
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.Create(in_proto, out_proto, self.api_config)

    # Valid when board passed.
    result = sysroot_lib.Sysroot('/sysroot/path')
    patch = self.PatchObject(sysroot_service, 'Create', return_value=result)
    in_proto = self._InputProto('board')
    out_proto = self._OutputProto()
    sysroot_controller.Create(in_proto, out_proto, self.api_config)
    patch.assert_called_once()

  def testArgumentHandling(self):
    """Test the arguments get processed and passed correctly."""
    sysroot_path = '/sysroot/path'

    sysroot = sysroot_lib.Sysroot(sysroot_path)
    create_patch = self.PatchObject(sysroot_service, 'Create',
                                    return_value=sysroot)
    rc_patch = self.PatchObject(sysroot_service, 'SetupBoardRunConfig')

    # Default values.
    board = 'board'
    profile = None
    force = False
    upgrade_chroot = True
    in_proto = self._InputProto(build_target=board, profile=profile,
                                replace=force, current=not upgrade_chroot)
    out_proto = self._OutputProto()
    sysroot_controller.Create(in_proto, out_proto, self.api_config)

    # Default value checks.
    rc_patch.assert_called_with(force=force, upgrade_chroot=upgrade_chroot,
                                package_indexes=[])
    self.assertEqual(board, out_proto.sysroot.build_target.name)
    self.assertEqual(sysroot_path, out_proto.sysroot.path)

    # Not default values.
    create_patch.reset_mock()
    board = 'board'
    profile = 'profile'
    force = True
    upgrade_chroot = False
    package_indexes = [
        common_pb2.PackageIndexInfo(
            snapshot_sha='SHA', snapshot_number=5,
            build_target=common_pb2.BuildTarget(name=board),
            location='LOCATION', profile=common_pb2.Profile(name=profile)),
        common_pb2.PackageIndexInfo(
            snapshot_sha='SHA2', snapshot_number=4,
            build_target=common_pb2.BuildTarget(name=board),
            location='LOCATION2', profile=common_pb2.Profile(name=profile))]

    in_proto = self._InputProto(build_target=board, profile=profile,
                                replace=force, current=not upgrade_chroot,
                                package_indexes=package_indexes)
    out_proto = self._OutputProto()
    sysroot_controller.Create(in_proto, out_proto, self.api_config)

    # Not default value checks.
    rc_patch.assert_called_with(
        force=force, package_indexes=[
            binpkg.PackageIndexInfo.from_protobuf(x)
            for x in package_indexes
        ], upgrade_chroot=upgrade_chroot)
    self.assertEqual(board, out_proto.sysroot.build_target.name)
    self.assertEqual(sysroot_path, out_proto.sysroot.path)


class GenerateArchiveTest(cros_test_lib.MockTempDirTestCase,
                          api_config.ApiConfigMixin):
  """GenerateArchive function tests."""

  def setUp(self):
    self.chroot_path = '/path/to/chroot'
    self.board = 'board'

  def _InputProto(self, build_target=None, chroot_path=None, pkg_list=None):
    """Helper to build and input proto instance."""
    # pkg_list will be a list of category/package strings such as
    # ['virtual/target-fuzzers'].
    if pkg_list:
      package_list = []
      for pkg in pkg_list:
        pkg_string_parts = pkg.split('/')
        package_info_msg = common_pb2.PackageInfo(
            category=pkg_string_parts[0],
            package_name=pkg_string_parts[1])
        package_list.append(package_info_msg)
    else:
      package_list = []

    return sysroot_pb2.SysrootGenerateArchiveRequest(
        build_target={'name': build_target},
        chroot={'path': chroot_path},
        packages=package_list)

  def _OutputProto(self):
    """Helper to build output proto instance."""
    return sysroot_pb2.SysrootGenerateArchiveResponse()

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'GenerateArchive')

    in_proto = self._InputProto(build_target=self.board,
                                chroot_path=self.chroot_path,
                                pkg_list=['virtual/target-fuzzers'])
    sysroot_controller.GenerateArchive(in_proto, self._OutputProto(),
                                       self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'GenerateArchive')

    in_proto = self._InputProto(build_target=self.board,
                                chroot_path=self.chroot_path,
                                pkg_list=['virtual/target-fuzzers'])
    sysroot_controller.GenerateArchive(in_proto,
                                       self._OutputProto(),
                                       self.mock_call_config)
    patch.assert_not_called()

  def testArgumentValidation(self):
    """Test the input argument validation."""
    # Error when no build target provided.
    in_proto = self._InputProto()
    out_proto = self._OutputProto()
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.GenerateArchive(in_proto, out_proto, self.api_config)

    # Error when packages is not specified.
    in_proto = self._InputProto(build_target='board',
                                chroot_path=self.chroot_path)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.GenerateArchive(in_proto, out_proto, self.api_config)

    # Valid when board, chroot path, and package are specified.
    patch = self.PatchObject(sysroot_service, 'GenerateArchive',
                             return_value='/path/to/sysroot/tar.bz')
    in_proto = self._InputProto(build_target='board',
                                chroot_path=self.chroot_path,
                                pkg_list=['virtual/target-fuzzers'])
    out_proto = self._OutputProto()
    sysroot_controller.GenerateArchive(in_proto, out_proto, self.api_config)
    patch.assert_called_once()


class InstallToolchainTest(cros_test_lib.MockTempDirTestCase,
                           api_config.ApiConfigMixin):
  """Install toolchain function tests."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)
    # Avoid running the portageq command.
    self.PatchObject(sysroot_controller, '_LogBinhost')
    self.board = 'board'
    self.sysroot = os.path.join(self.tempdir, 'board')
    self.invalid_sysroot = os.path.join(self.tempdir, 'invalid', 'sysroot')
    osutils.SafeMakedirs(self.sysroot)
    # Set up portage log directory.
    self.target_sysroot = sysroot_lib.Sysroot(self.sysroot)
    self.portage_dir = os.path.join(self.tempdir, 'portage_logdir')
    self.PatchObject(
        sysroot_lib.Sysroot, 'portage_logdir', new=self.portage_dir)
    osutils.SafeMakedirs(self.portage_dir)

  def _InputProto(self, build_target=None, sysroot_path=None,
                  compile_source=False):
    """Helper to build an input proto instance."""
    proto = sysroot_pb2.InstallToolchainRequest()
    if build_target:
      proto.sysroot.build_target.name = build_target
    if sysroot_path:
      proto.sysroot.path = sysroot_path
    if compile_source:
      proto.flags.compile_source = compile_source

    return proto

  def _OutputProto(self):
    """Helper to build output proto instance."""
    return sysroot_pb2.InstallToolchainResponse()

  def _CreatePortageLogFile(self, log_path, pkg_info, timestamp):
    """Creates a log file for testing for individual packages built by Portage.

    Args:
      log_path (pathlike): the PORTAGE_LOGDIR path
      pkg_info (PackageInfo): name components for log file.
      timestamp (datetime): timestamp used to name the file.
    """
    path = os.path.join(log_path,
                        f'{pkg_info.category}:{pkg_info.pvr}:' \
                        f'{timestamp.strftime("%Y%m%d-%H%M%S")}.log')
    osutils.WriteFile(path,
                      f'Test log file for package {pkg_info.category}/'
                      f'{pkg_info.package} written to {path}')
    return path

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'InstallToolchain')

    in_proto = self._InputProto(build_target=self.board,
                                sysroot_path=self.sysroot)
    sysroot_controller.InstallToolchain(in_proto, self._OutputProto(),
                                        self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'InstallToolchain')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.InstallToolchain(request, response,
                                             self.mock_call_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_SUCCESS, rc)

  def testMockError(self):
    """Sanity check that a mock error does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'InstallToolchain')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.InstallToolchain(request, response,
                                             self.mock_error_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    self.assertTrue(response.failed_packages)

  def testArgumentValidation(self):
    """Test the argument validation."""
    # Test errors on missing inputs.
    out_proto = self._OutputProto()
    # Both missing.
    in_proto = self._InputProto()
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallToolchain(in_proto, out_proto, self.api_config)

    # Sysroot path missing.
    in_proto = self._InputProto(build_target=self.board)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallToolchain(in_proto, out_proto, self.api_config)

    # Build target name missing.
    in_proto = self._InputProto(sysroot_path=self.sysroot)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallToolchain(in_proto, out_proto, self.api_config)

    # Both provided, but invalid sysroot path.
    in_proto = self._InputProto(build_target=self.board,
                                sysroot_path=self.invalid_sysroot)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallToolchain(in_proto, out_proto, self.api_config)

  def testSuccessOutputHandling(self):
    """Test the output is processed and recorded correctly."""
    self.PatchObject(sysroot_service, 'InstallToolchain')
    out_proto = self._OutputProto()
    in_proto = self._InputProto(build_target=self.board,
                                sysroot_path=self.sysroot)

    rc = sysroot_controller.InstallToolchain(in_proto, out_proto,
                                             self.api_config)
    self.assertFalse(rc)
    self.assertFalse(out_proto.failed_packages)


  def testErrorOutputHandling(self):
    """Test the error output is processed and recorded correctly."""
    out_proto = self._OutputProto()
    in_proto = self._InputProto(build_target=self.board,
                                sysroot_path=self.sysroot)

    err_pkgs = ['cat/pkg-1.0-r1', 'cat2/pkg2-1.0-r1']
    err_cpvs = [package_info.parse(pkg) for pkg in err_pkgs]
    expected = [('cat', 'pkg'), ('cat2', 'pkg2')]

    new_logs = {}
    for i, pkg in enumerate(err_pkgs):
      self._CreatePortageLogFile(self.portage_dir, err_cpvs[i],
                                 datetime.datetime(2021, 6, 9, 13, 37, 0))
      new_logs[pkg] = self._CreatePortageLogFile(self.portage_dir, err_cpvs[i],
                                                 datetime.datetime(2021, 6, 9,
                                                                   16, 20, 0)
                                                 )

    err = sysroot_lib.ToolchainInstallError('Error',
                                            cros_build_lib.CommandResult(),
                                            tc_info=err_cpvs)
    self.PatchObject(sysroot_service, 'InstallToolchain', side_effect=err)

    rc = sysroot_controller.InstallToolchain(in_proto, out_proto,
                                             self.api_config)
    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    self.assertTrue(out_proto.failed_packages)
    self.assertTrue(out_proto.failed_package_data)
    # This needs to return 2 to indicate the available error response.
    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    for data in out_proto.failed_package_data:
      package = controller_util.deserialize_package_info(data.name)
      cat_pkg = (data.name.category, data.name.package_name)
      self.assertIn(cat_pkg, expected)
      self.assertEqual(data.log_path.path, new_logs[package.cpvr])

    # TODO(b/206514844): remove when field is deleted
    for package in out_proto.failed_packages:
      cat_pkg = (package.category, package.package_name)
      self.assertIn(cat_pkg, expected)


class InstallPackagesTest(cros_test_lib.MockTempDirTestCase,
                          api_config.ApiConfigMixin):
  """InstallPackages tests."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)
    # Avoid running the portageq command.
    self.PatchObject(sysroot_controller, '_LogBinhost')
    self.build_target = 'board'
    self.sysroot = os.path.join(self.tempdir, 'build', 'board')
    osutils.SafeMakedirs(self.sysroot)
    # Set up portage log directory.
    self.target_sysroot = sysroot_lib.Sysroot(self.sysroot)
    self.portage_dir = os.path.join(self.tempdir, 'portage_logdir')
    self.PatchObject(
        sysroot_lib.Sysroot, 'portage_logdir', new=self.portage_dir)
    osutils.SafeMakedirs(self.portage_dir)
    # Set up goma directories.
    self.goma_dir = os.path.join(self.tempdir, 'goma_dir')
    osutils.SafeMakedirs(self.goma_dir)
    self.goma_out_dir = os.path.join(self.tempdir, 'goma_out_dir')
    osutils.SafeMakedirs(self.goma_out_dir)
    os.environ['GLOG_log_dir'] = self.goma_dir

  def _InputProto(self, build_target=None, sysroot_path=None,
                  build_source=False, goma_dir=None, goma_log_dir=None,
                  goma_stats_file=None, goma_counterz_file=None,
                  package_indexes=None, packages=None):
    """Helper to build an input proto instance."""
    instance = sysroot_pb2.InstallPackagesRequest()

    if build_target:
      instance.sysroot.build_target.name = build_target
    if sysroot_path:
      instance.sysroot.path = sysroot_path
    if build_source:
      instance.flags.build_source = build_source
    if goma_dir:
      instance.goma_config.goma_dir = goma_dir
    if goma_log_dir:
      instance.goma_config.log_dir.dir = goma_log_dir
    if goma_stats_file:
      instance.goma_config.stats_file = goma_stats_file
    if goma_counterz_file:
      instance.goma_config.counterz_file = goma_counterz_file
    if package_indexes:
      instance.package_indexes.extend(package_indexes)
    if packages:
      for pkg in packages:
        pkg_info = package_info.parse(pkg)
        pkg_info_msg = instance.packages.add()
        controller_util.serialize_package_info(pkg_info, pkg_info_msg)
    return instance

  def _OutputProto(self):
    """Helper to build an empty output proto instance."""
    return sysroot_pb2.InstallPackagesResponse()

  def _CreateGomaLogFile(self, goma_log_dir, name, timestamp):
    """Creates a log file for testing.

    Args:
      goma_log_dir (str): Directory where the file will be created.
      name (str): Log file 'base' name that is combined with the timestamp.
      timestamp (datetime): timestamp that is written to the file.
    """
    path = os.path.join(
        goma_log_dir,
        '%s.host.log.INFO.%s' % (name, timestamp.strftime('%Y%m%d-%H%M%S.%f')))
    osutils.WriteFile(
        path,
        timestamp.strftime('Goma log file created at: %Y/%m/%d %H:%M:%S'))

  def _CreatePortageLogFile(self, log_path, pkg_info, timestamp):
    """Creates a log file for testing for individual packages built by Portage.

    Args:
      log_path (pathlike): the PORTAGE_LOGDIR path
      pkg_info (PackageInfo): name components for log file.
      timestamp (datetime): timestamp used to name the file.
    """
    path = os.path.join(log_path,
                        f'{pkg_info.category}:{pkg_info.pvr}:' \
                        f'{timestamp.strftime("%Y%m%d-%H%M%S")}.log')
    osutils.WriteFile(path, f'Test log file for package {pkg_info.category}/'
                      f'{pkg_info.package} written to {path}')
    return path

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'BuildPackages')

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot)
    sysroot_controller.InstallPackages(in_proto, self._OutputProto(),
                                       self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'BuildPackages')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.InstallPackages(request, response,
                                            self.mock_call_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_SUCCESS, rc)

  def testMockError(self):
    """Sanity check that a mock error does not execute any logic."""
    patch = self.PatchObject(sysroot_service, 'BuildPackages')
    request = self._InputProto()
    response = self._OutputProto()

    rc = sysroot_controller.InstallPackages(request, response,
                                            self.mock_error_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    self.assertTrue(response.failed_packages)

  def testArgumentValidationAllMissing(self):
    """Test missing all arguments."""
    out_proto = self._OutputProto()
    in_proto = self._InputProto()
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallPackages(in_proto, out_proto, self.api_config)

  def testArgumentValidationNoSysroot(self):
    """Test missing sysroot path."""
    out_proto = self._OutputProto()
    in_proto = self._InputProto(build_target=self.build_target)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallPackages(in_proto, out_proto, self.api_config)

  def testArgumentValidationNoBuildTarget(self):
    """Test missing build target name."""
    out_proto = self._OutputProto()
    in_proto = self._InputProto(sysroot_path=self.sysroot)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallPackages(in_proto, out_proto, self.api_config)

  def testArgumentValidationInvalidSysroot(self):
    """Test sysroot that hasn't had the toolchain installed."""
    out_proto = self._OutputProto()
    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot)
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=False)
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallPackages(in_proto, out_proto, self.api_config)

  def testArgumentValidationInvalidPackage(self):
    out_proto = self._OutputProto()
    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot,
                                packages=['package-1.0.0-r2'])
    with self.assertRaises(cros_build_lib.DieSystemExit):
      sysroot_controller.InstallPackages(in_proto, out_proto, self.api_config)

  def testSuccessOutputHandling(self):
    """Test successful call output handling."""
    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot)
    out_proto = self._OutputProto()
    self.PatchObject(sysroot_service, 'BuildPackages')

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    self.assertFalse(rc)
    self.assertFalse(out_proto.failed_packages)

  def testSuccessPackageIndexes(self):
    """Test successful call with package_indexes."""
    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)
    package_indexes = [
        common_pb2.PackageIndexInfo(
            snapshot_sha='SHA', snapshot_number=5,
            build_target=common_pb2.BuildTarget(name='board'),
            location='LOCATION', profile=common_pb2.Profile(name='profile')),
        common_pb2.PackageIndexInfo(
            snapshot_sha='SHA2', snapshot_number=4,
            build_target=common_pb2.BuildTarget(name='board'),
            location='LOCATION2', profile=common_pb2.Profile(name='profile'))]

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot,
                                package_indexes=package_indexes)

    out_proto = self._OutputProto()
    rc_patch = self.PatchObject(sysroot_service, 'BuildPackagesRunConfig')
    self.PatchObject(sysroot_service, 'BuildPackages')

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    self.assertFalse(rc)
    rc_patch.assert_called_with(
        usepkg=True,
        install_debug_symbols=True,
        packages=[],
        package_indexes=[
            binpkg.PackageIndexInfo.from_protobuf(x) for x in package_indexes
        ],
        use_flags=[],
        use_goma=False,
        use_remoteexec=False,
        incremental_build=False,
        setup_board=False,
        dryrun=False)

  def testSuccessWithGomaLogs(self):
    """Test successful call with goma."""
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy',
                            datetime.datetime(2018, 9, 21, 12, 0, 0))
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy-subproc',
                            datetime.datetime(2018, 9, 21, 12, 1, 0))
    self._CreateGomaLogFile(self.goma_dir, 'gomacc',
                            datetime.datetime(2018, 9, 21, 12, 2, 0))

    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot,
                                goma_dir=self.goma_dir,
                                goma_log_dir=self.goma_out_dir)

    out_proto = self._OutputProto()
    self.PatchObject(sysroot_service, 'BuildPackages')

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    self.assertFalse(rc)
    self.assertFalse(out_proto.failed_packages)
    self.assertCountEqual(out_proto.goma_artifacts.log_files, [
        'compiler_proxy-subproc.host.log.INFO.20180921-120100.000000.gz',
        'compiler_proxy.host.log.INFO.20180921-120000.000000.gz',
        'gomacc.host.log.INFO.20180921-120200.000000.tar.gz'])

  def testSuccessWithGomaLogsAndStatsCounterzFiles(self):
    """Test successful call with goma including stats and counterz files."""
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy',
                            datetime.datetime(2018, 9, 21, 12, 0, 0))
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy-subproc',
                            datetime.datetime(2018, 9, 21, 12, 1, 0))
    self._CreateGomaLogFile(self.goma_dir, 'gomacc',
                            datetime.datetime(2018, 9, 21, 12, 2, 0))
    # Create stats and counterz files.
    osutils.WriteFile(os.path.join(self.goma_dir, 'stats.binaryproto'),
                      'File: stats.binaryproto')
    osutils.WriteFile(os.path.join(self.goma_dir, 'counterz.binaryproto'),
                      'File: counterz.binaryproto')

    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot,
                                goma_dir=self.goma_dir,
                                goma_log_dir=self.goma_out_dir,
                                goma_stats_file='stats.binaryproto',
                                goma_counterz_file='counterz.binaryproto')

    out_proto = self._OutputProto()
    self.PatchObject(sysroot_service, 'BuildPackages')

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    self.assertFalse(rc)
    self.assertFalse(out_proto.failed_packages)
    self.assertCountEqual(out_proto.goma_artifacts.log_files, [
        'compiler_proxy-subproc.host.log.INFO.20180921-120100.000000.gz',
        'compiler_proxy.host.log.INFO.20180921-120000.000000.gz',
        'gomacc.host.log.INFO.20180921-120200.000000.tar.gz'])
    # Verify that the output dir has 5 files -- since there should be 3 log
    # files, the stats file, and the counterz file.
    output_files = os.listdir(self.goma_out_dir)
    self.assertCountEqual(output_files, [
        'stats.binaryproto',
        'counterz.binaryproto',
        'compiler_proxy-subproc.host.log.INFO.20180921-120100.000000.gz',
        'compiler_proxy.host.log.INFO.20180921-120000.000000.gz',
        'gomacc.host.log.INFO.20180921-120200.000000.tar.gz'])
    self.assertEqual(out_proto.goma_artifacts.counterz_file,
                     'counterz.binaryproto')
    self.assertEqual(out_proto.goma_artifacts.stats_file,
                     'stats.binaryproto')

  def testFailureMissingGomaStatsCounterzFiles(self):
    """Test successful call with goma including stats and counterz files."""
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy',
                            datetime.datetime(2018, 9, 21, 12, 0, 0))
    self._CreateGomaLogFile(self.goma_dir, 'compiler_proxy-subproc',
                            datetime.datetime(2018, 9, 21, 12, 1, 0))
    self._CreateGomaLogFile(self.goma_dir, 'gomacc',
                            datetime.datetime(2018, 9, 21, 12, 2, 0))
    # Note that stats and counterz files are not created, but are specified in
    # the proto below.

    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot,
                                goma_dir=self.goma_dir,
                                goma_log_dir=self.goma_out_dir,
                                goma_stats_file='stats.binaryproto',
                                goma_counterz_file='counterz.binaryproto')

    out_proto = self._OutputProto()
    self.PatchObject(sysroot_service, 'BuildPackages')

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    self.assertFalse(rc)
    self.assertFalse(out_proto.failed_packages)
    self.assertCountEqual(out_proto.goma_artifacts.log_files, [
        'compiler_proxy-subproc.host.log.INFO.20180921-120100.000000.gz',
        'compiler_proxy.host.log.INFO.20180921-120000.000000.gz',
        'gomacc.host.log.INFO.20180921-120200.000000.tar.gz'])
    self.assertFalse(out_proto.goma_artifacts.counterz_file)
    self.assertFalse(out_proto.goma_artifacts.stats_file)

  def testFailureOutputHandling(self):
    """Test failed package handling."""
    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot)
    out_proto = self._OutputProto()

    # Failed package info and expected list for verification.
    err_pkgs = ['cat/pkg-1.0-r3', 'cat2/pkg2-1.0-r1']
    err_cpvs = [package_info.parse(cpv) for cpv in err_pkgs]
    expected = [('cat', 'pkg'), ('cat2', 'pkg2')]

    new_logs = {}
    for i, pkg in enumerate(err_pkgs):
      self._CreatePortageLogFile(self.portage_dir, err_cpvs[i],
                                 datetime.datetime(2021, 6, 9, 13, 37, 0))
      new_logs[pkg] = self._CreatePortageLogFile(self.portage_dir, err_cpvs[i],
                                                 datetime.datetime(2021, 6, 9,
                                                                   16, 20, 0)
                                                 )
    # Force error to be raised with the packages.
    error = sysroot_lib.PackageInstallError('Error',
                                            cros_build_lib.CommandResult(),
                                            packages=err_cpvs)
    self.PatchObject(sysroot_service, 'BuildPackages', side_effect=error)

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    # This needs to return 2 to indicate the available error response.
    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    for data in out_proto.failed_package_data:
      package = controller_util.deserialize_package_info(data.name)
      cat_pkg = (data.name.category, data.name.package_name)
      self.assertIn(cat_pkg, expected)
      self.assertEqual(data.log_path.path, new_logs[package.cpvr])

    # TODO(b/206514844): remove when field is deleted
    for package in out_proto.failed_packages:
      cat_pkg = (package.category, package.package_name)
      self.assertIn(cat_pkg, expected)

  def testNoPackageFailureOutputHandling(self):
    """Test failure handling without packages to report."""
    # Prevent argument validation error.
    self.PatchObject(sysroot_lib.Sysroot, 'IsToolchainInstalled',
                     return_value=True)

    in_proto = self._InputProto(build_target=self.build_target,
                                sysroot_path=self.sysroot)
    out_proto = self._OutputProto()

    # Force error to be raised with no packages.
    error = sysroot_lib.PackageInstallError('Error',
                                            cros_build_lib.CommandResult(),
                                            packages=[])
    self.PatchObject(sysroot_service, 'BuildPackages', side_effect=error)

    rc = sysroot_controller.InstallPackages(in_proto, out_proto,
                                            self.api_config)
    # All we really care about is it's not 0 or 2 (response available), so
    # test for that rather than a specific return code.
    self.assertTrue(rc)
    self.assertNotEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE,
                        rc)
