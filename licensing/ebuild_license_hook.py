# Copyright 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Emerge hook to pre-parse and verify license information.

Called from src/scripts/hooks/install/gen-package-licenses.sh as part of a
package emerge.
"""

import os

from chromite.lib import commandline
from chromite.licensing import licenses_lib


def main(args):
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('--builddir', type='path', dest='builddir',
                      help='Take $PORTAGE_BUILDDIR as argument.')
  parser.add_argument('--sysroot', type='path',
                      help='Take $SYSROOT as argument.')

  opts = parser.parse_args(args)
  opts.Freeze()

  sysroot = opts.sysroot
  if not sysroot:
    sysroot = os.environ.get('SYSROOT') or '/'

  licenses_lib.HookPackageProcess(opts.builddir, sysroot)
