# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module tests the `cros branch` command."""

from __future__ import print_function

import mock
import os

from chromite.cbuildbot.manifest_version import VersionInfo
from chromite.cli import command_unittest
from chromite.cli.cros.cros_branch import Branch
from chromite.cli.cros.cros_branch import BranchCommand
from chromite.cli.cros.cros_branch import BranchError
from chromite.cli.cros.cros_branch import CanBranchProject
from chromite.cli.cros.cros_branch import CanPinProject
from chromite.cli.cros.cros_branch import CheckoutManager
from chromite.cli.cros.cros_branch import CrosCheckout
from chromite.cli.cros.cros_branch import FactoryBranch
from chromite.cli.cros.cros_branch import FirmwareBranch
from chromite.cli.cros.cros_branch import ManifestRepository
from chromite.cli.cros.cros_branch import ProjectBranch
from chromite.cli.cros.cros_branch import ReleaseBranch
from chromite.cli.cros.cros_branch import StabilizeBranch
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import partial_mock
from chromite.lib import repo_manifest
from chromite.lib import repo_util


def FileUrl(*args):
  """Map path components to a qualified local URL."""
  return 'file://%s' % os.path.join(*args)


def ParseManifestXml(xml):
  """Parse the XML into a repo_manifest.Manifest.

  Args:
    xml: Manifest XML as a string.

  Returns:
    The parsed repo_manifest.Manifest.
  """
  return repo_manifest.Manifest.FromString(
      xml, allow_unsupported_features=True)


def ManifestXml(*args):
  """Joins arbitrary XML and wraps it in a <manifest> element."""
  xml = '\n'.join(args)
  return '<?xml version="1.0" encoding="UTF-8"?><manifest>%s</manifest>' % xml


def AsAttrDict(*args):
  """Create AttrDict from string values, indexed by CAPS_CASE value."""
  return config_lib.AttrDict({v.upper().replace('-', '_'): v for v in args})


# A "project" in this dictionary is actually a project ID, which
# is used by helper functions to generate project name/path/revision/etc.
# If you add a project to this list, remember to update the categories below
# as well as PROJECTS_EXTERNAL_XML and its internal equivalent.
PROJECTS = AsAttrDict(
    'manifest',
    'manifest-internal',
    'chromiumos-overlay',
    'multicheckout-a',
    'multicheckout-b',
    'implicit-pinned',
    'explicit-tot',
    'explicit-branch',
    'explicit-pinned')

# Categorize the projects above for use in testing.
PINNED_PROJECTS = (PROJECTS.EXPLICIT_PINNED, PROJECTS.IMPLICIT_PINNED)
TOT_PROJECTS = (PROJECTS.EXPLICIT_TOT,)
MULTI_CHECKOUT_PROJECTS = (PROJECTS.MULTICHECKOUT_A, PROJECTS.MULTICHECKOUT_B)
SINGLE_CHECKOUT_PROJECTS = (PROJECTS.CHROMIUMOS_OVERLAY,
                            PROJECTS.EXPLICIT_BRANCH,
                            PROJECTS.MANIFEST,
                            PROJECTS.MANIFEST_INTERNAL)
BRANCHED_PROJECTS = SINGLE_CHECKOUT_PROJECTS + MULTI_CHECKOUT_PROJECTS
NON_BRANCHED_PROJECTS = PINNED_PROJECTS + TOT_PROJECTS
MANIFEST_PROJECTS = (PROJECTS.MANIFEST, PROJECTS.MANIFEST_INTERNAL)
EXTERNAL_PROJECTS = (PROJECTS.MANIFEST,
                     PROJECTS.CHROMIUMOS_OVERLAY,
                     PROJECTS.IMPLICIT_PINNED,
                     PROJECTS.MULTICHECKOUT_A,
                     PROJECTS.MULTICHECKOUT_B)
INTERNAL_PROJECTS = (PROJECTS.MANIFEST_INTERNAL,
                     PROJECTS.EXPLICIT_TOT,
                     PROJECTS.EXPLICIT_BRANCH,
                     PROJECTS.EXPLICIT_PINNED)

# Define remotes. There is a public and an internal remote.
REMOTES = AsAttrDict('cros', 'cros-internal')

# Store commonly used values for convenience.
EXTERNAL_FILE_NAME = 'external.xml'
INTERNAL_FILE_NAME = 'internal.xml'

# Create the raw XML based on the above data. Note that by convention,
# the leaf directory of the project path MUST end with the project ID.
DEFAULT_XML = """
  <default revision="refs/heads/master" remote="cros"/>
"""

REMOTE_EXTERNAL_XML = """
  <remote name="cros" fetch="ext-fetch"/>
"""

REMOTE_INTERNAL_XML = """
  <remote name="cros-internal" fetch="int-fetch"/>
"""

PROJECTS_EXTERNAL_XML = """
  <project name="chromiumos/manifest" path="manifest"/>

  <project name="chromiumos/overlays/chromiumos-overlay"
           path="src/third_party/chromiumos-overlay"/>

  <project name="external/implicit-pinned"
           path="src/third_party/implicit-pinned"
           revision="refs/heads/implicit-pinned"/>

  <project name="chromiumos/multicheckout"
           path="src/third_party/multicheckout-a"
           revision="refs/heads/multicheckout-a"/>

  <project name="chromiumos/multicheckout"
           path="src/third_party/multicheckout-b"
           revision="refs/heads/multicheckout-b"/>
"""

