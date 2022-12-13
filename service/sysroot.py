# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sysroot service."""

import contextlib
import glob
import logging
import multiprocessing
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import (
    Dict,
    Generator,
    Iterator,
    List,
    NamedTuple,
    Optional,
    TYPE_CHECKING,
    Union,
)
import urllib

from chromite.lib import cache
from chromite.lib import constants
from chromite.lib import cpupower_helper
from chromite.lib import cros_build_lib
from chromite.lib import goma_lib
from chromite.lib import metrics_lib
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import remoteexec_util
from chromite.lib import sysroot_lib
from chromite.lib import workon_helper


if TYPE_CHECKING:
  from chromite.lib import binpkg
  from chromite.lib import build_target_lib
  from chromite.lib import chroot_lib

# TODO(xcl): Revisit/remove this after the Lacros launch if no longer needed
_CHROME_PACKAGES = ('chromeos-base/chromeos-chrome', 'chromeos-base/chrome-icu')

# A list of critical system packages that should never be incidentally
# reinstalled as a side effect of build_packages. All packages in this list
# are special cased to prefer matching installed versions, overriding the
# typical logic of upgrading to the newest available version.
#
# This list can't include any package that gets installed to a board!
# Packages such as LLVM or binutils must not be in this list as the normal
# rebuild logic must still apply to them for board targets.
#
# TODO(crbug/1050752): Remove this list once we figure out how to exclude
# toolchain packages from being upgraded transitively via BDEPEND relations.
_CRITICAL_SDK_PACKAGES = ('dev-embedded/hps-sdk', 'dev-lang/rust',
                          'dev-lang/go', 'sys-libs/glibc', 'sys-devel/gcc')

_PACKAGE_LIST = List[Optional[str]]

# The default to use for --backtrack everywhere. Must be manually changed in
# update_chroot.
BACKTRACK_DEFAULT = 10

class Error(Exception):
  """Base error class for the module."""


class NoFilesError(Error):
  """When there are no files to archive."""


class InvalidArgumentsError(Error):
  """Invalid arguments."""


class NotInChrootError(Error):
  """When SetupBoard is run outside of the chroot."""


class UpdateChrootError(Error):
  """Error occurred when running update chroot."""


class SetupBoardRunConfig(object):
  """Value object for full setup board run configurations."""

  def __init__(
      self,
      set_default: bool = False,
      force: bool = False,
      usepkg: bool = True,
      jobs: Optional[int] = None,
      regen_configs: bool = False,
      quiet: bool = False,
      update_toolchain: bool = True,
      upgrade_chroot: bool = True,
      init_board_pkgs: bool = True,
      local_build: bool = False,
      toolchain_changed: bool = False,
      package_indexes: Optional[List['binpkg.PackageIndexInfo']] = None,
      expanded_binhost_inheritance: bool = False,
      backtrack: int = BACKTRACK_DEFAULT,
  ):
    """Initialize method.

    Args:
      set_default: Whether to set the passed board as the default.
      force: Force a new sysroot creation when it already exists.
      usepkg: Whether to use binary packages to bootstrap.
      jobs: Max number of simultaneous packages to build.
      regen_configs: Whether to only regen the configs.
      quiet: Whether to print notification when sysroot exists.
      update_toolchain: Update the toolchain?
      upgrade_chroot: Upgrade the chroot before building?
      init_board_pkgs: Emerging packages to sysroot?
      local_build: Bootstrap only from local packages?
      toolchain_changed: Has a toolchain change occurred? Implies 'force'.
      package_indexes: List of information about available prebuilts, youngest
          first, or None.
      expanded_binhost_inheritance: Allow expanded binhost inheritance.
      backtrack: emerge --backtrack value.
    """
    self.set_default = set_default
    self.force = force or toolchain_changed
    self.usepkg = usepkg
    self.jobs = jobs
    self.regen_configs = regen_configs
    self.quiet = quiet
    self.update_toolchain = update_toolchain
    self.update_chroot = upgrade_chroot
    self.init_board_pkgs = init_board_pkgs
    self.local_build = local_build
    self.package_indexes = package_indexes or []
    self.expanded_binhost_inheritance = expanded_binhost_inheritance
    self.backtrack = backtrack

  def GetUpdateChrootArgs(self) -> List[str]:
    """Create a list containing the relevant update_chroot arguments.

    Returns:
      The list of arguments
    """
    args = [f'--backtrack={self.backtrack}']
    if self.usepkg:
      args += ['--usepkg']
    else:
      args += ['--nousepkg']

    if self.jobs:
      args += ['--jobs', str(self.jobs)]

    if not self.update_toolchain:
      args += ['--skip_toolchain_update']

    return args


