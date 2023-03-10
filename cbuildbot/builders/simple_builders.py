# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module containing the simple builders."""

import collections
import logging
import traceback

from chromite.cbuildbot import manifest_version
from chromite.cbuildbot.builders import generic_builders
from chromite.cbuildbot.stages import android_stages
from chromite.cbuildbot.stages import artifact_stages
from chromite.cbuildbot.stages import build_stages
from chromite.cbuildbot.stages import chrome_stages
from chromite.cbuildbot.stages import completion_stages
from chromite.cbuildbot.stages import generic_stages
from chromite.cbuildbot.stages import release_stages
from chromite.cbuildbot.stages import report_stages
from chromite.cbuildbot.stages import scheduler_stages
from chromite.cbuildbot.stages import sync_stages
from chromite.cbuildbot.stages import tast_test_stages
from chromite.cbuildbot.stages import test_stages
from chromite.cbuildbot.stages import vm_test_stages
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import failures_lib
from chromite.lib import parallel
from chromite.lib import results_lib


# TODO: SimpleBuilder needs to be broken up big time.


BoardConfig = collections.namedtuple('BoardConfig', ['board', 'name'])


class SimpleBuilder(generic_builders.Builder):
  """Builder that performs basic vetting operations."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.sync_stage = None

  def GetSyncInstance(self):
    """Sync to lkgm or TOT as necessary.

    Returns:
      The instance of the sync stage to run.
    """
    if self._run.options.force_version:
      sync_stage = self._GetStageInstance(
          sync_stages.ManifestVersionedSyncStage)
    elif self._run.config.use_chrome_lkgm:
      sync_stage = self._GetStageInstance(chrome_stages.ChromeLKGMSyncStage)
    else:
      sync_stage = self._GetStageInstance(sync_stages.SyncStage)

    self.sync_stage = sync_stage
    return sync_stage

  def GetVersionInfo(self):
    """Returns the CrOS version info from the chromiumos-overlay."""
    return manifest_version.VersionInfo.from_repo(self._run.buildroot)

  def _RunHWTests(self, builder_run, board):
    """Run hwtest-related stages for the specified board.

    Args:
      builder_run: BuilderRun object for these background stages.
      board: Board name.
    """
    self._RunStage(test_stages.TestPlanStage, board,
                   builder_run=builder_run)


  def _RunVMTests(self, builder_run, board):
    """Run VM test stages for the specified board.

    Args:
      builder_run: BuilderRun object for stages.
      board: String containing board name.
    """
    config = builder_run.config
    except_infos = []

    try:
      if config.vm_test_runs > 1:
        # Run the VMTests multiple times to see if they fail.
        self._RunStage(generic_stages.RepeatStage, config.vm_test_runs,
                       vm_test_stages.VMTestStage, board,
                       builder_run=builder_run)
      else:
        # Retry VM-based tests in case failures are flaky.
        self._RunStage(generic_stages.RetryStage, constants.VM_NUM_RETRIES,
                       vm_test_stages.VMTestStage, board,
                       builder_run=builder_run)
    except Exception as e:
      except_infos.extend(
          failures_lib.CreateExceptInfo(e, traceback.format_exc()))

    # Run stages serially to avoid issues encountered when running VMs (or the
    # devserver) in parallel: https://crbug.com/779267
    if config.tast_vm_tests:
      try:
        self._RunStage(generic_stages.RetryStage, constants.TAST_VM_NUM_RETRIES,
                       tast_test_stages.TastVMTestStage, board,
                       builder_run=builder_run)
      except Exception as e:
        except_infos.extend(
            failures_lib.CreateExceptInfo(e, traceback.format_exc()))

    if except_infos:
      raise failures_lib.CompoundFailure('VM tests failed', except_infos)

  def _RunDebugSymbolStages(self, builder_run, board):
    """Run debug-related stages for the specified board.

    Args:
      builder_run: BuilderRun object for these background stages.
      board: Board name.
    """
    # These stages should run sequentially.
    self._RunStage(android_stages.DownloadAndroidDebugSymbolsStage,
                   board, builder_run=builder_run)
    self._RunStage(artifact_stages.DebugSymbolsStage, board,
                   builder_run=builder_run)

  def _RunBackgroundStagesForBoardAndMarkAsSuccessful(self, builder_run, board):
    """Run background board-specific stages for the specified board.

    After finishing the build, mark it as successful.

    Args:
      builder_run: BuilderRun object for these background stages.
      board: Board name.
    """
    self._RunBackgroundStagesForBoard(builder_run, board)
    board_runattrs = builder_run.GetBoardRunAttrs(board)
    board_runattrs.SetParallel('success', True)

  def _RunBackgroundStagesForBoard(self, builder_run, board):
    """Run background board-specific stages for the specified board.

    Used by _RunBackgroundStagesForBoardAndMarkAsSuccessful. Callers should use
    that method instead.

    Args:
      builder_run: BuilderRun object for these background stages.
      board: Board name.
    """
    config = builder_run.config

    # TODO(mtennant): This is the last usage of self.archive_stages.  We can
    # kill it once we migrate its uses to BuilderRun so that none of the
    # stages below need it as an argument.
    archive_stage = self.archive_stages[BoardConfig(board, config.name)]
    if config.afdo_generate_min:
      self._RunParallelStages([archive_stage])
      return

    # paygen can't complete without push_image.
    assert not config.paygen or config.push_image

    # While this stage list is run in parallel, the order here dictates the
    # order that things will be shown in the log.  So group things together
    # that make sense when read in order.  Also keep in mind that, since we
    # gather output manually, early slow stages will prevent any output from
    # later stages showing up until it finishes.
    early_stage_list = [
        [test_stages.UnitTestStage, board],
    ]

    stage_list = []
    if config.debuginfo_test:
      stage_list += [
          [test_stages.DebugInfoTestStage, board],
      ]

    # Skip most steps if we're a compilecheck builder.
    if builder_run.config.compilecheck or builder_run.options.compilecheck:
      board_runattrs = builder_run.GetBoardRunAttrs(board)
      board_runattrs.SetParallel('test_artifacts_uploaded', False)
      stages = early_stage_list + stage_list
      for x in stages:
        self._RunStage(*x, builder_run=builder_run)
      return

    stage_list += [[chrome_stages.SimpleChromeArtifactsStage, board]]

    if config.gce_tests:
      stage_list += [[generic_stages.RetryStage, constants.VM_NUM_RETRIES,
                      vm_test_stages.GCETestStage, board]]

    if config.moblab_vm_tests:
      stage_list += [[vm_test_stages.MoblabVMTestStage, board]]

    stage_list += [
        [release_stages.SignerTestStage, board, archive_stage],
        [release_stages.SigningStage, board],
        [release_stages.PaygenStage, board],
        [test_stages.ImageTestStage, board],
        [artifact_stages.UploadPrebuiltsStage, board],
        [artifact_stages.DevInstallerPrebuiltsStage, board],
    ]

    if config.run_cpeexport:
      stage_list += [[artifact_stages.CPEExportStage, board]]

    if config.run_build_configs_export:
      stage_list += [[artifact_stages.BuildConfigsExportStage, board]]

    early_stage_list += [[artifact_stages.UploadTestArtifactsStage, board]]

    early_stage_objs = [
        self._GetStageInstance(*x, builder_run=builder_run)
        for x in early_stage_list
    ]

    stage_objs = [
        self._GetStageInstance(*x, builder_run=builder_run) for x in stage_list
    ]

    # Build the image first before running the steps.
    with self._build_image_lock:
      self._RunStage(build_stages.BuildImageStage, board,
                     builder_run=builder_run, afdo_use=config.afdo_use)

    # Run the debug symbols stage before the UnitTestStage to avoid generating
    # debug symbols from the altered, test symbols.
    self._RunDebugSymbolStages(builder_run, board)
    # Run UnitTestStage & UploadTestArtifactsStage in a separate pass before
    # any of the other parallel stages to prevent races with the image
    # construction in the ArchiveStage.
    # http://crbug.com/1000374
    self._RunParallelStages(early_stage_objs)

    parallel.RunParallelSteps([
        lambda: self._RunParallelStages(stage_objs + [archive_stage]),
        lambda: self._RunHWTests(builder_run, board),
    ])
    # Move VMTests out of parallel execution due to high failure rate.
    # http://crbug/932644
    self._RunVMTests(builder_run, board)

  def BoardsForSimpleBuilder(self, builder_run):
    """All boards for this builder.

    Defaults to builder_run.config.boards, but can be overridden if a
    HWTestDUTOverride was specified for this run.
    """
    if self._run.options.hwtest_dut_override:
      return [self._run.options.hwtest_dut_override.board]

    return builder_run.config.boards

  def RunSetupBoard(self):
    """Run the SetupBoard stage for all child configs and boards."""
    for builder_run in self._run.GetUngroupedBuilderRuns():
      for board in self.BoardsForSimpleBuilder(builder_run):
        self._RunStage(build_stages.SetupBoardStage, board,
                       builder_run=builder_run)

  def _RunMasterAndroidPFQBuild(self):
    """Runs through the stages of the paladin or chrome PFQ master build."""
    # If there are slave builders, schedule them.
    if self._run.config.slave_configs:
      self._RunStage(scheduler_stages.ScheduleSlavesStage, self.sync_stage)
    self._RunStage(build_stages.UprevStage)
    self._RunStage(build_stages.InitSDKStage)
    self._RunStage(build_stages.UpdateSDKStage)
    # The CQ/Chrome PFQ master will not actually run the SyncChrome stage, but
    # we want the logic that gets triggered when SyncChrome stage is skipped.
    self._RunStage(chrome_stages.SyncChromeStage)

  def RunEarlySyncAndSetupStages(self):
    """Runs through the early sync and board setup stages."""
    # If there are slave builders, schedule them.
    if self._run.config.slave_configs:
      self._RunStage(scheduler_stages.ScheduleSlavesStage, self.sync_stage)
    self._RunStage(build_stages.UprevStage)
    self._RunStage(build_stages.InitSDKStage)
    self._RunStage(build_stages.UpdateSDKStage)
    self._RunStage(build_stages.RegenPortageCacheStage)
    self.RunSetupBoard()
    self._RunStage(chrome_stages.SyncChromeStage)
    self._RunStage(android_stages.UprevAndroidStage)
    self._RunStage(android_stages.AndroidMetadataStage)

  def RunBuildStages(self):
    """Runs through the stages to perform the build and resulting tests."""
    # Prepare stages to run in background.  If child_configs exist then
    # run each of those here, otherwise use default config.
    builder_runs = self._run.GetUngroupedBuilderRuns()

    tasks = []
    for builder_run in builder_runs:
      # Prepare a local archive directory for each "run".
      builder_run.GetArchive().SetupArchivePath()

      for board in self.BoardsForSimpleBuilder(builder_run):
        archive_stage = self._GetStageInstance(
            artifact_stages.ArchiveStage, board, builder_run=builder_run,
            chrome_version=self._run.attrs.chrome_version)
        board_config = BoardConfig(board, builder_run.config.name)
        self.archive_stages[board_config] = archive_stage
        tasks.append((builder_run, board))

    # Set up a process pool to run test/archive stages in the background.
    # This process runs task(board) for each board added to the queue.
    task_runner = self._RunBackgroundStagesForBoardAndMarkAsSuccessful
    with parallel.BackgroundTaskRunner(task_runner) as queue:
      for builder_run, board in tasks:
        # Run BuildPackages in the foreground.
        kwargs = {'builder_run': builder_run}
        if builder_run.config.afdo_generate_min:
          kwargs['afdo_generate_min'] = True
        elif builder_run.config.afdo_use:
          kwargs['afdo_use'] = True

        self._RunStage(build_stages.BuildPackagesStage, board,
                       update_metadata=True, **kwargs)

        # Kick off our background stages.
        queue.put([builder_run, board])

  def _RunDefaultTypeBuild(self):
    """Runs through the stages of a non-special-type build."""
    self.RunEarlySyncAndSetupStages()
    self.RunBuildStages()

  def RunStages(self):
    """Runs through build process."""
    # TODO(sosa): Split these out into classes.
    if config_lib.IsMasterAndroidPFQ(self._run.config):
      self._RunMasterAndroidPFQBuild()
    else:
      self._RunDefaultTypeBuild()


class DistributedBuilder(SimpleBuilder):
  """Build class that has special logic to handle distributed builds.

  These builds sync using git/manifest logic in manifest_versions.  In general
  they use a non-distributed builder code for the bulk of the work.
  """

  def __init__(self, *args, **kwargs):
    """Initializes a buildbot builder.

    Extra variables:
      completion_stage_class:  Stage used to complete a build.  Set in the Sync
        stage.
    """
    super().__init__(*args, **kwargs)
    self.completion_stage_class = None
    self.sync_stage = None
    self._completion_stage = None

  def GetSyncInstance(self):
    """Syncs the tree using one of the distributed sync logic paths.

    Returns:
      The instance of the sync stage to run.
    """
    # Determine sync class to use.  CQ overrides PFQ bits so should check it
    # first.
    if config_lib.IsCanaryType(self._run.config.build_type):
      sync_stage = self._GetStageInstance(
          sync_stages.ManifestVersionedSyncStage)
      self.completion_stage_class = (
          completion_stages.CanaryCompletionStage)
    elif (config_lib.IsPFQType(self._run.config.build_type) or
          self._run.config.build_type in (constants.TOOLCHAIN_TYPE,
                                          constants.FULL_TYPE,
                                          constants.INCREMENTAL_TYPE)):
      sync_stage = self._GetStageInstance(sync_stages.MasterSlaveLKGMSyncStage)
      self.completion_stage_class = (
          completion_stages.MasterSlaveSyncCompletionStage)
    else:
      sync_stage = self._GetStageInstance(
          sync_stages.ManifestVersionedSyncStage)
      self.completion_stage_class = (
          completion_stages.ManifestVersionedSyncCompletionStage)

    self.sync_stage = sync_stage
    return self.sync_stage

  def GetCompletionInstance(self):
    """Returns the completion_stage_class instance that was used for this build.

    Returns:
      None if the completion_stage instance was not yet created (this
      occurs during Publish).
    """
    return self._completion_stage

  def Complete(self, was_build_successful, build_finished):
    """Completes build by publishing any required information.

    Args:
      was_build_successful: Whether the build succeeded.
      build_finished: Whether the build completed. A build can be successful
        without completing if it raises ExitEarlyException.
    """
    self._completion_stage = self._GetStageInstance(
        self.completion_stage_class, self.sync_stage, was_build_successful)
    completion_successful = False
    try:
      self._completion_stage.Run()
      completion_successful = True
    except failures_lib.StepFailure:
      raise
    finally:
      self._Publish(was_build_successful, build_finished, completion_successful)

  def _Publish(self, was_build_successful, build_finished,
               completion_successful):
    """Updates and publishes uprevs.

    Args:
      was_build_successful: Whether the build succeeded.
      build_finished: Whether the build completed. A build can be successful
        without completing if it raises ExitEarlyException.
      completion_successful: Whether the compeletion_stage succeeded.
    """
    if self._run.config.master:
      self._RunStage(report_stages.SlaveFailureSummaryStage)

    if (config_lib.IsCanaryMaster(self._run) or
        (self._run.config.master and
         self._run.config.build_type == constants.FULL_TYPE)):
      if build_finished and not self._run.config.basic_builder:
        self._RunStage(completion_stages.UpdateChromeosLKGMStage)
      else:
        logging.info(
            'Skipping UpdateChromeosLKGMStage, '
            'build_successful=%d completion_successful=%d '
            'build_finished=%d', was_build_successful, completion_successful,
            build_finished)

    if self._run.config.push_overlays:
      publish = (was_build_successful and completion_successful and
                 build_finished)
      # CQ and Master Chrome PFQ no longer publish uprevs. For Master Chrome
      # PFQ this is because this duty is being transitioned to the Chrome
      # PUpr in the PCQ world. See http://go/pupr.
      # There is no easy way to disable this in ChromeOS config,
      # so hack the check here.

      if publish and config_lib.IsMasterAndroidPFQ(self._run.config):
        self._RunStage(android_stages.UprevAndroidStage)
        self._RunStage(android_stages.AndroidMetadataStage)
      self._RunStage(completion_stages.PublishUprevChangesStage,
                     self.sync_stage, publish)

  def RunStages(self):
    """Runs simple builder logic and publishes information to overlays."""
    was_build_successful = False
    build_finished = False
    try:
      super().RunStages()
      build_identifier, _ = self._run.GetCIDBHandle()
      buildbucket_id = build_identifier.buildbucket_id
      was_build_successful = results_lib.Results.BuildSucceededSoFar(
          self.buildstore, buildbucket_id)
      build_finished = True
    except failures_lib.ExitEarlyException as ex:
      # If a stage throws ExitEarlyException, it's exiting with success,
      # so that means we should mark ourselves as successful.
      logging.info('Detected exception %s', ex)
      was_build_successful = True
      raise
    finally:
      self.Complete(was_build_successful, build_finished)
