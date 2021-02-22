# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the device_imager module."""

import os
import sys
import tempfile

import mock

from chromite.cli import device_imager
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import image_lib
from chromite.lib import image_lib_unittest
from chromite.lib import partial_mock
from chromite.lib import remote_access
from chromite.lib import remote_access_unittest
from chromite.lib.xbuddy import xbuddy


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


# pylint: disable=protected-access


def GetFdPath(fd):
  """Returns the fd path for the current process."""
  return f'/proc/self/fd/{fd}'


class DeviceImagerTest(cros_test_lib.MockTestCase):
  """Tests DeviceImager class methods."""

  def setUp(self):
    """Sets up the class by creating proper mocks."""
    self.rsh_mock = self.StartPatcher(remote_access_unittest.RemoteShMock())
    self.rsh_mock.AddCmdResult(partial_mock.In('${PATH}'), stdout='')
    self.path_env = 'PATH=%s:' % remote_access.DEV_BIN_PATHS

  def test_GetImageLocalFile(self):
    """Tests getting the path to local image."""
    with tempfile.NamedTemporaryFile() as fp:
      di = device_imager.DeviceImager(None, fp.name)
      self.assertEqual(di._GetImage(), (fp.name, device_imager.ImageType.FULL))

  def test_GetImageDir(self):
    """Tests failing on a given directory as a path."""
    di = device_imager.DeviceImager(None, '/tmp')
    with self.assertRaises(ValueError):
      di._GetImage()

  @mock.patch.object(xbuddy.XBuddy, 'Translate', return_value=('eve/R90', None))
  def test_GetImageXBuddyRemote(self, _):
    """Tests getting remote xBuddy image path."""
    di = device_imager.DeviceImager(None, 'xbuddy://remote/eve/latest')
    self.assertEqual(di._GetImage(),
                     ('gs://chromeos-image-archive/eve/R90',
                      device_imager.ImageType.REMOTE_DIRECTORY))

  @mock.patch.object(xbuddy.XBuddy, 'Translate',
                     return_value=('eve/R90', 'path/to/file'))
  def test_GetImageXBuddyLocal(self, _):
    """Tests getting local xBuddy image path."""
    di = device_imager.DeviceImager(None, 'xbuddy://local/eve/latest')
    self.assertEqual(di._GetImage(),
                     ('path/to/file', device_imager.ImageType.FULL))

  def test_SplitDevPath(self):
    """Tests splitting a device path into prefix and partition number."""

    di = device_imager.DeviceImager(None, None)
    self.assertEqual(di._SplitDevPath('/dev/foop3'), ('/dev/foop', 3))

    with self.assertRaises(device_imager.Error):
      di._SplitDevPath('/foo')

    with self.assertRaises(device_imager.Error):
      di._SplitDevPath('/foo/p3p')

  def test_GetKernelState(self):
    """Tests getting the current active and inactive kernel states."""
    di = device_imager.DeviceImager(None, None)
    self.assertEqual(di._GetKernelState(3), (device_imager.DeviceImager.A,
                                             device_imager.DeviceImager.B))
    self.assertEqual(di._GetKernelState(5), (device_imager.DeviceImager.B,
                                             device_imager.DeviceImager.A))

    with self.assertRaises(device_imager.Error):
      di._GetKernelState(1)

  @mock.patch.object(remote_access.ChromiumOSDevice, 'root_dev',
                     return_value='/dev/foop3', new_callable=mock.PropertyMock)
  def test_VerifyBootExpectations(self, _):
    """Tests verifying the boot expectations after reboot."""

    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      di = device_imager.DeviceImager(device, None)
      di._inactive_state = device_imager.DeviceImager.A
      di._VerifyBootExpectations()

  @mock.patch.object(remote_access.ChromiumOSDevice, 'root_dev',
                     return_value='/dev/foop3', new_callable=mock.PropertyMock)
  def test_VerifyBootExpectationsFails(self, _):
    """Tests failure of boot expectations."""

    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      di = device_imager.DeviceImager(device, None)
      di._inactive_state = device_imager.DeviceImager.B
      with self.assertRaises(device_imager.Error):
        di._VerifyBootExpectations()


