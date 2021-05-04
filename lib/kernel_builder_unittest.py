# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test the kernel_builder module."""

import os

from chromite.lib import constants
from chromite.lib import cros_test_lib
from chromite.lib import kernel_builder


class BuilderTest(cros_test_lib.RunCommandTestCase):
  """Test Builder."""

  def setUp(self):
    """Sets up common objects for testing."""
    self._kb = kernel_builder.Builder('foo-board', 'foo-tmp', 'foo-root')

  def testCreateCustomKernel(self):
    """Tests CreateCustomKernel()."""
    self.PatchObject(os.environ, 'get', return_value='z')
    self.rc.AddCmdResult(['portageq-foo-board', 'expand_virtual',
                          '/build/foo-board', 'virtual/linux-sources'],
                         stdout='kernel')

    self._kb.CreateCustomKernel(['x', 'y'])

    emerge_board = 'emerge-foo-board'
    extra_env = {
      'PKGDIR': os.path.join('foo-tmp', 'packages'),
      'USE': 'z x y'
    }
    self.assertCommandCalled(
      [emerge_board, 'chromeos-base/chromeos-initramfs'],
      enter_chroot=True, extra_env=extra_env)
    self.assertCommandCalled(
      [emerge_board, '--onlydeps', 'kernel'],
      enter_chroot=True, extra_env=extra_env)
    self.assertCommandCalled(
      [emerge_board, '--buildpkgonly', 'kernel'],
      enter_chroot=True, extra_env=extra_env)
    self.assertCommandCalled(
      [emerge_board, '--usepkgonly', '--root=foo-root', 'kernel'],
      enter_chroot=True, extra_env=extra_env)

  def testCreateKernelImageDefaultArgs(self):
    """Tests CreateKernelImage() with default arguments."""
    self.rc.AddCmdResult(['portageq-foo-board', 'envvar', 'ARCH'],
                         stdout='foo-arch')

    self._kb.CreateKernelImage('output')

    self.assertCommandCalled([
        os.path.join(constants.CROSUTILS_DIR, 'build_kernel_image.sh'),
        '--board=foo-board',
        '--arch=foo-arch',
        '--to=output',
        '--vmlinuz=foo-root/boot/vmlinuz',
        '--working_dir=foo-tmp',
        '--keep_work',
        f'--keys_dir={kernel_builder.VBOOT_DEVKEYS_DIR}',
        '--public=recovery_key.vbpubk',
        '--private=recovery_kernel_data_key.vbprivk',
        '--keyblock=recovery_kernel.keyblock',
    ], enter_chroot=True)

  def testCreateKernelImageWithArgs(self):
    """Tests CreateKernelImage() with default arguments."""
    self.rc.AddCmdResult(['portageq-foo-board', 'envvar', 'ARCH'],
                         stdout='foo-arch')

    self._kb.CreateKernelImage('output', keys_dir='foo-keys-dir',
                               boot_args='x y=foo',
                               serial='ttyfoo',
                               disable_rootfs_verification=True)

    self.assertCommandCalled([
        os.path.join(constants.CROSUTILS_DIR, 'build_kernel_image.sh'),
        '--board=foo-board',
        '--arch=foo-arch',
        '--to=output',
        '--vmlinuz=foo-root/boot/vmlinuz',
        '--working_dir=foo-tmp',
        '--keep_work',
        '--keys_dir=foo-keys-dir',
        '--public=recovery_key.vbpubk',
        '--private=recovery_kernel_data_key.vbprivk',
        '--keyblock=recovery_kernel.keyblock',
        '--noenable_rootfs_verification',
        '--boot_args="x y=foo"',
        '--enable_serial=ttyfoo',
    ], enter_chroot=True)
