# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Deps analysis service."""

import functools
import os
from pathlib import Path
from typing import List, Optional

from chromite.lib import build_target_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import dependency_lib
from chromite.lib import git
from chromite.lib import portage_util
from chromite.scripts import cros_extract_deps

if cros_build_lib.IsInsideChroot():
  from chromite.lib import depgraph


class Error(Exception):
  """Base error class for the module."""


def NormalizeSourcePaths(source_paths):
  """Return the "normalized" form of a list of source paths.

  Normalizing includes:
    * Sorting the source paths in alphabetical order.
    * Remove paths that are sub-path of others in the source paths.
    * Ensure all the directory path strings are ended with the trailing '/'.
    * Convert all the path from absolute paths to relative path (relative to
      the chroot source root).
  """
  return dependency_lib.normalize_source_paths(source_paths)


def GenerateSourcePathMapping(packages, sysroot_path, board):
  """Returns a map from each package to the source paths it depends on.

  A source path is considered dependency of a package if modifying files in that
  path might change the content of the resulting package.

  Notes:
    1) This method errs on the side of returning unneeded dependent paths.
       i.e: for a given package X, some of its dependency source paths may
       contain files which doesn't affect the content of X.

       On the other hands, any missing dependency source paths for package X is
       considered a bug.
    2) This only outputs the direct dependency source paths for a given package
       and does not takes include the dependency source paths of dependency
       packages.
       e.g: if package A depends on B (DEPEND=B), then results of computing
       dependency source paths of A doesn't include dependency source paths
       of B.

  Args:
    packages: The list of packages CPV names (str)
    sysroot_path (str): The path to the sysroot.  If the packages are board
      agnostic, then this should be '/'.
    board (str): The name of the board if packages are dependency of board. If
      the packages are board agnostic, then this should be None.

  Returns:
    Map from each package to the source path (relative to the repo checkout
      root, i.e: ~/trunk/ in your cros_sdk) it depends on.
    For each source path which is a directory, the string is ended with a
      trailing '/'.
  """
  return dependency_lib.get_source_path_mapping(packages, sysroot_path, board)


@functools.lru_cache()
def GetBuildDependency(sysroot_path, board=None, packages=None):
  """Return the build dependency and package -> source path map for |board|.

  Args:
    sysroot_path (str): The path to the sysroot, or None if no sysroot is being
        used.
    board (str): The name of the board whose artifacts are being created, or
        None if no sysroot is being used.
    packages (tuple[CPV]): The packages that need to be built, or empty / None
        to use the default list.

  Returns:
    JSON build dependencies report for the given board which includes:
      - Package level deps graph from portage
      - Map from each package to the source path
      (relative to the repo checkout root, i.e: ~/trunk/ in your cros_sdk) it
      depends on
  """
  if not sysroot_path:
    sysroot_path = build_target_lib.get_default_sysroot_path(board)

  results = {
      'sysroot_path': sysroot_path,
      'target_board': board,
      'package_deps': {},
      'source_path_mapping': {},
  }

  sdk_sysroot = build_target_lib.get_default_sysroot_path(None)
  sdk_results = {
      'sysroot_path': sdk_sysroot,
      'target_board': 'sdk',
      'package_deps': {},
      'source_path_mapping': {},
  }

  if sysroot_path != sdk_sysroot:
    board_packages = []
    if packages:
      board_packages.extend([cpv.cp for cpv in packages])
    else:
      board_packages.extend([
          constants.TARGET_OS_PKG,
          constants.TARGET_OS_DEV_PKG,
          constants.TARGET_OS_TEST_PKG,
          constants.TARGET_OS_FACTORY_PKG,
          constants.TARGET_OS_FACTORY_SHIM_PKG,
      ])
      # Since we don’t have a clear mapping from autotests to git repos
      # and/or portage packages, we assume every board run all autotests.
      board_packages += ['chromeos-base/autotest-all']

    board_deps, board_bdeps = cros_extract_deps.ExtractDeps(
        sysroot=sysroot_path,
        package_list=board_packages,
        include_bdepend=False,
        backtrack=False)

    results['package_deps'].update(board_deps)
    results['package_deps'].update(board_bdeps)
    sdk_results['package_deps'].update(board_bdeps)

  indep_packages = [
      'virtual/target-sdk', 'virtual/target-sdk-post-cross',
  ]

  indep_deps, _ = cros_extract_deps.ExtractDeps(
      sysroot=sdk_results['sysroot_path'], package_list=indep_packages)

  indep_map = GenerateSourcePathMapping(list(indep_deps), sdk_sysroot, None)
  results['package_deps'].update(indep_deps)
  results['source_path_mapping'].update(indep_map)

  sdk_results['package_deps'].update(indep_deps)
  sdk_results['source_path_mapping'].update(indep_map)

  if sysroot_path != sdk_sysroot:
    bdep_map = GenerateSourcePathMapping(list(board_bdeps), sdk_sysroot, None)
    board_map = GenerateSourcePathMapping(list(board_deps), sysroot_path, board)
    results['source_path_mapping'].update(bdep_map)
    results['source_path_mapping'].update(board_map)
    sdk_results['source_path_mapping'].update(bdep_map)

  return results, sdk_results