class BuildPackagesRunConfig(object):
  """Value object to hold build packages run configs."""

  def __init__(
      self,
      usepkg: bool = True,
      install_debug_symbols: bool = False,
      packages: Optional[List[str]] = None,
      use_flags: Optional[List[str]] = None,
      use_goma: bool = False,
      use_remoteexec: bool = False,
      incremental_build: bool = True,
      package_indexes: Optional[List['binpkg.PackageIndexInfo']] = None,
      dryrun: bool = False,
      usepkgonly: bool = False,
      workon: bool = True,
      install_auto_test: bool = True,
      autosetgov: bool = False,
      autosetgov_sticky: bool = False,
      use_any_chrome: bool = True,
      internal_chrome: bool = False,
      clean_build: bool = False,
      eclean: bool = True,
      rebuild_dep: bool = True,
      jobs: Optional[int] = None,
      local_pkg: bool = False,
      dev_image: bool = True,
      factory_image: bool = True,
      test_image: bool = True,
      debug_version: bool = True,
      backtrack: int = BACKTRACK_DEFAULT,
  ):
    """Init method.

    Args:
      usepkg: Whether to use binpkgs or build from source. False currently
        triggers a local build, which will enable local reuse.
      install_debug_symbols: Whether to include the debug symbols for all
        packages.
      packages: The list of packages to install, by default install all packages
        for the target.
      use_flags: A list of use flags to set.
      use_goma: Whether to enable goma.
      use_remoteexec: Whether to use RBE for remoteexec.
      incremental_build: Whether to treat the build as an incremental build or a
        fresh build. Always treating it as an incremental build is safe, but
        certain operations can be faster when we know we are doing a fresh
        build.
      package_indexes: List of information about available prebuilts, youngest
        first, or None.
      dryrun: Whether to do a dryrun and not actually build any packages.
      usepkgonly: Only use binary packages to bootstrap; abort if any are
        missing.
      workon: Force-build workon packages.
      install_auto_test: Build autotest client code.
      autosetgov: Automatically set cpu governor to 'performance'.
      autosetgov_sticky: Remember --autosetgov setting for future runs.
      use_any_chrome: Use any Chrome prebuilt available, even if the prebuilt
        doesn't match exactly.
      internal_chrome: Build the internal version of chrome.
      clean_build: Perform a clean build; delete sysroot if it exists before
        building.
      eclean: Run eclean to delete old binpkgs.
      rebuild_dep: Rebuild dependencies.
      jobs: How many packages to build in parallel at maximum.
      local_pkg: Bootstrap from local packages instead of remote packages.
      dev_image: Build useful developer friendly utilities.
      factory_image: Build factory installer.
      test_image: Build packages required for testing.
      debug_version: Build debug versions of Chromium-OS-specific packages.
      backtrack: emerge --backtrack value.
    """
    self.usepkg = usepkg
    self.install_debug_symbols = install_debug_symbols
    self.packages = packages
    self.use_flags = use_flags
    self.use_goma = use_goma
    self.use_remoteexec = use_remoteexec
    self.is_incremental = incremental_build
    self.package_indexes = package_indexes or []
    self.dryrun = dryrun
    self.usepkgonly = usepkgonly
    self.workon = workon
    self.install_auto_test = install_auto_test
    self.autosetgov = autosetgov
    self.autosetgov_sticky = autosetgov_sticky
    self.use_any_chrome = use_any_chrome
    self.internal_chrome = internal_chrome
    self.clean_build = clean_build
    self.eclean = eclean
    self.rebuild_dep = rebuild_dep
    self.jobs = jobs
    self.local_pkg = local_pkg
    self.dev_image = dev_image
    self.factory_image = factory_image
    self.test_image = test_image
    self.debug_version = debug_version
    self.backtrack = backtrack

  def GetUseFlags(self) -> Optional[str]:
    """Get the use flags as a single string."""
    use_flags = os.environ.get('USE', '').split()

    if self.use_flags:
      use_flags.extend(self.use_flags)

    if self.internal_chrome:
      use_flags.append('chrome_internal')

    if not self.debug_version:
      use_flags.append('-cros-debug')

    return ' '.join(use_flags) if use_flags else None

  def GetExtraEnv(self) -> Dict[str, str]:
    """Get the extra env for this config."""
    env = {}

    use_flags = self.GetUseFlags()
    if use_flags:
      env['USE'] = use_flags

    if self.use_goma:
      env['USE_GOMA'] = 'true'

    if self.use_remoteexec:
      env['USE_REMOTEEXEC'] = 'true'

    if self.package_indexes:
      env['PORTAGE_BINHOST'] = ' '.join(
          x.location for x in reversed(self.package_indexes))

    return env

  def GetPackages(self) -> List[str]:
    """Get the set of packages to build for this config."""
    if self.packages:
      return self.packages

    packages = ['virtual/target-os']

    if self.dev_image:
      packages.append('virtual/target-os-dev')

    if self.factory_image:
      packages.extend(
          ['virtual/target-os-factory', 'virtual/target-os-factory-shim'])

    if self.test_image:
      packages.append('virtual/target-os-test')

    if self.install_auto_test:
      packages.append('chromeos-base/autotest-all')

    return packages

  @metrics_lib.timed('service.sysroot.GetForceLocalBuildPackages')
  def GetForceLocalBuildPackages(self,
                                 sysroot: sysroot_lib.Sysroot) -> _PACKAGE_LIST:
    """Get the set of force local build packages for this config.

    This includes:
      1. Getting packages for a test image.
      2. Getting packages and reverse dependencies for cros workon packages.
      3. Getting packages and reverse dependencies for base install packages.

    Args:
      sysroot: The sysroot to get packages for.

    Returns:
      A list of packages to build from source.

    Raises:
      cros_build_lib.RunCommandError
    """
    sysroot_path = Path(sysroot.path)
    force_local_build_packages = set()
    packages = self.GetPackages()
    metrics_prefix = 'service.sysroot.GetForceLocalBuildPackages'

    if 'virtual/target-os-test' in packages:
      # chromeos-ssh-testkeys may generate ssh keys if the right USE flag is
      # set. We force rebuilding this package from source every time, so that
      # consecutive builds don't share ssh keys.
      force_local_build_packages.add('chromeos-base/chromeos-ssh-testkeys')

    cros_workon_packages = None
    if self.workon:
      cros_workon_packages = _GetCrosWorkonPackages(sysroot_path)

      # Any package that directly depends on an active cros_workon package also
      # needs to be rebuilt in order to be correctly built against the current
      # set of changes a user may have made to the cros_workon package.
      if cros_workon_packages:
        force_local_build_packages.update(cros_workon_packages)

        with metrics_lib.timer(
            f'{metrics_prefix}.CrosWorkonReverseDependencies'):
          reverse_dependencies = [
              x.atom for x in portage_util.GetReverseDependencies(
                  cros_workon_packages, sysroot_path)
          ]
        logging.info(
            'The following packages depend directly on an active cros_workon '
            'package and will be rebuilt: %s', ' '.join(reverse_dependencies))
        force_local_build_packages.update(reverse_dependencies)

    # Determine base install packages and reverse dependencies if incremental
    # build (--withdevdeps) and clean build (--cleanbuild) is not specified or
    # the sysroot path exists.
    if self.is_incremental and (not self.clean_build or sysroot_path.exists()):
      logging.info('Starting reverse dependency calculations...')

      # Temporarily modify the emerge flags so we can calculate the revdeps on
      # the modified packages.
      sim_emerge_flags = self.GetEmergeFlags()
      sim_emerge_flags.extend([
          '--pretend',
          '--columns',
          f'--reinstall-atoms={" ".join(packages)}',
          f'--usepkg-exclude={" ".join(packages)}',
      ])

      # cros-workon packages are always going to be force reinstalled, so we
      # add the forced reinstall behavior to the modified package calculation.
      # This is necessary to include when a user has already installed a 9999
      # ebuild and is now reinstalling that package with additional local
      # changes, because otherwise the modified package calculation would not
      # see that a 'new' package is being installed.
      if cros_workon_packages:
        sim_emerge_flags.extend([
            f'--reinstall-atoms={" ".join(cros_workon_packages)}',
            f'--usepkg-exclude={" ".join(cros_workon_packages)}',
        ])

      revdeps_packages = _GetBaseInstallPackages(sysroot_path, sim_emerge_flags,
                                                 packages)
      if revdeps_packages:
        force_local_build_packages.update(revdeps_packages)
        logging.info('Calculating reverse dependencies on packages: %s',
                     ' '.join(revdeps_packages))
        with metrics_lib.timer(f'{metrics_prefix}.ReverseDependencies'):
          r_revdeps_packages = portage_util.GetReverseDependencies(
              revdeps_packages, sysroot_path, indirect=True)

        exclude_patterns = ['virtual/']
        exclude_patterns.extend(_CHROME_PACKAGES)
        reverse_dependencies = [
            x.atom
            for x in r_revdeps_packages
            if not any(p in x.atom for p in exclude_patterns)
        ]
        logging.info('Final reverse dependencies that will be rebuilt: %s',
                     ' '.join(reverse_dependencies))
        force_local_build_packages.update(reverse_dependencies)

    return list(force_local_build_packages)

  def GetEmergeFlags(self) -> List[str]:
    """Get the emerge flags for this config."""
    flags = [
        '-uDNv',
        f'--backtrack={self.backtrack}',
        '--newrepo',
        '--with-test-deps',
        'y',
    ]

    if self.use_any_chrome:
      for pkg in _CHROME_PACKAGES:
        flags.append(f'--force-remote-binary={pkg}')

    extra_board_flags = os.environ.get('EXTRA_BOARD_FLAGS', '').split()
    if extra_board_flags:
      flags.extend(extra_board_flags)

    if self.dryrun:
      flags.append('--pretend')

    if self.usepkg or self.local_pkg or self.usepkgonly:
      # Use binary packages. Include all build-time dependencies, so as to
      # avoid unnecessary differences between source and binary builds.
      flags.extend(['--getbinpkg', '--with-bdeps', 'y'])
      if self.usepkgonly:
        flags.append('--usepkgonly')
      else:
        flags.append('--usepkg')

    if self.jobs:
      flags.append(f'--jobs={self.jobs}')

    if self.rebuild_dep:
      flags.append('--rebuild-if-new-rev')

    return flags


