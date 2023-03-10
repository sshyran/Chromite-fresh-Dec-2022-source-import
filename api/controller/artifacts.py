# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Implements ArtifactService."""

import logging
import os
from typing import Any, NamedTuple, Optional, TYPE_CHECKING

from chromite.api import controller
from chromite.api import faux
from chromite.api import validate
from chromite.api.controller import controller_util
from chromite.api.controller import image as image_controller
from chromite.api.controller import sysroot as sysroot_controller
from chromite.api.controller import test as test_controller
from chromite.api.gen.chromite.api import artifacts_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import chroot_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import sysroot_lib
from chromite.service import artifacts
from chromite.service import test

if TYPE_CHECKING:
  from chromite.api import api_config

class RegisteredGet(NamedTuple):
  """An registered function for calling Get on an artifact type."""
  output_proto: artifacts_pb2.GetResponse
  artifact_dict: Any


def ExampleGetResponse(_input_proto, _output_proto, _config):
  """Give an example GetResponse with a minimal coverage set."""
  _output_proto = artifacts_pb2.GetResponse(
      artifacts=common_pb2.UploadedArtifactsByService(
          image=image_controller.ExampleGetResponse(),
          sysroot=sysroot_controller.ExampleGetResponse(),
      ))
  return controller.RETURN_CODE_SUCCESS


@faux.empty_error
@faux.success(ExampleGetResponse)
@validate.exists('result_path.path.path')
@validate.validation_complete
def Get(
    input_proto: artifacts_pb2.GetRequest,
    output_proto: artifacts_pb2.GetResponse,
    _config: 'api_config.ApiConfig'):
  """Get all artifacts.

  Get all artifacts for the build.

  Note: As the individual artifact_type bundlers are added here, they *must*
  stop uploading it via the individual bundler function.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  output_dir = input_proto.result_path.path.path

  sysroot = controller_util.ParseSysroot(input_proto.sysroot)
  # This endpoint does not currently support any artifacts that are built
  # without a sysroot being present.
  if not sysroot.path:
    return controller.RETURN_CODE_SUCCESS

  chroot = controller_util.ParseChroot(input_proto.chroot)
  build_target = controller_util.ParseBuildTarget(
      input_proto.sysroot.build_target)

  # A list of RegisteredGet tuples (input proto, output proto, get results).
  get_res_list = [
      RegisteredGet(
          output_proto.artifacts.image,
          image_controller.GetArtifacts(
              input_proto.artifact_info.image, chroot, sysroot, build_target,
              output_dir)),
      RegisteredGet(
          output_proto.artifacts.sysroot,
          sysroot_controller.GetArtifacts(
              input_proto.artifact_info.sysroot, chroot, sysroot, build_target,
              output_dir)),
      RegisteredGet(
          output_proto.artifacts.test,
          test_controller.GetArtifacts(
              input_proto.artifact_info.test, chroot, sysroot, build_target,
              output_dir)),
  ]

  for get_res in get_res_list:
    for artifact_dict in get_res.artifact_dict:
      get_res.output_proto.artifacts.add(
          artifact_type=artifact_dict['type'],
          paths=[
              common_pb2.Path(
                  path=x, location=common_pb2.Path.Location.OUTSIDE)
              for x in artifact_dict['paths']
          ])
  return controller.RETURN_CODE_SUCCESS


def _BuildSetupResponse(_input_proto, output_proto, _config):
  """Just return POINTLESS for now."""
  # All of the artifact types we support claim that the build is POINTLESS.
  output_proto.build_relevance = artifacts_pb2.BuildSetupResponse.POINTLESS


@faux.success(_BuildSetupResponse)
@faux.empty_error
@validate.validation_complete
def BuildSetup(
    _input_proto: artifacts_pb2.GetRequest,
    output_proto: artifacts_pb2.GetResponse,
    _config: 'api_config.ApiConfig'):

  """Setup anything needed for building artifacts

  If any artifact types require steps prior to building the package, they go
  here.  For example, see ToolchainService/PrepareForBuild.

  Note: crbug/1034529 introduces this method as a noop.  As the individual
  artifact_type bundlers are added here, they *must* stop uploading it via the
  individual bundler function.

  Args:
    _input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  # If any artifact_type says "NEEDED", the return is NEEDED.
  # Otherwise, if any artifact_type says "UNKNOWN", the return is UNKNOWN.
  # Otherwise, the return is POINTLESS.
  output_proto.build_relevance = artifacts_pb2.BuildSetupResponse.POINTLESS
  return controller.RETURN_CODE_SUCCESS


