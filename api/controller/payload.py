# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Payload API Service."""

from typing import TYPE_CHECKING

from chromite.api import controller
from chromite.api import faux
from chromite.api import validate
from chromite.api.gen.chromite.api import payload_pb2
from chromite.lib import cros_build_lib
from chromite.lib.paygen import paygen_payload_lib
from chromite.service import payload


if TYPE_CHECKING:
  from chromite.api import api_config

_VALID_IMAGE_PAIRS = (('src_signed_image', 'tgt_signed_image'),
                      ('src_unsigned_image', 'tgt_unsigned_image'),
                      ('src_dlc_image', 'tgt_dlc_image'),
                      ('full_update', 'tgt_unsigned_image'),
                      ('full_update', 'tgt_signed_image'),
                      ('full_update', 'tgt_dlc_image'))
_VALID_MINIOS_PAIRS = (('src_signed_image', 'tgt_signed_image'),
                       ('src_unsigned_image', 'tgt_unsigned_image'),
                       ('full_update', 'tgt_unsigned_image'),
                       ('full_update', 'tgt_signed_image'))

_DEFAULT_PAYGEN_CACHE_DIR = '.paygen_cache'

# We have more fields we might validate however, they're either
# 'oneof' or allowed to be the empty value by design. If @validate
# gets more complex in the future we can add more here.
@faux.empty_success
@faux.empty_completed_unsuccessfully_error
@validate.require('bucket')
def GeneratePayload(input_proto: payload_pb2.GenerationRequest,
                    output_proto: payload_pb2.GenerationResponse,
                    config: 'api_config.ApiConfig') -> int:
  """Generate a update payload ('do paygen').

  Args:
    input_proto: Input proto.
    output_proto: Output proto.
    config: The API call config.

  Returns:
    A controller return code (e.g. controller.RETURN_CODE_SUCCESS).
  """

  # Resolve the tgt image oneof.
  tgt_name = input_proto.WhichOneof('tgt_image_oneof')
  try:
    tgt_image = getattr(input_proto, tgt_name)
  except AttributeError:
    cros_build_lib.Die('%s is not a known tgt image type' % (tgt_name,))

  # Resolve the src image oneof.
  src_name = input_proto.WhichOneof('src_image_oneof')

  # If the source image is 'full_update' we lack a source entirely.
  if src_name == 'full_update':
    src_image = None
  # Otherwise we have an image.
  else:
    try:
      src_image = getattr(input_proto, src_name)
    except AttributeError:
      cros_build_lib.Die('%s is not a known src image type' % (src_name,))

  # Ensure they are compatible oneofs.
  if (src_name, tgt_name) not in _VALID_IMAGE_PAIRS:
    cros_build_lib.Die('%s and %s are not valid image pairs' %
                       (src_image, tgt_image))

  # Ensure that miniOS payloads are only requested for compatible image types.
  if input_proto.minios and (src_name, tgt_name) not in _VALID_MINIOS_PAIRS:
    cros_build_lib.Die('%s and %s are not valid image pairs for miniOS' %
                       (src_image, tgt_image))

  # Find the value of bucket or default to 'chromeos-releases'.
  destination_bucket = input_proto.bucket or 'chromeos-releases'

  # There's a potential that some paygen_lib library might raise here, but since
  # we're still involved in config we'll keep it before the validate_only.
  payload_config = payload.PayloadConfig(tgt_image, src_image,
                                         destination_bucket, input_proto.minios,
                                         input_proto.verify,
                                         upload=not input_proto.dryrun,
                                         cache_dir=_DEFAULT_PAYGEN_CACHE_DIR)

  # If configured for validation only we're done here.
  if config.validate_only:
    return controller.RETURN_CODE_VALID_INPUT

  # Do payload generation.
  local_path, remote_uri = '', ''
  try:
    local_path, remote_uri = payload_config.GeneratePayload()
  except paygen_payload_lib.PayloadGenerationSkippedException as e:
    # If paygen was skipped, provide a reason if possible.
    if isinstance(e, paygen_payload_lib.NoMiniOSPartitionException):
      reason = payload_pb2.GenerationResponse.NOT_MINIOS_COMPATIBLE
      output_proto.failure_reason = reason

  _SetGeneratePayloadOutputProto(output_proto, local_path, remote_uri)
  if remote_uri or input_proto.dryrun and local_path:
    return controller.RETURN_CODE_SUCCESS
  elif output_proto.failure_reason:
    return controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE
  else:
    return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY


def _SetGeneratePayloadOutputProto(output_proto: payload_pb2.GenerationResponse,
                                   local_path: str,
                                   remote_uri: str):
  """Set the output proto with the results from the service class.

  Args:
    output_proto: The output proto.
    local_path: set output_proto with the local path, or ''.
    remote_uri: set output_proto with the remote uri, or ''.
  """
  output_proto.success = True
  output_proto.local_path = local_path or ''
  output_proto.remote_uri = remote_uri or ''
