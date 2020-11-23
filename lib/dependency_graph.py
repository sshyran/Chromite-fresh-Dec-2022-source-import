# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""DependencyGraph class.

At time of writing, the DependencyGraph is only used by the depgraph lib to
produce graphs from portage, but this class is decoupled from that file to
allow it to be used elsewhere. For example, the package index file in binhosts
contain enough information to generate a graph, and does not require portage
imports to parse.
"""

import collections
import enum
import sys
from typing import Iterable, Iterator, List, Set, Union

from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib.parser import package_info

assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


class Error(Exception):
  """Base module error."""


class NodeCollisionError(Error):
  """Found multiple nodes representing the same package."""


class SysrootValueError(Error, ValueError):
  """Sysroot argument value not valid."""


class PackageNode:
  """A package vertex in the depgraph.

  Attributes:
    pkg_info: The package the node represents.
    root: The root where the package is to be installed.
    _deps: The set of packages this package depends on.
    _rev_deps: The set of packages that depend on this package.
  """
  pkg_info: package_info.PackageInfo
  root: str

  def __init__(self, pkg_info: package_info.PackageInfo, root: str):
    self.pkg_info = pkg_info
    self.root = root
    self._deps = set()
    self._rev_deps = set()

  def __eq__(self, other: Union['PackageNode', package_info.PackageInfo]):
    if isinstance(other, PackageNode):
      return (self.pkg_info == other.pkg_info and
              self.root == other.root and
              self._deps == set(other.dependencies) and
              self._rev_deps == set(other.reverse_dependencies))
    elif isinstance(other, package_info.PackageInfo):
      return self.pkg_info == other
    else:
      return False

  def __hash__(self):
    return hash((self.name, self.root))

  def __str__(self):
    return f'PackageNode<{self.pkg_info} in {self.root}>'

  def __repr__(self):
    # Build truncated strings for deps and rdeps.
    truncated_len = 3
    deplen = min(len(self._deps), truncated_len)
    deps = ', '.join(str(p) for p in list(self._deps)[:deplen])
    if len(self._deps) > deplen:
      deps += ', ...'
    rdeplen = min(len(self._rev_deps), truncated_len)
    rdeps = ', '.join(str(p) for p in list(self._rev_deps)[:rdeplen])
    if len(self._rev_deps) > rdeplen:
      rdeps += ', ...'
    return (f'PackageNode<pkg_info: "{self.pkg_info}", root: "{self.root}", '
            f'deps: "{deps}", reverse deps: "{rdeps}">')

  @property
  def dependencies(self) -> Iterable['PackageNode']:
    """Get the packages this one depends on."""
    yield from self._deps

  @property
  def reverse_dependencies(self) -> Iterable['PackageNode']:
    """Get the packages that depend on this one."""
    yield from self._rev_deps

  @property
  def atom(self):
    """Get the package atom ("category/package")."""
    return self.pkg_info.atom

  @property
  def name(self):
    """Get the node name, a unique identifier for the package itself."""
    return self.pkg_info.cpvr

  def add_dependency(self, dependency: 'PackageNode'):
    """Add a package as a dependency of this node.

    Also registers this package as a reverse dependency of the other.
    """
    self._deps.add(dependency)
    dependency.add_reverse_dependency(self)

  def add_reverse_dependency(self, dependency: 'PackageNode'):
    """Add a reverse dependency.

    This method is not generally meant to be used directly. Use add_dependency
    to build out a DependencyGraph.
    """
    self._rev_deps.add(dependency)


@enum.unique
class RootType(enum.Enum):
  """Root type enum for DependencyGraph."""
  SYSROOT = enum.auto()
  SDK = enum.auto()
  ALL = enum.auto()


class DependencyGraph:
  """Dependency graph data structure.

  Data structure to enable more easily querying and traversing the depgraphs.
  Querying the depgraph currently supports the full CPVR package spec, and
  package atoms. The behavior of other package specs (e.g. CPV) is undefined.
  """

  def __init__(self, nodes: Iterable[PackageNode],
               sysroot: Union[str, 'sysroot_lib.Sysroot'],
               root_packages: List[Union[str, package_info.PackageInfo]]):
    """DependencyGraph init.

    The |nodes| are expected to already have their dependencies added.

    Args:
      nodes: The PackageNodes for the depgraph.
      sysroot: The sysroot the dependency graph was built from.
      root_packages: The packages emerged to create this depgraph.
    """
    ### Add all of the nodes to our internal structure.
    # The pkg/atom_dict are nested dictionaries. The first key is the package
    # CPF (category/package-version-revision). The next key is the package's
    # target root. This allows identifying packages that are installed to both
    # the sysroot and the SDK.
    self._pkg_dict = collections.defaultdict(dict)
    # The atom_list is a dictionary containing the list of packages that map
    # to a specific atom. Many packages will have a single entry, but the list
    # may contain multiple when a package is installed to both the sysroot
    # and the SDK root, and/or could contain multiple versions of a package.
    self._atom_list = collections.defaultdict(list)
    self._roots = set()
    self._len = 0

    for node in nodes:
      self._add_node(node)

    ### Verify found roots and store roots information.
    # Each entry should be installed to either the SDK (BDEPEND) or to
    # the sysroot (DEPEND/RDEPEND). Zero roots is possible only when the
    # depgraph is empty.
    assert 0 <= len(self._roots) <= 2, 'Unexpected roots: {self._roots}'

    # Figure out which roots we have roots, and that they're the ones we expect.
    given_sysroot = getattr(sysroot, 'path', sysroot)
    sdk_root = cros_build_lib.GetSysroot()
    is_sdk_graph = given_sysroot == sdk_root
    # Store the SDK (bdeps) root when present and it's not the SDK's depgraph.
    self.sdk_root = (
        sdk_root if sdk_root in self._roots and not is_sdk_graph else None)
    self.sysroot_path = given_sysroot if given_sysroot in self._roots else None

    if not self.sysroot_path:
      # Given sysroot could not be confirmed. It could mean we were given a bad
      # value, or just that nothing needed to be installed to the sysroot.

      # found_sysroot should always be either empty, or a set with exactly one
      # element in it.
      found_sysroot = self._roots - {self.sdk_root}
      if found_sysroot:
        raise SysrootValueError(
            f'Found sysroot {found_sysroot} does not match given sysroot '
            f'({given_sysroot}).')
      else:
        # Since it's valid no packages could be installed to it, just notify
        # the user.
        logging.info('Given %s but depgraph did not contain any packages '
                     'installed to it.', given_sysroot)

    ### Save the references to the root package nodes.
    # This must be done after the root information processing for the root
    # filtering functionality in _get_nodes().
    self._root_package_nodes = []
    for pkg in [package_info.parse(p) for p in root_packages]:
      self._root_package_nodes.extend(self.get_nodes(pkg, RootType.SYSROOT))

  def __contains__(
      self, item: Union[str, package_info.PackageInfo, PackageNode]) -> bool:
    """Check if the given package is in the depgraph."""
    if isinstance(item, PackageNode):
      return item.atom in self._atom_list and item in self._atom_list[item.atom]
    elif isinstance(item, package_info.PackageInfo):
      return item.cpvr in self._pkg_dict or item.atom in self._atom_list
    else:
      return item in self._pkg_dict or item in self._atom_list

  def __iter__(self):
    """BFS traversal of the depgraph."""
    pkgs = collections.deque(self._root_package_nodes)
    seen = set()
    while pkgs:
      pkg = pkgs.popleft()
      if pkg in seen:
        continue
      seen.add(pkg)
      pkgs.extend(pkg.dependencies)

      yield pkg

  def __len__(self):
    """Size of the depgraph."""
    return self._len

  def _add_node(self, node: PackageNode):
    """Add a package and its dependencies to the graph."""
    if node.root in self._pkg_dict[node.name]:
      if self._pkg_dict[node.name][node.root] == node:
        # Ignore if re-adding.
        return
      else:
        raise NodeCollisionError(f'Different node already exists for {node}.')

    # Add node.
    self._pkg_dict[node.name][node.root] = node
    self._atom_list[node.atom].append(node)
    self._roots.add(node.root)
    self._len += 1
    for dep in node.dependencies:
      self._add_node(dep)

  def _get_roots(self, root: RootType = RootType.ALL) -> Set[str]:
    """Helper to translate RootType value to a set of roots."""
    if root is RootType.SDK:
      return self._roots & {self.sdk_root}
    elif root is RootType.SYSROOT:
      return self._roots & {self.sysroot_path}
    else:
      return self._roots

  def get_nodes(self, pkg: Union[package_info.PackageInfo, str],
                root_type: RootType = RootType.ALL) -> List[PackageNode]:
    """Get all nodes matching the given package and root type."""
    pkg_info = package_info.parse(pkg)
    roots = self._get_roots(root_type)
    if pkg_info.cpvr in self._pkg_dict:
      # Have exact match.
      nodes = []
      for root in roots:
        if root in self._pkg_dict[pkg_info.cpvr]:
          nodes.append(self._pkg_dict[pkg_info.cpvr][root])
      return nodes
    elif pkg_info.atom in self._atom_list:
      # Given an atom string.
      return [x for x in self._atom_list[pkg_info.atom] if x.root in roots]
    else:
      return []

  def is_dependency(self, dep_pkg: Union[package_info.PackageInfo, str],
                    src_pkg: Union[package_info.PackageInfo, str],
                    dep_root_type: RootType = RootType.ALL,
                    src_root_type: RootType = RootType.ALL,
                    direct: bool = False) -> bool:
    """Check if |dep_pkg| is in the dependency graph of |src_pkg|.

    Args:
      dep_pkg: The potential dependency package.
      src_pkg: The root of the subgraph to search for |dep_pkg|.
      dep_root_type: Filters the root when finding |dep_pkg|.
      src_root_type: Filters the root when finding |src_pkg|.
      direct: Only search direct dependencies when set to True.
    """
    dep_pkg_nodes = self.get_nodes(dep_pkg, dep_root_type)
    src_pkg_nodes = self.get_nodes(src_pkg, src_root_type)

    if not dep_pkg_nodes or not src_pkg_nodes:
      # One or both not in the graph at all.
      return False
    elif direct:
      # Only check the direct dependencies.
      return any(d in s.dependencies
                 for d in dep_pkg_nodes
                 for s in src_pkg_nodes)
    else:
      # Check if it's in the subgraph(s) rooted at src_pkg.
      subgraph = DependencyGraph(src_pkg_nodes, self.sysroot_path, [src_pkg])
      return any(x in subgraph for x in dep_pkg_nodes)

  def get_dependencies(
      self,
      pkg: Union[package_info.PackageInfo, str],
      root_type: RootType = RootType.ALL) -> Iterator[PackageNode]:
    """Get the dependencies for a package.

    Use |root_type| to differentiate between the instances installed to the SDK
    and sysroot. Generates an empty list for packages not in the graph (or when
    filtered to a root the package isn't installed to). Does not ensure a
    unique list when multiple nodes are found.
    """
    for node in self.get_nodes(pkg, root_type):
      yield from node.dependencies

  def get_reverse_dependencies(
      self,
      pkg: Union[package_info.PackageInfo, str],
      root_type: RootType = RootType.ALL) -> Iterator[PackageNode]:
    """Get the reverse dependencies for a package.

    Like get_dependencies(), but get the reverse dependencies for the package.
    See get_dependencies() for more information.
    """
    for node in self.get_nodes(pkg, root_type):
      yield from node.reverse_dependencies
