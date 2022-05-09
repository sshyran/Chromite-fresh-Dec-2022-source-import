# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""build_image is used to build a Chromium OS image.

Chromium OS comes in many different forms. This script can be used to build
the following:

base - Pristine Chromium OS image. As similar to Chrome OS as possible.
dev [default] - Developer image. Like base but with additional dev packages.
test - Like dev, but with additional test specific packages and can be easily
  used for automated testing using scripts like test_that, etc.
factory_install - Install shim for bootstrapping the factory test process.
  Cannot be built along with any other image.

Examples:

build_image --board=<board> dev test - builds developer and test images.
build_image --board=<board> factory_install - builds a factory install shim.

Note if you want to build an image with custom size partitions, either consider
adding a new disk layout in build_library/legacy_disk_layout.json OR use
adjust_part. See build_image help, but here are a few examples:

adjust_part='STATE:+1G' -- add one GB to the size the stateful partition
adjust_part='ROOT-A:-1G' -- remove one GB from the primary rootfs partition
adjust_part='STATE:=1G' --  make the stateful partition 1 GB
"""

from pathlib import Path
from typing import List, Optional

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib


def main(argv: Optional[List[str]] = None) -> Optional[int]:
  commandline.RunInsideChroot()

  cmd = [
      'bash',
      Path(constants.CROSUTILS_DIR) / 'build_image.sh',
      '--script-is-run-only-by-chromite-and-not-users',
  ]
  cmd.extend(argv)
  try:
    cros_build_lib.sudo_run(cmd, print_cmd=False)
  except cros_build_lib.RunCommandError as e:
    cros_build_lib.Die(e)
