# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This script emerges packages and retrieves their lints.

Currently support is provided for both general and differential linting of C++
with Clang Tidy and Rust with Cargo Clippy for all packages within platform2.
"""

import json
import sys
from typing import List

from chromite.lib import build_target_lib
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib.parser import package_info
from chromite.service import toolchain
from chromite.utils import file_util


def get_arg_parser() -> commandline.ArgumentParser:
  """Creates an argument parser for this script."""
  default_board = cros_build_lib.GetDefaultBoard()
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument(
      '--differential',
      action='store_true',
      help='only lint lines touched by the last commit')
  parser.add_argument(
      '-b',
      '--board',
      '--build-target',
      dest='board',
      default=default_board,
      required=not default_board,
      help='The board to emerge packages for')
  parser.add_argument(
      '-o',
      '--output',
      default=sys.stdout,
      help='File to use instead of stdout.')
  parser.add_argument(
      '--no-clippy',
      dest='clippy',
      action='store_false',
      help='Disable cargo clippy linter.')
  parser.add_argument(
      '--no-tidy',
      dest='tidy',
      action='store_false',
      help='Disable clang tidy linter.')
  parser.add_argument(
      'packages', nargs='+', help='package(s) to emerge and retrieve lints for')
  return parser


def parse_args(argv: List[str]):
  """Parses arguments in argv and returns the options."""
  parser = get_arg_parser()
  opts = parser.parse_args(argv)
  opts.Freeze()
  return opts


def main(argv: List[str]) -> None:
  cros_build_lib.AssertInsideChroot()
  opts = parse_args(argv)

  packages = [package_info.parse(x) for x in opts.packages]
  sysroot = build_target_lib.get_default_sysroot_path(opts.board)

  build_linter = toolchain.BuildLinter(packages, sysroot, opts.differential)
  lints = build_linter.emerge_with_linting(
      use_clippy=opts.clippy, use_tidy=opts.tidy)

  with file_util.Open(opts.output, 'w') as output_file:
    json.dump(lints, output_file)
