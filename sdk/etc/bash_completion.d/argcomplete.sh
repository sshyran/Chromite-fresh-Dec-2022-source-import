#!/bin/bash
# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Find and source the bash completion script for Python argcomplete
# if the script exists.
# This search is hacky. It dynamically adapts to different paths between
# Python versions. Ideally argcomplete can tell us the path directly, but
# its tools don't yet support this.
# See https://github.com/kislyuk/argcomplete/issues/364.
argcomplete_path=$(find /usr/lib*/py*/site-packages/argcomplete \
  -name python-argcomplete.sh | head -n 1)
if [[ -n "${argcomplete_path}" ]]; then
  source "${argcomplete_path}"
fi