def _GetImageDir(build_root: str, target: str) -> Optional[str]:
  """Return path containing images for the given build target.

  TODO(saklein) Expand image_lib.GetLatestImageLink to support this use case.

  Args:
    build_root: Path to checkout where build occurs.
    target: Name of the build target.

  Returns:
    Path to the latest directory containing target images or None.
  """
  image_dir = os.path.join(build_root, 'src/build/images', target, 'latest')
  if not os.path.exists(image_dir):
    logging.warning('Expected to find image output for target %s at %s, but '
                    'path does not exist', target, image_dir)
    return None

  return image_dir


def _BundleImageArchivesResponse(input_proto, output_proto, _config):
  """Add artifact paths to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'path0.tar.xz')
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'path1.tar.xz')


@faux.success(_BundleImageArchivesResponse)
@faux.empty_error
@validate.require('build_target.name')
@validate.exists('output_dir')
@validate.validation_complete
def BundleImageArchives(input_proto, output_proto, _config):
  """Create a .tar.xz archive for each image that has been created."""
  build_target = controller_util.ParseBuildTarget(input_proto.build_target)
  output_dir = input_proto.output_dir
  image_dir = _GetImageDir(constants.SOURCE_ROOT, build_target.name)
  if image_dir is None:
    return

  archives = artifacts.ArchiveImages(image_dir, output_dir)

  for archive in archives:
    output_proto.artifacts.add().path = os.path.join(output_dir, archive)


def _BundleImageZipResponse(input_proto, output_proto, _config):
  """Add artifact zip files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'image.zip')


@faux.success(_BundleImageZipResponse)
@faux.empty_error
@validate.require('build_target.name', 'output_dir')
@validate.exists('output_dir')
@validate.validation_complete
def BundleImageZip(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Bundle image.zip.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  target = input_proto.build_target.name
  output_dir = input_proto.output_dir
  image_dir = _GetImageDir(constants.SOURCE_ROOT, target)
  if image_dir is None:
    return None

  archive = artifacts.BundleImageZip(output_dir, image_dir)
  output_proto.artifacts.add().path = os.path.join(output_dir, archive)


def _BundleTestUpdatePayloadsResponse(input_proto, output_proto, _config):
  """Add test payload files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'payload1.bin')


@faux.success(_BundleTestUpdatePayloadsResponse)
@faux.empty_error
@validate.require('build_target.name', 'output_dir')
@validate.exists('output_dir')
@validate.validation_complete
def BundleTestUpdatePayloads(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Generate minimal update payloads for the build target for testing.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  target = input_proto.build_target.name
  output_dir = input_proto.output_dir
  build_root = constants.SOURCE_ROOT

  # Use the first available image to create the update payload.
  img_dir = _GetImageDir(build_root, target)
  if img_dir is None:
    return None

  img_types = [constants.IMAGE_TYPE_TEST, constants.IMAGE_TYPE_DEV,
               constants.IMAGE_TYPE_BASE]
  img_names = [constants.IMAGE_TYPE_TO_NAME[t] for t in img_types]
  img_paths = [os.path.join(img_dir, x) for x in img_names]
  valid_images = [x for x in img_paths if os.path.exists(x)]

  if not valid_images:
    cros_build_lib.Die(
        'Expected to find an image of type among %r for target "%s" '
        'at path %s.', img_types, target, img_dir)
  image = valid_images[0]

  payloads = artifacts.BundleTestUpdatePayloads(image, output_dir)
  for payload in payloads:
    output_proto.artifacts.add().path = payload


def _BundleAutotestFilesResponse(input_proto, output_proto, _config):
  """Add test autotest files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'autotest-a.tar.gz')


@faux.success(_BundleAutotestFilesResponse)
@faux.empty_error
@validate.require('output_dir')
@validate.exists('output_dir')
def BundleAutotestFiles(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    config: 'api_config.ApiConfig'):
  """Tar the autotest files for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    config: The API call config.
  """
  output_dir = input_proto.output_dir
  target = input_proto.build_target.name
  chroot = controller_util.ParseChroot(input_proto.chroot)

  if target:
    sysroot_path = os.path.join('/build', target)
  else:
    # New style call, use chroot and sysroot.
    sysroot_path = input_proto.sysroot.path
    if not sysroot_path:
      cros_build_lib.Die('sysroot.path is required.')

  sysroot = sysroot_lib.Sysroot(sysroot_path)

  # TODO(saklein): Switch to the validate_only decorator when legacy handling
  #   is removed.
  if config.validate_only:
    return controller.RETURN_CODE_VALID_INPUT

  if not sysroot.Exists(chroot=chroot):
    cros_build_lib.Die('Sysroot path must exist: %s', sysroot.path)

  try:
    # Note that this returns the full path to *multiple* tarballs.
    archives = artifacts.BundleAutotestFiles(chroot, sysroot, output_dir)
  except artifacts.Error as e:
    logging.warning(e)
    return

  for archive in archives.values():
    output_proto.artifacts.add().path = archive


