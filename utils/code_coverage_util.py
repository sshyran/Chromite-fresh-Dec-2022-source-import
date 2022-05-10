# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Utilities for working with code coverage files."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

from chromite.lib import osutils


ZERO_COVERAGE_EXEC_COUNT = 0
ZERO_COVERAGE_START_COL = 1
LLVM_COVERAGE_JSON_TYPE = 'llvm.coverage.json.export'
LLVM_COVERAGE_VERSION = '2.0.1'


def _IsInstrumented(line: str, exclude_line_prefixes: Tuple[str]) -> bool:
  """Returns if the input line is instrumented or not.

    Method does a simple prefix based check to determine if
    a line is instrumendted or not.

  Args:
    line: Single code line to test for instrumentation.
    exclude_line_prefixes: tuple of un-instrumented line prefixes.

  Returns:
    True if the line is instrumented, otherwise false.
  """
  line = line.lstrip()
  if not line:
    return False
  return not line.startswith(tuple(exclude_line_prefixes))


def _CreateOpenSegment(line_number: int):
  """Create a segment corresponding to start of instrumented code region.

    Method to create and return a segment which represents start of an
    instrumented code region. For zero coverage purpose an open segment
    is always considered to start from col 1.

    More details about segments can be found here: go/chromeos-zero-coverage.

  Args:
    line_number: The line number from where the instrumented code region starts.

  Returns:
    An open segment.
  """
  return [
      line_number, ZERO_COVERAGE_START_COL, ZERO_COVERAGE_EXEC_COUNT, True,
      True, False
  ]


def _CreateCloseSegment(line_number: int, col: int):
  """Create a segment corresponding to end of instrumented code region.

    Method to create and return a segment which represents end of an
    instrumented code region.
    More details about segments can be found here: go/chromeos-zero-coverage.

  Args:
    line_number: Marks the end of instrumented code region.
    col: The col number which marks the end of the instrumented code region.

  Returns:
    A close segment.
  """
  return [line_number, col, ZERO_COVERAGE_EXEC_COUNT, False, False, False]


def _ExtractLlvmCoverageData(coverage_json: Dict) -> List:
  """Extract coverage data from coverage json.

  Args:
    coverage_json: llvm formatted coverage json.

  Returns:
    List of coverage data objects.
  """
  if (not coverage_json or not coverage_json.get('data')):
    return []

  return coverage_json['data'][0]['files']


def _GenerateZeroCoverageLLVMForFile(file_path: str, src_prefix_path: str,
                                     exclude_line_prefixes: Tuple[str]) -> Dict:
  """Generates LLVM json formatted zero % coverage for the given file.

    Method to identify all the instrumented lines within a file and generate
    mock coverage data json. The mock json marks all the instrumented lines
    as not-covered by unit tests.

    More detials: go/chromeos-zero-coverage.

  Args:
    file_path: path to the src file.
    src_prefix_path: prefix path for source code
    exclude_line_prefixes: Used to determine un-instrumented lines
    in the file.

  Returns:
    Dict representing zero coverage data for the file.
  """

  segments = []
  line_index = 0

  with open(file_path, 'r', encoding='utf8', errors='ignore') as file:

    lines = file.readlines()
    if not lines:
      return None

    while line_index < len(lines):
      # Search for next instrumented line
      while (line_index < len(lines) and
             not _IsInstrumented(lines[line_index], exclude_line_prefixes)):
        line_index += 1

      if line_index < len(lines):
        # Instrumented code block started. Add a open segment to indicate that
        segments.append(_CreateOpenSegment(line_index + 1))

      # Search for next un-instrumented line
      while (line_index < len(lines) and
             _IsInstrumented(lines[line_index], exclude_line_prefixes)):
        line_index += 1

      if line_index < len(lines):
        # Instrumented code block ended on previous line.
        # Add a close segment to indicate that
        segments.append(
            _CreateCloseSegment(line_index, len(lines[line_index - 1])))

    # If segment size is odd, this means there is an open instrumented
    # code block. Lets add a close segment.
    if len(segments) % 2 == 1:
      segments.append(
          _CreateCloseSegment(line_index, len(lines[line_index - 1])))

    file_data = {}
    file_data['filename'] = str(Path(file_path).relative_to(src_prefix_path))
    file_data['segments'] = segments
    # Zoss does not use summary field, so keep it empty
    file_data['summary'] = {}
    return file_data


def _ShouldExclude(file: str, exclude_files: List[str],
                   exclude_files_suffixes: Tuple[str]) -> bool:
  """Determine if the filename should be excluded from zero coverage.

    This method first does the suffixes based exclude check.
    Next it iterates over all |exclude_files| to search for |file|.
    Note that LLVM generated file paths are absolute paths, however
    |file| is relative to src.

  Args:
    file: Chromium src root relative file path.
    exclude_files: List of llvm generated file paths to exclude.
    exclude_files_suffixes: Used to exclude files based on suffixes

  Returns:
    True if a file should be excluded otherwise False.
  """
  should_exclude = False
  if file.endswith(exclude_files_suffixes):
    should_exclude = True
  else:
    for exclude_file in exclude_files:
      if file in exclude_file:
        should_exclude = True
        break

  if should_exclude:
    logging.info('Excluding file %s from coverage reports.', file)
  return should_exclude


