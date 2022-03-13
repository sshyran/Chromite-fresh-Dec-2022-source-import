// Copyright 2022 The Chromium OS Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as fs from 'fs';
import * as path from 'path';
import * as commonUtil from './common_util';

/**
 * @returns Boards that have been set up, ordered by access time (newest to
 * oldest).
 */
export async function getSetupBoardsRecentFirst(rootDir: string = '/'): Promise<string[]> {
  return getSetupBoardsOrdered(
      rootDir,
      async (dir) => fs.promises.stat(dir),
      (a, b) => b.atimeMs - a.atimeMs);
}

/**
 * @returns Boards that have been set up in alphabetic order.
 */
export async function getSetupBoardsAlphabetic(rootDir: string = '/'): Promise<string[]> {
  return getSetupBoardsOrdered(
      rootDir,
      async (dir) => dir,
      (a, b) => a.localeCompare(b));
}

async function getSetupBoardsOrdered<T>(
    rootDir: string = '/',
    keyFn: (dir: string) => Promise<T>,
    compareFn: (a: T, b: T) => number): Promise<string[]> {
  const build = path.join(rootDir, 'build');
  const dirs = await fs.promises.readdir(build);
  const dirStat: Array<[string, T]> = [];
  for (const dir of dirs) {
    if (dir === 'bin') {
      continue;
    }
    dirStat.push([dir, await keyFn(path.join(build, dir))]);
  }
  dirStat.sort(([, a], [, b]) => compareFn(a, b));
  return dirStat.map(([x]) => x);
}

/**
 * @returns Packages that are worked on.
 */
export async function getWorkedOnPackages(board: string): Promise<string[]> {
  const stdout = await commonUtil.exec(
      'cros_workon', ['--board', board, 'list']);
  return stdout.split('\n').filter(x => x.trim() !== '');
}
