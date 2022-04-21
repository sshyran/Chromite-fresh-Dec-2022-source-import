# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for linting OWNERS."""

import logging
import os
from pathlib import Path
from typing import Union

from chromite.lint.linters import whitespace


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
    logging.error('%s: empty owners file not allowed', path)

  for i, line in enumerate(lines):
    if '\t' in line:
      ret = False
      logging.error('%s:%i: no tabs allowed: "%s"', path, i, line)

    lstrip = line.lstrip()
    if lstrip != line:
      ret = False
      logging.error('%s:%i: no leading whitespace allowed: "%s"', path, i, line)

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
    return lint_data(path, path.read_text(encoding='utf-8'))
  else:
    return True
