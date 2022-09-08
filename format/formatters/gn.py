# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting GN files."""

import functools
import os

from chromite.lib import constants
from chromite.lib import cros_build_lib


@functools.lru_cache(maxsize=None)
def _find_gn() -> str:
    """Find the `gn` tool."""
    if cros_build_lib.IsInsideChroot():
        return "gn"
    else:
        return os.path.join(constants.DEFAULT_CHROOT_PATH, "usr", "bin", "gn")


def Data(data: str) -> str:
    """Format GN |data|.

    Args:
      data: The file content to lint.

    Returns:
      Formatted data.
    """
    result = cros_build_lib.run(
        [_find_gn(), "format", "--stdin"],
        capture_output=True,
        input=data,
        encoding="utf-8",
    )
    return result.stdout
