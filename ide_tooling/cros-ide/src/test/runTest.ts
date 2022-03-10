// Copyright 2022 The Chromium OS Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
import * as path from 'path';

import {runTests} from '@vscode/test-electron';

async function main() {
  try {
    // The folder containing the Extension Manifest package.json
    // Passed to `--extensionDevelopmentPath`
    const extensionDevelopmentPath = path.resolve(__dirname, '../../');

    // The path to test runner
    // Passed to --extensionTestsPath
    const extensionTestsPath = path.resolve(__dirname, './integration/index');

    // Download VS Code, unzip it and run the integration test
    await runTests({extensionDevelopmentPath, extensionTestsPath});
  } catch (err) {
    console.error('Failed to run tests');
    process.exit(1);
  }
}

main();
