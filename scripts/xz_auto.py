# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run xz from PATH with a thread for each core in the system."""

from __future__ import division

import getopt
import os
import subprocess
import sys

from chromite.lib import commandline
from chromite.lib import osutils
from chromite.utils import memoize


PIXZ_DISABLE_VAR = 'FOR_TEST_XZ_AUTO_NO_PIXZ'


@memoize.Memoize
def HasPixz():
  """Returns path to pixz if it's on PATH or None otherwise."""
  return PIXZ_DISABLE_VAR not in os.environ and osutils.Which('pixz')


def ParsePixzArgs(argv):
  """Determines flags to pass to pixz, per argv.

  Returns:
    A tuple containing:
    - A raw list of flags to pass to pixz.
    - An optional input file.
    - An optional output file (only exists if the input file is present).
  """
  # Glancing at docs, the following opts are supported. -i and -o are ignored,
  # since we assert in `main` that they're not present, but include parsing for
  # them anyway.
  flags, args = getopt.gnu_getopt(
      args=argv,
      shortopts='dlxi:o:0123456789p:tkch',
  )
  if not args:
    file_to_compress = None
    target = None
  elif len(args) == 1:
    file_to_compress = args[0]
    target = None
  else:
    file_to_compress = args[0]
    target = args[1]

  raw_flag_list = []
  for key, val in flags:
    raw_flag_list.append(key)
    if val:
      raw_flag_list.append(val)

  return raw_flag_list, file_to_compress, target


def Execvp(argv):
  """Execs the given argv."""
  os.execvp(argv[0], argv)


def ExecCompressCommand(stdout, argv):
  """Execs compression command."""
  # It appears that in order for pixz to do parallel decompression, compression
  # needs to be done with pixz. xz itself is only capable of parallel
  # compression.
  if not HasPixz():
    cmd = ['xz']

    if stdout:
      cmd.append('-zc')
    else:
      cmd.append('-z')
    cmd += argv
    Execvp(cmd)

  cmd = ['pixz']
  raw_flag_list, compressed_file_name, output_file = ParsePixzArgs(argv)

  autodelete_input_file = False
  if not compressed_file_name:
    assert not output_file
    compressed_file_name = '/dev/stdin'
    output_file = '/dev/stdout'
  elif stdout:
    output_file = '/dev/stdout'
  elif not output_file:
    # Pixz defaults to a `.pxz` suffix (or `.tpxz` if it's compressing a
    # tar file). We need the suffix to be consistent, so force it here.
    output_file = f'{compressed_file_name}.xz'
    autodelete_input_file = True

  cmd += raw_flag_list
  cmd.append(compressed_file_name)
  if output_file:
    cmd.append(output_file)

  if not autodelete_input_file:
    Execvp(cmd)

  return_code = subprocess.call(cmd)
  if not return_code:
    os.unlink(compressed_file_name)
  sys.exit(return_code)


def ExecDecompressCommand(stdout, argv):
  """Execs decompression command."""
  if HasPixz():
    cmd = ['pixz']
    cmd.append('-d')

    _, compressed_file_name, _ = ParsePixzArgs(argv)
    if stdout:
      # Explicitly tell pixz the file is the input, so it will dump the output
      # to stdout, instead of automatically choosing an output name.
      cmd.append('-i')
      if not compressed_file_name:
        cmd.append('/dev/stdin')
    elif not compressed_file_name:
      cmd += ['-i', '/dev/stdin']
    cmd += argv
    Execvp(cmd)

  cmd = ['xz']
  if stdout:
    cmd.append('-dc')
  else:
    cmd.append('-d')
  cmd += argv
  Execvp(cmd)


def GetParser():
  """Return a command line parser."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument(
      '-d',
      '--decompress',
      '--uncompress',
      help='Decompress rather than compress.',
      action='store_true')
  parser.add_argument(
      '-c',
      dest='stdout',
      action='store_true',
      help="Write to standard output and don't delete input files.")
  return parser


def main(argv):
  parser = GetParser()
  known_args, argv = parser.parse_known_args()
  if '-i' in argv or '-o' in argv:
    parser.error('It is invalid to use -i or -o with xz_auto')

  if known_args.decompress:
    ExecDecompressCommand(known_args.stdout, argv)
  else:
    ExecCompressCommand(known_args.stdout, argv)
