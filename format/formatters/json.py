# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting JSON."""

import json

from chromite.utils import pformat


def Data(data: str) -> str:
    """Clean up basic whitespace problems in |data|.

    Args:
      data: The file content to lint.

    Returns:
      Formatted data.
    """
    # If the file is one line, assume it should be condensed.  If it isn't, assume
    # it should be human readable.
    obj = json.loads(data)
    return pformat.json(obj, fp=None, compact="\n" not in data.strip())
