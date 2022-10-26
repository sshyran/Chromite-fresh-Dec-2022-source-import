// Copyright 2022 The ChromiumOS Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as path from 'path';
import * as vscode from 'vscode';
import * as cipd from '../../../../common/cipd';
import * as services from '../../../../services';
import * as gitDocument from '../../../../services/git_document';
import * as bgTaskStatus from '../../../../ui/bg_task_status';
import * as metrics from '../../../metrics/metrics';
import * as tricium from '../tricium';
import * as executor from './executor';

// Spellchecker demonstrates integration between Tricium's functions
// and CrOS IDE.
//
// If cros-ide.underDevelopment.triciumSpellchecker is not empty,
// then we use it as the path to the spellchecker and surface its findings
// in the IDE.

const STATUS_BAR_TASK_ID = 'Tricium';
const SHOW_LOG_COMMAND: vscode.Command = {
  command: 'cros-ide.showTriciumLog',
  title: 'Show Tricium Log',
};

/**
 * Activate should handle the errors instead of throwing them.
 * In particular, CIPD interaction is wrapped in try-catch block, which logs
 * an error and exits if the spellchecker cannot be installed.
 */
export async function activate(
  context: vscode.ExtensionContext,
  statusManager: bgTaskStatus.StatusManager,
  chromiumosRoot: string,
  cipdRepository: cipd.CipdRepository,
  textEditorsWatcher: services.TextEditorsWatcher,
  gitDirsWatcher: services.GitDirsWatcher
) {
  const outputChannel = vscode.window.createOutputChannel('CrOS IDE: Tricium');
  context.subscriptions.push(
    vscode.commands.registerCommand(SHOW_LOG_COMMAND.command, () =>
      outputChannel.show()
    )
  );

  let triciumSpellchecker: string;
  try {
    triciumSpellchecker = await cipdRepository.ensureTriciumSpellchecker(
      outputChannel
    );
  } catch (err) {
    outputChannel.append(`Could not download Tricium spellchecker: ${err}`);
    return;
  }

  const spellchecker = new Spellchecker(
    context,
    new executor.Executor(triciumSpellchecker, outputChannel),
    statusManager,
    chromiumosRoot,
    textEditorsWatcher,
    gitDirsWatcher
  );
  spellchecker.subscribeToDocumentChanges(context);

  // Action provider takes warning generated by Spellchecker and creates
  // code actions for them (clickable fixes).
  context.subscriptions.push(
    vscode.languages.registerCodeActionsProvider(
      {scheme: 'file'},
      new SpellcheckerActionProvider()
    )
  );
}

const DIAGNOSTIC_CODE = 'tricium-spellchecker';

class SpellcheckerDiagnostic extends vscode.Diagnostic {
  replacements: string[];
  path?: string;

  constructor(range: vscode.Range, message: string) {
    super(range, message, vscode.DiagnosticSeverity.Information);
    this.code = DIAGNOSTIC_CODE;
    this.replacements = [];
  }
}

class Spellchecker {
  private readonly diagnosticCollection: vscode.DiagnosticCollection;

  constructor(
    context: vscode.ExtensionContext,
    private readonly executor: executor.Executor,
    private readonly statusManager: bgTaskStatus.StatusManager,
    private readonly chromiumosRoot: string,
    private readonly textEditorsWatcher: services.TextEditorsWatcher,
    private readonly gitDirsWatcher: services.GitDirsWatcher
  ) {
    this.diagnosticCollection =
      vscode.languages.createDiagnosticCollection('spellchecker');
    context.subscriptions.push(this.diagnosticCollection);
  }

  /** Attach spellchecker to editor events. */
  subscribeToDocumentChanges(context: vscode.ExtensionContext): void {
    if (vscode.window.activeTextEditor) {
      void this.refreshFileDiagnostics(
        vscode.window.activeTextEditor.document.uri
      );
    }
    context.subscriptions.push(
      this.textEditorsWatcher.onDidActivate((doc: vscode.TextDocument) => {
        void this.refreshFileDiagnostics(doc.uri);
      })
    );

    context.subscriptions.push(
      vscode.workspace.onDidSaveTextDocument(doc =>
        this.refreshFileDiagnostics(doc.uri)
      )
    );

    context.subscriptions.push(
      this.textEditorsWatcher.onDidClose((doc: vscode.TextDocument) => {
        if (doc.uri.scheme === 'file') {
          this.delete(doc.uri);
        }
      })
    );

    // The code below triggers spellchecker on the commit message.
    this.gitDirsWatcher.visibleGitDirs.forEach(
      gitDir => void this.refreshCommitMessageDiagnostics(gitDir)
    );
    context.subscriptions.push(
      this.gitDirsWatcher.onDidChangeHead(e => {
        if (!e.head) {
          const uri = this.commitMessageUri(e.gitDir);
          this.delete(uri);
          return;
        }
        void this.refreshCommitMessageDiagnostics(e.gitDir);
      })
    );
  }

