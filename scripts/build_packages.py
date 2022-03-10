# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""build_packages updates the set of binary packages needed by Chrome OS.

The build_packages process cross compiles all packages that have been
updated into the given sysroot and builds binary packages as a side-effect.
The output packages will be used by the build_image script to create a
bootable Chrome OS image.
"""

import logging
import os
import urllib.error
import urllib.request

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib


def main(argv):
  commandline.RunInsideChroot()

  cmd = [
      'bash',
      os.path.join(constants.CROSUTILS_DIR, 'build_packages.sh'),
      '--script-is-run-only-by-chromite-and-not-users'
  ]
  cmd.extend(argv)
  try:
    # TODO(b/187793559): Don't pass in print_cmd once we switch to argparse
    cros_build_lib.dbg_run(cmd, print_cmd=False)
  except cros_build_lib.RunCommandError as e:
    try:
      request = urllib.request.urlopen(
          'https://chromiumos-status.appspot.com/current?format=raw')
      logging.notice('Tree Status: %s', request.read().decode())
    except urllib.error.HTTPError:
      pass
    cros_build_lib.Die(e)
