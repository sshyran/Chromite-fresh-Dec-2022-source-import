# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Command to visualize dependency tree for a given package."""

import sys
from typing import List, Dict

from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import depgraph

from . import visualize


def ParseArgs(argv):
  """Parse command line arguments."""
  parser = commandline.ArgumentParser(description=__doc__)
  target = parser.add_mutually_exclusive_group(required=True)
  target.add_argument('--sysroot', type='path', help='Path to the sysroot.')
  target.add_argument('-b', '--build-target', help='Name of the target build')
  parser.add_argument('pkgs', nargs='*')
  opts = parser.parse_args(argv)
  opts.Freeze()
  return opts


def CreateRuntimeTree(sysroot: str, pkg_list: str) -> Dict[str, List[str]]:
  """Calculate all packages that are RDEPENDS.

  Use the dependency information about packages to build a tree
  of only RDEPEDS packages and dependencies.

  Args:
    sysroot: The path to the root directory into which the package is
      pretend to be merged. This value is also used for setting
      PORTAGE_CONFIGROOT.
    pkg_list: The list of packages to extract their dependencies from.

  Returns:
    Returns a dictionary of runtime packages with their immediate dependencies.
  """

  # Setup for dependency extraction.
  lib_argv = ['--quiet', '--pretend', '--emptytree']
  lib_argv += ['--sysroot=%s' % sysroot]
  lib_argv.extend(pkg_list)
  dep_graph = depgraph.DepGraphGenerator()
  dep_graph.Initialize(lib_argv)
  deps_tree, _deps_info, _bdeps_tree = dep_graph.GenDependencyTree()

  runtime_tree = {pkg: deps_tree[pkg]['deps'].keys() for pkg in deps_tree}

  return runtime_tree


def main():
  opts = ParseArgs(sys.argv[1:])
  sysroot = opts.sysroot or cros_build_lib.GetSysroot(opts.build_target)
  runtime_tree = CreateRuntimeTree(sysroot, opts.pkgs)
  dep_vis = visualize.DepVisualizer(runtime_tree)
  dep_vis.VisualizeGraph()
