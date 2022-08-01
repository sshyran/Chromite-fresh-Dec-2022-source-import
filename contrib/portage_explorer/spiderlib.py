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
import enum
from pathlib import Path
from typing import List, Optional


class UseState(enum.Enum):
  """Disabled or enabled state for use flags."""
  DISABLED = False
  ENABLED = True


@dataclasses.dataclass
class ProfileUse:
  """USE flags used for profiles."""
  name: str
  enabled: UseState


@dataclasses.dataclass
class Profile:
  """A profile."""
  id_: str
  path: Path
  name: str
  parent_profiles: List[str] = dataclasses.field(default_factory=list)
  use_flags: List[ProfileUse] = dataclasses.field(default_factory=list)


  def set_enabled(self, flag: str, enabled: bool = True):
    """Set the enabled state for a specified use flag in this profile."""
    for use_flag in self.use_flags:
      if use_flag.name == flag:
        use_flag.enabled = UseState(enabled)


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
