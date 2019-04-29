# -*- coding: utf-8 -*-path + os.sep)
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for the dependency.py module."""

from __future__ import print_function

from chromite.lib import constants
from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.service import dependency

import os
from os.path import join


class DependencyTests(cros_test_lib.TestCase):
  """General unittests for dependency module."""

  def testNormalizeSourcePathsCollapsingSubPaths(self):
    self.assertEquals(
        dependency.NormalizeSourcePaths(
            ['/mnt/host/source/foo', '/mnt/host/source/ab/cd',
             '/mnt/host/source/foo/bar']),
        ['ab/cd', 'foo'])

    self.assertEquals(
        dependency.NormalizeSourcePaths(
            ['/mnt/host/source/foo/bar',
             '/mnt/host/source/ab/cd',
             '/mnt/host/source/foo/bar/..',
             '/mnt/host/source/ab/cde']),
        ['ab/cd', 'ab/cde', 'foo'])

  def testNormalizeSourcePathsFormatingDirectoryPaths(self):
    with osutils.TempDir() as tempdir:
      foo_dir = join(tempdir, 'foo')
      bar_baz_dir = join(tempdir, 'bar', 'baz')
      osutils.SafeMakedirs(join(tempdir, 'ab'))
      ab_cd_file = join(tempdir, 'ab', 'cd')

      osutils.SafeMakedirs(foo_dir)
      osutils.SafeMakedirs(bar_baz_dir)
      osutils.WriteFile(ab_cd_file, 'alphabet')


      expected_paths = [ab_cd_file, bar_baz_dir + '/', foo_dir + '/']
      expected_paths = [os.path.relpath(p, constants.CHROOT_SOURCE_ROOT) for
                        p in expected_paths]

      self.assertEquals(
          dependency.NormalizeSourcePaths([foo_dir, ab_cd_file, bar_baz_dir]),
          expected_paths)
