# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# TODO: Support cleaning /build/*/tmp.
# TODO: Support running `eclean -q packages` on / and the sysroots.
# TODO: Support cleaning sysroots as a destructive option.

"""Clean up working files in a Chromium OS checkout.

If unsure, just use the --safe flag to clean out various objects.
"""

import errno
import glob
import logging
import os

from chromite.cli import command
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import dev_server_wrapper
from chromite.lib import osutils
from chromite.utils import pformat
from chromite.utils import timer


@command.command_decorator('clean')
class CleanCommand(command.CliCommand):
  """Clean up working files from the build."""

  @classmethod
  def AddParser(cls, parser):
    """Add parser arguments."""
    super(CleanCommand, cls).AddParser(parser)

    parser.add_argument(
        '--safe',
        default=False,
        action='store_true',
        help='Clean up files that are automatically created.')
    parser.add_argument(
        '-n',
        '--dry-run',
        default=False,
        action='store_true',
        help='Show which paths would be cleaned up.')

    group = parser.add_argument_group(
        'Cache Selection (Advanced)',
        description='Clean out specific caches (--safe does all of these).')
    group.add_argument(
        '--cache',
        default=False,
        action='store_true',
        help='Clean up our shared cache dir.')
    group.add_argument(
        '--chromite',
        default=False,
        action='store_true',
        help='Clean up chromite working directories.')
    group.add_argument(
        '--deploy',
        default=False,
        action='store_true',
        help='Clean files cached by cros deploy.')
    group.add_argument(
        '--flash',
        default=False,
        action='store_true',
        help='Clean files cached by cros flash.')
    group.add_argument(
        '--images',
        default=False,
        action='store_true',
        help='Clean up locally generated images.')
    group.add_argument(
        '--incrementals',
        default=False,
        action='store_true',
        help='Clean up incremental package objects.')
    group.add_argument(
        '--logs',
        default=False,
        action='store_true',
        help='Clean up various build log files.')
    group.add_argument(
        '--workdirs',
        default=False,
        action='store_true',
        help='Clean up build various package build directories.')
    group.add_argument(
        '--chroot-tmp',
        default=False,
        action='store_true',
        help="Empty the chroot's /tmp directory.")

    group = parser.add_argument_group(
        'Unrecoverable Options (Dangerous)',
        description='Clean out objects that cannot be recovered easily.')
    group.add_argument(
        '--clobber',
        default=False,
        action='store_true',
        help='Delete all non-source objects.')
    group.add_argument(
        '--chroot',
        default=False,
        action='store_true',
        help='Delete build chroot (affects all boards).')
    group.add_argument(
        '--board', action='append', help='Delete board(s) sysroot(s).')
    group.add_argument(
        '--sysroots',
        default=False,
        action='store_true',
        help='Delete ALL of the sysroots. This is the same as calling with '
             '--board with every board that has been built.')
    group.add_argument(
        '--autotest',
        default=False,
        action='store_true',
        help='Delete build_externals packages.')

    group = parser.add_argument_group(
        'Advanced Customization',
        description='Advanced options that are rarely needed.')
    group.add_argument(
        '--sdk-path',
        type='path',
        default=constants.DEFAULT_CHROOT_PATH,
        help='The sdk (chroot) path. This only needs to be provided if your '
             'chroot is not in the default location.')

  def __init__(self, options):
    """Initializes cros clean."""
    command.CliCommand.__init__(self, options)

  @classmethod
  def ProcessOptions(cls, parser, options):
    """Post process options."""
    # If no option is set, default to "--safe".
    if not (options.autotest or
            options.board or
            options.cache or
            options.chromite or
            options.chroot or
            options.chroot_tmp or
            options.clobber or
            options.deploy or
            options.flash or
            options.images or
            options.incrementals or
            options.logs or
            options.safe or
            options.sysroots or
            options.workdirs):
      options.safe = True

    if options.clobber:
      options.chroot = True
      options.autotest = True
      options.safe = True

    if options.safe:
      options.cache = True
      options.chromite = True
      options.chroot_tmp = True
      options.deploy = True
      options.flash = True
      options.images = True
      options.incrementals = True
      options.logs = True
      options.workdirs = True

  @timer.timed('Cros Clean', logging.debug)
  def Run(self):
    """Perform the cros clean command."""
    chroot_dir = self.options.sdk_path

    cros_build_lib.AssertOutsideChroot()

    total_size = 0

    def _GetSize(path):
      """Calculate human size used by |path|."""
      nonlocal total_size
      result = cros_build_lib.dbg_run(['du', '--bytes', '--summarize', path],
                                      check=False, capture_output=True,
                                      encoding='utf-8')
      size = int(result.stdout.split()[0])
      total_size += size
      return pformat.size(size)

    def _LogClean(path):
      if not os.path.exists(path):
        return
      logging.notice('would have cleaned: %s (%s)', path, _GetSize(path))

    def Clean(path):
      """Helper wrapper for the dry-run checks"""
      if self.options.dry_run:
        _LogClean(path)
      else:
        osutils.RmDir(path, ignore_missing=True, sudo=True)

    def Empty(path):
      """Helper wrapper for the dry-run checks"""
      if self.options.dry_run:
        if os.path.exists(path):
          logging.notice('would have emptied: %s (%s)', path, _GetSize(path))
      else:
        osutils.EmptyDir(path, ignore_missing=True, sudo=True)

    def CleanNoBindMount(path):
      # This test is a convenience for developers that bind mount these dirs.
      if not os.path.ismount(path):
        Clean(path)
      else:
        logging.debug('Ignoring bind mounted dir: %s', path)

    # Delete this first since many of the caches below live in the chroot.
    if self.options.chroot:
      logging.debug('Remove the chroot.')
      if self.options.dry_run:
        logging.notice('would have cleaned: %s', chroot_dir)
      else:
        with timer.timer('Remove the chroot', logging.debug):
          cros_build_lib.run(['cros_sdk', '--delete'])

    boards = self.options.board or []
    if self.options.sysroots:
      try:
        boards = os.listdir(os.path.join(chroot_dir, 'build'))
      except OSError as e:
        if e.errno != errno.ENOENT:
          raise
    if boards:
      with timer.timer('Clean Sysroots', logging.debug):
        for b in boards:
          logging.debug('Clean up the %s sysroot.', b)
          with timer.timer(f'Clean up the {b} sysroot.', logging.debug):
            Clean(os.path.join(chroot_dir, 'build', b))

    if self.options.chroot_tmp:
      logging.debug('Empty chroot tmp directory.')
      with timer.timer('Empty chroot tmp directory', logging.debug):
        Empty(os.path.join(chroot_dir, 'tmp'))

    if self.options.cache:
      logging.debug('Clean the common cache.')
      with timer.timer('Clean the common cache', logging.debug):
        CleanNoBindMount(self.options.cache_dir)

      # Recreate dirs that cros_sdk does when entering.
      # TODO: When sdk_lib/enter_chroot.sh is moved to chromite, we should unify
      # with those code paths.
      if not self.options.dry_run:
        distfiles_dir = os.path.join(self.options.cache_dir, 'distfiles')
        osutils.SafeMakedirs(distfiles_dir)
        os.chmod(distfiles_dir, 0o2775)

        # The host & target subdirs aren't used anymore since we unified them,
        # but if the cache is shared with older branches, we don't want to have
        # files duplicated in them.  The unification happened in Jul 2020 for
        # 13360.0.0+ / R86+, so we can prob drop this logic ~Jul 2028?
        for subdir in ('host', 'target'):
          subdir = os.path.join(distfiles_dir, subdir)
          # Recreate the path if it isn't a symlink.
          if not os.path.islink(subdir):
            osutils.RmDir(subdir, ignore_missing=True, sudo=True)
            # Have the subdirs point to the common (parent) dir.
            os.symlink('.', subdir)

        ccache_dir = os.path.join(distfiles_dir, 'ccache')
        osutils.SafeMakedirs(ccache_dir)
        os.chmod(ccache_dir, 0o2775)

    if self.options.chromite:
      logging.debug('Clean chromite workdirs.')
      with timer.timer('Clean chromite workdirs', logging.debug):
        Clean(os.path.join(constants.CHROMITE_DIR, 'venv', 'venv'))
        Clean(os.path.join(constants.CHROMITE_DIR, 'venv', '.venv_lock'))

    if self.options.deploy:
      logging.debug('Clean up the cros deploy cache.')
      with timer.timer('Clean up the cros deploy cache', logging.debug):
        for subdir in ('custom-packages', 'gmerge-packages'):
          for d in glob.glob(os.path.join(chroot_dir, 'build', '*', subdir)):
            Clean(d)

    if self.options.flash:
      if self.options.dry_run:
        _LogClean(dev_server_wrapper.DEFAULT_STATIC_DIR)
      else:
        with timer.timer(dev_server_wrapper.DEFAULT_STATIC_DIR, logging.debug):
          dev_server_wrapper.DevServerWrapper.WipeStaticDirectory()

    if self.options.images:
      logging.debug('Clean the images cache.')
      cache_dir = os.path.join(constants.SOURCE_ROOT, 'src', 'build')
      with timer.timer('Clean the images cache', logging.debug):
        CleanNoBindMount(cache_dir)

    if self.options.incrementals:
      logging.debug('Clean package incremental objects.')
      with timer.timer('Clean package incremental objects', logging.debug):
        Empty(os.path.join(chroot_dir, 'var', 'cache', 'portage'))
        for d in glob.glob(
            os.path.join(chroot_dir, 'build', '*', 'var', 'cache', 'portage')):
          Empty(d)
        for d in glob.glob(
            os.path.join(chroot_dir, 'var', 'cache', 'chromeos-chrome', '*',
                         'src', 'out_*')):
          Clean(d)

    if self.options.logs:
      logging.debug('Clean log files.')
      with timer.timer('Clean log files', logging.debug):
        Empty(os.path.join(chroot_dir, 'var', 'log'))
        for d in glob.glob(
            os.path.join(chroot_dir, 'build', '*', 'tmp', 'portage', 'logs')):
          Empty(d)

    if self.options.workdirs:
      logging.debug('Clean package workdirs.')
      with timer.timer('Clean package workdirs', logging.debug):
        Clean(os.path.join(chroot_dir, 'var', 'tmp', 'portage'))
        Clean(os.path.join(constants.CHROMITE_DIR, 'venv', 'venv'))
        for d in glob.glob(
            os.path.join(chroot_dir, 'build', '*', 'tmp', 'portage')):
          Clean(d)

    if self.options.autotest:
      logging.debug('Clean build_externals.')
      with timer.timer('Clean build_externals', logging.debug):
        packages_dir = os.path.join(constants.SOURCE_ROOT, 'src', 'third_party',
                                    'autotest', 'files', 'site-packages')
        Clean(packages_dir)

    if total_size:
      logging.notice('Freed %s (apparent) space', pformat.size(total_size))
