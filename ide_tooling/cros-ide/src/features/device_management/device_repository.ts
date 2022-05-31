// Copyright 2022 The Chromium OS Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as vscode from 'vscode';
import * as ideUtil from '../../ide_util';

// Represents the type of a device.
export enum DeviceCategory {
  // An owned device is a device owned by the user.
  OWNED,
  // A leased device is a device temporarily leased to the user.
  LEASED,
}

export interface Device {
  readonly hostname: string;
}

export interface OwnedDevice extends Device {
  readonly category: DeviceCategory.OWNED;
}

export interface LeasedDevice extends Device {
  readonly category: DeviceCategory.LEASED;
}

/**
 * Maintains a list of owned devices available for the device management feature.
 * The list is backed by a user setting.
 */
export class OwnedDeviceRepository implements vscode.Disposable {
  private static readonly CONFIG_HOSTNAMES = 'deviceManagement.devices';

  private readonly onDidChangeEmitter = new vscode.EventEmitter<void>();
  readonly onDidChange = this.onDidChangeEmitter.event;

  private readonly subscriptions: vscode.Disposable[] = [
    this.onDidChangeEmitter,
  ];

  constructor() {
    this.subscriptions.push(
      vscode.workspace.onDidChangeConfiguration(() => {
        this.onDidChangeEmitter.fire();
      })
    );
  }

  dispose() {
    vscode.Disposable.from(...this.subscriptions).dispose();
  }

  getDevices(): OwnedDevice[] {
    const hostnames = this.getHostnames();
    return hostnames.map(hostname => ({
      category: DeviceCategory.OWNED,
      hostname,
    }));
  }

  async addDevice(hostname: string): Promise<void> {
    const hostnames = this.getHostnames();
    if (hostnames.includes(hostname)) {
      return;
    }
    const newHostnames = [...hostnames, hostname];
    await this.setHostnames(newHostnames);
  }

  async removeDevice(hostname: string): Promise<void> {
    const hostnames = this.getHostnames();
    if (!hostnames.includes(hostname)) {
      throw new Error(`Unknown owned host: ${hostname}`);
    }
    const newHostnames = hostnames.filter(h => h !== hostname);
    await this.setHostnames(newHostnames);
  }

  private getHostnames(): string[] {
    return (
      ideUtil
        .getConfigRoot()
        .get<string[]>(OwnedDeviceRepository.CONFIG_HOSTNAMES) ?? []
    );
  }

  private async setHostnames(hosts: string[]): Promise<void> {
    await ideUtil
      .getConfigRoot()
      .update(
        OwnedDeviceRepository.CONFIG_HOSTNAMES,
        hosts,
        vscode.ConfigurationTarget.Global
      );
  }
}

/**
 * Maintains a list of leased devices available for the device management feature.
 * The list is backed by the crosfleet command.
 */
export class LeasedDeviceRepository implements vscode.Disposable {
  private readonly onDidChangeEmitter = new vscode.EventEmitter<void>();
  readonly onDidChange = this.onDidChangeEmitter.event;

  private readonly subscriptions: vscode.Disposable[] = [
    this.onDidChangeEmitter,
  ];

  constructor() {}

  dispose() {
    vscode.Disposable.from(...this.subscriptions).dispose();
  }

  async getDevices(): Promise<LeasedDevice[]> {
    // TODO: Implement leasing.
    return [];
  }
}