# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Routines which facilitate data collection for build operations.

Service module to parse or extract data about build behavior for structured
data storage. Complementary to chromite.lib.metrics, chromite.api.metrics, and
related library usage.
"""

import re
from typing import NamedTuple, Pattern

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


def _get_version_component_regex() -> Pattern:
  # Parse version number, expecting up to 4 integer components arranged
  # like: major[.minor[.patch[.extended]]]
  extended = r'(?:\.(?P<extended>\d+))?'
  patch = rf'(?:\.(?P<patch>\d+){extended})?'
  minor = rf'(?:\.(?P<minor>\d+){patch})?'
  complete = rf'^(?P<major>\d+){minor}'
  return re.compile(complete)


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
