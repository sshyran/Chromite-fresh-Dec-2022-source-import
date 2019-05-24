# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Parser for Portage elog summary.log files

The summary.log file is created by Portage at ${PORT_LOGDIR}/elog/summary.log
and appended to by every run of `emerge`. Any package that emits information
via the `elog` system will have an entry in the summary log, even those with
fatal errors.

The `ebuild` command and invocations of `emerge` with --pretend will *NOT*
generate entries in the summary.log file.

Documentation for the Portage log system can be found at:
https://wiki.gentoo.org/wiki/Portage_log
"""
from __future__ import absolute_import
from __future__ import print_function

import re
from collections import defaultdict

import six

from chromite.lib import portage_util

SECTION_HEADER = re.compile(
    r'>>> Messages generated by process (?P<process>\d+) on (?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w{3}) for package (?P<package>[^:]+):'  #pylint: disable=line-too-long
)

LOG_ENTRY = re.compile(
    r'(?P<level>INFO|WARN|LOG|ERROR|QA): (?P<phase>setup|unpack|prepare|configure|compile|test|install|preinst|postinst)'  #pylint: disable=line-too-long
)


class Error(Exception):
  """Base exception type for this parser"""


class MalformedLogError(Error):
  """Error indicating a parsed log has unexpected structure"""


class DuplicatePackageError(Error):
  """Error indicating that duplicate packages were found in a summary.log"""


class SummaryLog(object):
  """Parsed contents of a summary.log file"""

  def __init__(self, log_contents):
    self.package_logs = sorted(
        PackageLog(cpv, logs) for cpv, logs in six.iteritems(log_contents))

  def has_failed_packages(self):
    return any(log.has_errors() for log in self.package_logs)

  def failed_packages(self):
    return sorted(log.cp for log in self.package_logs if log.has_errors())

  def has_warned_packages(self):
    return any(log.has_warnings() for log in self.package_logs)

  def warned_packages(self):
    return sorted(log.cp for log in self.package_logs if log.has_warnings())

  @staticmethod
  def parse_from_file(file_path):
    with open(file_path) as logfile:
      return _parse_summary_log_from_lines_iterator(logfile)

  @staticmethod
  def parse_from_string(string):
    return _parse_summary_log_from_lines_iterator(string.splitlines(True))


class PackageLog(object):
  """Parsed contents of a single package's entry from a summary.log"""

  def __init__(self, cpv, log_mapping):
    self.cpv = cpv
    self.log_levels = dict((k, dict(v)) for k, v in six.iteritems(log_mapping))

  @property
  def cp(self):
    return self.cpv.cp

  def has_errors(self):
    return "ERROR" in self.log_levels

  def has_warnings(self):
    return "WARN" in self.log_levels


def _parse_summary_log_from_lines_iterator(log_lines, no_duplicates=False):
  cpv = None
  level = None
  phase = None

  # A mapping of package cpv -> log level -> ebuild phase -> messages
  # Ex: contents["app-editor/vim"]["ERROR"]["compile"] -> "something happened"
  contents = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

  for line in log_lines:
    # Skip over blank lines
    if not line.strip():
      continue

    # Update the state once we're in a log section for a particular package
    # If we encounter the same package twice that means the log has entries
    # from a previous attempt.
    header_match = SECTION_HEADER.match(line.strip())
    if header_match:
      cpv = portage_util.SplitCPV(header_match.group('package'))
      if cpv in contents and no_duplicates:
        raise DuplicatePackageError()
      continue

    # Match the ebuild phase and log entry. If we don't have a package set yet,
    # then the log we're reading is malformed.
    entry_match = LOG_ENTRY.match(line.strip())
    if entry_match:
      if not cpv:
        raise MalformedLogError()
      phase = entry_match.group('phase')
      level = entry_match.group('level')
      continue

    # All other lines are then the actual messages printed by ebuilds. Append
    # them to their respective categories. If anything is unset by this point,
    # the log is again malformed.
    if not all((cpv, phase, level)):
      raise MalformedLogError()
    contents[cpv][level][phase] += line

  return SummaryLog(contents)
