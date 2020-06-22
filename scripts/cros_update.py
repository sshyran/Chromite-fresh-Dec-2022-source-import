# -*- coding: utf-8 -*-
# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""An utility for running updates over a DUT. (DEPRECATED: DO NOT USE.)"""

from __future__ import print_function

import os

from chromite.lib import auto_updater
from chromite.lib import auto_updater_transfer
from chromite.lib import cros_logging as logging
from chromite.lib import remote_access

# The preserved path in remote device, won't be deleted after rebooting.
CROS_PRESERVED_PATH = ('/mnt/stateful_partition/unencrypted/'
                       'preserve/cros-update')

# DO NOT USE THIS CLASS ANYMORE.
# TODO(crbug.com/1071483): remove this class once M85 is passed the stable.
class CrOSUpdateTrigger(object):
  """The class for CrOS auto-updater trigger."""

  def __init__(self, host_name, build_name, static_dir,
               log_file=None, au_tempdir=None, force_update=False,
               full_update=False, payload_filename=None,
               clobber_stateful=True, devserver_url=None, static_url=None,
               staging_server=None, transfer_class=None):
    self.host_name = host_name
    self.build_name = build_name
    self.static_dir = static_dir
    self.log_file = log_file
    self.au_tempdir = au_tempdir
    self.force_update = force_update
    self.full_update = full_update
    self.payload_filename = payload_filename
    self.clobber_stateful = clobber_stateful
    self.devserver_url = devserver_url
    self.static_url = static_url
    self.staging_server = staging_server
    self.transfer_class = transfer_class or auto_updater_transfer.LocalTransfer
    self._request_logs_dir = None

  @property
  def request_logs_dir(self):
    """Gets dire containing logs created by the nebraska process."""
    return self._request_logs_dir

  def TriggerAU(self):
    """Runs auto update."""
    try:
      with remote_access.ChromiumOSDeviceHandler(
          self.host_name, base_dir=CROS_PRESERVED_PATH) as device:
        logging.debug('Remote device %s is connected', self.host_name)

        payload_dir = os.path.join(self.static_dir, self.build_name)
        chromeos_AU = auto_updater.ChromiumOSUpdater(
            device, self.build_name, payload_dir,
            tempdir=self.au_tempdir,
            log_file=self.log_file,
            yes=True,
            payload_filename=self.payload_filename,
            clobber_stateful=self.clobber_stateful,
            do_stateful_update=False,
            staging_server=self.staging_server,
            transfer_class=self.transfer_class)

        # Get nebraska request logfiles dir from auto_updater.
        self._request_logs_dir = chromeos_AU.request_logs_dir

        chromeos_AU.RunUpdate()

    except Exception as e:
      logging.debug('Error happens in CrOS auto-update: %r', e)
      raise

def main():
  logging.notice('This binary is deprecated. DO NOT USE.')
