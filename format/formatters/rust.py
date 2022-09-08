# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting Rust code."""

from chromite.lib import cros_build_lib


def Data(data: str) -> str:
    """Clean up Rust format problems in |data|.

    Args:
      data: The file content to lint.

    Returns:
      Formatted data.
    """
    result = cros_build_lib.run(
        ["rustfmt", "--edition", "2018"],
        capture_output=True,
        input=data,
        encoding="utf-8",
    )
    return result.stdout
