# Copyright 2021 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Android service unittests."""

import logging
import os

from chromite.lib import constants
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import gs_unittest
from chromite.lib import osutils
from chromite.service import android


class ArtifactsConfigTest(cros_test_lib.TestCase):
    """Tests to ensure artifacts configs are properly written."""

    def testAllTargetsAreConfigured(self):
        """Ensure artifact patterns are configured for all packages and targets."""
        self.assertSetEqual(
            set(android.ARTIFACTS_TO_COPY),
            set(constants.ANDROID_PACKAGE_TO_BUILD_TARGETS),
            "Branches configured in ARTIFACTS_TO_COPY doesn't "
            "match list of all Android branches",
        )
        for (
            package,
            ebuild_target,
        ) in constants.ANDROID_PACKAGE_TO_BUILD_TARGETS.items():
            self.assertSetEqual(
                set(android.ARTIFACTS_TO_COPY[package]),
                set(ebuild_target.values()),
                f"For package {package}, targets configured in "
                "ARTIFACTS_TO_COPY doesn't match list of all "
                "supported targets",
            )


class GetAndroidBranchForPackageTest(cros_test_lib.TestCase):
    """Tests for GetAndroidBranchForPackage."""

    def testAllPackagesAreMapped(self):
        """Ensure all possible Android packages are mapped to valid branches."""
        for package in constants.ANDROID_ALL_PACKAGES:
            android.GetAndroidBranchForPackage(package)

    def testRaisesOnUnknownPackage(self):
        """Ensure passing an unknown package raises an exception."""
        with self.assertRaises(ValueError):
            android.GetAndroidBranchForPackage("not-an-android-package")


