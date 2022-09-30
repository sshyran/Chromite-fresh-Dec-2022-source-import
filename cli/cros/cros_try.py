# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Implement the `cros try` CLI, which forwards to the myjob binary.

The myjob binary is defined in the infra/infra repository, and distributed via
CIPD. This CLI ensures that the CIPD package is installed and up-to-date,
captures all input arguments, and forwards them to the myjob binary.

TODO (b/250076720): Update all `myjob` references to the new `try` package,
once it exists.
"""

import argparse
from pathlib import Path
from typing import List

from chromite.cli import command
from chromite.lib import cipd
from chromite.lib import cros_build_lib


PINNED_MYJOB_VERSION = "TtpakXXGnP2zeWvAG79iLTROZZU2tL0eIUgQvijeWHkC"


@command.command_decorator("try")
class TryCommand(command.CliCommand):
    """Implementation of the `cros try` command."""

    EPILOG = """
Run a builder with bespoke configurations via the myjob package.
For help, run `cros myjob help` (with no hyphens).
"""

    @classmethod
    def AddParser(cls, parser: argparse.ArgumentParser):
        """Capture all CLI args to forward to the go bin."""
        super().AddParser(parser)
        parser.add_argument("input", action="append", nargs=argparse.REMAINDER)

    def Run(self) -> int:
        """Install and run the myjob binary.

        Returns:
            The return code of the completed myjob process.
        """
        myjob_bin = _InstallMyjobPackage()
        return self._RunMyjob(myjob_bin, self.options.input[0])

    def _RunMyjob(self, myjob_bin: Path, args: List[str]) -> int:
        """Run the `myjob` command with the specified arguments.

        Args:
            myjob_bin: Path to the myjob binary.
            args: command-line args to pass into myjob.

        Returns:
            The return code of the completed myjob process.
        """
        cmd = [str(myjob_bin)] + args
        p = cros_build_lib.run(cmd, check=False)
        return p.returncode


def _InstallMyjobPackage(version: str = PINNED_MYJOB_VERSION) -> Path:
    """Install the `myjob` package from CIPD, and save its path.

    If the package is already present in the CIPD cache, it will be updated
    to the specified version.

    Args:
        version: The CIPD version of the package to install. Can be either
            an instance ID or a ref.

    Returns:
        The path to the myjob binary.
    """
    myjob_dir = cipd.InstallPackage(
        cipd.GetCIPDFromCache(),
        "chromiumos/infra/myjob/linux-amd64",
        version,
    )
    return Path(myjob_dir) / "myjob"