def SetupBoard(target: 'build_target_lib.BuildTarget',
               accept_licenses: Optional[str] = None,
               run_configs: Optional[SetupBoardRunConfig] = None) -> None:
  """Run the full process to setup a board's sysroot.

  This is the entry point to run the setup_board script.

  Args:
    target: The build target configuration.
    accept_licenses: The additional licenses to accept.
    run_configs: The run configs.

  Raises:
    sysroot_lib.ToolchainInstallError when the toolchain fails to install.
  """
  if not cros_build_lib.IsInsideChroot():
    raise NotInChrootError('SetupBoard must be run from inside the chroot')

  # Make sure we have valid run configs setup.
  run_configs = run_configs or SetupBoardRunConfig()

  sysroot = Create(target, run_configs, accept_licenses)

  if run_configs.regen_configs:
    # We're now done if we're only regenerating the configs.
    return

  InstallToolchain(target, sysroot, run_configs)


def Create(target: 'build_target_lib.BuildTarget',
           run_configs: SetupBoardRunConfig,
           accept_licenses: Optional[str]) -> sysroot_lib.Sysroot:
  """Create a sysroot.

  This entry point is the subset of the full setup process that does the
  creation and configuration of a sysroot, including installing portage.

  Args:
    target: The build target being installed in the sysroot being created.
    run_configs: The run configs.
    accept_licenses: The additional licenses to accept.
  """
  cros_build_lib.AssertInsideChroot()

  sysroot = sysroot_lib.Sysroot(target.root)

  if sysroot.Exists() and not run_configs.force and not run_configs.quiet:
    logging.warning(
        'Board output directory already exists: %s\n'
        'Use --force to clobber the board root and start again.', sysroot.path)

  # Override regen_configs setting to force full setup run if the sysroot does
  # not exist.
  run_configs.regen_configs = run_configs.regen_configs and sysroot.Exists()

  # Make sure the chroot is fully up to date before we start unless the
  # chroot update is explicitly disabled.
  if run_configs.update_chroot:
    logging.info('Updating chroot.')
    update_chroot = [
        os.path.join(constants.CROSUTILS_DIR, 'update_chroot'),
        '--toolchain_boards', target.name
    ]
    update_chroot += run_configs.GetUpdateChrootArgs()
    try:
      cros_build_lib.run(update_chroot)
    except cros_build_lib.RunCommandError:
      raise UpdateChrootError('Error occurred while updating the chroot. '
                              'See the logs for more information.')

  # Delete old sysroot to force a fresh start if requested.
  if sysroot.Exists() and run_configs.force:
    sysroot.Delete(background=True)

  # Step 1: Create folders.
  # Dependencies: None.
  # Create the skeleton.
  logging.info('Creating sysroot directories.')
  _CreateSysrootSkeleton(sysroot)

  # Step 2: Standalone configurations.
  # Dependencies: Folders exist.
  # Install main, board setup, and user make.conf files.
  logging.info('Installing configurations into sysroot.')
  _InstallConfigs(sysroot, target)

  # Step 3: Portage configurations.
  # Dependencies: make.conf.board_setup.
  # Create the command wrappers, choose profile, and make.conf.board.
  # Refresh the workon symlinks to compensate for crbug.com/679831.
  logging.info('Setting up portage in the sysroot.')
  _InstallPortageConfigs(
      sysroot,
      target,
      accept_licenses,
      run_configs.local_build,
      package_indexes=run_configs.package_indexes,
      expanded_binhost_inheritance=run_configs.expanded_binhost_inheritance)

  # Developer Experience Step: Set default board (if requested) to allow
  # running later commands without needing to pass the --board argument.
  if run_configs.set_default:
    cros_build_lib.SetDefaultBoard(target.name)

  return sysroot


