# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Image API unittests."""

import errno
import os
from pathlib import Path

from chromite.lib import chroot_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import sysroot_lib
from chromite.service import image


class BuildImageTest(cros_test_lib.RunCommandTempDirTestCase):
  """Build Image tests."""

  def setUp(self):
    osutils.Touch(
        os.path.join(self.tempdir, image.PARALLEL_EMERGE_STATUS_FILE_NAME))
    self.PatchObject(osutils.TempDir, '__enter__', return_value=self.tempdir)
    self.PatchObject(portage_util, 'GetBoardUseFlags', return_value='')

  def testCommand(self):
    """Test the build_image command."""
    image.Build('board', [constants.IMAGE_TYPE_BASE])
    self.assertCommandContains(
        [Path(constants.CROSUTILS_DIR) / 'build_image.sh'])

  def testBuildBoardHandling(self):
    """Test the argument handling."""
    # No board should raise an error.
    with self.assertRaises(image.InvalidArgumentError):
      image.Build(None, [constants.IMAGE_TYPE_BASE])

    with self.assertRaises(image.InvalidArgumentError):
      image.Build('', [constants.IMAGE_TYPE_BASE])

    # Should be using the passed board.
    image.Build('board', [constants.IMAGE_TYPE_BASE])
    self.assertCommandContains(['--board', 'board'])

  def testBuildImageTypes(self):
    """Test the image type handling."""
    result = image.Build('board', [])
    assert result.all_built and not result.build_run

    # Should be using the argument when passed.
    image.Build('board', [constants.IMAGE_TYPE_DEV])
    self.assertCommandContains(
        [constants.IMAGE_TYPE_TO_NAME[constants.IMAGE_TYPE_DEV]])

    # Multiple should all be passed.
    multi = [
        constants.IMAGE_TYPE_BASE,
        constants.IMAGE_TYPE_DEV,
        constants.IMAGE_TYPE_TEST,
    ]
    image.Build('board', multi)
    for x in multi:
      self.assertCommandContains([constants.IMAGE_TYPE_TO_NAME[x]])

    # Building RECOVERY only should cause base to be built.
    image.Build('board', [constants.IMAGE_TYPE_RECOVERY])
    self.assertCommandContains(
        [constants.IMAGE_TYPE_TO_NAME[constants.IMAGE_TYPE_BASE]])

  def testInvalidBuildImageTypes(self):
    """Test the image type handling with invalid input."""
    build_result = image.Build(
        'board', [constants.IMAGE_TYPE_BASE, constants.FACTORY_IMAGE_BIN])
    self.assertEqual(build_result.return_code, errno.EINVAL)


class BuildConfigTest(cros_test_lib.MockTestCase):
  """BuildConfig tests."""

  def testGetArguments(self):
    """GetArguments tests."""
    config = image.BuildConfig()
    self.assertIn('--script-is-run-only-by-chromite-and-not-users',
                  config.GetArguments())

    # Make sure each arg produces the correct argument individually.
    config = image.BuildConfig(builder_path='test_builder_path')
    self.assertIn('--builder_path', config.GetArguments())
    self.assertIn('test_builder_path', config.GetArguments())

    config = image.BuildConfig(disk_layout='disk')
    self.assertIn('--disk_layout', config.GetArguments())
    self.assertIn('disk', config.GetArguments())

    config = image.BuildConfig(enable_rootfs_verification=False)
    self.assertIn('--noenable_rootfs_verification', config.GetArguments())

    config = image.BuildConfig(replace=True)
    self.assertIn('--replace', config.GetArguments())

    config = image.BuildConfig(version='build_version')
    self.assertIn('--version', config.GetArguments())
    self.assertIn('build_version', config.GetArguments())

    config = image.BuildConfig(build_attempt=12)
    self.assertIn('--build_attempt', config.GetArguments())
    self.assertIn('12', config.GetArguments())

    config = image.BuildConfig(symlink='test_symlink')
    self.assertIn('--symlink', config.GetArguments())
    self.assertIn('test_symlink', config.GetArguments())

    config = image.BuildConfig(output_dir_suffix='test_output_suffix')
    self.assertIn('--output_suffix', config.GetArguments())
    self.assertIn('test_output_suffix', config.GetArguments())

    config = image.BuildConfig(adjust_partition='ROOT-A:+1G')
    self.assertIn('--adjust_part', config.GetArguments())
    self.assertIn('ROOT-A:+1G', config.GetArguments())

    config = image.BuildConfig(boot_args='initrd')
    self.assertIn('--boot_args', config.GetArguments())
    self.assertIn('initrd', config.GetArguments())

    config = image.BuildConfig(enable_bootcache=True)
    self.assertIn('--enable_bootcache', config.GetArguments())

    config = image.BuildConfig(output_root='test/output/dir')
    self.assertIn('--output_root', config.GetArguments())
    self.assertIn('test/output/dir', config.GetArguments())

    config = image.BuildConfig(build_root='test/build/dir')
    self.assertIn('--build_root', config.GetArguments())
    self.assertIn('test/build/dir', config.GetArguments())

    config = image.BuildConfig(enable_serial='ttyS1')
    self.assertIn('--enable_serial', config.GetArguments())
    self.assertIn('ttyS1', config.GetArguments())

    config = image.BuildConfig(kernel_loglevel=4)
    self.assertIn('--loglevel', config.GetArguments())
    self.assertIn('4', config.GetArguments())

    config = image.BuildConfig(jobs=40)
    self.assertIn('--jobs', config.GetArguments())
    self.assertIn('40', config.GetArguments())

    config = image.BuildConfig(eclean=False)
    self.assertIn('--noeclean', config.GetArguments())


