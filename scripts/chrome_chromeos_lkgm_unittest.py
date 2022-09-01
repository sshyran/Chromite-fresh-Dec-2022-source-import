# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the chrome_chromeos_lkgm program."""

from unittest import mock
import urllib.parse

from chromite.lib import cros_test_lib
from chromite.scripts import chrome_chromeos_lkgm


# pylint: disable=protected-access
class ChromeLKGMCommitterTester(cros_test_lib.RunCommandTestCase,
                                cros_test_lib.MockTempDirTestCase):
  """Test cros_chromeos_lkgm.Committer."""

  def setUp(self):
    """Common set up method for all tests."""
    self.committer = chrome_chromeos_lkgm.ChromeLKGMCommitter('1001.0.0',
                                                              'main')
    self.old_lkgm = None

  @mock.patch('chromite.lib.gob_util.GetFileContents')
  def testCommitNewLKGM(self, mock_get_file):
    """Tests that we can commit a new LKGM file."""
    mock_get_file.return_value = '999.0.0'
    with mock.patch.object(self.committer._gerrit_helper, 'CreateChange') as cg:
      cg.return_value = mock.MagicMock(gerrit_number=123456)
      with mock.patch.object(self.committer._gerrit_helper, 'ChangeEdit') as ce:
        with mock.patch.object(
            self.committer._gerrit_helper, 'SetReview') as bc:
          with mock.patch.object(self.committer._gerrit_helper, 'SetHashtags'):
            self.committer.UpdateLKGM()
            ce.assert_called_once_with(123456, 'chromeos/CHROMEOS_LKGM',
                                       '1001.0.0')
            bc.assert_called_once_with(123456, labels={'Bot-Commit': 1},
                                       notify='NONE')

  @mock.patch('chromite.lib.gob_util.GetFileContents')
  def testOlderLKGMFails(self, mock_get_file):
    """Tests that trying to update to an older lkgm version fails."""
    mock_get_file.return_value = '1002.0.0'
    with mock.patch.object(self.committer._gerrit_helper, 'CreateChange') as cg:
      cg.return_value = mock.MagicMock(gerrit_number=123456)
      with mock.patch.object(self.committer._gerrit_helper, 'ChangeEdit') as ce:
        self.assertRaises(chrome_chromeos_lkgm.LKGMNotValid,
                          self.committer.UpdateLKGM)
        ce.assert_not_called()

  @mock.patch('chromite.lib.gob_util.GetFileContents')
  def testVersionWithChromeBranch(self, mock_get_file):
    """Tests passing a version with a chrome branch strips the branch."""
    branch = 'refs/branch-heads/5000'
    self.committer = chrome_chromeos_lkgm.ChromeLKGMCommitter('1003.0.0-rc2',
                                                              branch)
    mock_get_file.return_value = '1002.0.0'

    with mock.patch.object(self.committer._gerrit_helper, 'CreateChange') as cg:
      cg.return_value = mock.MagicMock(gerrit_number=123456)
      with mock.patch.object(self.committer._gerrit_helper, 'ChangeEdit') as ce:
        with mock.patch.object(
            self.committer._gerrit_helper, 'SetReview') as bc:
          with mock.patch.object(self.committer._gerrit_helper, 'SetHashtags'):
            # Check the file was actually written out correctly.
            self.committer.UpdateLKGM()
            cg.assert_called_once_with('chromium/src', branch, mock.ANY, False)
            ce.assert_called_once_with(123456, 'chromeos/CHROMEOS_LKGM',
                                       '1003.0.0')
            bc.assert_called_once_with(123456, labels={'Bot-Commit': 1},
                                       notify='NONE')

  def testCommitMsg(self):
    """Tests format of the commit message."""
    self.committer._PRESUBMIT_BOTS = ['bot1', 'bot2']
    self.committer._buildbucket_id = 'some-build-id'
    commit_msg_lines = self.committer.ComposeCommitMsg().splitlines()
    self.assertIn(
        'Automated Commit: LKGM 1001.0.0 for chromeos.', commit_msg_lines)
    self.assertIn(
        'Uploaded by https://ci.chromium.org/b/some-build-id', commit_msg_lines)
    self.assertIn('CQ_INCLUDE_TRYBOTS=luci.chrome.try:bot1', commit_msg_lines)
    self.assertIn('CQ_INCLUDE_TRYBOTS=luci.chrome.try:bot2', commit_msg_lines)

  def testFindAlreadyOpenLKGMRoll(self):
    already_open_issues = [123456]
    self.committer._commit_msg_header = 'A message with spaces'
    with mock.patch.object(
        self.committer._gerrit_helper, 'Query',
        return_value=already_open_issues) as mock_query:
      self.assertEqual(
          self.committer.FindAlreadyOpenLKGMRoll(),
          already_open_issues[0])
      escaped_quotes = urllib.parse.quote('"')
      message = mock_query.call_args.kwargs['message']
      self.assertEqual(message.count(escaped_quotes), 2)
      self.assertTrue(message.startswith(escaped_quotes))
      self.assertTrue(message.endswith(escaped_quotes))
    already_open_issues = [123456, 654321]
    with mock.patch.object(
        self.committer._gerrit_helper, 'Query',
        return_value=already_open_issues):
      self.assertRaises(
          chrome_chromeos_lkgm.LKGMNotValid,
          self.committer.FindAlreadyOpenLKGMRoll)

  def testSubmitToCQ(self):
    self.committer._buildbucket_id = 'some-build-id'
    already_open_issue = 123456
    with mock.patch.object(
        self.committer._gerrit_helper, 'SetReview') as mock_review:
      self.committer.SubmitToCQ(already_open_issue)
    self.assertIn(
        self.committer._buildbucket_id, mock_review.call_args[1]['msg'])
