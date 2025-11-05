#!/usr/bin/env python3
"""
AppDoc Orchestrator CLI

Runs the end-to-end Documentron workflow:
  1) inspect   – repo analysis via C# adapter
  2) convert   – non-code asset conversion to JSON artifacts
  3) synthesize – documentation synthesis from artifacts
  4) verify    – basic validation and quality checks
  5) report    – concise summary report

Defaults are chosen so it runs without extra inputs.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, title: str | None = None, timeout: float | None = None) -> int:
    if title:
        print(f"\n=== {title} ===", flush=True)
    print("$", " ".join(str(c) for c in cmd), flush=True)
    try:
        result = subprocess.run(cmd, cwd=str(cwd) if cwd else None, timeout=timeout)
        if result.returncode != 0:
            print(f"Step failed with exit code {result.returncode}", file=sys.stderr)
        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds", file=sys.stderr)
        return 1


def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def bootstrap_workspace(workspace_root: Path) -> None:
    try:
        # .vscode/tasks.json
        vs_dir = workspace_root / ".vscode"
        vs_dir.mkdir(parents=True, exist_ok=True)
        tasks_json = vs_dir / "tasks.json"
        if not tasks_json.exists():
            tasks_json.write_text(
                """
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AppDoc: Run All",
      "type": "shell",
      "command": "python",
      "args": [
        "Documentron/ux/cli/appdoc.py",
        "--repo", ".",
        "--artifacts", "Generated Documentation",
        "--docs", "Generated Documentation/deterministic/docs"
      ],
      "problemMatcher": []
    },
    {
      "label": "AppDoc: Prepare AI Context",
      "type": "shell",
      "command": "python",
      "args": [
        "Documentron/ux/cli/appdoc.py",
        "--repo", ".",
        "--artifacts", "Generated Documentation",
        "--docs", "Generated Documentation/deterministic/docs",
        "--steps", "prepare-ai"
      ],
      "problemMatcher": []
    }
  ]
}
""".strip() + "\n",
                encoding="utf-8",
            )
        # .github/prompts/appdoc.prompt.md
        gh_dir = workspace_root / ".github" / "prompts"
        gh_dir.mkdir(parents=True, exist_ok=True)
        appdoc_prompt = gh_dir / "appdoc.prompt.md"
        if not appdoc_prompt.exists():
            appdoc_prompt.write_text(
                (
                    "# AppDoc End-to-End Prompt\n\n"
                    "Use this in GitHub Copilot Chat to run the full Documentron workflow.\n\n"
                    "Prompt:\n\n"
                    "/appdoc\n"
                    "Goal: Run inspect → convert → synthesize → verify → report for the current workspace, with zero manual steps.\n\n"
                    "Instructions for Copilot:\n"
                    "- If a terminal is not open, open one.\n"
                    "- Run: python Documentron/ux/cli/appdoc.py --repo .\n"
                    "- Stream the terminal output back here.\n"
                    "- If Python is not found, try: py -3 Documentron/ux/cli/appdoc.py --repo .\n"
                    "- On failure of any step, show the error and re-run only the failed step using --steps <step>.\n"
                    "- After completion, show a concise summary by printing 'Generated Documentation/report/summary.md' and, if present, 'Generated Documentation/report/quality.report.json'.\n"
                    "- To prepare AI context for VS Code agent, run: python Documentron/ux/cli/appdoc.py --repo . --steps prepare-ai\n"
                    "- Do not ask for additional input unless strictly required.\n"
                ),
                encoding="utf-8",
            )
        # Bootstrap launchers if missing
        ps1 = workspace_root / "appdoc.ps1"
        if not ps1.exists():
            ps1.write_text(
                (
                    "Param(\n"
                    "    [string]$Repo = '.',\n"
                    "    [string]$Artifacts = 'Generated Documentation',\n"
                    "    [string]$Docs = 'Generated Documentation/deterministic/docs',\n"
                    "    [string[]]$Steps,\n"
                    "    [string[]]$Skip\n"
                    ")\n\n"
                    "$argsList = @('Documentron/ux/cli/appdoc.py', '--repo', $Repo, '--artifacts', $Artifacts, '--docs', $Docs)\n"
                    "if ($Steps) { $argsList += @('--steps') + $Steps }\n"
                    "if ($Skip)  { $argsList += @('--skip')  + $Skip }\n\n"
                    "function Invoke-Python($argsList) {\n"
                    "  if ($env:PYTHONEXECUTABLE) { & $env:PYTHONEXECUTABLE $argsList; return $LASTEXITCODE }\n"
                    "  try { py -3 --version *> $null; if ($LASTEXITCODE -eq 0) { py -3 $argsList; return $LASTEXITCODE } } catch {}\n"
                    "  try { python --version *> $null; if ($LASTEXITCODE -eq 0) { python $argsList; return $LASTEXITCODE } } catch {}\n"
                    "  Write-Error 'Python not found. Please install Python 3.11+ or set PYTHONEXECUTABLE.'\n"
                    "  return 1\n"
                    "}\n\n"
                    "exit (Invoke-Python $argsList)\n"
                ),
                encoding="utf-8",
            )
        # No CMD launcher; PowerShell + Python only
    except Exception as e:
        print(f"Bootstrap skipped: {e}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Documentron end-to-end workflow")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Repository root path")
    parser.add_argument("--artifacts", type=Path, default=Path("Generated Documentation"), help="Artifacts root directory (base output dir)")
    parser.add_argument("--docs", type=Path, default=Path("Generated Documentation/deterministic/docs"), help="Deterministic docs output directory")
    parser.add_argument("--context", type=Path, default=Path("Generated Documentation/context"), help="AI context output directory")
    parser.add_argument("--ai-out", type=Path, default=Path("Generated Documentation/ai/docs"), help="AI-authored docs output directory (informational)")
    parser.add_argument("--steps", nargs="*", choices=["inspect", "convert", "synthesize", "prepare-ai", "verify", "report"],
                        help="Run only these steps (default: all)")
    parser.add_argument("--skip", nargs="*", choices=["inspect", "convert", "synthesize", "prepare-ai", "verify", "report"],
                        help="Skip these steps")
    parser.add_argument("--no-bootstrap", action="store_true", help="Do not create VS Code tasks or prompt files automatically")
    args = parser.parse_args()

    repo = args.repo.resolve()
    # Anchor outputs to the repo root when relative paths are provided
    artifacts_root = (args.artifacts if args.artifacts.is_absolute() else (repo / args.artifacts)).resolve()
    assets_dir = artifacts_root / "assets"
    reports_dir = artifacts_root / "report"
    docs_dir = (args.docs if args.docs.is_absolute() else (repo / args.docs)).resolve()
    context_dir = (args.context if args.context.is_absolute() else (repo / args.context)).resolve()
    # (context_dir already resolved above)

    ensure_dirs(assets_dir, reports_dir, docs_dir)

    # First-run bootstrap (workspace-level helpers)
    if not args.no_bootstrap:
        bootstrap_workspace(Path.cwd())

    desired = args.steps or ["inspect", "convert", "synthesize", "prepare-ai", "verify", "report"]
    skips = set(args.skip or [])
    steps = [s for s in desired if s not in skips]

    print("Documentron AppDoc starting...")
    print(f"repo     : {repo}")
    print(f"artifacts: {artifacts_root}")
    print(f"docs     : {docs_dir}")
    print(f"context  : {context_dir}")
    print(f"ai out   : {args.ai_out}\n")

    # 1) Inspect (C# adapter via Python wrapper)
    if "inspect" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.inspection.inspect",
            str(repo)
        ], title="Inspect (C# adapter)", cwd=repo)
        if code != 0:
            return code

    # 2) Convert assets
    if "convert" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.asset_conversion.main",
            str(repo),
            "--output-dir", str(assets_dir)
        ], title="Convert Assets", cwd=repo)
        if code != 0:
            return code

    # 3) Synthesize docs
    if "synthesize" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.synthesis.cli",
            "synthesize",
            "--artifacts", str(artifacts_root),
            "--out", str(docs_dir),
            "--profile", "default",
            "--max-docs", "6",
            "--temperature", "0.2",
            "--seed", "42",
        ], title="Synthesize Docs", cwd=repo)
        if code != 0:
            return code

    # 3b) Prepare AI context pack
    if "prepare-ai" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.context.prepare",
            str(repo),
            "--artifacts", str(artifacts_root),
            "--docs", str(docs_dir),
            "--out", str(context_dir),
        ], title="Prepare AI Context", cwd=repo)
        if code != 0:
            return code

    # 4) Verify (basic placeholder checks)
    quality_json = reports_dir / "quality.report.json"
    if "verify" in steps:
        # Placeholder: verify docs directory exists and is non-empty
        # Use bounded search to avoid full tree traversal
        has_docs = False
        if docs_dir.exists():
            for entry in docs_dir.iterdir():
                if entry.is_file() and entry.suffix == ".md":
                    has_docs = True
                    break
        # TODO: Implement actual coverage calculation (e.g., from API surface vs docs)
        coverage = None  # Placeholder until coverage metrics are implemented
        try:
            import json
            quality = {
                "ok": has_docs,
                "docs_path": str(docs_dir),
                "metrics": {
                    "api_coverage_percent": coverage,
                },
            }
            quality_json.write_text(json.dumps(quality, indent=2), encoding="utf-8")
            print(f"Wrote quality report: {quality_json}")
        except OSError as e:
            print(f"Failed to write quality report file: {e}", file=sys.stderr)
        except TypeError as e:
            print(f"Failed to serialize quality report to JSON: {e}", file=sys.stderr)

    # 5) Report (concise summary)
    if "report" in steps:
        summary_md = reports_dir / "summary.md"
        lines = [
            "# Documentron AppDoc Summary",
            "",
            f"- Repo: `{repo}`",
            f"- Artifacts: `{artifacts_root}`",
            f"- Deterministic Docs: `{docs_dir}`",
            f"- AI Context: `{context_dir}`",
            f"- AI Docs (target): `{args.ai_out}`",
        ]
        if quality_json.exists():
            try:
                import json
                q = json.loads(quality_json.read_text(encoding="utf-8"))
                lines.append(f"- Verification: {'OK' if q.get('ok') else 'FAILED'}")
                if "metrics" in q and "api_coverage_percent" in q["metrics"]:
                    lines.append(f"- API Coverage: {q['metrics']['api_coverage_percent']}%")
            except OSError:
                lines.append("- Verification: (error reading quality report)")
            except json.JSONDecodeError:
                lines.append("- Verification: (error parsing quality report)")
        else:
            lines.append("- Verification: (not run)")
        summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote summary: {summary_md}")

    print("\nAll requested steps completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
