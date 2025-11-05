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
1. Run doc synthesis (default paths):
   ```bash
   appdoc synthesize --artifacts "Generated Documentation" --profile default --out "Generated Documentation/docs" --max-docs 6 --temperature 0.2 --seed 42
   ```
2. Verify docs:
   ```bash
   appdoc report --artifacts "Generated Documentation" --docs "Generated Documentation/docs" --format md
   ```
3. Check that all docs contain citations and 'Where this may be wrong' sections.
4. Confirm API coverage ≥90% in api-reference.md or exclusions are justified.
5. For identical inputs, verify docs are byte-identical or have identical semantic hashes.

## Output
- Docs generated in `Generated Documentation/docs/`:
  - overview.md — high-level product overview (~1–2 pages, 500–1000 lines)
  - architecture.md — system architecture and design patterns (~2–3 pages, 800–1500 lines)
  - api-reference.md — auto-generated API docs with endpoint signatures and examples (~5–10 pages, 2000–4000 lines)
  - dependencies.md — dependency list, versions, and compatibility notes (~1 page, 200–500 lines)
  - maintenance-notes.md — operational guidance and troubleshooting (~1–2 pages, 400–800 lines)

## Troubleshooting
- If docs lack citations, check artifact paths and JSON pointers.
- If API coverage <90%, review exclusions and rationale.
- If hallucinated claims appear, ensure LLM temperature and seed settings are correct.
