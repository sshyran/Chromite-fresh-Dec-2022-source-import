# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This script moves ebuilds between 'stable' and 'live' states.

By default 'stable' ebuilds point at and build from source at the
last known good commit. Moving an ebuild to 'live' (via cros_workon start)
is intended to support development. The current source tip is fetched,
source modified and built using the unstable 'live' (9999) ebuild.
"""

from chromite.cli import command
from chromite.lib import build_target_lib
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import terminal
from chromite.lib import workon_helper


# These would preferably be class attributes, but it's difficult to make class
# attributes refer to each other with nested generators in class declarations.
_ACTIONS = (
    ('start', 'Moves an ebuild to live (intended to support development)'),
    ('stop', 'Moves an ebuild to stable (use last known good)'),
    ('info', 'Print package name, repo name, and source directory.'),
    ('list', 'List of live ebuilds (workon ebuilds if --all)'),
    ('list-all', 'List all of the live ebuilds for all setup boards'),
    ('iterate', 'For each ebuild, cd to the source dir and run a command'),
)

# Formatting for the "Actions" epilog section.
_fill = max(len(a[0]) for a in _ACTIONS) + 3
_action_epilog = '\n'.join(
    '  %s%s' % (a[0].ljust(_fill, ' '), a[1]) for a in _ACTIONS)


@command.CommandDecorator('workon')
class WorkonCommand(command.CliCommand):
  """Forces rebuilds of worked on packages from the local source."""

  EPILOG = f"""
Actions:
{_action_epilog}

Examples:
  There is some support for automatically locating ebuilds. The following two
  commands are equivalent.
    cros workon start chromeos-base/authpolicy --build-target eve
    cros workon start authpolicy -b eve

  Start working on a package (always build from source):
    cros workon start authpolicy -b eve

  Stop working on a package (use last known good version):
    cros workon stop authpolicy -b eve

  Stop working on all packages for a build target:
    cros workon stop --all -b eve

  Due to argparse limitations, the positional arguments must be together.
  Currently, the following will not parse correctly:
    cros workon stop -b eve authpolicy
"""

  @classmethod
  def AddParser(cls, parser: commandline.ArgumentParser):
    """Build the parser.

    Args:
      parser: The parser.
    """
    super().AddParser(parser)

    # The current argparse limitations mean we cannot correctly parse all
    # variations of the arguments, currently the positional arguments must
    # be listed together, e.g. `cros workon start -b eve package` will
    # not parse as you might expect. This has been addressed in python
    # 3.7 with intermixed parsing (ArgumentParse.parse_intermixed_args).
    # See: https://docs.python.org/3/library/argparse.html#intermixed-parsing
    # TODO: Add support for intermixed parsing when we are on 3.7.
    parser.add_argument(
        'action', choices=[a[0] for a in _ACTIONS], help='Action to run.')
    parser.add_argument(
        'packages', nargs='*', help='The packages to run the action against.')

    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument(
        '-b',
        '--board',
        '--build-target',
        dest='build_target_name',
        help='The name of the build target whose package is being worked on.')
    target_group.add_argument(
        '--host',
        default=False,
        action='store_true',
        help='Use the host (sdk) instead of a build target.')

    parser.add_argument(
        '--command',
        default='git status',
        dest='iterate_command',
        help='The command to be run by iterate.')

    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        '--workon_only',
        default=False,
        action='store_true',
        help='Apply to packages that have a workon ebuild only.')
    filter_group.add_argument(
        '--all',
        default=False,
        action='store_true',
        help='Apply to all possible packages for the given command.')

    return parser

  def Run(self):
    if self.options.build_target_name:
      self.options.build_target = build_target_lib.BuildTarget(
          self.options.build_target_name)
    else:
      self.options.build_target = None

    self.options.Freeze()

    has_target = self.options.host or self.options.build_target
    needs_target = self.options.action != 'list-all'
    if needs_target and not has_target:
      cros_build_lib.Die(f'{self.options.action} requires a build target or '
                         'specifying the host.')

    commandline.RunInsideChroot(self)

    if self.options.action == 'list-all':
      build_target_to_packages = workon_helper.ListAllWorkedOnAtoms()
      color = terminal.Color()
      for build_target_name in sorted(build_target_to_packages):
        print(color.Start(color.GREEN) + build_target_name + ':' + color.Stop())
        for package in build_target_to_packages[build_target_name]:
          print('    ' + package)
        print('')
      return 0

    if self.options.build_target:
      target = self.options.build_target.name
      sysroot = self.options.build_target.root
    else:
      target = 'host'
      sysroot = '/'

    helper = workon_helper.WorkonHelper(sysroot, target)
    try:
      if self.options.action == 'start':
        helper.StartWorkingOnPackages(
            self.options.packages,
            use_all=self.options.all,
            use_workon_only=self.options.workon_only)
      elif self.options.action == 'stop':
        helper.StopWorkingOnPackages(
            self.options.packages,
            use_all=self.options.all,
            use_workon_only=self.options.workon_only)
      elif self.options.action == 'info':
        triples = helper.GetPackageInfo(
            self.options.packages,
            use_all=self.options.all,
            use_workon_only=self.options.workon_only)
        for package, repos, paths in triples:
          print(package, ','.join(repos), ','.join(paths))
      elif self.options.action == 'list':
        packages = helper.ListAtoms(
            use_all=self.options.all, use_workon_only=self.options.workon_only)
        if packages:
          print('\n'.join(packages))
      elif self.options.action == 'iterate':
        helper.RunCommandInPackages(
            self.options.packages,
            self.options.iterate_command,
            use_all=self.options.all,
            use_workon_only=self.options.workon_only)
      else:
        cros_build_lib.Die(f'No implementation for {self.options.action}')
    except workon_helper.WorkonError as e:
      cros_build_lib.Die(e)
    return 0
