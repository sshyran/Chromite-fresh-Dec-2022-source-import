# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test the star module."""

import pytest

from chromite.format.formatters import star
from chromite.lib import cros_test_lib


# None means input is already formatted to avoid having to repeat.
@pytest.mark.parametrize(
    "fmt",
    (star.Data, star.BuildData, star.WorkspaceData, star.BzlData),
)
@pytest.mark.parametrize(
    "data,exp",
    (
        ("", None),
        ('workspace(name = "foo")\n', None),
        ('workspace(name="foo")\n', 'workspace(name = "foo")\n'),
    ),
)
@cros_test_lib.pytestmark_network_test  # requires CIPD
def test_check_format(fmt, data, exp):
    """Verify inputs match expected outputs."""
    if exp is None:
        exp = data
    assert exp == fmt(data)
