# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Call all the spiders in the correct order for them to fill out the output."""

from chromite.contrib.portage_explorer import get_boards_spider
from chromite.contrib.portage_explorer import get_overlays_spider
from chromite.contrib.portage_explorer import get_profiles_spider
from chromite.contrib.portage_explorer import spiderlib


def execute():
  """Calls the spiders which will fill out the output.

  Returns:
    SpiderOutput containing all the data collected from all the spiders.
  """
  output = spiderlib.SpiderOutput()
  get_boards_spider.execute(output)
  get_overlays_spider.execute(output)
  get_profiles_spider.execute(output)
  return output