def determine_package_relevance(dep_src_paths: List[str],
                                src_paths: Optional[List[str]] = None) -> bool:
  """Determine if the package is relevant to the given source paths.

  A package is relevant if any of its dependent source paths is in the given
  list of source paths. If no source paths are given, the default is True.

  Args:
    dep_src_paths: List of source paths the package depends on.
    src_paths: List of source paths of interest.
  """
  if not src_paths:
    return True
  for src_path in (Path(x) for x in src_paths):
    for dep_src_path in (Path(x) for x in dep_src_paths):
      try:
        # Will throw an error if src_path isn't under dep_src_path.
        src_path.relative_to(dep_src_path)
        return True
      except ValueError:
        pass
  return False


def GetDependencies(sysroot_path: str,
                    src_paths: Optional[List[str]] = None,
                    packages: Optional[List[str]] = None,
                    include_rev_dependencies: bool = False) -> List[str]:
  """Return the packages dependent on the given source paths for |board|.

  Args:
    sysroot_path: The path to the sysroot.
    src_paths: List of paths for which to get a list of dependent packages. If
      empty / None returns all package dependencies.
    packages: The packages that need to be built, or empty / None to use the
      default list.
    include_rev_dependencies: Whether to include the reverse dependencies of
      relevant packages.

  Returns:
    The relevant package dependencies based on the given list of packages and
      src_paths.
  """
  cros_build_lib.AssertInsideChroot()
  pkgs = tuple(packages) if packages else None
  dep_graph = depgraph.get_sysroot_dependency_graph(
      sysroot_path, pkgs, with_src_paths=True)

  if not src_paths:
    return [x.pkg_info for x in dep_graph.get_nodes()]

  dep_nodes = dep_graph.get_relevant_nodes(src_paths=src_paths)
  rev_dep_nodes = []
  if include_rev_dependencies:
    for dep in dep_nodes:
      rev_dep_nodes.extend(dep.reverse_dependencies)
  return list({dep.pkg_info for dep in dep_nodes + rev_dep_nodes})


def DetermineToolchainSourcePaths():
  """Returns a list of all source paths relevant to toolchain packages.

  A package is a 'toolchain package' if it is listed as a direct dependency
  of virtual/toolchain-packages. This function deliberately does not return
  deeper transitive dependencies so that only direct changes to toolchain
  packages trigger the expensive full re-compilation required to test toolchain
  changes. Eclasses & overlays are not returned as relevant paths for the same
  reason.

  Returned paths are relative to the root of the project checkout.

  Returns:
    List[str]: A list of paths considered relevant to toolchain packages.
  """
  source_paths = set()
  toolchain_pkgs = portage_util.GetFlattenedDepsForPackage(
      'virtual/toolchain-packages', depth=1)
  toolchain_pkg_ebuilds = portage_util.FindEbuildsForPackages(
      toolchain_pkgs, sysroot='/', check=True)

  # Include the entire directory containing the toolchain ebuild, as the
  # package's FILESDIR and patches also live there.
  source_paths.update(
      os.path.dirname(ebuild_path)
      for ebuild_path in toolchain_pkg_ebuilds.values())

  # Source paths which are cros workon source paths.
  buildroot = os.path.join(constants.CHROOT_SOURCE_ROOT, 'src')
  manifest = git.ManifestCheckout.Cached(buildroot)
  for ebuild_path in toolchain_pkg_ebuilds.values():
    attrs = portage_util.EBuild.Classify(ebuild_path)
    if (not attrs.is_workon or
        # Manually uprevved ebuild is pinned to a specific git sha1, so change
        # in that repo does not matter to the ebuild.
        attrs.is_manually_uprevved):
      continue
    ebuild = portage_util.EBuild(ebuild_path)
    workon_subtrees = ebuild.GetSourceInfo(buildroot, manifest).subtrees
    for path in workon_subtrees:
      source_paths.add(path)

  return NormalizeSourcePaths(list(source_paths))
