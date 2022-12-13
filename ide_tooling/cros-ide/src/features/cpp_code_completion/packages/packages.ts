// Copyright 2022 The ChromiumOS Authors.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as fs from 'fs';
import * as path from 'path';
import {findChroot, sourceDir} from '../../../common/common_util';
import {ChrootService} from '../../../services/chroot';
import {KNOWN_PACKAGES} from './known_packages';
import {generate} from './mapping';
import {SourceDir, PackageInfo} from './types';

// TODO(oka): Make this a singleton if this is used from multiple places.
export class Packages {
  private mapping = new Map<SourceDir, PackageInfo>();
  private generated = false;

  /**
   * If autoDetect is true, instead of using a hard-coded mapping, we lazily generate
   * the mapping from the current repository when it's needed.
   */
  constructor(
    private readonly chrootService: ChrootService,
    autoDetect?: boolean
  ) {
    if (autoDetect) {
      return;
    }
    for (const packageInfo of KNOWN_PACKAGES) {
      this.mapping.set(packageInfo.sourceDir, packageInfo);
    }
    this.generated = true;
  }

  private async ensureGenerated() {
    if (this.generated) {
      return;
    }
    const source = this.chrootService.source();
    if (!source) {
      return;
    }
    for (const packageInfo of await generate(source.root)) {
      this.mapping.set(packageInfo.sourceDir, packageInfo);
    }
    this.generated = true;
  }

  /**
   * Get information of the package that would compile the file and generates
   * compilation database, or null if no such package is known.
   */
  async fromFilepath(filepath: string): Promise<PackageInfo | null> {
    await this.ensureGenerated();

    let realpath = '';
    try {
      realpath = await fs.promises.realpath(filepath);
    } catch (_e) {
      // If filepath is an absolute path, assume it's a realpath. This is
      // convenient for testing, where the file may not exist.
      if (path.isAbsolute(filepath)) {
        realpath = filepath;
      } else {
        return null;
      }
    }

    const chroot = findChroot(realpath);
    if (chroot === undefined) {
      return null;
    }
    const sourcePath = sourceDir(chroot);

    let relPath = path.relative(sourcePath, realpath);
    if (relPath.startsWith('..') || path.isAbsolute(relPath)) {
      return null;
    }
    while (relPath !== '.') {
      const info = this.mapping.get(relPath);
      if (info !== undefined) {
        return info;
      }
      relPath = path.dirname(relPath);
    }
    return null;
  }
}
