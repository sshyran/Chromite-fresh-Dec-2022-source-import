# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests for timer."""

import time

from chromite.utils import pformat
from chromite.utils import timer


def test_timer_delta(monkeypatch):
  """Test basic usage of a Timer."""
  last_t = 0.0

  def time_mock():
    nonlocal last_t
    last_t += 1.0
    return last_t

  monkeypatch.setattr(time, 'perf_counter', time_mock)

  with timer.timer() as t:
    pass

  assert t.delta == 1.0


def test_timer_average(monkeypatch):
  """Test the timer __add__ and __truediv__ functions."""
  last_t = 0.0

  def time_mock():
    nonlocal last_t
    last_t += 1.0
    return last_t

  monkeypatch.setattr(time, 'perf_counter', time_mock)

  timers = []
  for x in range(10):
    with timer.Timer(str(x)) as t:
      pass
    timers.append(t)

  assert sum(timers, start=timer.Timer()).delta == 10.0
  assert (sum(timers, start=timer.Timer()) / len(timers)).delta == 1.0


def test_timer_decorator(monkeypatch):
  """Test the timed decorator."""
  delta = '1s'
  name = 'name'
  output_fn_called = False

  # monkeypatch the timedelta formatter to return the expected delta.
  def timedelta_mock(*_args, **_kwargs):
    return delta

  monkeypatch.setattr(pformat, 'timedelta', timedelta_mock)

  # Output function to check the value.
  def output_fn(value):
    nonlocal output_fn_called
    output_fn_called = True
    assert value == f'{name}: {delta}'

  # The decorated function.
  @timer.timed(name, output_fn)
  def timed_fn():
    pass

  # Run the function to trigger the test.
  timed_fn()

  assert output_fn_called
