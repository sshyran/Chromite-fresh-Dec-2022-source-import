# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""cros ap: firmware AP related commands."""

import os
from pathlib import Path
import sys

from abc import ABCMeta, abstractmethod
from chromite.lib import build_target_lib
from chromite.cli import command
from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import pformat
from chromite.lib.firmware import ap_firmware, flash_ap, servo_lib

COMMAND_DUMP_CONFIG = 'dump-config'
COMMAND_BUILD = 'build'
COMMAND_FLASH = 'flash'
COMMAND_READ = 'read'


@command.CommandDecorator('ap')
class APCommand(command.CliCommand):
  """Execute an AP-related command."""

  EPILOG = 'Use `cros ${subcommand} --help` to see command-specific help.'

  @classmethod
  def AddParser(cls, parser):
    """Add AP specific subcommands and options."""
    super(APCommand, cls).AddParser(parser)
    subparsers = parser.add_subparsers(
        title='AP subcommands', dest='ap_command')
    subparsers.required = True

    dump_config_parser = _AddSubparser(parser, subparsers, COMMAND_DUMP_CONFIG,
                                       'Dump the AP Config to a file.')
    DumpConfigSubcommand.AddCLIArguments(cls, dump_config_parser)

    build_parser = _AddSubparser(
        parser, subparsers, COMMAND_BUILD,
        'Build the AP Firmware for the requested build target.')
    BuildSubcommand.AddCLIArguments(cls, build_parser)

    flash_parser = _AddSubparser(parser, subparsers, COMMAND_FLASH,
                                 'Update the AP Firmware on a device.')
    FlashSubcommand.AddCLIArguments(cls, flash_parser)

    read_parser = _AddSubparser(parser, subparsers, COMMAND_READ,
                                'Read the AP Firmware from a device.')
    ReadSubcommand.AddCLIArguments(cls, read_parser)

  def Run(self):
    """The main handler of this CLI."""
    if self.options.ap_command == COMMAND_DUMP_CONFIG:
      subcmd = DumpConfigSubcommand(self.options)
    elif self.options.ap_command == COMMAND_BUILD:
      subcmd = BuildSubcommand(self.options)
    elif self.options.ap_command == COMMAND_FLASH:
      subcmd = FlashSubcommand(self.options)
    elif self.options.ap_command == COMMAND_READ:
      subcmd = ReadSubcommand(self.options)
    subcmd.run()


def _AddSubparser(parser, subparsers, name, description):
  """Adds a subparser to the given parser, with common options.

  Forwards some options from the parser to the new subparser to ensure
  consistent formatting of output etc.

  Args:
    parser: The parent parser for this subparser.
    subparsers: The subparsers group to add this subparser to.
    name: Name of the new sub-command.
    description: Description to be used for the sub-command.

  Returns:
    The new subparser.
  """
  return subparsers.add_parser(
      name,
      description=description,
      caching=parser.caching,
      help=description,
      formatter_class=parser.formatter_class,
  )


class APSubcommandInterface(metaclass=ABCMeta):
  """Virtual class declaring methods of AP subcommand."""

  def __init__(self, options) -> None:
    self.options = options

  @abstractmethod
  def run(self):
    """Executes the command."""

  @staticmethod
  @abstractmethod
  def AddCLIArguments(cmd, subparser):
    """Adds subcommand-specific CLI arguments to subparser."""


