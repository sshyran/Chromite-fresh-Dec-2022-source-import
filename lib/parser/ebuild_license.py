# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Parser for ebuild LICENSE settings.

Example values we have to handle:
LICENSE="
  licA
  licB
  flag1? ( licC )
  !flag1? ( licD )
  flag2? ( flag3? ( licE ) )
  || ( licF licG )
  || (
    licH
    flag4? ( licI licJ )
  )
"

Parsed into:
Node
  LicenseNode(licA)
  LicenseNode(licB)
  UseNode(flag1)
    LicenseNode(licC)
  UseNode(!flag1)
    LicenseNode(licD)
  UseNode(flag2)
    UseNode(flag3)
      LicenseNode(licE)
  OrNode
    LicenseNode(licF)
    LicenseNode(licG)
  OrNode
    LicenseNode(licH)
    UseNode(flag4)
      LicenseNode(licI)
      LicenseNode(licJ)
"""

import re
from typing import Callable, List, NamedTuple, Optional


# https://projects.gentoo.org/pms/7/pms.html#x1-220003.1.6
VALID_NAME_RE = re.compile(r"^[A-Za-z0-9+_.-]+$")


class Error(Exception):
    """Base error class for the module."""


class LicenseNameError(Error):
    """A license name is invalid."""


class LicenseSyntaxError(Error):
    """The license syntax is invalid."""


class NestedOrUnsupportedError(Error):
    """Using ||() directly within ||() doesn't make sense."""


def _dedupe_in_order(iterable) -> List:
    """Dedupe elements while maintaining order."""
    # This uses Python dict insertion order that is guaranteed in newer versions.
    return dict((x, None) for x in iterable).keys()


class LicenseNode(NamedTuple):
    """A license."""

    name: str

    def reduce(
        self,
        use_flags: Optional[set] = None,
        or_reduce: Optional[Callable] = None,
    ):  # pylint: disable=unused-argument
        return [self.name]

    def __str__(self):
        return self.name


class Node:
    """A group of license nodes."""

    def __init__(self):
        self.children = []

    def reduce(
        self,
        use_flags: Optional[set] = None,
        or_reduce: Optional[Callable] = None,
    ):
        return list(
            _dedupe_in_order(
                x
                for child in self.children
                for x in child.reduce(use_flags, or_reduce)
            )
        )

    def __str__(self):
        return " ".join(_dedupe_in_order(str(x) for x in self.children))


class OrNode(Node):
    """A group of optional/alternative licenses."""

    def reduce(
        self,
        use_flags: Optional[set] = None,
        or_reduce: Optional[Callable] = None,
    ):
        choices = super().reduce(use_flags, or_reduce)
        if or_reduce:
            return [or_reduce(choices)]
        # Just peel off the first one.
        return choices[:1]

    def __str__(self):
        return f"|| ( {super().__str__()} )"


class UseNode(Node):
    """A conditional node."""

    def __init__(self, flag: str):
        super().__init__()
        self.flag = flag

    def reduce(
        self,
        use_flags: Optional[set] = None,
        or_reduce: Optional[Callable] = None,
    ):
        if use_flags is None:
            use_flags = []

        if self.flag.startswith("!"):
            test = self.flag[1:] not in use_flags
        else:
            test = self.flag in use_flags

        return super().reduce(use_flags, or_reduce) if test else []

    def __str__(self):
        return (
            f"{self.flag}? ( " + " ".join(str(x) for x in self.children) + " )"
        )


def parse(data: str) -> Node:
    """Parse an ebuild license string into a structure."""
    root = Node()
    cur = root
    stack = [root]
    for token in data.split():
        if VALID_NAME_RE.match(token):
            cur.children.append(LicenseNode(token))
        elif token == "||":
            if cur is OrNode:
                # We could support this, but it doesn't make sense in general.
                # (A || (B || C)) is simply (A || B || C).
                raise NestedOrUnsupportedError(
                    f'Redundant nested OR deps are not supported: "{data}"'
                )
            node = OrNode()
            cur.children.append(node)
            stack.append(node)
            cur = node
        elif token == "(":
            if not isinstance(cur, (OrNode, UseNode)):
                raise LicenseSyntaxError(f'Unexpected "(": "{data}"')
        elif token == ")":
            if not isinstance(cur, (OrNode, UseNode)):
                raise LicenseSyntaxError(f'Unexpected ")": "{data}"')
            stack.pop()
            cur = stack[-1]
        elif token.endswith("?"):
            # USE flag conditional.
            node = UseNode(token[:-1])
            cur.children.append(node)
            stack.append(node)
            cur = node
        else:
            raise LicenseNameError(f'Invalid license name: "{token}"')

    # Make sure all '(...)' nodes finished processing.
    if len(stack) != 1:
        raise LicenseSyntaxError(f'Incomplete license: "{data}"')

    return root
