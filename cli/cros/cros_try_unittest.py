# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Tests the `cros try` command."""

from pathlib import Path
from typing import List

from chromite.cli.cros import cros_try
from chromite.lib import cros_test_lib
from chromite.scripts import cros


MOCK_TRY_DIR = Path("/tmp/try")
MOCK_TRY_BIN = MOCK_TRY_DIR / "try"


class TryCommandTest(cros_test_lib.RunCommandTestCase):
    """Test the TryCommand class."""

    def setUp(self):
        """Create patches."""
        self.PatchObject(
            cros_try, "_InstallTryPackage", return_value=MOCK_TRY_BIN
        )

    def runCrosTry(self, try_args: List[str]):
        """Simulate running the `cros try` command with the specified args."""
        return cros.main(["try"] + try_args)

    def testArgsForwarding(self):
        """Test that calling `cros try` forwards args to the try binary."""
        self.runCrosTry(["release", "-staging"])
        self.rc.assertCommandCalled(
            [str(MOCK_TRY_BIN), "release", "-staging"], check=False
        )

    def testExitCode(self):
        """Test that `cros try` returns the try binary's exit code."""
        self.rc.AddCmdResult([str(MOCK_TRY_BIN), "invalid-cmd"], returncode=128)
        actual_retcode = self.runCrosTry(["invalid-cmd"])
        self.assertEqual(actual_retcode, 128)
