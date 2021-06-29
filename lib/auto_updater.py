# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Library containing functions to execute auto-update on a remote device.

ChromiumOSUpdater includes:
  ----Check-----
  * Check functions, including kernel/version/cgpt check.

  ----Precheck---
  * Pre-check if the device can run its nebraska.
  * Pre-check for stateful/rootfs update/whole update.

  ----Tranfer----
  * This step is carried out by Transfer subclasses in
    auto_updater_transfer.py.

  ----Auto-Update---
  * Do rootfs partition update if it's required.
  * Do stateful partition update if it's required.
  * Do reboot for device if it's required.

  ----Verify----
  * Do verification if it's required.
  * Disable rootfs verification in device if it's required.
  * Post-check stateful/rootfs update/whole update.
"""

import json
import os
import re
import subprocess
import tempfile
import time

from chromite.cli import command
from chromite.lib import auto_update_util
from chromite.lib import auto_updater_transfer
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import nebraska_wrapper
from chromite.lib import operation
from chromite.lib import remote_access
from chromite.lib import retry_util
from chromite.lib import stateful_updater
from chromite.lib import timeout_util

from chromite.utils import key_value_store


# Naming conventions for global variables:
#   File on remote host without slash: REMOTE_XXX_FILENAME
#   File on remote host with slash: REMOTE_XXX_FILE_PATH
#   Path on remote host with slash: REMOTE_XXX_PATH
#   File on local server without slash: LOCAL_XXX_FILENAME

# Update Status for remote device.
UPDATE_STATUS_IDLE = 'UPDATE_STATUS_IDLE'
UPDATE_STATUS_DOWNLOADING = 'UPDATE_STATUS_DOWNLOADING'
UPDATE_STATUS_FINALIZING = 'UPDATE_STATUS_FINALIZING'
UPDATE_STATUS_UPDATED_NEED_REBOOT = 'UPDATE_STATUS_UPDATED_NEED_REBOOT'

# Max number of the times for retry:
# 1. for transfer functions to be retried.
# 2. for some retriable commands to be retried.
MAX_RETRY = 5

# The delay between retriable tasks.
DELAY_SEC_FOR_RETRY = 5

# Number of seconds to wait for the post check version to settle.
POST_CHECK_SETTLE_SECONDS = 15

# Number of seconds to delay between post check retries.
POST_CHECK_RETRY_SECONDS = 5


class ChromiumOSUpdateError(Exception):
  """Thrown when there is a general ChromiumOS-specific update error."""


class PreSetupUpdateError(ChromiumOSUpdateError):
  """Raised for the rootfs/stateful update pre-setup failures."""


class RootfsUpdateError(ChromiumOSUpdateError):
  """Raised for the Rootfs partition update failures."""


class StatefulUpdateError(ChromiumOSUpdateError):
  """Raised for the stateful partition update failures."""


class AutoUpdateVerifyError(ChromiumOSUpdateError):
  """Raised for verification failures after auto-update."""


class RebootVerificationError(ChromiumOSUpdateError):
  """Raised for failing to reboot errors."""


class BaseUpdater(object):
  """The base updater class."""

  def __init__(self, device, payload_dir):
    self.device = device
    self.payload_dir = payload_dir


class ChromiumOSUpdater(BaseUpdater):
  """Used to update DUT with image."""

  # Nebraska files.
  LOCAL_NEBRASKA_LOG_FILENAME = 'nebraska.log'
  REMOTE_NEBRASKA_FILENAME = 'nebraska.py'

  # rootfs update files.
  REMOTE_UPDATE_ENGINE_BIN_FILENAME = 'update_engine_client'
  REMOTE_UPDATE_ENGINE_LOGFILE_PATH = '/var/log/update_engine.log'

  UPDATE_CHECK_INTERVAL_PROGRESSBAR = 0.5
  UPDATE_CHECK_INTERVAL_NORMAL = 10

  # `mode` parameter when copying payload files to the DUT.
  PAYLOAD_MODE_PARALLEL = 'parallel'
  PAYLOAD_MODE_SCP = 'scp'

  # Related to crbug.com/276094: Restore to 5 mins once the 'host did not
  # return from reboot' bug is solved.
  REBOOT_TIMEOUT = 480

  REMOTE_STATEFUL_PATH_TO_CHECK = ('/var', '/home', '/mnt/stateful_partition')
  REMOTE_STATEFUL_TEST_FILENAME = '.test_file_to_be_deleted'
  REMOTE_UPDATED_MARKERFILE_PATH = '/run/update_engine_autoupdate_completed'
  REMOTE_LAB_MACHINE_FILE_PATH = '/mnt/stateful_partition/.labmachine'
  KERNEL_A = {'name': 'KERN-A', 'kernel': 2, 'root': 3}
  KERNEL_B = {'name': 'KERN-B', 'kernel': 4, 'root': 5}
  KERNEL_UPDATE_TIMEOUT = 180

  def __init__(self, device, build_name, payload_dir, transfer_class,
               log_file=None, tempdir=None, clobber_stateful=False,
               yes=False, do_rootfs_update=True, do_stateful_update=True,
               reboot=True, disable_verification=False,
               send_payload_in_parallel=False, payload_filename=None,
               staging_server=None, clear_tpm_owner=False,
               resolve_app_id_mismatch=False, ignore_appid=False,
               copy_payloads_to_device=True):
    """Initialize a ChromiumOSUpdater for auto-update a chromium OS device.

    Args:
      device: the ChromiumOSDevice to be updated.
      build_name: the target update version for the device.
      payload_dir: the directory of payload(s).
      transfer_class: A reference to any subclass of
          auto_updater_transfer.Transfer class.
      log_file: The file to save running logs.
      tempdir: the temp directory in caller, not in the device. For example,
          the tempdir for cros flash is /tmp/cros-flash****/, used to
          temporarily keep files when transferring update-utils package, and
          reserve nebraska and update engine logs.
      do_rootfs_update: whether to do rootfs partition update. The default is
          True.
      do_stateful_update: whether to do stateful partition update. The default
          is True.
      reboot: whether to reboot device after update. The default is True.
      disable_verification: whether to disabling rootfs verification on the
          device. The default is False.
      clobber_stateful: whether to do a clean stateful update. The default is
          False.
      yes: Assume "yes" (True) for any prompt. The default is False. However,
          it should be set as True if we want to disable all the prompts for
          auto-update.
      payload_filename: Filename of exact payload file to use for update.
      send_payload_in_parallel: whether to transfer payload in chunks
          in parallel. The default is False.
      staging_server: URL (str) of the server that's staging the payload files.
          Assuming transfer_class is None, if value for staging_server is None
          or empty, an auto_updater_transfer.LocalTransfer reference must be
          passed through the transfer_class parameter.
      clear_tpm_owner: If true, it will clear the TPM owner on reboot. The
          default is False.
      resolve_app_id_mismatch: Fixes the update payloads App ID if it is
          different than the devices's App ID so the nebraska.py can properly
          create a response.
      ignore_appid: True to tell Nebraska to ignore the update request's
          App ID. This allows mismatching the source and target version boards.
          One specific use case is updating between <board> and
          <board>-kernelnext images which have different App IDs.
      copy_payloads_to_device: If True, update payloads are copied to the
          Chromium OS device first. Otherwise, they are piped through SSH.
          Currently, this only applies to the stateful payloads.
    """
    super(ChromiumOSUpdater, self).__init__(device, payload_dir)

    self.tempdir = (tempdir if tempdir is not None
                    else tempfile.mkdtemp(prefix='cros-update'))
    self.inactive_kernel = None
    self.update_version = build_name

    # Update setting
    self._cmd_kwargs = {}
    self._cmd_kwargs_omit_error = {'check': False}
    self._do_stateful_update = do_stateful_update
    self._do_rootfs_update = do_rootfs_update
    self._disable_verification = disable_verification
    self._clobber_stateful = clobber_stateful
    self._reboot = reboot
    self._yes = yes
    # Device's directories
    self.device_dev_dir = os.path.join(self.device.work_dir, 'src')
    self.device_payload_dir = os.path.join(
        self.device.work_dir,
        auto_updater_transfer.Transfer.PAYLOAD_DIR_NAME)
    self.payload_filename = payload_filename
    if send_payload_in_parallel:
      self.payload_mode = self.PAYLOAD_MODE_PARALLEL
    else:
      self.payload_mode = self.PAYLOAD_MODE_SCP
    self.perf_id = None

    if log_file:
      log_kwargs = {
          'stdout': log_file,
          'append_to_file': True,
          'stderr': subprocess.STDOUT,
      }
      self._cmd_kwargs.update(log_kwargs)
      self._cmd_kwargs_omit_error.update(log_kwargs)

    self._staging_server = staging_server
    self._transfer_obj = self._CreateTransferObject(transfer_class)

    self._clear_tpm_owner = clear_tpm_owner
    self._resolve_app_id_mismatch = resolve_app_id_mismatch
    self._ignore_appid = ignore_appid
    self._copy_payloads_to_device = copy_payloads_to_device

  @property
  def is_au_endtoendtest(self):
    return isinstance(self._transfer_obj,
                      auto_updater_transfer.LabEndToEndPayloadTransfer)

  @property
  def request_logs_dir(self):
    """Returns path to the nebraska request logfiles directory.

    Returns:
      A complete path to the logfiles directory.
    """
    return self.tempdir

  def _CreateTransferObject(self, transfer_class):
    """Create the correct Transfer class.

    Args:
      transfer_class: A variable that contains a reference to one of the
          Transfer classes in auto_updater_transfer.
    """
    assert issubclass(transfer_class, auto_updater_transfer.Transfer)

    # Determine if staging_server needs to be passed as an argument to
    # class_ref.
    cls_kwargs = {}
    if self._staging_server:
      cls_kwargs['staging_server'] = self._staging_server

    return transfer_class(
        device=self.device, payload_dir=self.payload_dir,
        payload_name=self.payload_filename,
        cmd_kwargs=self._cmd_kwargs,
        transfer_rootfs_update=self._do_rootfs_update,
        transfer_stateful_update=self._do_rootfs_update,
        device_payload_dir=self.device_payload_dir, tempdir=self.tempdir,
        payload_mode=self.payload_mode, **cls_kwargs)

  def CheckRestoreStateful(self):
    """Check whether to restore stateful."""
    logging.debug('Checking whether to restore stateful...')
    restore_stateful = False
    try:
      self._CheckNebraskaCanRun()
      return restore_stateful
    except nebraska_wrapper.NebraskaStartupError as e:
      if self._do_rootfs_update:
        msg = ('Cannot start nebraska! The stateful partition may be '
               'corrupted: %s' % e)
        prompt = 'Attempt to restore the stateful partition?'
        restore_stateful = self._yes or cros_build_lib.BooleanPrompt(
            prompt=prompt, default=False, prolog=msg)
        if not restore_stateful:
          raise ChromiumOSUpdateError(
              'Cannot continue to perform rootfs update!')

    logging.debug('Restore stateful partition is%s required.',
                  ('' if restore_stateful else ' not'))
    return restore_stateful

  def _CheckNebraskaCanRun(self):
    """We can run Nebraska on |device|."""
    nebraska_bin = os.path.join(self.device_dev_dir,
                                self.REMOTE_NEBRASKA_FILENAME)
    nebraska = nebraska_wrapper.RemoteNebraskaWrapper(
        self.device, nebraska_bin=nebraska_bin)
    nebraska.CheckNebraskaCanRun()

  @classmethod
  def GetUpdateStatus(cls, device, keys=None):
    """Returns the status of the update engine on the |device|.

    Retrieves the status from update engine and confirms all keys are
    in the status.

    Args:
      device: A ChromiumOSDevice object.
      keys: the keys to look for in the status result (defaults to
          ['CURRENT_OP']).

    Returns:
      A list of values in the order of |keys|.
    """
    keys = keys or ['CURRENT_OP']
    result = device.run([cls.REMOTE_UPDATE_ENGINE_BIN_FILENAME, '--status'],
                        capture_output=True, log_output=True)

    if not result.output:
      raise Exception('Cannot get update status')

    try:
      status = key_value_store.LoadData(result.output)
    except ValueError:
      raise ValueError('Cannot parse update status')

    values = []
    for key in keys:
      if key not in status:
        raise ValueError('Missing "%s" in the update engine status' % key)

      values.append(status.get(key))

    return values

  def GetRootDev(self):
    """Get the current root device on |device|."""
    root_dev = self.device.root_dev
    logging.debug('Current root device is %s', root_dev)
    return root_dev

  def _StartUpdateEngineIfNotRunning(self, device):
    """Starts update-engine service if it is not running.

    Args:
      device: a ChromiumOSDevice object, defines the target root device.
    """
    try:
      result = device.run(['start', 'update-engine'],
                          capture_output=True, log_output=True).stdout
      if 'start/running' in result:
        logging.info('update engine was not running, so we started it.')
    except cros_build_lib.RunCommandError as e:
      if e.result.returncode != 1 or 'is already running' not in e.result.error:
        raise e

  def SetupRootfsUpdate(self):
    """Makes sure |device| is ready for rootfs update."""
    logging.info('Checking if update engine is idle...')
    self._StartUpdateEngineIfNotRunning(self.device)
    status = self.GetUpdateStatus(self.device)[0]
    if status == UPDATE_STATUS_UPDATED_NEED_REBOOT:
      logging.info('Device needs to reboot before updating...')
      self._Reboot('setup of Rootfs Update')
      status = self.GetUpdateStatus(self.device)[0]

    if status != UPDATE_STATUS_IDLE:
      raise RootfsUpdateError('Update engine is not idle. Status: %s' % status)

    if self.is_au_endtoendtest:
      # TODO(ahassani): This should only be done for jetsteam devices.
      self._RetryCommand(['sudo', 'stop', 'ap-update-manager'],
                         **self._cmd_kwargs_omit_error)

      self._RetryCommand(['rm', '-f', self.REMOTE_UPDATED_MARKERFILE_PATH],
                         **self._cmd_kwargs)
      self._RetryCommand(['stop', 'ui'], **self._cmd_kwargs_omit_error)


  def _GetDevicePythonSysPath(self):
    """Get python sys.path of the given |device|."""
    sys_path = self.device.run(
        ['python', '-c', '"import json, sys; json.dump(sys.path, sys.stdout)"'],
        capture_output=True, log_output=True).output
    return json.loads(sys_path)

  def _FindDevicePythonPackagesDir(self):
    """Find the python packages directory for the given |device|."""
    third_party_host_dir = ''
    sys_path = self._GetDevicePythonSysPath()
    for p in sys_path:
      if p.endswith('site-packages') or p.endswith('dist-packages'):
        third_party_host_dir = p
        break

    if not third_party_host_dir:
      raise ChromiumOSUpdateError(
          'Cannot find proper site-packages/dist-packages directory from '
          'sys.path for storing packages: %s' % sys_path)

    return third_party_host_dir

  def ResetStatefulPartition(self):
    """Clear any pending stateful update request."""
    logging.debug('Resetting stateful partition...')
    try:
      stateful_updater.StatefulUpdater(self.device).Reset()
    except stateful_updater.Error as e:
      raise StatefulUpdateError(e)

  def RevertBootPartition(self):
    """Revert the boot partition."""
    part = self.GetRootDev()
    logging.warning('Reverting update; Boot partition will be %s', part)
    try:
      self.device.run(['/postinst', part], **self._cmd_kwargs)
    except cros_build_lib.RunCommandError as e:
      logging.warning('Reverting the boot partition failed: %s', e)

  def UpdateRootfs(self):
    """Update the rootfs partition of the device (utilizing nebraska)."""
    logging.notice('Updating rootfs partition...')
    nebraska_bin = os.path.join(self.device_dev_dir,
                                self.REMOTE_NEBRASKA_FILENAME)

    nebraska = nebraska_wrapper.RemoteNebraskaWrapper(
        self.device, nebraska_bin=nebraska_bin,
        update_payloads_address='file://' + self.device_payload_dir,
        update_metadata_dir=self.device_payload_dir,
        ignore_appid=self._ignore_appid)

    try:
      nebraska.Start()

      # Use the localhost IP address (default) to ensure that update engine
      # client can connect to the nebraska.
      nebraska_url = nebraska.GetURL(critical_update=True)
      cmd = [self.REMOTE_UPDATE_ENGINE_BIN_FILENAME, '--check_for_update',
             '--omaha_url="%s"' % nebraska_url]

      self.device.run(cmd, **self._cmd_kwargs)

      # If we are using a progress bar, update it every 0.5s instead of 10s.
      if command.UseProgressBar():
        update_check_interval = self.UPDATE_CHECK_INTERVAL_PROGRESSBAR
        oper = operation.ProgressBarOperation()
      else:
        update_check_interval = self.UPDATE_CHECK_INTERVAL_NORMAL
        oper = None
      end_message_not_printed = True

      # Loop until update is complete.
      while True:
        # Number of times to retry `update_engine_client --status`. See
        # crbug.com/744212.
        update_engine_status_retry = 30
        op, progress = retry_util.RetryException(
            cros_build_lib.RunCommandError,
            update_engine_status_retry,
            self.GetUpdateStatus,
            self.device,
            ['CURRENT_OP', 'PROGRESS'],
            delay_sec=DELAY_SEC_FOR_RETRY)[0:2]
        logging.info('Waiting for update...status: %s at progress %s',
                     op, progress)

        if op == UPDATE_STATUS_UPDATED_NEED_REBOOT:
          logging.info('Update completed.')
          break

        if op == UPDATE_STATUS_IDLE:
          # Something went wrong. Try to get last error code.
          cmd = ['cat', self.REMOTE_UPDATE_ENGINE_LOGFILE_PATH]
          log = self.device.run(cmd).stdout.strip().splitlines()
          err_str = 'Updating payload state for error code: '
          targets = [line for line in log if err_str in line]
          logging.debug('Error lines found: %s', targets)
          if not targets:
            raise RootfsUpdateError(
                'Update failed with unexpected update status: %s' % op)
          else:
            # e.g 20 (ErrorCode::kDownloadStateInitializationError)
            raise RootfsUpdateError(targets[-1].rpartition(err_str)[2])

        if oper is not None:
          if op == UPDATE_STATUS_DOWNLOADING:
            oper.ProgressBar(float(progress))
          elif end_message_not_printed and op == UPDATE_STATUS_FINALIZING:
            oper.Cleanup()
            logging.info('Finalizing image.')
            end_message_not_printed = False

        time.sleep(update_check_interval)
    # TODO(ahassani): Scope the Exception to finer levels. For example we don't
    # need to revert the boot partition if the Nebraska fails to start, etc.
    except Exception as e:
      logging.error('Rootfs update failed %s', e)
      self.RevertBootPartition()
      logging.warning(nebraska.PrintLog() or 'No nebraska log is available.')
      raise RootfsUpdateError('Failed to perform rootfs update: %r' % e)
    finally:
      nebraska.Stop()

      nebraska.CollectLogs(os.path.join(self.tempdir,
                                        self.LOCAL_NEBRASKA_LOG_FILENAME))
      self.device.CopyFromDevice(
          self.REMOTE_UPDATE_ENGINE_LOGFILE_PATH,
          os.path.join(self.tempdir, os.path.basename(
              self.REMOTE_UPDATE_ENGINE_LOGFILE_PATH)),
          follow_symlinks=True, **self._cmd_kwargs_omit_error)

  def UpdateStateful(self):
    """Update the stateful partition of the device."""
    try:
      if self._copy_payloads_to_device:
        self._transfer_obj.TransferStatefulUpdate()
        stateful_update_payload = os.path.join(
            self.device.work_dir, auto_updater_transfer.STATEFUL_FILENAME)
      else:
        stateful_update_payload = os.path.join(
            self.payload_dir, auto_updater_transfer.STATEFUL_FILENAME)

      updater = stateful_updater.StatefulUpdater(self.device)
      updater.Update(
          stateful_update_payload,
          is_payload_on_device=self._copy_payloads_to_device,
          update_type=(stateful_updater.StatefulUpdater.UPDATE_TYPE_CLOBBER if
                       self._clobber_stateful else None))

      if self._copy_payloads_to_device:
        # Delete the stateful update file on success so it doesn't occupy extra
        # disk space. On failure it will get cleaned up.
        self.device.DeletePath(stateful_update_payload)
    except stateful_updater.Error as e:
      error_msg = 'Stateful update failed with error: %s' % str(e)
      logging.exception(error_msg)
      self.ResetStatefulPartition()
      raise StatefulUpdateError(error_msg)

  def RunUpdateRootfs(self):
    """Run all processes needed by updating rootfs.

    1. Check device's status to make sure it can be updated.
    2. Copy files to remote device needed for rootfs update.
    3. Do root updating.
    """

    # SetupRootfsUpdate() may reboot the device and therefore should be called
    # before any payloads are transferred to the device and only if rootfs
    # update is required.
    self.SetupRootfsUpdate()

    if self._resolve_app_id_mismatch:
      self._ResolveAPPIDMismatchIfAny()

    # Copy payload for rootfs update.
    self._transfer_obj.TransferRootfsUpdate()

    self.UpdateRootfs()

    if self.is_au_endtoendtest:
      self.PostCheckRootfsUpdate()

    # Delete the update file so it doesn't take much space on disk for the
    # remainder of the update process.
    self.device.DeletePath(self.device_payload_dir, recursive=True)

  def RebootAndVerify(self):
    """Reboot and verify the remote device.

    1. Reboot the remote device. If _clobber_stateful (--clobber-stateful)
    is executed, the stateful partition is wiped, and the working directory
    on the remote device no longer exists. So, recreate the working directory
    for this remote device.
    2. Verify the remote device, by checking that whether the root device
    changed after reboot.
    """
    logging.notice('Rebooting device...')
    # Record the current root device. This must be done after SetupRootfsUpdate
    # and before reboot, since SetupRootfsUpdate may reboot the device if there
    # is a pending update, which changes the root device, and reboot will
    # definitely change the root device if update successfully finishes.
    old_root_dev = self.GetRootDev()
    self.device.Reboot()
    if self._clobber_stateful:
      self.device.run(['mkdir', '-p', self.device.work_dir])

    if self._do_rootfs_update:
      logging.notice('Verifying that the device has been updated...')
      new_root_dev = self.GetRootDev()
      if old_root_dev is None:
        raise AutoUpdateVerifyError(
            'Failed to locate root device before update.')

      if new_root_dev is None:
        raise AutoUpdateVerifyError(
            'Failed to locate root device after update.')

      if new_root_dev == old_root_dev:
        raise AutoUpdateVerifyError(
            'Failed to boot into the new version. Possibly there was a '
            'signing problem, or an automated rollback occurred because '
            'your new image failed to boot.')

  def _ResolveAPPIDMismatchIfAny(self):
    """Resolves and APP ID mismatch between the payload and device.

    If the APP ID of the payload is different than the device, then the nebraska
    will fail. We empty the payload's App ID so nebraska can do partial APP ID
    matching.
    """
    if not self.device.app_id:
      logging.warning('Device does not have a propper APP ID!')
      return

    prop_file = os.path.join(self.payload_dir, self.payload_filename + '.json')
    with open(prop_file) as fp:
      content = json.load(fp)
      payload_app_id = content.get('appid', '')
      if not payload_app_id:
        # Payload's App ID is empty, we don't care, it is already partial match.
        return

    if self.device.app_id != payload_app_id:
      logging.warning('You are installing an image with a different release '
                      'App ID than the device (%s vs %s), we are forcing the '
                      'install!', payload_app_id, self.device.app_id)
      # Override the properties file with the new empty APP ID.
      content['appid'] = ''
      with open(prop_file, 'w') as fp:
        json.dump(content, fp)

  def RunUpdate(self):
    """Update the device with image of specific version."""
    self._transfer_obj.CheckPayloads()

    restore_stateful = False
    if self._do_rootfs_update:
      self._transfer_obj.TransferUpdateUtilsPackage()

      restore_stateful = self.CheckRestoreStateful()
      if restore_stateful:
        self.RestoreStateful()

      # Perform device updates.
      self.RunUpdateRootfs()
      logging.info('Rootfs update completed.')

    if self._do_stateful_update and not restore_stateful:
      self.UpdateStateful()
      logging.info('Stateful update completed.')

    if self._clear_tpm_owner:
      self.device.ClearTpmOwner()

    if self._reboot:
      self.RebootAndVerify()

    if self.is_au_endtoendtest:
      self.PostCheckCrOSUpdate()

    if self._disable_verification:
      logging.info('Disabling rootfs verification on the device...')
      self.device.DisableRootfsVerification()

  def _Reboot(self, error_stage, timeout=None):
    try:
      if timeout is None:
        timeout = self.REBOOT_TIMEOUT
      self.device.Reboot(timeout_sec=timeout)
    except remote_access.RebootError:
      raise ChromiumOSUpdateError('Could not recover from reboot at %s' %
                                  error_stage)
    except remote_access.SSHConnectionError:
      raise ChromiumOSUpdateError('Failed to connect at %s' % error_stage)

  def _cgpt(self, flag, kernel, dev='$(rootdev -s -d)'):
    """Return numeric cgpt value for the specified flag, kernel, device."""
    cmd = ['cgpt', 'show', '-n', '-i', '%d' % kernel['kernel'], flag, dev]
    return int(self._RetryCommand(
        cmd, capture_output=True, log_output=True).output.strip())

  def _GetKernelPriority(self, kernel):
    """Return numeric priority for the specified kernel.

    Args:
      kernel: information of the given kernel, KERNEL_A or KERNEL_B.
    """
    return self._cgpt('-P', kernel)

  def _GetKernelSuccess(self, kernel):
    """Return boolean success flag for the specified kernel.

    Args:
      kernel: information of the given kernel, KERNEL_A or KERNEL_B.
    """
    return self._cgpt('-S', kernel) != 0

  def _GetKernelTries(self, kernel):
    """Return tries count for the specified kernel.

    Args:
      kernel: information of the given kernel, KERNEL_A or KERNEL_B.
    """
    return self._cgpt('-T', kernel)

  def _GetKernelState(self):
    """Returns the (<active>, <inactive>) kernel state as a pair."""
    active_root = int(re.findall(r'(\d+\Z)', self.GetRootDev())[0])
    if active_root == self.KERNEL_A['root']:
      return self.KERNEL_A, self.KERNEL_B
    elif active_root == self.KERNEL_B['root']:
      return self.KERNEL_B, self.KERNEL_A
    else:
      raise ChromiumOSUpdateError('Encountered unknown root partition: %s' %
                                  active_root)

  def _GetReleaseVersion(self):
    """Get release version of the device."""
    lsb_release_content = self._RetryCommand(
        ['cat', '/etc/lsb-release'],
        capture_output=True, log_output=True).output.strip()
    regex = r'^CHROMEOS_RELEASE_VERSION=(.+)$'
    return auto_update_util.GetChromeosBuildInfo(
        lsb_release_content=lsb_release_content, regex=regex)

  def _GetReleaseBuilderPath(self):
    """Get release version of the device."""
    lsb_release_content = self._RetryCommand(
        ['cat', '/etc/lsb-release'],
        capture_output=True, log_output=True).output.strip()
    regex = r'^CHROMEOS_RELEASE_BUILDER_PATH=(.+)$'
    return auto_update_util.GetChromeosBuildInfo(
        lsb_release_content=lsb_release_content, regex=regex)

  def CheckVersion(self):
    """Check the image running in DUT has the expected version.

    Returns:
      True if the DUT's image version matches the version that the
      ChromiumOSUpdater tries to update to.
    """
    if not self.update_version:
      return False

    # Use CHROMEOS_RELEASE_BUILDER_PATH to match the build version if it exists
    # in lsb-release, otherwise, continue using CHROMEOS_RELEASE_VERSION.
    release_builder_path = self._GetReleaseBuilderPath()
    if release_builder_path:
      return self.update_version == release_builder_path

    return self.update_version.endswith(self._GetReleaseVersion())

  def _VerifyBootExpectations(self, expected_kernel_state, rollback_message):
    """Verify that we fully booted given expected kernel state.

    It verifies that we booted using the correct kernel state, and that the
    OS has marked the kernel as good.

    Args:
      expected_kernel_state: kernel state that we're verifying with i.e. I
        expect to be booted onto partition 4 etc. See output of _GetKernelState.
      rollback_message: string to raise as a RootfsUpdateError if we booted
        with the wrong partition.
    """
    logging.debug('Start verifying boot expectations...')
    # Figure out the newly active kernel
    active_kernel_state = self._GetKernelState()[0]

    # Rollback
    if (expected_kernel_state and
        active_kernel_state != expected_kernel_state):
      logging.debug('Dumping partition table.')
      self.device.run(['cgpt', 'show', '$(rootdev -s -d)'],
                      **self._cmd_kwargs)
      logging.debug('Dumping crossystem for firmware debugging.')
      self.device.run(['crossystem', '--all'], **self._cmd_kwargs)
      raise RootfsUpdateError(rollback_message)

    # Make sure chromeos-setgoodkernel runs
    try:
      timeout_util.WaitForReturnTrue(
          lambda: (self._GetKernelTries(active_kernel_state) == 0
                   and self._GetKernelSuccess(active_kernel_state)),
          self.KERNEL_UPDATE_TIMEOUT,
          period=5)
    except timeout_util.TimeoutError:
      services_status = self.device.run(
          ['status', 'system-services'], capture_output=True,
          log_output=True).output
      logging.debug('System services_status: %r', services_status)
      if services_status != 'system-services start/running\n':
        event = ('Chrome failed to reach login screen')
      else:
        event = ('update-engine failed to call '
                 'chromeos-setgoodkernel')
      raise RootfsUpdateError(
          'After update and reboot, %s '
          'within %d seconds' % (event, self.KERNEL_UPDATE_TIMEOUT))

  def _CheckVersionToConfirmInstall(self):
    logging.debug('Checking whether the new build is successfully installed...')
    if not self.update_version:
      logging.debug('No update_version is provided if test is executed with'
                    'local nebraska.')
      return True

    # Always try the default check_version method first, this prevents
    # any backward compatibility issue.
    if self.CheckVersion():
      return True

    return auto_update_util.VersionMatch(
        self.update_version, self._GetReleaseVersion())

  def _RetryCommand(self, cmd, **kwargs):
    """Retry commands if SSHConnectionError happens.

    Args:
      cmd: the command to be run by device.
      kwargs: the parameters for device to run the command.

    Returns:
      the output of running the command.
    """
    return retry_util.RetryException(
        remote_access.SSHConnectionError,
        MAX_RETRY,
        self.device.run,
        cmd, delay_sec=DELAY_SEC_FOR_RETRY,
        shell=isinstance(cmd, str),
        **kwargs)

  def PreSetupStatefulUpdate(self):
    """Pre-setup for stateful update for CrOS host."""
    logging.debug('Start pre-setup for stateful update...')
    if self._clobber_stateful:
      for folder in self.REMOTE_STATEFUL_PATH_TO_CHECK:
        touch_path = os.path.join(folder, self.REMOTE_STATEFUL_TEST_FILENAME)
        self._RetryCommand(['touch', touch_path], **self._cmd_kwargs)

  def PostCheckStatefulUpdate(self):
    """Post-check for stateful update for CrOS host."""
    logging.debug('Start post check for stateful update...')
    self._Reboot('post check of stateful update')
    if self._clobber_stateful:
      for folder in self.REMOTE_STATEFUL_PATH_TO_CHECK:
        test_file_path = os.path.join(folder,
                                      self.REMOTE_STATEFUL_TEST_FILENAME)
        # If stateful update succeeds, these test files should not exist.
        if self.device.IfFileExists(test_file_path,
                                    **self._cmd_kwargs_omit_error):
          raise StatefulUpdateError('failed to post-check stateful update.')

  def _IsUpdateUtilsPackageInstalled(self):
    """Check whether update-utils package is well installed.

    There's a chance that nebraska package is removed in the middle of
    auto-update process. This function double check it and transfer it if it's
    removed.
    """
    logging.info('Checking whether nebraska files are still on the device...')
    try:
      nebraska_bin = os.path.join(self.device_dev_dir,
                                  self.REMOTE_NEBRASKA_FILENAME)
      if not self.device.IfFileExists(
          nebraska_bin, **self._cmd_kwargs_omit_error):
        logging.info('Nebraska files not found on device. Resending them...')

        self._transfer_obj.TransferUpdateUtilsPackage()

      return True
    except cros_build_lib.RunCommandError as e:
      logging.warning('Failed to verify whether packages still exist: %s', e)
      return False

  def CheckNebraskaCanRun(self):
    """Check if nebraska can successfully run for ChromiumOSUpdater."""
    self._IsUpdateUtilsPackageInstalled()
    self._CheckNebraskaCanRun()

  def RestoreStateful(self):
    """Restore stateful partition for device."""
    logging.warning('Restoring the stateful partition.')
    self.PreSetupStatefulUpdate()
    self.ResetStatefulPartition()
    self.UpdateStateful()
    self.PostCheckStatefulUpdate()
    try:
      self.CheckNebraskaCanRun()
      logging.info('Stateful partition restored.')
    except nebraska_wrapper.NebraskaStartupError as e:
      raise ChromiumOSUpdateError(
          'Unable to restore stateful partition: %s' % e)

  def PostCheckRootfsUpdate(self):
    """Post-check for rootfs update for CrOS host."""
    logging.debug('Start post check for rootfs update...')
    active_kernel, inactive_kernel = self._GetKernelState()
    logging.debug('active_kernel= %s, inactive_kernel=%s',
                  active_kernel, inactive_kernel)
    if (self._GetKernelPriority(inactive_kernel) <
        self._GetKernelPriority(active_kernel)):
      raise RootfsUpdateError('Update failed. The priority of the inactive '
                              'kernel partition is less than that of the '
                              'active kernel partition.')
    self.inactive_kernel = inactive_kernel

  def PostCheckCrOSUpdate(self):
    """Post check for the whole auto-update process."""
    logging.debug('Post check for the whole CrOS update...')
    start_time = time.time()
    # Not use 'sh' here since current device.run cannot recognize
    # the content of $FILE.
    autoreboot_cmd = ('FILE="%s" ; [ -f "$FILE" ] || '
                      '( touch "$FILE" ; start autoreboot )')
    self._RetryCommand(autoreboot_cmd % self.REMOTE_LAB_MACHINE_FILE_PATH,
                       **self._cmd_kwargs)

    # Loop in case the initial check happens before the reboot.
    while True:
      try:
        start_verify_time = time.time()
        self._VerifyBootExpectations(
            self.inactive_kernel, rollback_message=
            'Build %s failed to boot on %s; system rolled back to previous '
            'build' % (self.update_version, self.device.hostname))

        # Check that we've got the build we meant to install.
        if not self._CheckVersionToConfirmInstall():
          raise ChromiumOSUpdateError(
              'Failed to update %s to build %s; found build '
              '%s instead' % (self.device.hostname,
                              self.update_version,
                              self._GetReleaseVersion()))
      except RebootVerificationError as e:
        # If a minimum amount of time since starting the check has not
        # occurred, wait and retry.  Use the start of the verification
        # time in case an SSH call takes a long time to return/fail.
        if start_verify_time - start_time < POST_CHECK_SETTLE_SECONDS:
          logging.warning('Delaying for re-check of %s to update to %s (%s)',
                          self.device.hostname, self.update_version, e)
          time.sleep(POST_CHECK_RETRY_SECONDS)
          continue
        raise
      break

    if not self._clobber_stateful:
      self.PostRebootUpdateCheckForAUTest()

  def PostRebootUpdateCheckForAUTest(self):
    """Do another update check after reboot to get the post update hostlog.

    This is only done with autoupdate_EndToEndTest.
    """
    logging.debug('Doing one final update check to get post update hostlog.')
    nebraska_bin = os.path.join(self.device_dev_dir,
                                self.REMOTE_NEBRASKA_FILENAME)
    nebraska = nebraska_wrapper.RemoteNebraskaWrapper(
        self.device, nebraska_bin=nebraska_bin,
        update_metadata_dir=self.device.work_dir)

    try:
      nebraska.Start()

      nebraska_url = nebraska.GetURL(critical_update=True, no_update=True)
      cmd = [self.REMOTE_UPDATE_ENGINE_BIN_FILENAME, '--check_for_update',
             '--omaha_url="%s"' % nebraska_url]
      self.device.run(cmd, **self._cmd_kwargs)
      op = self.GetUpdateStatus(self.device)[0]
      logging.info('Post update check status: %s', op)
    except Exception as err:
      logging.error('Post reboot update check failed: %s', str(err))
      logging.warning(nebraska.PrintLog() or 'No nebraska log is available.')
    finally:
      nebraska.Stop()