def GenerateArchive(output_dir: str, build_target_name: str,
                    pkg_list: List[str]) -> str:
  """Generate a sysroot tarball for informational builders.

  Args:
    output_dir: Directory to contain the created the sysroot.
    build_target_name: The build target for the sysroot being created.
    pkg_list: List of 'category/package' package strings.

  Returns:
    Path to the sysroot tar file.
  """
  cmd = [
      'cros_generate_sysroot', '--out-file', constants.TARGET_SYSROOT_TAR,
      '--out-dir', output_dir, '--board', build_target_name, '--package',
      ' '.join(pkg_list)
  ]
  cros_build_lib.run(cmd, cwd=constants.SOURCE_ROOT)
  return os.path.join(output_dir, constants.TARGET_SYSROOT_TAR)


def CreateSimpleChromeSysroot(chroot: 'chroot_lib.Chroot', _sysroot_class,
                              build_target: 'build_target_lib.BuildTarget',
                              output_dir: str) -> str:
  """Create a sysroot for SimpleChrome to use.

  Args:
    chroot: The chroot class used for these artifacts.
    sysroot_class: The sysroot class used for these artifacts.
    build_target: The build target used for these artifacts.
    output_dir: The path to write artifacts to.

  Returns:
    Path to the sysroot tar file.
  """
  cmd = [
      'cros_generate_sysroot', '--out-dir', '/tmp', '--board',
      build_target.name, '--deps-only', '--package', constants.CHROME_CP
  ]
  cros_build_lib.run(
      cmd,
      cwd=constants.SOURCE_ROOT,
      enter_chroot=True,
      chroot_args=chroot.get_enter_args(),
      extra_env=chroot.env)

  # Move the artifact out of the chroot.
  sysroot_tar_path = os.path.join(
      chroot.path, os.path.join('tmp', constants.CHROME_SYSROOT_TAR))
  shutil.copy(sysroot_tar_path, output_dir)
  return os.path.join(output_dir, constants.CHROME_SYSROOT_TAR)


def CreateChromeEbuildEnv(chroot: 'chroot_lib.Chroot',
                          sysroot_class: sysroot_lib.Sysroot, _build_target,
                          output_dir: str) -> Optional[str]:
  """Generate Chrome ebuild environment.

  Args:
    chroot: The chroot class used for these artifacts.
    sysroot_class: The sysroot where the original environment archive can be
      found.
    output_dir: Where the result should be stored.

  Returns:
    The path to the archive, or None.
  """
  pkg_dir = chroot.full_path(sysroot_class.path, portage_util.VDB_PATH)
  files = glob.glob(os.path.join(pkg_dir, constants.CHROME_CP) + '-*')
  if not files:
    logging.warning('No package found for %s', constants.CHROME_CP)
    return None

  if len(files) > 1:
    logging.warning('Expected one package for %s, found %d',
                    constants.CHROME_CP, len(files))

  chrome_dir = sorted(files)[-1]
  env_bzip = os.path.join(chrome_dir, 'environment.bz2')
  result_path = os.path.join(output_dir, constants.CHROME_ENV_TAR)
  with osutils.TempDir() as tempdir:
    # Convert from bzip2 to tar format.
    bzip2 = cros_build_lib.FindCompressor(cros_build_lib.COMP_BZIP2)
    tempdir_tar_path = os.path.join(tempdir, constants.CHROME_ENV_FILE)
    cros_build_lib.run([bzip2, '-d', env_bzip, '-c'], stdout=tempdir_tar_path)

    cros_build_lib.CreateTarball(result_path, tempdir)

  return result_path


def InstallToolchain(target: 'build_target_lib.BuildTarget',
                     sysroot: sysroot_lib.Sysroot,
                     run_configs: SetupBoardRunConfig) -> None:
  """Update the toolchain to a sysroot.

  This entry point just installs the target's toolchain into the sysroot.
  Everything else must have been done already for this to be successful.

  Args:
    target: The target whose toolchain is being installed.
    sysroot: The sysroot where the toolchain is being installed.
    run_configs: The run configs.
  """
  cros_build_lib.AssertInsideChroot()
  if not sysroot.Exists():
    # Sanity check before we try installing anything.
    raise ValueError('The sysroot must exist, run Create first.')

  # Step 4: Install toolchain and packages.
  # Dependencies: Portage configs and wrappers have been installed.
  if run_configs.init_board_pkgs:
    logging.info('Updating toolchain.')
    # Use the local packages if we're doing a local only build or usepkg is set.
    local_init = run_configs.usepkg or run_configs.local_build
    _InstallToolchain(sysroot, target, local_init=local_init)


