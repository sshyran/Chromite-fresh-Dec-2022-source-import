# Copyright 2013 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Script for dumping build config contents."""

from chromite.config import chromeos_config
from chromite.lib import commandline
from chromite.lib import constants
from chromite.utils import pformat


def GetParser():
    """Creates the argparse parser."""
    parser = commandline.ArgumentParser(description=__doc__)

    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        default=False,
        help="Dump fully expanded configs.",
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="store_true",
        default=False,
        help="Dump fully expanded configs as CSV.",
    )
    parser.add_argument(
        "-u",
        "--update_config",
        action="store_true",
        default=False,
        help="Update the site config json dump.",
    )
    parser.add_argument(
        "-b", "--builder", type=str, default=None, help="Single config to dump."
    )

    return parser


def main(argv):
    parser = GetParser()
    options = parser.parse_args(argv)

    site_config = chromeos_config.GetConfig()

    filename = "/dev/stdout"
    if options.update_config:
        filename = constants.CHROMEOS_CONFIG_FILE

    with open(filename, "w") as f:
        if options.builder:
            if options.builder not in site_config:
                raise Exception(
                    "%s: Not a valid build config." % options.builder
                )
            pformat.json(site_config[options.builder], fp=f)
        elif options.full:
            f.write(site_config.DumpExpandedConfigToString())
        elif options.csv:
            f.write(site_config.DumpConfigCsv())
        else:
            f.write(site_config.SaveConfigToString())
