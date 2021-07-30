# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for tricium_cargo_tidy.py."""

import json

from chromite.lib import cros_test_lib
from chromite.scripts import tricium_cargo_clippy


# These test cases were made by:
#   1) modifying trace_events to lint poorly
#   2) running USE="rust_clippy" emerge trace_events
#   3) removing null fields
#   4) replacing strings with shorter test strings
valid_test_cases = {
    json.dumps({
        'reason': 'compiler-message',
        'package_id': 'package_id_1',
        'target': {
            'kind': ['lib'],
            'crate_types': ['lib'],
            'name': 'trace_events',
            'src_path': '/path/to/some/git/repo/path/to/file_path_1',
            'edition': '2018',
            'doctest': True,
            'test': True
        },
        'message': {
            'rendered': 'warning: rendered message 1',
            'children': [
                {
                    'children': [],
                    'level': 'note',
                    'message': '`#[warn(bare_trait_objects)]` message 1',
                    'spans': []
                },
                {
                    'children': [],
                    'level': 'help',
                    'message': 'sub message 1',
                    'spans': [{
                        'file_name': 'file_name_1',
                        'byte_end': 7342, 'byte_start': 7336,
                        'column_end': 35, 'column_start': 29,
                        'is_primary': True,
                        'line_end': 262, 'line_start': 262,
                        'suggested_replacement': 'dyn Tracer',
                        'suggestion_applicability': 'MachineApplicable',
                        'text': [{
                            'highlight_end': 35, 'highlight_start': 29,
                            'text': 'highlight 1'
                        }]
                    }]
                }
            ],
            'code': {'code': 'bare_trait_objects'},
            'level': 'warning',
            'message': 'message 1',
            'spans': [{
                'byte_end': 7342, 'byte_start': 7336,
                'column_end': 35, 'column_start': 29,
                'file_name': 'file_name_1',
                'is_primary': True,
                'line_end': 262, 'line_start': 262,
                'text': [{
                    'highlight_end': 35, 'highlight_start': 29,
                    'text': 'highlight 1'
                }]
            }]
        }
    }): {
        'file_path': 'path/to/file_path_1',
        'locations': [
            tricium_cargo_clippy.CodeLocation(
                file_path='path/to/file_path_1',
                file_name='file_name_1',
                line_start=262,
                line_end=262,
                column_start=29,
                column_end=35
            )
        ],
        'level': 'warning',
        'message': 'warning: rendered message 1',
    },
    json.dumps({
        'reason': 'compiler-message',
        'package_id': 'package_id 1',
        'target': {
            'kind': ['lib'],
            'crate_types': ['lib'],
            'name': 'trace_events',
            'src_path': '/absolute/path/to/file_path_2',
            'edition': '2018', 'doctest': True, 'test': True
        },
        'message': {
            'rendered': 'warning: rendered message 2',
            'children': [
                {
                    'level': 'note',
                    'children': [],
                    'message': 'submessage 2.1',
                    'spans': []
                },
                {
                    'level': 'help',
                    'children': [],
                    'message': 'submessage 2.2',
                    'spans': []
                },
                {
                    'level': 'help',
                    'children': [],
                    'message': 'submessage 2.3',
                    'spans': [{
                        'file_name': 'file_name_2',
                        'byte_end': 7342, 'byte_start': 7327,
                        'column_end': 35, 'column_start': 20,
                        'line_end': 262, 'line_start': 262,
                        'is_primary': True,
                        'suggested_replacement': '&Tracer',
                        'suggestion_applicability': 'MachineApplicable',
                        'text': [{
                            'highlight_end': 35,
                            'highlight_start': 20,
                            'text': 'highlight 2'
                        }]
                    }]
                }
            ],
            'code': {'code': 'clippy::redundant_static_lifetimes'},
            'level': 'warning',
            'message': 'message 2',
            'spans': [{
                'file_name': 'file_name_2',
                'byte_end': 7335, 'byte_start': 7328,
                'column_end': 28, 'column_start': 21,
                'line_end': 262, 'line_start': 262,
                'is_primary': True,
                'text': [{
                    'highlight_end': 28,
                    'highlight_start': 21,
                    'text': 'highlight 2'
                }]
            }]
        }
    }): {
        'file_path': '/absolute/path/to/file_path_2',
        'locations': [
            tricium_cargo_clippy.CodeLocation(
                file_path='/absolute/path/to/file_path_2',
                file_name='file_name_2',
                line_start=262,
                line_end=262,
                column_start=21,
                column_end=28
            ),
            tricium_cargo_clippy.CodeLocation(
                file_path='/absolute/path/to/file_path_2',
                file_name='file_name_2',
                line_start=262,
                line_end=262,
                column_start=20,
                column_end=35
            )
        ],
        'level': 'warning',
        'message': 'warning: rendered message 2',
    },
    json.dumps({
        'reason': 'compiler-message',
        'package_id': 'package id 3',
        'target': {
            'kind': ['lib'],
            'crate_types': ['lib'],
            'name': 'trace_events',
            'src_path': '/path/to/some/git/repo//path/to/file_path_3',
            'edition': '2018', 'doctest': True, 'test': True
        },
        'message': {
            'rendered': 'warning: rendered message 3',
            'children': [
                {
                    'children': [],
                    'level': 'note',
                    'message': 'submessage 3.1',
                    'spans': []
                },
                {
                    'children': [],
                    'level': 'help',
                    'message': 'submessage 3.2',
                    'spans': [
                        {
                            'file_name': 'file_name_3',
                            'byte_end': 448, 'byte_start': 447,
                            'column_end': 8, 'column_start': 7,
                            'line_end': 14, 'line_start': 14,
                            'is_primary': True,
                            'suggested_replacement': '_x',
                            'suggestion_applicability': 'MachineApplicable',
                            'text': [{
                                'highlight_end': 8, 'highlight_start': 7,
                                'text': 'highlight 3'
                            }]
                        }
                    ]
                }
            ],
            'code': {'code': 'unused_variables'},
            'level': 'warning',
            'message': 'message 3',
            'spans': [{
                'file_name': 'file_name_3',
                'byte_end': 448, 'byte_start': 447,
                'column_end': 8, 'column_start': 7,
                'line_end': 14, 'line_start': 14,
                'is_primary': True,
                'text': [{
                    'highlight_end': 8,
                    'highlight_start': 7,
                    'text': 'highlight 3'
                }]
            }]
        }
    }): {
        'file_path': 'path/to/file_path_3',
        'locations': [
            tricium_cargo_clippy.CodeLocation(
                file_path='path/to/file_path_3',
                file_name='file_name_3',
                line_start=14,
                line_end=14,
                column_start=7,
                column_end=8
            )
        ],
        'level': 'warning',
        'message': 'warning: rendered message 3',
    },
    json.dumps({'reason': 'build-script-executed'}): {
        'skipped': True
    },
    json.dumps({'reason': 'compiler-artifact'}): {
        'skipped': True
    }
}

