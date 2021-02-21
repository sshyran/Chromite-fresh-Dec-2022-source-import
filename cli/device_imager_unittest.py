# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the device_imager module."""

import sys
import tempfile

import mock

from chromite.cli import device_imager
from chromite.lib import cros_test_lib
from chromite.lib import partial_mock
from chromite.lib import remote_access
from chromite.lib import remote_access_unittest
from chromite.lib.xbuddy import xbuddy


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


# pylint: disable=protected-access

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
