# AI Inspection Prompt

Goal: Read the repository and the context in `Generated Documentation/context/` to produce robust, human-readable documentation.

Instructions for the AI agent:
- Ground every claim in the codebase or context artifacts; include citations to file paths.
- Improve upon the deterministic docs in `Generated Documentation/deterministic/docs/`.
- Write outputs to `Generated Documentation/ai/docs/` (create directory if missing).
- Include a 'Where this may be wrong' section in each document.
- Maintain provenance: include a footer noting model, date, and source inputs.

Suggested steps:
1) Skim `context/index.json`, `file-manifest.json`, `symbols.min.json`, `deps.min.json`, `quality.json`.
2) Open deterministic docs and identify gaps.
3) Draft and save: overview.md, architecture.md, api-reference.md, dependencies.md, maintenance-notes.md.
4) Re-scan for missing citations and finalize.

