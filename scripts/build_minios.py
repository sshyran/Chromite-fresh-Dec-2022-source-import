# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A script to generate MiniOS kernel images.

And inserting them into the Chromium OS images.
"""

import tempfile

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import minios


def GetParser():
  """Creates an argument parser and returns it."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('--board', '-b', '--build-target', required=True,
                      help='The board name.')
  parser.add_argument('--image', type='path',
                      help='The path to the chromium os image.')
  parser.add_argument('--keys-dir', type='path',
                      help='The path to keyset.',
                      default=constants.VBOOT_DEVKEYS_DIR)
  parser.add_argument('--public-key', type='path',
                      help='Filename to the public key whose private part '\
                      'signed the keyblock.',
                      default=constants.RECOVERY_PUBLIC_KEY )
  parser.add_argument('--private-key', type='path',
                      help='Filename to the private key whose public part is '\
                      'baked into the keyblock.',
                      default=constants.RECOVERY_DATA_PRIVATE_KEY )
  parser.add_argument('--keyblock', type='path',
                      help='Filename to the kernel keyblock.',
                      default=constants.RECOVERY_KEYBLOCK)
  return parser


def main(argv):
  parser = GetParser()
  opts = parser.parse_args(argv)
  opts.Freeze()

  with tempfile.TemporaryDirectory() as work_dir:
    kernel = minios.CreateMiniOsKernelImage(opts.board, work_dir,
                                            opts.keys_dir, opts.public_key,
                                            opts.private_key, opts.keyblock)
    minios.InsertMiniOsKernelImage(opts.image, kernel)
