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
from chromite.lib import portage_util
from chromite.lib import workon_helper
from chromite.lib.parser import package_info
from chromite.service import toolchain
from chromite.utils import file_util


def parse_packages(build_target: build_target_lib.BuildTarget,
                   packages: List[str]) -> List[package_info.PackageInfo]:
  """Parse packages and insert the category if none is given.

  Args:
    build_target: build_target to find ebuild for
    packages: user input package names to parse

  Returns:
    A list of parsed PackageInfo objects
  """
  package_infos: List[package_info.PackageInfo] = []
  for package in packages:
    parsed = package_info.parse(package)
    if not parsed.category:
      # If a category is not specified, we can get it from the ebuild path.
      ebuild_path = portage_util.FindEbuildForBoardPackage(
          package, build_target.name, build_target.root)
      ebuild_data = portage_util.EBuild(ebuild_path)
      parsed = package_info.parse(ebuild_data.package)
    package_infos.append(parsed)
  return package_infos


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

  build_target = build_target_lib.BuildTarget(opts.board)
  packages = parse_packages(build_target, opts.packages)
  package_atoms = [x.atom for x in packages]

  with workon_helper.WorkonScope(build_target, package_atoms):
    build_linter = toolchain.BuildLinter(packages, build_target.root,
                                         opts.differential)
    lints = build_linter.emerge_with_linting(
        use_clippy=opts.clippy, use_tidy=opts.tidy)

  with file_util.Open(opts.output, 'w') as output_file:
    json.dump(lints, output_file)
