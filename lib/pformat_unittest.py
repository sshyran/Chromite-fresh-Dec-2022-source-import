# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test suite for pprint.py"""

import datetime
import sys

from chromite.lib import cros_test_lib
from chromite.lib import pformat


assert sys.version_info >= (3, 6), 'This module requires Python 3.6+'


class TestPPrintTimedelta(cros_test_lib.TestCase):
  """Tests PPrintTimedelta."""

  def testDays(self):
    delta = datetime.timedelta(days=1, hours=2, minutes=3, seconds=4)
    pretty_delta = pformat.timedelta(delta)
    self.assertEqual(pretty_delta, '1d2h3m4.000s')

  def testSeconds(self):
    delta = datetime.timedelta(seconds=12, microseconds=345678)
    pretty_delta = pformat.timedelta(delta)
    self.assertEqual(pretty_delta, '12.345s')

  def testManySeconds(self):
    delta = datetime.timedelta(seconds=200000)
    pretty_delta = pformat.timedelta(delta)
    self.assertEqual(pretty_delta, '2d7h33m20.000s')

  def testOnlyDaysAndSeconds(self):
    delta = datetime.timedelta(days=1, seconds=23)
    pretty_delta = pformat.timedelta(delta)
    self.assertEqual(pretty_delta, '1d23.000s')
