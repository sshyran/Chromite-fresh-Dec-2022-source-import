# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Firmware builder controller.

Handle all firmware builder related functionality.  Currently no service module
exists: all of the work is done here.
"""

import os
import tempfile

from google.protobuf import json_format

from chromite.api import controller
from chromite.api import faux
from chromite.api import validate
from chromite.api.gen.chromite.api import firmware_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import constants
from chromite.lib import cros_build_lib

def _call_entry(fw_loc, metric_proto, subcmd, **kwargs):
  """Calls into firmware_builder.py with the specified subcmd."""

  if fw_loc == common_pb2.PLATFORM_EC:
    fw_path = 'src/platform/ec/'
  elif fw_loc == common_pb2.PLATFORM_ZEPHYR:
    fw_path = 'src/platform/zephyr-chrome/'
  elif fw_loc == common_pb2.PLATFORM_TI50:
    fw_path = 'src/platform/ti50/common/'
  else:
    cros_build_lib.Die(f'Unknown firmware location {fw_loc}.')

  entry_point = os.path.join(constants.SOURCE_ROOT,
                             fw_path, 'firmware_builder.py')

  with tempfile.NamedTemporaryFile() as tmpfile:
    cmd = [entry_point, '--metrics', tmpfile.name, subcmd]
    for key, value in kwargs.items():
      cmd += [f'--{key.replace("_", "-")}', value]

    result = cros_build_lib.run(cmd, check=False)
    with open(tmpfile.name, 'r') as f:
      response = f.read()

  # Parse the entire metric file as our metric proto (as a passthru)
  json_format.Parse(response, metric_proto)

  if result.returncode == 0:
    return controller.RETURN_CODE_SUCCESS
  else:
    return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY


def _BuildAllTotFirmwareResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful response."""

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
  """Add a fw region metric to a successful response."""

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


def _BuildAllFirmwareResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful response."""

  metric = output_proto.success.value.add()
  metric.target_name = 'foo'
  metric.platform_name = 'bar'
  fw_section = metric.fw_section.add()
  fw_section.region = firmware_pb2.FwBuildMetric.FwSection.EC_RO
  fw_section.used = 100
  fw_section.total = 150

@faux.success(_BuildAllFirmwareResponse)
@faux.empty_completed_unsuccessfully_error
@validate.require('firmware_location')
@validate.validation_complete
def BuildAllFirmware(input_proto, output_proto, _config):
  """Build all of the firmware targets at the specified location."""

  return _call_entry(input_proto.firmware_location, output_proto.metrics,
                     'build')


def _TestAllFirmwareResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful response."""

  metric = output_proto.success.value.add()
  metric.name = 'foo-test'

@faux.success(_TestAllFirmwareResponse)
@faux.empty_completed_unsuccessfully_error
@validate.require('firmware_location')
@validate.validation_complete
def TestAllFirmware(input_proto, output_proto, _config):
  """Runs all of the firmware tests at the specified location."""

  return _call_entry(input_proto.firmware_location, output_proto.metrics,
                     'test')


def _BundleFirmwareArtifactsResponse(_input_proto, output_proto, _config):
  """Add a fw region metric to a successful response."""

  metric = output_proto.success.value.add()
  metric.name = 'foo-test'

@faux.success(_BundleFirmwareArtifactsResponse)
@faux.empty_completed_unsuccessfully_error
@validate.require('firmware_location')
@validate.validation_complete
def BundleFirmwareArtifacts(input_proto, output_proto, _config):
  """Runs all of the firmware tests at the specified location."""

  if len(input_proto.output_artifacts) > 1:
    raise ValueError('Must have exactly one output_artifact')

  with tempfile.NamedTemporaryFile() as meta:
    info = input_proto.output_artifacts[0]
    metadata_path = os.path.join(input_proto.result_path.path, meta.name)
    resp = _call_entry(
        info.location, output_proto.metrics, 'bundle',
        output_dir=input_proto.result_path.path, metadata=metadata_path)
    if common_pb2.FIRMWARE_TARBALL in info.artifact_types:
      out = output_proto.artifacts.add()
      out.artifact_types.append(common_pb2.FIRMWARE_TARBALL)
      # TODO(b/177907747): gather the paths from the response and add them to
      # out.paths.
      out.location = info.location
    if common_pb2.FIRMWARE_TARBALL_INFO in info.artifact_types:
      out = output_proto.artifacts.add()
      out.artifact_types.append(common_pb2.FIRMWARE_TARBALL_INFO)
      out.paths.append(
          common_pb2.Path(metadata_path, input_proto.result_path.path.location))
    return resp
