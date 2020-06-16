# -*- coding: utf-8 -*-
# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""An executable function cros-update for auto-update of a CrOS host.

The reason to create this file is to let devserver to trigger a background
process for CrOS auto-update. Therefore, when devserver service is restarted
sometimes, the CrOS auto-update process is still running and the corresponding
provision task won't claim failure.

It includes two classes:
  a. CrOSUpdateTrigger:
    1. Includes all logics which identify which types of update need to be
       performed in the current DUT.
    2. Responsible for write current status of CrOS auto-update process into
       progress_tracker.

  b. CrOSAUParser:
    1. Pre-setup the required args for CrOS auto-update.
    2. Parse the input parameters for cmd that runs 'cros_update.py'.
"""

from __future__ import print_function

import os
import traceback

from chromite.lib import auto_updater
from chromite.lib import auto_updater_transfer
from chromite.lib import commandline
from chromite.lib import cros_logging as logging
from chromite.lib import cros_update_logging
from chromite.lib import cros_update_progress
from chromite.lib import remote_access
from chromite.lib import timeout_util


# The build channel for recovering host's stateful partition.
STABLE_BUILD_CHANNEL = 'stable-channel'

# Timeout for CrOS auto-update process.
CROS_UPDATE_TIMEOUT_MIN = 30

# The preserved path in remote device, won't be deleted after rebooting.
CROS_PRESERVED_PATH = ('/mnt/stateful_partition/unencrypted/'
                       'preserve/cros-update')

# Standard error tmeplate to be written into status tracking log.
CROS_ERROR_TEMPLATE = cros_update_progress.ERROR_TAG + ' %s'

# Setting logging level
logConfig = cros_update_logging.loggingConfig()
logConfig.ConfigureLogging()


class CrOSUpdateTrigger(object):
  """The class for CrOS auto-updater trigger.

  This class is used for running all CrOS auto-update trigger logic.
  """

  def __init__(self, host_name, build_name, static_dir, progress_tracker=None,
               log_file=None, au_tempdir=None, force_update=False,
               full_update=False, payload_filename=None,
               clobber_stateful=True, devserver_url=None, static_url=None,
               staging_server=None, transfer_class=None):
    self.host_name = host_name
    self.build_name = build_name
    self.static_dir = static_dir
    self.progress_tracker = progress_tracker
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

  def _WriteAUStatus(self, content):
    if self.progress_tracker:
      self.progress_tracker.WriteStatus(content)

  def _StatefulUpdate(self, cros_updater):
    """The detailed process in stateful update.

    Args:
      cros_updater: The CrOS auto updater for auto-update.
    """
    self._WriteAUStatus('pre-setup stateful update')
    cros_updater.PreSetupStatefulUpdate()
    self._WriteAUStatus('perform stateful update')
    cros_updater.UpdateStateful()
    self._WriteAUStatus('post-check stateful update')
    cros_updater.PostCheckStatefulUpdate()

  def _RootfsUpdate(self, cros_updater):
    """The detailed process in rootfs update.

    Args:
      cros_updater: The CrOS auto updater for auto-update.
    """
    self._WriteAUStatus('Check whether devserver can run before rootfs update')
    cros_updater.CheckDevserverRun()
    self._WriteAUStatus('transfer rootfs update package')
    cros_updater.TransferRootfsUpdate()
    self._WriteAUStatus('pre-setup rootfs update')
    cros_updater.PreSetupRootfsUpdate()
    self._WriteAUStatus('rootfs update')
    cros_updater.UpdateRootfs()
    self._WriteAUStatus('post-check rootfs update')
    cros_updater.PostCheckRootfsUpdate()

  def TriggerAU(self):
    """Execute auto update for cros_host.

    The auto update includes 4 steps:
    1. if devserver cannot run, restore the stateful partition.
    2. if possible, do stateful update first, but never raise errors, except
       for timeout_util.TimeoutError caused by system.signal.
    3. If required or stateful_update fails, first do rootfs update, then do
       stateful_update.
    4. Post-check for the whole update.
    """
    try:
      with remote_access.ChromiumOSDeviceHandler(
          self.host_name, port=None,
          base_dir=CROS_PRESERVED_PATH,
          ping=False) as device:

        logging.debug('Remote device %s is connected', self.host_name)
        payload_dir = os.path.join(self.static_dir, self.build_name)

        chromeos_AU = auto_updater.ChromiumOSUpdater(
            device, self.build_name, payload_dir,
            tempdir=self.au_tempdir,
            log_file=self.log_file,
            yes=True,
            payload_filename=self.payload_filename,
            clobber_stateful=self.clobber_stateful,
            staging_server=self.staging_server,
            transfer_class=self.transfer_class)

        # Get nebraska request logfiles dir from auto_updater.
        self._request_logs_dir = chromeos_AU.request_logs_dir

        chromeos_AU.CheckPayloads()

        version_match = chromeos_AU.PreSetupCrOSUpdate()
        self._WriteAUStatus('Transfer Devserver/Stateful Update Package')
        chromeos_AU.TransferDevServerPackage()
        chromeos_AU.TransferStatefulUpdate()

        restore_stateful = chromeos_AU.CheckRestoreStateful()
        do_stateful_update = (not self.full_update and
                              version_match and self.force_update)
        stateful_update_complete = False
        logging.debug('Start CrOS update process...')
        try:
          if restore_stateful:
            self._WriteAUStatus('Restore Stateful Partition')
            chromeos_AU.RestoreStateful()
            stateful_update_complete = True
          else:
            # Whether to execute stateful update depends on:
            # a. full_update=False: No full reimage is required.
            # b. The update version is matched to the current version, And
            #    force_update=True: Update is forced even if the version
            #    installed is the same.
            if do_stateful_update:
              self._StatefulUpdate(chromeos_AU)
              stateful_update_complete = True

        except timeout_util.TimeoutError:
          raise
        except Exception as e:
          logging.debug('Error happens in stateful update: %r', e)

        # Whether to execute rootfs update depends on:
        # a. stateful update is not completed, or completed by
        #    update action 'restore_stateful'.
        # b. force_update=True: Update is forced no matter what the current
        #    version is. Or, the update version is not matched to the current
        #    version.
        require_rootfs_update = self.force_update or (
            not chromeos_AU.CheckVersion())
        if (not (do_stateful_update and stateful_update_complete)
            and require_rootfs_update):
          self._RootfsUpdate(chromeos_AU)
          self._StatefulUpdate(chromeos_AU)

        self._WriteAUStatus('post-check for CrOS auto-update')
        chromeos_AU.PostCheckCrOSUpdate()

        self._WriteAUStatus(cros_update_progress.FINISHED)

        logging.debug('Autoupdate successfully completed')

    except Exception as e:
      logging.debug('Error happens in CrOS auto-update: %r', e)
      self._WriteAUStatus(CROS_ERROR_TEMPLATE % str(traceback.format_exc()))
      raise


def ParseArguments(argv):
  """Returns a namespace for the CLI arguments."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('--hostname', type=str, dest='host_name',
                      help='host_name of a DUT')
  parser.add_argument('-b', type=str, dest='build_name',
                      help='build name to be auto-updated')
  parser.add_argument('--static_dir', type='path',
                      help='static directory of the devserver')
  parser.add_argument('--force_update', action='store_true', default=False,
                      help='force an update even if the version installed is '
                           'the same')
  parser.add_argument('--full_update', action='store_true', default=False,
                      help='force a rootfs update, skip stateful update')
  parser.add_argument('--payload_filename', type=str,
                      help='A custom payload filename')
  parser.add_argument('--clobber_stateful', action='store_true', default=False,
                      help='Whether to clobber stateful')
  parser.add_argument('--devserver_url', type=str,
                      help='Devserver URL base for RPCs')
  parser.add_argument('--static_url', type=str,
                      help='Devserver URL base for static files')

  opts = parser.parse_args(argv)
  opts.Freeze()

  return opts