def _BundleTastFilesResponse(input_proto, output_proto, _config):
  """Add test tast files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   'tast_bundles.tar.gz')


@faux.success(_BundleTastFilesResponse)
@faux.empty_error
@validate.require('output_dir')
@validate.exists('output_dir')
def BundleTastFiles(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    config: 'api_config.ApiConfig'):
  """Tar the tast files for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    config: The API call config.
  """
  target = input_proto.build_target.name
  output_dir = input_proto.output_dir
  build_root = constants.SOURCE_ROOT

  chroot = controller_util.ParseChroot(input_proto.chroot)
  sysroot_path = input_proto.sysroot.path

  # TODO(saklein) Cleanup legacy handling after it has been switched over.
  if target:
    # Legacy handling.
    chroot = chroot_lib.Chroot(path=os.path.join(build_root, 'chroot'))
    sysroot_path = os.path.join('/build', target)

  # New handling - chroot & sysroot based.
  # TODO(saklein) Switch this to the require decorator when legacy is removed.
  if not sysroot_path:
    cros_build_lib.Die('sysroot.path is required.')

  # TODO(saklein): Switch to the validation_complete decorator when legacy
  #   handling is removed.
  if config.validate_only:
    return controller.RETURN_CODE_VALID_INPUT

  sysroot = sysroot_lib.Sysroot(sysroot_path)
  if not sysroot.Exists(chroot=chroot):
    cros_build_lib.Die('Sysroot must exist.')

  archive = artifacts.BundleTastFiles(chroot, sysroot, output_dir)

  if archive:
    output_proto.artifacts.add().path = archive
  else:
    logging.warning('Found no tast files for %s.', target)


def BundlePinnedGuestImages(_input_proto, _output_proto, _config):
  # TODO(crbug/1034529): Remove this endpoint
  pass

def FetchPinnedGuestImageUris(_input_proto, _output_proto, _config):
  # TODO(crbug/1034529): Remove this endpoint
  pass


def _FetchMetadataResponse(_input_proto, output_proto, _config):
  """Populate the output_proto with sample data."""
  for fp in ('/metadata/foo.txt', '/metadata/bar.jsonproto'):
    output_proto.filepaths.add(path=common_pb2.Path(
        path=fp, location=common_pb2.Path.OUTSIDE))
  return controller.RETURN_CODE_SUCCESS


@faux.success(_FetchMetadataResponse)
@faux.empty_error
@validate.exists('chroot.path')
@validate.require('sysroot.path')
@validate.validation_complete
def FetchMetadata(
    input_proto: artifacts_pb2.FetchMetadataRequest,
    output_proto: artifacts_pb2.FetchMetadataResponse,
    _config: 'api_config.ApiConfig'):
  """FetchMetadata returns the paths to all build/test metadata files.

  This implements ArtifactsService.FetchMetadata.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    config: The API call config.
  """
  chroot = controller_util.ParseChroot(input_proto.chroot)
  sysroot = controller_util.ParseSysroot(input_proto.sysroot)
  for path in test.FindAllMetadataFiles(chroot, sysroot):
    output_proto.filepaths.add(
        path=common_pb2.Path(path=path, location=common_pb2.Path.OUTSIDE))
  return controller.RETURN_CODE_SUCCESS


def _BundleFirmwareResponse(input_proto, output_proto, _config):
  """Add test firmware image files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'firmware.tar.gz')


