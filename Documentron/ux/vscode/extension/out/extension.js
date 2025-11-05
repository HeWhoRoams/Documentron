const vscode = require('vscode');
const { execSync } = require('child_process');

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
  // Check for py command availability and build appropriate command
  const hasPy = checkCommandExists('py');
  const hasPython = checkCommandExists('python');
  
  if (hasPy) {
    return 'py -3 Documentron/ux/cli/appdoc.py --repo .';
  } else if (hasPython) {
    return 'python Documentron/ux/cli/appdoc.py --repo .';
  } else {
    // Fallback - let the shell handle it
    return 'python Documentron/ux/cli/appdoc.py --repo .';
  }
}

function buildRunSelectedCommand(steps) {
  const stepsArg = steps.map(s => `'${s}'`).join(' ');
  // Check for py command availability and build appropriate command
  const hasPy = checkCommandExists('py');
  const hasPython = checkCommandExists('python');
  
  if (hasPy) {
    return `py -3 Documentron/ux/cli/appdoc.py --repo . --steps ${stepsArg}`;
  } else if (hasPython) {
    return `python Documentron/ux/cli/appdoc.py --repo . --steps ${stepsArg}`;
  } else {
    // Fallback - let the shell handle it
    return `python Documentron/ux/cli/appdoc.py --repo . --steps ${stepsArg}`;
  }
}

function checkCommandExists(cmd) {
  try {
    const { execSync } = require('child_process');
    // Use different check commands based on platform
    const isWindows = process.platform === 'win32';
    const checkCmd = isWindows ? `where ${cmd} 2>nul` : `which ${cmd} 2>/dev/null`;
    execSync(checkCmd, { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
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

