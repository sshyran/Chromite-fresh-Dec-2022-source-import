# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for GerritHelper.

Most of the tests in this file reach out to a staging/test Gerrit server. By
default, this server is t3st-chr0m3-review.googlesource.com. These tests will
be skipped unless run_tests is passed the '--network' arg:
$ ./run_tests --network -- lib/gerrit_unittest.py
"""

import collections
import http.client
import http.cookiejar
import io
import json
import os
import re
import shutil
import stat
from unittest import mock
import urllib.parse

from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import gerrit
from chromite.lib import git
from chromite.lib import gob_util
from chromite.lib import osutils


class GerritTestCase(cros_test_lib.MockTempDirTestCase):
  """Test class for tests that interact with a Gerrit server.

  Configured by default to use a specially-configured test Gerrit server at
  t3st-chr0m3(-review).googlesource.com. The test server configuration may be
  altered by setting the following environment variables from the parent
  process:
    CROS_TEST_GIT_HOST: host name for git operations; defaults to
                        t3st-chr0me.googlesource.com.
    CROS_TEST_GERRIT_HOST: host name for Gerrit operations; defaults to
                           t3st-chr0me-review.googlesource.com.
    CROS_TEST_COOKIES_PATH: path to a cookies.txt file to use for git/Gerrit
                            requests; defaults to ~/.gitcookies.
    CROS_TEST_COOKIE_NAMES: comma-separated list of cookie names from
                            CROS_TEST_COOKIES_PATH to set on requests; defaults
                            to none. The current implementation only sends
                            cookies matching the exact host name and the empty
                            path ("/").
  """

  # pylint: disable=protected-access

  TEST_USERNAME = 'test-username'
  TEST_EMAIL = 'test-username@test.org'

  GerritInstance = collections.namedtuple('GerritInstance', [
      'cookie_names',
      'cookies_path',
      'gerrit_host',
      'gerrit_url',
      'git_host',
      'git_url',
      'project_prefix',
  ])

  def _create_gerrit_instance(self, tmp_dir):
    default_host = 't3st-chr0m3'
    git_host = os.environ.get('CROS_TEST_GIT_HOST',
                              constants.GOB_HOST % default_host)
    gerrit_host = os.environ.get('CROS_TEST_GERRIT_HOST',
                                 '%s-review.googlesource.com' % default_host)
    project_prefix = 'test-%s/' % (cros_build_lib.GetRandomString(),)
    cookies_path = os.environ.get('CROS_TEST_COOKIES_PATH',
                                  constants.GITCOOKIES_PATH)
    # "o" is the cookie name that GoB uses in its instructions.
    cookie_names_str = os.environ.get('CROS_TEST_COOKIE_NAMES', 'o')
    cookie_names = {c for c in cookie_names_str.split(',') if c}

    tmpcookies_path = os.path.join(tmp_dir, '.gitcookies')
    if os.path.exists(cookies_path):
      shutil.copy(cookies_path, tmpcookies_path)
    else:
      osutils.Touch(tmpcookies_path)

    return self.GerritInstance(
        cookie_names=cookie_names,
        cookies_path=tmpcookies_path,
        gerrit_host=gerrit_host,
        gerrit_url='https://%s/' % gerrit_host,
        git_host=git_host,
        git_url='https://%s/' % git_host,
        project_prefix=project_prefix,)

  def setUp(self):
    """Sets up the gerrit instances in a class-specific temp dir."""
    self.saved_params = {}
    os.environ['HOME'] = self.tempdir

    # Create gerrit instance.
    gi = self.gerrit_instance = self._create_gerrit_instance(self.tempdir)

    # This --global will use our tempdir $HOME we set above, not the real ~/.
    cros_build_lib.run(
        ['git', 'config', '--global', 'http.cookiefile', gi.cookies_path],
        quiet=True)

    # If you're seeing "does not look like a Netscape format cookies file"
    # errors here, make sure the first line in your gitcookies file is:
    # "# HTTP Cookie File"
    # TODO(b/210490942): Detect and handle this automatically.
    jar = http.cookiejar.MozillaCookieJar(gi.cookies_path)
    jar.load(ignore_expires=True)

    def GetCookies(host, _path):
      return dict(
          (c.name, urllib.parse.unquote(c.value)) for c in jar
          if c.domain == host and c.path == '/' and c.name in gi.cookie_names)

    self.PatchObject(gob_util, 'GetCookies', GetCookies)

    site_params = config_lib.GetSiteParams()

    # Make all chromite code point to the test server.
    self.patched_params = {
        'EXTERNAL_GOB_HOST': gi.git_host,
        'EXTERNAL_GERRIT_HOST': gi.gerrit_host,
        'EXTERNAL_GOB_URL': gi.git_url,
        'EXTERNAL_GERRIT_URL': gi.gerrit_url,
        'INTERNAL_GOB_HOST': gi.git_host,
        'INTERNAL_GERRIT_HOST': gi.gerrit_host,
        'INTERNAL_GOB_URL': gi.git_url,
        'INTERNAL_GERRIT_URL': gi.gerrit_url,
        'AOSP_GOB_HOST': gi.git_host,
        'AOSP_GERRIT_HOST': gi.gerrit_host,
        'AOSP_GOB_URL': gi.git_url,
        'AOSP_GERRIT_URL': gi.gerrit_url,

        'MANIFEST_URL': '%s/%s' % (
            gi.git_url, site_params.MANIFEST_PROJECT
        ),
        'MANIFEST_INT_URL': '%s/%s' % (
            gi.git_url, site_params.MANIFEST_INT_PROJECT
        ),
        'GIT_REMOTES': {
            site_params.EXTERNAL_REMOTE: gi.gerrit_url,
            site_params.INTERNAL_REMOTE: gi.gerrit_url,
            site_params.CHROMIUM_REMOTE: gi.gerrit_url,
            site_params.CHROME_REMOTE: gi.gerrit_url
        }
    }

    for k in self.patched_params.keys():
      self.saved_params[k] = site_params.get(k)

    site_params.update(self.patched_params)

  def tearDown(self):
    # Restore the 'patched' site parameters.
    site_params = config_lib.GetSiteParams()
    site_params.update(self.saved_params)

  def createProject(self, suffix, description='Test project', owners=None,
                    submit_type='CHERRY_PICK'):
    """Create a project on the test gerrit server."""
    name = self.gerrit_instance.project_prefix + suffix
    body = {
        'description': description,
        'submit_type': submit_type,
        'branches': ['main'],
    }
    if owners is not None:
      body['owners'] = owners
    path = 'projects/%s' % urllib.parse.quote(name, '')
    response = gob_util.CreateHttpConn(
        self.gerrit_instance.gerrit_host, path, reqtype='PUT', body=body)
    self.assertEqual(201, response.status,
                     'Expected 201, got %s' % response.status)
    s = io.BytesIO(response.read())
    self.assertEqual(b")]}'", s.readline().rstrip())
    jmsg = json.load(s)
    self.assertEqual(name, jmsg['name'])
    return name

  def _CloneProject(self, name, path):
    """Clone a project from the test gerrit server."""
    root = os.path.dirname(path)
    osutils.SafeMakedirs(root)
    url = '%s://%s/%s' % (
        gob_util.GIT_PROTOCOL, self.gerrit_instance.git_host, name)
    git.RunGit(root, ['clone', url, path])
    # Install commit-msg hook.
    hook_path = os.path.join(path, '.git', 'hooks', 'commit-msg')
    hook_cmd = ['curl', '-n', '-o', hook_path,
                '-b', self.gerrit_instance.cookies_path]
    hook_cmd.append('https://%s/a/tools/hooks/commit-msg'
                    % self.gerrit_instance.gerrit_host)
    cros_build_lib.run(hook_cmd, quiet=True)
    os.chmod(hook_path, stat.S_IRWXU)
    # Set git identity to test account
    cros_build_lib.run(
        ['git', 'config', 'user.email', self.TEST_EMAIL], cwd=path, quiet=True)
    return path

  def cloneProject(self, name, path=None):
    """Clone a project from the test gerrit server."""
    if path is None:
      path = os.path.basename(name)
      if path.endswith('.git'):
        path = path[:-4]
    path = os.path.join(self.tempdir, path)
    return self._CloneProject(name, path)

  @classmethod
  def _CreateCommit(cls, clone_path, filename=None, msg=None, text=None,
                    amend=False):
    """Create a commit in the given git checkout.

    Args:
      clone_path: The directory on disk of the git clone.
      filename: The name of the file to write. Optional.
      msg: The commit message. Optional.
      text: The text to append to the file. Optional.
      amend: Whether to amend an existing patch. If set, we will amend the
        HEAD commit in the checkout and upload that patch.

    Returns:
      (sha1, changeid) of the new commit.
    """
    if not filename:
      filename = 'test-file.txt'
    if not msg:
      msg = 'Test Message'
    if not text:
      text = 'Another day, another dollar.'
    fpath = os.path.join(clone_path, filename)
    osutils.WriteFile(fpath, '%s\n' % text, mode='a')
    cros_build_lib.run(['git', 'add', filename], cwd=clone_path, quiet=True)
    cmd = ['git', 'commit']
    cmd += ['--amend', '-C', 'HEAD'] if amend else ['-m', msg]
    cros_build_lib.run(cmd, cwd=clone_path, quiet=True)
    return cls._GetCommit(clone_path)

  def createCommit(self, clone_path, filename=None, msg=None, text=None,
                   amend=False):
    """Create a commit in the given git checkout.

    Args:
      clone_path: The directory on disk of the git clone.
      filename: The name of the file to write. Optional.
      msg: The commit message. Optional.
      text: The text to append to the file. Optional.
      amend: Whether to amend an existing patch. If set, we will amend the
        HEAD commit in the checkout and upload that patch.
    """
    clone_path = os.path.join(self.tempdir, clone_path)
    return self._CreateCommit(clone_path, filename, msg, text, amend)

  @staticmethod
  def _GetCommit(clone_path, ref='HEAD'):
    log_proc = cros_build_lib.run(
        ['git', 'log', '-n', '1', ref], cwd=clone_path,
        print_cmd=False, capture_output=True, encoding='utf-8')
    sha1 = None
    change_id = None
    for line in log_proc.stdout.splitlines():
      match = re.match(r'^commit ([0-9a-fA-F]{40})$', line)
      if match:
        sha1 = match.group(1)
        continue
      match = re.match(r'^\s+Change-Id:\s*(\S+)$', line)
      if match:
        change_id = match.group(1)
        continue
    return (sha1, change_id)

  def getCommit(self, clone_path, ref='HEAD'):
    """Get the sha1 and change-id for the head commit in a git checkout."""
    clone_path = os.path.join(self.tempdir, clone_path)
    (sha1, change_id) = self._GetCommit(clone_path, ref)
    self.assertTrue(sha1)
    self.assertTrue(change_id)
    return (sha1, change_id)

  @staticmethod
  def _UploadChange(clone_path, branch='main', remote='origin'):
    cros_build_lib.run(
        ['git', 'push', remote, 'HEAD:refs/for/%s' % branch], cwd=clone_path,
        quiet=True)

  def uploadChange(self, clone_path, branch='main', remote='origin'):
    """Create a gerrit CL from the HEAD of a git checkout."""
    clone_path = os.path.join(self.tempdir, clone_path)
    self._UploadChange(clone_path, branch, remote)

  @staticmethod
  def _PushBranch(clone_path, branch='main'):
    cros_build_lib.run(
        ['git', 'push', 'origin', 'HEAD:refs/heads/%s' % branch],
        cwd=clone_path, quiet=True)

  def pushBranch(self, clone_path, branch='main'):
    """Push a branch directly to gerrit, bypassing code review."""
    clone_path = os.path.join(self.tempdir, clone_path)
    self._PushBranch(clone_path, branch)

  def createAccount(self, name='Test User', email='test-user@test.org',
                    password=None, groups=None):
    """Create a new user account on gerrit."""
    username = urllib.parse.quote(email.partition('@')[0])
    path = 'accounts/%s' % username
    body = {
        'name': name,
        'email': email,
    }

    if password:
      body['http_password'] = password
    if groups:
      if isinstance(groups, str):
        groups = [groups]
      body['groups'] = groups
    response = gob_util.CreateHttpConn(
        self.gerrit_instance.gerrit_host, path, reqtype='PUT', body=body)
    self.assertEqual(201, response.status)
    s = io.BytesIO(response.read())
    self.assertEqual(b")]}'", s.readline().rstrip())
    jmsg = json.load(s)
    self.assertEqual(email, jmsg['email'])


@cros_test_lib.pytestmark_network_test
class GerritHelperTest(GerritTestCase):
  """Unittests for GerritHelper."""

  def _GetHelper(self, remote=config_lib.GetSiteParams().EXTERNAL_REMOTE):
    return gerrit.GetGerritHelper(remote)

  def createPatch(self, clone_path, project, remote='origin', **kwargs):
    """Create a patch in the given git checkout and upload it to gerrit.

    Args:
      clone_path: The directory on disk of the git clone.
      project: The associated project.
      remote: The remote to upload changes to.
      **kwargs: Additional keyword arguments to pass to createCommit.

    Returns:
      A GerritPatch object.
    """
    (revision, changeid) = self.createCommit(clone_path, **kwargs)
    helper = self._GetHelper()
    gpatch = helper.CreateGerritPatch(clone_path, remote, 'main',
                                      project=project)
    self.assertEqual(gpatch.change_id, changeid)
    self.assertEqual(gpatch.revision, revision)
    return gpatch

  def testSimpleQuery(self):
    """Create one independent and three dependent changes, then query them."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    (head_sha1, head_changeid) = self.createCommit(clone_path)
    for idx in range(3):
      cros_build_lib.run(
          ['git', 'checkout', head_sha1], cwd=clone_path, quiet=True)
      self.createCommit(clone_path, filename='test-file-%d.txt' % idx)
      self.uploadChange(clone_path)
    helper = self._GetHelper()
    changes = helper.Query(owner='self', project=project)
    self.assertEqual(len(changes), 4)
    changes = helper.Query(head_changeid, project=project, branch='main')
    self.assertEqual(len(changes), 1)
    self.assertEqual(changes[0].change_id, head_changeid)
    self.assertEqual(changes[0].sha1, head_sha1)
    change = helper.QuerySingleRecord(
        head_changeid, project=project, branch='main')
    self.assertTrue(change)
    self.assertEqual(change.change_id, head_changeid)
    self.assertEqual(change.sha1, head_sha1)
    change = helper.GrabPatchFromGerrit(project, head_changeid, head_sha1)
    self.assertTrue(change)
    self.assertEqual(change.change_id, head_changeid)
    self.assertEqual(change.sha1, head_sha1)

  @mock.patch.object(gerrit.GerritHelper, '_GERRIT_MAX_QUERY_RETURN', 2)
  def testGerritQueryTruncation(self):
    """Verify that we detect gerrit truncating our query, and handle it."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    # Using a shell loop is markedly faster than running a python loop.
    num_changes = 5
    cmd = ('for ((i=0; i<%i; i=i+1)); do '
           'echo "Another day, another dollar." > test-file-$i.txt; '
           'git add test-file-$i.txt; '
           'git commit -m "Test commit $i."; '
           'done' % num_changes)
    cros_build_lib.run(cmd, shell=True, cwd=clone_path, quiet=True)
    self.uploadChange(clone_path)
    helper = self._GetHelper()
    changes = helper.Query(project=project)
    self.assertEqual(len(changes), num_changes)

  def testIsChangeCommitted(self):
    """Tests that we can parse a json to check if a change is committed."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    gpatch = self.createPatch(clone_path, project)
    helper = self._GetHelper()
    helper.SetReview(gpatch.gerrit_number, labels={'Code-Review':'+2'})
    helper.SubmitChange(gpatch)
    self.assertTrue(helper.IsChangeCommitted(gpatch.gerrit_number))

    gpatch = self.createPatch(clone_path, project)
    self.assertFalse(helper.IsChangeCommitted(gpatch.gerrit_number))

  def testGetLatestSHA1ForBranch(self):
    """Verifies that we can query the tip-of-tree commit in a git repository."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    for _ in range(5):
      (main_sha1, _) = self.createCommit(clone_path)
    self.pushBranch(clone_path, 'main')
    for _ in range(5):
      (testbranch_sha1, _) = self.createCommit(clone_path)
    self.pushBranch(clone_path, 'testbranch')
    helper = self._GetHelper()
    self.assertEqual(
        helper.GetLatestSHA1ForBranch(project, 'main'),
        main_sha1)
    self.assertEqual(
        helper.GetLatestSHA1ForBranch(project, 'testbranch'),
        testbranch_sha1)

  def testChangeEdit(self):
    """Verifies that CreateChange & ChangeEdit can create CLs with changes."""
    project = self.createProject('testProject')
    # Gerrit returns "Destination branch does not exist" errors if we don't push
    # something onto the new project's branch.
    clone_path = self.cloneProject(project)
    self.createCommit(clone_path)
    self.pushBranch(clone_path, 'main')
    helper = self._GetHelper()
    # There should be no changes in our project that touch some_file.
    file_path = 'some_file'
    self.assertEqual(len(helper.Query(project=project, path=file_path)), 0)
    change = helper.CreateChange(project, 'main', 'Test Change', True)
    helper.ChangeEdit(change.gerrit_number, file_path, 'some file contents')
    # After creating the change and adding a file modification, there should be
    # a single change that touches some_file in our project.
    self.assertEqual(len(helper.Query(project=project, path=file_path)), 1)

  def _ChooseReviewers(self):
    # TODO(b/210507794): register some test accounts on test server. This fixed
    # list of real IDs has a few problems, not limited to the following:
    #  * Some functions behave differently if the account is inactive;
    #  * Gerrit doesn't let you add yourself as a reviewer. So these accounts
    #    can't run the tests correctly. ;)
    return ['dborowitz@google.com', 'jrn@google.com']

  def testSetAttentionSet(self):
    """Verify that we can set the attention set on a CL."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    gpatch = self.createPatch(clone_path, project)
    emails = self._ChooseReviewers()
    helper = self._GetHelper()
    helper.SetReviewers(gpatch.gerrit_number, add=(
        emails[0], emails[1]))
    helper.SetAttentionSet(gpatch.gerrit_number, add=(
        emails[0], emails[1]))
    attention = gob_util.GetAttentionSet(helper.host, gpatch.gerrit_number)
    self.assertEqual(len(attention), 2)
    self.assertCountEqual(
        [r['account']['email'] for r in attention],
        [emails[0], emails[1]])
    helper.SetAttentionSet(gpatch.gerrit_number,
                           remove=(emails[0],))
    attention = gob_util.GetAttentionSet(helper.host, gpatch.gerrit_number)
    self.assertEqual(len(attention), 1)
    self.assertEqual(attention[0]['account']['email'], emails[1])

  def testSetReviewers(self):
    """Verify that we can set reviewers on a CL."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    gpatch = self.createPatch(clone_path, project)
    emails = self._ChooseReviewers()
    helper = self._GetHelper()
    helper.SetReviewers(gpatch.gerrit_number, add=(
        emails[0], emails[1]))
    reviewers = gob_util.GetReviewers(helper.host, gpatch.gerrit_number)
    self.assertEqual(len(reviewers), 2)
    self.assertCountEqual(
        [r['email'] for r in reviewers],
        [emails[0], emails[1]])
    helper.SetReviewers(gpatch.gerrit_number,
                        remove=(emails[0],))
    reviewers = gob_util.GetReviewers(helper.host, gpatch.gerrit_number)
    self.assertEqual(len(reviewers), 1)
    self.assertEqual(reviewers[0]['email'], emails[1])

  def testPatchNotFound(self):
    """Test case where ChangeID isn't found on the server."""
    changeids = ['I' + ('deadbeef' * 5), 'I' + ('beadface' * 5)]
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      changeids)
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      ['*' + cid for cid in changeids])
    # Change ID sequence starts at 1000.
    gerrit_numbers = ['123', '543']
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      gerrit_numbers)
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      ['*' + num for num in gerrit_numbers])

  def testVagueQuery(self):
    """Verify GerritHelper complains if an ID matches multiple changes."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    (sha1, _) = self.createCommit(clone_path)
    (_, changeid) = self.createCommit(clone_path)
    self.uploadChange(clone_path, 'main')
    cros_build_lib.run(
        ['git', 'checkout', sha1], cwd=clone_path, quiet=True)
    self.createCommit(clone_path)
    self.pushBranch(clone_path, 'testbranch')
    self.createCommit(
        clone_path, msg='Test commit.\n\nChange-Id: %s' % changeid)
    self.uploadChange(clone_path, 'testbranch')
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      [changeid])

  def testQueries(self):
    """Verify assorted query operations."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project)
    gpatch = self.createPatch(clone_path, project)
    helper = self._GetHelper()

    # Multi-queries with one valid and one invalid term should raise.
    invalid_change_id = 'I1234567890123456789012345678901234567890'
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      [invalid_change_id, gpatch.change_id])
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      [gpatch.change_id, invalid_change_id])
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      ['9876543', gpatch.gerrit_number])
    self.assertRaises(gerrit.GerritException, gerrit.GetGerritPatchInfo,
                      [gpatch.gerrit_number, '9876543'])

    site_params = config_lib.GetSiteParams()
    # Simple query by project/changeid/sha1.
    patch_info = helper.GrabPatchFromGerrit(gpatch.project, gpatch.change_id,
                                            gpatch.sha1)
    self.assertEqual(patch_info.gerrit_number, gpatch.gerrit_number)
    self.assertEqual(patch_info.remote, site_params.EXTERNAL_REMOTE)

    # Simple query by gerrit number to external remote.
    patch_info = gerrit.GetGerritPatchInfo([gpatch.gerrit_number])
    self.assertEqual(patch_info[0].gerrit_number, gpatch.gerrit_number)
    self.assertEqual(patch_info[0].remote, site_params.EXTERNAL_REMOTE)

    # Simple query by gerrit number to internal remote.
    patch_info = gerrit.GetGerritPatchInfo(['*' + gpatch.gerrit_number])
    self.assertEqual(patch_info[0].gerrit_number, gpatch.gerrit_number)
    self.assertEqual(patch_info[0].remote, site_params.INTERNAL_REMOTE)

    # Query to external server by gerrit number and change-id which refer to
    # the same change should return one result.
    fq_changeid = '~'.join((gpatch.project, 'main', gpatch.change_id))
    patch_info = gerrit.GetGerritPatchInfo([gpatch.gerrit_number, fq_changeid])
    self.assertEqual(len(patch_info), 1)
    self.assertEqual(patch_info[0].gerrit_number, gpatch.gerrit_number)
    self.assertEqual(patch_info[0].remote, site_params.EXTERNAL_REMOTE)

    # Query to internal server by gerrit number and change-id which refer to
    # the same change should return one result.
    patch_info = gerrit.GetGerritPatchInfo(
        ['*' + gpatch.gerrit_number, '*' + fq_changeid])
    self.assertEqual(len(patch_info), 1)
    self.assertEqual(patch_info[0].gerrit_number, gpatch.gerrit_number)
    self.assertEqual(patch_info[0].remote, site_params.INTERNAL_REMOTE)

  def testSubmitOutdatedCommit(self):
    """Tests that we can parse a json to check if a change is committed."""
    project = self.createProject('testProject')
    clone_path = self.cloneProject(project, 'p1')

    # Create a change.
    gpatch1 = self.createPatch(clone_path, project)

    # Update the change.
    gpatch2 = self.createPatch(clone_path, project, amend=True)

    # Make sure we're talking about the same change.
    self.assertEqual(gpatch1.change_id, gpatch2.change_id)

    # Try submitting the out-of-date change.
    helper = self._GetHelper()
    helper.SetReview(gpatch1.gerrit_number, labels={'Code-Review':'+2'})
    with self.assertRaises(gob_util.GOBError) as ex:
      helper.SubmitChange(gpatch1)
    self.assertEqual(ex.exception.http_status, http.client.CONFLICT)
    self.assertFalse(helper.IsChangeCommitted(gpatch1.gerrit_number))

    # Try submitting the up-to-date change.
    helper.SubmitChange(gpatch2)
    helper.IsChangeCommitted(gpatch2.gerrit_number)

  def testResetReviewLabels(self):
    """Tests that we can remove a code review label."""
    project = self.createProject('testProject')
    helper = self._GetHelper()
    clone_path = self.cloneProject(project, 'p1')
    gpatch = self.createPatch(clone_path, project, msg='Init')
    helper.SetReview(gpatch.gerrit_number, labels={'Code-Review':'+2'})
    gob_util.ResetReviewLabels(helper.host, gpatch.gerrit_number,
                               label='Code-Review', notify='OWNER')

  def testApprovalTime(self):
    """Approval timestamp should be reset when a new patchset is created."""
    # Create a change.
    project = self.createProject('testProject')
    helper = self._GetHelper()
    clone_path = self.cloneProject(project, 'p1')
    gpatch = self.createPatch(clone_path, project, msg='Init')
    helper.SetReview(gpatch.gerrit_number, labels={'Code-Review':'+2'})

    # Update the change.
    new_msg = 'New %s' % gpatch.commit_message
    cros_build_lib.run(
        ['git', 'commit', '--amend', '-m', new_msg], cwd=clone_path, quiet=True)
    self.uploadChange(clone_path)
    gpatch2 = self._GetHelper().QuerySingleRecord(
        change=gpatch.change_id, project=gpatch.project, branch='main')
    self.assertNotEqual(gpatch2.approval_timestamp, 0)
    self.assertNotEqual(gpatch2.commit_timestamp, 0)
    self.assertEqual(gpatch2.approval_timestamp, gpatch2.commit_timestamp)


