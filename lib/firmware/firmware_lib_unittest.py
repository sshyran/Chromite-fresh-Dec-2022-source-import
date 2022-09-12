# Copyright 2021 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests for the firmware_lib module."""

from unittest import mock

from chromite.lib import build_target_lib
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.lib.firmware import firmware_config
from chromite.lib.firmware import firmware_lib


class CleanTest(cros_test_lib.RunCommandTestCase):
    """Tests for cleaning up firmware artifacts and dependencies."""

    def setUp(self):
        self.pkgs = [
            "pkg1",
            "pkg2",
            "coreboot-private-files",
            "chromeos-config-bsp",
        ]

    def test_clean(self):
        """Sanity check for the clean command (ideal case)."""
        fw_config = mock.MagicMock(
            build_workon_packages=None, build_packages=("pkg3", "pkg4")
        )

        self.PatchObject(firmware_config, "get_config", return_value=fw_config)

        pkgs = [*self.pkgs, *fw_config.build_packages]

        def run_side_effect(*args, **kwargs):
            if args[0][0].startswith("qfile"):
                if kwargs.get("capture_output"):
                    return mock.MagicMock(stdout="\n".join(pkgs).encode())
                return mock.MagicMock(stdout="".encode())
            elif args[0][0].startswith("emerge"):
                return mock.MagicMock(returncode=0)

        run_mock = self.PatchObject(
            cros_build_lib, "run", side_effect=run_side_effect
        )
        self.PatchObject(osutils, "RmDir")
        firmware_lib.clean(build_target_lib.BuildTarget("boardname"))
        run_mock.assert_any_call(
            [mock.ANY, mock.ANY, *sorted(pkgs)],
            capture_output=mock.ANY,
            dryrun=False,
        )

    def test_nonexistent_board_clean(self):
        """Verifies exception thrown when target board was not configured."""
        se = cros_build_lib.RunCommandError("nonexistent board")
        self.PatchObject(cros_build_lib, "run", side_effect=se)
        with self.assertRaisesRegex(firmware_lib.CleanError, "qfile"):
            firmware_lib.clean(build_target_lib.BuildTarget("schrodinger"))
