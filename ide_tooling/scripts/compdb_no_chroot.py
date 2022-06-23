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
from typing import Optional


class Converter:
  """Converts compilation database to work outside chroot"""
  def __init__(self, external_trunk_path: str):
    self.external_trunk_path = external_trunk_path
    self.external_chroot_path = os.path.join(external_trunk_path, 'chroot')

  def convert_filepath(self, filepath: str) -> str:
    # If out-of-tree build is enabled, source files under /mnt/host/source are
    # used. This directory is inaccessible outside chroot, so we convert it.
    m = re.fullmatch(r'(\.\.(/\.\.)*)?/mnt/host/source/(.*)', filepath)
    if m:
      return os.path.join(self.external_trunk_path, m[3])

    # If out-of-tree build is disabled, source files are copied in a temporary
    # directory, and the filepath may point to the copied file. We convert this
    # so that code navigation doesn't jump to the file in chroot.
    # We use a heuristic (using /platform2/ as a marker) here to support
    # platform2 packages.
    # TODO(oka): Revisit this logic to support packages outside platform2.
    m = re.fullmatch(r'.*/platform2(/.*)?', filepath)
    if m:
      platform2 = os.path.join(self.external_trunk_path, 'src/platform2')
      if m[1]:
        return os.path.join(platform2, m[1][1:])
      return platform2

    if filepath.startswith('/'):
      return os.path.join(self.external_chroot_path, filepath[1:])

    return filepath

  def convert_clang_option_value(self, value: str) -> str:
    if '/' in value:
      return self.convert_filepath(value)
    return value

  def convert_clang_option(self, option: str) -> Optional[str]:
    if not option.startswith('-'):
      return self.convert_clang_option_value(option)

    # Convert flag value
    if option.startswith('-I'):
      return '-I' + self.convert_filepath(option[2:])

    # Remove a few compiler options that might not be available in the
    # potentially older clang version outside the chroot.
    # TODO(oka): Cover this logic with unit test.
    if option in ['-fdebug-info-for-profiling', '-mretpoline',
                  '-mretpoline-external-thunk', '-mfentry']:
      return None

    if '=' in option:
      flag, value = option.split('=', 2)
      return flag + '=' + self.convert_clang_option_value(value)

    if '/' in option:
      raise Exception(f'Unknown flag that suffixes a filepath: {option}')
    return option

  def convert_command(self, command: str) -> str:
    exe, *options = command.split(' ')

    # We should call clang directly instead of using CrOS wrappers.
    converted_exe: str
    for x in ['clang', 'clang++']:
      if exe.endswith(x):
        converted_exe = x
        break
    if not converted_exe:
      raise Exception(f'Unexpected executable name: {exe}')

    converted_options = []
    if re.match(r'^(aarch64|arm)', exe):
      converted_options.append('--target=arm')
    for option in options:
      converted_option = self.convert_clang_option(option)
      if converted_option:
        converted_options.append(converted_option)

    # Add "-stdlib=libc++" so that the clang outside the chroot can
    # find built-in headers like <string> and <memory>
    converted_options.append('-stdlib=libc++')

    return converted_exe + ' ' + ' '.join(converted_options)

def generate(data, external_trunk_path):
  """Generates non-chroot version of the compilation database"""

  converter = Converter(external_trunk_path)

  converted = []
  for x in data:
    directory = x['directory']
    command = x['command']
    filepath = x['file']
    output = x['output']

    converted.append({
        'directory': converter.convert_filepath(directory),
        'command': converter.convert_command(command),
        'file': converter.convert_filepath(filepath),
        'output': converter.convert_filepath(output),
    })
  return converted

def main():
  data = json.load(sys.stdin)
  external_trunk_path = sys.argv[1]
  if not os.path.exists(external_trunk_path):
    raise Exception(f'{external_trunk_path} should be trunk path')
  json.dump(generate(data, sys.argv[1]), sys.stdout, indent=2)

if __name__ == '__main__':
  main()
