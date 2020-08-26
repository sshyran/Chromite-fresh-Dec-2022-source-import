# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for cros_update."""

from __future__ import print_function

from chromite.lib import auto_updater
from chromite.lib import cros_test_lib
from chromite.scripts import cros_update


class CrosUpdateTest(cros_test_lib.RunCommandTestCase):
  """Tests cros_update functions."""

  def testTriggerAU(self):
    cros_update_trigger = cros_update.CrOSUpdateTrigger(
        'foo-host-name', 'foo-build-name', 'foo-static-dir')
    run_update_mock = self.PatchObject(auto_updater.ChromiumOSUpdater,
                                       'RunUpdate')
    cros_update_trigger.TriggerAU()
    run_update_mock.assert_called_once()
