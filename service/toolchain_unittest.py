# Copyright 2022 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Toolchain service tests."""


from collections import defaultdict
import os
from typing import Dict, List, NamedTuple, Text

from chromite.lib import cros_test_lib
from chromite.service import toolchain


class MockArtifact(NamedTuple):
    """Data for a Mocked Artifact."""

    linter: Text
    package: Text
    file_name: Text
    contents: Text


class MockBuildLinter(toolchain.BuildLinter):
    """Mocked version of Build Linters class."""

    def __init__(self, tempdir: Text, packages: List[Text] = None):
        super().__init__([], "")
        self.tempdir = tempdir
        self.packages = [] if packages is None else packages
        self.package_atoms = packages

        self.artifacts = defaultdict(lambda: defaultdict(list))
        self.artifacts_base = os.path.join(self.tempdir, "artifacts")

    def add_artifact(self, artifact: MockArtifact):
        """Adds a mock artifact and writes it to tempdir."""
        tmp_path = os.path.join(
            self.artifacts_base,
            artifact.linter,
            artifact.package,
            artifact.file_name,
        )

        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
        with open(tmp_path, "w") as tmp_artifact_file:
            tmp_artifact_file.write(artifact.contents)
        self.artifacts[artifact.linter][artifact.package].append(tmp_path)

    def _fetch_from_linting_artifacts(self, subdir) -> Dict[Text, List[Text]]:
        """Get file from emerge artifact directory."""
        artifacts = {}
        for package, package_artifacts in self.artifacts[subdir].items():
            if not self.packages or package in self.package_atoms:
                if package not in artifacts:
                    artifacts[package] = []
                artifacts[package].extend(package_artifacts)
        return artifacts


