#!/usr/bin/env python3
# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""CR and CQ +2 Zephyr commits for downstreaming.

For Zephyr Downstreaming Rotation: go/zephyr-downstreaming-guide
"""

import logging

from chromite.lib import commandline
from chromite.lib import config_lib
from chromite.lib import gerrit


def main(args):
  """Downstream Zephyr CLs."""
  # TODO(aaronmassey): Add option to rebase CLs.
  parser = commandline.ArgumentParser(__doc__)
  parser.add_argument('--dry-run',
                      action='store_true',
                      help='Dry run, no updates to Gerrit.')
  opts = parser.parse_args(args)
  dry_run = opts.dry_run

  site_params = config_lib.GetSiteParams()
  cros = gerrit.GetGerritHelper(site_params.EXTERNAL_REMOTE)

  cls_to_downstream = cros.Query(topic='zephyr-downstream', status='open',
                                 raw=True)
  cls_to_downstream.sort(key=lambda patch: patch['number'])

  logging.info('Downstreaming the following CLs:\n%s',
               '\n'.join((patch['number'] for patch in cls_to_downstream)))

  # TODO(aaronmassey): Investigate bulk changes from Gerrit lib API instead.
  for i, patch in enumerate(cls_to_downstream):
    change_num = patch['number']
    logging.info('Downstreaming %s: %d/%d',
                 change_num,
                 i + 1,
                 len(cls_to_downstream))

    cros.SetReviewers(change=change_num, dryrun=dry_run, notify='NONE')
    cros.SetReview(change=change_num,
                   dryrun=dry_run,
                   # Add Verified label because client POST removes it.
                   labels={'Verified': '1',
                           'Code-Review': '2',
                           'Commit-Queue': '2', })

  logging.info('All finished! Remember to monitor the CQ!')
