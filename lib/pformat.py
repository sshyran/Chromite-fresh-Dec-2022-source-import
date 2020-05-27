# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Functions for formatting things in a human-readable format."""

import datetime
import sys


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


def timedelta(delta):
  """Returns a more human-readable version of the datetime.timedelta.

  Useful when printing durations >= 1 second in logs.

  Args:
    delta: A datetime.timedelta.

  Returns:
    Formatted string of the delta like '1d2h3m4.000s'.
  """
  if not isinstance(delta, datetime.timedelta):
    raise TypeError('delta must be of type datetime.timedelta')
  formated_delta = ''
  if delta.days:
    formated_delta = '%dd' % delta.days
  minutes, seconds = divmod(delta.seconds, 60)
  hours, minutes = divmod(minutes, 60)
  if hours > 0:
    formated_delta += '%dh' % hours
  if minutes > 0:
    formated_delta += '%dm' % minutes
  formated_delta += '%i.%03is' % (seconds, delta.microseconds // 1000)
  return formated_delta
