# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting Starlark files."""

import functools
import os

from chromite.lib import cipd
from chromite.lib import cros_build_lib


@functools.lru_cache(maxsize=None)
def _find_buildifier() -> str:
    """Find or install the `buildifier` tool."""
    path = cipd.InstallPackage(
        cipd.GetCIPDFromCache(),
        "infra/3pp/tools/buildifier/linux-amd64",
        "latest",
    )
    return os.path.join(path, "buildifier")


def Data(data: str, *, type_="default") -> str:
    """Format starlark |data|.

    Args:
      data: The file content to lint.
      type_: The type of the starlark file.

    Returns:
      Formatted data.
    """
    result = cros_build_lib.run(
        [_find_buildifier(), f"--type={type_}"],
        capture_output=True,
        input=data,
        encoding="utf-8",
    )
    return result.stdout


BuildData = functools.partial(Data, type_="build")
BzlData = functools.partial(Data, type_="bzl")
WorkspaceData = functools.partial(Data, type_="workspace")
