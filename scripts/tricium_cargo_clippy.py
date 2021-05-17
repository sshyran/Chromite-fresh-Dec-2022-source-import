# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Runs cargo clippy across the given files, dumping diagnostics to a JSON file.

This script is intended specifically for use with Tricium (go/tricium).
"""

import json
import os
from pathlib import Path
import re
from typing import List, Dict, Iterable, Any, Text, NamedTuple

from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging


class Error(Exception):
  """Base error class for tricium-cargo-clippy."""


class CargoClippyJSONError(Error):
  """Raised when cargo-clippy parsing jobs are not proper JSON."""

  def __init__(self, source: Text, line_num: int):
    super().__init__(f'{source}:{line_num}: is not valid JSON')
    self.source = source
    self.line_num = line_num


class CargoClippyReasonError(Error):
  """Raised when cargo-clippy parsing jobs don't provide a "reason" field."""

  def __init__(self, source: Text, line_num: int):
    super().__init__(f'{source}:{line_num}: is missing its reason')
    self.source = source
    self.line_num = line_num


class CargoClippyFieldError(Error):
  """Raised when cargo-clippy parsing jobs fail to determine a field."""

  def __init__(self, source: Text, line_num: int, field: Text):
    super().__init__(
        f'{source}:{line_num}: {field} could not be parsed from original json'
    )
    self.source = source
    self.line_num = line_num
    self.field = field


def resolve_path(file_path: Text) -> Text:
  return str(Path(file_path).resolve())


class CodeLocation(NamedTuple):
  """Holds the location a ClippyDiagnostic Finding."""
  file_path: Text
  file_name: Text
  line_start: int
  line_end: int
  column_start: int
  column_end: int

  def to_dict(self):
    return {
        **self._asdict(),
        'file_path': resolve_path(self.file_path)
    }


class ClippyDiagnostic(NamedTuple):
  """Holds information about a compiler message from Clippy."""
  file_path: Text
  locations: Iterable['CodeLocation']
  level: Text
  message: Text

  def as_json(self):
    return json.dumps({
        **self._asdict(),
        'locations': [loc.to_dict() for loc in self.locations],
    })


def parse_file_path(
    src: Text, src_line: int, orig_json: Dict[Text, Any]) -> Text:
  """The path to the file targeted by the lint.

  Args:
    src: Name of the file orig_json was found in.
    src_line: Line number where orig_json was found.
    orig_json: An iterable of clippy entries in original json.

  Returns:
    A resolved path to the original source location as a string.

  Raises:
    CargoClippyFieldError: Parsing failed to determine the file path.
  """
  target_src_path = orig_json.get('target', {}).get('src_path')
  if not target_src_path:
    raise CargoClippyFieldError(src, src_line, 'file_path')
  return resolve_path(target_src_path)


def parse_locations(
    orig_json: Dict[Text, Any],
    file_path: Text) -> Iterable['CodeLocation']:
  """The code locations associated with this diagnostic as an iter.

  The relevant code location can appear in either the messages[spans] field,
  which will be used if present, or else child messages each have their own
  locations specified.

  Args:
    orig_json: An iterable of clippy entries in original json.
    file_path: A resolved path to the original source location.

  Yields:
    A CodeLocation object associated with a relevant span.

  Raises:
    CargoClippyFieldError: Parsing failed to determine any code locations.
  """
  spans = orig_json.get('message', {}).get('spans', [])
  children = orig_json.get('message', {}).get('children', [])
  for child in children:
    spans = spans + child.get('spans', [])
  locations = set()
  for span in spans:
    location = CodeLocation(
        file_path=file_path,
        file_name=span.get('file_name'),
        line_start=span.get('line_start'),
        line_end=span.get('line_end'),
        column_start=span.get('column_start'),
        column_end=span.get('column_end'))
    if location not in locations:
      locations.add(location)
      yield location


def parse_level(src: Text, src_line: int, orig_json: Dict[Text, Any]) -> Text:
  """The level (error or warning) associated with this diagnostic.

  Args:
    src: Name of the file orig_json was found in.
    src_line: Line number where orig_json was found.
    orig_json: An iterable of clippy entries in original json.

  Returns:
    The level of the diagnostic as a string (either error or warning).

  Raises:
    CargoClippyFieldError: Parsing failed to determine the level.
  """
  level = orig_json.get('level')
  if not level:
    level = orig_json.get('message', {}).get('level')
  if not level:
    raise CargoClippyFieldError(src, src_line, 'level')
  return level


def parse_message(
    src: Text, src_line: int, orig_json: Dict[Text, Any]) -> Text:
  """The formatted linter message for this diagnostic.

  Args:
    src: Name of the file orig_json was found in.
    src_line: Line number where orig_json was found.
    orig_json: An iterable of clippy entries in original json.

  Returns:
    The rendered message of the diagnostic.

  Raises:
    CargoClippyFieldError: Parsing failed to determine the message.
  """
  message = orig_json.get('message', {}).get('rendered')
  if message is None:
    raise CargoClippyFieldError(src, src_line, 'message')
  return message