@metrics_lib.timed('service.sysroot.BuildPackages')
def BuildPackages(target: 'build_target_lib.BuildTarget',
                  sysroot: sysroot_lib.Sysroot,
                  run_configs: BuildPackagesRunConfig) -> None:
  """Build and install packages into a sysroot.

  Args:
    target: The target whose packages are being installed.
    sysroot: The sysroot where the packages are being installed.
    run_configs: The run configs.

  Raises:
    sysroot_lib.PackageInstallError when packages fail to install.
  """
  cros_build_lib.AssertInsideChroot()
  cros_build_lib.AssertNonRootUser()
  metrics_prefix = 'service.sysroot.BuildPackages'

  extra_env = run_configs.GetExtraEnv()
  extra_env['PKGDIR'] = f'{sysroot.path}/packages'
  with osutils.TempDir() as tempdir, cpupower_helper.ModifyCpuGovernor(
      run_configs.autosetgov, run_configs.autosetgov_sticky):
    extra_env[constants.CROS_METRICS_DIR_ENVVAR] = tempdir

    cros_build_lib.ClearShadowLocks(sysroot.path)

    portage_binhost = portage_util.PortageqEnvvar('PORTAGE_BINHOST',
                                                  target.name)
    logging.info('PORTAGE_BINHOST: %s', portage_binhost)

    # Before running any emerge operations, regenerate the Portage dependency
    # cache in parallel.
    logging.info('Rebuilding Portage cache.')
    with metrics_lib.timer(f'{metrics_prefix}.RegenPortageCache'):
      portage_util.RegenDependencyCache(
          sysroot=sysroot.path, jobs=run_configs.jobs)

    # Clean out any stale binpkgs we've accumulated. This is done immediately
    # after regenerating the cache in case ebuilds have been removed (e.g. from
    # a revert).
    if run_configs.eclean:
      _CleanStaleBinpkgs(sysroot.path)

    emerge_cmd = _GetEmergeCommand(sysroot.path)
    emerge_flags = run_configs.GetEmergeFlags()
    rebuild_pkgs = ' '.join(run_configs.GetForceLocalBuildPackages(sysroot))
    if rebuild_pkgs:
      emerge_flags.extend([
          f'--reinstall-atoms={rebuild_pkgs}',
          f'--usepkg-exclude={rebuild_pkgs}',
      ])

    sdk_pkgs = ' '.join(_CRITICAL_SDK_PACKAGES)
    emerge_flags.extend([
        f'--useoldpkg-atoms={sdk_pkgs}',
        f'--rebuild-exclude={sdk_pkgs}',
    ])
    with RemoteExecution(run_configs.use_goma, run_configs.use_remoteexec):
      logging.info('Merging board packages now.')
      try:
        with metrics_lib.timer(f'{metrics_prefix}.emerge'):
          cros_build_lib.sudo_run(
              emerge_cmd + emerge_flags + run_configs.GetPackages(),
              preserve_env=True,
              extra_env=extra_env)
        logging.info('Builds complete.')
      except cros_build_lib.RunCommandError as e:
        failed_pkgs = portage_util.ParseDieHookStatusFile(tempdir)
        raise sysroot_lib.PackageInstallError(
            str(e), e.result, exception=e, packages=failed_pkgs)

    if run_configs.install_debug_symbols:
      logging.info('Fetching the debug symbols.')
      try:
        # TODO(xcl): Convert to directly importing and calling a Python lib
        # instead of calling a binary.
        cros_build_lib.run([
            Path(constants.CHROMITE_BIN_DIR) / 'cros_install_debug_syms',
            f'--board={sysroot.build_target_name}',
            '--all',
        ])
      except cros_build_lib.RunCommandError as e:
        logging.error('Unable to install debug symbols: %s', e)

    # Remove any broken or outdated binpkgs.
    if run_configs.eclean:
      portage_util.CleanOutdatedBinaryPackages(sysroot.path, deep=True)


def _CleanStaleBinpkgs(sysroot: Union[str, os.PathLike]) -> None:
  """Clean any accumulated stale binpkgs.

  Args:
    sysroot: The sysroot to clean stale binpkgs for.

  Raises:
    cros_build_lib.RunCommandError
  """
  logging.info('Cleaning stale binpkgs.')
  exclude_pkgs = [
      x.package_info.atom
      for x in portage_util.PortageDB().InstalledPackages()
      if x.category.startswith('cross-')
  ]
  with tempfile.NamedTemporaryFile(mode='w') as f:
    f.write('\n'.join(exclude_pkgs))
    f.flush()
    portage_util.CleanOutdatedBinaryPackages(
        sysroot, deep=True, exclusion_file=f.name)


def _GetCrosWorkonPackages(sysroot: Union[str, os.PathLike]) -> _PACKAGE_LIST:
  """Get cros_workon packages.

  Args:
    sysroot: The sysroot to get cros_workon packages for.

  Raises:
    cros_build_lib.RunCommandError
  """
  # TODO(xcl): Migrate this to calling an imported Python lib
  cmd = ['cros_list_modified_packages', '--sysroot', sysroot]
  result = cros_build_lib.run(
      cmd, print_cmd=False, capture_output=True, encoding='utf-8')
  logging.info('Detected cros_workon modified packages: %s',
               result.stdout.rstrip())
  packages = result.stdout.split()

  if os.environ.get('CHROME_ORIGIN'):
    packages.extend(_CHROME_PACKAGES)

  return packages


def _GetBaseInstallPackages(sysroot: Union[str, os.PathLike], emerge_flags: str,
                            packages: List[str]) -> List[Optional[str]]:
  """Get packages to determine reverse dependencies for.

  Args:
    sysroot: The sysroot to get packages for.
    emerge_flags: Emerge flags to run the command with.
    packages: The packages to get dependencies for.

  Raises:
    cros_build_lib.RunCommandError
  """
  # Do a pretend `emerge` command to get a list of what would be built.
  # Sample output:
  # [binary N] dev-go/containerd ... to /build/eve/ USE="..."
  # [ebuild r U] chromeos-base/tast-build-deps ... to /build/eve/ USE="..."
  # [binary U] chromeos-base/chromeos-chrome ... to /build/eve/ USE="..."
  cmd = _GetEmergeCommand(sysroot)
  result = cros_build_lib.sudo_run(
      cmd + emerge_flags + packages, capture_output=True, encoding='utf-8')

  # Filter to a heuristic set of packages known to have incorrectly specified
  # dependencies that will be installed to the board sysroot.
  # Sample output is filtered to:
  # [ebuild r U] chromeos-base/tast-build-deps ... to /build/eve/ USE="..."
  include_patterns = ['coreboot-private-files', 'tast-build-deps']

  # Pattern used to rewrite the line from Portage's full output to only
  # $CATEGORY/$PACKAGE.
  pattern = re.compile(r'\[ebuild(.*?)\]\s(.*?)\s')

  # Filter and sort the output and remove any duplicate entries.
  packages = set()
  for line in result.stdout.splitlines():
    if 'to /build/' in line and any(x in line for x in include_patterns):
      # Use regex to get substrings that matches a
      # '[ebuild ...] <some characters> ' pattern. The second matching group
      # returns the $CATEGORY/$PACKAGE from a line of the emerge output.
      m = pattern.search(line)
      if m:
        packages.add(m.group(2))
  return sorted(packages)


