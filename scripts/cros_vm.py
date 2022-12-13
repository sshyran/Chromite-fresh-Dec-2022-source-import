# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""CLI entry point into lib/vm.py; used for VM management."""

import logging

from chromite.lib import vm


def main(argv):
  opts = vm.VM.GetParser().parse_args(argv)
  opts.Freeze()

  try:
    vm.VM(opts).Run()
    return 0
  except vm.VMError as e:
    logging.error('%s', e)
    if opts.debug:
      raise

    logging.error('(Re-run with --debug for more details.)')
    return 1
