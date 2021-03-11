# -*- coding: utf-8 -*-
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Servo-related functionality."""

from __future__ import print_function

from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging


SERVO_C2D2 = 'c2d2'
SERVO_CCD_CR50 = 'ccd_cr50'
SERVO_MICRO = 'servo_micro'
SERVO_V2 = 'servo_v2'
SERVO_V4_CCD = 'servo_v4_with_ccd_cr50'
SERVO_V4_MICRO = 'servo_v4_with_servo_micro'

VALID_SERVOS = (
    SERVO_C2D2,
    SERVO_CCD_CR50,
    SERVO_MICRO,
    SERVO_V2,
    SERVO_V4_CCD,
    SERVO_V4_MICRO,
)

CCD_SERVOS = (SERVO_CCD_CR50, SERVO_V4_CCD)
MICRO_SERVOS = (SERVO_MICRO, SERVO_V4_MICRO)
V2_SERVOS = (SERVO_V2,)
V4_SERVOS = (SERVO_V4_CCD, SERVO_V4_MICRO)

_SERIAL_NUMBER_OPTION = 'serialname'
_SERIAL_NUMBER_OPTION_OVERRIDE = {
    SERVO_V4_CCD: 'ccd_serialname',
    SERVO_V4_MICRO: 'servo_micro_serialname',
}


class Error(Exception):
  """Base error class for the module."""


class InvalidServoVersion(Error):
  """Invalid servo version error."""


class DutConnectionError(Error):
  """Error when fetching data from a dut."""


class DutControl(object):
  """Wrapper for dut_control calls."""

  def __init__(self, port):
    self._base_cmd = ['dut-control']
    if port:
      self._base_cmd.append('--port=%s' % port)

  def get_value(self, arg):
    """Get the value of |arg| from dut_control."""
    try:
      result = cros_build_lib.run(
          self._base_cmd + [arg], stdout=True, encoding='utf-8')
    except cros_build_lib.CalledProcessError as e:
      logging.debug('dut-control error: %s', str(e))
      raise DutConnectionError(
          'Could not establish servo connection. Verify servod is running in '
          'the background, and the servo is properly connected.')

    # Return value from the "key:value" output.
    return result.stdout.partition(':')[2].strip()

  def run(self, cmd_fragment, verbose=False, dryrun=False):
    """Run a dut_control command.

    Args:
      cmd_fragment (list[str]): The dut_control command to run.
      verbose (bool): Whether to print the command before it's run.
      dryrun (bool): Whether to actually execute the command or just print it.
    """
    cros_build_lib.run(
        self._base_cmd + cmd_fragment, print_cmd=verbose, dryrun=dryrun)

  def run_all(self, cmd_fragments, verbose=False, dryrun=False):
    """Run multiple dut_control commands in the order given.

    Args:
      cmd_fragments (list[list[str]]): The dut_control commands to run.
      verbose (bool): Whether to print the commands as they are run.
      dryrun (bool): Whether to actually execute the command or just print it.
    """
    for cmd in cmd_fragments:
      self.run(cmd, verbose=verbose, dryrun=dryrun)


class Servo(object):
  """Data class for servos."""

  def __init__(self, version, serial):
    assert version in VALID_SERVOS
    self.version = version
    self.serial = serial

  @property
  def is_ccd(self):
    return self.version in CCD_SERVOS

  @property
  def is_c2d2(self):
    return self.version == SERVO_C2D2

  @property
  def is_micro(self):
    return self.version in MICRO_SERVOS

  @property
  def is_v2(self):
    return self.version in V2_SERVOS

  @property
  def is_v4(self):
    return self.version in V4_SERVOS


def get(dut_ctl: DutControl) -> Servo:
  """Get the Servo instance the given dut_control command is using.

  Args:
    dut_ctl: The dut_control command wrapper instance.
  """
  version = dut_ctl.get_value('servo_type')
  if version not in VALID_SERVOS:
    raise InvalidServoVersion('Unrecognized servo version: %s' % version)

  option = _SERIAL_NUMBER_OPTION_OVERRIDE.get(version, _SERIAL_NUMBER_OPTION)
  serial = dut_ctl.get_value(option)
  return Servo(version, serial)
