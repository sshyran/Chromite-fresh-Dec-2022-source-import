# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Skyrim configs."""

from chromite.lib.firmware import servo_lib

BUILD_PACKAGES = (
    'chromeos-ec',
    'coreboot',
    'depthcharge',
    'libpayload',
    'vboot_reference',
    'chromeos-bootimage',
    'coreboot-private-files-board',
    'coreboot-private-files-chipset',
    'amd-cezanne-fsp',
)


def get_config(servo: servo_lib.Servo) -> servo_lib.ServoConfig:
  """Get DUT controls and programmer argument to flash Guybrush.

  Each board needs specific config including the voltage for Vref, to turn
  on and turn off the SPI flash. get_config() returns servo_lib.ServoConfig
  with settings to flash a servo for a particular build target.
  The voltage for this board needs to be set to 1.8 V.

  Args:
    servo: The servo connected to the target DUT.

  Returns:
    servo_lib.ServoConfig:
      dut_control_{on, off}=2d arrays formatted like [["cmd1", "arg1", "arg2"],
                                                      ["cmd2", "arg3", "arg4"]]
                            where cmd1 will be run before cmd2.
      programmer=programmer argument (-p) for flashrom and futility.
  """
  dut_control_on = []
  dut_control_off = []

  # Common flashing sequence for C2D2 and CCD
  # Shutdown AP so that it enters G3 state.
  dut_control_on.append(['ec_uart_cmd:apshutdown'])
  # Sleep to ensure the SoC rails get chance to discharge enough.
  dut_control_on.append(['sleep:5'])

  if servo.is_c2d2:
    # CPLD will actually require AP_FLASH_SELECT of 0 in flashing
    dut_control_on.append(['ap_flash_select:off'])
    dut_control_on.append(['spi2_vref:pp1800'])
    dut_control_off.append(['spi2_vref:off'])
    programmer = 'raiden_debug_spi:serial=%s' % servo.serial
  elif servo.is_micro:
    # Note servo micro is only supported for dauntless daughterboard for
    # a limited time. Once Dauntless moves to MLB, there will be no 50-pin
    # servo connector to attach servo micro to.
    dut_control_on.append(['ec_uart_cmd:apshutdown'])
    dut_control_on.append([
        'spi2_vref:pp1800',
        'spi2_buf_en:on',
        'spi2_buf_on_flex_en:on',
        'spi_hold:off',
    ])
    dut_control_off.append([
        'spi2_vref:off',
        'spi2_buf_en:off',
        'spi2_buf_on_flex_en:off',
        'spi_hold:off',
    ])
    dut_control_off.append(['ec_uart_cmd:powerb'])
    programmer = 'raiden_debug_spi:serial=%s' % servo.serial
  elif servo.is_ccd:
    dut_control_off.append(['power_state:reset'])
    programmer = ('raiden_debug_spi:target=AP,custom_rst=True,serial=%s' %
                  servo.serial)
  else:
    raise servo_lib.UnsupportedServoVersionError('%s not supported' %
                                                 servo.version)

  return servo_lib.ServoConfig(dut_control_on, dut_control_off, programmer)
