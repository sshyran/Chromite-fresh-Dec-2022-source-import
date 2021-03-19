# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Android service unittests."""

import os

from chromite.lib import constants
from chromite.lib import cros_logging as logging
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import gs_unittest
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.service import android


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
    self.android_package = constants.ANDROID_CONTAINER_PACKAGE_KEYWORD

    self.tmp_overlay = os.path.join(self.tempdir, 'chromiumos-overlay')
    self.mock_android_dir = os.path.join(
        self.tmp_overlay,
        portage_util.GetFullAndroidPortagePackageName(self.android_package))

    self.old_version = '25'
    self.old2_version = '50'
    self.new_version = '100'
    self.partial_new_version = '150'
    self.not_new_version = '200'

    self.arm_acl_data = '-g google.com:READ'
    self.x86_acl_data = '-g google.com:WRITE'
    self.public_acl_data = '-u AllUsers:READ'
    self.arm_acl = os.path.join(self.mock_android_dir,
                                android.ARC_BUCKET_ACL_ARM)
    self.x86_acl = os.path.join(self.mock_android_dir,
                                android.ARC_BUCKET_ACL_X86)
    self.public_acl = os.path.join(self.mock_android_dir,
                                   android.ARC_BUCKET_ACL_PUBLIC)

    osutils.WriteFile(self.arm_acl, self.arm_acl_data, makedirs=True)
    osutils.WriteFile(self.x86_acl, self.x86_acl_data, makedirs=True)
    osutils.WriteFile(self.public_acl, self.public_acl_data, makedirs=True)

    self.bucket_url = 'gs://u'
    self.build_branch = constants.ANDROID_PI_BUILD_BRANCH
    self.gs_mock = self.StartPatcher(gs_unittest.GSContextMock())
    self.arc_bucket_url = 'gs://a'
    self.targets = constants.ANDROID_BRANCH_TO_BUILD_TARGETS[self.build_branch]

    builds = {
        'APPS': [
            self.old_version, self.old2_version, self.new_version,
        ],
        'ARM': [
            self.old_version, self.old2_version, self.new_version,
            self.partial_new_version
        ],
        'ARM64': [
            self.old_version, self.old2_version, self.new_version,
        ],
        'X86': [self.old_version, self.old2_version, self.new_version],
        'X86_64': [self.old_version, self.old2_version, self.new_version],
        'ARM_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version,
        ],
        'ARM64_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version,
        ],
        'X86_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version
        ],
        'X86_64_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version
        ],
        'SDK_GOOGLE_X86_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version
        ],
        'SDK_GOOGLE_X86_64_USERDEBUG': [
            self.old_version, self.old2_version, self.new_version
        ],
    }
    for build_type, builds in builds.items():
      url = self.makeSrcTargetUrl(self.targets[build_type][0])
      builds = '\n'.join(os.path.join(url, version) for version in builds)
      self.gs_mock.AddCmdResult(['ls', '--', url], output=builds)

    for version in [self.old_version, self.old2_version, self.new_version]:
      for key in self.targets.keys():
        self.setupMockBuild(key, version)
    self.new_subpaths = {
        'APPS': 'apps100',
        'ARM': 'cheets_arm-user100',
        'ARM64': 'cheets_arm64-user100',
        'X86': 'cheets_x86-user100',
        'X86_64': 'cheets_x86_64-user100',
        'ARM_USERDEBUG': 'cheets_arm-userdebug100',
        'ARM64_USERDEBUG': 'cheets_arm64-userdebug100',
        'X86_USERDEBUG': 'cheets_x86-userdebug100',
        'X86_64_USERDEBUG': 'cheets_x86_64-userdebug100',
        'SDK_GOOGLE_X86_USERDEBUG': 'sdk_cheets_x86-userdebug100',
        'SDK_GOOGLE_X86_64_USERDEBUG': 'sdk_cheets_x86_64-userdebug100',
    }

    self.setupMockBuild('APPS', self.partial_new_version, valid=False)
    self.setupMockBuild('ARM', self.partial_new_version)
    self.setupMockBuild('ARM64', self.partial_new_version, valid=False)
    self.setupMockBuild('X86', self.partial_new_version, valid=False)
    self.setupMockBuild('X86_64', self.partial_new_version, valid=False)
    self.setupMockBuild('ARM_USERDEBUG', self.partial_new_version, valid=False)
    self.setupMockBuild('ARM64_USERDEBUG', self.partial_new_version,
                        valid=False)
    self.setupMockBuild('X86_USERDEBUG', self.partial_new_version, valid=False)
    self.setupMockBuild('X86_64_USERDEBUG', self.partial_new_version,
                        valid=False)
    self.setupMockBuild('SDK_GOOGLE_X86_USERDEBUG', self.partial_new_version,
                        valid=False)
    self.setupMockBuild('SDK_GOOGLE_X86_64_USERDEBUG', self.partial_new_version,
                        valid=False)

    for key in self.targets.keys():
      self.setupMockBuild(key, self.not_new_version, False)

  def setupMockBuild(self, key, version, valid=True):
    """Helper to mock a build."""
    def _RaiseGSNoSuchKey(*_args, **_kwargs):
      raise gs.GSNoSuchKey('file does not exist')

    target = self.targets[key][0]
    src_url = self.makeSrcUrl(target, version)
    if valid:
      # Show source subpath directory.
      src_subdir = os.path.join(src_url, self.makeSubpath(target, version))
      self.gs_mock.AddCmdResult(['ls', '--', src_url], output=src_subdir)

      # Show files.
      mock_file_template_list = {
          'APPS': ['org.chromium.arc.cachebuilder.jar'],
          'ARM': ['file-%(version)s.zip', 'adb', 'sepolicy.zip'],
          'ARM64': ['cheets_arm64-file-%(version)s.zip', 'sepolicy.zip'],
          'X86': ['file-%(version)s.zip'],
          'X86_64': ['file-%(version)s.zip'],
          'ARM_USERDEBUG': ['cheets_arm-file-%(version)s.zip', 'adb',
                            'sepolicy.zip'],
          'ARM64_USERDEBUG': ['cheets_arm64-file-%(version)s.zip', 'adb',
                              'sepolicy.zip'],
          'X86_USERDEBUG': ['cheets_x86-file-%(version)s.zip', 'sepolicy.zip'],
          'X86_64_USERDEBUG': ['cheets_x86_64-file-%(version)s.zip'],
          'SDK_GOOGLE_X86_USERDEBUG':
              ['sdk_cheets_x86-file-%(version)s.zip'],
          'SDK_GOOGLE_X86_64_USERDEBUG':
              ['sdk_cheets_x86_64-file-%(version)s.zip'],
      }
      filelist = [template % {'version': version}
                  for template in mock_file_template_list[key]]
      src_filelist = [os.path.join(src_subdir, filename)
                      for filename in filelist]
      self.gs_mock.AddCmdResult(['ls', '--', src_subdir],
                                output='\n'.join(src_filelist))
      for src_file in src_filelist:
        self.gs_mock.AddCmdResult(['stat', '--', src_file],
                                  output=(self.STAT_OUTPUT) % src_url)

      # Show nothing in destination.
      dst_url = self.makeDstUrl(target, version)
      # Show files.
      mock_file_template_list = {
          'APPS': ['org.chromium.arc.cachebuilder.jar'],
          'ARM': ['file-%(version)s.zip', 'adb', 'sepolicy.zip'],
          'ARM64': ['cheets_arm64-file-%(version)s.zip', 'sepolicy.zip'],
          'X86': ['file-%(version)s.zip'],
          'X86_64': ['file-%(version)s.zip'],
          'ARM_USERDEBUG': ['cheets_arm_userdebug-file-%(version)s.zip',
                            'adb', 'sepolicy.zip'],
          'ARM64_USERDEBUG': ['cheets_arm64_userdebug-file-%(version)s.zip',
                              'adb', 'sepolicy.zip'],
          'X86_USERDEBUG':
              ['cheets_x86_userdebug-file-%(version)s.zip', 'sepolicy.zip'],
          'X86_64_USERDEBUG': ['cheets_x86_64_userdebug-file-%(version)s.zip'],
          'SDK_GOOGLE_X86_USERDEBUG':
              ['cheets_sdk_google_x86_userdebug-file-%(version)s.zip'],
          'SDK_GOOGLE_X86_64_USERDEBUG':
              ['cheets_sdk_google_x86_64_userdebug-file-%(version)s.zip'],
      }
      filelist = [template % {'version': version}
                  for template in mock_file_template_list[key]]
      dst_filelist = [os.path.join(dst_url, filename)
                      for filename in filelist]
      for dst_file in dst_filelist:
        self.gs_mock.AddCmdResult(['stat', '--', dst_file],
                                  side_effect=_RaiseGSNoSuchKey)
      logging.warning('mocking no %s', dst_url)

      # Allow copying of source to dest.
      for src_file, dst_file in zip(src_filelist, dst_filelist):
        self.gs_mock.AddCmdResult(['cp', '-v', '--', src_file, dst_file])

      # Allow setting ACL on dest files.
      acls = {
          'APPS': self.public_acl_data,
          'ARM': self.arm_acl_data,
          'ARM64': self.arm_acl_data,
          'X86': self.x86_acl_data,
          'X86_64': self.x86_acl_data,
          'ARM_USERDEBUG': self.arm_acl_data,
          'ARM64_USERDEBUG': self.arm_acl_data,
          'X86_USERDEBUG': self.x86_acl_data,
          'X86_64_USERDEBUG': self.x86_acl_data,
          'SDK_GOOGLE_X86_USERDEBUG': self.x86_acl_data,
          'SDK_GOOGLE_X86_64_USERDEBUG': self.x86_acl_data,
      }
      for dst_file in dst_filelist:
        self.gs_mock.AddCmdResult(
            ['acl', 'ch'] + acls[key].split() + [dst_file])
    else:
      self.gs_mock.AddCmdResult(['ls', '--', src_url],
                                side_effect=_RaiseGSNoSuchKey)

  def makeSrcTargetUrl(self, target):
    """Helper to return the url for a target."""
    return os.path.join(self.bucket_url,
                        f'{self.build_branch}-linux-{target}')

  def makeSrcUrl(self, target, version):
    """Helper to return the url for a build."""
    return os.path.join(self.makeSrcTargetUrl(target), version)

  def makeDstTargetUrl(self, target):
    """Helper to return the url for a target."""
    return os.path.join(self.arc_bucket_url,
                        f'{self.build_branch}-linux-{target}')

  def makeDstUrl(self, target, version):
    """Helper to return the url for a build."""
    return os.path.join(self.makeDstTargetUrl(target), version)

  def makeSubpath(self, target, version):
    """Helper to return the subpath for a build."""
    return '%s%s' % (target, version)

  def testIsBuildIdValid(self):
    """Test if checking if build valid."""
    subpaths = android.IsBuildIdValid(self.bucket_url, self.build_branch,
                                      self.old_version)
    self.assertTrue(subpaths)
    self.assertEqual(len(subpaths), 11)
    self.assertEqual(subpaths['APPS'], 'apps25')
    self.assertEqual(subpaths['ARM'], 'cheets_arm-user25')
    self.assertEqual(subpaths['ARM64'], 'cheets_arm64-user25')
    self.assertEqual(subpaths['X86'], 'cheets_x86-user25')
    self.assertEqual(subpaths['X86_64'], 'cheets_x86_64-user25')
    self.assertEqual(subpaths['ARM_USERDEBUG'], 'cheets_arm-userdebug25')
    self.assertEqual(subpaths['ARM64_USERDEBUG'], 'cheets_arm64-userdebug25')
    self.assertEqual(subpaths['X86_USERDEBUG'], 'cheets_x86-userdebug25')
    self.assertEqual(subpaths['X86_64_USERDEBUG'], 'cheets_x86_64-userdebug25')
    self.assertEqual(subpaths['SDK_GOOGLE_X86_USERDEBUG'],
                     'sdk_cheets_x86-userdebug25')
    self.assertEqual(subpaths['SDK_GOOGLE_X86_64_USERDEBUG'],
                     'sdk_cheets_x86_64-userdebug25')

    subpaths = android.IsBuildIdValid(self.bucket_url, self.build_branch,
                                      self.new_version)
    self.assertEqual(subpaths, self.new_subpaths)

    subpaths = android.IsBuildIdValid(self.bucket_url, self.build_branch,
                                      self.partial_new_version)
    self.assertEqual(subpaths, None)

    subpaths = android.IsBuildIdValid(self.bucket_url, self.build_branch,
                                      self.not_new_version)
    self.assertEqual(subpaths, None)

  def testGetLatestBuild(self):
    """Test determination of latest build from gs bucket."""
    version, subpaths = android.GetLatestBuild(self.bucket_url,
                                               self.build_branch)
    self.assertEqual(version, self.new_version)
    self.assertTrue(subpaths)
    self.assertEqual(len(subpaths), 11)
    self.assertEqual(subpaths['APPS'], 'apps100')
    self.assertEqual(subpaths['ARM'], 'cheets_arm-user100')
    self.assertEqual(subpaths['ARM64'], 'cheets_arm64-user100')
    self.assertEqual(subpaths['X86'], 'cheets_x86-user100')
    self.assertEqual(subpaths['X86_64'], 'cheets_x86_64-user100')
    self.assertEqual(subpaths['ARM_USERDEBUG'], 'cheets_arm-userdebug100')
    self.assertEqual(subpaths['ARM64_USERDEBUG'], 'cheets_arm64-userdebug100')
    self.assertEqual(subpaths['X86_USERDEBUG'], 'cheets_x86-userdebug100')
    self.assertEqual(subpaths['X86_64_USERDEBUG'], 'cheets_x86_64-userdebug100')
    self.assertEqual(subpaths['SDK_GOOGLE_X86_USERDEBUG'],
                     'sdk_cheets_x86-userdebug100')
    self.assertEqual(subpaths['SDK_GOOGLE_X86_64_USERDEBUG'],
                     'sdk_cheets_x86_64-userdebug100')

  def _AuxGetArcBasename(self, build, basename):
    """Helper function for readability."""
    # pylint: disable=protected-access
    return android._GetArcBasename(build, basename)

  def testGetArcBasenameNoRename(self):
    """Test build targets that don't require renaming."""
    default_bn = 'do_not_rename_basename'
    no_rename_build_targets = ['ARM', 'ARM64', 'X86']
    for build in no_rename_build_targets:
      self.assertEqual(self._AuxGetArcBasename(build, default_bn), default_bn)

    self.assertEqual(self._AuxGetArcBasename('UNKNOWN', default_bn), default_bn)
    self.assertEqual(self._AuxGetArcBasename('', default_bn), default_bn)
    self.assertEqual(self._AuxGetArcBasename(None, default_bn), default_bn)

  def testGetArcBasenameRenameValid(self):
    """Test renaming when input basename is valid."""
    # Actual name patterns.
    build_targets = {
        'X86_USERDEBUG':
            ('cheets_x86-target_files-25.zip',
             'cheets_x86_userdebug-target_files-25.zip'),
        'SDK_GOOGLE_X86_USERDEBUG':
            ('sdk_cheets_x86-target_files-25.zip',
             'cheets_sdk_google_x86_userdebug-target_files-25.zip'),
    }
    for build, (src, dst) in build_targets.items():
      self.assertEqual(self._AuxGetArcBasename(build, src), dst)

    # More generic name patterns.
    build_targets['X86_USERDEBUG'] = (
        ('cheets_-XXX', 'cheets_x86_userdebug-XXX')
    )
    build_targets['SDK_GOOGLE_X86_USERDEBUG'] = (
        ('cheets_-XXX', 'cheets_sdk_google_x86_userdebug-XXX')
    )
    for build, (src, dst) in build_targets.items():
      self.assertEqual(self._AuxGetArcBasename(build, src), dst)

    # Check bertha also.
    build_targets['X86_USERDEBUG'] = (
        ('bertha_-XXX', 'bertha_x86_userdebug-XXX')
    )
    build_targets['SDK_GOOGLE_X86_USERDEBUG'] = (
        ('bertha_-XXX', 'bertha_sdk_google_x86_userdebug-XXX')
    )
    for build, (src, dst) in build_targets.items():
      self.assertEqual(self._AuxGetArcBasename(build, src), dst)

  def testGetArcBasenameRenameInvalid(self):
    """Test that basename is unchanged if it's not as expected."""
    # Missing hyphen.
    self.assertEqual(self._AuxGetArcBasename('X86_USERDEBUG',
                                             'cheets_x86.zip'),
                     'cheets_x86.zip')
    # Missing 'cheets_' before first hyphen.
    self.assertEqual(self._AuxGetArcBasename('X86_USERDEBUG',
                                             'marlin_x86-25.zip'),
                     'marlin_x86-25.zip')
    self.assertEqual(self._AuxGetArcBasename('X86_USERDEBUG',
                                             'XX-cheets_x86-25.zip'),
                     'XX-cheets_x86-25.zip')

  def testCopyToArcBucket(self):
    """Test copying of images to ARC bucket."""
    android.CopyToArcBucket(self.bucket_url, self.build_branch,
                            self.new_version, self.new_subpaths,
                            self.arc_bucket_url, self.mock_android_dir)
