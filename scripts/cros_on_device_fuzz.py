#!/usr/bin/env python3
# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run fuzzers on ChromeOS Devices for given packages.

Given a remote host and a list of portage packages,
run the associated package fuzzers in a sysroot on the
remote host.

As of 2022-10-24, this script is intended to
only test fuzzers on x86_64 devices.

Example:
    cros_on_device_fuzz setup 'myhost:1234' 'my_package'
    cros_on_device_fuzz fuzz 'myhost:1234' 'my_installed_fuzzer'
"""

import logging
from pathlib import Path
import re
import tempfile
from typing import Iterable

from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import on_device_fuzz
from chromite.lib import remote_access


_DEFAULT_PRIVATE_KEY = Path.home() / ".ssh" / "testing_rsa"
_DUT_FUZZER_ROOT = Path("/usr/local/tmp/fuzzer_root")
_IMPLICIT_SYSTEM_PACKAGE = "virtual/implicit-system"
_PACKAGE_SEPARATOR = re.compile("[ ,]+")


def main(argv: Iterable[str]):
    """Dispatch to other functions."""
    args = parse_args(argv)
    args.func(args)


def setup_main(args):
    """Setup up the DUT for fuzzing."""
    cros_build_lib.AssertInsideChroot()
    device = _parse_device(args.device_host, _DEFAULT_PRIVATE_KEY)
    # We do this version check to ensure we have a CrOS device
    # immediately.
    try:
        version = device.version
    except Exception:
        logging.error("Unable to get version of remote %s", args.device_host)
        raise
    logging.info("Connected to %s; CrOS version %s", args.device_host, version)
    packages = set(re.split(_PACKAGE_SEPARATOR, args.packages))
    # We require virtual/implicit-system so that we can
    # build the on-device sysroot. Without it, we'll
    # miss critical libs and binaries.
    packages.add(_IMPLICIT_SYSTEM_PACKAGE)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tarball_name = "sysroot_fuzzer_tarball.tar.xz"
        on_device_fuzz.create_sysroot_tarball(
            packages=packages,
            board="amd64-generic",
            output_path=tmpdir / tarball_name,
        )
        on_device_fuzz.create_dut_sysroot(
            device,
            sysroot_tarball=tmpdir / tarball_name,
            sysroot_device_path=_DUT_FUZZER_ROOT,
        )
    logging.info("Fuzzer set up complete for %s", args.device_host)


def fuzz_main(args):
    """Run a given fuzzer on the DUT."""
    cros_build_lib.AssertInsideChroot()
    fuzzer_install_path = Path("/usr/libexec/fuzzers")
    device = _parse_device(args.device_host, _DEFAULT_PRIVATE_KEY)
    libfuzzer_options = {}
    on_device_fuzz.run_fuzzer_executable(
        device,
        sysroot_device_path=_DUT_FUZZER_ROOT,
        sysroot_fuzzer_path=fuzzer_install_path / args.fuzzer_name,
        libfuzzer_options=libfuzzer_options,
    )


def _parse_device(
    device_host: str, private_key: Path
) -> remote_access.ChromiumOSDevice:
    """Get ChromiumOSDevice host from device_host format string.

    Gets a ChromiumOSDevice, executing as root.

    Args:
        device_host: 'hostname:port' or 'hostname' string.
        private_key: Path to private key to log into the device for.

    Returns:
        A remote_access.ChromiumOSDevice connection.

    Raises:
        ValueError if device_host is not formatted correctly.
    """
    host = device_host.split(":")
    if len(host) == 2:
        device = remote_access.ChromiumOSDevice(
            host[0],
            port=host[1],
            username="root",
            private_key=private_key,
            connect=True,
        )
    elif len(host) == 1:
        device = remote_access.ChromiumOSDevice(
            host[0],
            username="root",
            private_key=private_key,
            connect=True,
        )
    else:
        raise ValueError(f"Badly formatted device host: {device_host}")
    return device


def parse_args(raw_args: Iterable[str]):
    """Parse CLI arguments."""
    parser = commandline.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-key",
        type=Path,
        default=_DEFAULT_PRIVATE_KEY,
        help=f"RSA key for device. (default: {_DEFAULT_PRIVATE_KEY})",
    )
    subparsers = parser.add_subparsers()

    # setup subcommand
    setup_parser = subparsers.add_parser(
        "setup", help="Installs fuzzers on device sysroot."
    )
    setup_parser.set_defaults(func=setup_main)
    device_host_help = "Device host, in the format 'hostname:port'"
    setup_parser.add_argument(
        "--device-sysroot-path",
        type=Path,
        help="Absolute location on device for the"
        f" fuzzer sysroot. (default: {_DUT_FUZZER_ROOT})",
        default=_DUT_FUZZER_ROOT,
    )
    setup_parser.add_argument("device_host", help=device_host_help)
    setup_parser.add_argument(
        "packages",
        help="Portage packages to install fuzzers for."
        " Space or comma separated."
        f" Automatically includes {_IMPLICIT_SYSTEM_PACKAGE}",
    )

    # fuzz subcommand
    fuzz_parser = subparsers.add_parser(
        "fuzz", help="Runs a fuzzer in device sysroot."
    )
    fuzz_parser.set_defaults(func=fuzz_main)
    fuzz_parser.add_argument("device_host", help=device_host_help)
    fuzz_parser.add_argument(
        "fuzzer_name", help="Name of the fuzzer executable to run."
    )

    return parser.parse_args(raw_args)