PROJECTS_INTERNAL_XML = """
  <project name="chromeos/manifest-internal"
           path="manifest-internal"
           remote="cros-internal"/>

  <project name="chromeos/explicit-pinned"
           path="src/explicit-pinned"
           revision="refs/heads/explicit-pinned"
           remote="cros-internal">
    <annotation name="branch-mode" value="pin"/>
  </project>

  <project name="chromeos/explicit-branch"
           path="src/explicit-branch"
           remote="cros-internal">
    <annotation name="branch-mode" value="create"/>
  </project>

  <project name="chromeos/explicit-tot"
           path="src/explicit-tot"
           remote="cros-internal">
    <annotation name="branch-mode" value="tot"/>
  </project>
"""

INCLUDE_EXTERNAL_XML = """
  <include name="external.xml"/>
"""

INCLUDE_INTERNAL_XML = """
  <include name="internal.xml"/>
"""

# Combine the XML chunks above into meaningful files. Create files for
# both manifest and manifest-internal projects.
MANIFEST_FILES = {
    EXTERNAL_FILE_NAME: ManifestXml(DEFAULT_XML,
                                    REMOTE_EXTERNAL_XML,
                                    PROJECTS_EXTERNAL_XML),
    constants.OFFICIAL_MANIFEST: ManifestXml(INCLUDE_EXTERNAL_XML),
    constants.DEFAULT_MANIFEST: ManifestXml(INCLUDE_EXTERNAL_XML),
}
MANIFEST_INTERNAL_FILES = {
    EXTERNAL_FILE_NAME: MANIFEST_FILES[EXTERNAL_FILE_NAME],
    INTERNAL_FILE_NAME: ManifestXml(DEFAULT_XML,
                                    REMOTE_INTERNAL_XML,
                                    PROJECTS_INTERNAL_XML),
    constants.OFFICIAL_MANIFEST: ManifestXml(INCLUDE_INTERNAL_XML,
                                             INCLUDE_EXTERNAL_XML),
    constants.DEFAULT_MANIFEST: ManifestXml(INCLUDE_INTERNAL_XML,
                                            INCLUDE_EXTERNAL_XML),
}

# Finally, store the full, parsed manifest XML. Essentially the output
# of the command `repo manifest`.
FULL_XML = ManifestXml(DEFAULT_XML,
                       REMOTE_EXTERNAL_XML,
                       REMOTE_INTERNAL_XML,
                       PROJECTS_EXTERNAL_XML,
                       PROJECTS_INTERNAL_XML)


class ManifestTestCase(cros_test_lib.TestCase):
  """Test case providing valid manifest test data.

  This class generates a diverse collection of manifest XML strings, and
  provides convenience methods for reading from those manifests.
  """

  def NameFor(self, pid):
    """Return the test project's name.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      Name of the project, e.g. 'chromeos/manifest-internal'.
    """
    return self.ProjectFor(pid).name

  def PathFor(self, pid):
    """Return the test project's path.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      Path to the project, always of the form '<test path>/<project ID>'.
    """
    return self.ProjectFor(pid).Path()

  def PathListRegexFor(self, pid):
    """Return the test project's path as a ListRegex.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay').

    Returns:
      partial_mock.ListRegex for project path.
    """
    return partial_mock.ListRegex('.*/%s' % self.PathFor(pid))

  def RevisionFor(self, pid):
    """Return the test project's revision.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay')

    Returns:
      Reivision for the project, always of form 'refs/heads/<project ID>'.
    """
    return self.ProjectFor(pid).Revision()

  def RemoteFor(self, pid):
    """Return the test project's remote name.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay')

    Returns:
      Remote name for the project, e.g. 'cros'.
    """
    return self.ProjectFor(pid).Remote().GitName()

  def ProjectFor(self, pid):
    """Return the test project's repo_manifest.Project.

    Args:
      pid: The test project ID (e.g. 'chromiumos-overlay')

    Returns:
      Corresponding repo_manifest.Project.
    """
    # Project paths always end with the project ID, so use that as key.
    match = [p for p in self.full_manifest.Projects() if p.Path().endswith(pid)]
    assert len(match) == 1
    return match[0]

  def setUp(self):
    # Parse and cache the full manifest to take advantage of the
    # utility functions in repo_manifest.
    self.full_manifest = repo_manifest.Manifest.FromString(FULL_XML)


class UtilitiesTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for all top-level utility functions."""

  def testCanBranchProjectAcceptsBranchableProjects(self):
    """Test CanBranchProject returns true when project is branchable."""
    for project in map(self.ProjectFor, BRANCHED_PROJECTS):
      self.assertTrue(CanBranchProject(project))

  def testCanBranchProjectRejectsNonBranchableProjects(self):
    """Test CanBranchProject returns false when project is not branchable."""
    for project in map(self.ProjectFor, NON_BRANCHED_PROJECTS):
      self.assertFalse(CanBranchProject(project))

  def testCanPinProjectAcceptsPinnedProjects(self):
    """Test CanPinProject returns true when project is pinned."""
    for project in map(self.ProjectFor, PINNED_PROJECTS):
      self.assertTrue(CanPinProject(project))

  def testCanPinProjectRejectsNonPinnedProjects(self):
    """Test CanPinProject returns false when project is not pinned."""
    for project in map(self.ProjectFor, BRANCHED_PROJECTS + TOT_PROJECTS):
      self.assertFalse(CanPinProject(project))

  def testTotMutualExclusivity(self):
    """Test CanBranch/PinProject both return false only when project is TOT."""
    for pid in PROJECTS.values():
      project = self.ProjectFor(pid)
      if not CanBranchProject(project) and not CanPinProject(project):
        self.assertIn(pid, TOT_PROJECTS)


class CheckoutManagerTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for CheckoutManager functions."""

  def AssertCommandCalledInProject(self, cmd, expected=True):
    """Assert the command was called inside the git repo.

    Args:
      cmd: Command as a list of arguments.
      expected: True if the command should have been called.
    """
    self.rc_mock.assertCommandContains(
        cmd,
        cwd=partial_mock.ListRegex('.*/' + self.project.Path()),
        expected=expected)

  def SetCurrentBranch(self, branch):
    """Mock git.GetCurrentBranch to always return the given branch.

    Args:
      branch: Name of the branch to return.
    """
    self.PatchObject(git, 'GetCurrentBranch', return_value=branch)

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    self.checkout = CrosCheckout('/', manifest=self.full_manifest)
    self.project = self.ProjectFor(PROJECTS.CHROMIUMOS_OVERLAY)

  def testEnterNoCheckout(self):
    """Test __enter__ does not checkout when already on desired branch."""
    self.SetCurrentBranch('master')
    with CheckoutManager(self.checkout, self.project):
      self.AssertCommandCalledInProject(['git', 'fetch'], expected=False)
      self.AssertCommandCalledInProject(['git', 'checkout'], expected=False)

  def testEnterWithCheckout(self):
    """Test __enter__ fetches and checkouts when not on desired branch."""
    self.SetCurrentBranch('branch')
    with CheckoutManager(self.checkout, self.project):
      self.AssertCommandCalledInProject(
          ['git', 'fetch', 'cros', 'refs/heads/master'])
      self.AssertCommandCalledInProject(['git', 'checkout', 'FETCH_HEAD'])

  def testExitNoCheckout(self):
    """Test __exit__ does not checkout when already on desired branch."""
    self.SetCurrentBranch('master')
    with CheckoutManager(self.checkout, self.project):
      pass
    self.AssertCommandCalledInProject(['git', 'checkout'], expected=False)

  def testExitWithCheckout(self):
    """Test __exit__ does checkouts old branch when not on desired branch."""
    self.SetCurrentBranch('branch')
    with CheckoutManager(self.checkout, self.project):
      pass
    self.AssertCommandCalledInProject(['git', 'checkout', 'refs/heads/branch'])


class ManifestRepositoryTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for ManifestRepository functions."""

  def GitRevisionMock(self, project):
    """Mock git.GetGitRepoRevision returning fake revision for given project.

    Args:
      project: Project to get the revision for.

    Returns:
      The repo HEAD as a string.
    """
    return project.Revision()

  def FromFileMock(self, path, allow_unsupported_features=False):
    """Forward repo_manifest.FromFile to repo_manifest.FromString.

    Args:
      path: File path for internal manifest. Used to look up XML in a table.
      allow_unsupported_features: See repo_manifest.Manifest.

    Returns:
      repo_manifest.Manifest created from test data.
    """
    return repo_manifest.Manifest.FromString(
        MANIFEST_INTERNAL_FILES[os.path.basename(path)],
        allow_unsupported_features=allow_unsupported_features)

  def setUp(self):
    self.PatchObject(CrosCheckout, 'GitRevision', self.GitRevisionMock)
    self.PatchObject(repo_manifest.Manifest, 'FromFile', self.FromFileMock)

    self.checkout = CrosCheckout('/root', manifest=self.full_manifest)
    self.project = self.ProjectFor(PROJECTS.MANIFEST_INTERNAL)
    self.manifest_repo = ManifestRepository(self.checkout, self.project)

  def testAbsoluteManifestPath(self):
    """Test AbsoluteManifestPath joins path with file name."""
    self.assertEqual(
        self.manifest_repo.AbsoluteManifestPath('test.xml'),
        '/root/manifest-internal/test.xml')

  def testListManifestsSingleFileNoIncludes(self):
    """Test ListManifests on a root file with no includes."""
    roots = expected = [EXTERNAL_FILE_NAME]
    actual = self.manifest_repo.ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testListManifestsSingleFileWithIncludes(self):
    """Test ListManifests on a root file with unique includes."""
    roots = [constants.DEFAULT_MANIFEST]
    expected = roots + [EXTERNAL_FILE_NAME, INTERNAL_FILE_NAME]
    actual = self.manifest_repo.ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testListManifestsMultipleFilesWithIncludes(self):
    """Test ListManifests on root files with shared includes."""
    roots = [constants.DEFAULT_MANIFEST, EXTERNAL_FILE_NAME]
    expected = roots + [INTERNAL_FILE_NAME]
    actual = self.manifest_repo.ListManifests(roots)
    self.assertItemsEqual(actual, expected)

  def testRepairManifestDeletesDefaultRevisions(self):
    """Test RepairManifest deletes revision attr on <default> and <remote>."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'beep',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'boop',
    }
    actual = self.manifest_repo.RepairManifest(INTERNAL_FILE_NAME, branches)
    self.assertIsNone(actual.Default().revision)
    self.assertIsNone(actual.GetRemote(REMOTES.CROS_INTERNAL).revision)

  def testRepairManifestUpdatesBranchedProjectRevisions(self):
    """Test RepairManifest updates revision=branch on branched projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'branch-a',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'branch-b'
    }
    actual = self.manifest_repo.RepairManifest(INTERNAL_FILE_NAME, branches)

    manifest_internal = actual.GetUniqueProject(
        self.NameFor(PROJECTS.MANIFEST_INTERNAL))
    self.assertEqual(manifest_internal.revision, 'refs/heads/branch-a')

    explicit_branch = actual.GetUniqueProject(
        self.NameFor(PROJECTS.EXPLICIT_BRANCH))
    self.assertEqual(explicit_branch.revision, 'refs/heads/branch-b')

  def testRepairManifestUpdatesPinnedProjectRevisions(self):
    """Test RepairManifest retains revision attr on pinned projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'irrelevant',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'should-not-matter'
    }
    actual = self.manifest_repo.RepairManifest(INTERNAL_FILE_NAME, branches)
    proj = actual.GetUniqueProject(self.NameFor(PROJECTS.EXPLICIT_PINNED))
    self.assertEqual(proj.revision, self.RevisionFor(PROJECTS.EXPLICIT_PINNED))

  def testRepairManifestUpdatesTotProjectRevisions(self):
    """Test RepairManifest sets revision=refs/heads/master on TOT projects."""
    branches = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'irrelevant',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'should-not-matter'
    }
    actual = self.manifest_repo.RepairManifest(INTERNAL_FILE_NAME, branches)
    proj = actual.GetUniqueProject(self.NameFor(PROJECTS.EXPLICIT_TOT))
    self.assertEqual(proj.revision, 'refs/heads/master')

  def testRepairManifestsOnDisk(self):
    """Test RepairManifestsOnDisk writes all manifests."""
    repair = self.PatchObject(ManifestRepository, 'RepairManifest',
                              return_value=self.full_manifest)
    write = self.PatchObject(repo_manifest.Manifest, 'Write')

    branches = [
        ProjectBranch(self.ProjectFor(PROJECTS.MANIFEST_INTERNAL), 'branch-a'),
        ProjectBranch(self.ProjectFor(PROJECTS.EXPLICIT_BRANCH), 'branch-b'),
    ]
    branches_by_path = {
        self.PathFor(PROJECTS.MANIFEST_INTERNAL): 'branch-a',
        self.PathFor(PROJECTS.EXPLICIT_BRANCH): 'branch-b',
    }

    self.manifest_repo.RepairManifestsOnDisk(branches)
    self.assertItemsEqual(repair.call_args_list, [
        mock.call('/root/manifest-internal/default.xml', branches_by_path),
        mock.call('/root/manifest-internal/official.xml', branches_by_path),
        mock.call('/root/manifest-internal/internal.xml', branches_by_path),
        mock.call('/root/manifest-internal/external.xml', branches_by_path),
    ])
    self.assertItemsEqual(write.call_args_list, [
        mock.call('/root/manifest-internal/default.xml'),
        mock.call('/root/manifest-internal/official.xml'),
        mock.call('/root/manifest-internal/internal.xml'),
        mock.call('/root/manifest-internal/external.xml'),
    ])


class CrosCheckoutTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for nontrivial methods in CrosCheckout."""

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    self.PatchObject(repo_util.Repository, '__init__', return_value=None)
    self.PatchObject(repo_util.Repository, 'Manifest',
                     return_value=self.full_manifest)
    self.PatchObject(VersionInfo, 'from_repo',
                     return_value=VersionInfo('1.2.3'))
    self.PatchObject(
        config_lib,
        'GetSiteParams',
        return_value=config_lib.AttrDict(
            EXTERNAL_MANIFEST_VERSIONS_PATH='manifest-versions',
            INTERNAL_MANIFEST_VERSIONS_PATH='manifest-versions-internal',
        ))
    self.get_current_branch = self.PatchObject(git, 'GetCurrentBranch',
                                               return_value='local-branch')
    self.get_git_repo_revision = self.PatchObject(git, 'GetGitRepoRevision',
                                                  return_value='abcdef')
    constants.CHROMITE_DIR = '/run-root/chromite'

  def testSyncVersionMinimal(self):
    """Test SyncVersion passes minimal args to repo_sync_manifest."""
    checkout = CrosCheckout('/root')
    checkout.SyncVersion('1.2.3')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--manifest-versions-int', '/root/manifest-versions-internal',
         '--manifest-versions-ext', '/root/manifest-versions',
         '--version', '1.2.3'])

  def testSyncVersionAllOptions(self):
    """Test SyncVersion passes all args to repo_sync_manifest."""
    checkout = CrosCheckout(
        '/root', repo_url='repo.com', manifest_url='manifest.com')
    checkout.SyncVersion('1.2.3')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--manifest-versions-int', '/root/manifest-versions-internal',
         '--manifest-versions-ext', '/root/manifest-versions',
         '--version', '1.2.3',
         '--repo-url', 'repo.com',
         '--manifest-url', 'manifest.com'])

  def testSyncBranchMinimal(self):
    """Test SyncBranch passes minimal args to repo_sync_manifest."""
    checkout = CrosCheckout('/root')
    checkout.SyncBranch('branch')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--branch', 'branch'])

  def testSyncBranchAllOptions(self):
    """Test SyncBranch passes all args to repo_sync_manifest."""
    checkout = CrosCheckout(
        '/root', repo_url='repo.com', manifest_url='manifest.com')
    checkout.SyncBranch('branch')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--branch', 'branch',
         '--repo-url', 'repo.com',
         '--manifest-url', 'manifest.com'])

  def testSyncFileMinimal(self):
    """Test SyncFile passes correct args to repo_sync_manifest."""
    checkout = CrosCheckout('/root')
    checkout.SyncFile('manifest.xml')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--manifest-file', 'manifest.xml'])

  def testSyncFileAllOptions(self):
    """Test SyncFile passes all args to repo_sync_manifest."""
    checkout = CrosCheckout(
        '/root', repo_url='repo.com', manifest_url='manifest.com')
    checkout.SyncFile('manifest.xml')
    self.rc_mock.assertCommandContains(
        ['/run-root/chromite/scripts/repo_sync_manifest',
         '--repo-root', '/root',
         '--manifest-file', 'manifest.xml',
         '--repo-url', 'repo.com',
         '--manifest-url', 'manifest.com'])

  def testAbsolutePath(self):
    """Test AbsolutePath joins root to given path."""
    checkout = CrosCheckout('/foo')
    self.assertEqual(checkout.AbsolutePath('bar'), '/foo/bar')

  def testAbsoluteProjectPath(self):
    """Test AbsoluteProjectPath joins root and project path."""
    checkout = CrosCheckout('/foo')
    project = self.ProjectFor(PROJECTS.MANIFEST)
    actual = checkout.AbsoluteProjectPath(project, 'bar')
    self.assertEqual(actual, '/foo/manifest/bar')

  def testReadVersion(self):
    """Test ReadVersion does not modify VersionInfo."""
    checkout = CrosCheckout('/root')
    vinfo = checkout.ReadVersion()
    self.assertEqual(vinfo.build_number, '1')
    self.assertEqual(vinfo.branch_build_number, '2')
    self.assertEqual(vinfo.patch_number, '3')

  def testRunGit(self):
    """Test RunGit runs git command in project directory."""
    checkout = CrosCheckout('/root')
    project = self.ProjectFor(PROJECTS.MANIFEST)

    checkout.RunGit(project, ['branch', '-m', 'foo'])
    self.rc_mock.assertCommandContains(
        ['git', 'branch', '-m', 'foo'],
        cwd='/root/manifest',
        print_cmd=True)

  def testGitRevision(self):
    """Test GitRevision properly forwards project path."""
    checkout = CrosCheckout('/root')
    project = self.ProjectFor(PROJECTS.MANIFEST)

    actual = checkout.GitRevision(project)
    self.assertEqual(
        self.get_git_repo_revision.call_args_list,
        [mock.call('/root/manifest')])
    self.assertEqual(actual, 'abcdef')

  def testGitBranch(self):
    """Test GitBranch properly forwards project path."""
    checkout = CrosCheckout('/root')
    project = self.ProjectFor(PROJECTS.MANIFEST)

    actual = checkout.GitBranch(project)
    self.assertEqual(
        self.get_current_branch.call_args_list,
        [mock.call('/root/manifest')])
    self.assertEqual(actual, 'local-branch')


class BranchTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests core functionality of Branch class."""

  def SetVersion(self, version):
    """Mock VersionInfo.from_repo to always return the given version.

    Args:
      version: The version string to return.
    """
    self.PatchObject(CrosCheckout, 'ReadVersion',
                     return_value=VersionInfo(version))

  def AssertProjectBranched(self, project, branch):
    """Assert branch created for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'checkout', '-B', branch],
        cwd=self.PathListRegexFor(project))

  def AssertBranchRenamed(self, project, branch):
    """Assert current branch renamed for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch', '-m', branch],
        cwd=self.PathListRegexFor(project))

  def AssertBranchDeleted(self, project, branch):
    """Assert given branch deleted for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch', '-D', branch],
        cwd=self.PathListRegexFor(project))

  def AssertProjectNotBranched(self, project):
    """Assert no branch was created for the given project.

    Args:
      project: Project ID.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'checkout', '-B'],
        cwd=self.PathListRegexFor(project),
        expected=False)

  def AssertBranchNotModified(self, project):
    """Assert no `git branch` calls for given project.

    Args:
      project: Project ID.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'branch'],
        cwd=self.PathListRegexFor(project),
        expected=False)

  def AssertBranchPushed(self, project, branch):
    """Assert given branch pushed to remote for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'push', self.RemoteFor(project),
         'refs/heads/%s:refs/heads/%s' % (branch, branch)],
        cwd=self.PathListRegexFor(project))

  def AssertRemoteBranchDeleted(self, project, branch):
    """Assert given branch deleted on remote for given project.

    Args:
      project: Project ID.
      branch: Expected name for the branch.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'push', self.RemoteFor(project), '--delete',
         'refs/heads/%s' % branch],
        cwd=self.PathListRegexFor(project))

  def AssertNoPush(self, project):
    """Assert no push operation run inside the given project.

    Args:
      project: Project ID.
    """
    self.rc_mock.assertCommandContains(
        ['git', 'push'],
        cwd=self.PathListRegexFor(project),
        expected=False)

  def AssertManifestRepairsCommitted(self):
    """Assert commits made to all manifest repositories."""
    for manifest_project in MANIFEST_PROJECTS:
      self.rc_mock.assertCommandContains(
          ['git', 'commit', '-a'],
          cwd=partial_mock.ListRegex('.*/%s' % manifest_project))

  def setUp(self):
    self.rc_mock = cros_test_lib.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    self.StartPatcher(self.rc_mock)

    # ManifestRepository and CrosCheckout tested separately, so mock them.
    self.PatchObject(ManifestRepository, 'RepairManifestsOnDisk')
    self.PatchObject(CrosCheckout, 'ReadVersion',
                     return_value=VersionInfo('1.2.0'))
    self.bump_version = self.PatchObject(CrosCheckout, 'BumpVersion')

    # The instance under test.
    self.checkout = CrosCheckout('/', manifest=self.full_manifest)
    self.branch = Branch('branch', self.checkout)

  def testCreateBranchesCorrectProjects(self):
    """Test Create branches the correct projects with correct branch names."""
    self.branch.Create()
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertProjectNotBranched(project)

  def testCreateRepairsManifests(self):
    """Test Create commits repairs to manifest repositories."""
    self.branch.Create()
    self.AssertManifestRepairsCommitted()

  def testCreateBumpsBranchNumber(self):
    """Test WhichVersionShouldBump bumps branch number on X.0.0 version."""
    self.SetVersion('1.0.0')
    self.branch.Create()
    self.assertEqual(self.bump_version.call_args_list,
                     [mock.call('branch', mock.ANY)])

  def testCreateBumpsPatchNumber(self):
    """Test WhichVersionShouldBump bumps patch number on X.X.0 version."""
    self.SetVersion('1.2.0')
    self.branch.Create()
    self.assertEqual(self.bump_version.call_args_list,
                     [mock.call('patch', mock.ANY)])

  def testCreateDiesOnNonzeroPatchNumber(self):
    """Test WhichVersionShouldBump dies on X.X.X version."""
    self.SetVersion('1.2.3')
    with self.assertRaises(BranchError):
      self.branch.Create()

  def testCreatePushesToRemote(self):
    """Test Create pushes new branch to remote."""
    self.branch.Create(push=True)
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchPushed(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchPushed(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertNoPush(project)

  def testRenameCreatesNewBranch(self):
    """Test Rename creates a branch with the new name."""
    self.branch.Rename('original')
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertProjectBranched(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertProjectNotBranched(project)

  def testRenameDeletesOldBranch(self):
    """Test Rename deletes the original branch."""
    self.branch.Rename('original')
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'original')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'original-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertBranchNotModified(project)

  def testRenameRepairsManifests(self):
    """Test Rename commits repairs to manifest repositories."""
    self.branch.Rename('original')
    self.AssertManifestRepairsCommitted()

  def testRenamePushesNewBranch(self):
    """Test Rename pushes the new branch to remote."""
    self.branch.Rename('original', push=True)
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchPushed(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchPushed(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertNoPush(project)

  def testRenamePushesDeletionOfOldBranch(self):
    self.branch.Rename('original', push=True)
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertRemoteBranchDeleted(project, 'original')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertRemoteBranchDeleted(project, 'original-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertNoPush(project)

  def testDeleteModifiesCorrectProjects(self):
    """Test Delete deletes correct project branches."""
    self.branch.Delete()
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertBranchDeleted(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertBranchNotModified(project)

  def testDeleteRequiresForceForRemotePush(self):
    """Verify Delete does nothing when push is True but force is False."""
    with self.assertRaises(BranchError):
      self.branch.Delete(push=True)
    for project in PROJECTS.values():
      self.AssertBranchNotModified(project)
      self.AssertNoPush(project)

  def testDeletePushesDeletions(self):
    """Verify delete deletes remote branches when push=force=True."""
    self.branch.Delete(push=True, force=True)
    for project in SINGLE_CHECKOUT_PROJECTS:
      self.AssertRemoteBranchDeleted(project, 'branch')
    for project in MULTI_CHECKOUT_PROJECTS:
      self.AssertRemoteBranchDeleted(project, 'branch-' + project)
    for project in NON_BRANCHED_PROJECTS:
      self.AssertNoPush(project)


class StandardBranchTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests branch logic specific to the standard branches."""

  def SetVersion(self, milestone, version):
    """Mock VersionInfo to always return the given versions.

    Args:
      milestone: The Chrome branch number, e.g. '47'
      version: The manifest version string, e.g. '1.2.0'
    """
    self.PatchObject(
        CrosCheckout,
        'ReadVersion',
        return_value=VersionInfo(version, milestone))

  def setUp(self):
    self.checkout = CrosCheckout('/', manifest=self.full_manifest)

  def testGenerateNameWithoutBranchVersion(self):
    """Test GenerateName on a X.0.0 version."""
    self.SetVersion('12', '3.0.0')
    branch_names = {
        'release-R12-3.B': ReleaseBranch,
        'factory-3.B': FactoryBranch,
        'firmware-3.B': FirmwareBranch,
        'stabilize-3.B': StabilizeBranch,
    }
    for branch_name, branch_type in branch_names.iteritems():
      self.assertEqual(branch_type(self.checkout).name, branch_name)

  def testGenerateNameWithBranchVersion(self):
    """Test GenerateName on a X.X.0 version."""
    self.SetVersion('12', '3.4.0')
    branch_names = {
        'release-R12-3.4.B': ReleaseBranch,
        'factory-3.4.B': FactoryBranch,
        'firmware-3.4.B': FirmwareBranch,
        'stabilize-3.4.B': StabilizeBranch,
    }
    for branch_name, cls in branch_names.iteritems():
      self.assertEqual(cls(self.checkout).name, branch_name)


