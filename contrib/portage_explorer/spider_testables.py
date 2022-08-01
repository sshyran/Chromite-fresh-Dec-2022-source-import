# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Utilities for testing spiders in portage_explorer."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import chromite as cr
from chromite.contrib.portage_explorer import spiderlib


def create_overlays(tmp_path: Path, name: str) -> Tuple[cr.test.Overlay,
                                                        spiderlib.Overlay]:
  """Create test overlays for unittesting spiders.

  Create the cr.test.Overlay and spiderlib.Overlay versions of the overlays to
  replicate in the temporary path.

  Args:
    tmp_path: Temporary path to put mock data in
    name: Name of overlay

  Returns:
    A tuple containing the cr.test.Overlay and spiderlib.Overlay version of the
    overlay
  """
  overlay_path = tmp_path / f'src/overlay-{name}'
  test_overlay = cr.test.Overlay(overlay_path, name)
  spider_overlay = spiderlib.Overlay(overlay_path.relative_to(tmp_path), name)
  return (test_overlay, spider_overlay)


def create_profiles(
    tmp_path: Path, test_overlay: cr.test.Overlay,
    profile_names: List[str],
    parent_profiles: Optional[Dict[str, cr.test.Profile]] = None,
    make_defaults: Optional[Dict[str, Dict[str, str]]] = None
    ) -> Tuple[Dict[str, cr.test.Profile], Dict[str, spiderlib.Profile],
               Dict[str, spiderlib.Profile]]:
  """Create test profiles for unittesting spiders.

  Create the unpopulated and populated versions of the profiles for the overlay
  to represent the before and after of running the spider against the mock data.

  Args:
    tmp_path: Temporary path to put mock data in
    test_overlay: cr.test.Overlay instance to create a profile within
    profile_names: List of strings representing profile names for this overlay
    parent_profiles: Dict of profile names matched to corresponding
        portage_testables profile.
    make_defaults: Dict of profile names matched to corresponding make_defaults
        from portage_testables when creating profiles, which is a dict of the
        variable and its value.

  Returns:
    A tuple containing the cr.test.Profiles, the profiles to run through the
    spider, and the profiles to compare the the output against
  """
  test_profiles = {}
  unpopulated_profiles = {}
  populated_profiles = {}
  if not parent_profiles:
    parent_profiles = {}
  if not make_defaults:
    make_defaults = {}
  for profile_name in profile_names:
    test_profile = test_overlay.create_profile(
        Path(profile_name),
        profile_parents=parent_profiles.get(profile_name, []),
        make_defaults=make_defaults.get(profile_name, {}))
    test_profiles[profile_name] = test_profile
    unpopulated_spider_profile = spiderlib.Profile(
        f'{test_profile.overlay}:{profile_name}',
        test_profile.full_path.relative_to(tmp_path), profile_name)
    unpopulated_profiles[profile_name] = unpopulated_spider_profile
    populated_spider_profile = spiderlib.Profile(
        f'{test_profile.overlay}:{profile_name}',
        test_profile.full_path.relative_to(tmp_path), profile_name)
    for parent in parent_profiles.get(profile_name, []):
      populated_spider_profile.parent_profiles.append(
          f'{parent.overlay}:{parent.path}')
    spider_flags = []
    for flag in make_defaults.get(profile_name, {}).get('USE', '').split():
      flag_name = flag.strip('-')
      spider_use = spiderlib.ProfileUse(
          flag_name, spiderlib.UseState(not flag.startswith('-')))
      spider_flags.append(spider_use)
    populated_spider_profile.use_flags = sorted(
        spider_flags, key=lambda use_flag: use_flag.name)
    populated_profiles[profile_name] = populated_spider_profile
  return (test_profiles, unpopulated_profiles, populated_profiles)
