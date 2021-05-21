# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests for dependency_lib."""

import os

from chromite.lib import constants
from chromite.lib import dependency_lib
from chromite.lib import osutils


def test_normalize_source_paths_collapsing_sub_paths():
  """Test normalize produces"""
  actual_paths = dependency_lib.normalize_source_paths(
      [os.path.join(constants.SOURCE_ROOT, 'foo'),
       os.path.join(constants.SOURCE_ROOT, 'ab', 'cd'),
       os.path.join(constants.SOURCE_ROOT, 'foo', 'bar')])
  expected_paths = {'ab/cd', 'foo'}
  assert set(actual_paths) == expected_paths

  actual_paths = dependency_lib.normalize_source_paths([
      os.path.join(constants.SOURCE_ROOT, 'foo', 'bar'),
      os.path.join(constants.SOURCE_ROOT, 'ab', 'cd'),
      os.path.join(constants.SOURCE_ROOT, 'foo', 'bar', '..'),
      os.path.join(constants.SOURCE_ROOT, 'ab', 'cde'),
  ])
  expected_paths = {'ab/cd', 'ab/cde', 'foo'}
  assert set(actual_paths) == expected_paths


def test_normalize_source_paths_formatting_directory_paths():
  with osutils.TempDir() as tempdir:
    foo_dir = os.path.join(tempdir, 'foo')
    bar_baz_dir = os.path.join(tempdir, 'bar', 'baz')
    osutils.SafeMakedirs(os.path.join(tempdir, 'ab'))
    ab_cd_file = os.path.join(tempdir, 'ab', 'cd')

    osutils.SafeMakedirs(foo_dir)
    osutils.SafeMakedirs(bar_baz_dir)
    osutils.WriteFile(ab_cd_file, 'alphabet')

    expected_paths = [ab_cd_file, bar_baz_dir + '/', foo_dir + '/']
    expected_paths = [os.path.relpath(p, constants.SOURCE_ROOT) for
                      p in expected_paths]

    actual_paths = dependency_lib.normalize_source_paths(
        [foo_dir, ab_cd_file, bar_baz_dir])
    assert actual_paths == expected_paths


def test_parse_ebuild_cache_entry_md5_cache(tmp_path):
  """Verify parsing eclasses from md5 cache style files."""
  expected = [
      ('eclass1', 'abc123'),
      ('eclass2', '123abc'),
      ('eclass3', 'def789'),
  ]
  eclass_str = '\t'.join('\t'.join(x) for x in expected)
  contents = f"""
KEYWORDS=*
LICENSE=license
PROPERTIES=live
RDEPEND=>=foo/bar-0.0.1:= foo/baz:=
SLOT=0/0
_eclasses_={eclass_str}
_md5=123456
"""

  cache_file = os.path.join(tmp_path, 'cache_file')
  osutils.WriteFile(cache_file, contents)

  # pylint: disable=protected-access
  result = dependency_lib._parse_ebuild_cache_entry(cache_file)

  assert set(expected) == set(result)


def test_parse_ebuild_cache_entry_edb_cache(tmp_path):
  """Verify parsing eclasses from edb cache style files."""
  expected = [
      ('eclass1', 'abc123'),
      ('eclass2', '123abc'),
      ('eclass3', 'def789'),
  ]
  eclass_str = '\t'.join('\t'.join((c, '/some/path', d)) for (c, d) in expected)
  contents = f"""
KEYWORDS=*
LICENSE=license
PROPERTIES=live
RDEPEND=>=foo/bar-0.0.1:= foo/baz:=
SLOT=0/0
_eclasses_={eclass_str}
_md5=123456
"""

  cache_file = os.path.join(tmp_path, 'cache_file')
  osutils.WriteFile(cache_file, contents)

  # pylint: disable=protected-access
  result = dependency_lib._parse_ebuild_cache_entry(cache_file)

  assert set(expected) == set(result)
