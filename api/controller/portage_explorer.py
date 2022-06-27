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
