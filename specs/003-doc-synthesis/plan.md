
# Implementation Plan: Doc Synthesis

**Branch**: `003-doc-synthesis` | **Date**: 2025-11-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-doc-synthesis/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Synthesize human-readable, Diátaxis-aligned documentation strictly from deterministic machine-generated artifacts, with explicit provenance, confidence signals, and coverage reporting. Prevent hallucinated claims and ensure reproducibility and traceability.

## Technical Context

**Language/Version**: Python 3.11, C# (adapter), PowerShell (scripts)
**Primary Dependencies**: jsonschema, pytest, markdown, OpenAPI, VS Code Copilot Chat integration
**Storage**: Filesystem (artifacts in out/, docs in docs/)
**Testing**: pytest, manual artifact validation, hash comparison
**Target Platform**: Windows (PowerShell), VS Code, CLI
**Project Type**: Single repo, modular (core, adapters, ux)
**Performance Goals**: ≤30s per 1k LOC for inspect+artifact; docs ≤4000 tokens each
**Constraints**: Determinism (same input → same output), API coverage ≥90%, LLM temperature ≤0.2, binary size ≤300 LOC/module
**Scale/Scope**: 1M LOC, 6 doc types, 5 core artifacts, parallelizable synthesis/verification

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

- Determinism over cleverness: All synthesis is artifact-driven, reproducible, and hash-checked
- Artifacts first: No raw repo inspection; only machine-generated artifacts are used
- Budgeted complexity: All modules ≤300 LOC net, ≤12 primary prompts, ≤30s/1k LOC latency
- Test as guardrail: All features require independently failing/passing tests
- Replaceable adapters: C# logic isolated behind ILanguageAdapter

**Status:** All gates satisfied for planning phase

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (Documentron subfolder)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., Documentron/core/inspection, Documentron/adapters/csharp). 
  The delivered plan must not include Option labels.
  
  NOTE: All implementation MUST be in Documentron/ subfolder. Root level is
  reserved for Speckit methodology artifacts (.specify/, specs/, .github/).
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
Documentron/
├── src/
│   ├── models/
│   ├── services/
│   ├── cli/
│   └── lib/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
Documentron/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
Documentron/
├── api/
│   └── [same as backend above]
└── ios/ or android/
    └── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
