# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Package related functionality."""

from __future__ import print_function

from chromite.api import faux
from chromite.api import validate
from chromite.api.controller import controller_util
from chromite.api.gen.chromite.api import binhost_pb2
from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import build_target_util
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib.uprev_lib import GitRef
from chromite.service import packages


_OVERLAY_TYPE_TO_NAME = {
    binhost_pb2.OVERLAYTYPE_PUBLIC: constants.PUBLIC_OVERLAYS,
    binhost_pb2.OVERLAYTYPE_PRIVATE: constants.PRIVATE_OVERLAYS,
    binhost_pb2.OVERLAYTYPE_BOTH: constants.BOTH_OVERLAYS,
}


@faux.all_empty
@validate.require('overlay_type')
@validate.is_in('overlay_type', _OVERLAY_TYPE_TO_NAME)
@validate.validation_complete
def Uprev(input_proto, output_proto, _config):
  """Uprev all cros workon ebuilds that have changes."""
  target_names = [t.name for t in input_proto.build_targets]
  build_targets = [build_target_util.BuildTarget(t) for t in target_names]
  overlay_type = _OVERLAY_TYPE_TO_NAME[input_proto.overlay_type]
  chroot = controller_util.ParseChroot(input_proto.chroot)
  output_dir = input_proto.output_dir or None

  try:
    uprevved = packages.uprev_build_targets(build_targets, overlay_type, chroot,
                                            output_dir)
  except packages.Error as e:
    # Handle module errors nicely, let everything else bubble up.
    cros_build_lib.Die(e)

  for path in uprevved:
    output_proto.modified_ebuilds.add().path = path


@faux.all_empty
@validate.require('versions')
@validate.require('package_info.package_name', 'package_info.category')
@validate.validation_complete
def UprevVersionedPackage(input_proto, output_proto, _config):
  """Uprev a versioned package.

  See go/pupr-generator for details about this endpoint.
  """
  chroot = controller_util.ParseChroot(input_proto.chroot)
  build_targets = controller_util.ParseBuildTargets(input_proto.build_targets)
  package = controller_util.PackageInfoToCPV(input_proto.package_info)
  refs = []
  for ref in input_proto.versions:
    refs.append(GitRef(path=ref.repository, ref=ref.ref, revision=ref.revision))

  try:
    result = packages.uprev_versioned_package(package, build_targets, refs,
                                              chroot)
  except packages.Error as e:
    # Handle module errors nicely, let everything else bubble up.
    cros_build_lib.Die(e)

  if not result.uprevved:
    # No uprevs executed, skip the output population.
    return

  for modified in result.modified:
    uprev_response = output_proto.responses.add()
    uprev_response.version = modified.new_version
    for path in modified.files:
      uprev_response.modified_ebuilds.add().path = path



@faux.all_empty
@validate.require('atom')
@validate.validation_complete
def GetBestVisible(input_proto, output_proto, _config):
  """Returns the best visible PackageInfo for the indicated atom."""
  build_target = None
  if input_proto.build_target.name:
    build_target = controller_util.ParseBuildTarget(input_proto.build_target)

  cpv = packages.get_best_visible(input_proto.atom, build_target=build_target)
  package_info = common_pb2.PackageInfo()
  controller_util.CPVToPackageInfo(cpv, package_info)
  output_proto.package_info.CopyFrom(package_info)


@faux.all_empty
@validate.require('build_target.name')
@validate.validation_complete
def GetChromeVersion(input_proto, output_proto, _config):
  """Returns the chrome version."""
  build_target = controller_util.ParseBuildTarget(input_proto.build_target)
  cpv = packages.get_best_visible(
      constants.CHROME_CP, build_target=build_target)

  # Something like 1.2.3.4_rc -> 1.2.3.4.
  output_proto.version = cpv.version_no_rev.split('_')[0]


def _HasChromePrebuiltSuccess(_input_proto, output_proto, _config):
  """The mock success case for HasChromePrebuilt."""
  output_proto.has_prebuilt = True


@faux.success(_HasChromePrebuiltSuccess)
@faux.empty_error
@validate.require('build_target.name')
@validate.validation_complete
def HasChromePrebuilt(input_proto, output_proto, _config):
  """Checks if the most recent version of Chrome has a prebuilt."""
  build_target = controller_util.ParseBuildTarget(input_proto.build_target)
  exists = packages.has_prebuilt(constants.CHROME_CP, build_target=build_target)

  output_proto.has_prebuilt = exists


def _BuildsChromeSuccess(_input_proto, output_proto, _config):
  """Mock success case for BuildsChrome."""
  output_proto.builds_chrome = True


@faux.success(_BuildsChromeSuccess)
@faux.empty_error
@validate.require('build_target.name')
@validate.validation_complete
def BuildsChrome(input_proto, output_proto, _config):
  """Check if the board builds chrome."""
  build_target = controller_util.ParseBuildTarget(input_proto.build_target)
  builds_chrome = packages.builds(constants.CHROME_CP, build_target)
  output_proto.builds_chrome = builds_chrome
