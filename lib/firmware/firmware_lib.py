# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Utilities to do build, flash, read, and other operations with AP Firmware.
"""

import logging
import os
import shutil
import tempfile
from typing import Iterable, Optional

from chromite.lib import build_target_lib
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import workon_helper
from chromite.lib.firmware import firmware_config
from chromite.lib.firmware import dut
from chromite.service import sysroot


class Error(Exception):
  """Base module error class."""


class DeployFailed(Error):
  """Error raised when deploy fails."""


class BuildError(Error):
  """Failure in the build command."""


class CleanError(Error):
  """Failure in the clean command."""


def deploy(build_target,
           image,
           device=None,
           flashrom=False,
           port=None,
           verbose=False,
           dryrun=False,
           flash_contents: Optional[str] = None,
           passthrough_args: Iterable[str] = tuple()):
  """Deploy an AP FW image to a device.

  Args:
    build_target (build_target_lib.BuildTarget): The DUT build target.
    image (str): The image path.
    device (commandline.Device): The device to be used. Temporarily optional.
    flashrom (bool): Whether to use flashrom or futility.
    port (int|None): The servo port.
    verbose (bool): Whether to use verbose output for flash commands.
    dryrun (bool): Whether to actually execute the deployment or just print the
      operations that would have been performed.
    flash_contents: Path to the file that contains the existing contents.
    passthrough_args: List of additional options passed to flashrom or futility.
  """
  ip = None
  if device:
    port = device.port
    if device.scheme == commandline.DEVICE_SCHEME_SSH:
      ip = device.hostname
      port = port or device.port
  else:
    ip = os.getenv('IP')

  if ip:
    _deploy_ssh(build_target, image, flashrom, verbose, ip, port, dryrun,
                passthrough_args)
  else:
    _deploy_servo(build_target, image, flashrom, verbose, port, dryrun,
                  flash_contents, passthrough_args)


def _deploy_servo(build_target,
                  image,
                  flashrom,
                  verbose,
                  port,
                  dryrun,
                  flash_contents: Optional[str] = None,
                  passthrough_args: Iterable[str] = tuple()):
  """Deploy to a servo connection.

  Args:
    build_target (build_target_lib.BuildTarget): The DUT build target.
    image (str): Path to the image to flash.
    flashrom (bool): Whether to use flashrom or futility.
    verbose (bool): Whether to use verbose output for flash commands.
    port (int|None): The servo port.
    dryrun (bool): Whether to actually execute the deployment or just print the
      operations that would have been performed.
    flash_contents: Path to the file that contains the existing contents.
    passthrough_args: Additional options passed to flashrom or futility.
  """
  dut_ctl = dut.DutControl(port)
  servo = dut_ctl.get_servo()
  fw_config = firmware_config.get_config(build_target.name, servo)

  use_flashrom = flashrom or fw_config.force_flashrom
  logging.notice('Attempting to flash via servo using %s.',
                 'flashrom' if use_flashrom else 'futility')

  flashrom_cmd = ['flashrom', '-p', fw_config.programmer, '-w', image]
  futility_cmd = [
      'futility',
      'update',
      '-p',
      fw_config.programmer,
      '-i',
      image,
  ]
  futility_cmd += ['--force', '--wp=0']
  if verbose:
    flashrom_cmd += ['-V']
    futility_cmd += ['-v']
  if flash_contents is not None:
    flashrom_cmd += ['--flash-contents', flash_contents]
  if passthrough_args:
    flashrom_cmd += passthrough_args
    futility_cmd += passthrough_args

  if use_flashrom and fw_config.flash_extra_flags_flashrom:
    if passthrough_args:
      logging.warning(
          'Extra flashing arguments provided in CLI (%s) '
          'override arguments provided by config file (%s)', passthrough_args,
          fw_config.flash_extra_flags_flashrom)
    else:
      flashrom_cmd += fw_config.flash_extra_flags_flashrom

  if not use_flashrom and fw_config.flash_extra_flags_futility:
    if passthrough_args:
      logging.warning(
          'Extra flashing arguments provided in CLI (%s) '
          'override arguments provided by config file (%s)', passthrough_args,
          fw_config.flash_extra_flags_futility)
    else:
      futility_cmd += fw_config.flash_extra_flags_futility

  flash_cmd = flashrom_cmd if use_flashrom else futility_cmd
  if dut_ctl.servo_run(fw_config.dut_control_on, fw_config.dut_control_off,
                       flash_cmd, verbose, dryrun):
    logging.notice('SUCCESS. Exiting flash_ap.')
  else:
    logging.error('Unable to complete flash, verify servo connection '
                  'is correct and servod is running in the background.')


def _deploy_ssh(build_target,
                image,
                flashrom,
                verbose,
                ip,
                port,
                dryrun,
                passthrough_args: Iterable[str] = tuple()):
  """Deploy to a servo connection.

  Args:
    build_target (build_target_lib.BuildTarget): The DUT build target.
    image (str): Path to the image to flash.
    flashrom (bool): Whether to use flashrom or futility.
    verbose (bool): Whether to use verbose output for flash commands.
    ip (str): The DUT ip address.
    port (int): The port to ssh to.
    dryrun (bool): Whether to execute the deployment or just print the
      commands that would have been executed.
    passthrough_args: List of additional options passed to flashrom or futility.
  """

  fw_config = firmware_config.get_config(build_target.name, None)

  use_flashrom = flashrom or fw_config.force_flashrom
  logging.notice('Attempting to flash via ssh using %s.',
                 'flashrom' if use_flashrom else 'futility')

  logging.info('connecting to: %s\n', ip)
  id_filename = '/mnt/host/source/chromite/ssh_keys/testing_rsa'
  tmpfile = tempfile.NamedTemporaryFile()
  shutil.copyfile(id_filename, tmpfile.name)

  if use_flashrom and fw_config.flash_extra_flags_flashrom:
    if passthrough_args:
      logging.warning(
          'Extra flashing arguments provided in CLI (%s) '
          'override arguments provided by config file (%s)', passthrough_args,
          fw_config.flash_extra_flags_flashrom)
    else:
      passthrough_args = fw_config.flash_extra_flags_flashrom

  if not use_flashrom and fw_config.flash_extra_flags_futility:
    if passthrough_args:
      logging.warning(
          'Extra flashing arguments provided in CLI (%s) '
          'override arguments provided by config file (%s)', passthrough_args,
          fw_config.flash_extra_flags_futility)
    else:
      passthrough_args = fw_config.flash_extra_flags_futility

  scp_cmd, flash_cmd = _build_flash_ssh_cmds(not flashrom, ip, port, image,
                                             tmpfile.name, verbose,
                                             passthrough_args)
  try:
    cros_build_lib.run(scp_cmd, print_cmd=verbose, check=True, dryrun=dryrun)
  except cros_build_lib.CalledProcessError as e:
    logging.error('Could not copy image to dut.')
    raise e

  logging.info('Flashing now, may take several minutes.')
  try:
    cros_build_lib.run(flash_cmd, print_cmd=verbose, check=True, dryrun=dryrun)
  except cros_build_lib.CalledProcessError as e:
    logging.error('Flashing over SSH failed. Try using a servo instead.')
    raise e

  logging.notice('ssh flash successful. Exiting flash_ap')


def _build_flash_ssh_cmds(futility,
                          ip,
                          port,
                          path,
                          tmp_file_name,
                          verbose,
                          passthrough_args: Iterable[str] = tuple()):
  """Helper function to build commands for flashing over ssh

  Args:
    futility (bool): if True then flash with futility, otherwise flash
      with flashrom.
    ip (string): ip address of dut to flash.
    port (int): The port to ssh to.
    path (string): path to BIOS image to be flashed.
    tmp_file_name (string): name of tempfile with copy of testing_rsa
      keys.
    verbose (bool): if True set -v flag in flash command.
    passthrough_args: List of additional options passed to flashrom or futility.

  Returns:
    scp_cmd ([string]):
    flash_cmd ([string]):
  """
  ssh_parameters = [
      '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no',
      '-o', 'CheckHostIP=no'
  ]
  ssh_port = ['-p', str(port)] if port else []
  scp_port = ['-P', str(port)] if port else []
  tmp = '/tmp'
  hostname = 'root@%s' % ip
  scp_cmd = (['scp', '-i', tmp_file_name] + scp_port + ssh_parameters +
             [path, '%s:%s' % (hostname, tmp)])
  flash_cmd = ['ssh', hostname, '-i', tmp_file_name] + ssh_port + ssh_parameters
  if futility:
    flash_cmd += [
        'futility', 'update', '-p', 'host', '-i',
        os.path.join(tmp, os.path.basename(path))
    ]
    if verbose:
      flash_cmd += ['-v']
  else:
    flash_cmd += [
        'flashrom', '-p', 'host', '-w',
        os.path.join(tmp, os.path.basename(path))
    ]
    if verbose:
      flash_cmd += ['-V']
  if passthrough_args:
    flash_cmd.extend(passthrough_args)
  flash_cmd += ['&& reboot']
  return scp_cmd, flash_cmd


def build(build_target, fw_name=None, dry_run=False):
  """Build the AP Firmware.

  Args:
    build_target (BuildTarget): The build target (board) being built.
    fw_name (str|None): Optionally set the FW_NAME envvar to allow building
      the firmware for only a specific variant.
    dry_run (bool): Whether to perform a dry run.
  """
  logging.notice('Building AP Firmware.')

  if not os.path.exists(build_target.root):
    logging.warning(
        'Sysroot for target %s is not available. Attempting '
        'to configure sysroot via default setup_board command.',
        build_target.name)
    try:
      sysroot.SetupBoard(build_target)
    except (portage_util.MissingOverlayError, sysroot.Error):
      cros_build_lib.Die('setup_board with default specifications failed. '
                         "Please configure the board's sysroot separately.")

  config = firmware_config.get_config(build_target.name, None)

  with workon_helper.WorkonScope(build_target, config.workon_packages):
    extra_env = {'FW_NAME': fw_name} if fw_name else None
    # Run the emerge command to build the packages. Don't raise an exception
    # here if it fails so we can cros workon stop afterwords.
    logging.info('Building the AP firmware packages.')
    # Print command with --debug.
    print_cmd = logging.getLogger(__name__).getEffectiveLevel() == logging.DEBUG
    default_build_flags = [
        '--deep', '--update', '--newuse', '--newrepo', '--jobs', '--verbose'
    ]
    result = cros_build_lib.run(
        [build_target.get_command('emerge')] + default_build_flags +
        list(config.build_packages),
        print_cmd=print_cmd,
        check=False,
        debug_level=logging.DEBUG,
        dryrun=dry_run,
        extra_env=extra_env)

  if result.returncode:
    # Now raise the emerge failure since we're done cleaning up.
    raise BuildError('The emerge command failed. '
                     'See the emerge output above for details.')

  logging.notice(
      'AP firmware image for device %s was built successfully '
      'and is available at %s/firmware.', build_target.name,
      build_target.full_path())


def ssh_read(path, verbose, ip, port, dryrun, region):
  """This function reads AP firmware over ssh.

  Tries to ssh to ip address once. If the ssh connection is successful the
  image is read from the DUT using flashrom, and then is copied back via scp.

  Args:
    path (str): path to the BIOS image to be flashed or read.
    verbose (bool): if True to set -v flag in flash command and
      print other debug info, if False do nothing.
    ip (str): ip address of DUT.
    port (int): The port to ssh to.
    dryrun (bool): Whether to actually execute the commands or just print
      the commands that would have been run.
    region (str): Region to read.

  Returns:
    bool: True on success, False on failure.
  """
  logging.info('Connecting to: %s\n', ip)
  id_filename = '/mnt/host/source/chromite/ssh_keys/testing_rsa'
  tmpfile = tempfile.NamedTemporaryFile()
  shutil.copyfile(id_filename, tmpfile.name)

  scp_cmd, flash_cmd = _build_read_ssh_cmds(ip, port, path, tmpfile.name,
                                            verbose, region)

  logging.info('Reading now, may take several minutes.')
  try:
    cros_build_lib.run(flash_cmd, print_cmd=verbose, check=True, dryrun=dryrun)
  except cros_build_lib.CalledProcessError:
    logging.error('Read failed.')
    return False

  try:
    cros_build_lib.run(scp_cmd, print_cmd=verbose, check=True, dryrun=dryrun)
  except cros_build_lib.CalledProcessError:
    logging.error('Could not copy image from dut.')
    return False

  return True


def _build_read_ssh_cmds(ip, port, path, tmp_file_name, verbose, region):
  """Helper function to build commands for reading images over ssh

  Args:
    ip (string): ip address of DUT.
    port (int): The port to ssh to.
    path (string): path to store the read BIOS image.
    tmp_file_name (string): name of tempfile with copy of testing_rsa
      keys.
    verbose (bool): if True set -v flag in flash command.
    region (str): Region to read.

  Returns:
    scp_cmd ([string]):
    flash_cmd ([string]):
  """
  ssh_parameters = [
      '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no',
      '-o', 'CheckHostIP=no'
  ]
  ssh_port = ['-p', str(port)] if port else []
  scp_port = ['-P', str(port)] if port else []
  remote_path = os.path.join('/tmp', os.path.basename(path))
  hostname = 'root@%s' % ip
  scp_cmd = (['scp', '-i', tmp_file_name] + scp_port + ssh_parameters +
             ['%s:%s' % (hostname, remote_path), path])
  flash_cmd = (['ssh', hostname, '-i', tmp_file_name] + ssh_port +
               ssh_parameters + ['flashrom', '-p', 'host', '-r', remote_path])
  if region:
    flash_cmd += ['-i', region]
  if verbose:
    flash_cmd += ['-V']
  return scp_cmd, flash_cmd


def clean(build_target: build_target_lib.BuildTarget, dry_run=False):
  """Cleans packages and dependencies related to a specified target.

  After running the command, the user's environment should be able to
  successfully build packages for a target board.

  Args:
    build_target: Target board to be cleaned
    dry_run: Indicates that packages and system files should not be modified
  """
  pkgs = []
  try:
    qfile_pkgs = cros_build_lib.run(
        [build_target.get_command('qfile'), '/firmware'],
        capture_output=True,
        check=False,
        dryrun=dry_run).stdout
    pkgs = [l.split()[0] for l in qfile_pkgs.decode().splitlines()]
  except cros_build_lib.RunCommandError as e:
    raise CleanError('qfile for target board %s is not present; board may '
                     'not have been set up.' % build_target.name)

  config = firmware_config.get_config(build_target.name, None)
  pkgs = set(pkgs).union(config.build_packages)
  pkgs = sorted(
      set(pkgs).union(['coreboot-private-files', 'chromeos-config-bsp']))

  err = []
  try:
    cros_build_lib.run(
        [build_target.get_command('emerge'), '--rage-clean', *pkgs],
        capture_output=True,
        dryrun=dry_run)
  except cros_build_lib.RunCommandError as e:
    err.append(e)

  try:
    if dry_run:
      logging.notice('rm -rf -- /build/%s/firmware/*', build_target.name)
    else:
      osutils.RmDir(
          '/build/%s/firmware/*' % build_target.name,
          sudo=True,
          ignore_missing=True)
  except (EnvironmentError, cros_build_lib.RunCommandError) as e:
    err.append(e)

  if err:
    logging.warning(
        'All processes for %s have completed, but some were '
        'completed with errors.', build_target.name)
    for e in err:
      logging.error(e)
    raise CleanError("`cros ap clean -b %s' did not complete successfully." %
                     build_target.name)

  logging.notice(
      'AP firmware image for device %s was successfully cleaned.'
      '\nThe following packages were unmerged: %s'
      '\nThe following build target directory was removed: '
      '/build/%s/firmware', build_target.name, ' '.join(pkgs),
      build_target.name)
