# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Utilities to create sysroots."""

import glob
import multiprocessing
import os
from typing import Iterable, Union

from chromite.api.gen.chromiumos import common_pb2
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import locking
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import toolchain
from chromite.lib.parser import package_info


class ConfigurationError(Exception):
  """Raised when an invalid configuration is found."""


STANDARD_FIELD_PORTDIR_OVERLAY = 'PORTDIR_OVERLAY'
STANDARD_FIELD_CHOST = 'CHOST'
STANDARD_FIELD_BOARD_OVERLAY = 'BOARD_OVERLAY'
STANDARD_FIELD_BOARD_USE = 'BOARD_USE'
STANDARD_FIELD_ARCH = 'ARCH'

_PORTAGE_WRAPPER_TEMPLATE = """#!/bin/sh

# If we try to use sudo when the sandbox is active, we get ugly warnings that
# just confuse developers.  Disable the sandbox in this case by rexecing.
if [ "${{SANDBOX_ON}}" = "1" ]; then
  SANDBOX_ON=0 exec "$0" "$@"
else
  unset LD_PRELOAD
fi

export CHOST="{chost}"
export PORTAGE_CONFIGROOT="{sysroot}"
export SYSROOT="{sysroot}"
if [ -z "$PORTAGE_USERNAME" ]; then
  export PORTAGE_USERNAME=$(basename "${{HOME}}")
fi
export ROOT="{sysroot}"
exec sudo -E {command} "$@"
"""

_BOARD_WRAPPER_TEMPLATE = """#!/bin/sh
exec {command} --board="{board}" "$@"
"""

_BOARD_WRAPPER_DEPRECATED_CMD_TEMPLATE = """#!/bin/sh
echo "{deprecated}"
exec {command} --board="{board}" "$@"
"""

_BUILD_TARGET_WRAPPER_TEMPLATE = """#!/bin/sh
exec {command} --build-target="{build_target}" "$@"
"""

_PKGCONFIG_WRAPPER_TEMPLATE = """#!/bin/bash

PKG_CONFIG_LIBDIR=$(printf '%s:' "{sysroot}"/usr/*/pkgconfig)
export PKG_CONFIG_LIBDIR

export PKG_CONFIG_SYSROOT_DIR="{sysroot}"

# Portage will get confused and try to "help" us by exporting this.
# Undo that logic.
unset PKG_CONFIG_PATH

# Use full path to bypass automated wrapper checks that block `pkg-config`.
# https://crbug.com/985180
exec /usr/bin/pkg-config "$@"
"""

_wrapper_dir = '/usr/local/bin'

_IMPLICIT_SYSROOT_DEPS_KEY = 'IMPLICIT_SYSROOT_DEPS'
_IMPLICIT_SYSROOT_DEPS = ['sys-kernel/linux-headers', 'sys-libs/gcc-libs',
                          'sys-libs/libcxxabi', 'sys-libs/libcxx']

_MAKE_CONF = 'etc/make.conf'
_MAKE_CONF_BOARD_SETUP = 'etc/make.conf.board_setup'
_MAKE_CONF_BOARD = 'etc/make.conf.board'
_MAKE_CONF_USER = 'etc/make.conf.user'
_MAKE_CONF_HOST_SETUP = 'etc/make.conf.host_setup'

_CONFIGURATION_PATH = _MAKE_CONF_BOARD_SETUP

_CACHE_PATH = 'var/cache/edb/chromeos'

_CHROMIUMOS_OVERLAY = '/usr/local/portage/chromiumos'
_CHROMIUMOS_CONFIG = os.path.join(_CHROMIUMOS_OVERLAY, 'chromeos', 'config')
_ECLASS_OVERLAY = '/usr/local/portage/eclass-overlay'

_INTERNAL_BINHOST_DIR = os.path.join(
    constants.SOURCE_ROOT, 'src/private-overlays/chromeos-partner-overlay/'
    'chromeos/binhost/target')
