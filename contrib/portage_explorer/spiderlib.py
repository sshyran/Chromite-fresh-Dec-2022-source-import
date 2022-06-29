# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Common dataclasses used between spiders."""

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
    build_targets: List of build targets.
  """
  build_targets: List[BuildTarget]
