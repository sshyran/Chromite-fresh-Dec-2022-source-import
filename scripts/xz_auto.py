# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run xz from PATH with a thread for each core in the system."""

from __future__ import division

import getopt
import os

from chromite.lib import commandline
from chromite.lib import osutils
from chromite.utils import memoize


PIXZ_DISABLE_VAR = 'FOR_TEST_XZ_AUTO_NO_PIXZ'


@memoize.Memoize
def HasPixz():
  """Returns path to pixz if it's on PATH or None otherwise."""
  return osutils.Which('pixz') and not os.environ.get(PIXZ_DISABLE_VAR)


def BasePixzCommand(jobs):
  """Returns a command that invokes pixz with the given job count."""
  return ['pixz', '-p', str(jobs)]


def BaseXzCommand(jobs):
  """Returns a command that invokes xz with the given job count."""
  return ['xz', f'-T{jobs}']


def DetermineFilesPassedToPixz(argv):
  """Attempt to figure out what file we're trying to compress."""
  # Glancing at docs, the following opts are supported. -i and -o are ignored,
  # since we assert in `main` that they're not present, but include parsing for
  # them anyway.
  _, args = getopt.gnu_getopt(
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

  return file_to_compress, target


def GetCompressCommand(stdout, jobs, argv):
  """Returns compression command."""
  # It appears that in order for pixz to do parallel decompression, compression
  # needs to be done with pixz. xz itself is only capable of parallel
  # compression.
  if HasPixz():
    cmd = BasePixzCommand(jobs)

    compressed_file_name, specifies_output_file = DetermineFilesPassedToPixz(
        argv)

    if compressed_file_name:
      if not (stdout or specifies_output_file):
        # Pixz defaults to a `.pxz` suffix (or `.tpxz` if it's compressing a
        # tar file). We need the suffix to be consistent, so force it here.
        cmd += ['-o', f'{compressed_file_name}.xz']
    else:
      cmd += ['-i', '/dev/stdin']
    return cmd

  cmd = BaseXzCommand(jobs)

  if stdout:
    cmd.append('-zc')
  else:
    cmd.append('-z')
  return cmd


def GetDecompressCommand(stdout, jobs, argv):
  """Returns decompression command."""
  if HasPixz():
    cmd = BasePixzCommand(jobs)
    cmd.append('-d')

    compressed_file_name, _ = DetermineFilesPassedToPixz(argv)
    if stdout:
      # Explicitly tell pixz the file is the input, so it will dump the output
      # to stdout, instead of automatically choosing an output name.
      cmd.append('-i')
      if not compressed_file_name:
        cmd.append('/dev/stdin')
    elif not compressed_file_name:
      cmd += ['-i', '/dev/stdin']
    return cmd

  cmd = BaseXzCommand(jobs)
  if stdout:
    cmd.append('-dc')
  else:
    cmd.append('-d')
  return cmd


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

  # Use half of our CPUs to avoid starving other processes.
  jobs = max(1, os.cpu_count() // 2)

  if known_args.decompress:
    args = GetDecompressCommand(known_args.stdout, jobs, argv)
  else:
    args = GetCompressCommand(known_args.stdout, jobs, argv)

  os.execvp(args[0], args + argv)