class BuildLinterTests(cros_test_lib.MockTempDirTestCase):
    """Unit tests for Build Linter Class."""

    def checkArtifacts(
        self,
        expected_artifacts: List[MockArtifact],
        retrieved_artifact_paths: Dict[Text, List[Text]],
    ):
        """Asserts that artifact paths match the list of expected results."""

        actual_artifacts = []
        for paths in retrieved_artifact_paths.values():
            actual_artifacts.extend(paths)
        self.assertEqual(len(actual_artifacts), len(expected_artifacts))

        for artifact in expected_artifacts:
            for artifact_path in retrieved_artifact_paths:
                if artifact_path.endswith(
                    f"{artifact.linter}/{artifact.package}/{artifact.file_name}"
                ):
                    with open(artifact_path, "r") as artifact_file:
                        contents = artifact_file.read()
                    self.assertEqual(contents, artifact.contents)

    def testMockBuildLinter(self):
        mbl = MockBuildLinter(self.tempdir, ["pkg_1", "pkg_2", "pkg_3"])
        relevant_artifacts = [
            MockArtifact("linter_1", "pkg_1", "out.txt", "Hello world"),
            MockArtifact("linter_1", "pkg_2", "out2.txt", "Hello world 2"),
            MockArtifact("linter_1", "pkg_3", "out.txt", "Hello\nWorld"),
        ]
        irrelevant_artifacts = [
            MockArtifact("linter_2", "pkg_2", "out.txt", "Goodbye World"),
            MockArtifact("linter_1", "pkg_4", "out.txt", "Goodbye world"),
            MockArtifact("linter_2", "pkg_5", "out.txt", "Goodbye world 2"),
            MockArtifact("linter_3", "pkg_6", "out.txt", "Goodbye\nWorld"),
            MockArtifact("linter_4", "pkg_1", "out.txt", "Goodbye\nWorld"),
        ]
        for artifact in relevant_artifacts + irrelevant_artifacts:
            mbl.add_artifact(artifact)

        # pylint: disable=protected-access
        retrieved_artifact_paths = mbl._fetch_from_linting_artifacts("linter_1")

        self.checkArtifacts(relevant_artifacts, retrieved_artifact_paths)

    def testMockBuildLinterNoPackages(self):
        mbl = MockBuildLinter(self.tempdir, [])
        relevant_artifacts = [
            MockArtifact("linter_1", "pkg_1", "out.txt", "Hello world"),
            MockArtifact("linter_1", "pkg_2", "out2.txt", "Hello world 2"),
            MockArtifact("linter_1", "pkg_3", "out.txt", "Hello\nWorld"),
            MockArtifact("linter_1", "pkg_4", "out.txt", "Hello world"),
        ]
        irrelevant_artifacts = [
            MockArtifact("linter_2", "pkg_2", "out.txt", "Goodbye World"),
            MockArtifact("linter_2", "pkg_5", "out.txt", "Goodbye world 2"),
            MockArtifact("linter_3", "pkg_6", "out.txt", "Goodbye\nWorld"),
            MockArtifact("linter_4", "pkg_1", "out.txt", "Goodbye\nWorld"),
        ]
        for artifact in relevant_artifacts + irrelevant_artifacts:
            mbl.add_artifact(artifact)

        # pylint: disable=protected-access
        retrieved_artifact_paths = mbl._fetch_from_linting_artifacts("linter_1")

        self.checkArtifacts(relevant_artifacts, retrieved_artifact_paths)

    def testParseIWYUFiles(self):
        mbl = MockBuildLinter(self.tempdir)

        artifacts = [
            MockArtifact(
                "iwyu",
                "pkg",
                "iwyu.out",
                (
                    "\n".join(
                        [
                            "(/a/good/file.c has correct #includes/fwd-decls)",
                            "",
                            "/path/to/some/file.c should add these lines:",
                            "#include <missing1.h>  // for func1, func2, func3",
                            "#include <missing2.h>  // for func4, func5, func6",
                            "",
                            "/path/to/some/file.c should remove these lines:",
                            "- #include <unwanted.h>  // lines 11-11",
                            "",
                            "The full include-list for /path/to/some/file.c:",
                            "#include <missing1.h>  // for func1, func2, func3",
                            "#include <missing2.h>  // for func4, func5, func6",
                            "#include <stdint.h>",
                            "#include <stdlib.h>",
                            '#include "lib/foo.h"  // for func7, func8',
                            "---",
                        ]
                    )
                ),
            ),
            MockArtifact(
                "iwyu",
                "pkg",
                "duplicate.out",
                (
                    "\n".join(
                        [
                            "/path/to/some/file.c should add these lines:",
                            "#include <missing1.h>  // for func1, func2, func3",
                            "#include <missing2.h>  // for func4, func5, func6",
                            "",
                            "/path/to/some/file.c should remove these lines:",
                            "- #include <unwanted.h>  // lines 11-11",
                            "",
                            "The full include-list for /path/to/some/file.c:",
                            "#include <missing1.h>  // for func1, func2, func3",
                            "#include <missing2.h>  // for func4, func5, func6",
                            "#include <stdint.h>",
                            "#include <stdlib.h>",
                            '#include "lib/foo.h"  // for func7, func8',
                            "---",
                        ]
                    )
                ),
            ),
            MockArtifact("IWYU", "pkg", "empty.out", ""),
        ]

        expected_findings = [
            toolchain.LinterFinding(
                name="add",
                message="\n".join(
                    [
                        "Include list is missing:",
                        "\t#include <missing1.h>",
                        "Which is required for func1, func2, func3",
                        "",
                        "The full suggested include-list for this file:",
                        "#include <missing1.h>  // for func1, func2, func3",
                        "#include <missing2.h>  // for func4, func5, func6",
                        "#include <stdint.h>",
                        "#include <stdlib.h>",
                        '#include "lib/foo.h"  // for func7, func8',
                        "",
                        "Note: Suggestions from IWYU are not always correct and"
                        " thus require human supervision.",
                    ]
                ),
                locations=(
                    toolchain.CodeLocation(
                        "/path/to/some/file.c",
                        "",
                        line_start=1,
                        line_end=1,
                        col_start=None,
                        col_end=None,
                    ),
                ),
                linter="iwyu",
                suggested_fixes=tuple(),
            ),
            toolchain.LinterFinding(
                name="add",
                message="\n".join(
                    [
                        "Include list is missing:",
                        "\t#include <missing2.h>",
                        "Which is required for func4, func5, func6",
                        "",
                        "The full suggested include-list for this file:",
                        "#include <missing1.h>  // for func1, func2, func3",
                        "#include <missing2.h>  // for func4, func5, func6",
                        "#include <stdint.h>",
                        "#include <stdlib.h>",
                        '#include "lib/foo.h"  // for func7, func8',
                        "",
                        "Note: Suggestions from IWYU are not always correct and"
                        " thus require human supervision.",
                    ]
                ),
                locations=(
                    toolchain.CodeLocation(
                        "/path/to/some/file.c",
                        "",
                        line_start=1,
                        line_end=1,
                        col_start=None,
                        col_end=None,
                    ),
                ),
                linter="iwyu",
                suggested_fixes=tuple(),
            ),
            toolchain.LinterFinding(
                name="remove",
                message="\n".join(
                    [
                        "Remove from include list:",
                        "\t#include <unwanted.h>",
                        "",
                        "The full suggested include-list for this file:",
                        "#include <missing1.h>  // for func1, func2, func3",
                        "#include <missing2.h>  // for func4, func5, func6",
                        "#include <stdint.h>",
                        "#include <stdlib.h>",
                        '#include "lib/foo.h"  // for func7, func8',
                        "",
                        "Note: Suggestions from IWYU are not always correct and"
                        " thus require human supervision.",
                    ]
                ),
                locations=(
                    toolchain.CodeLocation(
                        "/path/to/some/file.c",
                        "",
                        line_start=11,
                        line_end=11,
                        col_start=None,
                        col_end=None,
                    ),
                ),
                linter="iwyu",
                suggested_fixes=tuple(),
            ),
        ]

        for artifact in artifacts:
            mbl.add_artifact(artifact)

        # pylint: disable=protected-access
        parses = mbl._fetch_iwyu_lints()

        self.assertCountEqual(parses, expected_findings)
