// Copyright 2022 The ChromiumOS Authors.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as path from 'path';
import * as vscode from 'vscode';
import * as config from '../../services/config';
import {cleanState} from '../testing';
import * as fakes from '../testing/fakes';

/**
 * Spy for the `vscode` module.
 */
export type VscodeSpy = ReturnType<typeof newVscodeSpy>;

type SpiableVscodeWindow = Omit<
  typeof vscode.window,
  'showInformationMessage'
> & {
  // Original type doesn't work due to
  // https://github.com/DefinitelyTyped/DefinitelyTyped/issues/42455 .
  showErrorMessage: jasmine.Func;
  showInformationMessage: jasmine.Func;
  showQuickPick: jasmine.Func;
  showWarningMessage: jasmine.Func;
};

type SpiableVscodeWorkspace = typeof vscode.workspace & {
  openTextDocument: jasmine.Func;
};

/**
 * Creates a new VscodeSpy.
 * The fields should be substituted in installVscodeDouble().
 */
function newVscodeSpy() {
  return {
    commands: jasmine.createSpyObj<typeof vscode.commands>('vscode.commands', [
      'registerCommand',
      'registerTextEditorCommand',
      'executeCommand',
    ]),
    env: jasmine.createSpyObj<typeof vscode.env>('vscode.env', [
      'openExternal',
    ]),
    window: jasmine.createSpyObj<SpiableVscodeWindow>('vscode.window', [
      'createOutputChannel',
      'createStatusBarItem',
      'showErrorMessage',
      'showInformationMessage',
      'showInputBox',
      'showQuickPick',
      'showTextDocument',
      'showWarningMessage',
    ]),
    workspace: jasmine.createSpyObj<SpiableVscodeWorkspace>(
      'vscode.workspace',
      ['getConfiguration', 'openTextDocument']
    ),
    extensions: jasmine.createSpyObj<typeof vscode.extensions>(
      'vscode.extensions',
      ['getExtension']
    ),
  };
}

/**
 * Emitters for events in the 'vscode' module.
 */
export type VscodeEmitters = ReturnType<typeof newVscodeEmitters>;

function newVscodeEmitters() {
  return {
    window: {
      // TODO(oka): Add more `onDid...` event emitters here.
      onDidChangeActiveTextEditor: new vscode.EventEmitter<
        vscode.TextEditor | undefined
      >(),
    },
    workspace: {
      // Add more `onDid...` and `onWill...` event emitters here.
      onDidSaveTextDocument: new vscode.EventEmitter<vscode.TextDocument>(),
      onDidChangeConfiguration:
        new vscode.EventEmitter<vscode.ConfigurationChangeEvent>(),
    },
  };
}

/**
 * Installs a double for the vscode namespace and returns handlers to interact
 * with it.
 */
export function installVscodeDouble(): {
  vscodeSpy: VscodeSpy;
  vscodeEmitters: VscodeEmitters;
} {
  const vscodeSpy = cleanState(() => newVscodeSpy());
  const vscodeEmitters = cleanState(() => newVscodeEmitters());

  const real = vscode;
  const original = Object.assign({}, real);
  beforeEach(() => {
    real.commands = vscodeSpy.commands;
    real.env = vscodeSpy.env;
    real.extensions = vscodeSpy.extensions;
    real.window = buildNamespace(vscodeSpy.window, vscodeEmitters.window);
    real.workspace = buildNamespace(
      vscodeSpy.workspace,
      vscodeEmitters.workspace
    );
  });
  afterEach(() => {
    Object.assign(real, original);
  });

  return {
    vscodeSpy,
    vscodeEmitters,
  };
}

function buildNamespace(
  spies: jasmine.SpyObj<unknown>,
  emitters: {[key: string]: vscode.EventEmitter<unknown>}
) {
  return Object.fromEntries([
    ...Object.entries(spies).map(([key, spy]) => [
      key,
      (...args: unknown[]) => (spy as jasmine.Spy)(...args),
    ]),
    ...Object.entries(emitters).map(([key, emitter]) => [key, emitter.event]),
  ]);
}

/**
 * Installs a fake configuration for testing.
 */
export function installFakeConfigs(
  vscodeSpy: VscodeSpy,
  vscodeEmitters: VscodeEmitters
): void {
  const subscriptions: vscode.Disposable[] = [];

  beforeEach(() => {
    const fakeConfig = new fakes.FakeWorkspaceConfiguration(
      path.join(__dirname, '../../../package.json'),
      config.TEST_ONLY.CROS_IDE_PREFIX
    );
    subscriptions.push(fakeConfig);

    vscodeSpy.workspace.getConfiguration
      .withArgs(config.TEST_ONLY.CROS_IDE_PREFIX)
      .and.returnValue(fakeConfig as vscode.WorkspaceConfiguration);
    subscriptions.push(
      fakeConfig.onDidChange(ev =>
        vscodeEmitters.workspace.onDidChangeConfiguration.fire(ev)
      )
    );
  });

  afterEach(() => {
    vscode.Disposable.from(...subscriptions).dispose();
    subscriptions.splice(0);
  });
}
