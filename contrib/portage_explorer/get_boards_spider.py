# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Spider to find all board names."""

import re
from typing import Pattern

from chromite.contrib.portage_explorer import spiderlib
from chromite.lib import portage_util


def get_board_name(regex: Pattern[str], overlay_path: str) -> str:
  """Parse overlay path with regex to find board name.

  Args:
    regex: Regex to match the board name from the path.
    overlay_path: Path to the overlay.

  Returns:
    The board name as a string.
  """
  board = regex.search(overlay_path)
  if board:
    if board.group('board_from_private'):
      return board.group('board_from_private')
    return board.group('board_from_public')
  return ''


def execute(output: spiderlib.SpiderOutput):
  """Get the board names from all the overlay paths and add to the output.

  Args:
    output: SpiderOutput representing the final output from all the spiders.
  """
  regex = re.compile(r'(?<!-)(?=overlay-.*-private)overlay-'
                     r'(?P<board_from_private>.*)-private|(?<!-)overlay-'
                     r'(?P<board_from_public>.*)')
  overlays = portage_util.FindOverlays('both')
  boards = set()
  for overlay_path in overlays:
    board_name = get_board_name(regex, overlay_path)
    if board_name:
      boards.add(board_name)
  for board in sorted(boards):
    output.build_targets.append(spiderlib.BuildTarget(board))