def _GetEmergeCommand(
    sysroot: Optional[Union[str, os.PathLike]] = None
) -> List[Union[str, os.PathLike]]:
  """Get the emerge command to use with build_packages."""
  # TODO(xcl): Convert to directly importing and calling a Python lib instead
  # of calling a binary.
  cmd = [Path(constants.CHROMITE_BIN_DIR) / 'parallel_emerge']
  if sysroot:
    cmd.extend([
        f'--sysroot={sysroot}',
        f'--root={sysroot}',
    ])
  return cmd


def _CreateSysrootSkeleton(sysroot: sysroot_lib.Sysroot) -> None:
  """Create the sysroot skeleton.

  Dependencies: None.
  Creates the sysroot directory structure and installs the portage hooks.

  Args:
    sysroot: The sysroot.
  """
  sysroot.CreateSkeleton()


def _InstallConfigs(sysroot: sysroot_lib.Sysroot,
                    target: 'build_target_lib.BuildTarget') -> None:
  """Install standalone configuration files into the sysroot.

  Dependencies: The sysroot exists (i.e. CreateSysrootSkeleton).
  Installs the main, board setup, and user make.conf files.

  Args:
    sysroot: The sysroot.
    target: The build target being setup in the sysroot.
  """
  sysroot.InstallMakeConf()
  sysroot.InstallMakeConfBoardSetup(target.name)
  sysroot.InstallMakeConfUser()


def _InstallPortageConfigs(
    sysroot: sysroot_lib.Sysroot,
    target: 'build_target_lib.BuildTarget',
    accept_licenses: Optional[str],
    local_build: bool,
    package_indexes: List['binpkg.PackageIndexInfo'] = None,
    expanded_binhost_inheritance: bool = False) -> None:
  """Install portage wrappers and configurations.

  Dependencies: make.conf.board_setup (InstallConfigs).
  Create the command wrappers, choose profile, and generate make.conf.board.
  Refresh the workon symlinks to compensate for crbug.com/679831.

  Args:
    sysroot: The sysroot.
    target: The build target being installed in the sysroot.
    accept_licenses: Additional accepted licenses as a string.
    local_build: If the build is a local only build.
    package_indexes: List of information about available prebuilts, youngest
      first, or None.
    expanded_binhost_inheritance: Whether to allow expanded binhost inheritance.
  """
  sysroot.CreateAllWrappers(friendly_name=target.name)
  _ChooseProfile(target, sysroot)
  _RefreshWorkonSymlinks(target.name, sysroot)
  # Must be done after the profile is chosen or binhosts may be incomplete.
  sysroot.InstallMakeConfBoard(
      accepted_licenses=accept_licenses,
      local_only=local_build,
      package_indexes=package_indexes,
      expanded_binhost_inheritance=expanded_binhost_inheritance)


def _InstallToolchain(sysroot: sysroot_lib.Sysroot,
                      target: 'build_target_lib.BuildTarget',
                      local_init: bool = True) -> None:
  """Install toolchain and packages.

  Dependencies: Portage configs and wrappers have been installed
    (InstallPortageConfigs).
  Install the toolchain and the implicit dependencies.

  Args:
    sysroot: The sysroot to install to.
    target: The build target whose toolchain is being installed.
    local_init: Whether to use local packages to bootstrap implicit
      dependencies.
  """
  sysroot.UpdateToolchain(target.name, local_init=local_init)


def _RefreshWorkonSymlinks(target: str, sysroot: sysroot_lib.Sysroot) -> None:
  """Force refresh the workon symlinks.

  Create an instance of the WorkonHelper, which will recreate all symlinks
  to masked/unmasked packages currently worked on in case the sysroot was
  recreated (crbug.com/679831).

  This was done with a call to `cros_workon list` in the bash version of
  the script, but all we actually need is for the WorkonHelper to be
  instantiated since it refreshes the symlinks in its __init__.

  Args:
    target: The build target name.
    sysroot: The board's sysroot.
  """
  workon_helper.WorkonHelper(sysroot.path, friendly_name=target)


def _ChooseProfile(target: 'build_target_lib.BuildTarget',
                   sysroot: sysroot_lib.Sysroot) -> None:
  """Helper function to execute cros_choose_profile.

  TODO(saklein) Refactor cros_choose_profile to avoid needing the run
  call here, and by extension this method all together.

  Args:
    target: The build target whose profile is being chosen.
    sysroot: The sysroot for which the profile is being chosen.
  """
  choose_profile = [
      'cros_choose_profile', '--board', target.name, '--board-root',
      sysroot.path
  ]
  if target.profile:
    # Chooses base by default, only override when we have a passed param.
    choose_profile += ['--profile', target.profile]
  try:
    cros_build_lib.run(choose_profile, print_cmd=False)
  except cros_build_lib.RunCommandError as e:
    logging.error('Selecting profile failed, removing incomplete board '
                  'directory!')
    sysroot.Delete()
    raise e