_EXTERNAL_BINHOST_DIR = os.path.join(
    constants.SOURCE_ROOT, constants.CHROMIUMOS_OVERLAY_DIR,
    'chromeos/binhost/target')

_CHROMEOS_INTERNAL_BOTO_PATH = os.path.join(
    constants.SOURCE_ROOT, 'src', 'private-overlays', 'chromeos-overlay',
    'googlestorage_account.boto')

_ARCH_MAPPING = {
    'amd64': 'amd64-generic',
    'x86': 'x86-generic',
    'arm': 'arm-generic',
    'arm64': 'arm64-generic',
    'mips': 'mipsel-o32-generic',
}


class Error(Exception):
  """Module base error class."""


# This error is meant to be used with build_packages. The script has not yet
# been ported to chromite but the error is already useful for the script wrapper
# implementation. This exists here so the setup_board (ToolchainInstallError)
# and build_packages errors exist in a common, sensible location.
class PackageInstallError(Error, cros_build_lib.RunCommandError):
  """An error installing packages."""

  def __init__(self, msg, result, exception=None, packages=None):
    """Init method.

    Args:
      msg (str): The message.
      result (cros_build_lib.CommandResult): The command result.
      exception (BaseException|None): An origin exception.
      packages (list[package_info.CPV]): The list of failed packages.
    """
    super(PackageInstallError, self).__init__(msg, result, exception)
    self.failed_packages = packages
    self.args = (self.args, packages)

  def Stringify(self, stdout=True, stderr=True):
    """Stringify override to include the failed package info.

    See:
      cros_build_lib.RunCommandError.Stringify
    """
    items = [super(PackageInstallError, self).Stringify(stdout, stderr)]

    pkgs = []
    for cpv in self.failed_packages:
      if cpv.cpf:
        pkgs.append(cpv.cpf)
      elif cpv.cp:
        pkgs.append(cpv.cp)
      elif cpv.package:
        pkgs.append(cpv.package)

    if pkgs:
      items.append('Failed Packages: %s' % ' '.join(pkgs))

    return '\n'.join(items)


class ToolchainInstallError(PackageInstallError):
  """An error when installing a toolchain package.

  Essentially identical to PackageInstallError, but has names that better
  reflect that the packages are toolchain packages.
  """

  def __init__(self, msg, result, exception=None, tc_info=None):
    """Init method.

    Args:
      msg (str): The message.
      result (cros_build_lib.CommandResult): The command result.
      exception (BaseException|None): An origin exception.
      tc_info (list[package_info.CPV]): The list of failed toolchain packages.
    """
    super(ToolchainInstallError, self).__init__(msg, result, exception,
                                                packages=tc_info)

  @property
  def failed_toolchain_info(self):
    return self.failed_packages


def _CreateWrapper(wrapper_path, template, **kwargs):
  """Creates a wrapper from a given template.

  Args:
    wrapper_path: path to the wrapper.
    template: wrapper template.
    kwargs: fields to be set in the template.
  """
  osutils.WriteFile(wrapper_path, template.format(**kwargs), makedirs=True,
                    sudo=True)
  cros_build_lib.sudo_run(['chmod', '+x', wrapper_path], print_cmd=False,
                          stderr=True)


def _NotEmpty(filepath):
  """Returns True if |filepath| is not empty.

  Args:
    filepath: path to a file.
  """
  return os.path.exists(filepath) and osutils.ReadFile(filepath).strip()


def _DictToKeyValue(dictionary):
  """Formats dictionary in to a key=value string.

  Args:
    dictionary: a python dictionary.
  """
  output = []
  for key in sorted(dictionary.keys()):
    output.append('%s="%s"' % (key, dictionary[key]))

  return '\n'.join(output)


def _GetMakeConfGenericPath():
  """Get the path to the make.conf.generic-target file."""
  return os.path.join(_CHROMIUMOS_CONFIG, 'make.conf.generic-target')


