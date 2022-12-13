# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Image service tests."""

import os
from pathlib import Path
from typing import List, Optional
from unittest import mock

from chromite.api import api_config
from chromite.api import controller
from chromite.api.controller import image as image_controller
from chromite.api.gen.chromite.api import image_pb2
from chromite.api.gen.chromite.api import sysroot_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.scripts import pushimage
from chromite.service import image as image_service


class CreateTest(cros_test_lib.MockTempDirTestCase, api_config.ApiConfigMixin):
  """Create image tests."""

  def setUp(self):
    self.response = image_pb2.CreateImageResult()

  def _GetRequest(self,
                  board=None,
                  types=None,
                  version=None,
                  builder_path=None,
                  disable_rootfs_verification=False,
                  base_is_recovery=False):
    """Helper to build a request instance."""
    return image_pb2.CreateImageRequest(
        build_target={'name': board},
        image_types=types,
        disable_rootfs_verification=disable_rootfs_verification,
        version=version,
        builder_path=builder_path,
        base_is_recovery=base_is_recovery,
    )

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(image_service, 'Build')

    request = self._GetRequest(board='board')
    image_controller.Create(request, self.response, self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Test that mock call does not execute any logic, returns mocked value."""
    patch = self.PatchObject(image_service, 'Build')

    request = self._GetRequest(board='board')
    image_controller.Create(request, self.response, self.mock_call_config)
    patch.assert_not_called()
    self.assertEqual(self.response.success, True)

  def testMockError(self):
    """Test that mock call does not execute any logic, returns error."""
    patch = self.PatchObject(image_service, 'Build')

    request = self._GetRequest(board='board')
    rc = image_controller.Create(request, self.response, self.mock_error_config)
    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY, rc)

  def testNoBoard(self):
    """Test no board given fails."""
    request = self._GetRequest()

    # No board should cause it to fail.
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.Create(request, self.response, self.api_config)

  def testNoTypeSpecified(self):
    """Test the image type default."""
    request = self._GetRequest(board='board')

    # Failed result to avoid the success handling logic.
    result = image_service.BuildResult([constants.IMAGE_TYPE_BASE])
    result.return_code = 1
    build_patch = self.PatchObject(image_service, 'Build', return_value=result)

    image_controller.Create(request, self.response, self.api_config)
    build_patch.assert_any_call(
        'board', [constants.IMAGE_TYPE_BASE], config=mock.ANY)

  def testSingleTypeSpecified(self):
    """Test it's properly using a specified type."""
    request = self._GetRequest(board='board', types=[common_pb2.IMAGE_TYPE_DEV])

    # Failed result to avoid the success handling logic.
    result = image_service.BuildResult([constants.IMAGE_TYPE_DEV])
    result.return_code = 1
    build_patch = self.PatchObject(image_service, 'Build', return_value=result)

    image_controller.Create(request, self.response, self.api_config)
    build_patch.assert_any_call(
        'board', [constants.IMAGE_TYPE_DEV], config=mock.ANY)

  def testMultipleAndImpliedTypes(self):
    """Test multiple types and implied type handling."""
    # The TEST_VM type should force it to build the test image.
    types = [common_pb2.IMAGE_TYPE_BASE, common_pb2.IMAGE_TYPE_TEST_VM]
    expected_images = [constants.IMAGE_TYPE_BASE, constants.IMAGE_TYPE_TEST]

    request = self._GetRequest(board='board', types=types)

    # Failed result to avoid the success handling logic.
    result = image_service.BuildResult(expected_images)
    result.return_code = 1
    build_patch = self.PatchObject(image_service, 'Build', return_value=result)

    image_controller.Create(request, self.response, self.api_config)
    build_patch.assert_any_call('board', expected_images, config=mock.ANY)

  def testRecoveryImpliedTypes(self):
    """Test implied type handling of recovery images."""
    # The TEST_VM type should force it to build the test image.
    types = [common_pb2.IMAGE_TYPE_RECOVERY]

    request = self._GetRequest(board='board', types=types)

    # Failed result to avoid the success handling logic.
    result = image_service.BuildResult([])
    result.return_code = 1
    build_patch = self.PatchObject(image_service, 'Build', return_value=result)

    image_controller.Create(request, self.response, self.api_config)
    build_patch.assert_any_call(
        'board', [constants.IMAGE_TYPE_BASE], config=mock.ANY)

  def testFailedPackageHandling(self):
    """Test failed packages are populated correctly."""
    result = image_service.BuildResult([])
    result.return_code = 1
    result.failed_packages = ['foo/bar', 'cat/pkg']
    expected_packages = [('foo', 'bar'), ('cat', 'pkg')]
    self.PatchObject(image_service, 'Build', return_value=result)

    input_proto = self._GetRequest(board='board')

    rc = image_controller.Create(input_proto, self.response, self.api_config)

    self.assertEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE, rc)
    for package in self.response.failed_packages:
      self.assertIn((package.category, package.package_name), expected_packages)

  def testNoPackagesFailureHandling(self):
    """Test failed packages are populated correctly."""
    result = image_service.BuildResult([])
    result.return_code = 1
    self.PatchObject(image_service, 'Build', return_value=result)

    input_proto = image_pb2.CreateImageRequest()
    input_proto.build_target.name = 'board'

    rc = image_controller.Create(input_proto, self.response, self.api_config)
    self.assertTrue(rc)
    self.assertNotEqual(controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE,
                        rc)
    self.assertFalse(self.response.failed_packages)