def BundleDebugSymbols(chroot: 'chroot_lib.Chroot',
                       sysroot_class: sysroot_lib.Sysroot,
                       _build_target: 'build_target_lib.BuildTarget',
                       output_dir: str) -> Optional[str]:
  """Bundle debug symbols into a tarball for importing into GCE.

  Bundle the debug symbols found in the sysroot into a .tgz. This assumes
  these files are present.

  Args:
    chroot: The chroot class used for these artifacts.
    sysroot_class: The sysroot class used for these artifacts.
    build_target: The build target used for these artifacts.
    output_dir: The path to write artifacts to.

  Returns:
    A string path to the output debug.tgz artifact, or None.
  """
  base_path = chroot.full_path(sysroot_class.path)
  debug_dir = os.path.join(base_path, 'usr/lib/debug')

  if not os.path.isdir(debug_dir):
    logging.error('No debug directory found at %s.', debug_dir)
    return None

  # Create tarball from destination_tmp, then copy it...
  tarball_path = os.path.join(output_dir, constants.DEBUG_SYMBOLS_TAR)
  exclude_breakpad_tar_arg = ('--exclude=%s' %
                              os.path.join(debug_dir, 'breakpad'))
  result = None
  try:
    result = cros_build_lib.CreateTarball(
        tarball_path,
        debug_dir,
        compression=cros_build_lib.COMP_GZIP,
        sudo=True,
        extra_args=[exclude_breakpad_tar_arg])
  except cros_build_lib.TarballError:
    pass
  if not result or result.returncode:
    # We don't abort here, because the tar may still be somewhat intact.
    err = result.return_code if result else 'TarballError'
    logging.error('Error (%s) when creating tarball %s from %s', err,
                  tarball_path, debug_dir)
  if os.path.exists(tarball_path):
    return tarball_path
  else:
    return None


def BundleBreakpadSymbols(chroot: 'chroot_lib.Chroot',
                          sysroot_class: sysroot_lib.Sysroot,
                          build_target: 'build_target_lib.BuildTarget',
                          output_dir: str) -> Optional[str]:
  """Bundle breakpad debug symbols into a tarball for importing into GCE.

  Call the GenerateBreakpadSymbols function and archive this into a tar.gz.

  Args:
    chroot: The chroot class used for these artifacts.
    sysroot_class: The sysroot class used for these artifacts.
    build_target: The build target used for these artifacts.
    output_dir: The path to write artifacts to.

  Returns:
    A string path to the output debug_breakpad.tar.gz artifact, or None.
  """
  base_path = chroot.full_path(sysroot_class.path)

  result = GenerateBreakpadSymbols(chroot, build_target, debug=True)

  # Verify breakpad symbol generation before gathering the sym files.
  if result.returncode:
    logging.error('Error (%d) when generating breakpad symbols',
                  result.returncode)
    return None
  with chroot.tempdir() as symbol_tmpdir, chroot.tempdir() as dest_tmpdir:
    breakpad_dir = os.path.join(base_path, 'usr/lib/debug/breakpad')
    # Call list on the atifacts.GatherSymbolFiles generator function to
    # materialize and consume all entries so that all are copied to
    # dest dir and complete list of all symbol files is returned.
    sym_file_list = list(
        GatherSymbolFiles(
            tempdir=symbol_tmpdir, destdir=dest_tmpdir, paths=[breakpad_dir]))

    if not sym_file_list:
      logging.warning('No sym files found in %s.', breakpad_dir)
    # Create tarball from destination_tmp, then copy it...
    tarball_path = os.path.join(output_dir,
                                constants.BREAKPAD_DEBUG_SYMBOLS_TAR)
    result = cros_build_lib.CreateTarball(tarball_path, dest_tmpdir)
    if result.returncode != 0:
      logging.error('Error (%d) when creating tarball %s from %s',
                    result.returncode, tarball_path, dest_tmpdir)
      return None
  return tarball_path


# A SymbolFileTuple is a data object that contains:
#  relative_path (str): Relative path to the file based on initial search path.
#  source_file_name (str): Full path to where the SymbolFile was found.
# For example, if the search path for symbol files is '/some/bot/path/'
# and a symbol file is found at '/some/bot/path/a/b/c/file1.sym',
# then the relative_path would be 'a/b/c/file1.sym' and the source_file_name
# would be '/some/bot/path/a/b/c/file1.sym'.
# The source_file_name is informational for two reasons:
# 1) They are typically copied off a machine (such as a build bot) where
#    that path will disappear, which is why when we find them they get
#    copied to a destination directory.
# 2) For tar files, the source_file_name is not a full path that can be
#    opened, since it is the path the tar file plus the relative path of
#    the file when we untar it.
class SymbolFileTuple(NamedTuple):
  """Contain a relative and full path to a SymbolFile."""
  relative_path: str
  source_file_name: str


