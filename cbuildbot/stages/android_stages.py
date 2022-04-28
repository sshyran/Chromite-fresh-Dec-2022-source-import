# Copyright 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module containing the Android stages."""

import logging
import os

from chromite.cbuildbot import cbuildbot_alerts
from chromite.cbuildbot import cbuildbot_run
from chromite.cbuildbot import commands
from chromite.cbuildbot.stages import generic_stages
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import gs
from chromite.lib import osutils
from chromite.lib import results_lib


ANDROIDPIN_MASK_PATH = os.path.join(constants.SOURCE_ROOT,
                                    constants.CHROMIUMOS_OVERLAY_DIR,
                                    'profiles', 'default', 'linux',
                                    'package.mask', 'androidpin')


def _GetAndroidVersionFromMetadata(metadata):
  """Return the Android version from metadata; None if is does not exist.

  In Android PFQ, Android version is set to metadata in master
  (MasterSlaveLKGMSyncStage).
  """
  version_dict = metadata.GetDict().get('version', {})
  return version_dict.get('android')


class UprevAndroidStage(generic_stages.BuilderStage,
                        generic_stages.ArchivingStageMixin):
  """Stage that uprevs Android container if needed."""

  category = constants.PRODUCT_ANDROID_STAGE

  def PerformStage(self):
    # This stage runs only in builders where |android_rev| config is set,
    # namely Android PFQ and pre-flight-branch builders.
    if not self._android_rev:
      logging.info('Not uprevving Android.')
      return

    with osutils.ChdirContext(self._build_root):
      android_package = self._run.config.android_package
      android_build_branch = self._run.config.android_import_branch
      android_version = _GetAndroidVersionFromMetadata(self._run.attrs.metadata)

    assert android_package
    assert android_build_branch
    # |android_version| is usually set by MasterSlaveLKGMSyncStage, but we allow
    # it to be unset to indicate uprev'ing to the latest version. In fact, it is
    # not set in trybots.

    logging.info('Android package: %s', android_package)
    logging.info('Android branch: %s', android_build_branch)
    logging.info('Android version: %s', android_version or 'LATEST')

    if self._run.config.master and self._run.config.android_update_lkgb:
      # If android_update_lkgb is set, the master builder publishes a LKGB
      # update instead of an ebuild uprev. The LKGB update will in turn trigger
      # the PUpr generator to generate actual Android uprev CLs.
      commands.MarkAndroidLKGB(buildroot=self._build_root,
                               android_package=android_package,
                               android_version=android_version)
      return

    try:
      android_atom_to_build = commands.MarkAndroidAsStable(
          buildroot=self._build_root,
          android_package=android_package,
          android_build_branch=android_build_branch,
          boards=self._boards,
          android_version=android_version)
    except commands.AndroidIsPinnedUprevError as e:
      # If uprev failed due to a pin, record that failure (so that the
      # build ultimately fails) but try again without the pin, to allow the
      # slave to test the newer version anyway).
      android_atom_to_build = e.new_android_atom
      results_lib.Results.Record(self.name, e)
      cbuildbot_alerts.PrintBuildbotStepFailure()
      logging.error('Android is pinned. Unpinning Android and continuing '
                    'build for Android atom %s. This stage will be marked '
                    'as failed to prevent an uprev.',
                    android_atom_to_build)
      logging.info('Deleting pin file at %s and proceeding.',
                   ANDROIDPIN_MASK_PATH)
      osutils.SafeUnlink(ANDROIDPIN_MASK_PATH)

    logging.info('New Android package atom: %s', android_atom_to_build)