class RecoveryImageTest(cros_test_lib.RunCommandTempDirTestCase,
                        api_config.ApiConfigMixin):
  """Recovery image tests."""

  def setUp(self):
    self.response = image_pb2.CreateImageResult()
    self.types = [common_pb2.IMAGE_TYPE_BASE, common_pb2.IMAGE_TYPE_RECOVERY]
    self.build_result = self._CreateMockBuildResult(
        [common_pb2.IMAGE_TYPE_BASE])

    self.PatchObject(
        image_service,
        'Build',
        side_effect=[
            self.build_result,
            self._CreateMockBuildResult([common_pb2.IMAGE_TYPE_FACTORY]),
        ])
    self.copy_image_mock = self.PatchObject(
        image_service,
        'CopyBaseToRecovery',
        side_effect=[
            self._CreateMockBuildResult([common_pb2.IMAGE_TYPE_RECOVERY]),
        ])
    self.recov_image_mock = self.PatchObject(
        image_service,
        'BuildRecoveryImage',
        side_effect=[
            self._CreateMockBuildResult([common_pb2.IMAGE_TYPE_RECOVERY]),
        ])

  def _GetRequest(self,
                  board=None,
                  types=None,
                  version=None,
                  builder_path=None,
                  disable_rootfs_verification=False,
                  base_is_recovery=False):
    """Helper to build a request instance."""
    return image_pb2.CreateImageRequest(
        build_target={'name': board},
        image_types=types,
        disable_rootfs_verification=disable_rootfs_verification,
        version=version,
        builder_path=builder_path,
        base_is_recovery=base_is_recovery,
    )

  def _CreateMockBuildResult(
      self, image_types: List[int]) -> Optional[image_service.BuildResult]:
    """Helper to create Mock build_image results.

    Args:
      image_types: A list of image types for which the mock BuildResult has to
        be creates.

    Returns:
      A list of mock BuildResult.
    """
    image_types_names = [
        image_controller.SUPPORTED_IMAGE_TYPES[x]
        for x in image_types
        if image_controller.SUPPORTED_IMAGE_TYPES[x] in
        constants.IMAGE_TYPE_TO_NAME
    ]

    if not image_types_names:
      if common_pb2.IMAGE_TYPE_FACTORY in image_types and len(image_types) == 1:
        image_types_names.append(constants.IMAGE_TYPE_FACTORY_SHIM)
      else:
        return None

    _build_result = image_service.BuildResult(image_types_names)
    _build_result.return_code = 0
    for image_type in image_types_names:
      test_image = Path(self.tempdir) / constants.IMAGE_TYPE_TO_NAME[image_type]
      test_image.touch()
      _build_result.add_image(image_type, test_image)

    return _build_result

  def testBaseIsRecoveryTrue(self):
    """Test that cp is called."""
    input_proto = self._GetRequest(
        board='board', types=self.types, base_is_recovery=True)
    image_controller.Create(input_proto, self.response, self.api_config)

    self.copy_image_mock.assert_called_with(
        board='board',
        image_path=self.build_result.images[constants.IMAGE_TYPE_BASE])

  def testBaseIsRecoveryFalse(self):
    """Test that mod_image_for_recovery.sh is called."""
    input_proto = self._GetRequest(
        board='board', types=self.types, base_is_recovery=False)
    image_controller.Create(input_proto, self.response, self.api_config)

    self.recov_image_mock.assert_called_with(
        board='board',
        image_path=self.build_result.images[constants.IMAGE_TYPE_BASE])


