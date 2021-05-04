# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A script to generate MiniOS kernel images.

And inserting them into the Chromium OS images.
"""

import tempfile

from chromite.lib import commandline
from chromite.lib import minios


def GetParser():
  """Creates an argument parser and returns it."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('--board', '-b', '--build-target', required=True,
                      help='The board name.')
  parser.add_argument('--image', type='path',
                      help='The path to the chromium os image.')
  return parser


def main(argv):
  parser = GetParser()
  opts = parser.parse_args(argv)
  opts.Freeze()

  with tempfile.TemporaryDirectory() as work_dir:
    kernel = minios.CreateMiniOsKernelImage(opts.board, work_dir)
    minios.InsertMiniOsKernelImage(opts.image, kernel)
