# Copyright 2017 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Process metrics."""

from __future__ import absolute_import

from functools import partial
import logging

import psutil  # pylint: disable=import-error

from chromite.lib import metrics


logger = logging.getLogger(__name__)

_count_metric = metrics.GaugeMetric(
    "proc/count", description="Number of processes currently running."
)
_cpu_percent_metric = metrics.GaugeMetric(
    "proc/cpu_percent", description="CPU usage percent of processes."
)


def collect_proc_info():
    collector = _ProcessMetricsCollector()
    collector.collect()


class _ProcessMetricsCollector(object):
    """Class for collecting process metrics."""

    def __init__(self):
        self._metrics = [
            _ProcessMetric("autoserv", test_func=_is_parent_autoserv),
            _ProcessMetric(
                "cache-downloader",
                test_func=partial(_is_process_name, "downloader")
            ),
            _ProcessMetric(
                "common-tls", test_func=partial(_is_process_name, "common-tls")
            ),
            _ProcessMetric("curl", test_func=partial(_is_process_name, "curl")),
            _ProcessMetric(
                "dnsmasq", test_func=partial(_is_process_name, "dnsmasq")
            ),
            _ProcessMetric(
                "drone-agent",
                test_func=partial(_is_process_name, "drone-agent")
            ),
            _ProcessMetric(
                "fleet-tlw", test_func=partial(_is_process_name, "fleet-tlw")
            ),
            _ProcessMetric(
                "getty", test_func=partial(_is_process_name, "getty")
            ),
            _ProcessMetric(
                "gs_offloader",
                test_func=partial(_is_process_name, "gs_offloader.py"),
            ),
            _ProcessMetric("gsutil", test_func=_is_gsutil),
            _ProcessMetric("java", test_func=partial(_is_process_name, "java")),
            _ProcessMetric(
                "labservice", test_func=partial(_is_process_name, "labservice")
            ),
            _ProcessMetric(
                "lxc-attach", test_func=partial(_is_process_name, "lxc-attach")
            ),
            _ProcessMetric(
                "lxc-start", test_func=partial(_is_process_name, "lxc-start")
            ),
            _ProcessMetric("sshd", test_func=partial(_is_process_name, "sshd")),
            _ProcessMetric("swarming_bot", test_func=_is_swarming_bot),
            _ProcessMetric(
                "sysmon",
                test_func=partial(_is_python_module, "chromite.scripts.sysmon"),
            ),
            _ProcessMetric("tko_proxy", test_func=_is_tko_proxy),
        ]
        self._other_metric = _ProcessMetric("other")

    def collect(self):
        for proc in psutil.process_iter():
            self._collect_proc(proc)
        self._flush()

    def _collect_proc(self, proc):
        for metric in self._metrics:
            if metric.add(proc):
                break
        else:
            self._other_metric.add(proc)

    def _flush(self):
        for metric in self._metrics:
            metric.flush()
        self._other_metric.flush()


class _ProcessMetric(object):
    """Class for gathering process metrics."""

    def __init__(self, process_name, test_func=lambda proc: True):
        """Initialize instance.

        process_name is used to identify the metric stream.

        test_func is a function called
        for each process.  If it returns True, the process is counted.  The
        default test is to count every process.
        """
        self._fields = {
            "process_name": process_name,
        }
        self._test_func = test_func
        self._count = 0
        self._cpu_percent = 0

    def add(self, proc):
        """Do metric collection for the given process.

        Returns True if the process was collected.
        """
        if not self._test_func(proc):
            return False
        self._count += 1
        self._cpu_percent += proc.cpu_percent()
        return True

    def flush(self):
        """Finish collection and send metrics."""
        _count_metric.set(self._count, fields=self._fields)
        self._count = 0
        _cpu_percent_metric.set(
            int(round(self._cpu_percent)), fields=self._fields
        )
        self._cpu_percent = 0


def _is_parent_autoserv(proc):
    """Return whether proc is a parent (not forked) autoserv process."""
    return _is_autoserv(proc) and not _is_autoserv(proc.parent())


def _is_autoserv(proc):
    """Return whether proc is an autoserv process."""
    # This relies on the autoserv script being run directly.  The script should
    # be named autoserv exactly and start with a shebang that is /usr/bin/python,
    # NOT /bin/env
    return _is_process_name("autoserv", proc)


def _is_python_module(module, proc):
    """Return whether proc is a process running a Python module."""
    cmdline = proc.cmdline()
    return (
        cmdline
        and cmdline[0].endswith("python")
        and cmdline[1:3] == ["-m", module]
    )


def _is_process_name(name, proc):
    """Return whether process proc is named name."""
    return proc.name() == name


def _is_swarming_bot(proc):
    """Return whether proc is a Swarming bot.

    A swarming bot process is like '/usr/bin/python3.8 <bot-zip-path> start_bot'.
    """
    cmdline = proc.cmdline()
    return (
        len(cmdline) == 3
        and cmdline[0].split("/")[-1].startswith("python")
        and cmdline[2] == "start_bot"
    )


def _is_gsutil(proc):
    """Return whether proc is gsutil."""
    cmdline = proc.cmdline()
    return (
        len(cmdline) >= 2
        and cmdline[0] == "python"
        and cmdline[1].endswith("gsutil")
    )


def _is_tko_proxy(proc):
    """Return whether proc is a tko proxy.

    A tk proxy process is like
    '/opt/cloud_sql_proxy -dir=<...>
        -instances=google.com:chromeos-lab:us-central1:tko
        -credential_file=<...>'.
    """
    cmdline = proc.cmdline()
    return (
        len(cmdline) == 4
        and cmdline[0].split("/")[-1] == 'cloud_sql_proxy'
        and cmdline[2] == '-instances=google.com:chromeos-lab:us-central1:tko'
    )
