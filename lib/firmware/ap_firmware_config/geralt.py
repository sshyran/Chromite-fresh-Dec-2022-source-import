# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Geralt configs."""

from typing import List, Optional

from chromite.lib.firmware import servo_lib


BUILD_PACKAGES = (
    # TODO: enable after ec ready: "chromeos-zephyr",
    "coreboot",
    "depthcharge",
    "libpayload",
    "chromeos-bmpblk",
    "chromeos-bootimage",
)


def deploy_extra_flags_futility(servo: Optional[servo_lib.Servo]) -> List[str]:
    """Returns extra flags for flashing with futility.

    Args:
        servo: The servo connected to the target DUT. Return flags for ssh if
            None.

    Returns:
        extra_flags: List of extra flags.
    """
    if not servo:
        # extra flags for flashing with futility directly over ssh
        return []
    if servo.is_ccd:
        # when flashing over CCD, skip verify step
        return ["--fast"]
    return []


def deploy_extra_flags_flashrom(servo: Optional[servo_lib.Servo]) -> List[str]:
    """Returns extra flags for flashing with flashrom.

    Args:
        servo: The servo connected to the target DUT. Return flags for ssh if
            None.

    Returns:
        extra_flags: List of extra flags.
    """
    if not servo:
        # extra flags for flashing with flashrom directly over ssh
        return []
    if servo.is_ccd:
        # when flashing over CCD, skip verify step
        return ["-n"]
    return []


def get_config(servo: servo_lib.Servo) -> servo_lib.ServoConfig:
    """Get DUT controls and programmer argument to flash a build target.

    Each board needs specific config including the voltage for Vref, to turn
    on and turn off the SPI flash. get_config() returns servo_lib.ServoConfig
    with settings to flash a servo for a particular build target.
    The voltage for this board needs to be set to 1.8 V.

    Args:
        servo: The servo connected to the target DUT.

    Returns:
        servo_lib.ServoConfig:
            dut_control_{on, off}=2d arrays formatted like
                [["cmd1", "arg1", "arg2"], ["cmd2", "arg3", "arg4"]]
                where cmd1 will be run before cmd2.
            programmer=programmer argument (-p) for flashrom and futility.
    """
    dut_control_on = [["cpu_fw_spi:on"]]
    dut_control_off = [["cpu_fw_spi:off"]]
    if servo.is_micro or servo.is_c2d2:
        programmer = "raiden_debug_spi:serial=%s" % servo.serial
    elif servo.is_ccd:
        dut_control_on = []
        dut_control_off = []
        programmer = "raiden_debug_spi:target=AP,serial=%s" % servo.serial
    else:
        raise servo_lib.UnsupportedServoVersionError(
            "%s not supported" % servo.version
        )

    return servo_lib.ServoConfig(dut_control_on, dut_control_off, programmer)