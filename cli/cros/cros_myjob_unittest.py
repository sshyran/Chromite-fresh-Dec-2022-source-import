# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests the `cros myjob` command."""

from chromite.lib import cipd
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.scripts import cros


MOCK_MYJOB_DIR = "/tmp/myjob"
MOCK_MYJOB_BIN = f"{MOCK_MYJOB_DIR}/myjob"


class MyjobCommandTest(cros_test_lib.MockTestCase):
    """Test the MyjobCommand class."""

    def setUp(self):
        """Create patches."""
        self.PatchObject(cipd, "InstallPackage", return_value=MOCK_MYJOB_DIR)
        self._run_patch = self.PatchObject(cros_build_lib, "run")

    def runCrosMyjob(self, myjob_args):
        """Simulate running the `cros myjob` command with the specified args."""
        cros.main(["myjob"] + myjob_args)

    def testArgsForwarding(self):
        """Test that calling `cros myjob` forwards args to the myjob binary."""
        self.runCrosMyjob(["release", "-staging"])
        self._run_patch.assert_called_with(
            [MOCK_MYJOB_BIN, "release", "-staging"]
        )
