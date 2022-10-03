# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Implement the `cros try` CLI, which forwards to the try binary.

The try binary is defined in the infra/infra repository, and distributed via
CIPD. This CLI ensures that the CIPD package is installed and up-to-date,
captures all input arguments, and forwards them to the try binary.
"""

import argparse
from pathlib import Path
from typing import List

from chromite.cli import command
from chromite.lib import cipd
from chromite.lib import cros_build_lib


PINNED_TRY_VERSION = "KV2Fc_xe8IsjZRypqi10EN5N0w4pp28KaTEN-_oFTN4C"


@command.command_decorator("try")
class TryCommand(command.CliCommand):
    """Implementation of the `cros try` command."""

    EPILOG = """
Run a builder with bespoke configurations via the try package.
For help, run `cros try help` (with no hyphens).
"""

    @classmethod
    def AddParser(cls, parser: argparse.ArgumentParser):
        """Capture all CLI args to forward to the go bin."""
        super().AddParser(parser)
        parser.add_argument("input", action="append", nargs=argparse.REMAINDER)

    def Run(self) -> int:
        """Install and run the try binary.

        Returns:
            The return code of the completed try process.
        """
        try_bin = _InstallTryPackage()
        return self._RunTry(try_bin, self.options.input[0])

    def _RunTry(self, try_bin: Path, args: List[str]) -> int:
        """Run the `try` command with the specified arguments.

        Args:
            try_bin: Path to the try binary.
            args: command-line args to pass into try.

        Returns:
            The return code of the completed try process.
        """
        cmd = [str(try_bin)] + args
        p = cros_build_lib.run(cmd, check=False)
        return p.returncode


def _InstallTryPackage(version: str = PINNED_TRY_VERSION) -> Path:
    """Install the `try` package from CIPD, and save its path.

    If the package is already present in the CIPD cache, it will be updated
    to the specified version.

    Args:
        version: The CIPD version of the package to install. Can be either
            an instance ID or a ref.

    Returns:
        The path to the try binary.
    """
    try_dir = cipd.InstallPackage(
        cipd.GetCIPDFromCache(),
        "chromiumos/infra/try/linux-amd64",
        version,
    )
    return Path(try_dir) / "try"
