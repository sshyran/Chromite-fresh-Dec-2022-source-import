# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""build_image is used to build a Chromium OS image.

Chromium OS comes in many different forms. This script can be used to build
the following:

base - Pristine Chromium OS image. As similar to Chrome OS as possible.
dev [default] - Developer image. Like base but with additional dev packages.
test - Like dev, but with additional test specific packages and can be easily
  used for automated testing using scripts like test_that, etc.
factory_install - Install shim for bootstrapping the factory test process.
  Cannot be built along with any other image.

Examples:

build_image --board=<board> dev test - builds developer and test images.
build_image --board=<board> factory_install - builds a factory install shim.

Note if you want to build an image with custom size partitions, either consider
adding a new disk layout in build_library/legacy_disk_layout.json OR use
adjust-part. Here are a few examples:

adjust-part='STATE:+1G' -- add one GB to the size the stateful partition
adjust-part='ROOT-A:-1G' -- remove one GB from the primary rootfs partition
adjust-part='STATE:=1G' --  make the stateful partition 1 GB
"""

import argparse
import os
from pathlib import Path
from typing import List, Optional, Tuple

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.service import image


def build_shell_bool_style_args(
    parser: commandline.ArgumentParser,
    name: str,
    default_val: bool,
    help_str: str,
    deprecation_note: str,
    alternate_name: Optional[str] = None,
    additional_neg_options: Optional[List[str]] = None) -> None:
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
  TODO(b/232566937): Remove the creation of --noargA in case 1 and --arg_A and
  --noarg_A in case 2.

  Args:
    parser: The parser to update.
    name: The input argument name. This will be used as 'dest' variable name.
    default_val: The default value to assign.
    help_str: The help string for the input argument.
    deprecation_note: A deprecation note to use.
    alternate_name: Alternate argument to be used after deprecation.
    additional_neg_options: Additional negative alias options to use.
  """
  arg = f'--{name}'
  shell_narg = f'--no{name}'
  py_narg = f'--no-{name}'
  alt_arg = f'--{alternate_name}' if alternate_name else None
  alt_py_narg = f'--no-{alternate_name}' if alternate_name else None
  default_val_str = f'{help_str} (Default: %(default)s).'

  if alternate_name:
    _alternate_narg_list = [alt_py_narg]
    if additional_neg_options:
      _alternate_narg_list.extend(additional_neg_options)

    parser.add_argument(
        alt_arg,
        action='store_true',
        default=default_val,
        dest=name,
        help=default_val_str)
    parser.add_argument(
        *_alternate_narg_list,
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
    _py_narg_list = [py_narg]
    if additional_neg_options:
      _py_narg_list.extend(additional_neg_options)

    parser.add_argument(
        *_py_narg_list,
        action='store_false',
        dest=name,
        help="Don't " + help_str.lower())


def build_shell_string_style_args(parser: commandline.ArgumentParser, name: str,
                                  default_val: Optional[str], help_str: str,
                                  deprecation_note: str,
                                  alternate_name: str) -> None:
  """Build the shell string input argument equivalent.

  Args:
    parser: The parser to update.
    name: The input argument name. This will be used as 'dest' variable name.
    default_val: The default value to assign.
    help_str: The help string for the input argument.
    deprecation_note: A deprecation note to use.
    alternate_name: Alternate argument to be used after deprecation.
  """
  default_val_str = (f'{help_str} (Default: %(default)s).'
                     if default_val else help_str)

  parser.add_argument(
      f'--{alternate_name}',
      dest=f'{name}',
      default=default_val,
      help=default_val_str)
  parser.add_argument(
      f'--{name}',
      deprecated=deprecation_note % f'--{alternate_name}',
      help=argparse.SUPPRESS)


def get_parser() -> commandline.ArgumentParser:
  """Creates the cmdline argparser, populates the options and description.

  Returns:
    Argument parser.
  """
  deprecation_note = 'Argument will be removed January, 2023. Use %s instead.'
  parser = commandline.ArgumentParser(description=__doc__)

  parser.add_argument(
      '-b',
      '--board',
      '--build-target',
      dest='board',
      default=cros_build_lib.GetDefaultBoard(),
      help='The board to build images for.')
  build_shell_string_style_args(
      parser, 'adjust_part', None,
      'Adjustments to apply to partition table (LABEL:[+-=]SIZE) '
      'e.g. ROOT-A:+1G.', deprecation_note, 'adjust-partition')
  build_shell_string_style_args(
      parser, 'output_root',
      Path(constants.DEFAULT_BUILD_ROOT) / 'images',
      'Directory in which to place image result directories '
      '(named by version).', deprecation_note, 'output-root')
  build_shell_string_style_args(
      parser, 'builder_path', None,
      'The build name to be installed on DUT during hwtest.', deprecation_note,
      'builder-path')
  build_shell_string_style_args(parser, 'disk_layout', 'default',
                                'The disk layout type to use for this image.',
                                deprecation_note, 'disk-layout')

  # Kernel related options.
  group = parser.add_argument_group('Kernel Options')
  build_shell_string_style_args(
      group, 'enable_serial', None,
      'Enable serial port for printks. Example values: ttyS0.',
      deprecation_note, 'enable-serial')
  group.add_argument(
      '--kernel-loglevel',
      type=int,
      default=7,
      help='The loglevel to add to the kernel command line. '
      '(Default: %(default)s).')
  group.add_argument(
      '--loglevel',
      dest='kernel_loglevel',
      type=int,
      deprecated=deprecation_note % 'kernel-loglevel',
      help=argparse.SUPPRESS)

  # Bootloader related options.
  group = parser.add_argument_group('Bootloader Options')
  build_shell_string_style_args(
      group, 'boot_args', 'noinitrd',
      'Additional boot arguments to pass to the commandline.', deprecation_note,
      'boot-args')
  build_shell_bool_style_args(group, 'enable_bootcache', False,
                              'Make all bootloaders to use boot cache.',
                              deprecation_note, 'enable-bootcache')
  build_shell_bool_style_args(
      group, 'enable_rootfs_verification', True,
      'Make all bootloaders to use kernel based root-fs integrity checking.',
      deprecation_note, 'enable-rootfs-verification', ['-r'])

  # Advanced options.
  group = parser.add_argument_group('Advanced Options')
  group.add_argument(
      '--build-attempt',
      type=int,
      default=1,
      help='The build attempt for this image build. (Default: %(default)s).')
  group.add_argument(
      '--build_attempt',
      type=int,
      deprecated=deprecation_note % 'build-attempt',
      help=argparse.SUPPRESS)
  build_shell_string_style_args(
      group, 'build_root',
      Path(constants.DEFAULT_BUILD_ROOT) / 'images',
      'Directory in which to compose the image, before copying it to '
      'output_root.', deprecation_note, 'build-root')
  group.add_argument(
      '-j',
      '--jobs',
      dest='jobs',
      type=int,
      default=os.cpu_count(),
      help='Number of packages to build in parallel at maximum. '
      '(Default: %(default)s).')
  build_shell_bool_style_args(group, 'replace', False,
                              'Overwrite existing output, if any.',
                              deprecation_note)
  group.add_argument(
      '--symlink',
      default='latest',
      help='Symlink name to use for this image. (Default: %(default)s).')
  group.add_argument(
      '--version',
      default=None,
      help='Overrides version number in name to this version.')
  build_shell_string_style_args(group, 'output_suffix', None,
                                'Add custom suffix to output directory.',
                                deprecation_note, 'output-suffix')
  group.add_argument(
      '--eclean',
      action='store_true',
      default=True,
      dest='eclean',
      deprecated=('eclean is being removed from build_images. Argument will be '
                  'removed January, 2023.'),
      help=argparse.SUPPRESS)
  group.add_argument(
      '--noeclean',
      action='store_false',
      dest='eclean',
      deprecated=('eclean is being removed from build_images. Argument will be '
                  'removed January, 2023.'),
      help=argparse.SUPPRESS)
  group.add_argument(
      '--no-eclean',
      action='store_false',
      dest='eclean',
      deprecated=('eclean is being removed from build_images. Argument will be '
                  'removed January, 2023.'),
      help=argparse.SUPPRESS)

  parser.add_argument(
      'images',
      nargs='*',
      default=['dev'],
      help='list of images to build. (Default: %(default)s).')

  return parser


def parse_args(
    argv: List[str]
) -> Tuple[commandline.ArgumentParser, commandline.ArgumentNamespace]:
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

  opts.build_run_config = image.BuildConfig(
      adjust_partition=opts.adjust_part,
      output_root=opts.output_root,
      builder_path=opts.builder_path,
      disk_layout=opts.disk_layout,
      enable_serial=opts.enable_serial,
      kernel_loglevel=opts.kernel_loglevel,
      boot_args=opts.boot_args,
      enable_bootcache=opts.enable_bootcache,
      enable_rootfs_verification=opts.enable_rootfs_verification,
      build_attempt=opts.build_attempt,
      build_root=opts.build_root,
      jobs=opts.jobs,
      replace=opts.replace,
      symlink=opts.symlink,
      version=opts.version,
      output_dir_suffix=opts.output_suffix,
  )
  opts.Freeze()

  return parser, opts


def main(argv: Optional[List[str]] = None) -> Optional[int]:
  commandline.RunInsideChroot()
  parser, opts = parse_args(argv)

  # If the opts.board is not set, then it means user hasn't specified a default
  # board in 'src/scripts/.default_board' and didn't specify it as input
  # argument.
  if not opts.board:
    parser.error('--board is required')

  invalid_image = [
      x for x in opts.images if x not in constants.IMAGE_TYPE_TO_NAME
  ]
  if invalid_image:
    parser.error(f'Invalid image type argument(s) {invalid_image}')

  result = image.Build(opts.board, opts.images, opts.build_run_config)
  if result.run_error:
    cros_build_lib.Die(
        f'Error running build_image. Exit Code : {result.return_code}')
