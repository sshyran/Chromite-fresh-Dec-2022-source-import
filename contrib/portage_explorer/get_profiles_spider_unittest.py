# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittest for the get_profiles_spider."""

from chromite.contrib.portage_explorer import get_profiles_spider
from chromite.contrib.portage_explorer import spider_testables
from chromite.contrib.portage_explorer import spiderlib


def test_execute(monkeypatch, tmp_path):
  """Test the get_profiles_spider's execute function.

  Ensure the get_profiles_spider is getting all the right profiles and
  connecting the profiles to the correct overlays and boards.
  """
  overlay_zork = spider_testables.create_overlays(tmp_path, 'zork')[1]
  test_brya, overlay_brya = spider_testables.create_overlays(tmp_path, 'brya')
  test_oak, overlay_oak = spider_testables.create_overlays(tmp_path, 'oak')
  test_brya_private, overlay_brya_private = spider_testables.create_overlays(
      tmp_path, 'brya-private')
  test_oak_private, overlay_oak_private = spider_testables.create_overlays(
      tmp_path, 'oak-private')
  brya_profiles = spider_testables.create_profiles(tmp_path, test_brya,
                                                   ['base', 'foo'])[1]
  oak_profiles = spider_testables.create_profiles(tmp_path, test_oak,
                                                  ['base'])[1]
  brya_private_profiles = spider_testables.create_profiles(tmp_path,
                                                           test_brya_private,
                                                           ['bar'])[1]
  oak_private_profiles = spider_testables.create_profiles(tmp_path,
                                                          test_oak_private,
                                                          ['base'])[1]
  build_target_brya = spiderlib.BuildTarget('brya')
  build_target_oak = spiderlib.BuildTarget('oak')
  test_output = spiderlib.SpiderOutput([build_target_brya, build_target_oak,],
                                       [overlay_zork, overlay_brya,
                                        overlay_oak,
                                        overlay_brya_private,
                                        overlay_oak_private,
                                        ])
  monkeypatch.setattr('chromite.lib.constants.SOURCE_ROOT', str(tmp_path))
  get_profiles_spider.execute(test_output)
  assert test_output.build_targets[0].profile == brya_profiles['base']
  assert test_output.build_targets[1].profile == oak_private_profiles['base']
  assert test_output.overlays[0].profiles == []
  assert test_output.overlays[1].profiles == [brya_profiles['base'],
                                              brya_profiles['foo'],
                                              ]
  assert test_output.overlays[2].profiles == [oak_profiles['base']]
  assert test_output.overlays[3].profiles == [brya_private_profiles['bar']]
  assert test_output.overlays[4].profiles == [oak_private_profiles['base']]