def GenerateBreakpadSymbols(chroot: 'chroot_lib.Chroot',
                            build_target: 'build_target_lib.BuildTarget',
                            debug: bool) -> cros_build_lib.CompletedProcess:
  """Generate breakpad (go/breakpad) symbols for debugging.

  This function generates .sym files to /build/<board>/usr/lib/debug/breakpad
  from .debug files found in /build/<board>/usr/lib/debug by calling
  cros_generate_breakpad_symbols.

  Args:
    chroot: The chroot in which the sysroot should be built.
    build_target: The sysroot's build target.
    debug: Include extra debugging output.
  """
  # The firmware directory contains elf symbols that we have trouble parsing
  # and that don't help with breakpad debugging (see https://crbug.com/213670).
  exclude_dirs = ['firmware']

  cmd = ['cros_generate_breakpad_symbols']
  if debug:
    cmd += ['--debug']

  # Execute for board in parallel with half # of cpus available to avoid
  # starving other parallel processes on the same machine.
  cmd += [
      '--board=%s' % build_target.name, '--jobs',
      str(max(1,
              multiprocessing.cpu_count() // 2))
  ]
  cmd += ['--exclude-dir=%s' % x for x in exclude_dirs]

  logging.info('Generating breakpad symbols: %s.', cmd)
  result = cros_build_lib.run(
      cmd, enter_chroot=True, chroot_args=chroot.get_enter_args())
  return result


def GatherSymbolFiles(
    tempdir: str, destdir: str,
    paths: List[str]) -> Generator[SymbolFileTuple, None, None]:
  """Locate symbol files in |paths|

  This generator function searches all paths for .sym files and copies them to
  destdir. A path to a tarball will result in the tarball being unpacked and
  examined. A path to a directory will result in the directory being searched
  for .sym files. The generator yields SymbolFileTuple objects that contain
  symbol file references which are valid after this exits. Those files may exist
  externally, or be created in the tempdir (when expanding tarballs). Typical
  usage in the BuildAPI will be for the .sym files to exist under a directory
  such as /build/<board>/usr/lib/debug/breakpad so that the path to a sym file
  will always be unique.
  Note: the caller must clean up the tempdir.
  Note: this function is recursive for tar files.

  Args:
    tempdir: Path to use for temporary files.
    destdir: All .sym files are copied to this path. Tarfiles are opened inside
      a tempdir and any .sym files within them are copied to destdir from within
      that temp path.
    paths: A list of input paths to walk. Files are returned based on .sym name
      w/out any checking internal symbol file format.
      Dirs are searched for files that end in ".sym". Urls are not handled.
      Tarballs are unpacked and walked.

  Yields:
    A SymbolFileTuple for every symbol file found in paths.
  """
  logging.info('GatherSymbolFiles tempdir %s destdir %s paths %s', tempdir,
               destdir, paths)
  for p in paths:
    o = urllib.parse.urlparse(p)
    if o.scheme:
      raise NotImplementedError('URL paths are not expected/handled: ', p)
    elif not os.path.exists(p):
      raise NoFilesError('The path did not exist: ', p)
    elif os.path.isdir(p):
      for root, _, files in os.walk(p):
        for f in files:
          if f.endswith('.sym'):
            # If p is '/tmp/foo' and filename is '/tmp/foo/bar/bar.sym',
            # relative_path = 'bar/bar.sym'
            filename = os.path.join(root, f)
            relative_path = filename[len(p):].lstrip('/')
            try:
              shutil.copy(filename, os.path.join(destdir, relative_path))
            except IOError:
              # Handles pre-3.3 Python where we may need to make the target
              # path's dirname before copying.
              os.makedirs(os.path.join(destdir, os.path.dirname(relative_path)))
              shutil.copy(filename, os.path.join(destdir, relative_path))
            yield SymbolFileTuple(
                relative_path=relative_path, source_file_name=filename)

    elif cros_build_lib.IsTarball(p):
      tardir = tempfile.mkdtemp(dir=tempdir)
      cache.Untar(os.path.realpath(p), tardir)
      for sym in GatherSymbolFiles(tardir, destdir, [tardir]):
        # The SymbolFileTuple is generated from [tardir], but we want the
        # source_file_name (which informational) to reflect the tar path
        # plus the relative path after the file is untarred.
        # Thus, something like /botpath/some/path/tmp22dl33sa/dir1/fileB.sym
        # (where the tardir is /botpath/some/path/tmp22dl33sa)
        # has a resulting path /botpath/some/path/symfiles.tar/dir1/fileB.sym
        # When we call GatherSymbolFiles with [tardir] as the argument,
        # the os.path.isdir case above will walk the tar contents,
        # processing only .sym. Non-sym files within the tar file will be
        # ignored (even tar files within tar files, which we don't expect).
        new_source_file_name = sym.source_file_name.replace(tardir, p)
        yield SymbolFileTuple(
            relative_path=sym.relative_path,
            source_file_name=new_source_file_name)

    elif os.path.isfile(p):
      # Path p is a file. This code path is only executed when a full file path
      # is one of the elements in the 'paths' argument. When a directory is an
      # element of the 'paths' argument, we walk the tree (above) and process
      # each file. When a tarball is an element of the 'paths' argument, we
      # untar it into a directory and recurse with the temp tardir as the
      # directory, so that tarfile contents are processed (above) in the os.walk
      # of the directory.
      if p.endswith('.sym'):
        shutil.copy(p, destdir)
        yield SymbolFileTuple(
            relative_path=os.path.basename(p), source_file_name=p)
    else:
      raise ValueError('Unexpected input to GatherSymbolFiles: ', p)


@contextlib.contextmanager
def RemoteExecution(use_goma: bool, use_remoteexec: bool) -> Iterator[None]:
  """A context manager to start goma or remoteexec instance.

  The context manager depending on the input argument will decide to start
  either the goma or remote exec instance.

  Args:
    use_goma: If true, start the goma instance.
    use_remoteexec: If true, start the remoteexec instance.

  Yields:
    Iterator.
  """
  goma_dir = Path(os.environ.get('GOMA_DIR', Path.home() / 'goma'))
  goma_tmp_dir = os.environ.get('GOMA_TMP_DIR')
  goma_service_json = os.environ.get('GOMA_SERVICE_ACCOUNT_JSON_FILE')
  glog_log_dir = os.environ.get('GLOG_log_dir')
  reclient_dir = os.environ.get('RECLIENT_DIR')
  reproxy_cfg_file = os.environ.get('REPROXY_CFG')
  remoteexec_instance = None
  goma_instance = None

  try:
    if use_remoteexec and reclient_dir and reproxy_cfg_file:
      logging.info('Starting RBE reproxy.')
      remoteexec_instance = remoteexec_util.Remoteexec(reclient_dir,
                                                       reproxy_cfg_file)
    elif use_goma:
      logging.info('Starting goma compiler_proxy.')
      goma_instance = goma_lib.Goma(
          goma_dir,
          goma_service_json,
          goma_tmp_dir,
          stage_name='BuildPackages',
          log_dir=glog_log_dir)
  except ValueError:
    logging.warning('Remote execution initialization error.')

  try:
    if remoteexec_instance:
      remoteexec_instance.Start()
    elif goma_instance:
      goma_instance.Restart()
    yield
  finally:
    if remoteexec_instance:
      logging.info('Stopping RBE reproxy.')
      remoteexec_instance.Stop()
    elif goma_instance:
      logging.info('Stopping goma compiler_proxy.')
      goma_instance.Stop()
