# Implementation Plan: Repository Inspection and Artifact Generation

**Branch**: `001-repo-inspection` | **Date**: 2025-11-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-repo-inspection/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements a workflow for analyzing C# repositories using Roslyn and MSBuild, orchestrated by a prompt in GitHub Copilot Chat. The workflow produces five canonical artifacts (build.info.json, symbol.graph.json, api.surface.json, deps.map.json, quality.report.json) that serve as the single source of truth for downstream documentation and validation. The process is fully deterministic, meets strict quality budgets, and is validated by running the workflow against itself.

## Technical Context

**Language/Version**: Python 3.11 (workflow orchestration), C# (analysis via Roslyn/MSBuild)  
**Primary Dependencies**: pythonnet, Roslyn, MSBuild, jsonschema, pytest  
**Storage**: Filesystem (JSON artifacts in Documentron/artifacts/)  
**Testing**: pytest (Python), xUnit (C#), schema validation  
**Target Platform**: Windows 10+, VS Code, GitHub Copilot Chat  
**Project Type**: Single project (Documentron subfolder)  
**Performance Goals**: ≤30s per 1k LOC for inspection; ≥97% symbol resolution; ≥98% project discovery  
**Constraints**: Deterministic output, schema validation, no heuristic parsing  
**Scale/Scope**: 1–100k LOC, multi-solution repos, CI/CD integration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Determinism: All inputs produce identical artifacts
- Artifacts-first: LLMs and downstream tools consume only generated artifacts
- Tight interfaces: Python orchestrates C# analysis via well-defined CLI and API boundaries
- Budgeted complexity: Quality budgets enforced (latency, symbol resolution, project discovery)
- Replaceable adapters: C# analysis isolated in Documentron/adapters/csharp
- Inspect > infer: Roslyn/MSBuild only; no regex or heuristics
- Test as guardrail: pytest/xUnit tests required for all features
- Docs as product: Documentation generated from artifacts
- Workflow integrity through testing: Workflow validated by running against this repo

**GATE STATUS: PASS**

## Project Structure

### Documentation (this feature)

```text
specs/001-repo-inspection/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (Documentron subfolder)

```text
Documentron/
├── core/
│   ├── inspection/     # Python orchestrator, C# analyzers
│   ├── artifacts/      # JSON schema validation, writers
│   ├── synthesis/      # Prompt builders, LLM runners
│   └── verification/   # Quality checks, coverage, determinism
├── adapters/
│   └── csharp/         # Roslyn/MSBuild integration
├── ux/
│   ├── vscode/         # Copilot Chat prompt orchestration
│   └── cli/            # CLI entry points
├── tests/              # pytest, xUnit, golden files
├── docs/               # Generated documentation
└── artifacts/          # Output JSON files
```

**Structure Decision**: Single project in Documentron/ with clear separation of orchestration (Python), analysis (C#), and artifacts. All implementation and outputs reside in Documentron/ subfolder for compliance with constitution.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |
