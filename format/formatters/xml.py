# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides utility for formatting XML files.

Not all XML files are formatted the same unfortunately.
"""

from xml.etree import ElementTree

from chromite.format.formatters import repo_manifest
from chromite.format.formatters import whitespace


def Data(data: str) -> str:
  """Format XML |data|.

  Args:
    data: The file content to lint.

  Returns:
    Formatted data.
  """
  root = ElementTree.fromstring(data)
  if root.tag == 'manifest':
    data = repo_manifest.Data(data)
  else:
    data = whitespace.Data(data)
  return data
