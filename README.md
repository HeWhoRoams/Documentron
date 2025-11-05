# Documentron

A lean, deterministic inspection and documentation toolkit for C# codebases. It produces machine‑readable artifacts and reproducible docs, with an optional AI phase to refine results.

## Two‑Phase Workflow

1) Deterministic (no AI)
- Inspect code via MSBuild (or lite fallback)
- Convert assets (DOCX/XLSX/VDX) to normalized JSON
- Synthesize reproducible Markdown docs from artifacts
- Verify and summarize

2) AI Inspection (optional)
- Prepare a compact context bundle for an AI agent
- Use VS Code + Copilot (or your agent) to generate enhanced human‑readable docs grounded in artifacts and code

## Prerequisites

- Windows with .NET 8 SDK (for C# inspection)
- Python 3.11+
- Optional: `python-docx` (DOCX), `openpyxl` (XLSX), `defusedxml` (VDX)

## Copy‑Into‑Repo Flow

1) Copy the inner `Documentron/` folder into the root of the repo you want to document (e.g., `C:\MyApp\Documentron`).
2) From the repo root, run one of the launchers below.
3) All generated outputs are written to `Generated Documentation/` — nothing is written into `Documentron/`.

## Launchers

```powershell
# PowerShell (from repo root)
./Documentron/appdoc.ps1

# Or from the inner Documentron folder
./appdoc.ps1

# Optional: Python directly (from repo root)
py -3 Documentron/ux/cli/appdoc.py --repo .
```

## One‑Liner (end‑to‑end)

```bash
# From repo root
python Documentron/ux/cli/appdoc.py

# Steps: inspect → convert → synthesize → prepare-ai → verify → report
# Outputs base: Generated Documentation/
# Artifacts:    Generated Documentation/
# Deterministic Docs: Generated Documentation/deterministic/docs
# AI Context:  Generated Documentation/context
# AI Docs:     Generated Documentation/ai/docs (written by your AI agent)
```

## Run Specific Steps

```bash
python Documentron/ux/cli/appdoc.py --steps inspect
python Documentron/ux/cli/appdoc.py --steps synthesize report
python Documentron/ux/cli/appdoc.py --skip verify
```

## Prepare AI Context (one click)

```bash
python Documentron/ux/cli/appdoc.py --repo . --steps prepare-ai
```

VS Code tasks (auto‑bootstrapped on first run):
- Tasks: Run Task → “AppDoc: Run All”
- Tasks: Run Task → “AppDoc: Prepare AI Context”

Next:
- Open `Generated Documentation/context/prompts/ai-inspection.md`
- Paste into Copilot Chat (or your agent), ask it to write to `Generated Documentation/ai/docs/`

## Output Structure

- `Generated Documentation/`
  - `build.info.json`, `symbol.graph.json`, `api.surface.json`, `deps.map.json`, `quality.report.json`
  - `assets/` — normalized JSON from DOCX/XLSX/VDX
  - `deterministic/docs/` — reproducible Markdown docs
  - `context/` — AI context bundle (index, manifest, symbols/deps minified, quality, prompts)
  - `ai/docs/` — AI‑authored docs (created by your agent)
  - `report/` — summary and quality report

## Architecture

- `adapters/csharp/` — C# inspection
- `core/synthesis/` — deterministic doc synthesis
- `core/context/` — AI context bundle generation
- `core/artifacts/` — writers/schemas
- `ux/cli/` — command‑line tools
- `ux/vscode/` — extension helpers

## Notes

- If MSBuild cannot be used, the inspector falls back to a lightweight mode and prints why.
- Missing format libraries only skip that format; others still convert.