class TestReaderBase(cros_test_lib.MockTestCase):
  """Test ReaderBase class"""

  def testNamedPipe(self):
    """Tests initializing the class with named pipe."""
    with device_imager.ReaderBase(use_named_pipes=True) as r:
      self.assertIsInstance(r.Target(), str)
      self.assertEqual(r._Source(), r.Target())
      self.assertExists(r.Target())

      r._CloseSource()  # Should not have any effect.
      self.assertExists(r._Source())

    # Closing target should delete the named pipe.
    r.CloseTarget()
    self.assertNotExists(r.Target())

  def testFdPipe(self):
    """Tests initializing the class with normal file descriptor pipes."""
    with device_imager.ReaderBase() as r:
      self.assertIsInstance(r.Target(), int)
      self.assertIsInstance(r._Source(), int)
      self.assertNotEqual(r._Source(), r.Target())
      self.assertExists(GetFdPath(r.Target()))
      self.assertExists(GetFdPath(r._Source()))

      r._CloseSource()
      self.assertNotExists(GetFdPath(r._Source()))
      self.assertExists(GetFdPath(r.Target()))

    r.CloseTarget()
    self.assertNotExists(GetFdPath(r.Target()))

  def testFdPipeCommunicate(self):
    """Tests that file descriptors pipe can actually communicate."""
    with device_imager.ReaderBase() as r:
      with os.fdopen(r._Source(), 'w') as fp:
        fp.write('helloworld')

    with os.fdopen(r.Target(), 'r') as fp:
      self.assertEqual(fp.read(), 'helloworld')


class PartialFileReaderTest(cros_test_lib.RunCommandTestCase):
  """Tests PartialFileReader class."""

  def testRun(self):
    """Tests the main run() function."""
    with device_imager.PartialFileReader(
          '/foo', 512 * 2, 512, cros_build_lib.COMP_GZIP) as pfr:
      pass

    self.assertCommandCalled(
        'dd status=none if=/foo ibs=512 skip=2 count=1 | /usr/bin/pigz',
        stdout=pfr._Source(), shell=True)

    # Make sure the source has been close.
    self.assertNotExists(GetFdPath(pfr._Source()))


class GsFileCopierTest(cros_test_lib.TestCase):
  """Tests GsFileCopier class."""

  @mock.patch.object(gs.GSContext, 'Copy')
  def testRun(self, copy_mock):
    """Tests the run() function."""
    image = 'gs://path/to/image'
    with device_imager.GsFileCopier(image) as gfc:
      self.assertTrue(gfc._use_named_pipes)

    copy_mock.assert_called_with(image, gfc._Source())


class PartitionUpdaterBaseTest(cros_test_lib.TestCase):
  """Tests PartitionUpdaterBase class"""

  def testRunNotImplemented(self):
    """Tests running the main Run() function is not implemented."""
    # We just want to make sure the _Run() function is not implemented here.
    pub = device_imager.PartitionUpdaterBase(None, None, None, None, None)
    with self.assertRaises(NotImplementedError):
      pub.Run()

  def testRevertNotImplemented(self):
    """Tests running the Revert() function is not implemented."""
    pub = device_imager.PartitionUpdaterBase(None, None, None, None, None)
    with self.assertRaises(NotImplementedError):
      pub.Revert()

  @mock.patch.object(device_imager.PartitionUpdaterBase, '_Run')
  def testIsFinished(self, _):
    """Tests IsFinished() function."""
    pub = device_imager.PartitionUpdaterBase(None, None, None, None, None)
    self.assertFalse(pub.IsFinished())
    pub.Run()
    self.assertTrue(pub.IsFinished())


