# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Strip packages and place them in <sysroot>/stripped-packages."""

import os
import sys
from typing import List

from chromite.lib import build_target_lib
from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import osutils

# The builder module lives in the devserver path.
sys.path.append('/usr/lib/devserver/')
import builder

_DEFAULT_MASK = 'DEFAULT_INSTALL_MASK'

def create_parser() -> commandline.ArgumentParser:
  """Creates the cmdline argparser, populates the options and description."""
  parser = commandline.ArgumentParser(description=__doc__)

  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--board',
                     default=cros_build_lib.GetDefaultBoard(),
                     help='The board that processed packages belong to.')
  group.add_argument('--sysroot',
                     type='path',
                     help='Sysroot that processed packages belong to. '
                     'This is incompatible with --board.')

  parser.add_argument('--deep',
                      action='store_true',
                      default=False,
                      help='Also strip dependencies of packages.')
  parser.add_argument('packages',
                      nargs='+',
                      metavar='package',
                      help='Packages to strip.')
  return parser


def populate_install_mask() -> bool:
  """Extract the default install mask and populate the local environment."""
  env_var_value = osutils.SourceEnvironment(
      os.path.join(constants.CROSUTILS_DIR, 'common.sh'),
      [_DEFAULT_MASK],
      multiline=True)

  if _DEFAULT_MASK not in env_var_value:
    return False
  os.environ[_DEFAULT_MASK] = env_var_value[_DEFAULT_MASK]
  return True


def main(argv: List[str]) -> int:
  """Main function."""
  cros_build_lib.AssertInsideChroot()
  parser = create_parser()
  options = parser.parse_args(argv)
  options.Freeze()

  if options.sysroot is not None:
    sysroot = options.sysroot
  else:
    sysroot = build_target_lib.get_default_sysroot_path(options.board)

  if not populate_install_mask():
    return False
  if not builder.UpdateGmergeBinhost(sysroot, options.packages, options.deep):
    return 1
  return 0
