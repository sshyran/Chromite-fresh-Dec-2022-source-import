# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run upstart-specific lint checks on the specified .conf files."""

# TODO(b/222119485) build out additional features:
#  * a flag for build mode when some lints are ignored
#  * Additional checks:
#    + require 'oom score'
#    + no \r characters
#    + no trailing whitespace on lines
#    + no leading blank lines
#    + no trailing blank lines
#    + require trailing newline

import functools
import json
import logging
from pathlib import Path
import os
import re
from typing import Dict, Generator, List


AUDITED_SHELL_COMMAND_REGEX = re.compile(
    # Match comment lines so they can be excluded.
    r'(?P<comment>^\s*#.*$)|'
    # Match common command delimiters.
    r'(?:^\s*|;|&&|[|][|]|(?P<prefix>(?:[$][(]|`)+)\s*)'
    # Match command name.
    r'\b(?P<command>chown|chgrp|chmod|mkdir|ln|rm|mv|cp|touch)\s+'
    # Match command args across line splits.
    r'(?P<args>(?:\\\n|[^\n;])*)',
    re.MULTILINE)
SHELL_TOKEN_SPLIT_REGEX = re.compile(r'(?:\\\n|\s)+', re.MULTILINE)
IGNORE_LINT_REGEX = re.compile(r'#\s+croslint:\s+disable')

# TODO(python3.9): Change to functools.cache.
@functools.lru_cache(maxsize=None)
def GetIgnoreLookup() -> Dict[str, List[str]]:
  """Returns the lookup table of upstart config lines to ignore.

  On first invocation this loads the list from upstart_exceptions.json.
  Otherwise the cached copy is used.

  This is intended to be removed once the call sites are either migrated to
  tmpfiles.d or have '# croslint: disable' added.
  """
  FILE = Path(__file__).resolve()
  exceptions_path = FILE.parent / 'upstart_exceptions.json'
  with exceptions_path.open('rb') as fp:
    return json.load(fp)


def ExtractCommands(text: str) -> Generator[List[str], None, None]:
  """Finds and normalizes audited commands."""
  for match in AUDITED_SHELL_COMMAND_REGEX.finditer(text, re.S):
    # Skip comments.
    if match.group('comment'):
      continue

    cmd_prefix = match.group('prefix')
    cmd_name = match.group('command')
    cmd_args = match.group('args')

    # Skip if 'croslint: disable' is set.
    if IGNORE_LINT_REGEX.search(cmd_args):
      continue

    if cmd_prefix:
      cmd = [SHELL_TOKEN_SPLIT_REGEX.sub(cmd_prefix, ' ') + cmd_name]
    else:
      cmd = [cmd_name]
    cmd.extend(x for x in SHELL_TOKEN_SPLIT_REGEX.split(cmd_args) if x)
    yield cmd


def CheckForRequiredLines(text: str, full_path: Path,
                          tokens_to_find=None) -> bool:
  """Check the upstart config for required clause."""
  if not tokens_to_find:
    tokens_to_find = {
        'author',
        'description',
        # TODO add 'oom' after adding it to missing scripts.
    }
  for line in text.splitlines():
    try:
      token = line.split()[0]
    except IndexError:
      continue

    try:
      tokens_to_find.remove(token)
    except KeyError:
      continue

    if not tokens_to_find:
      return True
  logging.error('Missing clauses from upstart script "%s": %s',
                full_path, ', '.join(tokens_to_find))
  return False


def CheckInitConf(full_path: Path) -> bool:
  """Check an upstart conf file for linter errors."""
  ret = True
  text = full_path.read_text(encoding='utf-8')
  if not CheckForRequiredLines(text, full_path):
    ret = False

  label = os.path.basename(full_path)
  ignore_set = set(GetIgnoreLookup().get(label, []))

  found = []
  for cmd in ExtractCommands(text):
    norm_cmd = ' '.join(cmd)
    if norm_cmd not in ignore_set:
      found.append(norm_cmd)

  if found:
    logging.error('Init script "%s" has unsafe commands:', full_path)
    for cmd in found:
      logging.error('    %s', cmd)
    logging.error('Please use a tmpfiles.d config for the commands or have '
                  'them reviewed by security and add "# croslint: disable:"')
    ret = False
  return ret
