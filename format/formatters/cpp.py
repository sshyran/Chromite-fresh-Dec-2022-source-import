# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting C & C++ files.

This currently only supports clang-format.
"""

from chromite.lib import cros_build_lib


def Data(data: str) -> str:
    """Format C & C++ |data|.

    Args:
      data: The file content to lint.

    Returns:
      Formatted data.
    """
    result = cros_build_lib.run(
        ["clang-format", "--style=file"],
        capture_output=True,
        input=data,
        encoding="utf-8",
    )
    return result.stdout
