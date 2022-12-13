# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Payload operations."""

from chromite.api import api_config
from chromite.api import controller
from chromite.api.controller import payload
from chromite.api.gen.chromite.api import payload_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import cros_test_lib
from chromite.lib.paygen import paygen_payload_lib


class PayloadApiTests(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Unittests for PayloadApi."""

  def setUp(self):
    self.response = payload_pb2.GenerationResponse()

    src_build = payload_pb2.Build(version='1.0.0', bucket='test',
                                  channel='test-channel', build_target=
                                  common_pb2.BuildTarget(name='cave'))

    src_image = payload_pb2.UnsignedImage(
        build=src_build, image_type=6, milestone='R70')

    tgt_build = payload_pb2.Build(version='2.0.0', bucket='test',
                                  channel='test-channel', build_target=
                                  common_pb2.BuildTarget(name='cave'))

    tgt_image = payload_pb2.UnsignedImage(
        build=tgt_build, image_type=6, milestone='R70')

    self.req = payload_pb2.GenerationRequest(
        tgt_unsigned_image=tgt_image,
        src_unsigned_image=src_image,
        bucket='test-destination-bucket',
        verify=True,
        keyset='update_signer',
        dryrun=False)

    self.minios_req = payload_pb2.GenerationRequest(
        tgt_unsigned_image=tgt_image,
        src_unsigned_image=src_image,
        bucket='test-destination-bucket',
        minios=True,
        verify=True,
        keyset='update_signer',
        dryrun=False)

    self.result = payload_pb2.GenerationResponse(
        success=True,
        local_path='/tmp/aohiwdadoi/delta.bin',
        remote_uri='gs://something')

  def testValidateOnly(self):
    """Basic check that a validate only call does not execute any logic."""

    res = payload.GeneratePayload(self.req, self.result,
                                  self.validate_only_config)
    self.assertEqual(res, controller.RETURN_CODE_VALID_INPUT)

  def testCallSucceeds(self):
    """Check that a call is made successfully."""
    # Deep patch the paygen lib, this is a full run through service as well.
    patch_obj = self.PatchObject(paygen_payload_lib, 'PaygenPayload')
    patch_obj.return_value.Run.return_value = 'gs://something'
    res = payload.GeneratePayload(self.req, self.result, self.api_config)
    self.assertEqual(res, controller.RETURN_CODE_SUCCESS)

  def testMockError(self):
    """Test mock error call does not execute any logic, returns error."""
    patch = self.PatchObject(paygen_payload_lib, 'PaygenPayload')

    res = payload.GeneratePayload(self.req, self.result,
                                  self.mock_error_config)
    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY, res)

  def testMockCall(self):
    """Test mock call does not execute any logic, returns success."""
    patch = self.PatchObject(paygen_payload_lib, 'PaygenPayload')

    res = payload.GeneratePayload(self.req, self.result,
                                  self.mock_call_config)
    patch.assert_not_called()
    self.assertEqual(controller.RETURN_CODE_SUCCESS, res)

  def testMiniOSSuccess(self):
    """Test a miniOS paygen request."""
    patch = self.PatchObject(paygen_payload_lib, 'PaygenPayload')
    patch.return_value.Run.return_value = 'gs://minios/something'
    res = payload.GeneratePayload(self.minios_req, self.result, self.api_config)
    self.assertEqual(res, controller.RETURN_CODE_SUCCESS)

  def testNoMiniOSPartition(self):
    """Test a miniOS paygen request on an image with no miniOS part."""
    patch = self.PatchObject(paygen_payload_lib, 'PaygenPayload')
    patch.side_effect = paygen_payload_lib.NoMiniOSPartitionException
    response_code = payload.GeneratePayload(self.minios_req, self.result,
                                            self.api_config)
    self.assertEqual(self.result.failure_reason,
                     payload_pb2.GenerationResponse.NOT_MINIOS_COMPATIBLE)
    self.assertEqual(response_code,
                     controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE)
