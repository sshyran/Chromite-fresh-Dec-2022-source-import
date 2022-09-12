#!/usr/bin/env python3
# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""CR and CQ +2 Zephyr commits for downstreaming.

For Zephyr Downstreaming Rotation: go/zephyr-downstreaming-guide
"""

import logging

from chromite.lib import commandline
from chromite.lib import config_lib
from chromite.lib import gerrit


# Gerrit will merge a max of 240 dependencies. Leave some room
# for dependencies from the platform/ec repo.
MAX_GERRIT_CHANGES = 225


def main(args):
    """Downstream Zephyr CLs."""
    # TODO(aaronmassey): Add option to rebase CLs.
    parser = commandline.ArgumentParser(__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Dry run, no updates to Gerrit."
    )
    parser.add_argument(
        "--limit", type=int, help="How many changes to modify, from the oldest."
    )
    parser.add_argument(
        "--stop-at", type=str, help="Stop at the specified change number."
    )
    opts = parser.parse_args(args)
    dry_run = opts.dry_run

    site_params = config_lib.GetSiteParams()
    cros = gerrit.GetGerritHelper(site_params.EXTERNAL_REMOTE)

    cls_to_downstream = cros.Query(
        topic="zephyr-downstream", status="open", raw=True
    )
    cls_to_downstream.sort(key=lambda patch: patch["number"])

    if opts.limit:
        cls_to_downstream = cls_to_downstream[: opts.limit]

    logging.info(
        "Downstreaming the following CLs:\n%s",
        "\n".join((patch["number"] for patch in cls_to_downstream)),
    )

    stop_at = opts.stop_at
    # TODO(aaronmassey): Investigate bulk changes from Gerrit lib API instead.
    for i, patch in enumerate(cls_to_downstream):
        change_num = patch["number"]

        if stop_at and stop_at == change_num:
            logging.info(
                "Matched change: %s, stop processing other changes", change_num
            )
            break

        if i + 1 > MAX_GERRIT_CHANGES:
            logging.info(
                "Maximum Gerrit limit reached at change: %s,"
                " stop processing other changes",
                change_num,
            )
            break

        logging.info(
            "Downstreaming %s: %d/%d", change_num, i + 1, len(cls_to_downstream)
        )

        cros.SetReviewers(change=change_num, dryrun=dry_run, notify="NONE")
        cros.SetReview(
            change=change_num,
            dryrun=dry_run,
            # Add Verified label because client POST removes it.
            labels={
                "Verified": "1",
                "Code-Review": "2",
                "Commit-Queue": "2",
            },
        )

    logging.info("All finished! Remember to monitor the CQ!")
