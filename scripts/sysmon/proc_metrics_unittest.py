# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for proc_metrics."""

# pylint: disable=protected-access

from __future__ import absolute_import

from unittest import mock

import psutil  # pylint: disable=import-error

from chromite.lib import cros_test_lib
from chromite.scripts.sysmon import proc_metrics


def _mock_process(name, cmdline, parent=None):
    proc = mock.Mock(dir(psutil.Process))
    proc.name.return_value = name
    proc.cmdline.return_value = cmdline
    proc.cpu_percent.return_value = 2
    if parent is not None:
        proc.parent.return_value = parent
    return proc


def _mock_forked_process(name, cmdline):
    parent_proc = _mock_process(name, cmdline)
    return _mock_process(name, cmdline, parent=parent_proc)


def _expected_calls_for(name):
    """Return expected calls for a process metric."""
    return [
        mock.call("proc/count", (name,), None, 1, enforce_ge=mock.ANY),
        mock.call("proc/cpu_percent", (name,), None, 2, enforce_ge=mock.ANY),
    ]


class TestProcMetrics(cros_test_lib.TestCase):
    """Tests for proc_metrics."""

    def setUp(self):
        patcher = mock.patch(
            "chromite.third_party.infra_libs.ts_mon.common.interface.state.store",
            autospec=True,
        )
        self.store = patcher.start()
        self.addCleanup(patcher.stop)

    def test_collect(self):
        with mock.patch("psutil.process_iter", autospec=True) as process_iter:
            process_iter.return_value = [
                _mock_process(
                    name="autoserv",
                    cmdline=[
                        "/usr/bin/python",
                        "-u",
                        "/usr/local/autotest/server/autoserv",
                        "-p",
                        "-r",
                        (
                            "/usr/local/autotest/results/hosts/"
                            "chromeos4-row3-rack13-host9/646252-provision"
                            "/20171307125911"
                        ),
                        "-m",
                        "chromeos4-row3-rack13-host9",
                        "--verbose",
                        "--lab",
                        "True",
                        "--provision",
                        "--job-labels",
                        "cros-version:winky-release/R61-9741.0.0",
                    ],
                ),
                _mock_forked_process(
                    name="autoserv",
                    cmdline=[
                        "/usr/bin/python",
                        "-u",
                        "/usr/local/autotest/server/autoserv",
                        "-p",
                        "-r",
                        (
                            "/usr/local/autotest/results/hosts/"
                            "chromeos4-row3-rack13-host9/646252-provision"
                            "/20171307125911"
                        ),
                        "-m",
                        "chromeos4-row3-rack13-host9",
                        "--verbose",
                        "--lab",
                        "True",
                        "--provision",
                        "--job-labels",
                        "cros-version:winky-release/R61-9741.0.0",
                    ],
                ),
                _mock_process(
                    name="gs_offloader.py",
                    cmdline=[
                        "/usr/bin/python",
                        "/usr/local/autotest/site_utils/gs_offloader.py",
                        "-s",
                        "--parallelism=30",
                    ],
                ),
                _mock_process(
                    name="python",
                    cmdline=[
                        (
                            "/usr/local/google/home/chromeos-test/.cache/cros_venv"
                            "/venv-2.7.6-5addca6cf590166d7b70e22a95bea4a0"
                            "/bin/python"
                        ),
                        "-m",
                        "chromite.scripts.sysmon",
                        "--interval",
                        "60",
                    ],
                ),
                _mock_process(
                    name="lxc-start",
                    cmdline=[
                        "[lxc monitor] /usr/local/autotest/containers"
                        " test_196499100_1525673902_240543]"
                    ],
                ),
                _mock_process(
                    name="lxc-attach",
                    cmdline=[
                        "lxc-attach",
                        "-P",
                        "/usr/local/autotest/containers",
                        "-n",
                        "test_196499100_1525673902_240543",
                        "--",
                        "bash",
                        "-c",
                        (
                            "/usr/local/autotest/server/autoserv"
                            " -s -P 196499100-chromeos-test/group0 ..."
                        ),
                    ],
                ),
                _mock_process(
                    name="getty",
                    cmdline=[
                        "/sbin/getty",
                        "-8",
                        "38400",
                        "console",
                    ],
                ),
                _mock_process(
                    name="sshd", cmdline=["sshd:", "chromeos-test", "[priv]"]
                ),
                _mock_process(
                    name="python3.8",
                    cmdline=[
                        "/usr/bin/python3.8",
                        "/home/chromeos-test/skylab_bots/"
                        "c6-r16-r17-h13.2757785382/swarming_bot.1.zip",
                        "start_bot",
                    ],
                ),
                _mock_process(
                    name="curl", cmdline=["curl", "server:port/path"]
                ),
                _mock_process(
                    name="python",
                    cmdline=[
                        "python",
                        "-m",
                        "gs_archive_server",
                        "-p",
                        "18000",
                        "-c",
                        "127.0.0.1:8082",
                    ],
                ),
                _mock_process(name="java", cmdline=["java", "-Xmx4g", "..."]),
                _mock_process(
                    name="python",
                    cmdline=[
                        "python",
                        "/tmp/chromeos-cache/common/gsutil_4.57.tar.gz/"
                        "gsutil/gsutil",
                        "-o",
                        "Boto:num_retries=10",
                        "cat",
                        "gs://eve-release/R100-14488.0.0/file",
                    ],
                ),
            ]
            proc_metrics.collect_proc_info()

        setter = self.store.set
        calls = []
        calls.extend(_expected_calls_for("autoserv"))
        calls.extend(_expected_calls_for("curl"))
        calls.extend(_expected_calls_for("getty"))
        calls.extend(_expected_calls_for("gs_archive_server"))
        calls.extend(_expected_calls_for("gs_offloader"))
        calls.extend(_expected_calls_for("gsutil"))
        calls.extend(_expected_calls_for("java"))
        calls.extend(_expected_calls_for("lxc-attach"))
        calls.extend(_expected_calls_for("lxc-start"))
        calls.extend(_expected_calls_for("sshd"))
        calls.extend(_expected_calls_for("swarming_bot"))
        calls.extend(_expected_calls_for("sysmon"))
        calls.extend(_expected_calls_for("other"))
        setter.assert_has_calls(calls)
        self.assertEqual(len(setter.mock_calls), len(calls))
