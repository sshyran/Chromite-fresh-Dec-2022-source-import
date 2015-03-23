# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for cros."""

from __future__ import print_function

from chromite.cli import command
from chromite.lib import cros_test_lib
from chromite.lib import stats
from chromite.lib import stats_unittest
from chromite.scripts import cros


class RunScriptTest(cros_test_lib.MockTempDirTestCase):
  """Test the main functionality."""

  def setUp(self):
    self.stats_module_mock = stats_unittest.StatsModuleMock()
    self.StartPatcher(self.stats_module_mock)
    self.PatchObject(cros, '_RunSubCommand', autospec=True)
    # Use the `cros` toolset for these tests.
    self.PatchObject(command, '_GetToolset', autospec=True, return_value='cros')

  def testStatsUpload(self, upload_count=1, return_value=0):
    """Test stats uploading."""
    return_value = cros.main(['chrome-sdk', '--board', 'lumpy'])
    # pylint: disable=protected-access
    self.assertEquals(stats.StatsUploader._Upload.call_count, upload_count)
    # pylint: enable=protected-access
    self.assertEquals(return_value, return_value)

  def testStatsUploadError(self):
    """We don't upload stats if the stats creation failed."""
    self.stats_module_mock.stats_mock.init_exception = True
    with cros_test_lib.LoggingCapturer():
      self.testStatsUpload(upload_count=0)
