# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module to use remoteexec from builders."""

import getpass
import os


class Remoteexec(object):
  """Interface to use remoteexec on bots."""

  def __init__(self, reclient_dir, reproxy_cfg_file):
    """Initializes a Remoteexec instance.

    Args:
      reclient_dir: Path to the re-client directory that contains
        the reproxy, bootstrap, rewrapper binaries.
      reproxy_cfg_file: Path to the config file for starting reproxy.
    """

    if not os.path.isdir(reclient_dir):
      raise ValueError(
          f'reclient_dir does not point to a directory: {reclient_dir}')

    if not os.path.exists(reproxy_cfg_file):
      raise ValueError(
          f'reproxy_cfg_file does not exist: {reproxy_cfg_file}')

    self.reclient_dir = reclient_dir
    self.reproxy_cfg_file = reproxy_cfg_file

  def GetChrootExtraEnv(self):
    """Extra env vars set to do remoteexec inside chroot."""
    reclient_dir = os.path.join('/home', getpass.getuser(), 'reclient')
    reproxy_cfg_file = os.path.join('/home', getpass.getuser(),
                                    'reclient_cfgs', 'reproxy_chroot.cfg')
    result = {'RECLIENT_DIR': reclient_dir,
              'REPROXY_CFG_FILE': reproxy_cfg_file}

    return result