class DumpConfigSubcommand(APSubcommandInterface):
  """Dump the AP Config to a file."""

  def __init__(self, options):
    super().__init__(options)
    if self.options.output:
      self.options.output = Path(self.options.output)
    self.options.Freeze()

  @staticmethod
  def AddCLIArguments(cmd, subparser):
    """Adds AP DumpConfig specific CLI arguments to subparser."""
    subparser.add_argument(
        '-b',
        '--boards',
        default=None,
        action='split_extend',
        dest='boards',
        help='Space-separated list of boards. '
        '(default: all boards in chromite/lib/firmware/ap_firmware_config)')
    subparser.add_argument(
        '--serial',
        default='%s',
        help='Serial of the servos. (default: %(default)s)')
    subparser.add_argument('-o', '--output', type='path', help='Output file.')
    subparser.epilog = """
Dump DUT controls and programmer arguments into a provided file.

To dump AP config of all boards into /tmp/cros-read-ap-config.json
  cros ap dump-config -o /tmp/cros-read-ap-config.json

To dump AP config of drallion and dedede boards:
  cros ap dump-config -o /tmp/cros-read-ap-config.json -b drallion,dedede
"""

  def run(self):
    """Perform the cros ap dump-config command."""
    boards = []
    if self.options.boards:
      boards = self.options.boards
    else:
      # Get the board list from config python modules in
      # chromite/lib/firmware/ap_firmware_config
      path_to_firmware_configs = (
          Path(constants.CHROMITE_DIR) / 'lib' / 'firmware' /
          'ap_firmware_config')
      for p in path_to_firmware_configs.glob('*.py'):
        if not p.is_file():
          continue
        if p.name.startswith('_'):
          continue
        # Remove paths, leaving only filenames, and remove .py suffixes.
        boards.append(p.with_suffix('').name)
    boards.sort()

    if self.options.output:
      output_path = self.options.output
      logging.info('Dumping AP config to %s', output_path)
      logging.info('List of boards: %s', ', '.join(boards))
      logging.info('List of servos: %s', ', '.join(servo_lib.VALID_SERVOS))
    else:
      output_path = sys.stdout

    output = {}
    failed_board_servos = {}
    for board in boards:
      module = ap_firmware.get_config_module(board)
      output[board] = {}
      for servo_version in servo_lib.VALID_SERVOS:
        servo = servo_lib.Servo(servo_version, self.options.serial)
        # get_config() call is expected to fail for some board:servo pairs.
        # Disable logging to avoid inconsistent error messages from config
        # modules' get_config() calls.
        logging.disable(logging.CRITICAL)
        try:
          ap_config = module.get_config(servo)
        except servo_lib.UnsupportedServoVersionError:
          failed_board_servos.setdefault(board, []).append(servo_version)
          continue
        finally:
          # Reenable logging.
          logging.disable(logging.DEBUG)

        output[board][servo_version] = {
            'dut_control_on': ap_config.dut_control_on,
            'dut_control_off': ap_config.dut_control_off,
            'programmer': ap_config.programmer,
        }
    for board, servos in failed_board_servos.items():
      logging.notice(f'[{board}] skipping servos ' f'{", ".join(servos)}')

    with cros_build_lib.Open(output_path, 'w', encoding='utf-8') as f:
      pformat.json(output, f)


class BuildSubcommand(APSubcommandInterface):
  """Build the AP Firmware for the requested build target."""

  def __init__(self, options):
    super().__init__(options)
    self.build_target = build_target_lib.BuildTarget(self.options.build_target)
    self.options.Freeze()

  @staticmethod
  def AddCLIArguments(cmd, subparser):
    """Adds AP Build specific CLI arguments to subparser."""
    subparser.add_argument(
        '-b',
        '--build-target',
        dest='build_target',
        default=cros_build_lib.GetDefaultBoard(),
        required=not bool(cros_build_lib.GetDefaultBoard()),
        help='The build target whose AP firmware should be built.')
    subparser.add_argument(
        '--fw-name',
        '--variant',
        dest='fw_name',
        help='Sets the FW_NAME environment variable. Set to build only the '
        "specified variant's firmware.")
    # TODO(saklein): Remove when added to base parser.
    subparser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        default=False,
        help='Perform a dry run, describing the steps without running them.')
    subparser.epilog = """
To build the AP Firmware for foo:
  cros ap build -b foo

To build the AP Firmware only for foo-variant:
  cros ap build -b foo --fw-name foo-variant
"""

  def run(self):
    commandline.RunInsideChroot(self)

    try:
      ap_firmware.build(
          self.build_target,
          fw_name=self.options.fw_name,
          dry_run=self.options.dry_run)
    except ap_firmware.Error as e:
      cros_build_lib.Die(e)


