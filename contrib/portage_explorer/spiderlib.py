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
from pathlib import Path
from typing import List, Optional


@dataclasses.dataclass
class Profile:
  """A profile."""
  id_: str
  path: Path
  name: str
  parent_profiles: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class BuildTarget:
  """A build target."""
  name: str
  profile: Optional[Profile] = None


@dataclasses.dataclass
class Overlay:
  """An overlay."""
  path: Path
  name: str
  profiles: List[Profile] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SpiderOutput:
  """Output from all the spiders.

  The output from all the spiders will be used to fill in the output proto of
  the RunSpiders endpoint for the PortageExplorerService.

  Attributes:
    build_targets: List of build targets. Default value is an empty list.
    overlays: List of overlays. Default value is an empty list.
  """
  build_targets: List[BuildTarget] = dataclasses.field(default_factory=list)
  overlays: List[Overlay] = dataclasses.field(default_factory=list)
