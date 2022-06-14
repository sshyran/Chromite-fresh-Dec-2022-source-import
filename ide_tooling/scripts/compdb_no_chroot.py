#!/usr/bin/env python3
# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Converts compilation database to work outside chroot.

Gets a compilation database generated inside chroot from stdin and outputs the
one that works outside chroot to stdout. This script is used from
platform.eclass.
"""

import json
import os
import re
import sys


# Generate non-chroot version of the DB with the following
# changes:
#
# 1. translate file and directory paths
# 2. call clang directly instead of using CrOS wrappers
# 3. use standard clang target triples
# 4. remove a few compiler options that might not be available
#    in the potentially older clang version outside the chroot
def update_value(value: str, external_trunk_path):
  external_chroot_path = f'{external_trunk_path}/chroot'

  value = re.sub(r'(\.\./|\.\.)*/mnt/host/source/', f'{external_trunk_path}/',
                 value)
  value = re.sub(r'/build/(\S*)', f'{external_chroot_path}/build/\\1', value)
  value = re.sub(r'-isystem /', f'-isystem {external_chroot_path}/', value)
  value = re.sub(r'[a-z0-9_]+-(cros|pc)-linux-gnu([a-z]*)?-clang', 'clang',
                 value)
  # TODO(oka): Cover this logic with unit test.
  for x in [r'\b-fdebug-info-for-profiling\b', r'\b-mretpoline\b',
            r'\b-mretpoline-external-thunk\b', r'\b-mfentry\b']:
    value = re.sub(x, '', value)

  return value

def generate(data, external_trunk_path):
  out = []
  for x in data:
    updated = {}
    for key, value in x.items():
      updated[key] = update_value(value, external_trunk_path)
    # Add "-stdlib=libc++" so that the clang outside the chroot can
    # find built-in headers like <string> and <memory>
    updated['command'] += ' -stdlib=libc++'
    out.append(updated)
  return out

def main():
  data = json.load(sys.stdin)
  external_trunk_path = sys.argv[1]
  if not os.path.exists(external_trunk_path):
    raise Exception(f'{external_trunk_path} should be trunk path')
  json.dump(generate(data, sys.argv[1]), sys.stdout)

if __name__ == '__main__':
  main()