def GetLLVMCoverageWithFilesExcluded(coverage_json: Dict,
                                     exclude_files_suffixes: Tuple[str]
                                    ) -> Dict:
  """Removes and returns required file entries from coverage json.

     Method to remove file entries in coverage json which ends with one of
     the suffixes mentioned in |exclude_files_suffixes|.

  Args:
    coverage_json: llvm coverage json
    exclude_files_suffixes: Used to remove files based on suffixes

  Returns:
    llvm coverage json after required entries are removed.
  """
  if not exclude_files_suffixes:
    return coverage_json

  coverage_data = _ExtractLlvmCoverageData(coverage_json)
  result_coverage_data = []
  for entry in coverage_data:
    if not entry['filename'].endswith(exclude_files_suffixes):
      result_coverage_data.append(entry)
    else:
      logging.info('skipping file %s from zero coverage.',
                   entry['filename'])
  return CreateLlvmCoverageJson(result_coverage_data)


def MergeLLVMCoverageJson(coverage_json_1: Dict, coverage_json_2: Dict) -> Dict:
  """Merge coverage data of two coverage json and return single coverage json.

  Args:
    coverage_json_1: llvm coverage json to merge.
    coverage_json_2: llvm coverage json to merge.

  Returns:
    Single merged llvm formatted coverage json.
  """
  coverage_data_1 = _ExtractLlvmCoverageData(coverage_json_1)
  coverage_data_2 = _ExtractLlvmCoverageData(coverage_json_2)

  result = coverage_data_1.copy()
  result.extend(coverage_data_2)

  return CreateLlvmCoverageJson(result)


def ExtractFilenames(coverage_json: Dict) -> List[str]:
  """Extracts filenames from coverage json.

  Args:
    coverage_json: The coverage json in LLVM format.

  Returns:
    List of filenames.
  """
  if (not coverage_json or not coverage_json.get('data') or
      not coverage_json['data'][0].get('files')):
    return []

  files = coverage_json['data'][0]['files']
  filenames = []
  for file_data in files:
    filenames.append(file_data['filename'])

  return filenames


def CreateLlvmCoverageJson(coverage_data: List) -> Dict:
  """Given coverage_data, generate llvm format coverage json.

  Args:
    coverage_data: The coverage data containing array of file cov info.

  Returns:
    coverage json llvm format.
  """
  coverage_json = {
      'data': [{
          'files': coverage_data,
      }],
      'type': LLVM_COVERAGE_JSON_TYPE,
      'version': LLVM_COVERAGE_VERSION,
  }
  return coverage_json


def GenerateZeroCoverageLlvm(path_to_src_directories: List[str],
                             src_file_extensions: List[str],
                             exclude_line_prefixes: Tuple[str],
                             exclude_files: List[str],
                             exclude_files_suffixes: Tuple[str],
                             src_prefix_path: str) -> Dict:
  """Generate zero coverage for all src files under  |path_to_src_directories|.

     More detials on how to generate zero coverage: go/chromeos-zero-coverage.

  Args:
    path_to_src_directories: Dir to look for files to generate zero coverage.
    src_file_extensions: Filter files based on these extensions.
    exclude_line_prefixes: Used to determine un-instrumented code.
    exclude_files: files to exclude from zero coverage.
    exclude_files_suffixes: Used to exclude files based on suffixes
    src_prefix_path: prefix path for source code

  Returns:
    llvm format coverage json.
  """
  coverage_data = []
  filenames = []
  for basedir in path_to_src_directories:
    for dirpath, _dirnames, filenames in os.walk(basedir):
      for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        relative_file_path = full_file_path.replace(basedir, '')
        if (filename.endswith(tuple(src_file_extensions)) and
            not _ShouldExclude(relative_file_path, exclude_files,
                               exclude_files_suffixes)):

          zero_cov = _GenerateZeroCoverageLLVMForFile(full_file_path,
                                                      src_prefix_path,
                                                      exclude_line_prefixes)

          if zero_cov:
            coverage_data.append(zero_cov)

  return CreateLlvmCoverageJson(coverage_data)


def GetLlvmJsonCoverageDataIfValid(path_to_file: str):
  """Gets the content of a file if it matches the llvm coverage json format.

  Args:
    path_to_file: The path of the file to read.

  Returns:
    The file contents if they match the llvm json structure, otherwise None.
  """
  try:
    # Only coverage.json files matter for llvm json coverage.
    if os.path.basename(path_to_file) != 'coverage.json':
      return None

    # Make sure the file exists.
    if not os.path.isfile(path_to_file):
      return None

    # Attempt to parse as json. It's fine for this to fail,
    # it means we can't manipulate it rather than an actual error.
    data = json.loads(osutils.ReadFile(path_to_file))

    # Validate the file structure is:
    # { data: [...], type: "..", version: "..." }.
    if 'data' not in data or 'type' not in data or 'version' not in data:
      return None

    if data['type'] != 'llvm.coverage.json.export':
      return None

    return data
  except Exception as e:
    logging.warning('GetLlvmJsonCoverageDataIfValid failed %s', e)
    return None
