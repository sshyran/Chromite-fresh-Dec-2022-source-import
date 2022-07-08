# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Common dataclasses used between spiders.

  The dataclasses should be similar to those from portage_explorer.proto. Use
  the actual objects to represent the relationships (except for profile
  inheritance where ids should be used) instead of ids for ease of access and
  organization.
"""

import dataclasses
from typing import List


@dataclasses.dataclass
class BuildTarget:
  """A build target."""
  name: str


@dataclasses.dataclass
class SpiderOutput:
  """Output from all the spiders which is used for the output proto.

  Attributes:
    build_targets: List of build targets. Default value is an empty list.
  """
  build_targets: List[BuildTarget] = dataclasses.field(default_factory=list)
