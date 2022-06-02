# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for service/observability.py methods."""

# pylint: disable=unused-import
import pytest

from chromite.lib.parser import package_info
from chromite.service import observability


def test_parse_package_name__full_with_mmpe():
  """Test version parsing for 4-part version number with no suffix."""
  lacros_pkg_info = package_info.parse(
      'chromeos-base/chromeos-lacros-104.0.5083.0-r1')
  lacros_identifier = observability.parse_package_name(lacros_pkg_info)

  assert lacros_identifier.package_version.major == 104
  assert lacros_identifier.package_version.minor == 0
  assert lacros_identifier.package_version.patch == 5083
  assert lacros_identifier.package_version.extended == 0
  assert lacros_identifier.package_version.revision == 1
  assert lacros_identifier.package_version.full_version == lacros_pkg_info.vr
  assert lacros_identifier.package_name.atom == lacros_pkg_info.atom
  assert lacros_identifier.package_name.category == lacros_pkg_info.category
  assert lacros_identifier.package_name.package_name == lacros_pkg_info.package
  assert lacros_identifier.package_version.full_version == '104.0.5083.0-r1'

  assert lacros_identifier.package_name.atom == 'chromeos-base/chromeos-lacros'
  assert lacros_identifier.package_name.category == 'chromeos-base'
  assert lacros_identifier.package_name.package_name == 'chromeos-lacros'


def test_parse_package_name__full_with_mmp():
  """Test version parsing for standard 3-part version number with no suffix."""
  py_pkg_info = package_info.parse('dev-lang/python-3.6.15-r2')
  py_identifier = observability.parse_package_name(py_pkg_info)

  assert py_identifier.package_version.major == 3
  assert py_identifier.package_version.minor == 6
  assert py_identifier.package_version.patch == 15
  assert py_identifier.package_version.extended == 0
  assert py_identifier.package_version.revision == 2
  assert py_identifier.package_version.full_version == '3.6.15-r2'

  assert py_identifier.package_name.atom == 'dev-lang/python'
  assert py_identifier.package_name.category == 'dev-lang'
  assert py_identifier.package_name.package_name == 'python'


def test_parse_package_name__full_with_suffix():
  """Test version parsing for 2-part version number with suffix included."""
  fake_pkg_info = package_info.parse('cat/test-pkg-1.1b_alpha3')
  fake_identifier = observability.parse_package_name(fake_pkg_info)

  assert fake_identifier.package_version.major == 1
  assert fake_identifier.package_version.minor == 1
  assert fake_identifier.package_version.patch == 0
  assert fake_identifier.package_version.extended == 0
  assert fake_identifier.package_version.revision == 0
  assert fake_identifier.package_version.full_version == '1.1b_alpha3'

  assert fake_identifier.package_name.atom == 'cat/test-pkg'
  assert fake_identifier.package_name.category == 'cat'
  assert fake_identifier.package_name.package_name == 'test-pkg'
