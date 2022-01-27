# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""build_packages updates the set of binary packages needed by Chrome OS.

The build_packages process cross compiles all packages that have been
updated into the given sysroot and builds binary packages as a side-effect.
The output packages will be used by the build_image script to create a
bootable Chrome OS image.
"""

import os

from chromite.lib import constants
from chromite.lib import cros_build_lib


def main(argv):
  cmd = [
      'bash',
      os.path.join(constants.CROSUTILS_DIR, 'build_packages.sh'),
      '--script-is-run-only-by-chromite-and-not-users'
  ]
  cmd.extend(argv)
  try:
    cros_build_lib.run(cmd)
  except cros_build_lib.RunCommandError as e:
    cros_build_lib.Die(e)
