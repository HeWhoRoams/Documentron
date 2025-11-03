# Quickstart: Doc Synthesis

## Prerequisites
- Ensure all required artifacts are present in `out/`:
  - build.info.json
  - symbol.graph.json
  - api.surface.json
  - deps.map.json
  - quality.report.json
  - (optional) assets/*.json

## Steps
1. Run doc synthesis:
   ```bash
   appdoc synthesize --artifacts ./out --profile default --out ./docs --max-docs 6 --temperature 0.2 --seed 42
   ```
2. Verify docs:
   ```bash
   appdoc report --artifacts ./out --docs ./docs --format md
   ```
3. Check that all docs contain citations and 'Where this may be wrong' sections.
4. Confirm API coverage ≥90% in api-reference.md or exclusions are justified.
5. For identical inputs, verify docs are byte-identical or have identical semantic hashes.

## Output
- Docs generated in `docs/`:
  - overview.md
  - architecture.md
  - api-reference.md
  - dependencies.md
  - maintenance-notes.md

## Troubleshooting
- If docs lack citations, check artifact paths and JSON pointers.
- If API coverage <90%, review exclusions and rationale.
- If hallucinated claims appear, ensure LLM temperature and seed settings are correct.
