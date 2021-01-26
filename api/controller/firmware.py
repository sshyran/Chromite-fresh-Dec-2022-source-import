# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Firmware builder controller.

Handle all firmware builder related functionality.
"""

import os
import tempfile

from google.protobuf import json_format

from chromite.api import controller
from chromite.api import faux
from chromite.api import validate
from chromite.api.gen.chromite.api import firmware_pb2
from chromite.lib import constants
from chromite.lib import cros_build_lib

def _call_entry(fw_loc, metric_proto, subcmd):
  """Calls into firmware_builder.py with the specified subcmd."""

  if fw_loc == firmware_pb2.PLATFORM_EC:
    fw_path = 'src/platform/ec/'
  elif fw_loc == firmware_pb2.PLATFORM_ZEPHYR:
    fw_path = 'src/platform/zephyr-chrome/'
  elif fw_loc == firmware_pb2.PLATFORM_TI50:
    fw_path = 'src/platform/ti50/common/'
  else:
    cros_build_lib.Die(f'Unknown firmware location {fw_loc}!')

  entry_point = os.path.join(constants.SOURCE_ROOT,
                             fw_path, 'firmware_builder.py')

  with tempfile.NamedTemporaryFile() as file:
    result = cros_build_lib.run([entry_point, '--metrics', file.name, subcmd],
                                check=False)
    with open(file.name, 'r') as f:
      response = f.read()

  # Parse the entire metric file as our metric proto (as a passthru)
  json_format.Parse(response, metric_proto)

  if result.returncode == 0:
    return controller.RETURN_CODE_SUCCESS
  else:
    return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY


def _BuildAllTotFirmwareResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful repose."""

  metric = output_proto.success.value.add()
  metric.target_name = 'foo'
  metric.platform_name = 'bar'
  fw_section = metric.fw_section.add()
  fw_section.region = firmware_pb2.FwBuildMetric.FwSection.EC_RO
  fw_section.used = 100
  fw_section.total = 150

@faux.success(_BuildAllTotFirmwareResponse)
@faux.empty_completed_unsuccessfully_error
@validate.require('firmware_location')
@validate.validation_complete
def BuildAllTotFirmware(input_proto, output_proto, _config):
  """Build all of the firmware targets at the specified location."""

  return _call_entry(input_proto.firmware_location, output_proto.metrics,
                     'build')


def _TestAllTotFirmwareResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful repose."""

  metric = output_proto.success.value.add()
  metric.name = 'foo-test'

@faux.success(_TestAllTotFirmwareResponse)
@faux.empty_completed_unsuccessfully_error
@validate.require('firmware_location')
@validate.validation_complete
def TestAllTotFirmware(input_proto, output_proto, _config):
  """Runs all of the firmware tests at the specified location."""

  return _call_entry(input_proto.firmware_location, output_proto.metrics,
                     'test')
