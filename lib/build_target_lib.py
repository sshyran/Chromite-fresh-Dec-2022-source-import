# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Build target class and related functionality."""

import os
import re
from typing import Optional

from chromite.api.gen.chromiumos import common_pb2


class Error(Exception):
  """Base module error class."""


class BuildTarget(object):
  """Class to handle the build target information."""

  def __init__(self,
               name: Optional[str],
               profile: Optional[str] = None,
               build_root: Optional[str] = None):
    """Build Target init.

    Args:
      name: The full name of the target.
      profile: The profile name.
      build_root: The path to the buildroot.
    """
    self._name = name or None
    self.profile = profile

    if build_root:
      self.root = os.path.normpath(build_root)
    else:
      self.root = get_default_sysroot_path(self.name)

  def __eq__(self, other):
    if self.__class__ is other.__class__:
      return (self.name == other.name and self.profile == other.profile and
              self.root == other.root)

    return NotImplemented

  def __hash__(self):
    return hash(self.name)

  def __str__(self):
    return self.name

  @property
  def name(self):
    return self._name

  @property
  def as_protobuf(self):
    return common_pb2.BuildTarget(name=self.name or '')

  @classmethod
  def from_protobuf(cls, message):
    return cls(name=message.name)

  @property
  def profile_protobuf(self):
    return common_pb2.Profile(name=self.profile)

  def full_path(self, *args):
    """Turn a sysroot-relative path into an absolute path."""
    return os.path.join(self.root, *[part.lstrip(os.sep) for part in args])

  def get_command(self, base_command: str) -> str:
    """Get the build target's variant of the given base command.

    We create wrappers for many scripts that handle the build target's
    arguments. Build the target-specific variant for such a command.
    e.g. emerge -> emerge-eve.

    TODO: Add optional validation the command exists.

    Args:
      base_command: The wrapped command.

    Returns:
      The build target's command wrapper.
    """
    if self.is_host():
      return base_command

    return '%s-%s' % (base_command, self.name)

  def is_host(self) -> bool:
    """Check if the build target refers to the host."""
    return not self.name


def get_default_sysroot_path(build_target_name=None):
  """Get the default sysroot location or '/' if |build_target_name| is None."""
  if build_target_name is None:
    return '/'
  return os.path.join('/build', build_target_name)


def get_sdk_sysroot_path() -> str:
  """Get the SDK's sysroot path.

  Convenience/clarification wrapper for get_default_sysroot_path for use when
  explicitly fetching the SDK's sysroot path.
  """
  return get_default_sysroot_path()


def is_valid_name(build_target_name):
  """Validate |build_target_name| is a valid name."""
  return bool(re.match(r'^[a-zA-Z0-9-_]+$', build_target_name))