class AndroidMetadataStage(generic_stages.BuilderStage,
                           generic_stages.ArchivingStageMixin):
  """Stage that records Android container version in metadata.

  This stage runs on every builder, not limited to Android PFQ. Metadata
  written by this stage must reflect the actual Android version of the build
  artifact.

  Metadata written by this stage will be consumed by various external tools
  such as GoldenEye.
  """

  category = constants.PRODUCT_ANDROID_STAGE

  def _UpdateBoardDictsForAndroidBuildInfo(self):
    """Updates board metadata to fill in Android build info.

    Returns:
      (versions, branches, targets) where:
        versions: A set of Android versions used in target boards.
        branches: A set of Android branch names used in target boards.
        targets: A set of Android targets used in target boards.
    """
    # Need to always iterate through and generate the board-specific
    # Android version metadata.  Each board must be handled separately
    # since there might be differing builds in the same release group.
    versions = set()
    branches = set()
    targets = set()

    for builder_run in self._run.GetUngroupedBuilderRuns():
      for board in builder_run.config.boards:
        try:
          # Determine the version for each board and record metadata.
          version = self._run.DetermineAndroidVersion(boards=[board])
          builder_run.attrs.metadata.UpdateBoardDictWithDict(
              board, {'android-container-version': version})
          versions.add(version)
          logging.info('Board %s has Android version %s', board, version)
        except cbuildbot_run.NoAndroidVersionError as ex:
          logging.info('Board %s does not contain Android (%s)', board, ex)
        try:
          # Determine the branch for each board and record metadata.
          branch = self._run.DetermineAndroidBranch(board)
          builder_run.attrs.metadata.UpdateBoardDictWithDict(
              board, {'android-container-branch': branch})
          branches.add(branch)
          logging.info('Board %s has Android branch %s', board, branch)
        except cbuildbot_run.NoAndroidBranchError as ex:
          logging.info('Board %s does not contain Android (%s)', board, ex)
        try:
          # Determine the target for each board and record metadata.
          target = self._run.DetermineAndroidTarget(board)
          builder_run.attrs.metadata.UpdateBoardDictWithDict(
              board, {'android-container-target': target})
          targets.add(target)
          logging.info('Board %s has Android target %s', board, target)
        except cbuildbot_run.NoAndroidTargetError as ex:
          logging.info('Board %s does not contain Android (%s)', board, ex)
        arc_use = self._run.HasUseFlag(board, 'arc')
        logging.info('Board %s %s arc USE flag set.', board,
                     'has' if arc_use else 'does not have')
        builder_run.attrs.metadata.UpdateBoardDictWithDict(
            board, {'arc-use-set': arc_use})

    return (versions, branches, targets)

  def PerformStage(self):
    with osutils.ChdirContext(self._build_root):
      versions, branches, targets = self._UpdateBoardDictsForAndroidBuildInfo()

    # Unfortunately we can't inspect Android build info in slaves from masters,
    # so metadata is usually unavailable on masters (e.g. master-release).
    # An exception is builders uprev'ing Android; those info is available
    # from configs and metadata. But note that version can be still unspecified.
    if self._android_rev:
      uprev_version = _GetAndroidVersionFromMetadata(self._run.attrs.metadata)
      # |uprev_version| can be not set.
      if uprev_version:
        versions.add(uprev_version)

      uprev_branch = self._run.config.android_import_branch
      assert uprev_branch
      branches.add(uprev_branch)

      # If we uprev Android, branch/version must be consistent.
      # TODO(b/152768977): Provide assertion that awares about ARCVM PFQ for
      # union builds. In last case, there are 2 versions and branches.
      # assert len(versions) <= 1, 'Multiple Android versions: %r' % versions
      # assert len(branches) <= 1, 'Multiple Android branches: %r' % branches

    # If there is a unique one across all the boards, treat it as the version
    # for the build.
    # TODO(nya): Represent "N/A" and "Multiple" differently in metadata.
    def _Aggregate(v):
      if not v:
        return (None, 'N/A')
      elif len(v) == 1:
        return (v[0], str(v[0]))
      return (None, 'Multiple')

    metadata_version, debug_version = _Aggregate(list(versions))
    metadata_branch, debug_branch = _Aggregate(list(branches))
    metadata_target, debug_target = _Aggregate(list(targets))

    # Update the primary metadata and upload it.
    self._run.attrs.metadata.UpdateKeyDictWithDict(
        'version',
        {'android': metadata_version,
         'android-branch': metadata_branch,
         'android-target': metadata_target})
    self.UploadMetadata(filename=constants.PARTIAL_METADATA_JSON)

    # Leave build info in buildbot steps page for convenience.
    cbuildbot_alerts.PrintBuildbotStepText('tag %s' % debug_version)
    cbuildbot_alerts.PrintBuildbotStepText('branch %s' % debug_branch)
    cbuildbot_alerts.PrintBuildbotStepText('target %s' % debug_target)


class DownloadAndroidDebugSymbolsStage(generic_stages.BoardSpecificBuilderStage,
                                       generic_stages.ArchivingStageMixin):
  """Stage that downloads Android debug symbols.

  Downloaded archive will be picked up by DebugSymbolsStage.
  """

  category = constants.CI_INFRA_STAGE

  def PerformStage(self):
    if not config_lib.IsCanaryType(self._run.config.build_type):
      logging.info('This stage runs only in release builders.')
      return

    # Get the Android versions set by AndroidMetadataStage.
    version_dict = self._run.attrs.metadata.GetDict().get('version', {})
    android_build_branch = version_dict.get('android-branch')
    android_version = version_dict.get('android')

    # On boards not supporting Android, versions will be None.
    if not (android_build_branch and android_version):
      logging.info('Android is not enabled on this board. Skipping.')
      return

    logging.info(
        'Downloading symbols of Android %s (%s)...',
        android_version, android_build_branch)

    with osutils.ChdirContext(self._build_root):
      arch = self._run.DetermineAndroidABI(self._current_board)
      variant = self._run.DetermineAndroidVariant(self._current_board)
      android_target = self._run.DetermineAndroidTarget(self._current_board)

    symbols_file_url = constants.ANDROID_SYMBOLS_URL_TEMPLATE % {
        'branch': android_build_branch,
        'target': android_target,
        'arch': arch,
        'version': android_version,
        'variant': variant,
    }
    symbols_file = os.path.join(self.archive_path,
                                constants.ANDROID_SYMBOLS_FILE)
    gs_context = gs.GSContext()
    gs_context.Copy(symbols_file_url, symbols_file)
