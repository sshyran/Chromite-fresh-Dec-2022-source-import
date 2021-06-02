# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""MiniOS build library."""

import os
import pathlib

from chromite.lib import build_target_lib
from chromite.lib import cros_logging as logging
from chromite.lib import cros_build_lib
from chromite.lib import kernel_builder
from chromite.lib import image_lib


MINIOS_KERNEL_IMAGE = 'minios_vmlinuz.image'
KERNEL_FLAGS = ['minios', 'minios_ramfs', 'tpm', 'i2cdev', 'vfat',
                'kernel_compress_xz', 'pcserial', '-kernel_afdo']
PART_NAME = 'MINIOS-A'
BLOCK_SIZE = 512


class Error(Exception):
  """Base error class for the module."""


class MiniOsError(Error):
  """Raised when failing to build Mini OS image."""


def CreateMiniOsKernelImage(board: str, work_dir: str) -> str:
  """Creates the MiniOS kernel image.

  And puts it in the work directory.

  Args:
    board: The board to build the kernel for.
    work_dir: The directory for keeping intermediary files.

  Returns:
    The path to the generated kernel image.
  """
  install_root = os.path.join(
    (build_target_lib.get_default_sysroot_path(board)), 'factory-root')
  kb = kernel_builder.Builder(board, work_dir, install_root)
  kb.CreateCustomKernel(KERNEL_FLAGS)
  kernel = os.path.join(work_dir, MINIOS_KERNEL_IMAGE)
  kb.CreateKernelImage(kernel, boot_args='noinitrd panic=60',
                       serial='ttyS2')
  return kernel


def InsertMiniOsKernelImage(image: str, kernel: str):
  """Writes the MiniOS into MINIOS-A partition of the Chromium OS image.

  It assumes the Chromium OS image has enough space in MINIOS-A partition,
  otherwise it will fail.

  Args:
    image: The path to the Chromium OS image.
    kernel: The path to the kernel image.
  """
  with image_lib.LoopbackPartitions(image) as devs:
    part_info = devs.GetPartitionInfo(PART_NAME)
    if pathlib.Path(kernel).stat().st_size > part_info.size:
      raise MiniOsError(
          'MiniOS kernel image is larger than the MINIOS-A partition.')

    device = devs.GetPartitionDevName(PART_NAME)
    logging.debug('Mini OS loopback partition is %s', device)

    logging.info('Writing the MiniOS kernel image %s into the Chromium OS '
                 'image %s', kernel, image)
    # First zero out the partition. This generally would help with update
    # payloads so we don't have to compress junk bytes. The target file is a
    # loopback dev device of the MINIOS-A partition.
    cros_build_lib.sudo_run(['dd', 'if=/dev/zero', f'of={device}',
                             f'bs={BLOCK_SIZE}',
                             f'count={part_info.size // BLOCK_SIZE}'])
    # Write the actual MiniOS kernel into the MINIOS-A partition.
    cros_build_lib.sudo_run(['dd', f'if={kernel}', f'of={device}',
                             f'bs={BLOCK_SIZE}'])