invalid_test_cases = {
    'not json': ['json'],
    r'{}': ['reason'],
    json.dumps({
        'reason': 'compiler-message',
    }): ['file_path', 'level', 'message'],
    json.dumps({
        'reason': 'compiler-message',
        'level': 'warning',
        'message': {
            'rendered': 'warning: a message'
        }
    }): ['file_path'],
    json.dumps({
        'reason': 'compiler-message',
        'target': {
            'src_path': 'file path'
        },
        'message': {
            'rendered': 'warning: a message'
        }
    }): ['level'],
    json.dumps({
        'reason': 'compiler-message',
        'level': 'warning',
        'target': {
            'src_path': 'file path'
        },
    }): ['message'],
}

test_git_repo = '/path/to/some/git/repo'


class TriciumCargoClippyTests(cros_test_lib.LoggingTestCase):
  """Tests for Cargo Clippy."""

  def test_parse_file_path(self):
    """Tests that parse_file_path is as expected."""
    for i, (test_case, exp_results) in enumerate(valid_test_cases.items()):
      if 'file_path' not in exp_results:
        continue
      test_json = json.loads(test_case)
      file_path = tricium_cargo_clippy.parse_file_path(
          'valid', i, test_json, test_git_repo)
      self.assertEqual(file_path, exp_results['file_path'])

  def test_parse_locations(self):
    """Tests that parse_locations is as expected."""
    for test_case, exp_results in valid_test_cases.items():
      if 'locations' not in exp_results:
        continue
      test_json = json.loads(test_case)
      locations = list(tricium_cargo_clippy.parse_locations(
          test_json, exp_results['file_path']))
      self.assertEqual(locations, exp_results['locations'])

  def test_parse_level(self):
    """Tests that parse_level is as expected."""
    for i, (test_case, exp_results) in enumerate(valid_test_cases.items()):
      if 'level' not in exp_results:
        continue
      test_json = json.loads(test_case)
      level = tricium_cargo_clippy.parse_level('valid', i, test_json)
      self.assertEqual(level, exp_results['level'])

  def test_parse_message(self):
    """Tests that parse_message is as expected."""
    for i, (test_case, exp_results) in enumerate(valid_test_cases.items()):
      if 'message' not in exp_results:
        continue
      test_json = json.loads(test_case)
      message = tricium_cargo_clippy.parse_message('valid', i, test_json)
      self.assertEqual(message, exp_results['message'])

  def test_parse_diagnostics(self):
    """Tests that parse_diagnostics yields correct diagnostics."""
    diags = list(tricium_cargo_clippy.parse_diagnostics(
        'valid_test_cases', list(valid_test_cases.keys()), test_git_repo))

    # Verify parse_diagnostics retrieved correct amount of diagnostics
    exp_len = len([
        values for values in valid_test_cases.values()
        if not values.get('skipped')
    ])
    self.assertEqual(len(diags), exp_len)

    # Verify diagnostics are from correct source
    for i, diag in enumerate(diags):
      locations = list(diag.locations)
      expected_locations = list(valid_test_cases.values())[i].get('locations')
      self.assertEqual(locations, expected_locations)

  def test_logs_invalid_parse_diagnostic_cases(self):
    """Tests that parse_diagnostics logs proper exceptions."""
    for invalid_case, exp_errors in invalid_test_cases.items():
      with self.assertRaises(
          tricium_cargo_clippy.Error,
          msg=f'Expected error parsing {invalid_case} but got none.') as ctx:
        list(tricium_cargo_clippy.parse_diagnostics(
            'invalid', [invalid_case], test_git_repo))
      if 'json' in exp_errors:
        exp_error = tricium_cargo_clippy.CargoClippyJSONError('invalid', 0)
      elif 'reason' in exp_errors:
        exp_error = tricium_cargo_clippy.CargoClippyReasonError('invalid', 0)
      else:
        for field in ('file_path', 'locations', 'level', 'message'):
          if field in exp_errors:
            exp_error = tricium_cargo_clippy.CargoClippyFieldError(
                'invalid', 0, field)
            break
      self.assertIs(type(ctx.exception), type(exp_error))
      self.assertEqual(ctx.exception.args, exp_error.args)

  def test_filter_diagnostics(self):
    file_path = 'some_filepath.json'
    example_code_location = tricium_cargo_clippy.CodeLocation(
        file_path=file_path,
        file_name=file_path,
        line_start=1,
        line_end=4,
        column_start=0,
        column_end=12
    )
    accepted_diags = [
        tricium_cargo_clippy.ClippyDiagnostic(
            file_path=file_path,
            locations=[example_code_location],
            level='warning',
            message='warning: be warned.'
        )
    ]
    ignored_diags = [
        # "aborting due to previous error" messages
        tricium_cargo_clippy.ClippyDiagnostic(
            file_path=file_path,
            locations=[example_code_location],
            level='warning',
            message='warning: aborting due to previous error...'
        ),
        # No locations provided
        tricium_cargo_clippy.ClippyDiagnostic(
            file_path=file_path,
            locations=[],
            level='warning',
            message='warning: 6 warnings emitted.'
        )
    ]
    filtered_diags = list(tricium_cargo_clippy.filter_diagnostics(
        accepted_diags + ignored_diags))
    self.assertEqual(filtered_diags, accepted_diags)