class ImageSignerTestTest(cros_test_lib.MockTempDirTestCase,
                          api_config.ApiConfigMixin):
  """Image signer test tests."""

  def setUp(self):
    self.image_path = os.path.join(self.tempdir, 'image.bin')
    self.result_directory = os.path.join(self.tempdir, 'results')

    osutils.SafeMakedirs(self.result_directory)
    osutils.Touch(self.image_path)

  def testValidateOnly(self):
    """Sanity check that validate-only calls don't execute any logic."""
    patch = self.PatchObject(image_lib, 'SecurityTest', return_value=True)
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    output_proto = image_pb2.TestImageResult()

    image_controller.SignerTest(input_proto, output_proto,
                                self.validate_only_config)

    patch.assert_not_called()

  def testMockCall(self):
    """Test that mock call does not execute any logic, returns mocked value."""
    patch = self.PatchObject(image_lib, 'SecurityTest', return_value=True)
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    output_proto = image_pb2.TestImageResult()

    image_controller.SignerTest(input_proto, output_proto,
                                self.mock_call_config)

    patch.assert_not_called()
    self.assertEqual(output_proto.success, True)

  def testMockError(self):
    """Test that mock call does not execute any logic, returns error."""
    patch = self.PatchObject(image_lib, 'SecurityTest', return_value=True)
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    output_proto = image_pb2.TestImageResult()

    rc = image_controller.SignerTest(input_proto, output_proto,
                                     self.mock_error_config)

    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY, rc)

  def testSignerTestNoImage(self):
    """Test function argument validation."""
    input_proto = image_pb2.TestImageRequest()
    output_proto = image_pb2.TestImageResult()

    # Nothing provided.
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.SignerTest(input_proto, output_proto, self.api_config)

  def testSignerTestSuccess(self):
    """Test successful call handling."""
    self.PatchObject(image_lib, 'SecurityTest', return_value=True)
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    output_proto = image_pb2.TestImageResult()

    image_controller.SignerTest(input_proto, output_proto, self.api_config)

  def testSignerTestFailure(self):
    """Test function output tests."""
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    output_proto = image_pb2.TestImageResult()

    self.PatchObject(image_lib, 'SecurityTest', return_value=False)
    image_controller.SignerTest(input_proto, output_proto, self.api_config)
    self.assertFalse(output_proto.success)