class RawPartitionUpdaterTest(cros_test_lib.MockTempDirTestCase):
  """Tests RawPartitionUpdater class."""

  def setUp(self):
    """Sets up the class by creating proper mocks."""
    self.rsh_mock = self.StartPatcher(remote_access_unittest.RemoteShMock())
    self.rsh_mock.AddCmdResult(partial_mock.In('${PATH}'), stdout='')
    self.path_env = 'PATH=%s:' % remote_access.DEV_BIN_PATHS

  @mock.patch.object(device_imager.RawPartitionUpdater, '_GetPartitionName',
                     return_value=constants.PART_KERN_A)
  @mock.patch.object(image_lib, 'GetImageDiskPartitionInfo',
                     return_value=image_lib_unittest.LOOP_PARTITION_INFO)
  @mock.patch.object(device_imager.PartialFileReader, 'CloseTarget')
  @mock.patch.object(device_imager.PartialFileReader, 'run')
  def test_RunFullImage(self, run_mock, close_mock, _, name_mock):
    """Test main Run() function for full image.

    This function should parts of the source image and write it into the device
    using proper compression programs.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      self.rsh_mock.AddCmdResult([partial_mock.In('which'), 'gzip'],
                                 returncode=0)
      self.rsh_mock.AddCmdResult(
        self.path_env +
        ' gzip --decompress --stdout | dd bs=1M oflag=direct of=/dev/mmcblk0p2')

      device_imager.RawPartitionUpdater(
          device, 'foo-image', device_imager.ImageType.FULL,
          '/dev/mmcblk0p2', cros_build_lib.COMP_GZIP).Run()
      run_mock.assert_called()
      close_mock.assert_called()
      name_mock.assert_called()

  def test_RunRemoteImage(self):
    """Test main Run() function for remote images."""
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      self.rsh_mock.AddCmdResult([partial_mock.In('which'), 'gzip'],
                                 returncode=0)
      self.rsh_mock.AddCmdResult(
        self.path_env +
        ' gzip --decompress --stdout | dd bs=1M oflag=direct of=/dev/mmcblk0p2')

      path = os.path.join(self.tempdir,
                          constants.QUICK_PROVISION_PAYLOAD_KERNEL)
      with open(path, 'w') as image:
        image.write('helloworld')

      device_imager.KernelUpdater(
          device, self.tempdir, device_imager.ImageType.REMOTE_DIRECTORY,
          '/dev/mmcblk0p2', cros_build_lib.COMP_GZIP).Run()


class KernelUpdaterTest(cros_test_lib.MockTempDirTestCase):
  """Tests KernelUpdater class."""

  def test_GetPartitionName(self):
    """Tests the name of the partitions."""
    ku = device_imager.KernelUpdater(None, None, None, None, None)
    self.assertEqual(constants.PART_KERN_B, ku._GetPartitionName())

  def test_GetRemotePartitionName(self):
    """Tests the name of the partitions."""
    ku = device_imager.KernelUpdater(None, None, None, None, None)
    self.assertEqual(constants.QUICK_PROVISION_PAYLOAD_KERNEL,
                     ku._GetRemotePartitionName())


class RootfsUpdaterTest(cros_test_lib.MockTestCase):
  """Tests RootfsUpdater class."""

  def setUp(self):
    """Sets up the class by creating proper mocks."""
    self.rsh_mock = self.StartPatcher(remote_access_unittest.RemoteShMock())
    self.rsh_mock.AddCmdResult(partial_mock.In('${PATH}'), stdout='')
    self.path_env = 'PATH=%s:' % remote_access.DEV_BIN_PATHS

  def test_GetPartitionName(self):
    """Tests the name of the partitions."""
    ru = device_imager.RootfsUpdater(None, None, None, None, None, None)
    self.assertEqual(constants.PART_ROOT_A, ru._GetPartitionName())

  def test_GetRemotePartitionName(self):
    """Tests the name of the partitions."""
    ru = device_imager.RootfsUpdater(None, None, None, None, None, None)
    self.assertEqual(constants.QUICK_PROVISION_PAYLOAD_ROOTFS,
                     ru._GetRemotePartitionName())

  @mock.patch.object(device_imager.RootfsUpdater, '_RunPostInst')
  @mock.patch.object(device_imager.RootfsUpdater, '_CopyPartitionFromImage')
  def test_Run(self, copy_mock, postinst_mock):
    """Test main Run() function.

    This function should parts of the source image and write it into the device
    using proper compression programs.
    """
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      device_imager.RootfsUpdater(
          '/dev/mmcblk0p5', device, 'foo-image', device_imager.ImageType.FULL,
          '/dev/mmcblk0p3', cros_build_lib.COMP_GZIP).Run()

      copy_mock.assert_called_with(constants.PART_ROOT_A)
      postinst_mock.assert_called_with()

  def test_RunPostInstOnTarget(self):
    """Test _RunPostInst() function."""
    target = '/dev/mmcblk0p3'
    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      device._work_dir = '/tmp/work_dir'
      temp_dir = os.path.join(device.work_dir, 'dir')
      self.rsh_mock.AddCmdResult(
          [self.path_env, 'mktemp', '-d', '-p', device.work_dir],
          stdout=temp_dir)
      self.rsh_mock.AddCmdResult(
          [self.path_env, 'mount', '-o', 'ro', target, temp_dir])
      self.rsh_mock.AddCmdResult(
          [self.path_env, os.path.join(temp_dir, 'postinst'), target])
      self.rsh_mock.AddCmdResult([self.path_env, 'umount', temp_dir])

      device_imager.RootfsUpdater(
          '/dev/mmcblk0p5', device, 'foo-image', device_imager.ImageType.FULL,
          target, cros_build_lib.COMP_GZIP)._RunPostInst()

  def test_RunPostInstOnCurrentRoot(self):
    """Test _RunPostInst() on current root (used for reverting an update)."""
    root_dev = '/dev/mmcblk0p5'
    self.rsh_mock.AddCmdResult([self.path_env, '/postinst', root_dev])

    with remote_access.ChromiumOSDeviceHandler(remote_access.TEST_IP) as device:
      device_imager.RootfsUpdater(
          root_dev, device, 'foo-image', device_imager.ImageType.FULL,
          '/dev/mmcblk0p3', cros_build_lib.COMP_GZIP)._RunPostInst(
              on_target=False)

  @mock.patch.object(device_imager.RootfsUpdater, '_RunPostInst')
  def testRevert(self, postinst_mock):
    """Tests Revert() function."""
    ru = device_imager.RootfsUpdater(None, None, None, None, None, None)

    ru.Revert()
    postinst_mock.assert_not_called()

    ru._ran_postinst = True
    ru.Revert()
    postinst_mock.assert_called_with(on_target=False)