class GerritParserTest(cros_test_lib.TestCase):
  """Unittests for GerritHelper."""

  # pylint: disable=protected-access

  def _GetHelper(self, remote=config_lib.GetSiteParams().EXTERNAL_REMOTE):
    return gerrit.GetGerritHelper(remote)

  def testGetChangeFromStdoutPass(self):
    """Test that the proper change number is returned from the git stdout."""
    stdout = ('remote:\nremote:\nremote:   '
              'https://example.com/c/some/project/repo/+/123 gerrit: test')
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)
    self.assertEqual(changenum, '123')

    stdout = ('remote:\nremote:   '
              'https://example.com/c/some/project3/repo/+/123 gerrit: test')
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)
    self.assertEqual(changenum, '123')

    stdout = ('remote:   '
              'https://example.com/c/some/project/repo/+/123 gerrit: test 456')
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)
    self.assertEqual(changenum, '123')

    stdout = ('remote:   '
              'https://example.com/c/some/project/repo/+/123 '
              'handle /+/124 in URI')
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)
    self.assertEqual(changenum, '123')

  def testGetChangeFromStdoutFail(self):
    """Test that the function returns None when an improper stdout is given."""

    # Fails because remote is not at the start of the text.
    stdout = """
    remote:
    remote:   https://example./c/some/project/repo/+/123 gerrit: test
    """
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)
    self.assertIsNone(changenum)

    stdout = """
    remote:https://example./c/some/project/repo/+/123 gerrit: test
    """
    changenum = self._GetHelper()._get_changenumber_from_stdout(stdout)

    self.assertIsNone(changenum)


