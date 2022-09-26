# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Implement the `cros tryjob` CLI, which forwards to the myjob binary.

The myjob binary is defined in the infra/infra repository, and distributed via
CIPD. This CLI ensures that the CIPD package is installed and up-to-date,
captures all input arguments, and forwards them to the myjob binary.

The myjob CLI launches a builder via `bb add`, incorporating input properties
specified via command-line args.
"""

import argparse

from chromite.cli import command
from chromite.lib import cipd
from chromite.lib import cros_build_lib


@command.command_decorator("myjob")
class MyjobCommand(command.CliCommand):
    """Implementation of the `cros myjob` command."""

    EPILOG = """
    Run a builder with bespoke configurations via the myjob package.
    For help, run `cros myjob help` (with no hyphens).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._myjob_cmd = None

    @classmethod
    def AddParser(cls, parser):
        """Capture all CLI args to forward to the go bin."""
        super(cls, MyjobCommand).AddParser(parser)
        parser.add_argument("input", action="append", nargs=argparse.REMAINDER)

    def Run(self):
        """Install and run the myjob binary."""
        self._InstallMyjobPackage()
        self._RunMyjob(self.options.input[0])

    def _InstallMyjobPackage(self, version="prod"):
        """Install the `myjob` package from CIPD, and save its path.

        If the package is already present in the CIPD cache, it will be updated
        to the specified version.

        Args:
            version: The CIPD version of the package to install. Can be either
                an instance ID or a ref.
        """
        myjob_dir = cipd.InstallPackage(
            cipd.GetCIPDFromCache(),
            "chromiumos/infra/myjob/linux-amd64",
            version,
        )
        self._myjob_cmd = f"{myjob_dir}/myjob"

    def _RunMyjob(self, args):
        """Run the `myjob` command with the specified arguments.

        Args:
            args: List[str], command-line args to pass into myjob.
        """
        assert (
            self._myjob_cmd is not None
        ), "Must install myjob package before running myjob command."
        cmd = [self._myjob_cmd]
        cmd.extend(args)
        cros_build_lib.run([self._myjob_cmd] + args)