  private commitMessageUri(dir: string) {
    return gitDocument.commitMessageUri(dir, 'HEAD');
  }

  /** Execute Tricium binary and refresh diagnostics for the commit message. */
  private async refreshCommitMessageDiagnostics(gitDir: string): Promise<void> {
    const result = await gitDocument.getCommitMessage(gitDir, 'HEAD');

    // TODO(b:217287367): Handle errors instead of ignoring them.
    if (result instanceof Error) {
      return;
    }
    const commitMessage = result.stdout;

    const gitUri = this.commitMessageUri(gitDir);

    const results = await this.executor.checkCommitMessage(commitMessage);
    return this.refreshDiagnostics(gitUri, results);
  }

  /** Execute Tricium binary and refreshe diagnostics for the document. */
  private async refreshFileDiagnostics(uri: vscode.Uri): Promise<void> {
    if (uri.scheme !== 'file') {
      return;
    }

    if (path.relative(this.chromiumosRoot, uri.fsPath).startsWith('..')) {
      return;
    }

    // TODO(b:217287367): Cancel the operation if the active editor changes.
    const results = await this.executor.checkFile(
      this.chromiumosRoot,
      uri.fsPath
    );
    return this.refreshDiagnostics(uri, results);
  }

  private async refreshDiagnostics(
    uri: vscode.Uri,
    results: tricium.Results | Error
  ): Promise<void> {
    if (results instanceof Error) {
      this.setStatus(bgTaskStatus.TaskStatus.ERROR);
      metrics.send({
        category: 'error',
        group: 'spellchecker',
        description: `Spellchecker failed: ${results}`,
      });
      return;
    }

    const diagnostics: vscode.Diagnostic[] = [];

    if (results.comments) {
      for (const comment of results.comments) {
        const range = Spellchecker.range(comment);
        if (!range) {
          continue;
        }
        const diagnostic = new SpellcheckerDiagnostic(range, comment.message);
        // We expect exactly one suggestion, but the keep the code flexible.
        if (comment.suggestions) {
          for (const s of comment.suggestions) {
            if (s.replacements) {
              for (const r of s.replacements) {
                diagnostic.replacements.push(r.replacement);
              }
            }
          }
        }
        diagnostics.push(diagnostic);
      }
    }

    if (diagnostics.length) {
      metrics.send({
        category: 'background',
        group: 'spellchecker',
        action: 'diagnostics',
        value: diagnostics.length,
      });
    }
    this.diagnosticCollection.set(uri, diagnostics);
    this.setStatus(bgTaskStatus.TaskStatus.OK);
  }

  private setStatus(status: bgTaskStatus.TaskStatus) {
    this.statusManager.setTask(STATUS_BAR_TASK_ID, {
      status,
      command: SHOW_LOG_COMMAND,
    });
  }

  /** Clear diagnostics for the specified uri. */
  private delete(uri: vscode.Uri) {
    this.diagnosticCollection.delete(uri);
  }

  private static range(comment: tricium.Comment): vscode.Range | undefined {
    if (!comment.startLine) {
      return undefined;
    }
    return new vscode.Range(
      comment.startLine - 1,
      comment.startChar ?? 0,
      comment.endLine - 1,
      comment.endChar
    );
  }
}

/**
 * Adds suggested fixes to SpellcheckerDiagnostics.
 */
class SpellcheckerActionProvider implements vscode.CodeActionProvider {
  constructor() {}

  provideCodeActions(
    document: vscode.TextDocument,
    _range: vscode.Range | vscode.Selection,
    context: vscode.CodeActionContext,
    _token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.CodeAction[]> {
    return context.diagnostics
      .filter(diagnostic => diagnostic.code === DIAGNOSTIC_CODE)
      .flatMap(diagnostic =>
        this.createFix(document, diagnostic as SpellcheckerDiagnostic)
      );
  }

  private createFix(
    document: vscode.TextDocument,
    diagnostic: SpellcheckerDiagnostic
  ): vscode.CodeAction[] {
    const codeActions: vscode.CodeAction[] = [];
    for (const replacement of diagnostic.replacements) {
      const fix = new vscode.CodeAction(
        `Replace with: "${replacement}"`,
        vscode.CodeActionKind.QuickFix
      );
      fix.edit = new vscode.WorkspaceEdit();
      fix.edit.replace(document.uri, diagnostic.range, replacement);
      codeActions.push(fix);
    }
    return codeActions;
  }
}
