# Copyright 2022 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Use with an IDE to copy a link to the current file/line to your clipboard.

Public and private repos are supported. The internal/public arguments are only
used if the repo is public, private repos always link to the internal code
search.

By default always generates a link to the public code search, but can also
generate links to the internal code search.

Currently only works locally and if using X11.

To allow use over SSH, enable X11 forwarding.
Client side: -X, or add "X11Forwarding yes" to your ~/.ssh/config.
Server side: "X11Forwarding yes" must be in /etc/ssh/sshd_config.

IDE integration instructions. Please add your IDE if it's not listed, or update
the instructions if they're vague or out of date!

For Intellij:
Create a new External Tool (Settings > Tools > External Tools).
Tool Settings:
  Program: ~/chromiumos/chromite/contrib/generate_cs_path
  Arguments: $FilePath$ -l $LineNumber$

For VSCode:
Create a custom task (code.visualstudio.com/docs/editor/tasks#_custom-tasks)
with the command:
  ~/chromiumos/chromite/contrib/generate_cs_path ${file} -l ${lineNumber}
"""

import os
from pathlib import Path
import sys

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import git

# HEAD is the ref for the codesearch repo, not the project itself.
_PUBLIC_CS_BASE = (
    'https://source.chromium.org/chromiumos/chromiumos/codesearch/+/HEAD:')
_INTERNAL_CS_BASE = 'http://cs/chromeos_public/'
_INTERNAL_CS_PRIVATE_BASE = 'http://cs/chromeos_internal/'


def GetParser():
  """Build the argument parser."""
  parser = commandline.ArgumentParser(description=__doc__)

  # Public/internal code search selection arguments.
  type_group = parser.add_mutually_exclusive_group()
  type_group.add_argument(
      '-p',
      '--public',
      dest='public_link',
      action='store_true',
      default=True,
      help='Generate a link to the public code search.')
  type_group.add_argument(
      '-i',
      '--internal',
      dest='public_link',
      action='store_false',
      help='Generate a link to the internal code search.')

  parser.add_argument('-l', '--line', type=int, help='Line number.')

  parser.add_argument(
      '-o',
      '--open',
      action='store_true',
      default=False,
      help='Open the link in a browser rather than copying it to the clipboard.'
  )

  parser.add_argument('path', type='path', help='Path to a file.')

  return parser


def _ParseArguments(argv):
  """Parse and validate arguments."""
  parser = GetParser()
  opts = parser.parse_args(argv)

  opts.path = Path(opts.path).relative_to(constants.SOURCE_ROOT)

  opts.Freeze()
  return opts


def main(argv):
  opts = _ParseArguments(argv)

  checkout = git.ManifestCheckout.Cached(opts.path)

  # Find the project.
  checkout_path = None
  private_repo = False
  for checkout_path, attrs in checkout.checkouts_by_path.items():
    try:
      relative_path = opts.path.relative_to(checkout_path)
    except ValueError:
      continue
    else:
      # Public/private determination.
      private_repo = attrs.get('remote_alias') == 'cros-internal'
      break
  else:
    cros_build_lib.Die('No project found for %s.', opts.path)

  line = f';l={opts.line}' if opts.line else ''

  if private_repo:
    # Private repos not on public CS, so force internal private.
    base = _INTERNAL_CS_PRIVATE_BASE
  elif opts.public_link:
    base = _PUBLIC_CS_BASE
  else:
    base = _INTERNAL_CS_BASE

  cs_str = f'{base}{checkout_path}/{relative_path}{line}'

  is_mac_os = sys.platform.startswith('darwin')

  if opts.open:
    cmd = ['open' if is_mac_os else 'xdg-open', cs_str]
    os.execvp(cmd[0], cmd)
  else:
    cmd = ['pbcopy'] if is_mac_os else ['xsel', '--clipboard', '--input']
    cros_build_lib.run(cmd, input=cs_str)