class CreateVmTest(cros_test_lib.RunCommandTestCase):
  """Create VM tests."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)

  def testNoBoardFails(self):
    """Should fail when not given a valid board-ish value."""
    with self.assertRaises(AssertionError):
      image.CreateVm('')

  def testBoardArgument(self):
    """Test the board argument."""
    image.CreateVm('board')
    self.assertCommandContains(['--board', 'board'])

  def testTestImage(self):
    """Test the application of the --test_image argument."""
    image.CreateVm('board', is_test=True)
    self.assertCommandContains(['--test_image'])

  def testNonTestImage(self):
    """Test the non-application of the --test_image argument."""
    image.CreateVm('board', is_test=False)
    self.assertCommandContains(['--test_image'], expected=False)

  def testDiskLayout(self):
    """Test the application of the --disk_layout argument."""
    image.CreateVm('board', disk_layout='5000PB')
    self.assertCommandContains(['--disk_layout', '5000PB'])

  def testCommandError(self):
    """Test handling of an error when running the command."""
    self.rc.SetDefaultCmdResult(returncode=1)
    with self.assertRaises(image.ImageToVmError):
      image.CreateVm('board')

  def testResultPath(self):
    """Test the path building."""
    self.PatchObject(image_lib, 'GetLatestImageLink', return_value='/tmp')
    self.assertEqual(
        os.path.join('/tmp', constants.VM_IMAGE_BIN), image.CreateVm('board'))


class CopyBaseToRecoveryTest(cros_test_lib.MockTempDirTestCase):
  """Tests the CopyBaseToRecovery method."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)
    self.PatchObject(Path, 'exists', return_value=True)
    self.base_image = self.tempdir / constants.BASE_IMAGE_BIN
    self.recovery_image = self.tempdir / constants.RECOVERY_IMAGE_BIN

  def testCopyRecoveryImage(self):
    self.base_image.touch()
    result = image.CopyBaseToRecovery('board', self.base_image)

    self.assertEqual(result.return_code, 0)
    self.assertEqual(result.images[constants.IMAGE_TYPE_RECOVERY],
                     self.recovery_image)
    self.assertExists(self.recovery_image)

  def testCopyRecoveryImageInvalid(self):
    result = image.CopyBaseToRecovery('board', self.base_image)

    self.assertNotEqual(result.return_code, 0)
    self.assertNotExists(self.recovery_image)

class BuildRecoveryTest(cros_test_lib.RunCommandTestCase):
  """Create recovery image tests."""

  def setUp(self):
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)

  def testNoBoardFails(self):
    """Should fail when not given a valid board-ish value."""
    with self.assertRaises(image.InvalidArgumentError):
      image.BuildRecoveryImage('')

  def testBoardArgument(self):
    """Test the board argument."""
    image.BuildRecoveryImage('board')
    self.assertCommandContains(['--board', 'board'])