class MockAndroidBuildArtifactsTest(cros_test_lib.MockTempDirTestCase):
    """Tests using a mocked GS bucket containing Android build artifacts."""

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
        self.android_package = "android-package"

        self.tmp_overlay = os.path.join(self.tempdir, "chromiumos-overlay")
        self.mock_android_dir = android.GetAndroidPackageDir(
            self.android_package, overlay_dir=self.tmp_overlay
        )

        self.old_version = "25"
        self.old2_version = "50"
        self.new_version = "100"
        self.partial_new_version = "150"
        self.not_new_version = "200"

        self.arm_acl_data = "-g google.com:READ"
        self.x86_acl_data = "-g google.com:WRITE"
        self.public_acl_data = "-u AllUsers:READ"
        self.arm_acl = os.path.join(
            self.mock_android_dir, android.ARC_BUCKET_ACL_ARM
        )
        self.x86_acl = os.path.join(
            self.mock_android_dir, android.ARC_BUCKET_ACL_X86
        )
        self.public_acl = os.path.join(
            self.mock_android_dir, android.ARC_BUCKET_ACL_PUBLIC
        )

        osutils.WriteFile(self.arm_acl, self.arm_acl_data, makedirs=True)
        osutils.WriteFile(self.x86_acl, self.x86_acl_data, makedirs=True)
        osutils.WriteFile(self.public_acl, self.public_acl_data, makedirs=True)

        self.bucket_url = "gs://u"
        self.build_branch = "android-branch"
        self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
        self.arc_bucket_url = "gs://a"
        self.targets = {
            "apps": "^(foo|bar)$",
            "target_arm": r"\.zip$",
            "target_x86": r"\.zip$",
        }

        self.PatchDict(
            android.ARTIFACTS_TO_COPY, {self.android_package: self.targets}
        )
        self.PatchObject(
            android,
            "GetAndroidBranchForPackage",
            return_value=self.build_branch,
        )

        targets = {
            "apps": {
                self.old_version,
                self.old2_version,
                self.new_version,
            },
            "target_arm": [
                self.old_version,
                self.old2_version,
                self.new_version,
                self.partial_new_version,
            ],
            "target_x86": [
                self.old_version,
                self.old2_version,
                self.new_version,
            ],
        }

        for target, versions in targets.items():
            url = self.makeSrcTargetUrl(target)
            versions = "\n".join(
                os.path.join(url, version) for version in versions
            )
            self.gs_mock.AddCmdResult(["ls", "--", url], stdout=versions)

        for version in [self.old_version, self.old2_version, self.new_version]:
            for target in self.targets:
                self.setupMockBuild(target, version)

        self.new_subpaths = {
            "apps": "apps100",
            "target_arm": "target_arm100",
            "target_x86": "target_x86100",
        }

        self.setupMockBuild("apps", self.partial_new_version, valid=False)
        self.setupMockBuild("target_arm", self.partial_new_version)
        self.setupMockBuild("target_x86", self.partial_new_version, valid=False)

        for key in self.targets.keys():
            self.setupMockBuild(key, self.not_new_version, False)

    def setupMockBuild(self, target, version, valid=True):
        """Helper to mock a build."""

        def _RaiseGSNoSuchKey(*_args, **_kwargs):
            raise gs.GSNoSuchKey("file does not exist")

        src_url = self.makeSrcUrl(target, version)
        if valid:
            # Show source subpath directory.
            src_subdir = os.path.join(
                src_url, self.makeSubpath(target, version)
            )
            self.gs_mock.AddCmdResult(["ls", "--", src_url], stdout=src_subdir)

            # Show files.
            mock_file_template_list = {
                "apps": ["foo", "bar", "baz"],
                "target_arm": [
                    "foo-%(version)s.zip",
                    "bar.zip",
                    "baz",
                ],
                "target_x86": [
                    "foo-%(version)s.zip",
                    "bar.zip",
                    "baz",
                ],
            }
            filelist = [
                template % {"version": version}
                for template in mock_file_template_list[target]
            ]
            src_filelist = [
                os.path.join(src_subdir, filename) for filename in filelist
            ]
            self.gs_mock.AddCmdResult(
                ["ls", "--", src_subdir], stdout="\n".join(src_filelist)
            )
            for src_file in src_filelist:
                self.gs_mock.AddCmdResult(
                    ["stat", "--", src_file],
                    stdout=(self.STAT_OUTPUT) % src_url,
                )

            # Show nothing in destination.
            dst_url = self.makeDstUrl(target, version)
            filelist = [
                template % {"version": version}
                for template in mock_file_template_list[target]
            ]
            dst_filelist = [
                os.path.join(dst_url, filename) for filename in filelist
            ]
            for dst_file in dst_filelist:
                self.gs_mock.AddCmdResult(
                    ["stat", "--", dst_file], side_effect=_RaiseGSNoSuchKey
                )
            logging.warning("mocking no %s", dst_url)

            # Allow copying of source to dest.
            for src_file, dst_file in zip(src_filelist, dst_filelist):
                self.gs_mock.AddCmdResult(
                    ["cp", "-v", "--", src_file, dst_file]
                )

            # Allow setting ACL on dest files.
            acls = {
                "apps": self.public_acl_data,
                "target_arm": self.arm_acl_data,
                "target_x86": self.x86_acl_data,
            }
            for dst_file in dst_filelist:
                self.gs_mock.AddCmdResult(
                    ["acl", "ch"] + acls[target].split() + [dst_file]
                )
        else:
            self.gs_mock.AddCmdResult(
                ["ls", "--", src_url], side_effect=_RaiseGSNoSuchKey
            )

    def makeSrcTargetUrl(self, target):
        """Helper to return the url for a target."""
        return os.path.join(
            self.bucket_url, f"{self.build_branch}-linux-{target}"
        )

    def makeSrcUrl(self, target, version):
        """Helper to return the url for a build."""
        return os.path.join(self.makeSrcTargetUrl(target), version)

    def makeDstTargetUrl(self, target):
        """Helper to return the url for a target."""
        return os.path.join(
            self.arc_bucket_url, f"{self.build_branch}-linux-{target}"
        )

    def makeDstUrl(self, target, version):
        """Helper to return the url for a build."""
        return os.path.join(self.makeDstTargetUrl(target), version)

    def makeSubpath(self, target, version):
        """Helper to return the subpath for a build."""
        return "%s%s" % (target, version)

    def testIsBuildIdValid(self):
        """Test if checking if build valid."""
        subpaths = android.IsBuildIdValid(
            self.android_package, self.old_version, self.bucket_url
        )
        self.assertTrue(subpaths)
        self.assertEqual(len(subpaths), len(self.targets))
        self.assertEqual(subpaths["apps"], "apps25")
        self.assertEqual(subpaths["target_arm"], "target_arm25")
        self.assertEqual(subpaths["target_x86"], "target_x8625")

        subpaths = android.IsBuildIdValid(
            self.android_package, self.new_version, self.bucket_url
        )
        self.assertEqual(subpaths, self.new_subpaths)

        subpaths = android.IsBuildIdValid(
            self.android_package,
            self.partial_new_version,
            self.bucket_url,
        )
        self.assertEqual(subpaths, None)

        subpaths = android.IsBuildIdValid(
            self.android_package,
            self.not_new_version,
            self.bucket_url,
        )
        self.assertEqual(subpaths, None)

    def testGetLatestBuild(self):
        """Test determination of latest build from gs bucket."""
        version, subpaths = android.GetLatestBuild(
            self.android_package, self.bucket_url
        )
        self.assertEqual(version, self.new_version)
        self.assertTrue(subpaths)
        self.assertEqual(len(subpaths), len(self.targets))
        self.assertEqual(subpaths["apps"], "apps100")
        self.assertEqual(subpaths["target_arm"], "target_arm100")
        self.assertEqual(subpaths["target_x86"], "target_x86100")

    def testCopyToArcBucket(self):
        """Test copying of images to ARC bucket."""
        android.CopyToArcBucket(
            self.bucket_url,
            self.android_package,
            self.new_version,
            self.new_subpaths,
            self.arc_bucket_url,
            self.mock_android_dir,
        )


class LKGBTest(cros_test_lib.TempDirTestCase):
    """Tests ReadLKGB/WriteLKGB."""

    def testWriteReadLGKB(self):
        android_package_dir = self.tempdir
        build_id = "build-id"

        android.WriteLKGB(android_package_dir, build_id)
        self.assertEqual(android.ReadLKGB(android_package_dir), build_id)

    def testReadLKGBMissing(self):
        android_package_dir = self.tempdir

        with self.assertRaises(android.MissingLKGBError):
            android.ReadLKGB(android_package_dir)

    def testReadLKGBNotJSON(self):
        android_package_dir = self.tempdir
        with open(os.path.join(android_package_dir, "LKGB.json"), "w") as f:
            f.write("not-a-json-file")

        with self.assertRaises(android.InvalidLKGBError):
            android.ReadLKGB(android_package_dir)

    def testReadLKGBMissingBuildID(self):
        android_package_dir = self.tempdir
        with open(os.path.join(android_package_dir, "LKGB.json"), "w") as f:
            f.write('{"not_build_id": "foo"}')

        with self.assertRaises(android.InvalidLKGBError):
            android.ReadLKGB(android_package_dir)
