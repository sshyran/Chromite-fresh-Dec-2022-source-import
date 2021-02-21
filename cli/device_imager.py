# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Library containing functions to install an image on a Chromium OS device."""

import enum
import os
import re
import sys
from typing import Tuple, Dict

from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import gs
from chromite.lib import parallel
from chromite.lib import remote_access
from chromite.lib import retry_util
from chromite.lib.xbuddy import devserver_constants
from chromite.lib.xbuddy import xbuddy


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


class Error(Exception):
  """Thrown when there is a general Chromium OS-specific flash error."""


class ImageType(enum.Enum):
  """Type of the image that is used for flashing the device."""

  # The full image on disk (e.g. chromiumos_test_image.bin).
  FULL = 0
  # The remote directory path
  # (e.g gs://chromeos-image-archive/eve-release/R90-x.x.x)
  REMOTE_DIRECTORY = 1


class Partition(enum.Enum):
  """An enum for partition types like kernel and rootfs."""
  KERNEL = 0
  ROOTFS = 1


class DeviceImager(object):
  """A class to flash a Chromium OS device.

  This utility uses parallelism as much as possible to achieve its goal as fast
  as possible. For example, it uses parallel compressors, parallel transfers,
  and simultaneous pipes.
  """

  # The parameters of the kernel and rootfs's two main partitions.
  A = {Partition.KERNEL: 2, Partition.ROOTFS: 3}
  B = {Partition.KERNEL: 4, Partition.ROOTFS: 5}

  def __init__(self, device, image: str,
               no_rootfs_update: bool = False,
               no_stateful_update: bool = False,
               no_reboot: bool = False,
               disable_verification: bool = False,
               clobber_stateful: bool = False,
               clear_tpm_owner: bool = False):
    """Initialize DeviceImager for flashing a Chromium OS device.

    Args:
      device: The ChromiumOSDevice to be updated.
      image: The target image path (can be xBuddy path).
      no_rootfs_update: Whether to do rootfs partition update.
      no_stateful_update: Whether to do stateful partition update.
      no_reboot: Whether to reboot device after update. The default is True.
      disable_verification: Whether to disabling rootfs verification on the
          device.
      clobber_stateful: Whether to do a clean stateful partition.
      clear_tpm_owner: If true, it will clear the TPM owner on reboot.
    """

    self._device = device
    self._image = image
    self._no_rootfs_update = no_rootfs_update
    self._no_stateful_update = no_stateful_update
    self._no_reboot = no_reboot
    self._disable_verification = disable_verification
    self._clobber_stateful = clobber_stateful
    self._clear_tpm_owner = clear_tpm_owner

    self._compression = cros_build_lib.COMP_XZ
    self._inactive_state = None

  def Run(self):
    """Update the device with image of specific version."""

    try:
      self._Run()
    except Exception as e:
      raise Error(f'DeviceImager Failed with error: {e}')

    logging.info('DeviceImager completed.')

  def _Run(self):
    """Runs the various operations to install the image on device."""
    image, image_type = self._GetImage()
    logging.info('Using image %s of type %s', image, image_type )

    if image_type == ImageType.REMOTE_DIRECTORY:
      self._compression = cros_build_lib.COMP_GZIP

    self._InstallPartitions(image, image_type)

    if self._clear_tpm_owner:
      self._device.ClearTpmOwner()

    if not self._no_reboot:
      self._Reboot()
      self._VerifyBootExpectations()

    if self._disable_verification:
      self._device.DisableRootfsVerification()

  def _GetImage(self) -> Tuple[str, ImageType]:
    """Returns the path to the final image(s) that need to be installed.

    If the paths is local, the image should be the Chromium OS GPT image
    (e.g. chromiumos_test_image.bin). If the path is remote, it should be the
    remote directory where we can find the quick-provision and stateful update
    files (e.g. gs://chromeos-image-archive/eve-release/R90-x.x.x).

    NOTE: At this point there is no caching involved. Hence we always download
    the partition payloads or extract them from the Chromium OS image.

    Returns:
      A tuple of image path and image type.
    """
    if os.path.isfile(self._image):
      return self._image, ImageType.FULL

    # TODO(b/172212406): We could potentially also allow this by searching
    # through the directory to see whether we have quick-provision and stateful
    # payloads. This only makes sense when a user has their workstation at home
    # and doesn't want to incur the bandwidth cost of downloading the same
    # image multiple times. For that, they can simply download the GPT image
    # image first and flash that instead.
    if os.path.isdir(self._image):
      raise ValueError(
          f'{self._image}: input must be a disk image, not a directory.')

    if gs.PathIsGs(self._image):
      # TODO(b/172212406): Check whether it is a directory. If it wasn't a
      # directory download the image into some temp location and use it instead.
      return self._image, ImageType.REMOTE_DIRECTORY

    # Assuming it is an xBuddy path.
    xb = xbuddy.XBuddy(log_screen=False)
    build_id, local_file = xb.Translate([self._image])
    if build_id is None:
      raise Error(f'{self._image}: unable to find matching xBuddy path.')
    logging.info('XBuddy path translated to build ID %s', build_id)

    if local_file:
      return local_file, ImageType.FULL

    return (f'{devserver_constants.GS_IMAGE_DIR}/{build_id}',
            ImageType.REMOTE_DIRECTORY)

  def _SplitDevPath(self, path: str) -> Tuple[str, int]:
    """Splits the given /dev/x path into prefix and the dev number.

    Args:
      path: The path to a block dev device.

    Returns:
      A tuple of representing the prefix and the index of the dev path.
      e.g.: '/dev/mmcblk0p1' -> ['/dev/mmcblk0p', 1]
    """
    match = re.search(r'(.*)([0-9]+)$', path)
    if match is None:
      raise Error(f'{path}: Could not parse root dev path.')

    return match.group(1), int(match.group(2))

  def _GetKernelState(self, root_num: int) -> Tuple[Dict, Dict]:
    """Returns the kernel state.

    Returns:
      A tuple of two dictionaries: The current active kernel state and the
      inactive kernel state. (Look at A and B constants in this class.)
    """
    if root_num == self.A[Partition.ROOTFS]:
      return self.A, self.B
    elif root_num == self.B[Partition.ROOTFS]:
      return self.B, self.A
    else:
      raise Error(f'Invalid root partition number {root_num}')

  def _InstallPartitions(self, image: str, image_type):
    """The main method that installs the partitions of a Chrome OS device.

    It uses parallelism to install the partitions as fast as possible.

    Args:
      image: The image path (local file or remote directory).
      image_type: The type of the image (ImageType).
    """
    updaters = []

    # Retry the partitions updates that failed, in case a transient error (like
    # SSH drop, etc) caused the error.
    num_retries = 1
    try:
      retry_util.RetryException(Error, num_retries,
                                parallel.RunParallelSteps,
                                (x.Run for x in updaters if not x.IsFinished()),
                                halt_on_error=True)
    except Exception:
      # If one of the partitions failed to be installed, revert all partitions.
      parallel.RunParallelSteps(x.Revert for x in updaters)
      raise

  def _Reboot(self):
    """Reboots the device."""
    try:
      self._device.Reboot(timeout_sec=60)
    except remote_access.RebootError:
      raise Error('Could not recover from reboot. Once example reason'
                  ' could be the image provided was a non-test image'
                  ' or the system failed to boot after the update.')
    except Exception as e:
      raise Error(f'Failed to reboot to the device with error: {e}')

  def _VerifyBootExpectations(self):
    """Verify that we fully booted into the expected kernel state."""
    # Discover the newly active kernel.
    _, root_num = self._SplitDevPath(self._device.root_dev)
    active_state, _ = self._GetKernelState(root_num)

    # If this happens, we should rollback.
    if active_state != self._inactive_state:
      raise Error('The expected kernel state after update is invalid.')

    logging.info('Verified boot expectations.')