def main(argv):
  options = ParseArguments(argv)

  # Use process group id as the unique id in track and log files, since
  # os.setsid is executed before the current process is run.
  pid = os.getpid()
  pgid = os.getpgid(pid)

  # Setting log files for CrOS auto-update process.
  # Log file:  file to record every details of CrOS auto-update process.
  log_file = cros_update_progress.GetExecuteLogFile(options.host_name, pgid)
  logging.info('Writing executing logs into file: %s', log_file)
  logConfig.SetFileHandler(log_file)

  # Create a progress_tracker for tracking CrOS auto-update progress.
  progress_tracker = cros_update_progress.AUProgress(options.host_name, pgid)

  # Create a dir for temporarily storing devserver codes and logs.
  au_tempdir = cros_update_progress.GetAUTempDirectory(options.host_name, pgid)

  # Create cros_update instance to run CrOS auto-update.
  cros_updater_trigger = CrOSUpdateTrigger(
      options.host_name, options.build_name, options.static_dir,
      progress_tracker=progress_tracker,
      log_file=log_file,
      au_tempdir=au_tempdir,
      force_update=options.force_update,
      full_update=options.full_update,
      payload_filename=options.payload_filename,
      clobber_stateful=options.clobber_stateful,
      devserver_url=options.devserver_url,
      static_url=options.static_url)

  # Set timeout the cros-update process.
  try:
    with timeout_util.Timeout(CROS_UPDATE_TIMEOUT_MIN * 60):
      cros_updater_trigger.TriggerAU()
  except timeout_util.TimeoutError as e:
    error_msg = ('%s. The CrOS auto-update process is timed out, thus will be '
                 'terminated' % str(e))
    progress_tracker.WriteStatus(CROS_ERROR_TEMPLATE % error_msg)
