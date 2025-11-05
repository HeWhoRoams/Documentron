const vscode = require('vscode');

function runInTerminal(cmd, cwd) {
  const term = vscode.window.createTerminal({ name: 'Documentron AppDoc', cwd });
  term.show(true);
  term.sendText(cmd, true);
}

function getWorkspaceFolderPath() {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) { return undefined; }
  return folders[0].uri.fsPath;
}

function buildRunAllCommand() {
  // Try py -3, then python
  return 'py -3 Documentron/ux/cli/appdoc.py --repo . || python Documentron/ux/cli/appdoc.py --repo .';
}

function buildRunSelectedCommand(steps) {
  const stepsArg = steps.map(s => `'${s}'`).join(' ');
  return `py -3 Documentron/ux/cli/appdoc.py --repo . --steps ${stepsArg} || python Documentron/ux/cli/appdoc.py --repo . --steps ${stepsArg}`;
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const runAll = vscode.commands.registerCommand('documentron.appdoc.runAll', () => {
    const cwd = getWorkspaceFolderPath();
    if (!cwd) { vscode.window.showErrorMessage('No workspace folder open.'); return; }
    runInTerminal(buildRunAllCommand(), cwd);
  });

  const runSelect = vscode.commands.registerCommand('documentron.appdoc.runSelectSteps', async () => {
    const cwd = getWorkspaceFolderPath();
    if (!cwd) { vscode.window.showErrorMessage('No workspace folder open.'); return; }
    const all = ['inspect', 'convert', 'synthesize', 'verify', 'report'];
    const picks = await vscode.window.showQuickPick(all.map(label => ({ label })), { canPickMany: true, title: 'Select AppDoc steps' });
    if (!picks || picks.length === 0) { return; }
    const steps = picks.map(p => p.label);
    runInTerminal(buildRunSelectedCommand(steps), cwd);
  });

  context.subscriptions.push(runAll, runSelect);
}

function deactivate() {}

module.exports = { activate, deactivate };

