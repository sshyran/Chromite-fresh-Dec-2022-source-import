# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""build_packages updates the set of binary packages needed by Chrome OS.

The build_packages process cross compiles all packages that have been
updated into the given sysroot and builds binary packages as a side-effect.
The output packages will be used by the build_image script to create a
bootable Chrome OS image.

If packages are specified in cli, only build those specific packages and any
dependencies they might need.

For the fastest builds, use --nowithautotest --noworkon.
"""

import argparse
import logging
import os
import urllib.error
import urllib.request
from typing import List, Optional, Tuple

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.service import sysroot


def build_shell_bool_style_args(parser: commandline.ArgumentParser,
                                name: str,
                                default_val: bool,
                                help_str: str,
                                deprecation_note: str,
                                alternate_name: Optional[str] = None) -> None:
  """Build the shell boolean input argument equivalent.

  There are two cases which we will need to handle,
  case 1: A shell boolean arg, which doesn't need to be re-worded in python.
  case 2: A shell boolean arg, which needs to be re-worded in python.
  Example below.
  For Case 1, for a given input arg name 'argA', we create three python
  arguments.
  --argA, --noargA, --no-argA. The arguments --argA and --no-argA will be
  retained after deprecating --noargA.
  For Case 2, for a given input arg name 'arg_A' we need to use alternate
  argument name 'arg-A'. we create four python arguments in this case.
  --arg_A, --noarg_A, --arg-A, --no-arg-A. The first two arguments will be
  deprecated later.
  TODO(b/218522717): Remove the creation of --noargA in case 1 and --arg_A and
  --noarg_A in case 2.

  Args:
    parser: The parser to update.
    name: The input argument name. This will be used as 'dest' variable name.
    default_val: The default value to assign.
    help_str: The help string for the input argument.
    deprecation_note: A deprecation note to use.
    alternate_name: Alternate argument to be used after deprecation.
  """
  arg = f'--{name}'
  shell_narg = f'--no{name}'
  py_narg = f'--no-{name}'
  alt_arg = f'--{alternate_name}' if alternate_name else None
  alt_py_narg = f'--no-{alternate_name}' if alternate_name else None
  default_val_str = f'{help_str} (Default: %(default)s).'

  if alternate_name:
    parser.add_argument(
        alt_arg,
        action='store_true',
        default=default_val,
        dest=name,
        help=default_val_str)
    parser.add_argument(
        alt_py_narg,
        action='store_false',
        dest=name,
        help="Don't " + help_str.lower())

  parser.add_argument(
      arg,
      action='store_true',
      default=default_val,
      dest=name,
      deprecated=deprecation_note % alt_arg if alternate_name else None,
      help=default_val_str if not alternate_name else argparse.SUPPRESS)
  parser.add_argument(
      shell_narg,
      action='store_false',
      dest=name,
      deprecated=deprecation_note %
      (alt_py_narg if alternate_name else py_narg),
      help=argparse.SUPPRESS)

  if not alternate_name:
    parser.add_argument(
        py_narg,
        action='store_false',
        dest=name,
        help="Don't " + help_str.lower())


def get_parser() -> commandline.ArgumentParser:
  """Creates the cmdline argparser, populates the options and description.

  Returns:
    Argument parser.
  """
  deprecation_note = 'Argument will be removed July, 2022. Use %s instead.'
  parser = commandline.ArgumentParser(description=__doc__)

  # TODO(rchandrasekar): Check if the board input is set.
  # Don't proceed if not set.
  parser.add_argument(
      '--board',
      default=cros_build_lib.GetDefaultBoard(),
      help='The board to build packages for.')

  build_shell_bool_style_args(
      parser, 'usepkg', True, 'Use binary packages to bootstrap when possible.',
      deprecation_note)
  build_shell_bool_style_args(
      parser, 'usepkgonly', False,
      'Use binary packages only to bootstrap; abort if any are missing.',
      deprecation_note)
  build_shell_bool_style_args(parser, 'workon', True,
                              'Force-build workon packages.', deprecation_note)
  build_shell_bool_style_args(parser, 'showoutput', False,
                              'Show all output from parallel_emerge.',
                              deprecation_note)
  build_shell_bool_style_args(
      parser, 'withrevdeps', True,
      'Calculate reverse dependencies on changed ebuilds.', deprecation_note)
  build_shell_bool_style_args(
      parser, 'cleanbuild', False,
      'Perform a clean build; delete sysroot if it exists before building.',
      deprecation_note)
  build_shell_bool_style_args(
      parser, 'pretend', False,
      'Pretend building packages, just display which packages would have '
      'been installed.', deprecation_note)

  # The --sysroot flag specifies the environment variables ROOT and PKGDIR.
  # This allows fetching and emerging of all packages to specified sysroot.
  # Note that --sysroot will setup the board normally in /build/$BOARD, if
  # it's not setup yet. It also expects the toolchain to already be installed
  # in the sysroot.
  # --usepkgonly and --norebuild are required, because building is not
  # supported when board_root is set.
  parser.add_argument(
      '--sysroot', type='path', help='Emerge packages to sysroot.')
  parser.add_argument(
      '--board_root',
      type='path',
      dest='sysroot',
      deprecated=deprecation_note % '--sysroot',
      help=argparse.SUPPRESS)

  # CPU Governor related options.
  group = parser.add_argument_group('CPU Governor Options')
  build_shell_bool_style_args(
      group, 'autosetgov', False,
      "Automatically set cpu governor to 'performance'.", deprecation_note)
  build_shell_bool_style_args(
      group,
      'autosetgov_sticky',
      False,
      'Remember --autosetgov setting for future runs.',
      deprecation_note,
      alternate_name='autosetgov-sticky')

  # Chrome building related options.
  group = parser.add_argument_group('Chrome Options')
  build_shell_bool_style_args(
      group,
      'use_any_chrome',
      True,
      "Use any Chrome prebuilt available, even if the prebuilt doesn't "
      'match exactly.',
      deprecation_note,
      alternate_name='use-any-chrome')
  build_shell_bool_style_args(
      group, 'internal', False,
      'Build the internal version of chrome(set the chrome_internal USE flag).',
      deprecation_note)
  build_shell_bool_style_args(
      group, 'chrome', False, 'Ensure chrome instead of chromium. Alias for '
      '--internal --no-use-any-chrome.', deprecation_note)

  # Setup board related options.
  group = parser.add_argument_group('Setup Board Config Options')
  build_shell_bool_style_args(
      group,
      'skip_chroot_upgrade',
      False,
      'Skip the automatic chroot upgrade; use with care.',
      deprecation_note,
      alternate_name='skip-chroot-upgrade')
  build_shell_bool_style_args(
      group,
      'skip_toolchain_update',
      False,
      'Skip automatic toolchain update',
      deprecation_note,
      alternate_name='skip-toolchain-update')
  build_shell_bool_style_args(
      group,
      'skip_setup_board',
      False,
      'Skip running setup_board. Implies '
      '--skip-chroot-upgrade --skip-toolchain-update.',
      deprecation_note,
      alternate_name='skip-setup-board')

  # Image Type selection related options.
  group = parser.add_argument_group('Image Type Options')
  build_shell_bool_style_args(group, 'withdev', True,
                              'Build useful developer friendly utilities.',
                              deprecation_note)
  build_shell_bool_style_args(
      group, 'withdebug', True,
      'Build debug versions of Chromium-OS-specific packages.',
      deprecation_note)
  build_shell_bool_style_args(group, 'withfactory', True,
                              'Build factory installer.', deprecation_note)
  build_shell_bool_style_args(group, 'withtest', True,
                              'Build packages required for testing.',
                              deprecation_note)
  build_shell_bool_style_args(group, 'withautotest', True,
                              'Build autotest client code.', deprecation_note)
  build_shell_bool_style_args(group, 'withdebugsymbols', False,
                              'Install the debug symbols for all packages.',
                              deprecation_note)

  # Advanced Options.
  group = parser.add_argument_group('Advanced Options')
  group.add_argument(
      '--accept-licenses', help='Licenses to append to the accept list.')
  group.add_argument(
      '--accept_licenses',
      deprecated=deprecation_note % '--accept-licenses',
      help=argparse.SUPPRESS)
  build_shell_bool_style_args(group, 'eclean', True,
                              'Run eclean to delete old binpkgs.',
                              deprecation_note)
  group.add_argument(
      '--jobs',
      type=int,
      default=os.cpu_count(),
      help='Number of packages to build in parallel. '
      '(Default: %(default)s)')
  build_shell_bool_style_args(group, 'rebuild', True,
                              'Automatically rebuild dependencies.',
                              deprecation_note)
  # TODO(b/218522717): Remove the --nonorebuild argument support.
  group.add_argument(
      '--nonorebuild',
      action='store_true',
      dest='rebuild',
      deprecated=deprecation_note % '--rebuild',
      help=argparse.SUPPRESS)
  build_shell_bool_style_args(group, 'expandedbinhosts', True,
                              'Allow expanded binhost inheritance.',
                              deprecation_note)
  # The --reuse-pkgs-from-local-boards flag tells Portage to share binary
  # packages between boards that are built locally, so that the total time
  # required to build several boards is reduced. This flag is only useful
  # when you are not able to use remote binary packages, since remote binary
  # packages are usually more up to date than anything you have locally.
  build_shell_bool_style_args(
      group,
      'reuse_pkgs_from_local_boards',
      False,
      'Bootstrap from local packages instead of remote packages.',
      deprecation_note,
      alternate_name='reuse-pkgs-from-local-boards')

  # --run-goma option is designed to be used on bots.
  # If you're trying to build packages with goma in your local dev env, this is
  # *not* the option you're looking for. Please see comments below.
  # This option; 1) starts goma, 2) builds packages (expecting that goma is
  # used), then 3) stops goma explicitly.
  # 4) is a request from the goma team, so that stats/logs can be taken.
  # Note: GOMA_DIR and GOMA_SERVICE_ACCOUNT_JSON_FILE are expected to be passed
  # via env var.
  #
  # In local dev env cases, compiler_proxy is expected to keep running.
  # In such a case;
  #   $ python ${GOMA_DIR}/goma_ctl.py ensure_start
  #   $ ./build_packages (... and options without --run-goma ...)
  # is an expected commandline sequence. If you set --run-goma flag while
  # compiler_proxy is already running, the existing compiler_proxy will be
  # stopped.
  #
  # TODO(rchandrasekar): Use of env variable as input is not right. Added
  # options to provide them as input arguments. Migrate users to use these
  # options and deprecate the '--run-goma' arg.
  build_shell_bool_style_args(
      group,
      'run_goma',
      False,
      'If set to true, (re)starts goma, builds packages, and then stops goma..',
      deprecation_note,
      alternate_name='run-goma')
  group.add_argument('--goma-dir', type='path', help='Goma directory path.')
  group.add_argument(
      '--goma-cfg', type='path', help='Goma service account json file to use.')
  # This option is for building chrome remotely.
  # 1) starts reproxy 2) builds chrome with reproxy and 3) stops reproxy so
  # logs/stats can be collected.
  # Note: RECLIENT_DIR and REPROXY_CFG env var will be deprecated July, 2022.
  # Use --reclient-dir and --reproxy-cfg input options instead.
  #
  # TODO(rchandrasekar): Use of env variable as input is not right. Added
  # options to provide them as input arguments. Migrate users to use these
  # options and deprecate the '--run-remoteexec' arg.
  build_shell_bool_style_args(
      group, 'run_remoteexec', False,
      'If set to true, starts RBE reproxy, builds packages, and then stops '
      'reproxy.', deprecation_note)
  group.add_argument('--reclient-dir', type='path', help='Reproxy client path.')
  group.add_argument(
      '--reproxy-cfg', type='path', help='Reproxy config file to use.')

  parser.add_argument('packages', nargs='*', help='Packages to build.')
  return parser


def parse_args(argv: List[str]) -> Tuple[commandline.ArgumentParser,
                                         commandline.ArgumentNamespace]:
  """Parse and validate CLI arguments.

  Args:
    argv: Arguments passed via CLI.

  Returns:
    Tuple having the below two,
    Argument Parser
    Validated argument namespace.
  """
  parser = get_parser()
  opts = parser.parse_args(argv)

  if opts.chrome:
    opts.internal_chrome = True
    opts.use_any_chrome = False

  opts.build_run_config = sysroot.BuildPackagesRunConfig(
      usepkg=opts.usepkg,
      install_debug_symbols=opts.withdebugsymbols,
      packages=opts.packages,
      use_goma=opts.run_goma,
      use_remoteexec=opts.run_remoteexec,
      incremental_build=opts.withrevdeps,
      expanded_binhosts=opts.expandedbinhosts,
      setup_board=not opts.skip_setup_board,
      dryrun=opts.pretend,
      usepkgonly=opts.usepkgonly,
      workon=opts.workon,
      verbose=opts.showoutput,
      install_auto_test=opts.withautotest,
      autosetgov=opts.autosetgov,
      autosetgov_sticky=opts.autosetgov_sticky,
      use_any_chrome=opts.use_any_chrome,
      internal_chrome=opts.internal,
      clean_build=opts.cleanbuild,
      eclean=opts.eclean,
      rebuild_dep=opts.rebuild,
      accept_licenses=opts.accept_licenses,
      jobs=opts.jobs,
      local_pkg=opts.reuse_pkgs_from_local_boards,
      dev_image=opts.withdev,
      factory_image=opts.withfactory,
      test_image=opts.withtest,
      debug_version=opts.withdebug,
      update_toolchain=not opts.skip_toolchain_update,
      upgrade_chroot=not opts.skip_chroot_upgrade)
  opts.Freeze()
  return parser, opts


def main(argv: Optional[List[str]] = None) -> Optional[int]:
  commandline.RunInsideChroot()
  parser, opts = parse_args(argv)

  # TODO(rchandrasekar): Pass the BuildPackage run config to BuildPackage in
  # sysroot service.
  #
  # If the opts.board is not set, then it means user hasn't specified a default
  # board in 'src/scripts/.default_board' and didn't specify it as input
  # argument.
  if not opts.board:
    parser.error('--board is required')

  cmd = [
      'bash',
      os.path.join(constants.CROSUTILS_DIR, 'build_packages.sh'),
      '--script-is-run-only-by-chromite-and-not-users'
  ]
  cmd.extend(argv)
  try:
    # TODO(b/187793559): Don't pass in print_cmd once we switch to argparse
    cros_build_lib.dbg_run(cmd, print_cmd=False)
  except cros_build_lib.RunCommandError as e:
    try:
      request = urllib.request.urlopen(
          'https://chromiumos-status.appspot.com/current?format=raw')
      logging.notice('Tree Status: %s', request.read().decode())
    except urllib.error.HTTPError:
      pass
    cros_build_lib.Die(e)
