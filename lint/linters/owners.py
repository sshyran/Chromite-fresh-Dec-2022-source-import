# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for linting OWNERS."""

import logging
import os
from pathlib import Path
import re
from typing import Union

from chromite.lint.linters import whitespace


# Cross-repository includes take the form:
# include [server/path[:branch]:]/path/to/file
INCLUDE_RE = re.compile(
    r"^include +((?P<repo>[^:]*):((?P<branch>[^:]*):)?)?(?P<path>[^\s]*)"
)

# Current version of our owners repo.
SHARED_OWNERS_BRANCH = "v1"


def lint_data(path: Union[str, os.PathLike], data: str) -> bool:
    """Run basic checks on |data|.

    Args:
      path: The name of the file (for diagnostics).
      data: The file content to lint.

    Returns:
      True if everything passed.
    """
    ret = whitespace.LintData(path, data)

    lines = data.splitlines()

    if not lines:
        ret = False
        logging.error("%s: empty owners file not allowed", path)

    for i, line in enumerate(lines):
        if "\t" in line:
            ret = False
            logging.error('%s:%i: no tabs allowed: "%s"', path, i, line)

        lstrip = line.lstrip()
        if lstrip != line:
            ret = False
            logging.error(
                '%s:%i: no leading whitespace allowed: "%s"', path, i, line
            )

        m = INCLUDE_RE.match(lstrip)
        if m:
            if m.group("repo") in ("chromiumos/owners", "chromeos/owners"):
                if m.group("branch") != SHARED_OWNERS_BRANCH:
                    ret = False
                    logging.error(
                        '%s:%i: shared owners must use branch "%s", not "%s"',
                        path,
                        i,
                        SHARED_OWNERS_BRANCH,
                        m.group("branch"),
                    )

                p = m.group("path")
                if not p.startswith("/"):
                    ret = False
                    logging.error(
                        '%s:%i: shared owners files use absolute paths: "%s"',
                        path,
                        i,
                        line,
                    )

                if p.split("/")[-1] == "OWNERS":
                    ret = False
                    logging.error(
                        "%s:%i: shared owners files may not include plain "
                        '"OWNERS": "%s"',
                        path,
                        i,
                        line,
                    )

    return ret


def lint_path(path: Union[str, os.PathLike]) -> bool:
    """Run basic checks on |path|.

    Args:
      path: The name of the file.

    Returns:
      True if everything passed.
    """
    path = Path(path)
    if path.exists():
        return lint_data(path, path.read_text(encoding="utf-8"))
    else:
        return True
