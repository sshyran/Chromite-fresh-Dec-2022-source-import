# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run the right formatter on the specified files.

TODO: Support stdin & diffs.
"""

import difflib
import fnmatch
import functools
import itertools
import logging
import os
import re
from typing import Callable, Union

from chromite.cli import command
from chromite.format import formatters
from chromite.lib import osutils
from chromite.lib import parallel
from chromite.utils.parser import shebang


# Map file extensions to a formatter function.
_EXT_TOOL_MAP = {
    frozenset({".bzl"}): (formatters.star.BzlData,),
    frozenset({".c", ".cc", ".cpp", ".cxx", ".h"}): (formatters.cpp.Data,),
    frozenset({".gn", ".gni"}): (formatters.gn.Data,),
    frozenset({".go"}): (formatters.go.Data,),
    frozenset({".json"}): (formatters.json.Data,),
    # TODO(build): Add a formatter for this.
    frozenset({".ebuild", ".eclass"}): (formatters.whitespace.Data,),
    # TODO(build): Add a formatter for this.
    frozenset({".md"}): (formatters.whitespace.Data,),
    # TODO(build): Add a formatter for this (minijail seccomp policies).
    frozenset({".policy"}): (formatters.whitespace.Data,),
    frozenset({".proto"}): (formatters.proto.Data,),
    frozenset({".py"}): (formatters.python.Data,),
    frozenset({".rs"}): (formatters.rust.Data,),
    # TODO(build): Add a formatter for this.
    frozenset({".sh"}): (formatters.whitespace.Data,),
    frozenset({".star"}): (formatters.star.Data,),
    # TODO(build): Add a formatter for this (SELinux policies).
    frozenset({".te"}): (formatters.whitespace.Data,),
    frozenset({".xml"}): (formatters.xml.Data,),
    # TODO(build): Switch .toml to rustfmt when available.
    # https://github.com/rust-lang/rustfmt/issues/4091
    frozenset({".cfg", ".conf", ".ini", ".rules", ".toml", ".txt"}): (
        formatters.whitespace.Data,
    ),
}


# Map known filenames to a tool function.
_FILENAME_PATTERNS_TOOL_MAP = {
    frozenset({".gn"}): (formatters.gn.Data,),
    frozenset({"BUILD", "BUILD.bazel"}): (formatters.star.BuildData,),
    frozenset({"WORKSPACE"}): (formatters.star.WorkspaceData,),
    # These are plain text files.
    frozenset(
        {
            ".clang-format",
            ".gitignore",
            ".gitmodules",
            "COPYING*",
            "LICENSE*",
            "make.defaults",
            "package.accept_keywords",
            "package.force",
            "package.keywords",
            "package.mask",
            "package.provided",
            "package.unmask",
            "package.use",
            "package.use.mask",
        }
    ): (formatters.whitespace.Data,),
    # TODO(build): Add a formatter for this.
    frozenset({"DIR_METADATA"}): (formatters.whitespace.Data,),
    # TODO(build): Add a formatter for this.
    frozenset({"OWNERS*"}): (formatters.whitespace.Data,),
}


# TODO: Move to a centralized configuration somewhere.
_EXCLUDED_FILE_REGEX = (
    # Compiled python protobuf bindings.
    re.compile(r".*_pb2\.py"),
    # Vendored third-party code.
    re.compile(r".*third_party/.*\.py"),
)


def _BreakoutDataByTool(map_to_return, path):
    """Maps a tool method to the content of the |path|."""
    # Detect by content of the file itself.
    try:
        with open(path, "rb") as fp:
            # We read 128 bytes because that's the Linux kernel's current limit.
            # Look for BINPRM_BUF_SIZE in fs/binfmt_script.c.
            data = fp.read(128)

            try:
                result = shebang.parse(data)
            except ValueError:
                # If the file doesn't have a shebang, nothing to do.
                return

            prog = result.command
            if prog == "/usr/bin/env":
                prog = result.args
            basename = os.path.basename(prog)
            if basename.startswith("python") or basename.startswith("vpython"):
                for tool in _EXT_TOOL_MAP[frozenset({".py"})]:
                    map_to_return.setdefault(tool, []).append(path)
            elif basename in ("sh", "dash", "bash"):
                for tool in _EXT_TOOL_MAP[frozenset({".sh"})]:
                    map_to_return.setdefault(tool, []).append(path)
    except IOError as e:
        logging.debug("%s: reading initial data failed: %s", path, e)


def _BreakoutFilesByTool(files):
    """Maps a tool method to the list of files to process."""
    map_to_return = {}

    for f in files:
        # Skip if excluded.
        if any(x.search(f) for x in _EXCLUDED_FILE_REGEX):
            continue

        extension = os.path.splitext(f)[1]
        for extensions, tools in _EXT_TOOL_MAP.items():
            if extension in extensions:
                for tool in tools:
                    map_to_return.setdefault(tool, []).append(f)
                break
        else:
            name = os.path.basename(f)
            for patterns, tools in _FILENAME_PATTERNS_TOOL_MAP.items():
                if any(fnmatch.fnmatch(name, x) for x in patterns):
                    for tool in tools:
                        map_to_return.setdefault(tool, []).append(f)
                    break
            else:
                if os.path.isfile(f):
                    _BreakoutDataByTool(map_to_return, f)

    return map_to_return


def _Dispatcher(
    inplace: bool,
    _debug: bool,
    diff: bool,
    dryrun: bool,
    tool: Callable,
    path: Union[str, os.PathLike],
) -> int:
    """Call |tool| on |path| and take care of coalescing exit codes."""
    old_data = osutils.ReadFile(path)
    new_data = tool(old_data)
    if new_data == old_data:
        return 0

    if dryrun:
        logging.warning("%s: needs formatting", path)
        return 1
    elif diff:
        path = str(path).lstrip("/")
        print(
            "\n".join(
                difflib.unified_diff(
                    old_data.splitlines(),
                    new_data.splitlines(),
                    fromfile=f"a/{path}",
                    tofile=f"b/{path}",
                    fromfiledate="(original)",
                    tofiledate="(formatted)",
                    lineterm="",
                )
            )
        )
        return 1
    elif inplace:
        logging.debug("Updating %s", path)
        osutils.WriteFile(path, new_data)
        return 0
    else:
        print(new_data, end="")
        return 1


@command.command_decorator("format")
class FormatCommand(command.CliCommand):
    """Run the right formatter on the specified files."""

    EPILOG = """
