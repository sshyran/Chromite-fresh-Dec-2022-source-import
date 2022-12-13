# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module tests the cros flash command."""

from chromite.cli import command_unittest
from chromite.cli import flash
from chromite.cli.cros import cros_flash
from chromite.lib import commandline
from chromite.lib import cros_test_lib
from chromite.lib import remote_access


pytestmark = cros_test_lib.pytestmark_inside_only


class MockFlashCommand(command_unittest.MockCommand):
  """Mock out the flash command."""
  TARGET = 'chromite.cli.cros.cros_flash.FlashCommand'
  TARGET_CLASS = cros_flash.FlashCommand
  COMMAND = 'flash'


class CrosFlashTest(cros_test_lib.MockTempDirTestCase,
                    cros_test_lib.OutputTestCase):
  """Test calling `cros flash` with various arguments.

  These tests just check that arguments as specified on the command
  line are properly passed through to flash.Flash(). Testing the
  actual update flow is done in the flash.Flash() unit tests.
  """

  IMAGE = '/path/to/image'
  DEVICE = remote_access.TEST_IP

  def SetupCommandMock(self, cmd_args):
    """Setup comand mock."""
    self.cmd_mock = MockFlashCommand(
        cmd_args, base_args=['--cache-dir', str(self.tempdir)])
    self.StartPatcher(self.cmd_mock)

  def setUp(self):
    """Patches objects."""
    self.cmd_mock = None
    self.flash_mock = self.PatchObject(flash, 'Flash', autospec=True)

  def VerifyFlashParameters(self, device, image, **kwargs):
    """Verifies the arguments passed to flash.Flash().

    This function helps verify that command line specifications are
    parsed properly and handed to flash.Flash() as expected.

    Args:
      device: expected device hostname; currently only SSH devices
          are supported.
      image: expected image parameter.
      kwargs: keyword arguments expected in the call to flash.Flash().
          Arguments unspecified here are checked against their default
          value for `cros flash`.
    """
    flash_args, flash_kwargs = self.flash_mock.call_args
    self.assertEqual(device, flash_args[0].hostname)
    self.assertEqual(image, flash_args[1])
    # `cros flash` default options. Must match the configuration in AddParser().
    expected_kwargs = {
        'board': None,
        'version': 'latest',
        'no_minios_update': True,
        'no_rootfs_update': False,
        'no_stateful_update': False,
        'clobber_stateful': False,
        'clear_tpm_owner': False,
        'reboot': True,
        'ssh_private_key': None,
        'ping': True,
        'disable_rootfs_verification': False,
        'clear_cache': False,
        'yes': False,
        'force': False,
        'debug': False,
        'delta': False,
    }
    # Overwrite defaults with any variations in this test.
    expected_kwargs.update(kwargs)
    self.assertDictEqual(expected_kwargs, flash_kwargs)

  def testDefaults(self):
    """Tests `cros flash` default values."""
    self.SetupCommandMock([self.DEVICE, self.IMAGE])
    self.cmd_mock.inst.Run()
    self.VerifyFlashParameters(self.DEVICE, self.IMAGE)

  def testDoesNotEnterChroot(self):
    """Test that cros flash doesn't enter the chroot."""
    self.SetupCommandMock([self.DEVICE, self.IMAGE])
    enter_chroot = self.PatchObject(commandline, 'RunInsideChroot')
    self.cmd_mock.inst.Run()
    self.assertFalse(enter_chroot.called)

  def testFlashError(self):
    """Tests that FlashErrors are passed through."""
    with self.OutputCapturer():
      self.SetupCommandMock([self.DEVICE, self.IMAGE])
      self.flash_mock.side_effect = flash.FlashError
      with self.assertRaises(flash.FlashError):
        self.cmd_mock.inst.Run()