class ReadSubcommand(APSubcommandInterface):
  """Read the AP Firmware from a device."""

  def __init__(self, options):
    super().__init__(options)
    if self.options.device is None:
      cros_build_lib.Die('Specify device using --device argument.')
    self.options.output_path = Path(self.options.output)
    self.options.Freeze()

  @staticmethod
  def AddCLIArguments(cmd, subparser):
    """Adds AP Read specific CLI arguments to subparser."""
    cmd.AddDeviceArgument(
        subparser,
        schemes=[
            commandline.DEVICE_SCHEME_SSH, commandline.DEVICE_SCHEME_SERVO
        ])
    subparser.add_argument(
        '-b',
        '--build-target',
        default=cros_build_lib.GetDefaultBoard(),
        dest='build_target',
        help='The name of the build target.')
    subparser.add_argument('-r'
                           '--region',
                           dest='region',
                           type=str,
                           help='Region to read.')
    subparser.add_argument(
        '-o', '--output', type='path', required=True, help='Output file.')
    subparser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        help='Execute a dry-run. Print the commands that would be run instead '
        'of running them.')
    subparser.epilog = """Command to read the AP firmware from a DUT.
To read image of device.cros via SSH:
  cros ap read -b volteer -o /tmp/volteer-image.bin -d ssh://device.cros

If you don't have ssh access from within the chroot, you may set up ssh tunnel:
  ssh -L 2222:localhost:22 device.cros
  cros ap read -b volteer -o /tmp/volteer-image.bin -d ssh://localhost:2222

To read image from DUT via SERVO on port 1234:
  cros ap read -b volteer -o /tmp/volteer-image.bin -d servo:port:1234

To read a specific region from DUT via SERVO on default port(9999):
  cros ap read -b volteer -r region -o /tmp/volteer-image.bin -d servo:port
"""

  def run(self):
    if not cros_build_lib.IsInsideChroot():
      logging.notice('Command will run in chroot, '
                     'and the output file path will be inside.')
    commandline.RunInsideChroot(self)
    build_target = build_target_lib.BuildTarget(self.options.build_target)

    ip = None
    if self.options.device:
      port = self.options.device.port
      if self.options.device.scheme == commandline.DEVICE_SCHEME_SSH:
        ip = self.options.device.hostname
        port = port or self.options.device.port
    else:
      ip = os.getenv('IP')

    region = None
    if hasattr(self.options, 'region'):
      region = self.options.region

    if ip:
      flash_ap.ssh_read(self.options.output, self.options.verbose, ip, port,
                        self.options.dry_run, region)
    else:
      dut_ctl = servo_lib.DutControl(port)
      servo = servo_lib.get(dut_ctl)

      config_module = ap_firmware.get_config_module(build_target.name)
      ap_config = config_module.get_config(servo)

      flashrom_cmd = [
          'flashrom', '-p', ap_config.programmer, '-r', self.options.output
      ]
      if self.options.verbose:
        flashrom_cmd += ['-V']
      if region:
        flashrom_cmd += ['-i', self.options.region]
      if not flash_ap.servo_run(dut_ctl, ap_config.dut_control_on,
                                ap_config.dut_control_off, flashrom_cmd,
                                self.options.verbose, self.options.dry_run):
        logging.error('Unable to read, verify servo connection '
                      'is correct and servod is running in the background.')


class FlashSubcommand(APSubcommandInterface):
  """Update the AP Firmware on a device."""

  def __init__(self, options):
    super().__init__(options)
    if not os.path.exists(self.options.image):
      logging.error(
          '%s does not exist, verify the path of your build and try '
          'again.', self.options.image)
    self.options.Freeze()

  @staticmethod
  def AddCLIArguments(cmd, subparser):
    """Adds AP Flash specific CLI arguments to subparser."""
    cmd.AddDeviceArgument(
        subparser,
        schemes=[
            commandline.DEVICE_SCHEME_SSH, commandline.DEVICE_SCHEME_SERVO
        ])
    subparser.add_argument(
        '-i',
        '--image',
        required=True,
        type='path',
        help='/path/to/BIOS_image.bin')
    subparser.add_argument(
        '-b',
        '--build-target',
        default=cros_build_lib.GetDefaultBoard(),
        dest='build_target',
        help='The name of the build target.')
    subparser.add_argument(
        '--flashrom',
        action='store_true',
        help='Use flashrom to flash instead of futility.')
    subparser.add_argument(
        '--flash-contents',
        type=str,
        help='Assume flash contents to be the specified file. '
        'Only available when using --flashrom.')
    subparser.add_argument(
        '--fast',
        action='store_true',
        help='Speed up flashing by not validating flash.')
    subparser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        help='Execute a dry-run. Print the commands that would be run instead '
        'of running them.')
    subparser.epilog = """
Command to flash the AP firmware onto a DUT.

To flash your zork DUT with an IP of 1.1.1.1 via SSH:
  cros ap flash -b zork -i /path/to/image.bin -d ssh://1.1.1.1

To flash your volteer DUT via SERVO on the default port (9999):
  cros ap flash -d servo:port -b volteer -i /path/to/image.bin

To flash your volteer DUT via SERVO on port 1234:
  cros ap flash -d servo:port:1234 -b volteer -i /path/to/image.bin
"""

  def run(self):
    commandline.RunInsideChroot(self)

    build_target = build_target_lib.BuildTarget(self.options.build_target)
    try:
      ap_firmware.deploy(
          build_target,
          self.options.image,
          self.options.device,
          flashrom=self.options.flashrom,
          fast=self.options.fast,
          verbose=self.options.verbose,
          dryrun=self.options.dry_run,
          flash_contents=self.options.flash_contents)
    except ap_firmware.Error as e:
      cros_build_lib.Die(e)