@faux.success(_BundleFirmwareResponse)
@faux.empty_error
@validate.require('output_dir', 'sysroot.path')
@validate.exists('output_dir')
@validate.validation_complete
def BundleFirmware(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Tar the firmware images for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  output_dir = input_proto.output_dir
  chroot = controller_util.ParseChroot(input_proto.chroot)
  sysroot_path = input_proto.sysroot.path
  sysroot = sysroot_lib.Sysroot(sysroot_path)

  if not chroot.exists():
    cros_build_lib.Die('Chroot does not exist: %s', chroot.path)
  elif not sysroot.Exists(chroot=chroot):
    cros_build_lib.Die('Sysroot does not exist: %s',
                       chroot.full_path(sysroot.path))

  archive = artifacts.BuildFirmwareArchive(chroot, sysroot, output_dir)

  if archive is None:
    logging.warning(
        'Could not create firmware archive. No firmware found for %s.',
        sysroot_path)
    return

  output_proto.artifacts.add().path = archive


def _BundleFpmcuUnittestsResponse(input_proto, output_proto, _config):
  """Add fingerprint MCU unittest binaries to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'fpmcu_unittests.tar.gz')


@faux.success(_BundleFpmcuUnittestsResponse)
@faux.empty_error
@validate.require('output_dir', 'sysroot.path')
@validate.exists('output_dir')
@validate.validation_complete
def BundleFpmcuUnittests(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Tar the fingerprint MCU unittest binaries for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  output_dir = input_proto.output_dir
  chroot = controller_util.ParseChroot(input_proto.chroot)
  sysroot_path = input_proto.sysroot.path
  sysroot = sysroot_lib.Sysroot(sysroot_path)

  if not chroot.exists():
    cros_build_lib.Die('Chroot does not exist: %s', chroot.path)
  elif not sysroot.Exists(chroot=chroot):
    cros_build_lib.Die('Sysroot does not exist: %s',
                       chroot.full_path(sysroot.path))

  archive = artifacts.BundleFpmcuUnittests(chroot, sysroot, output_dir)

  if archive is None:
    logging.warning(
        'No fpmcu unittests found for %s.', sysroot_path)
    return

  output_proto.artifacts.add().path = archive


def _BundleEbuildLogsResponse(input_proto, output_proto, _config):
  """Add test log files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'ebuild-logs.tar.gz')


@faux.success(_BundleEbuildLogsResponse)
@faux.empty_error
@validate.exists('output_dir')
def BundleEbuildLogs(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    config: 'api_config.ApiConfig'):
  """Tar the ebuild logs for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    config: The API call config.
  """
  output_dir = input_proto.output_dir
  sysroot_path = input_proto.sysroot.path
  chroot = controller_util.ParseChroot(input_proto.chroot)

  # TODO(mmortensen) Cleanup legacy handling after it has been switched over.
  target = input_proto.build_target.name
  if target:
    # Legacy handling.
    build_root = constants.SOURCE_ROOT
    chroot = chroot_lib.Chroot(path=os.path.join(build_root, 'chroot'))
    sysroot_path = os.path.join('/build', target)

  # TODO(saklein): Switch to validation_complete decorator after legacy
  #   handling has been cleaned up.
  if config.validate_only:
    return controller.RETURN_CODE_VALID_INPUT

  sysroot = sysroot_lib.Sysroot(sysroot_path)
  archive = artifacts.BundleEBuildLogsTarball(chroot, sysroot, output_dir)
  if archive is None:
    cros_build_lib.Die(
        'Could not create ebuild logs archive. No logs found for %s.',
        sysroot.path)
  output_proto.artifacts.add().path = os.path.join(output_dir, archive)


def _BundleChromeOSConfigResponse(input_proto, output_proto, _config):
  """Add test config files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'config.yaml')


@faux.success(_BundleChromeOSConfigResponse)
@faux.empty_error
@validate.exists('output_dir')
@validate.validation_complete
def BundleChromeOSConfig(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Output the ChromeOS Config payload for a build target.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  output_dir = input_proto.output_dir
  sysroot_path = input_proto.sysroot.path
  chroot = controller_util.ParseChroot(input_proto.chroot)

  # TODO(mmortensen) Cleanup legacy handling after it has been switched over.
  target = input_proto.build_target.name
  if target:
    # Legacy handling.
    build_root = constants.SOURCE_ROOT
    chroot = chroot_lib.Chroot(path=os.path.join(build_root, 'chroot'))
    sysroot_path = os.path.join('/build', target)

  sysroot = sysroot_lib.Sysroot(sysroot_path)
  chromeos_config = artifacts.BundleChromeOSConfig(chroot, sysroot, output_dir)
  if not chromeos_config:
    return

  output_proto.artifacts.add().path = os.path.join(output_dir, chromeos_config)


def _BundleSimpleChromeArtifactsResponse(input_proto, output_proto, _config):
  """Add test simple chrome files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'simple_chrome.txt')


