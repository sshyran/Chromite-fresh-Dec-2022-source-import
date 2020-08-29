# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run xz from PATH with a thread for each core in the system."""

from __future__ import division
from __future__ import print_function

import multiprocessing
import os
import sys

from chromite.lib import commandline
from chromite.lib import osutils
from chromite.utils import memoize


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


@memoize.Memoize
def HasPixz():
  """Returns path to pixz if it's on PATH or None otherwise."""
  return osutils.Which('pixz')


@memoize.Memoize
def GetJobCount():
  """Returns half of the total number of the machine's CPUs as a string.

  Returns half rather than all of them to avoid starving out other parallel
  processes on the same machine.
  """
  return str(int(max(1, multiprocessing.cpu_count() / 2)))


def GetDecompressCommand():
  """Returns decompression command."""
  if HasPixz():
    return ['pixz', '-d', '-p', GetJobCount()]
  return ['xz', '-d']


def GetParser():
  """Return a command line parser."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument(
      '-d', '--decompress', '--uncompress',
      help='Decompress rather than compress.',
      action='store_true')
  return parser


def main(argv):
  parser = GetParser()
  known_args, argv = parser.parse_known_args()
  # xz doesn't support multi-threaded decompression, so try using pixz for that.
  if known_args.decompress:
    args = GetDecompressCommand()
    os.execvp(args[0], args + argv)
  os.execvp('xz', ['xz', '-T0'] + argv)
