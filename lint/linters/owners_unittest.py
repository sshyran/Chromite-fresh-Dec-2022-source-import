# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test the owners module."""

import pytest

from chromite.lint.linters import owners


def test_missing_file():
  """Given a missing file should be OK."""
  assert owners.lint_path('/.....ajlsdkfjalskdfjalskdfasdf')


GOOD_DATA = (
    'v@e.x\n',
    # Shared owners includes.
    f'include chromiumos/owners:{owners.SHARED_OWNERS_BRANCH}:/OWNERS.foo\n'
    f'include chromeos/owners:{owners.SHARED_OWNERS_BRANCH}:/OWNERS.foo\n'
)

@pytest.mark.parametrize('data', GOOD_DATA)
def test_good_owners(data):
  """Test good owners files."""
  assert owners.lint_data('pylint', data)


BAD_DATA = (
    '',
    # Leading blank line.
    '\nv@e.x\n',
    # Trailing blank line.
    '\nv@e.x\n\n',
    # Missing final blank line.
    '\nv@e.x',
    # Tabs!
    '\tv@e.x\n',
    # Leading whitespace.
    '  v@e.x\n',
    # Shared owners missing branch.
    'include chromiumos/owners:/OWNERS.foo\n'
    'include chromeos/owners:/OWNERS.foo\n'
    # Shared owners bad branch.
    'include chromiumos/owners:foo:/OWNERS.foo\n'
    'include chromeos/owners:foo:/OWNERS.foo\n'
    # Shared owners bad includes.
    f'include chromiumos/owners:{owners.SHARED_OWNERS_BRANCH}:OWNERS.foo\n'
    f'include chromeos/owners:{owners.SHARED_OWNERS_BRANCH}:OWNERS.foo\n'
    f'include chromiumos/owners:{owners.SHARED_OWNERS_BRANCH}:/OWNERS\n'
    f'include chromeos/owners:{owners.SHARED_OWNERS_BRANCH}:/OWNERS\n'
    f'include chromiumos/owners:{owners.SHARED_OWNERS_BRANCH}:/foo/OWNERS\n'
    f'include chromeos/owners:{owners.SHARED_OWNERS_BRANCH}:/foo/OWNERS\n'
)

@pytest.mark.parametrize('data', BAD_DATA)
def test_bad_owners(data):
  """Test good owners files."""
  assert not owners.lint_data('pylint', data)
