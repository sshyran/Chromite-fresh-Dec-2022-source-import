# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Determines all Chrome OS packages that are marked as `hot`.

Dumps results as a list of package names to a JSON file. Hotness is
determined by statically analyzing an ebuild.

Primarily intended for use by the Chrome OS toolchain team.
"""

import json
import logging
from pathlib import Path
from typing import Iterable, List, Tuple

from chromite.lib import commandline
from chromite.lib import portage_util


def contains_ebuild_hot_marker(file_path: Path):
  """Returns whether a file seems to be marked as hot."""
  ebuild_contents = file_path.read_text(encoding='utf-8')
  return 'cros_optimize_package_for_speed' in ebuild_contents


def locate_all_package_ebuilds(
    overlays: Iterable[Path]) -> Iterable[Tuple[Path, str, List[Path]]]:
  """Determines package -> ebuild mappings for all packages.

  Yields a series of (package_path, package_name, [path_to_ebuilds]). This may
  yield the same package name multiple times if it's available in multiple
  overlays.
  """
  for overlay in overlays:
    # Note that portage_util.GetOverlayEBuilds can't be used here, since that
    # specifically only searches for cros_workon candidates. We care about
    # everything we can possibly build.
    for package_dir in overlay.glob('*/*'):
      ebuilds = list(package_dir.glob('*.ebuild'))
      if ebuilds:
        package_name = f'{package_dir.parent.name}/{package_dir.name}'
        yield package_dir, package_name, ebuilds


def locate_all_hot_env_packages(overlays: Iterable[Path]) -> Iterable[str]:
  """Yields packages marked hot by files in chromeos/config/env."""
  for overlay in overlays:
    env_dir = overlay / 'chromeos' / 'config' / 'env'
    for f in env_dir.glob('*/*'):
      if f.is_file() and contains_ebuild_hot_marker(f):
        yield f'{f.parent.name}/{f.name}'


def main(argv: List[str]):
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument('--output', required=True, type=Path)
  opts = parser.parse_args(argv)

  ebuilds_found = 0
  packages_found = 0
  merged_packages = 0

  overlays = portage_util.FindOverlays(overlay_type='both')
  logging.debug('Found overlays %s', overlays)
  overlays = [Path(x) for x in overlays]

  mappings = {x: True for x in locate_all_hot_env_packages(overlays)}
  logging.debug('Found hot packages %r from env search', sorted(mappings))
  for package_dir, package, ebuilds in locate_all_package_ebuilds(overlays):
    packages_found += 1
    ebuilds_found += len(ebuilds)
    logging.debug('Found package %r in %r with ebuilds %r', package,
                  package_dir, ebuilds)

    is_marked_hot = any(contains_ebuild_hot_marker(x) for x in ebuilds)
    if is_marked_hot:
      logging.debug('Package is marked as hot')
    else:
      logging.debug('Package is not marked as hot')

    if package in mappings:
      logging.warning('Multiple entries found for package %r; merging', package)
      merged_packages += 1
      mappings[package] = is_marked_hot or mappings[package]
    else:
      mappings[package] = is_marked_hot

  hot_packages = sorted(
      package for package, is_hot in mappings.items() if is_hot)

  logging.info('%d ebuilds found', ebuilds_found)
  logging.info('%d packages found', packages_found)
  logging.info('%d packages merged', merged_packages)
  logging.info('%d hot packages found, total', len(hot_packages))

  opts.output.write_text(json.dumps(hot_packages), encoding='utf-8')
