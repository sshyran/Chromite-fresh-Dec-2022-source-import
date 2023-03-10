# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""cros chroot: Enter the chroot for the current build environment."""

import argparse

from chromite.lib import constants
from chromite.cli import command
from chromite.lib import cros_build_lib


@command.command_decorator('chroot')
class ChrootCommand(command.CliCommand):
  """Enter the chroot."""

  def _RunChrootCommand(self, cmd):
    """Run the specified command inside the chroot.

    Args:
      cmd: A list or tuple of strings to use as a command and its arguments.
           If empty, run 'bash'.

    Returns:
      The commands result code.
    """
    # If there is no command, run bash.
    if not cmd:
      cmd = ['bash']

    chroot_args = ['--log-level', self.options.log_level]

    result = cros_build_lib.run(cmd, print_cmd=False, check=False,
                                cwd=constants.SOURCE_ROOT, enter_chroot=True,
                                chroot_args=chroot_args)
    return result.returncode

  @classmethod
  def AddParser(cls, parser):
    """Adds a parser."""
    super(cls, ChrootCommand).AddParser(parser)
    parser.add_argument(
        'command', nargs=argparse.REMAINDER,
        help='(optional) Command to execute inside the chroot.')

  def Run(self):
    """Runs `cros chroot`."""
    cmd = self.options.command

    # If -- was used to separate out the command from arguments, ignore it.
    if cmd and cmd[0] == '--':
      cmd = cmd[1:]

    return self._RunChrootCommand(cmd)
