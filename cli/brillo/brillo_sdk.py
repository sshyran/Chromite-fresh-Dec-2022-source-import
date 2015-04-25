# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Manage Project SDK installation, NOT REALATED to 'cros_sdk'."""

from __future__ import print_function

import os
import tempfile

from chromite.cbuildbot import constants
from chromite.cbuildbot import repository
from chromite.cli import command
from chromite.lib import bootstrap_lib
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import git
from chromite.lib import gs
from chromite.lib import osutils
from chromite.lib import project_sdk
from chromite.lib import workspace_lib


_BRILLO_SDK_NO_UPDATE = 'BRILLO_SDK_NO_UPDATE'

# To fake the repo command into accepting a simple manifest, we
# have to put that manifest into a git repository. This is the
# name of that repo.
_BRILLO_SDK_LOCAL_MANIFEST_REPO = '.local_manifest_repo'


def _ResolveLatest(gs_ctx):
  """Find the 'latest' SDK release."""
  return gs_ctx.Cat(constants.BRILLO_LATEST_RELEASE_URL).strip()


def _DownloadSdk(gs_ctx, sdk_dir, version):
  """Downloads the specified SDK to |sdk_dir|.

  Args:
    gs_ctx: GS Context to use.
    sdk_dir: Directory in which to create a repo.
    version: Project SDK version to sync. Can be a version number or 'tot';
      'latest' should be resolved before calling this.
  """
  try:
    # Create the SDK dir, if it doesn't already exist.
    osutils.SafeMakedirs(sdk_dir)

    repo_cmd = os.path.join(constants.BOOTSTRAP_DIR, 'repo')

    logging.notice('Fetching files. This could take a few minutes...')
    # TOT is a special case, handle it first.
    if version.lower() == 'tot':
      # Init new repo.
      repo = repository.RepoRepository(
          constants.MANIFEST_URL, sdk_dir, groups='project_sdk',
          repo_cmd=repo_cmd)
      # Sync it.
      repo.Sync()
      return

    with tempfile.NamedTemporaryFile() as manifest:
      # Fetch manifest into temp file.
      manifest_url = os.path.join(constants.BRILLO_RELEASE_MANIFESTS_URL,
                                  '%s.xml' % version)
      gs_ctx.Copy(manifest_url, manifest.name)

      manifest_git_dir = os.path.join(sdk_dir, _BRILLO_SDK_LOCAL_MANIFEST_REPO)

      # Convert manifest into a git repository for the repo command.
      repository.PrepManifestForRepo(manifest_git_dir, manifest.name)

      # Fetch the SDK.
      repo = repository.RepoRepository(manifest_git_dir, sdk_dir, depth=1,
                                       repo_cmd=repo_cmd)
      repo.Sync()

    # TODO(dgarrett): Embed this step into the manifest itself.
    # Write out the SDK Version.
    sdk_version_file = project_sdk.VersionFile(sdk_dir)
    osutils.WriteFile(sdk_version_file, version)
  except:
    # If we fail for any reason, remove the partial/corrupt SDK.
    osutils.RmDir(sdk_dir, ignore_missing=True)
    raise


def _UpdateBootstrap(bootstrap_path):
  """Update the bootstrap repository."""
  # If our bootstrap is part of a repository, we shouldn't update.
  if project_sdk.FindRepoRoot(bootstrap_path):
    return

  # If the 'skip update' variable is set, we shouldn't update.
  if os.environ.get(_BRILLO_SDK_NO_UPDATE):
    return

  # Perform the git pull to update our bootstrap.
  logging.info('Updating SDK bootstrap...')
  git.RunGit(bootstrap_path, ['pull'])

  # Prevent updating again, after we restart.
  logging.debug('Re-exec...')
  os.environ[_BRILLO_SDK_NO_UPDATE] = "1"
  commandline.ReExec()


def _UpdateWorkspaceSdk(bootstrap_path, workspace_path, version):
  """Install SDK |version| and attach it to a workspace.

  Args:
    bootstrap_path: Path to bootstrap location.
    workspace_path: Path to workspace location.
    version: Project SDK version to sync. Can be a version number, 'tot', or
      'latest'.
  """
  if project_sdk.FindRepoRoot(bootstrap_path):
    cros_build_lib.Die('brillo sdk must run from a git clone. brbug.com/580')

  # We fetch versioned manifests from GS.
  gs_ctx = gs.GSContext()

  # Resolve 'latest' into a concrete version.
  if version.lower() == 'latest':
    version = _ResolveLatest(gs_ctx)

  sdk_path = bootstrap_lib.ComputeSdkPath(bootstrap_path, version)

  # If this version already exists, no need to reinstall it.
  if not os.path.exists(sdk_path) or version == 'tot':
    _DownloadSdk(gs_ctx, sdk_path, version)

  # Store the new version in the workspace.
  workspace_lib.SetActiveSdkVersion(workspace_path, version)


def _PrintWorkspaceSdkVersion(workspace_path, to_stdout=False):
  """Prints a workspace SDK version.

  If an SDK version can't be found, calls cros_build_lib.Die().

  Args:
    workspace_path: workspace directory path.
    to_stdout: True to print to stdout, False to use the logger.
  """
  # Print the SDK version.
  sdk_version = workspace_lib.GetActiveSdkVersion(workspace_path)
  if sdk_version is None:
    cros_build_lib.Die(
        'This workspace does not have an SDK.\n'
        'Use `brillo sdk --update latest` to attach to the latest SDK.')
  if to_stdout:
    print(sdk_version)
  else:
    logging.notice('Version: %s', sdk_version)


@command.CommandDecorator('sdk')
class SdkCommand(command.CliCommand):
  """Manage Project SDK installations."""

  @classmethod
  def AddParser(cls, parser):
    super(cls, SdkCommand).AddParser(parser)
    parser.add_argument(
        '--update', help='Update the SDK to version 1.2.3, tot, or latest.')
    parser.add_argument('--version', default=False, action='store_true',
                        help='Display current version.')

  def Run(self):
    """Run brillo sdk."""
    self.options.Freeze()

    # Must run outside the chroot.
    cros_build_lib.AssertOutsideChroot()

    workspace_path = workspace_lib.WorkspacePath()
    if not workspace_path:
      cros_build_lib.Die('You must be in a workspace.')

    # Perform the update.
    if self.options.update:
      bootstrap_path = bootstrap_lib.FindBootstrapPath()

      logging.info('Update bootstrap...')
      _UpdateBootstrap(bootstrap_path)

      # Verify environment after _UpdateBootstrap() so we could potentially
      # fix some problems automatically.
      if not project_sdk.VerifyEnvironment():
        cros_build_lib.Die('Environment verification failed.')

      logging.notice('Updating SDK...')
      _UpdateWorkspaceSdk(bootstrap_path, workspace_path, self.options.update)

    # The --version argument should print to stdout for consumption by scripts.
    _PrintWorkspaceSdkVersion(workspace_path, to_stdout=self.options.version)
