# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for cros_update."""

from __future__ import print_function

import mock

from chromite.lib import auto_updater
from chromite.lib import auto_updater_transfer
from chromite.lib import cros_test_lib
from chromite.scripts import cros_update


# pylint: disable=protected-access

class CrosUpdateTest(cros_test_lib.RunCommandTestCase):
  """Tests cros_update functions."""

  def setUp(self):
    """Setup an instance of CrOSUpdateTrigger."""
    self._cros_update_trigger = cros_update.CrOSUpdateTrigger(
        'foo-host-name', 'foo-build-name', 'foo-static-dir',
        static_url='foo-static', devserver_url='foo-devserver-url')
    self._cros_updater = auto_updater.ChromiumOSUpdater(
        mock.MagicMock(work_dir='foo-dir'), 'foo-build-name', 'foo-payload-dir',
        transfer_class=auto_updater_transfer.LocalTransfer)