def _GetChrootMakeConfUserPath():
  """Get the path to the chroot's make.conf.user file."""
  return '/%s' % _MAKE_CONF_USER


class Profile(object):
  """Class that encapsulates the profile name for a sysroot."""

  def __init__(self, name=''):
    self._name = name

  @property
  def name(self):
    return self._name

  def __eq__(self, other):
    return self.name == other.name

  @property
  def as_protobuf(self):
    return common_pb2.Profile(name=self._name)

  @classmethod
  def from_protobuf(cls, message):
    return cls(name=message.name)


class Sysroot(object):
  """Class that encapsulate the interaction with sysroots."""

  def __init__(self, path):
    self.path = path
    self._config_file = self._Path(_CONFIGURATION_PATH)
    self._cache_file = self._Path(_CACHE_PATH)
    self._cache_file_lock = self._cache_file + '.lock'

  def __eq__(self, other):
    """Equality check."""
    return self.path == other.path

  def Exists(self, chroot=None):
    """Check if the sysroot exists.

    Args:
      chroot (chroot_lib.Chroot): Optionally check if the sysroot exists inside
        the specified chroot.

    Returns:
      bool
    """
    if chroot:
      return chroot.has_path(self.path)

    return os.path.exists(self.path)

  def _Path(self, *args):
    """Helper to build out a path within the sysroot.

    Pass args as if calling os.path.join().

    Args:
      args (str): path components to join.

    Returns:
      str
    """
    return os.path.join(self.path, *args)

  def GetStandardField(self, field):
    """Returns the value of a standard field.

    Args:
      field: Field from the standard configuration file to get.
        One of STANDARD_FIELD_* from above.
    """
    return osutils.SourceEnvironment(self._config_file,
                                     [field], multiline=True).get(field)

  def GetCachedField(self, field):
    """Returns the value of |field| in the sysroot cache file.

    Access to the cache is thread-safe as long as we access it through this
    methods or the bash helper in common.sh.

    Args:
      field: name of the field.
    """
    if not os.path.exists(self._cache_file):
      return None

    with locking.FileLock(
        self._cache_file_lock, locktype=locking.FLOCK,
        world_writable=True).read_lock():
      return osutils.SourceEnvironment(self._cache_file, [field]).get(field)

  def SetCachedField(self, field, value):
    """Sets |field| to |value| in the sysroot cache file.

    Access to the cache is thread-safe as long as we access it through this
    methods or the bash helper in common.sh.

    Args:
      field: name of the field.
      value: value to set. If |value| is None, the field is unset.
    """
    # TODO(bsimonnet): add support for values with quotes and newlines.
    # crbug.com/476764.
    for symbol in '\n`$"\\':
      if value and symbol in value:
        raise ValueError('Cannot use \\n, `, $, \\ or " in cached value.')

    with locking.FileLock(
        self._cache_file_lock, locktype=locking.FLOCK,
        world_writable=True).write_lock():
      lines = []
      if os.path.exists(self._cache_file):
        lines = osutils.ReadFile(self._cache_file).splitlines()

        # Remove the old value for field if it exists.
        lines = [l for l in lines if not l.startswith(field + '=')]

      if value is not None:
        lines.append('%s="%s"' % (field, value))
      osutils.WriteFile(self._cache_file, '\n'.join(lines), sudo=True)

  def _WrapperPath(self, command, friendly_name=None):
    """Returns the path to the wrapper for |command|.

    Args:
      command: command to wrap.
      friendly_name: suffix to add to the command name. If None, the wrapper
        will be created in the sysroot.
    """
    if friendly_name:
      return os.path.join(_wrapper_dir, '%s-%s' % (command, friendly_name))
    return self._Path('build', 'bin', command)

  def CreateAllWrappers(self, friendly_name=None):
    """Creates all the wrappers.

    Creates all portage tools wrappers, plus wrappers for gdb, cros_workon and
    pkg-config.

    Args:
      friendly_name: if not None, create friendly wrappers with |friendly_name|
        added to the command.
    """
    chost = self.GetStandardField(STANDARD_FIELD_CHOST)
    for cmd in ('ebuild', 'eclean', 'emaint', 'equery', 'portageq', 'qcheck',
                'qdepends', 'qfile', 'qlist', 'qmerge', 'qsize'):
      args = {'sysroot': self.path, 'chost': chost, 'command': cmd}
      if friendly_name:
        _CreateWrapper(self._WrapperPath(cmd, friendly_name),
                       _PORTAGE_WRAPPER_TEMPLATE, **args)
      _CreateWrapper(self._WrapperPath(cmd),
                     _PORTAGE_WRAPPER_TEMPLATE, **args)

    if friendly_name:
      _CreateWrapper(self._WrapperPath('emerge', friendly_name),
                     _PORTAGE_WRAPPER_TEMPLATE, sysroot=self.path, chost=chost,
                     command='emerge --root-deps',
                     source_root=constants.SOURCE_ROOT)
      # TODO(crbug.com/1108874): Delete the deprecated wrapper.
      _CreateWrapper(
          self._WrapperPath('cros_workon', friendly_name),
          _BOARD_WRAPPER_DEPRECATED_CMD_TEMPLATE,
          board=friendly_name,
          command='cros_workon',
          deprecated=(
              'cros_workon-%s is deprecated, use cros-workon-%s instead.' %
              (friendly_name, friendly_name)))
      _CreateWrapper(self._WrapperPath('cros-workon', friendly_name),
                     _BUILD_TARGET_WRAPPER_TEMPLATE, build_target=friendly_name,
                     command='cros workon')
      _CreateWrapper(self._WrapperPath('gdb', friendly_name),
                     _BOARD_WRAPPER_TEMPLATE, board=friendly_name,
                     command='cros_gdb')
      _CreateWrapper(self._WrapperPath('pkg-config', friendly_name),
                     _PKGCONFIG_WRAPPER_TEMPLATE, sysroot=self.path)

    _CreateWrapper(self._WrapperPath('pkg-config'),
                   _PKGCONFIG_WRAPPER_TEMPLATE, sysroot=self.path)
    _CreateWrapper(self._WrapperPath('emerge'), _PORTAGE_WRAPPER_TEMPLATE,
                   sysroot=self.path, chost=chost, command='emerge --root-deps',
                   source_root=constants.SOURCE_ROOT)

    # Create a link to the debug symbols in the chroot so that gdb can detect
    # them.
    debug_symlink = os.path.join('/usr/lib/debug', self.path.lstrip('/'))
    sysroot_debug = self._Path('usr/lib/debug')
    osutils.SafeMakedirs(os.path.dirname(debug_symlink), sudo=True)
    osutils.SafeMakedirs(os.path.dirname(sysroot_debug), sudo=True)

    osutils.SafeSymlink(sysroot_debug, debug_symlink, sudo=True)

  def InstallMakeConf(self):
    """Make sure the make.conf file exists and is up to date."""
    config_file = _GetMakeConfGenericPath()
    osutils.SafeSymlink(config_file, self._Path(_MAKE_CONF), sudo=True)

  def InstallMakeConfBoard(self, accepted_licenses=None, local_only=False,
                           package_indexes=None,
                           expanded_binhost_inheritance: bool = False):
    """Make sure the make.conf.board file exists and is up to date.

    Args:
      accepted_licenses (str): Any additional accepted licenses.
      local_only (bool): Whether prebuilts can be fetched from remote sources.
      package_indexes (list[PackageIndexInfo]): List of information about
        available prebuilts, youngest first, or None.
      expanded_binhost_inheritance: Whether to enable expanded binhost
        inheritance, which searches for additional binhosts to include to
        attempt to improve binhost hit rates.
    """
    board_conf = self.GenerateBoardMakeConf(accepted_licenses=accepted_licenses)
    make_conf_path = self._Path(_MAKE_CONF_BOARD)
    osutils.WriteFile(make_conf_path, board_conf, sudo=True)

    # Once make.conf.board has been generated, generate the binhost config.
    # We need to do this in two steps as the binhost generation step needs
    # portageq to be available.
    binhost_conf = self.GenerateBinhostConf(
        local_only=local_only,
        package_indexes=package_indexes,
        expanded_binhost_inheritance=expanded_binhost_inheritance)
    osutils.WriteFile(make_conf_path, '%s\n%s\n' % (board_conf, binhost_conf),
                      sudo=True)

  def InstallMakeConfBoardSetup(self, board):
    """Make sure the sysroot has the make.conf.board_setup file.

    Args:
      board (str): The name of the board being setup in the sysroot.
    """
    osutils.WriteFile(self._Path(_MAKE_CONF_BOARD_SETUP),
                      self.GenerateBoardSetupConfig(board), sudo=True)

  def InstallMakeConfUser(self):
    """Make sure the sysroot has the make.conf.user file.

    This method assumes the chroot's make.conf.user file exists.
    See chroot_util.CreateMakeConfUser() to create one if needed.
    Only works inside the chroot.
    """
    make_user = _GetChrootMakeConfUserPath()
    link_path = self._Path(_MAKE_CONF_USER)
    if not os.path.exists(link_path):
      osutils.SafeSymlink(make_user, link_path, sudo=True)

  def _GenerateConfig(self, toolchains, board_overlays, portdir_overlays,
                      header, **kwargs):
    """Create common config settings for boards and bricks.

    Args:
      toolchains: ToolchainList object to use.
      board_overlays: List of board overlays.
      portdir_overlays: List of portage overlays.
      header: Header comment string; must start with #.
      kwargs: Additional configuration values to set.

    Returns:
      Configuration string.

    Raises:
      ConfigurationError: Could not generate a valid configuration.
    """
    config = {}

    default_toolchains = toolchain.FilterToolchains(toolchains, 'default', True)
    if not default_toolchains:
      raise ConfigurationError('No default toolchain could be found.')
    config['CHOST'] = list(default_toolchains)[0]
    config['ARCH'] = toolchain.GetArchForTarget(config['CHOST'])

    config['BOARD_OVERLAY'] = '\n'.join(board_overlays)
    config['PORTDIR_OVERLAY'] = '\n'.join(portdir_overlays)

    config['MAKEOPTS'] = '-j%s' % str(multiprocessing.cpu_count())
    config['ROOT'] = self.path + '/'
    config['PKG_CONFIG'] = self._WrapperPath('pkg-config')

    config.update(kwargs)

    return '\n'.join((header, _DictToKeyValue(config)))

  def GenerateBoardSetupConfig(self, board):
    """Generates the setup configuration for a given board.

    Args:
      board (str): board name to use to generate the configuration.
    """
    toolchains = toolchain.GetToolchainsForBoard(board)

    # Compute the overlay list.
    portdir_overlays = portage_util.FindOverlays(constants.BOTH_OVERLAYS, board)
    prefix = os.path.join(constants.SOURCE_ROOT, 'src', 'third_party')
    board_overlays = [o for o in portdir_overlays if not o.startswith(prefix)]

    header = '# Created by cros_sysroot_utils from --board=%s.' % board
    return self._GenerateConfig(toolchains, board_overlays, portdir_overlays,
                                header, BOARD_USE=board)

  def WriteConfig(self, config):
    """Writes the configuration.

    Args:
      config: configuration to use.
    """
    osutils.WriteFile(self._config_file, config, makedirs=True, sudo=True)

  def GenerateBoardMakeConf(self, accepted_licenses=None):
    """Generates the board specific make.conf.

    Args:
      accepted_licenses: Licenses accepted by portage as a string.

    Returns:
      The make.conf file as a python string.
    """
    config = ["""# AUTO-GENERATED FILE. DO NOT EDIT.

  # Source make.conf from each overlay."""]

    overlay_list = self.GetStandardField(STANDARD_FIELD_BOARD_OVERLAY)
    boto_config = ''
    for overlay in overlay_list.splitlines():
      make_conf = os.path.join(overlay, 'make.conf')
      boto_file = os.path.join(overlay, 'googlestorage_account.boto')
      if os.path.isfile(make_conf):
        config.append('source %s' % make_conf)

      if os.path.isfile(boto_file):
        boto_config = boto_file

    # If there is a boto file in the chromeos internal overlay, use it as it
    # will have access to the most stuff.
    if os.path.isfile(_CHROMEOS_INTERNAL_BOTO_PATH):
      boto_config = _CHROMEOS_INTERNAL_BOTO_PATH
    else:
      # NB: Do not touch this w/out build consult.  Pretend this doesn't exist.
      config.append('USE="$USE -ondevice_speech"')

    gs_fetch_binpkg = os.path.join(constants.SOURCE_ROOT, 'chromite', 'bin',
                                   'gs_fetch_binpkg')
    gsutil_cmd = '%s \\"${URI}\\" \\"${DISTDIR}/${FILE}\\"' % gs_fetch_binpkg
    config.append('BOTO_CONFIG="%s"' % boto_config)
    config.append('FETCHCOMMAND_GS="bash -c \'BOTO_CONFIG=%s %s\'"'
                  % (boto_config, gsutil_cmd))
    config.append('RESUMECOMMAND_GS="$FETCHCOMMAND_GS"')

    if accepted_licenses:
      config.append('ACCEPT_LICENSE="%s"' % accepted_licenses)

    return '\n'.join(config)

  def GenerateBinhostConf(self, local_only=False, package_indexes=None,
                          expanded_binhost_inheritance: bool = False):
    """Returns the binhost configuration.

    Args:
      local_only (bool): If True, use binary packages from local boards only.
      package_indexes (list[PackageIndexInfo]): List of information about
        available prebuilts, youngest first, or None.
      expanded_binhost_inheritance: Look for additional binhosts to inherit.

    Returns:
      str - The config contents.
    """
    board = self.GetStandardField(STANDARD_FIELD_BOARD_USE)
    if local_only:
      if not board:
        return ''
      # TODO(bsimonnet): Refactor cros_generate_local_binhosts into a function
      # here and remove the following call.
      local_binhosts = cros_build_lib.run(
          [os.path.join(constants.CHROMITE_BIN_DIR,
                        'cros_generate_local_binhosts'), '--board=%s' % board],
          print_cmd=False, capture_output=True, encoding='utf-8').stdout
      return '\n'.join([local_binhosts,
                        'PORTAGE_BINHOST="$LOCAL_BINHOST"'])

    config = []
    if package_indexes:
      # TODO(crbug/1088059): Drop all use of overlay commits, once the solution
      # is in place for non-snapshot checkouts.
      # If present, this defines PORTAGE_BINHOST.  These are independent of the
      # overlay commits.
      config.append('# This is the list of binhosts provided by the API.')
      config.append('PASSED_BINHOST="%s"' % ' '.join(
          x.location for x in reversed(package_indexes)))
      config.append('PORTAGE_BINHOST="$PASSED_BINHOST"')
      return '\n'.join(config)

    postsubmit_binhost, postsubmit_binhost_internal = self._PostsubmitBinhosts(
        board, expanded_binhost_inheritance)

    config.append("""
# FULL_BINHOST is populated by the full builders. It is listed first because it
# is the lowest priority binhost. It is better to download packages from the
# postsubmit binhost because they are fresher packages.
PORTAGE_BINHOST="$FULL_BINHOST"
""")

    if postsubmit_binhost:
      config.append("""
# POSTSUBMIT_BINHOST is populated by the postsubmit builders. If the same
# package is provided by both the postsubmit and full binhosts, the package is
# downloaded from the postsubmit binhost.
source %s
PORTAGE_BINHOST="$PORTAGE_BINHOST $POSTSUBMIT_BINHOST"
""" % postsubmit_binhost)

    if postsubmit_binhost_internal:
      config.append("""
# The internal POSTSUBMIT_BINHOST is populated by the internal postsubmit
# builders. It takes priority over the public postsubmit binhost.
source %s
PORTAGE_BINHOST="$PORTAGE_BINHOST $POSTSUBMIT_BINHOST"
""" % postsubmit_binhost_internal)

    return '\n'.join(config)

  def _PostsubmitBinhosts(self, board: Union[str, None],
                          expanded_binhost_inheritance: bool):
    """Returns the postsubmit binhost to use."""
    prefixes = []
    # The preference of picking the binhost file for a board is in the same
    # order of prefixes, so it's critical to make sure
    # <board>-POSTSUBMIT_BINHOST.conf is at the top of |prefixes| list.
    if board:
      prefixes = [board]
      # Add reference board if applicable.
      if '_' in board:
        prefixes.append(board.split('_')[0])
      elif expanded_binhost_inheritance:
        # Search the public parent overlays for the given board, and include
        # the parents' binhosts; e.g. eve for eve-kvm.
        overlays = portage_util.FindOverlays(constants.PUBLIC_OVERLAYS,
                                             board=board)
        names = [portage_util.GetOverlayName(x) for x in overlays]
        prefixes.extend(x for x in names if x != board)

    # Add base architecture board.
    arch = self.GetStandardField(STANDARD_FIELD_ARCH)
    if arch in _ARCH_MAPPING:
      prefixes.append(_ARCH_MAPPING[arch])

    filenames = ['%s-POSTSUBMIT_BINHOST.conf' % p for p in prefixes]

    external = internal = None
    for filename in filenames:
      # The binhost file must exist and not be empty, both for internal and
      # external binhosts.
      # When a builder is deleted and no longer publishes prebuilts, we need
      # developers to pick up the next set of prebuilts. Clearing the binhost
      # files triggers this.
      candidate = os.path.join(_INTERNAL_BINHOST_DIR, filename)
      if not internal and _NotEmpty(candidate):
        internal = candidate

      candidate = os.path.join(_EXTERNAL_BINHOST_DIR, filename)
      if not external and _NotEmpty(candidate):
        external = candidate

    return external, internal

  def CreateSkeleton(self):
    """Creates a sysroot skeleton."""
    needed_dirs = [
        self._Path('etc', 'portage', 'hooks'),
        self._Path('etc', 'portage', 'profile'),
        '/usr/local/bin',
    ]
    for d in needed_dirs:
      osutils.SafeMakedirs(d, sudo=True)

    # Create links for portage hooks.
    hook_glob = os.path.join(constants.CROSUTILS_DIR, 'hooks', '*')
    for filename in glob.glob(hook_glob):
      linkpath = self._Path('etc', 'portage', 'hooks',
                            os.path.basename(filename))
      osutils.SafeSymlink(filename, linkpath, sudo=True)

  def UpdateToolchain(self, board, local_init=True):
    """Updates the toolchain packages.

    This will install both the toolchains and the packages that are implicitly
    needed (gcc-libs, linux-headers).

    Args:
      board (str): The name of the board.
      local_init (bool): Whether to use local packages to bootstrap the
        implicit dependencies.
    """
    try:
      toolchain.InstallToolchain(self)
    except toolchain.ToolchainInstallError as e:
      raise ToolchainInstallError(str(e), e.result, exception=e.exception,
                                  tc_info=e.failed_toolchain_info)

    if not self.IsToolchainInstalled():
      # Emerge the implicit dependencies.
      emerge = self._UpdateToolchainCommand(board, local_init)

      # Use a tempdir to handle the status file cleanup.
      with osutils.TempDir() as tempdir:
        extra_env = {constants.CROS_METRICS_DIR_ENVVAR: tempdir}

        try:
          cros_build_lib.sudo_run(emerge, preserve_env=True,
                                  extra_env=extra_env)
        except cros_build_lib.RunCommandError as e:
          # Include failed packages from the status file in the error.
          failed_pkgs = portage_util.ParseDieHookStatusFile(tempdir)
          raise ToolchainInstallError(str(e), e.result, exception=e,
                                      tc_info=failed_pkgs)

      # Record we've installed them so we don't call emerge each time.
      self.SetCachedField(_IMPLICIT_SYSROOT_DEPS_KEY, 'yes')

  def _UpdateToolchainCommand(self, board, local_init):
    """Helper function to build the emerge command for UpdateToolchain."""
    emerge = [os.path.join(constants.CHROMITE_BIN_DIR, 'parallel_emerge'),
              '--board=%s' % board, '--root-deps=rdeps', '--select',
              '--quiet']

    if local_init:
      emerge += ['--getbinpkg', '--usepkg']

    emerge += _IMPLICIT_SYSROOT_DEPS

    return emerge

  def IsToolchainInstalled(self):
    """Check if the toolchain has been installed."""
    return self.GetCachedField(_IMPLICIT_SYSROOT_DEPS_KEY) == 'yes'

  def Delete(self, background=False):
    """Delete the sysroot.

    Optionally run asynchronously. Async delete moves the sysroot into a temp
    directory and then deletes the tempdir with a background task.

    Args:
      background (bool): Whether to run the delete as a background operation.
    """
    rm = ['rm', '-rf', '--one-file-system', '--']
    if background:
      # Make the temporary directory in the same folder as the sysroot were
      # deleting to avoid crossing disks, mounts, etc. that'd cause us to
      # synchronously copy the entire thing before we delete it.
      cwd = os.path.normpath(self._Path('..'))
      try:
        result = cros_build_lib.sudo_run(['mktemp', '-d', '-p', cwd],
                                         print_cmd=False, encoding='utf-8',
                                         stdout=True, cwd=cwd)
      except cros_build_lib.RunCommandError:
        # Fall back to a synchronous delete just in case.
        logging.notice('Error deleting sysroot asynchronously. Deleting '
                       'synchronously instead. This may take a minute.')
        return self.Delete(background=False)

      tempdir = result.output.strip()
      cros_build_lib.sudo_run(['mv', self.path, tempdir], quiet=True)
      if not os.fork():
        # Child process, just delete the sysroot root and _exit.
        result = cros_build_lib.sudo_run(rm + [tempdir], quiet=True,
                                         check=False)
        if result.returncode:
          # Log it so it can be handled manually.
          logging.warning('Unable to delete old sysroot now at %s: %s', tempdir,
                          result.error)
        # pylint: disable=protected-access
        os._exit(result.returncode)
    else:
      cros_build_lib.sudo_run(rm + [self.path], quiet=True)

  def get_sdk_provided_packages(self) -> Iterable[package_info.PackageInfo]:
    """Find all packages provided by the SDK (i.e. package.provided)."""
    # Look at packages in package.provided.
    sdk_file_path = self._Path('etc', 'portage', 'profile', 'package.provided')
    for line in osutils.ReadFile(sdk_file_path).splitlines():
      # Skip comments and empty lines.
      line = line.split('#', 1)[0].strip()
      if not line:
        continue
      yield package_info.parse(line)


def get_sdk_provided_packages(
    sysroot_path: str) -> Iterable[package_info.PackageInfo]:
  """Find all packages provided by the SDK (i.e. package.provided).

  Convenience wrapper for the Sysroot method.

  Args:
    sysroot_path: The sysroot to use when finding SDK packages.

  Returns:
    The provided packages.
  """
  sysroot = Sysroot(sysroot_path)
  return sysroot.get_sdk_provided_packages()