class ImageTestTest(cros_test_lib.RunCommandTempDirTestCase):
  """Image Test tests."""

  def setUp(self):
    """Setup the filesystem."""
    self.board = 'board'
    self.chroot_container = os.path.join(self.tempdir, 'outside')
    self.outside_result_dir = os.path.join(self.chroot_container, 'results')
    self.inside_result_dir_inside = '/inside/results_inside'
    self.inside_result_dir_outside = os.path.join(self.chroot_container,
                                                  'inside/results_inside')
    self.image_dir_inside = '/inside/build/board/latest'
    self.image_dir_outside = os.path.join(self.chroot_container,
                                          'inside/build/board/latest')

    D = cros_test_lib.Directory
    filesystem = (D('outside', (
        D('results', ()),
        D('inside', (
            D('results_inside', ()),
            D('build', (D('board',
                          (D('latest',
                             ('%s.bin' % constants.BASE_IMAGE_NAME,)),)),)),
        )),
    )),)

    cros_test_lib.CreateOnDiskHierarchy(self.tempdir, filesystem)

  def testTestFailsInvalidArguments(self):
    """Test invalid arguments are correctly failed."""
    with self.assertRaises(image.InvalidArgumentError):
      image.Test(None, None)
    with self.assertRaises(image.InvalidArgumentError):
      image.Test('', '')
    with self.assertRaises(image.InvalidArgumentError):
      image.Test(None, self.outside_result_dir)
    with self.assertRaises(image.InvalidArgumentError):
      image.Test(self.board, None)

  def testTestInsideChrootAllProvided(self):
    """Test behavior when inside the chroot and all paths provided."""
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)
    image.Test(
        self.board, self.outside_result_dir, image_dir=self.image_dir_inside)

    # Inside chroot shouldn't need to do any path manipulations, so we should
    # see exactly what we called it with.
    self.assertCommandContains([
        '--board',
        self.board,
        '--test_results_root',
        self.outside_result_dir,
        self.image_dir_inside,
    ])

  def testTestInsideChrootNoImageDir(self):
    """Test image dir generation inside the chroot."""
    mocked_dir = '/foo/bar'
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)
    self.PatchObject(image_lib, 'GetLatestImageLink', return_value=mocked_dir)
    image.Test(self.board, self.outside_result_dir)

    self.assertCommandContains([
        '--board',
        self.board,
        '--test_results_root',
        self.outside_result_dir,
        mocked_dir,
    ])


class TestCreateFactoryImageZip(cros_test_lib.MockTempDirTestCase):
  """Unittests for create_factory_image_zip."""

  def setUp(self):
    # Create a chroot_path.
    self.chroot_path = os.path.join(self.tempdir, 'chroot_dir')
    self.chroot = chroot_lib.Chroot(path=self.chroot_path)
    self.sysroot_path = os.path.join(self.chroot_path, 'build', 'target')
    self.sysroot = sysroot_lib.Sysroot(path=self.sysroot_path)

    # Create appropriate sysroot structure.
    osutils.SafeMakedirs(self.sysroot_path)
    factory_bundle_path = self.chroot.full_path(self.sysroot.path, 'usr',
                                                'local', 'factory', 'bundle')
    osutils.SafeMakedirs(factory_bundle_path)
    osutils.Touch(os.path.join(factory_bundle_path, 'bundle_foo'))

    # Create factory shim directory.
    self.factory_shim_path = os.path.join(self.tempdir, 'factory_shim_dir')
    osutils.SafeMakedirs(self.factory_shim_path)
    osutils.Touch(os.path.join(self.factory_shim_path, 'factory_install.bin'))
    osutils.Touch(os.path.join(self.factory_shim_path, 'partition'))
    osutils.SafeMakedirs(os.path.join(self.factory_shim_path, 'netboot'))
    osutils.Touch(os.path.join(self.factory_shim_path, 'netboot', 'bar'))

    # Create output dir.
    self.output_dir = os.path.join(self.tempdir, 'output_dir')
    osutils.SafeMakedirs(self.output_dir)

  def test(self):
    """create_factory_image_zip calls cbuildbot/commands with correct args."""
    version = '1.2.3.4'
    output_file = image.create_factory_image_zip(self.chroot, self.sysroot,
                                                 Path(self.factory_shim_path),
                                                 version, self.output_dir)

    # Check that all expected files are present.
    zip_contents = cros_build_lib.run(['zipinfo', '-1', output_file],
                                      cwd=self.output_dir,
                                      stdout=True)
    zip_files = sorted(zip_contents.output.decode('UTF-8').strip().split('\n'))
    expected_files = sorted([
        'factory_shim_dir/netboot/',
        'factory_shim_dir/netboot/bar',
        'factory_shim_dir/factory_install.bin',
        'factory_shim_dir/partition',
        'bundle_foo',
        'BUILD_VERSION',
    ])
    self.assertListEqual(zip_files, expected_files)

    # Check contents of BUILD_VERSION.
    cmd = ['unzip', '-p', output_file, 'BUILD_VERSION']
    version_file = cros_build_lib.run(cmd, cwd=self.output_dir, stdout=True)
    self.assertEqual(version_file.output.decode('UTF-8').strip(), version)
