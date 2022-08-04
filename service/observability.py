# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Routines which facilitate data collection for build operations.

Service module to parse or extract data about build behavior for structured
data storage. Complementary to chromite.lib.metrics, chromite.api.metrics, and
related library usage.
"""

import functools
import logging
import os
import re
from typing import Dict, Iterable, NamedTuple, Pattern, Tuple

from chromite.lib import portage_util
from chromite.lib.parser import package_info


class PackageVersion(NamedTuple):
  """Container class akin to chromite.observability.PackageVersion proto."""
  major: int
  minor: int
  patch: int
  extended: int
  revision: int
  full_version: str


class PackageName(NamedTuple):
  """Container class akin to chromite.observability.PackageName proto."""
  atom: str
  category: str
  package_name: str


class PackageIdentifier(NamedTuple):
  """Container class akin to chromite.observability.PackageIdentifier proto."""
  package_name: PackageName
  package_version: PackageVersion


@functools.lru_cache(maxsize=None)
def _get_version_component_regex() -> Pattern:
  # Parse version number, expecting up to 4 integer components arranged
  # like: major[.minor[.patch[.extended]]]
  extended = r'(?:\.(?P<extended>\d+))?'
  patch = rf'(?:\.(?P<patch>\d+){extended})?'
  minor = rf'(?:\.(?P<minor>\d+){patch})?'
  complete = rf'^(?P<major>\d+){minor}'
  return re.compile(complete)


# TODO(zland): refactor scripts/pkg_size (and this function) to use common
# library. This implementation does not want to recreate metrics records for the
# base image's rootfs, and we may not want to append all of the partition &
# image information to metrics, so a simplified approach to
# chromite/scripts/pkg_size is being used here.
def get_package_details_for_partition(
    installation_path: os.PathLike,
    pkgs: Iterable[Tuple[portage_util.InstalledPackage, Iterable[Tuple[str,
                                                                       str]]]]
) -> Dict[PackageIdentifier, int]:
  """Retrieve package size and format name details for a given set of packages.

  Args:
    installation_path: The path to the partition's root that the package's
      installed files are relative to.
    pkgs: The packages of interest in the partition (typically, the entire
      contents of the package db).
  """
  details = {}
  for installed_package, pkg_fileset in pkgs:
    size = portage_util.CalculatePackageSize(pkg_fileset, installation_path)
    pkg_identifier = parse_package_name(installed_package.package_info)
    details[pkg_identifier] = size.apparent_size
  return details


def parse_package_name(pkg_info: package_info.PackageInfo) -> PackageIdentifier:
  """Produce detailed NamedTuple for a package from a PackageInfo object."""
  # Version number parsing, looking for 1-4 numerical components and ignoring
  # any alphanumeric suffixes (e.g. _alpha1).
  matcher = _get_version_component_regex()
  matches = matcher.match(pkg_info.version)
  major = int(matches.group('major') or 0)
  minor = int(matches.group('minor') or 0)
  patch = int(matches.group('patch') or 0)
  extended = int(matches.group('extended') or 0)
  version = PackageVersion(
      major=major,
      minor=minor,
      patch=patch,
      extended=extended,
      revision=pkg_info.revision,
      full_version=pkg_info.vr)
  name = PackageName(
      atom=pkg_info.atom,
      category=pkg_info.category,
      package_name=pkg_info.package)
  return PackageIdentifier(package_name=name, package_version=version)
