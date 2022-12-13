# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""SDK tests."""

from unittest import mock

from chromite.api import api_config
from chromite.api.controller import sdk as sdk_controller
from chromite.api.gen.chromite.api import sdk_pb2
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.service import sdk as sdk_service


class SdkCreateTest(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Create tests."""

  def setUp(self):
    """Setup method."""
    # We need to run the command outside the chroot.
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=False)
    self.response = sdk_pb2.CreateResponse()

  def _GetRequest(self, no_replace=False, bootstrap=False, no_use_image=False,
                  cache_path=None, chroot_path=None, sdk_version=None,
                  skip_chroot_upgrade=False):
    """Helper to build a create request message."""
    request = sdk_pb2.CreateRequest()
    request.flags.no_replace = no_replace
    request.flags.bootstrap = bootstrap
    request.flags.no_use_image = no_use_image

    if cache_path:
      request.chroot.cache_dir = cache_path
    if chroot_path:
      request.chroot.path = chroot_path
    if sdk_version:
      request.sdk_version = sdk_version
    if skip_chroot_upgrade:
      request.skip_chroot_upgrade = skip_chroot_upgrade

    return request

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Create')

    sdk_controller.Create(self._GetRequest(), self.response,
                          self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Create')

    rc = sdk_controller.Create(self._GetRequest(), self.response,
                               self.mock_call_config)
    patch.assert_not_called()
    self.assertFalse(rc)
    self.assertTrue(self.response.version.version)

  def testSuccess(self):
    """Test the successful call output handling."""
    self.PatchObject(sdk_service, 'Create', return_value=1)

    request = self._GetRequest()

    sdk_controller.Create(request, self.response, self.api_config)

    self.assertEqual(1, self.response.version.version)

  def testFalseArguments(self):
    """Test False argument handling."""
    # Create the patches.
    self.PatchObject(sdk_service, 'Create', return_value=1)
    args_patch = self.PatchObject(sdk_service, 'CreateArguments')

    # Flag translation tests.
    # Test all false values in the message.
    request = self._GetRequest(no_replace=False, bootstrap=False,
                               no_use_image=False)
    sdk_controller.Create(request, self.response, self.api_config)
    args_patch.assert_called_with(
        replace=True,
        bootstrap=False,
        use_image=True,
        chroot_path=mock.ANY,
        cache_dir=mock.ANY,
        sdk_version=mock.ANY,
        skip_chroot_upgrade=mock.ANY)

  def testTrueArguments(self):
    """Test True arguments handling."""
    # Create the patches.
    self.PatchObject(sdk_service, 'Create', return_value=1)
    args_patch = self.PatchObject(sdk_service, 'CreateArguments')

    # Test all True values in the message.
    request = self._GetRequest(no_replace=True, bootstrap=True,
                               no_use_image=True, sdk_version='foo',
                               skip_chroot_upgrade=True)
    sdk_controller.Create(request, self.response, self.api_config)
    args_patch.assert_called_with(
        replace=False,
        bootstrap=True,
        use_image=False,
        chroot_path=mock.ANY,
        cache_dir=mock.ANY,
        sdk_version='foo',
        skip_chroot_upgrade=True)


class SdkDeleteTest(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Create tests."""

  def setUp(self):
    """Setup method."""
    # We need to run the command outside the chroot.
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=False)
    self.response = sdk_pb2.DeleteResponse()

  def _GetRequest(self, chroot_path=None):
    """Helper to build a delete request message."""
    request = sdk_pb2.DeleteRequest()
    if chroot_path:
      request.chroot.path = chroot_path

    return request

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Delete')

    sdk_controller.Delete(self._GetRequest(), self.response,
                          self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Delete')

    rc = sdk_controller.Delete(self._GetRequest(), self.response,
                               self.mock_call_config)
    patch.assert_not_called()
    self.assertFalse(rc)

  def testSuccess(self):
    """Test the successful call by verifying service invocation."""
    patch = self.PatchObject(sdk_service, 'Delete', return_value=1)

    request = self._GetRequest()

    sdk_controller.Delete(request, self.response, self.api_config)
    # Verify that by default sdk_service.Delete is called with force=True.
    patch.assert_called_once_with(mock.ANY, force=True)


class SdkUnmountPathTest(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Update tests."""

  def setUp(self):
    """Setup method."""
    self.response = sdk_pb2.UnmountPathResponse()

  def _UnmountPathRequest(self, path=None):
    """Helper to build a delete request message."""
    request = sdk_pb2.UnmountPathRequest()
    if path:
      request.path.path = path
    return request

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'UnmountPath')

    sdk_controller.UnmountPath(self._UnmountPathRequest('/test/path'),
                               self.response, self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'UnmountPath')

    rc = sdk_controller.UnmountPath(self._UnmountPathRequest(), self.response,
                                    self.mock_call_config)
    patch.assert_not_called()
    self.assertFalse(rc)

  def testSuccess(self):
    """Test the successful call by verifying service invocation."""
    patch = self.PatchObject(sdk_service, 'UnmountPath', return_value=1)

    request = self._UnmountPathRequest('/test/path')
    sdk_controller.UnmountPath(request, self.response, self.api_config)
    patch.assert_called_once_with('/test/path')


class SdkUpdateTest(cros_test_lib.MockTestCase, api_config.ApiConfigMixin):
  """Update tests."""

  def setUp(self):
    """Setup method."""
    # We need to run the command inside the chroot.
    self.PatchObject(cros_build_lib, 'IsInsideChroot', return_value=True)

    self.response = sdk_pb2.UpdateResponse()

  def _GetRequest(self, build_source=False, targets=None):
    """Helper to simplify building a request instance."""
    request = sdk_pb2.UpdateRequest()
    request.flags.build_source = build_source

    for target in targets or []:
      added = request.toolchain_targets.add()
      added.name = target

    return request

  def testValidateOnly(self):
    """Sanity check that a validate only call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Update')

    sdk_controller.Update(self._GetRequest(), self.response,
                          self.validate_only_config)
    patch.assert_not_called()

  def testMockCall(self):
    """Sanity check that a mock call does not execute any logic."""
    patch = self.PatchObject(sdk_service, 'Update')

    rc = sdk_controller.Create(self._GetRequest(), self.response,
                               self.mock_call_config)
    patch.assert_not_called()
    self.assertFalse(rc)
    self.assertTrue(self.response.version.version)

  def testSuccess(self):
    """Successful call output handling test."""
    expected_version = 1
    self.PatchObject(sdk_service, 'Update', return_value=expected_version)
    request = self._GetRequest()

    sdk_controller.Update(request, self.response, self.api_config)

    self.assertEqual(expected_version, self.response.version.version)

  def testArgumentHandling(self):
    """Test the proto argument handling."""
    args = sdk_service.UpdateArguments()
    self.PatchObject(sdk_service, 'Update', return_value=1)
    args_patch = self.PatchObject(sdk_service, 'UpdateArguments',
                                  return_value=args)

    # No boards and flags False.
    request = self._GetRequest(build_source=False)
    sdk_controller.Update(request, self.response, self.api_config)
    args_patch.assert_called_with(
        build_source=False, toolchain_targets=[], toolchain_changed=False)

    # Multiple boards and flags True.
    targets = ['board1', 'board2']
    request = self._GetRequest(build_source=True, targets=targets)
    sdk_controller.Update(request, self.response, self.api_config)
    args_patch.assert_called_with(
        build_source=True, toolchain_targets=targets, toolchain_changed=False)
