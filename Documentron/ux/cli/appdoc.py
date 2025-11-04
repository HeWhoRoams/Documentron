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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Documentron end-to-end workflow")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Repository root path")
    parser.add_argument("--artifacts", type=Path, default=Path("Documentron/artifacts"), help="Artifacts root directory")
    parser.add_argument("--docs", type=Path, default=Path("Documentron/docs"), help="Docs output directory")
    parser.add_argument("--steps", nargs="*", choices=["inspect", "convert", "synthesize", "verify", "report"],
                        help="Run only these steps (default: all)")
    parser.add_argument("--skip", nargs="*", choices=["inspect", "convert", "synthesize", "verify", "report"],
                        help="Skip these steps")
    args = parser.parse_args()

    repo = args.repo.resolve()
    artifacts_root = args.artifacts.resolve()
    assets_dir = artifacts_root / "assets"
    reports_dir = artifacts_root / "report"
    docs_dir = args.docs.resolve()

    ensure_dirs(assets_dir, reports_dir, docs_dir)

    desired = args.steps or ["inspect", "convert", "synthesize", "verify", "report"]
    skips = set(args.skip or [])
    steps = [s for s in desired if s not in skips]

    print("Documentron AppDoc starting...")
    print(f"repo     : {repo}")
    print(f"artifacts: {artifacts_root}")
    print(f"docs     : {docs_dir}\n")

    # 1) Inspect (C# adapter via Python wrapper)
    if "inspect" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.inspection.inspect",
            str(repo)
        ], title="Inspect (C# adapter)")
        if code != 0:
            return code

    # 2) Convert assets
    if "convert" in steps:
        code = run([
            sys.executable,
            "-m", "Documentron.core.asset_conversion.main",
            str(repo),
            "--output-dir", str(assets_dir)
        ], title="Convert Assets")
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
        ], title="Synthesize Docs")
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
            f"- Docs: `{docs_dir}`",
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