class ImageTestTest(cros_test_lib.MockTempDirTestCase,
                    api_config.ApiConfigMixin):
  """Image test tests."""

  def setUp(self):
    self.image_path = os.path.join(self.tempdir, 'image.bin')
    self.board = 'board'
    self.result_directory = os.path.join(self.tempdir, 'results')

    osutils.SafeMakedirs(self.result_directory)
    osutils.Touch(self.image_path)

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(image_service, 'Test')

    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    input_proto.build_target.name = self.board
    input_proto.result.directory = self.result_directory
    output_proto = image_pb2.TestImageResult()

    image_controller.Test(input_proto, output_proto, self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Test that mock call does not execute any logic, returns mocked value."""
    patch = self.PatchObject(image_service, 'Test')

    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    input_proto.build_target.name = self.board
    input_proto.result.directory = self.result_directory
    output_proto = image_pb2.TestImageResult()

    image_controller.Test(input_proto, output_proto, self.mock_call_config)
    patch.assert_not_called()
    self.assertEqual(output_proto.success, True)

  def testMockError(self):
    """Test that mock call does not execute any logic, returns error."""
    patch = self.PatchObject(image_service, 'Test')

    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    input_proto.build_target.name = self.board
    input_proto.result.directory = self.result_directory
    output_proto = image_pb2.TestImageResult()

    rc = image_controller.Test(input_proto, output_proto,
                               self.mock_error_config)
    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY, rc)

  def testTestArgumentValidation(self):
    """Test function argument validation tests."""
    self.PatchObject(image_service, 'Test', return_value=True)
    input_proto = image_pb2.TestImageRequest()
    output_proto = image_pb2.TestImageResult()

    # Nothing provided.
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.Test(input_proto, output_proto, self.api_config)

    # Just one argument.
    input_proto.build_target.name = self.board
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.Test(input_proto, output_proto, self.api_config)

    # Two arguments provided.
    input_proto.result.directory = self.result_directory
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.Test(input_proto, output_proto, self.api_config)

    # Invalid image path.
    input_proto.image.path = '/invalid/image/path'
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.Test(input_proto, output_proto, self.api_config)

    # All valid arguments.
    input_proto.image.path = self.image_path
    image_controller.Test(input_proto, output_proto, self.api_config)

  def testTestOutputHandling(self):
    """Test function output tests."""
    input_proto = image_pb2.TestImageRequest()
    input_proto.image.path = self.image_path
    input_proto.build_target.name = self.board
    input_proto.result.directory = self.result_directory
    output_proto = image_pb2.TestImageResult()

    self.PatchObject(image_service, 'Test', return_value=True)
    image_controller.Test(input_proto, output_proto, self.api_config)
    self.assertTrue(output_proto.success)

    self.PatchObject(image_service, 'Test', return_value=False)
    image_controller.Test(input_proto, output_proto, self.api_config)
    self.assertFalse(output_proto.success)


class PushImageTest(api_config.ApiConfigMixin):
  """Push image test."""

  def _GetRequest(
      self,
      gs_image_dir='gs://chromeos-image-archive/atlas-release/R89-13604.0.0',
      build_target_name='atlas',
      profile='foo',
      sign_types=None,
      dryrun=True,
      channels=None):
    return image_pb2.PushImageRequest(
        gs_image_dir=gs_image_dir,
        sysroot=sysroot_pb2.Sysroot(
            build_target=common_pb2.BuildTarget(name=build_target_name)),
        profile=common_pb2.Profile(name=profile),
        sign_types=sign_types,
        dryrun=dryrun,
        channels=channels)

  def _GetResponse(self):
    return image_pb2.PushImageRequest()

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testValidateOnly(self, MockPushImage):
    """Check that a validate only call does not execute any logic."""
    req = self._GetRequest(sign_types=[
        common_pb2.IMAGE_TYPE_RECOVERY, common_pb2.IMAGE_TYPE_FACTORY,
        common_pb2.IMAGE_TYPE_FIRMWARE, common_pb2.IMAGE_TYPE_ACCESSORY_USBPD,
        common_pb2.IMAGE_TYPE_ACCESSORY_RWSIG, common_pb2.IMAGE_TYPE_BASE,
        common_pb2.IMAGE_TYPE_GSC_FIRMWARE, common_pb2.IMAGE_TYPE_HPS_FIRMWARE,
    ])
    rc = image_controller.PushImage(req, self.NewResponse(),
                                    self.validate_only_config)
    MockPushImage.assert_not_called()
    self.assertEqual(rc, controller.RETURN_CODE_VALID_INPUT)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testValidateOnlyInvalid(self, MockPushImage):
    """Check that validate call rejects invalid sign types."""
    # Pass unsupported image type.
    req = self._GetRequest(sign_types=[common_pb2.IMAGE_TYPE_DLC])
    rc = image_controller.PushImage(req, self._GetResponse(),
                                    self.validate_only_config)
    MockPushImage.assert_not_called()
    self.assertEqual(rc, controller.RETURN_CODE_INVALID_INPUT)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testMockCall(self, MockPushImage):
    """Test that mock call does not execute any logic, returns mocked value."""
    rc = image_controller.PushImage(self._GetRequest(), self._GetResponse(),
                                    self.mock_call_config)
    MockPushImage.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_SUCCESS, rc)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testMockError(self, MockPushImage):
    """Test that mock call does not execute any logic, returns error."""
    rc = image_controller.PushImage(self._GetRequest(), self._GetResponse(),
                                    self.mock_error_config)
    MockPushImage.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY, rc)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testNoBuildTarget(self, _):
    """Test no build target given fails."""
    request = self._GetRequest(build_target_name='')
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.PushImage(request, self._GetResponse(), self.api_config)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testNoGsImageDir(self, _):
    """Test no image dir given fails."""
    request = self._GetRequest(gs_image_dir='')
    with self.assertRaises(cros_build_lib.DieSystemExit):
      image_controller.PushImage(request, self._GetResponse(), self.api_config)

  @mock.patch.object(pushimage, 'PushImage', return_value={})
  def testCallCorrect(self, MockPushImage):
    """Check that a call is called with the correct parameters."""
    request = self._GetRequest(
        dryrun=False, profile='', sign_types=[common_pb2.IMAGE_TYPE_RECOVERY],
        channels=[common_pb2.CHANNEL_DEV, common_pb2.CHANNEL_CANARY])
    request.dest_bucket = 'gs://foo'
    image_controller.PushImage(request, self._GetResponse(), self.api_config)
    MockPushImage.assert_called_with(
        request.gs_image_dir,
        request.sysroot.build_target.name,
        dry_run=request.dryrun,
        sign_types=['recovery'],
        dest_bucket=request.dest_bucket,
        force_channels=['dev', 'canary'])

  @mock.patch.object(pushimage, 'PushImage', return_value={
      'dev': ['gs://dev/instr1', 'gs://dev/instr2'],
      'canary': ['gs://canary/instr1']})
  def testOutput(self, _):
    """Check that a call populates the response object."""
    request = self._GetRequest(
        profile='', sign_types=[common_pb2.IMAGE_TYPE_RECOVERY],
        channels=[common_pb2.CHANNEL_DEV, common_pb2.CHANNEL_CANARY])
    request.dest_bucket = 'gs://foo'
    response = self._GetResponse()
    image_controller.PushImage(request, response, self.api_config)
    self.assertEqual(
        sorted([i.instructions_file_path for i in response.instructions]),
        sorted(['gs://dev/instr1', 'gs://dev/instr2', 'gs://canary/instr1']))

  def testCallSucceeds(self, _):
    """Check that a (dry run) call is made successfully."""
    request = self._GetRequest(sign_types=[common_pb2.IMAGE_TYPE_RECOVERY])
    rc = image_controller.PushImage(
        request,
        self._GetResponse(),
        self.api_config)
    self.assertEqual(rc, controller.RETURN_CODE_SUCCESS)

  def testCallFailsWithBadImageDir(self):
    """Check that a (dry run) call fails when given a bad gs_image_dir."""
    request = self._GetRequest(gs_image_dir='foo')
    rc = image_controller.PushImage(request, self._GetResponse, self.api_config)
    self.assertEqual(rc, controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY)
