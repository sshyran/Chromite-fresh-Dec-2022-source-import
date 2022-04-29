# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for LTS_kernel_uprev."""

import copy
import os
from unittest.mock import patch
import xml.etree.ElementTree as ET

from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.scripts import lts_kernel_uprev


SAMPLE_MANIFEST_XML = """<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <include name="_remotes.xml" />
  <default revision="refs/heads/main"
           remote="cros"
           sync-j="8" />

  <include name="_kernel_upstream.xml" />

  <project path="src/third_party/kernel/v5.10"
           name="chromiumos/third_party/kernel"
           revision="refs/heads/chromeos-5.10" />
  <project path="src/third_party/kernel/v5.10-arcvm"
           name="chromiumos/third_party/kernel"
           revision="refs/heads/chromeos-5.10-arcvm" />
 </manifest>"""

SAMPLE_CL_UPLOAD = """remote: Processing changes: refs: 1, new: 1, done
remote:
remote: SUCCESS
remote:
remote:   https://chrome-internal-review.googlesource.com/c/chromeos/\
manifest-internal/+/4286699 LTS: update kernel commit ids for LTS branches [NEW]
remote:
To https://chrome-internal-review.googlesource.com/chromeos/manifest-internal
 * [new reference]         main -> refs/for/main
"""


# Helper functions to mock calls within lts_kernel_uprev methods
def branches_mock(run_cmd, **unused_kwargs):
  if 'refs/remotes/cros/release-R96-*' in run_cmd:
    return cros_build_lib.CommandResult(
        stdout=('release-R96-14268.B-chromeos-5.10\nrelease-R96-14268.'
                'B-chromeos-5.10-arcvm\nrelease-R96-14268.B-chromeos-5.'
                '4\nrelease-R96-14268.B-chromeos-5.4-arcvm\nrelease-R96-14268.'
                'B-chromeos-5.4-manatee'))
  else:
    return cros_build_lib.CommandResult(stdout=(''))


def tag_mock(*unused_args, **unused_kwargs):
  return cros_build_lib.CommandResult(stdout='v5.10.71-12106-gbca20254cbdc')


def git_rev_mock(*unused_args, **unused_kwargs):
  return 'e028e1181cdcfc94865861d460c96ddb5e08bb6f'


def commit_date_mock(unused_obj, unused_repo, commit_id):
  if commit_id == 'e028e1181cdcfc94865861d460c96ddb5e08bb6f':
    return '2021-10-28 21:52:39 +0000'
  else:
    return None


def git_commit_mock(*unused_args, **unused_kwargs):
  return cros_build_lib.CommandResult(stdout='2021-05-01 03:51:23 +0000')


