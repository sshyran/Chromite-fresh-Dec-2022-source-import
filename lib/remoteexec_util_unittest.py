
# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for remoteexec_util.py"""

import os

from chromite.lib import remoteexec_util
from chromite.lib import cros_test_lib
from chromite.lib import osutils


class TestRemoteexecUtil(cros_test_lib.MockTempDirTestCase):
  """Tests for remoteexec_util."""

  def testExtraEnvCustomChroot(self):
    """Test that the extra chroot envs for remoteexec are correct."""
    reclient_dir = os.path.join(self.tempdir, 'cipd/rbe')
    reproxy_cfg_file = os.path.join(self.tempdir,
                                    'reclient_cfgs/reproxy_config.cfg')

    osutils.SafeMakedirs(reclient_dir)
    osutils.SafeMakedirs(reproxy_cfg_file)
    remote = remoteexec_util.Remoteexec(reclient_dir, reproxy_cfg_file)

    chroot_env = remote.GetChrootExtraEnv()
    self.assertEndsWith(chroot_env['RECLIENT_DIR'], '/reclient')
    self.assertEndsWith(chroot_env['REPROXY_CFG_FILE'], '/reproxy_chroot.cfg')
