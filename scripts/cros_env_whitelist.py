# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Print the environment whitelist."""

import sys

from chromite.lib import constants


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


def main(_argv):
  print(' '.join(constants.CHROOT_ENVIRONMENT_WHITELIST))
