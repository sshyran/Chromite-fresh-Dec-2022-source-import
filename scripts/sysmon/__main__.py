# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Send system monitoring data to the timeseries monitoring API."""

from __future__ import print_function

import random
import time

import psutil

from chromite.lib import commandline
from chromite.lib import cros_logging as logging
from chromite.lib import metrics
from chromite.lib import ts_mon_config
from chromite.scripts.sysmon import puppet_metrics
from chromite.scripts.sysmon import system_metrics
from chromite.scripts.sysmon import loop
from infra_libs.ts_mon.common import interface

logger = logging.getLogger(__name__)


def collect_metrics(cycles):
  system_metrics.get_uptime()
  system_metrics.get_cpu_info()
  system_metrics.get_disk_info()
  system_metrics.get_mem_info()
  system_metrics.get_net_info()
  system_metrics.get_proc_info()
  system_metrics.get_load_avg()
  puppet_metrics.get_puppet_summary()
  if cycles == 0:
    system_metrics.get_os_info()
  system_metrics.get_unix_time()  # must be just before flush
  metrics.Flush()


def main():
  parser = commandline.ArgumentParser(
      description=__doc__,
      default_log_level='DEBUG')
  parser.add_argument(
      '--interval',
      default=60,
      type=int,
      help='time (in seconds) between sampling system metrics')
  opts = parser.parse_args()
  opts.Freeze()

  # This returns a 0 value the first time it's called.  Call it now and
  # discard the return value.
  psutil.cpu_times_percent()

  # Wait a random amount of time before starting the loop in case sysmon
  # is started at exactly the same time on all machines.
  time.sleep(random.uniform(0, opts.interval))

  # This call returns a context manager that doesn't do anything, so we
  # ignore the return value.
  ts_mon_config.SetupTsMonGlobalState('sysmon', auto_flush=False)
  # The default prefix is '/chrome/infra/'.
  interface.state.metric_name_prefix = (interface.state.metric_name_prefix
                                        + 'chromeos/sysmon/')

  loop.SleepLoop(callback=collect_metrics,
                 interval=opts.interval).loop_forever()


if __name__ == '__main__':
  main()
