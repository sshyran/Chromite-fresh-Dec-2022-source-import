# Copyright 2016 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for cros_mark_android_as_stable.py."""

import builtins
import os

from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import gs_unittest
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.scripts import cros_mark_android_as_stable
from chromite.service import android


pytestmark = cros_test_lib.pytestmark_inside_only


class CrosMarkAndroidAsStable(cros_test_lib.MockTempDirTestCase):
    """Tests for cros_mark_android_as_stable."""

    unstable_data = 'KEYWORDS="~x86 ~arm"'
    stable_data = 'KEYWORDS="x86 arm"'

    STAT_OUTPUT = """%s:
        Creation time:    Sat, 23 Aug 2014 06:53:20 GMT
        Content-Language: en
        Content-Length:   74
        Content-Type:   application/octet-stream
        Hash (crc32c):    BBPMPA==
        Hash (md5):   ms+qSYvgI9SjXn8tW/5UpQ==
        ETag:     CNCgocbmqMACEAE=
        Generation:   1408776800850000
        Metageneration:   1
      """

    def setUp(self):
        """Setup vars and create mock dir."""
        self.android_package = constants.ANDROID_PI_PACKAGE

        self.tmp_overlay = os.path.join(
            self.tempdir, "private-overlays", "project-cheets-private"
        )
        self.mock_android_dir = android.GetAndroidPackageDir(
            self.android_package, overlay_dir=self.tmp_overlay
        )

        ebuild = os.path.join(
            self.mock_android_dir, self.android_package + "-%s.ebuild"
        )
        self.unstable = ebuild % "9999"
        self.old_version = "25"
        self.old = ebuild % ("%s-r1" % self.old_version)
        self.old2_version = "50"
        self.old2 = ebuild % ("%s-r1" % self.old2_version)
        self.new_version = "100"
        self.new = ebuild % ("%s-r1" % self.new_version)

        osutils.WriteFile(self.unstable, self.unstable_data, makedirs=True)
        osutils.WriteFile(self.old, self.stable_data, makedirs=True)
        osutils.WriteFile(self.old2, self.stable_data, makedirs=True)

        self.build_branch = constants.ANDROID_PI_BUILD_BRANCH
        self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
        self.arc_bucket_url = "gs://a"
        self.runtime_artifacts_bucket_url = "gs://r"

    def setupMockRuntimeDataBuild(self, android_version):
        """Helper to mock a build for runtime data."""

        def _RaiseGSNoSuchKey(*_args, **_kwargs):
            raise gs.GSNoSuchKey("file does not exist")

        archs = ["arm", "arm64", "x86", "x86_64"]
        build_types = ["user", "userdebug"]
        runtime_datas = ["gms_core_cache", "ureadahead_pack_host", "tts_cache"]

        for arch in archs:
            for build_type in build_types:
                for runtime_data in runtime_datas:
                    path = (
                        f"{self.runtime_artifacts_bucket_url}/{runtime_data}_{arch}_"
                        f"{build_type}_{android_version}.tar"
                    )
                    self.gs_mock.AddCmdResult(
                        ["stat", "--", path], side_effect=_RaiseGSNoSuchKey
                    )
        pin_path = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"{constants.ANDROID_PI_BUILD_BRANCH}_pin_version"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", pin_path], side_effect=_RaiseGSNoSuchKey
        )

    def testFindAndroidCandidates(self):
        """Test creation of stable ebuilds from mock dir."""
        (unstable, stable) = cros_mark_android_as_stable.FindAndroidCandidates(
            self.mock_android_dir
        )

        stable_ebuild_paths = [x.ebuild_path for x in stable]
        self.assertEqual(unstable.ebuild_path, self.unstable)
        self.assertEqual(len(stable), 2)
        self.assertIn(self.old, stable_ebuild_paths)
        self.assertIn(self.old2, stable_ebuild_paths)

    def testMarkAndroidEBuildAsStable(self):
        """Test updating of ebuild."""
        self.PatchObject(cros_build_lib, "run")
        self.PatchObject(
            portage_util.EBuild, "GetCrosWorkonVars", return_value=None
        )
        stable_candidate = portage_util.EBuild(self.old2)
        unstable = portage_util.EBuild(self.unstable)
        android_version = self.new_version
        package_dir = self.mock_android_dir
        self.setupMockRuntimeDataBuild(android_version)

        revved = cros_mark_android_as_stable.MarkAndroidEBuildAsStable(
            stable_candidate,
            unstable,
            self.android_package,
            android_version,
            package_dir,
            self.build_branch,
            self.arc_bucket_url,
            self.runtime_artifacts_bucket_url,
        )

        self.assertIsNotNone(revved)
        version_atom, files_to_add, files_to_remove = revved
        self.assertEqual(
            version_atom,
            f"chromeos-base/{self.android_package}-{self.new_version}-r1",
        )
        self.assertEqual(
            files_to_add, [self.new, os.path.join(package_dir, "Manifest")]
        )
        self.assertEqual(files_to_remove, [self.old2])

    def testUpdateDataCollectorArtifacts(self):
        android_version = 100
        # Mock by default runtime artifacts are not found.
        self.setupMockRuntimeDataBuild(android_version)

        # Override few as existing.
        path1 = (
            f"{self.runtime_artifacts_bucket_url}/ureadahead_pack_host_x86_64_"
            f"user_{android_version}.tar"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", path1], stdout=(self.STAT_OUTPUT) % path1
        )
        path2 = (
            f"{self.runtime_artifacts_bucket_url}/gms_core_cache_arm_"
            f"userdebug_{android_version}.tar"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", path2], stdout=(self.STAT_OUTPUT) % path2
        )
        path3 = (
            f"{self.runtime_artifacts_bucket_url}/tts_cache_arm64_"
            f"user_{android_version}.tar"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", path3], stdout=(self.STAT_OUTPUT) % path3
        )

        variables = cros_mark_android_as_stable.UpdateDataCollectorArtifacts(
            android_version,
            self.runtime_artifacts_bucket_url,
            constants.ANDROID_PI_BUILD_BRANCH,
        )

        version_reference = "${PV}"
        expectation1 = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"ureadahead_pack_host_x86_64_user_{version_reference}.tar"
        )
        expectation2 = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"gms_core_cache_arm_userdebug_{version_reference}.tar"
        )
        expectation3 = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"tts_cache_arm64_user_{version_reference}.tar"
        )
        self.assertEqual(
            {
                "X86_64_USER_UREADAHEAD_PACK_HOST": expectation1,
                "ARM_USERDEBUG_GMS_CORE_CACHE": expectation2,
                "ARM64_USER_TTS_CACHE": expectation3,
            },
            variables,
        )

    def testUpdateDataCollectorArtifactsPin(self):
        android_version = 100
        android_pin_version = 50
        # Mock by default runtime artifacts are not found.
        self.setupMockRuntimeDataBuild(android_version)
        self.setupMockRuntimeDataBuild(android_pin_version)

        # Override few as existing.
        path1 = (
            f"{self.runtime_artifacts_bucket_url}/ureadahead_pack_host_x86_64_"
            f"user_{android_pin_version}.tar"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", path1], stdout=(self.STAT_OUTPUT) % path1
        )
        path2 = (
            f"{self.runtime_artifacts_bucket_url}/gms_core_cache_arm_"
            f"userdebug_{android_pin_version}.tar"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", path2], stdout=(self.STAT_OUTPUT) % path2
        )
        pin_path = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"{constants.ANDROID_PI_BUILD_BRANCH}_pin_version"
        )
        self.gs_mock.AddCmdResult(
            ["stat", "--", pin_path], stdout=(self.STAT_OUTPUT) % pin_path
        )
        self.gs_mock.AddCmdResult(
            ["cat", pin_path], stdout=str(android_pin_version)
        )

        variables = cros_mark_android_as_stable.UpdateDataCollectorArtifacts(
            android_version,
            self.runtime_artifacts_bucket_url,
            constants.ANDROID_PI_BUILD_BRANCH,
        )

        version_reference = "50"
        expectation1 = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"ureadahead_pack_host_x86_64_user_{version_reference}.tar"
        )
        expectation2 = (
            f"{self.runtime_artifacts_bucket_url}/"
            f"gms_core_cache_arm_userdebug_{version_reference}.tar"
        )
        self.assertEqual(
            {
                "X86_64_USER_UREADAHEAD_PACK_HOST": expectation1,
                "ARM_USERDEBUG_GMS_CORE_CACHE": expectation2,
            },
            variables,
        )

    def testMainRevved(self):
        android_version = self.new_version

        self.PatchObject(cros_build_lib, "run")
        self.PatchObject(
            portage_util.EBuild, "GetCrosWorkonVars", return_value=None
        )
        self.setupMockRuntimeDataBuild(android_version)
        mock_mirror_artifacts = self.PatchObject(
            android, "MirrorArtifacts", return_value=android_version
        )
        mock_print = self.PatchObject(builtins, "print")
        android_bucket_url = "gs://ab"

        cros_mark_android_as_stable.main(
            [
                "--android_bucket_url",
                android_bucket_url,
                "--android_build_branch",
                self.build_branch,
                "--android_package",
                self.android_package,
                "--arc_bucket_url",
                self.arc_bucket_url,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--runtime_artifacts_bucket_url",
                self.runtime_artifacts_bucket_url,
                "--skip_commit",
            ]
        )

        mock_mirror_artifacts.assert_called_once_with(
            android_bucket_url,
            self.build_branch,
            self.arc_bucket_url,
            self.mock_android_dir,
            android_version,
        )
        # pylint: disable=line-too-long
        mock_print.assert_called_once_with(
            '\n{"android_atom": "chromeos-base/android-container-pi-100-r1", "modified_files": ["chromeos-base/android-container-pi/android-container-pi-100-r1.ebuild", "chromeos-base/android-container-pi/Manifest", "chromeos-base/android-container-pi/android-container-pi-50-r1.ebuild"], "revved": true}'
        )

    def testMainNotRevved(self):
        android_version = self.old2_version

        # Mock to create a stable ebuild identical to the original.
        def MockMarkAsStable(_unstable_path, new_stable_path, _vars, **_kwargs):
            osutils.WriteFile(new_stable_path, self.stable_data)

        self.PatchObject(
            portage_util.EBuild, "GetCrosWorkonVars", return_value=None
        )
        self.PatchObject(
            portage_util.EBuild, "MarkAsStable", side_effect=MockMarkAsStable
        )
        self.setupMockRuntimeDataBuild(android_version)
        mock_mirror_artifacts = self.PatchObject(
            android, "MirrorArtifacts", return_value=android_version
        )
        mock_print = self.PatchObject(builtins, "print")
        android_bucket_url = "gs://ab"

        cros_mark_android_as_stable.main(
            [
                "--android_bucket_url",
                android_bucket_url,
                "--android_build_branch",
                self.build_branch,
                "--android_package",
                self.android_package,
                "--arc_bucket_url",
                self.arc_bucket_url,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--runtime_artifacts_bucket_url",
                self.runtime_artifacts_bucket_url,
                "--skip_commit",
            ]
        )

        mock_mirror_artifacts.assert_called_once_with(
            android_bucket_url,
            self.build_branch,
            self.arc_bucket_url,
            self.mock_android_dir,
            android_version,
        )
        mock_print.assert_called_once_with('\n{"revved": false}')

    def testMainUpdateLKGB(self):
        """Tests a successful LKGB update without an actual uprev."""
        android_version = "android-version"
        old_version = "old-version"

        self.PatchObject(cros_mark_android_as_stable, "_PrepareGitBranch")
        mock_commit = self.PatchObject(
            cros_mark_android_as_stable, "_CommitChange"
        )
        self.PatchObject(android, "ReadLKGB", return_value=old_version)
        mock_write_lkgb = self.PatchObject(android, "WriteLKGB")
        mock_mirror_artifacts = self.PatchObject(android, "MirrorArtifacts")
        mock_mark_as_stable = self.PatchObject(
            portage_util.EBuild, "MarkAsStable"
        )

        cros_mark_android_as_stable.main(
            [
                "--android_package",
                self.android_package,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--update_lkgb",
            ]
        )

        mock_write_lkgb.assert_called_once_with(
            self.mock_android_dir, android_version
        )
        mock_commit.assert_called_once()
        mock_mirror_artifacts.assert_not_called()
        mock_mark_as_stable.assert_not_called()

    def testMainUpdateLKGBMissingLKGB(self):
        """Tests LKGB update when LKGB file is currently missing."""
        android_version = "android-version"

        self.PatchObject(cros_mark_android_as_stable, "_PrepareGitBranch")
        mock_commit = self.PatchObject(
            cros_mark_android_as_stable, "_CommitChange"
        )
        self.PatchObject(
            android, "ReadLKGB", side_effect=android.MissingLKGBError()
        )
        mock_write_lkgb = self.PatchObject(android, "WriteLKGB")

        cros_mark_android_as_stable.main(
            [
                "--android_package",
                self.android_package,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--update_lkgb",
            ]
        )

        mock_write_lkgb.assert_called_once_with(
            self.mock_android_dir, android_version
        )
        mock_commit.assert_called_once()

    def testMainUpdateLKGBInvalidLKGB(self):
        """Tests LKGB update when current LKGB file is invalid."""
        android_version = "android-version"

        self.PatchObject(cros_mark_android_as_stable, "_PrepareGitBranch")
        mock_commit = self.PatchObject(
            cros_mark_android_as_stable, "_CommitChange"
        )
        self.PatchObject(
            android, "ReadLKGB", side_effect=android.InvalidLKGBError()
        )
        mock_write_lkgb = self.PatchObject(android, "WriteLKGB")

        cros_mark_android_as_stable.main(
            [
                "--android_package",
                self.android_package,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--update_lkgb",
            ]
        )

        mock_write_lkgb.assert_called_once_with(
            self.mock_android_dir, android_version
        )
        mock_commit.assert_called_once()

    def testMainUpdateLKGBNoUpdate(self):
        """Tests if nothing happens when LKGB is left unchanged."""
        android_version = "old-version"
        old_version = "old-version"

        self.PatchObject(cros_mark_android_as_stable, "_PrepareGitBranch")
        mock_commit = self.PatchObject(
            cros_mark_android_as_stable, "_CommitChange"
        )
        self.PatchObject(android, "ReadLKGB", return_value=old_version)
        mock_write_lkgb = self.PatchObject(android, "WriteLKGB")

        cros_mark_android_as_stable.main(
            [
                "--android_package",
                self.android_package,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--update_lkgb",
            ]
        )

        mock_write_lkgb.assert_not_called()
        mock_commit.assert_not_called()

    def testMainUpdateLKGBWithoutVersion(self):
        """Tests when --force_version flag is missing during LKGB update."""
        self.PatchObject(cros_mark_android_as_stable, "_PrepareGitBranch")

        with self.assertRaises(Exception):
            cros_mark_android_as_stable.main(
                [
                    "--android_package",
                    self.android_package,
                    "--srcroot",
                    str(self.tempdir),
                    "--update_lkgb",
                ]
            )

    def testMainUpdateLKGBSkipCommit(self):
        """Tests when --skip_commit is set during LKGB update."""
        android_version = "android-version"
        old_version = "old-version"

        mock_commit = self.PatchObject(
            cros_mark_android_as_stable, "_CommitChange"
        )
        self.PatchObject(android, "ReadLKGB", return_value=old_version)
        mock_write_lkgb = self.PatchObject(android, "WriteLKGB")

        cros_mark_android_as_stable.main(
            [
                "--android_package",
                self.android_package,
                "--force_version",
                android_version,
                "--srcroot",
                str(self.tempdir),
                "--skip_commit",
                "--update_lkgb",
            ]
        )

        mock_write_lkgb.assert_called_once_with(
            self.mock_android_dir, android_version
        )
        mock_commit.assert_not_called()