@faux.success(_BundleSimpleChromeArtifactsResponse)
@faux.empty_error
@validate.require('output_dir', 'sysroot.build_target.name', 'sysroot.path')
@validate.exists('output_dir')
@validate.validation_complete
def BundleSimpleChromeArtifacts(input_proto, output_proto, _config):
  """Create the simple chrome artifacts."""
  sysroot_path = input_proto.sysroot.path
  output_dir = input_proto.output_dir

  # Build out the argument instances.
  build_target = controller_util.ParseBuildTarget(
      input_proto.sysroot.build_target)
  chroot = controller_util.ParseChroot(input_proto.chroot)
  # Sysroot.path needs to be the fully qualified path, including the chroot.
  full_sysroot_path = os.path.join(chroot.path, sysroot_path.lstrip(os.sep))
  sysroot = sysroot_lib.Sysroot(full_sysroot_path)

  # Quick sanity check that the sysroot exists before we go on.
  if not sysroot.Exists():
    cros_build_lib.Die('The sysroot does not exist.')

  try:
    results = artifacts.BundleSimpleChromeArtifacts(chroot, sysroot,
                                                    build_target, output_dir)
  except artifacts.Error as e:
    cros_build_lib.Die('Error %s raised in BundleSimpleChromeArtifacts: %s',
                       type(e), e)

  for file_name in results:
    output_proto.artifacts.add().path = file_name


def _BundleVmFilesResponse(input_proto, output_proto, _config):
  """Add test vm files to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'f1.tar')


@faux.success(_BundleVmFilesResponse)
@faux.empty_error
@validate.require('chroot.path', 'test_results_dir', 'output_dir')
@validate.exists('output_dir')
@validate.validation_complete
def BundleVmFiles(
    input_proto: artifacts_pb2.BundleVmFilesRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Tar VM disk and memory files.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  chroot = controller_util.ParseChroot(input_proto.chroot)
  test_results_dir = input_proto.test_results_dir
  output_dir = input_proto.output_dir

  archives = artifacts.BundleVmFiles(
      chroot, test_results_dir, output_dir)
  for archive in archives:
    output_proto.artifacts.add().path = archive

def _ExportCpeReportResponse(input_proto, output_proto, _config):
  """Add test cpe results to a successful response."""
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'cpe_report.txt')
  output_proto.artifacts.add().path = os.path.join(
      input_proto.output_dir, 'cpe_warnings.txt')


@faux.success(_ExportCpeReportResponse)
@faux.empty_error
@validate.exists('output_dir')
def ExportCpeReport(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    config: 'api_config.ApiConfig'):
  """Export a CPE report.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    config: The API call config.
  """
  chroot = controller_util.ParseChroot(input_proto.chroot)
  output_dir = input_proto.output_dir

  if input_proto.build_target.name:
    # Legacy handling - use the default sysroot path for the build target.
    build_target = controller_util.ParseBuildTarget(input_proto.build_target)
    sysroot = sysroot_lib.Sysroot(build_target.root)
  elif input_proto.sysroot.path:
    sysroot = sysroot_lib.Sysroot(input_proto.sysroot.path)
  else:
    # TODO(saklein): Switch to validate decorators once legacy handling can be
    #   cleaned up.
    cros_build_lib.Die('sysroot.path is required.')

  if config.validate_only:
    return controller.RETURN_CODE_VALID_INPUT

  cpe_result = artifacts.GenerateCpeReport(chroot, sysroot, output_dir)

  output_proto.artifacts.add().path = cpe_result.report
  output_proto.artifacts.add().path = cpe_result.warnings


def _BundleGceTarballResponse(input_proto, output_proto, _config):
  """Add artifact tarball to a successful response."""
  output_proto.artifacts.add().path = os.path.join(input_proto.output_dir,
                                                   constants.TEST_IMAGE_GCE_TAR)


@faux.success(_BundleGceTarballResponse)
@faux.empty_error
@validate.require('build_target.name', 'output_dir')
@validate.exists('output_dir')
@validate.validation_complete
def BundleGceTarball(
    input_proto: artifacts_pb2.BundleRequest,
    output_proto: artifacts_pb2.BundleResponse,
    _config: 'api_config.ApiConfig'):
  """Bundle the test image into a tarball suitable for importing into GCE.

  Args:
    input_proto: The input proto.
    output_proto: The output proto.
    _config: The API call config.
  """
  target = input_proto.build_target.name
  output_dir = input_proto.output_dir
  image_dir = _GetImageDir(constants.SOURCE_ROOT, target)
  if image_dir is None:
    return None

  tarball = artifacts.BundleGceTarball(output_dir, image_dir)
  output_proto.artifacts.add().path = tarball
