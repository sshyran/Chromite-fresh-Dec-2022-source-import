#!/usr/bin/env python3
# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for compdb_no_chroot.py.
"""

import json
import os
import sys

import compdb_no_chroot


sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..'))
# pylint: disable=wrong-import-position
from chromite.lib import cros_test_lib


# pylint: enable=wrong-import-position


EXT_TRUNK_PATH = '/usr/local/google/home/oka/os2'

class GenerateTest(cros_test_lib.TestCase):
  """Tests generate()"""

  def testAll(self):
    testdata = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'compdb_no_chroot_testdata')
    input_dir = os.path.join(testdata, 'input')
    expected_dir = os.path.join(testdata, 'expected')
    for name in os.listdir(input_dir):
      given = json.load(open(os.path.join(input_dir, name)))
      expected = json.load(open(os.path.join(expected_dir, name)))

      got = compdb_no_chroot.generate(given, EXT_TRUNK_PATH)
      self.assertEqual(got, expected)

if __name__ == '__main__':
  cros_test_lib.main(module=__name__)