def parse_diagnostics(
    src: Text, orig_jsons: Iterable[Text]) -> ClippyDiagnostic:
  """Parses original JSON to find the fields of a Clippy Diagnostic.

  Args:
    src: Name of the file orig_json was found in.
    orig_jsons: An iterable of clippy entries in original json.

  Yields:
    A ClippyDiagnostic for orig_json.

  Raises:
    CargoClippyJSONError: if a diagnostic is not valid JSON.
    CargoClippyReasonError: if a diagnostic is missing a "reason" field.
    CargoClippyFieldError: if a field cannot be determined while parsing.
  """
  for src_line, orig_json in enumerate(orig_jsons):
    try:
      line_json = json.loads(orig_json)
    except json.decoder.JSONDecodeError:
      json_error = CargoClippyJSONError(src, src_line)
      logging.error(json_error)
      raise json_error
    # Clippy outputs several types of logs, as distinguished by the "reason"
    # field, but we only want to process "compiler-message" logs.
    reason = line_json.get('reason')
    if reason is None:
      reason_error = CargoClippyReasonError(src, src_line)
      logging.error(reason_error)
      raise reason_error
    if reason != 'compiler-message':
      continue

    file_path = parse_file_path(src, src_line, line_json)
    locations = parse_locations(line_json, file_path)
    level = parse_level(src, src_line, line_json)
    message = parse_message(src, src_line, line_json)

    # TODO(ryanbeltran): Export suggested replacements
    yield ClippyDiagnostic(file_path, locations, level, message)


def parse_files(input_dir: Text) -> Iterable[ClippyDiagnostic]:
  """Gets all compiler-message lints from all the input files in input_dir.

  Args:
    input_dir: path to directory to scan for files

  Yields:
    Clippy Diagnostics objects found in files in the input directory
  """
  for root_path, _, file_names in os.walk(input_dir):
    for file_name in file_names:
      file_path = os.path.join(root_path, file_name)
      with open(file_path, encoding='utf-8') as clippy_file:
        yield from parse_diagnostics(file_path, clippy_file)


def filter_diagnostics(
    diags: Iterable[ClippyDiagnostic],
    file_filter: Text) -> Iterable[ClippyDiagnostic]:
  """Filters diagnostics by file_path and message and validates schemas."""
  for diag in diags:
    # only include diagnostics if their file path matches the file_filter
    if not include_file_pattern(file_filter).fullmatch(diag.file_path):
      continue
    # ignore redundant messages: "aborting due to previous error..."
    if 'aborting due to previous error' in diag.message:
      continue
    # findings with no location are never useful
    if not diag.locations:
      continue
    yield diag



def include_file_pattern(file_filter: Text) -> 're.Pattern':
  """Constructs a regex pattern matching relevant file paths."""
  # FIXME(ryanbeltran): currently does not support prefixes for recursive
  #   wildcards such as a**/b.
  assert not re.search(r'[^/]\*\*', file_filter), (
      'prefixes for recursive wildcard ** not supported unless ending with /')
  tmp_char = chr(0)
  return re.compile(
      file_filter
      # Escape any .'s
      .replace('.', r'\.')
      # Squash recursive wildcards into a single symbol
      .replace('**/', tmp_char)
      .replace('**', tmp_char)
      # Nonrecursive wildcards match any string of non-"/" symbols
      .replace('*', r'[^/]*')
      # Recursive wildcards match any string of symbols
      .replace(tmp_char, r'(.*/)?')
      # Some paths may contain "//" which is equivalent to "/"
      .replace('//', '/')
  )


def get_arg_parser() -> commandline.ArgumentParser:
  """Creates an argument parser for this script."""
  parser = commandline.ArgumentParser(description=__doc__)
  parser.add_argument(
      '--output', required=True, type='path', help='File to write results to.')
  parser.add_argument(
      '--files',
      required=False,
      default='/**/*',
      type='path',
      help='File(s) to output lints for. If none are specified, this tool '
      'outputs all lints from clippy after applying filtering '
      'from |--git-repo-base|, if applicable.')
  parser.add_argument(
      '--clippy-json-dir',
      type='path',
      help='Directory where clippy outputs were previously written to.')
  return parser


def main(argv: List[str]) -> None:
  cros_build_lib.AssertInsideChroot()

  logging.basicConfig()

  parser = get_arg_parser()
  opts = parser.parse_args(argv)
  opts.Freeze()

  input_dir = resolve_path(opts.clippy_json_dir)
  output_path = resolve_path(opts.output)
  file_filter = resolve_path(opts.files)

  diagnostics = filter_diagnostics(parse_files(input_dir), file_filter)
  with open(output_path, 'w', encoding='utf-8') as output_file:
    output_file.writelines(f'{diag}\n' for diag in diagnostics)