class MockBranchCommand(command_unittest.MockCommand):
  """Mock out the `cros branch` command."""
  TARGET = 'chromite.cli.cros.cros_branch.BranchCommand'
  TARGET_CLASS = BranchCommand
  COMMAND = 'branch'


class BranchCommandTest(ManifestTestCase, cros_test_lib.MockTestCase):
  """Tests for BranchCommand functions."""

  def RunCommandMock(self, args):
    """Patch the mock command and run it.

    Args:
      args: List of arguments for the command.
    """
    self.cmd = MockBranchCommand(args)
    self.StartPatcher(self.cmd)
    self.cmd.inst.Run()

  def AssertSynced(self, args):
    """Assert repo_sync_manifest was run with at least the given args.

    Args:
      args: Expected args for repo_sync_manifest.
    """
    self.cmd.rc_mock.assertCommandContains(
        [partial_mock.ListRegex('.*/repo_sync_manifest')] + args)

  def AssertNoDangerousOptions(self):
    """Assert that force and push were not set."""
    self.assertFalse(self.cmd.inst.options.force)
    self.assertFalse(self.cmd.inst.options.push)

  def setUp(self):
    self.cmd = None
    self.PatchObject(Branch, 'Create')
    self.PatchObject(Branch, 'Rename')
    self.PatchObject(Branch, 'Delete')
    self.PatchObject(repo_util.Repository, 'Manifest',
                     return_value=self.full_manifest)

  def testCreateReleaseCommandParses(self):
    """Test `cros branch create` parses with '--release' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--release'])
    self.assertIs(self.cmd.inst.options.cls, ReleaseBranch)
    self.AssertNoDangerousOptions()

  def testCreateFactoryCommandParses(self):
    """Test `cros branch create` parses with '--factory' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--factory'])
    self.assertIs(self.cmd.inst.options.cls, FactoryBranch)
    self.AssertNoDangerousOptions()

  def testCreateFirmwareCommandParses(self):
    """Test `cros branch create` parses with '--firmware' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--firmware'])
    self.assertIs(self.cmd.inst.options.cls, FirmwareBranch)
    self.AssertNoDangerousOptions()

  def testCreateStabilizeCommandParses(self):
    """Test `cros branch create` parses with '--stabilize' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--stabilize'])
    self.assertIs(self.cmd.inst.options.cls, StabilizeBranch)
    self.AssertNoDangerousOptions()

  def testCreateCustomCommandParses(self):
    """Test `cros branch create` parses with '--custom' flag."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--custom', 'branch'])
    self.assertEqual(self.cmd.inst.options.name, 'branch')
    self.AssertNoDangerousOptions()

  def testCreateSyncsToFile(self):
    """Test `cros branch create` calls repo_sync_manifest to sync to file."""
    self.RunCommandMock(['create', '--file', 'manifest.xml', '--stabilize'])
    self.AssertSynced(['--manifest-file', 'manifest.xml'])

  def testCreateSyncsToVersion(self):
    """Test `cros branch create` calls repo_sync_manifest to sync to version."""
    self.RunCommandMock(['create', '--version', '1.2.0', '--stabilize'])
    self.AssertSynced(['--version', '1.2.0'])

  def testRenameSyncsToBranch(self):
    """Test `cros branch rename` calls repo_sync_manifest to sync to branch."""
    self.RunCommandMock(['rename', 'branch', 'new-branch'])
    self.AssertSynced(['--branch', 'branch'])

  def testDeleteSyncsToBranch(self):
    """Test `cros branch delete` calls repo_sync_manifest to sync to branch."""
    self.RunCommandMock(['delete', 'branch'])
    self.AssertSynced(['--branch', 'branch'])


class FunctionalTest(ManifestTestCase, cros_test_lib.TempDirTestCase):
  """Test `cros branch` end to end on data generated from ManifestTestCase.

  This test creates external and internal "remotes" on disk using the test
  data generated by ManifestTestCase. A local checkout is also created by
  running `repo sync` on the fake internal remote. Projects on the remote
  are built from empty commits, with three exceptions: chromite, which
  contains the code under test, and manifest/manifest-internal, which contain
  test manifests.
  """

  def CreateTempDir(self, *args):
    """Create a temporary directory and return its absolute path.

    Args:
      args: Arbitrary subdirectories.

    Returns:
      Absolute path to new temporary directory.
    """
    path = os.path.join(self.tempdir, *args)
    osutils.SafeMakedirs(path)
    return path

  def CreateRef(self, git_repo, ref):
    """Create a ref in a git repository.

    The ref will point to a new commit containing all previously unstaged
    changes. If there are no active changes in the repo, the ref will point to a
    new, empty commit.

    Args:
      git_repo: Path to the repository.
      ref: Name of the ref to create.
    """
    git.RunGit(git_repo, ['add', '-A'])
    git.Commit(git_repo, 'Ref %s.' % ref, allow_empty=True)
    git.CreateBranch(git_repo, git.StripRefs(ref))

  def CreateProjectsOnRemote(self, remote, projects):
    """Create remote git repos for the given projects.

    This method creates two refs for each project: TOT, i.e. a master branch,
    and a project-specific branch. Any files in the project's directory will
    exist on both branches.

    Args:
      remote: Name of the remote.
      projects: List of projects IDs to be created on the remote.
    """
    for project in projects:
      repo_path = self.CreateTempDir(remote, self.NameFor(project))
      git.Init(repo_path)
      self.CreateRef(repo_path, 'master')
      self.CreateRef(repo_path, self.RevisionFor(project))

  def WriteVersionFile(self, milestone, build, branch, patch):
    """Write chromeos_version.sh to the remote with given version numbers.

    Args:
      milestone: The Chrome branch number.
      build: The Chrome OS build number.
      branch: The branch build number.
      patch: The patch build number.
    """
    content = '\n'.join([
        '#!/bin/sh',
        'CHROME_BRANCH=%d' % milestone,
        'CHROMEOS_BUILD=%d' % build,
        'CHROMEOS_BRANCH=%d' % branch,
        'CHROMEOS_PATCH=%d' % patch,
    ])
    version_file_dir = self.CreateTempDir(
        REMOTES.CROS,
        self.NameFor(PROJECTS.CHROMIUMOS_OVERLAY),
        'chromeos/config')
    version_file_path = os.path.join(version_file_dir, 'chromeos_version.sh')
    osutils.WriteFile(version_file_path, content)

  def WriteManifest(self, manifest, path):
    """Write the manifest to the given file name at the given path.

    This method also repairs remote fetch paths, which is not known
    when the test data is generated.

    Args:
      manifest: The repo_manifest.Manifest to write.
      path: The path to write it at.
    """
    for remote in manifest.Remotes():
      remote.fetch = (self.cros_root if remote.GitName() == REMOTES.CROS else
                      self.cros_internal_root)
    manifest.Write(path)

  def WriteManifestFiles(self, remote, project, files):
    """Write all manifest files to the given remote.

    Args:
      remote: Name of the remote.
      project: Manifest project ID.
      files: Dict mapping file name to string XML contents.

    Returns:
      Path to the created manifest project.
    """
    repo_path = self.CreateTempDir(remote, self.NameFor(project))
    for filename, xml in files.iteritems():
      manifest = ParseManifestXml(xml)
      self.WriteManifest(manifest, os.path.join(repo_path, filename))
    return repo_path

  def setUp(self):
    # Create the remotes. We must create all root directories first
    # because remotes typically know about each other.
    self.cros_root = self.CreateTempDir(REMOTES.CROS)
    self.cros_internal_root = self.CreateTempDir(REMOTES.CROS_INTERNAL)

    # Add necessary files to remote before creating git repos.
    self.WriteVersionFile(12, 3, 4, 0)
    self.WriteManifestFiles(REMOTES.CROS, PROJECTS.MANIFEST, MANIFEST_FILES)
    self.manifest_internal_root = self.WriteManifestFiles(
        REMOTES.CROS_INTERNAL,
        PROJECTS.MANIFEST_INTERNAL,
        MANIFEST_INTERNAL_FILES)

    self.CreateProjectsOnRemote(REMOTES.CROS, EXTERNAL_PROJECTS)
    self.CreateProjectsOnRemote(REMOTES.CROS_INTERNAL, INTERNAL_PROJECTS)

    # We want to branch from the full manifest, so put it somewhere accessbile.
    self.full_manifest_path = os.path.join(self.tempdir, 'manifest.xml')
    self.WriteManifest(self.full_manifest, self.full_manifest_path)

    # "Locally" checkout the internal remote.
    self.repo_url = FileUrl(constants.CHROOT_SOURCE_ROOT, '.repo/repo')
    self.local_root = self.CreateTempDir('local')
    repo_util.Repository.Initialize(
        root=self.local_root,
        manifest_url=self.manifest_internal_root,
        repo_url=self.repo_url,
        repo_branch='default')

  def testCreate(self):
    """Test create runs without dying."""
    cros_build_lib.RunCommand(
        ['cros', 'branch',
         '--push',
         '--root', self.local_root,
         '--repo-url', self.repo_url,
         '--manifest-url', self.manifest_internal_root,
         'create',
         '--file', self.full_manifest_path,
         '--custom', 'new-branch'])
