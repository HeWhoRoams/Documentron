#!/usr/bin/env python3
"""
Prepare AI Context Pack

Builds a compact, deterministic context bundle from artifacts and
deterministic docs to guide an AI agent in VS Code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

EXCLUDED_DIRS = {'.git', '.venv', 'node_modules', '.specify', 'Documentron', 'Generated Documentation'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
    except (FileNotFoundError, PermissionError, OSError) as e:
        logging.error(f"Failed to read file {path}: {e}")
        raise IOError(f"Failed to read file {path}: {e}") from e
    return h.hexdigest()


def build_artifacts_index(artifacts_root: Path) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    if artifacts_root.exists():
        for p in sorted(artifacts_root.rglob('*.json')):
            # Skip report JSONs; include them separately in quality.json
            rel = p.relative_to(artifacts_root)
            if rel.parts and rel.parts[0] == 'report':
                continue
            rel_posix = rel.as_posix()
            size = p.stat().st_size
            digest = sha256_file(p)
            items.append({
                'path': rel_posix,
                'size': size,
                'sha256': digest,
            })
    return {'root': str(artifacts_root), 'items': items}


def build_file_manifest(repo_root: Path, max_files: int = 2000) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    count = 0
    for root, dirs, files in os.walk(repo_root):
        # prune excluded dirs in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for name in files:
            p = Path(root) / name
            try:
                rel = p.relative_to(repo_root).as_posix()
            except ValueError:
                continue
            size = 0
            try:
                size = p.stat().st_size
            except OSError:
                pass
            entries.append({'path': rel, 'size': size, 'ext': p.suffix})
            count += 1
            if count >= max_files:
                return {'count': count, 'truncated': True, 'files': entries}
    return {'count': count, 'truncated': False, 'files': entries}


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def build_min_symbol_graph(artifacts_root: Path) -> Dict[str, Any]:
    sym = load_json(artifacts_root / 'symbol.graph.json')
    if not isinstance(sym, dict):
        return {'symbols': []}
    symbols = sym.get('symbols') or sym.get('nodes') or []
    # keep to first 200 for compact context
    if isinstance(symbols, list) and len(symbols) > 200:
        symbols = symbols[:200]
    return {'symbols': symbols}


def build_min_deps(artifacts_root: Path) -> Dict[str, Any]:
    deps = load_json(artifacts_root / 'deps.map.json')
    if not isinstance(deps, dict):
        return {'dependencies': []}
    dependencies = deps.get('dependencies', [])
    if isinstance(dependencies, list) and len(dependencies) > 500:
        dependencies = dependencies[:500]
    return {'dependencies': dependencies}


def build_quality(artifacts_root: Path) -> Dict[str, Any]:
    # prefer quality.report.json under report/, else at root
    candidates = [
        artifacts_root / 'report' / 'quality.report.json',
        artifacts_root / 'quality.report.json',
    ]
    for c in candidates:
        q = load_json(c)
        if isinstance(q, dict):
            return q
    return {'placeholder': True, 'metrics': {}}


def write_prompts(out_dir: Path, deterministic_docs_dir: Path) -> None:
    prompts_dir = out_dir / 'prompts'
    prompts_dir.mkdir(parents=True, exist_ok=True)
    seed = (
        "# AI Inspection Prompt\n\n"
        "Goal: Read the repository code and 'Generated Documentation/context/' artifacts to produce robust, human-readable documentation.\n\n"
        "Instructions:\n"
        "- Ground every claim in the codebase or artifacts; include citations to file paths.\n"
        "- Write outputs to 'Generated Documentation/ai/docs/'.\n"
        "- Include a 'Where this may be wrong' section per doc.\n"
        f"- Review deterministic docs in '{deterministic_docs_dir.as_posix()}' and improve them.\n"
    )
    (prompts_dir / 'ai-inspection.md').write_text(seed, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Prepare AI context bundle')
    parser.add_argument('repo', type=Path, help='Repository root')
    parser.add_argument('--artifacts', type=Path, required=True, help='Artifacts root directory')
    parser.add_argument('--docs', type=Path, required=True, help='Deterministic docs directory')
    parser.add_argument('--out', type=Path, required=True, help='Context output directory')
    args = parser.parse_args()

    repo_root = args.repo.resolve()
    artifacts_root = args.artifacts.resolve()
    docs_dir = args.docs.resolve()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build components
    index = build_artifacts_index(artifacts_root)
    manifest = build_file_manifest(repo_root)
    symbols = build_min_symbol_graph(artifacts_root)
    deps = build_min_deps(artifacts_root)
    quality = build_quality(artifacts_root)

    # Write files
    (out_dir / 'index.json').write_text(json.dumps(index, indent=2), encoding='utf-8')
    (out_dir / 'file-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    (out_dir / 'symbols.min.json').write_text(json.dumps(symbols, indent=2), encoding='utf-8')
    (out_dir / 'deps.min.json').write_text(json.dumps(deps, indent=2), encoding='utf-8')
    (out_dir / 'quality.json').write_text(json.dumps(quality, indent=2), encoding='utf-8')

    write_prompts(out_dir, docs_dir)

    # Write a short README with next steps
    readme = [
        '# AI Context Prepared',
        '',
        f'- Context: `{out_dir}`',
        f'- Deterministic Docs: `{docs_dir}`',
        '',
        'Next:',
        "- Open VS Code and run the command: Tasks: Run Task → 'AppDoc: Prepare AI Context' (or re-run the CLI step).",
        "- Open 'Generated Documentation/context/prompts/ai-inspection.md'.",
        "- In Copilot Chat, paste the prompt and ask it to write docs to 'Generated Documentation/ai/docs/'.",
    ]
    (out_dir / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8')

    print(f"AI context prepared at: {out_dir}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