Supported file formats: %s
Supported file names: %s
""" % (
        " ".join(sorted(itertools.chain(*_EXT_TOOL_MAP))),
        " ".join(sorted(itertools.chain(*_FILENAME_PATTERNS_TOOL_MAP))),
    )

    @classmethod
    def AddParser(cls, parser):
        super().AddParser(parser)
        parser.add_argument(
            "-n",
            "--dry-run",
            "--check",
            dest="dryrun",
            action="store_true",
            help="Display unformatted files & exit non-zero",
        )
        parser.add_argument(
            "--diff",
            action="store_true",
            help="Display diff instead of formatted content",
        )
        parser.add_argument(
            "--stdout",
            dest="inplace",
            action="store_false",
            help="Write to stdout",
        )
        parser.add_argument(
            "-i",
            "--inplace",
            default=True,
            action="store_true",
            help="Format files inplace (default)",
        )
        parser.add_argument("files", help="Files to format", nargs="*")

    def Run(self):
        files = self.options.files
        if not files:
            # Running with no arguments is allowed to make the repo upload hook
            # simple, but print a warning so that if someone runs this manually
            # they are aware that nothing was changed.
            logging.warning("No files provided to format.  Doing nothing.")
            return 0

        tool_map = _BreakoutFilesByTool(files)
        dispatcher = functools.partial(
            _Dispatcher,
            self.options.inplace,
            self.options.debug,
            self.options.diff,
            self.options.dryrun,
        )

        # If we filtered out all files, do nothing.
        # Special case one file (or fewer) as it's common -- faster to avoid the
        # parallel startup penalty.
        tasks = []
        for tool, files in tool_map.items():
            tasks.extend([tool, x] for x in files)
        if not tasks:
            logging.warning("No files support formatting.")
            ret = 0
        elif len(tasks) == 1:
            tool, files = next(iter(tool_map.items()))
            ret = dispatcher(tool, files[0])
        else:
            # Run the tool in parallel on the files.
            ret = sum(parallel.RunTasksInProcessPool(dispatcher, tasks))

        return 1 if ret else 0