@cros_test_lib.pytestmark_network_test
class DirectGerritHelperTest(cros_test_lib.TestCase):
  """Unittests for GerritHelper that use the real Chromium instance."""

  # A big list of real changes.
  CHANGES = ['235893', '*189165', '231790', '*190026', '231647', '234645']

  def testMultipleChangeDetail(self):
    """Test ordering of results in GetMultipleChangeDetail"""
    changes = [x for x in self.CHANGES if not x.startswith('*')]
    helper = gerrit.GetCrosExternal()
    results = list(helper.GetMultipleChangeDetail([str(x) for x in changes]))
    gerrit_numbers = [str(x['_number']) for x in results]
    self.assertEqual(changes, gerrit_numbers)

  def testQueryMultipleCurrentPatchset(self):
    """Test ordering of results in QueryMultipleCurrentPatchset"""
    changes = [x for x in self.CHANGES if not x.startswith('*')]
    helper = gerrit.GetCrosExternal()
    results = list(helper.QueryMultipleCurrentPatchset(changes))
    self.assertEqual(changes, [x.gerrit_number for _, x in results])
    self.assertEqual(changes, [x for x, _ in results])

  def testGetGerritPatchInfo(self):
    """Test ordering of results in GetGerritPatchInfo"""
    # Swizzle from our old syntax to the new syntax.
    changes = []
    for change in self.CHANGES:
      if change.startswith('*'):
        changes.append('chrome-internal:%s' % (change[1:],))
      else:
        changes.append('chromium:%s' % (change,))
    results = list(gerrit.GetGerritPatchInfo(changes))
    self.assertEqual(changes, [x.gerrit_number_str for x in results])
