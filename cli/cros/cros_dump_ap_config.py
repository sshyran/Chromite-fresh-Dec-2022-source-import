# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""dump-ap-config command."""

import importlib
from pathlib import Path
import sys

from chromite.cli import command
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import pformat
from chromite.lib.firmware import servo_lib

assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


@command.CommandDecorator('dump-ap-config')
class DumpApConfigCommand(command.CliCommand):
  """Dump the AP Config to a file."""

  EPILOG = """Dump DUT controls and programmer arguments into a provided file.

To dump AP config of all boards into /tmp/cros-read-ap-config.json
  cros read-ap-config -o /tmp/cros-read-ap-config.json

To dump AP config of drallion and dedede boards:
  cros read-ap-config -o /tmp/cros-read-ap-config.json -b drallion,dedede
"""

  @classmethod
  def AddParser(cls, parser):
    super().AddParser(parser)
    parser.add_argument(
        '-b',
        '--boards',
        default=None,
        action='split_extend',
        dest='boards',
        help='Space-separated list of boards. '
        '(default: all boards in chromite/lib/firmware/ap_firmware_config)')
    parser.add_argument(
        '--serial',
        default='%s',
        help='Serial of the servos. (default: %(default)s)')
    parser.add_argument(
        '-o', '--output', type='path', required=True, help='Output file.')

  def validate_options(self):
    """Parse the arguments."""
    self.options.output_path = Path(self.options.output)
    self.options.Freeze()

  def Run(self):
    """Perform the cros dump-ap-config command."""
    self.validate_options()

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

    logging.info('Dumping AP config to %s', self.options.output_path)
    logging.info('List of boards: %s', ', '.join(boards))
    logging.info('List of servos: %s', ', '.join(servo_lib.VALID_SERVOS))

    output = {}
    failed_board_servos = {}
    for board in boards:
      module_name = f'chromite.lib.firmware.ap_firmware_config.{board}'
      try:
        module = importlib.import_module(module_name)
      except ImportError as e:
        cros_build_lib.Die(f'Failed to import config module {module_name}: {e}')

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

    with self.options.output_path.open('w', encoding='utf-8') as f:
      pformat.json(output, f)
