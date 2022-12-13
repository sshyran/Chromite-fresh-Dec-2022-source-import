# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittest for the get_profile_inheritance_spider."""

from chromite.contrib.portage_explorer import get_profile_inheritance_spider
from chromite.contrib.portage_explorer import spider_testables
from chromite.contrib.portage_explorer import spiderlib


def test_execute(monkeypatch, tmp_path):
  """Test the get_profile_inheritance_spider's execute function.

  Ensure the profiles have the right parents in the right order.
  """
  test_oak, overlay_oak = spider_testables.create_overlays(tmp_path, 'oak')
  test_oak_private, overlay_oak_private = spider_testables.create_overlays(
      tmp_path, 'oak-private')
  (test_oak_private_profiles, oak_private_profiles,
   oak_private_profiles_parents) = spider_testables.create_profiles(
       tmp_path, test_oak_private, ['base', 'foo', 'bar'])
  (test_oak_profiles, oak_profiles,
   oak_profiles_parents) = spider_testables.create_profiles(
       tmp_path, test_oak, ['base'], {
           'base': [
               test_oak_private_profiles['foo'],
               test_oak_private_profiles['base'],
           ]
       })
  parent_file = (test_oak_profiles['base'].full_path / 'parent').open('a')
  parent_file.write('oak-private:bar # oak-private:baz\n# oak-private:baz\n ')
  parent_file.close()
  oak_profiles_parents['base'].parent_profiles.append('oak-private:bar')
  overlay_oak_private.profiles = [
      oak_private_profiles['base'],
      oak_private_profiles['foo'],
      oak_private_profiles['bar'],
  ]
  overlay_oak.profiles = [
      oak_profiles['base'],
  ]
  test_output = spiderlib.SpiderOutput([], [
      overlay_oak,
      overlay_oak_private,
  ])
  monkeypatch.setattr('chromite.lib.constants.SOURCE_ROOT', str(tmp_path))
  get_profile_inheritance_spider.execute(test_output)
  assert test_output.build_targets == []
  assert test_output.overlays[0].profiles == [
      oak_profiles_parents['base'],
  ]
  assert test_output.overlays[1].profiles == [
      oak_private_profiles_parents['base'],
      oak_private_profiles_parents['foo'],
      oak_private_profiles_parents['bar'],
  ]