class CrosLtsKernelUprevTests(cros_test_lib.TempDirTestCase):
  """Tests for LTS kernel uprev functionality."""

  def setUp(self):
    """General set up for LTS kernel uprev tests."""
    options = lts_kernel_uprev.parse_args(['--release=R96'])
    self.LtsKernelUprev = lts_kernel_uprev.LtsKernelUprev(
        options.release, options.buildroot)
    self.buildroot = options.buildroot
    # Write a sample manifest.
    self.temp_manifest_path = os.path.join(self.tempdir, 'ltsTestManifest.xml')
    osutils.WriteFile(self.temp_manifest_path, SAMPLE_MANIFEST_XML)

  @patch.object(cros_build_lib, 'run', new_callable=lambda: branches_mock)
  def test_get_branch_name(self, unused_patch_run):
    """Tests LtsKernelUprev.get_branch_name returns expected results."""
    # Test a valid milestone.
    branch_name = self.LtsKernelUprev.get_branch_name()
    self.assertEqual('release-R96-14268.B-chromeos-', branch_name)
    # Test a non-existent milestone.
    lts_no_milestone = lts_kernel_uprev.LtsKernelUprev('NoMilestone',
                                                       self.buildroot)
    no_branch = lts_no_milestone.get_branch_name()
    self.assertIsNone(no_branch)

  @patch.object(cros_build_lib, 'run', new_callable=lambda: tag_mock)
  @patch.object(git, 'GetGitRepoRevision', new_callable=lambda: git_rev_mock)
  @patch.object(
      lts_kernel_uprev.LtsKernelUprev,
      'get_commit_date',
      new_callable=lambda: commit_date_mock)
  def test_find_new_kernel_commit_ids(self, unused_patch_run,
                                      unused_patch_gitrev,
                                      unused_patch_commitdate):
    """Tests LtsKernelUprev.find_new_kernel_commit_ids returns exp. results."""
    branch_name = 'release-R96-14268.B-chromeos-'
    xml_tree = ET.parse(self.temp_manifest_path)
    # Test with a valid manifest.
    replace_mapping = self.LtsKernelUprev.find_new_kernel_commit_ids(
        branch_name, xml_tree)
    self.assertEqual(
        {
            'v5.10': {
                'new_revision': 'e028e1181cdcfc94865861d460c96ddb5e08bb6f',
                'original_revision': 'refs/heads/chromeos-5.10',
                'original_date_str': None,
                'new_date_str': '2021-10-28 21:52:39 +0000',
            },
            'v5.10-arcvm': {
                'new_revision': 'refs/heads/chromeos-5.10-arcvm',
                'original_revision': 'refs/heads/chromeos-5.10-arcvm',
                'original_date_str': None,
                'new_date_str': None,
            },
        }, replace_mapping)
    # Test with an invalid kernel repo path in the manifest.
    xml_invalid_kernel = os.path.join(self.tempdir,
                                      'ltsTestInvalidKernelManifest.xml')
    osutils.WriteFile(
        xml_invalid_kernel,
        SAMPLE_MANIFEST_XML.replace('kernel/v5.10', 'kernel/invalid'))
    xml_tree = ET.parse(xml_invalid_kernel)
    branch_name = 'release-R96-14268.B-chromeos-'
    replace_mapping = self.LtsKernelUprev.find_new_kernel_commit_ids(
        branch_name, xml_tree)
    self.assertEqual({}, replace_mapping)

  @patch.object(cros_build_lib, 'run', new_callable=lambda: git_commit_mock)
  def test_get_commit_date(self, unused_patch_run):
    """Tests LtsKernelUprev.get_commit_date returns expected results."""
    kernel_repo_path = self.buildroot / 'src/third_party/kernel/v5.10'
    # Test with a valid commit id.
    commit_id_date_str = self.LtsKernelUprev.get_commit_date(
        kernel_repo_path, '355a95829e9f0f868603b87cc881e0355a26ec16')
    self.assertEqual('2021-05-01 03:51:23 +0000', commit_id_date_str)
    # Test with an invalid commit id.
    commit_id_date_str = self.LtsKernelUprev.get_commit_date(
        kernel_repo_path, '3049ae9b253')
    self.assertIsNone(commit_id_date_str)

  def test_remove_invalid_revisions(self):
    """Tests LtsKernelUprev.remove_invalid_revisions has exp. side effect."""
    # Test valid commit id revisions are not removed.
    replace_mapping = {
        'v5.10': {
            'original_revision': '355a95829e9f0f868603b87cc881e0355a26ec16',
            'new_revision': 'ff5140f08b2a362171848f9215504e801863ab86',
            'original_date_str': '2021-05-01 03:51:23 +0000',
            'new_date_str': '2021-05-01 09:11:33 +0000',
        },
        'v5.4': {
            'original_revision': '355a95829e9f0f868603b87cc881e0355a26ec16',
            'new_revision': 'refs/heads/chromeos-5.10',
            'original_date_str': '2021-05-01 03:51:23 +0000',
            'new_date_str': None,
        },
    }
    replace_mapping_copy = copy.deepcopy(replace_mapping)
    self.LtsKernelUprev.remove_invalid_revisions(replace_mapping)
    self.assertEqual(replace_mapping_copy, replace_mapping)
    # Test invalid commit id revisions are removed.
    replace_mapping = {
        'v5.10': {
            'new_revision': '355a95829e9f0f868603b87cc881e0355a26ec16',
            'original_revision': 'ff5140f08b2a362171848f9215504e801863ab86',
            'new_date_str': '2021-05-01 03:51:23 +0000',
            'original_date_str': '2021-05-01 09:11:33 +0000',
        },
    }
    self.LtsKernelUprev.remove_invalid_revisions(replace_mapping)
    self.assertEqual({}, replace_mapping)

  def test_pretty_update_xml(self):
    """Tests LtsKernelUprev.pretty_update_xml has expected side effect."""
    replace_mapping = {
        'v5.10': {
            'new_revision': 'e028e1181cdcfc94865861d460c96ddb5e08bb6f',
            'original_revision': 'refs/heads/chromeos-5.10',
        },
    }
    self.LtsKernelUprev.pretty_update_xml(replace_mapping,
                                          self.temp_manifest_path)
    updated_manifest_xml = osutils.ReadFile(self.temp_manifest_path)
    expected_manifest_xml = SAMPLE_MANIFEST_XML.replace(
        'revision="refs/heads/chromeos-5.10"',
        'revision="e028e1181cdcfc94865861d460c96ddb5e08bb6f"')
    self.assertEqual(updated_manifest_xml, expected_manifest_xml)
