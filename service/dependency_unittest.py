# -*- coding: utf-8 -*-path + os.sep)
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for the dependency.py module."""

from __future__ import print_function

from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import cros_test_lib
from chromite.service import dependency

pytestmark = cros_test_lib.pytestmark_inside_only


class DependencyTests(cros_test_lib.MockTestCase):
  """General unittests for dependency module."""

  def setUp(self):
    self.json_deps = {
        'target_board': 'deathstar',
        'sysroot_path': '/build/deathstar',
        'package_deps': {
            'commander/darthvader-1.49.3.3': {
                'action': 'merge',
                'category': 'commander',
                'cpes': [],
                'deps': ['troop/clone', 'troop/robot'],
                'rev_deps': [],
                'full_name': 'commander/darthvader-1.49.3.3',
                'name': 'darthvader',
                'version': '1.49.3.3'
            },
            'troop/clone-1.2.3': {
                'action': 'merge',
                'category': 'troop',
                'cpes': [],
                'deps': ['equipment/jetpack'],
                'rev_deps': ['commander/darthvader'],
                'full_name': 'troop/clone-1.2.3',
                'name': 'clone',
                'version': '1.2.3'
            },
            'troop/robot-2.3.4': {
                'action': 'merge',
                'category': 'troop',
                'cpes': [],
                'deps': [],
                'rev_deps': ['commander/darthvader'],
                'full_name': 'troop/robot-2.3.4',
                'name': 'robot',
                'version': '2.3.4'
            },
            'equipment/jetpack-3.4.5': {
                'action': 'merge',
                'category': 'equipment',
                'cpes': [],
                'deps': [],
                'rev_deps': ['commander/darthvader'],
                'full_name': 'equipment/jetpack-3.4.5',
                'name': 'jetpack',
                'version': '3.4.5'
            },
        },
        'source_path_mapping': {
            'commander/darthvader-1.49.3.3': ['/control/room'],
            'troop/clone-1.2.3': ['/bunker'],
            'troop/robot-2.3.4': ['/factory'],
            'equipment/jetpack-3.4.5': ['/factory'],
        },
    }

  def testDeterminePackageRelevanceNotRelevant(self):
    """Test determine_package_relevance with no matching paths."""
    src_paths = ['foo/bar/baz', 'foo/bar/b', 'foo/bar', 'bar/foo']
    dep_src_paths = ['foo/bar/ba']
    self.assertFalse(
        dependency.determine_package_relevance(dep_src_paths, src_paths))

  def testDeterminePackageRelevanceExactMatch(self):
    """Test determine_package_relevance given an exact match."""
    src_paths = ['foo/bar/baz']
    dep_src_paths = ['foo/bar/baz']
    self.assertTrue(
        dependency.determine_package_relevance(dep_src_paths, src_paths))

  def testDeterminePackageRelevanceDirectoryMatch(self):
    """Test determine_package_relevance given a directory match."""
    src_paths = ['foo/bar/baz']
    dep_src_paths = ['foo/bar']
    self.assertTrue(
        dependency.determine_package_relevance(dep_src_paths, src_paths))

  def testGetDependenciesWithDefaultArgs(self):
    """Test GetDependencies using the default args."""
    self.PatchObject(
        dependency,
        'GetBuildDependency',
        return_value=(self.json_deps, self.json_deps))
    sysroot_path = '/build/deathstar'
    build_target = common_pb2.BuildTarget(name='target')
    actual_deps = dependency.GetDependencies(sysroot_path, build_target)
    expected_deps = [
        'commander/darthvader-1.49.3.3',
        'troop/clone-1.2.3',
        'troop/robot-2.3.4',
        'equipment/jetpack-3.4.5',
    ]
    self.assertCountEqual(expected_deps, actual_deps)

  def testGetDependenciesWithSrcPaths(self):
    """Test GetDependencies given a list of paths."""
    self.PatchObject(
        dependency,
        'GetBuildDependency',
        return_value=(self.json_deps, self.json_deps))
    sysroot_path = '/build/deathstar'
    build_target = common_pb2.BuildTarget(name='target')
    src_paths = ['/bunker', '/nowhere']
    actual_deps = dependency.GetDependencies(sysroot_path, build_target,
                                             src_paths)
    expected_deps = ['troop/clone-1.2.3']
    self.assertCountEqual(expected_deps, actual_deps)
