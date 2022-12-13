# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Portage Explorer Spider Controller.

Handles the endpoint for running all the spiders and generating the protobuf.
"""

from chromite.api import faux
from chromite.api import validate
from chromite.contrib import portage_explorer


def _RunSpiders(_input_proto, output_proto, _config_proto):
  """Mock success output for the RunSpiders endpoint."""
  mock_build_target = output_proto.build_targets.add()
  mock_build_target.name = 'board'

@faux.success(_RunSpiders)
@faux.empty_error
@validate.validation_complete
def RunSpiders(_input_proto, output_proto, _config_proto):
  """Run all the spiders from portage_explorer and enter data into proto."""
  spider_output = portage_explorer.execute()
  for build_target in spider_output.build_targets:
    proto_build_target = output_proto.build_targets.add()
    proto_build_target.name = build_target.name
    proto_build_target.profile_id.id = build_target.profile.id_
  for overlay in spider_output.overlays:
    proto_overlay = output_proto.overlays.add()
    proto_overlay.path = str(overlay.path)
    proto_overlay.name = overlay.name
    for profile in overlay.profiles:
      proto_profile = proto_overlay.profiles.add()
      proto_profile.id = profile.id_
      proto_profile.path = str(profile.path)
      proto_profile.name = profile.name
