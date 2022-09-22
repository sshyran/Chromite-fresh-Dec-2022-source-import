# Copyright 2017 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the chrome_chromeos_lkgm program."""

from unittest import mock

from chromite.lib import cros_test_lib
from chromite.scripts import chrome_chromeos_lkgm


class StubGerritChange:
    """Stab class corresponding to cros_patch.GerritChange."""

    def __init__(self, gerrit_number, file_content, subject):
        self._gerrit_number = gerrit_number
        self._subject = subject
        self._file_content = file_content

    @property
    def subject(self):
        return self._subject

    @property
    def gerrit_number(self):
        return self._gerrit_number

    def GetFileContents(self, _path: str):
        return self._file_content


# pylint: disable=protected-access
class ChromeLKGMCommitterTester(
    cros_test_lib.RunCommandTestCase, cros_test_lib.MockTempDirTestCase
):
    """Test cros_chromeos_lkgm.Committer."""

    def setUp(self):
        """Common set up method for all tests."""
        self.committer = chrome_chromeos_lkgm.ChromeLKGMCommitter(
            "1001.0.0", "main"
        )

    @mock.patch("chromite.lib.gob_util.GetFileContents")
    def testCommitNewLKGM(self, mock_get_file):
        """Tests that we can commit a new LKGM file."""
        mock_get_file.return_value = "999.0.0"
        with mock.patch.object(
            self.committer._gerrit_helper, "CreateChange"
        ) as cg:
            cg.return_value = mock.MagicMock(gerrit_number=123456)
            with mock.patch.object(
                self.committer._gerrit_helper, "ChangeEdit"
            ) as ce:
                with mock.patch.object(
                    self.committer._gerrit_helper, "SetReview"
                ) as bc:
                    with mock.patch.object(
                        self.committer._gerrit_helper, "SetHashtags"
                    ):
                        self.committer.UpdateLKGM()
                        ce.assert_called_once_with(
                            123456, "chromeos/CHROMEOS_LKGM", "1001.0.0"
                        )
                        bc.assert_called_once_with(
                            123456,
                            labels={"Bot-Commit": 1, "Commit-Queue": 2},
                            notify="NONE",
                            ready=True,
                            reviewers=[
                                "chrome-os-gardeners-reviews@google.com"
                            ],
                        )

    @mock.patch("chromite.lib.gob_util.GetFileContents")
    def testOlderLKGMFails(self, mock_get_file):
        """Tests that trying to update to an older lkgm version fails."""
        mock_get_file.return_value = "1002.0.0"
        with mock.patch.object(
            self.committer._gerrit_helper, "CreateChange"
        ) as cg:
            cg.return_value = mock.MagicMock(gerrit_number=123456)
            with mock.patch.object(
                self.committer._gerrit_helper, "ChangeEdit"
            ) as ce:
                self.assertRaises(
                    chrome_chromeos_lkgm.LKGMNotValid, self.committer.UpdateLKGM
                )
                ce.assert_not_called()

    @mock.patch("chromite.lib.gob_util.GetFileContents")
    def testAbandonObsoleteLKGMs(self, mock_get_file):
        """Tests that trying to abandon the obsolete lkgm CLs."""
        mock_get_file.return_value = "10002.0.0"

        older_change = StubGerritChange(3876550, "10001.0.0", "10001.0.0")
        newer_change = StubGerritChange(3876551, "10003.0.0", "10003.0.0")
        open_issues = [older_change, newer_change]

        with mock.patch.object(
            self.committer._gerrit_helper, "Query", return_value=open_issues
        ) as mock_query:
            with mock.patch.object(
                self.committer._gerrit_helper, "AbandonChange"
            ) as ac:
                self.committer.AbandonObsoleteLKGMRolls()
                mock_query.assert_called_once()
                ac.assert_called_once_with((older_change), msg=mock.ANY)

    @mock.patch("chromite.lib.gob_util.GetFileContents")
    def testVersionWithChromeBranch(self, mock_get_file):
        """Tests passing a version with a chrome branch strips the branch."""
        branch = "refs/branch-heads/5000"
        self.committer = chrome_chromeos_lkgm.ChromeLKGMCommitter(
            "1003.0.0-rc2", branch
        )
        mock_get_file.return_value = "1002.0.0"

        with mock.patch.object(
            self.committer._gerrit_helper, "CreateChange"
        ) as cg:
            cg.return_value = mock.MagicMock(gerrit_number=123456)
            with mock.patch.object(
                self.committer._gerrit_helper, "ChangeEdit"
            ) as ce:
                with mock.patch.object(
                    self.committer._gerrit_helper, "SetReview"
                ) as bc:
                    with mock.patch.object(
                        self.committer._gerrit_helper, "SetHashtags"
                    ):
                        # Check the file was actually written out correctly.
                        self.committer.UpdateLKGM()
                        cg.assert_called_once_with(
                            "chromium/src", branch, mock.ANY, False
                        )
                        ce.assert_called_once_with(
                            123456, "chromeos/CHROMEOS_LKGM", "1003.0.0"
                        )
                        bc.assert_called_once_with(
                            123456,
                            labels={"Bot-Commit": 1, "Commit-Queue": 2},
                            notify="NONE",
                            ready=True,
                            reviewers=[
                                "chrome-os-gardeners-reviews@google.com"
                            ],
                        )

    def testCommitMsg(self):
        """Tests format of the commit message."""
        self.committer._PRESUBMIT_BOTS = ["bot1", "bot2"]
        self.committer._buildbucket_id = "some-build-id"
        commit_msg_lines = self.committer.ComposeCommitMsg().splitlines()
        self.assertIn(
            "Automated Commit: LKGM 1001.0.0 for chromeos.", commit_msg_lines
        )
        self.assertIn(
            "Uploaded by https://ci.chromium.org/b/some-build-id",
            commit_msg_lines,
        )
        self.assertIn(
            "CQ_INCLUDE_TRYBOTS=luci.chrome.try:bot1", commit_msg_lines
        )
        self.assertIn(
            "CQ_INCLUDE_TRYBOTS=luci.chrome.try:bot2", commit_msg_lines
        )
