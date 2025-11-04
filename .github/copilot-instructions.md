# Documentron - AI Coding Agent Guidelines

## Project Overview

**Documentron** (formerly AppDocU) is a lean, deterministic C# codebase inspection and documentation system that emits structured artifacts for LLM consumption. Built with **Speckit methodology** - a spec-driven development approach with strict quality gates.

## Architecture & Core Concepts

### Speckit Development Workflow
- **Constitution → Spec → Plan → Implement** phases with strict gates
- Feature branches follow `###-feature-name` pattern (e.g., `001-user-auth`)
- Each feature gets a `specs/###-feature-name/` directory with structured documentation
- **Quality budgets** are hard stops - must pass before merge

### Core Modules (Planned)
```
Documentron/core/inspection/    # C# inspectors (Roslyn/MSBuild), collectors, normalizers
Documentron/core/artifacts/     # schemas, validators, writers (JSON/YAML)  
Documentron/core/synthesis/     # prompt builders, LLM runners, reducers
Documentron/core/verification/  # structural checks, doc coverage, hallucination guards
Documentron/adapters/csharp/    # concrete ILanguageAdapter for C#
Documentron/ux/vscode/         # Copilot Chat recipes, tasks, code lenses
Documentron/ux/cli/            # deterministic commands mirroring chat recipes
```

### Critical Artifacts (Authoritative Truth)
- `build.info.json` - solutions/projects/targets
- `symbol.graph.json` - types, members, relations (call/uses/inherits)
- `api.surface.json` - public APIs, visibility, obsolescence
- `deps.map.json` - project/package/dependency edges + version pins
- `risk.findings.json` - smells (with rule id, evidence, severity)
- `quality.report.json` - metrics (budgets, coverage, latencies)

## Development Commands & Scripts

### PowerShell Scripts (Windows-focused)
```powershell
# Create new feature
.\.specify\scripts\powershell\create-new-feature.ps1 "Feature description"

# Setup implementation plan
.\.specify\scripts\powershell\setup-plan.ps1 -Json

# Check prerequisites 
.\.specify\scripts\powershell\check-prerequisites.ps1 -RequireTasks

# Update agent context files
.\.specify\scripts\powershell\update-agent-context.ps1 -AgentType copilot
```

### VS Code Integration
- Terminal auto-approval for `.specify/scripts/` directories
- Chat prompt file recommendations enabled for speckit templates
- Five core prompt templates: constitution, specify, plan, tasks, implement

## Critical Principles

1. **Determinism over cleverness** - Same input → same artifacts
2. **Artifacts first** - LLMs read artifacts, not raw repos  
3. **Budgeted complexity** - Hard stops on latency, size, prompt count
4. **Test as guardrail** - Features without tests don't ship
5. **Replaceable adapters** - Language-specific code isolated behind `ILanguageAdapter`

## Quality Budgets (Hard Stops)

- **Latency**: ≤ 30s per 1k LOC for inspect+artifact
- **Symbol resolution**: ≥ 97% named symbols resolved
- **API coverage**: ≥ 90% of public APIs in docs
- **LLM determinism**: temperature ≤ 0.2
- **Binary size**: ≤ 300 LOC net per module without review
- **Prompt set**: ≤ 12 primary prompts total

## Feature Specification Patterns

### User Story Structure
Each feature must have **prioritized, independently testable** user stories:
- P1, P2, P3 priorities where P1 is MVP
- Each story deliverable independently  
- "Independent Test" criteria for each story
- Given/When/Then acceptance scenarios

### Implementation Plan Structure
Technical context must specify:
- Language/Version, Primary Dependencies, Storage, Testing
- Target Platform, Performance Goals, Constraints, Scale/Scope  
- Project structure (single/web/mobile patterns)
- Constitution compliance check

### Task Organization
- Tasks grouped by user story for independent implementation
- Phase structure: Setup → Foundational → User Stories → Polish
- Parallel opportunities marked with `[P]`
- Tests written FIRST (must fail before implementation)

## LLM Integration Guidelines

### Chat Recipes (Stable API)
- `appdoc.inspect` → produce artifacts only
- `appdoc.summarize` → synthesize docs from artifacts
- `appdoc.verify` → run validators + budgets
- `appdoc.report` → generate human summary
- `appdoc.diff` → compare artifact deltas

### LLM Governance
- Input: Only artifacts + minimal cited code excerpts
- Structure: system → constraints → artifacts → task → format
- Provenance: outputs carry input hashes + prompt versions
- Grounding: require citations back to artifact paths

## Project Status & Implementation

**Current State**: Constitution and templates defined, no implementation yet  
**Next Steps**: Scaffold modules, implement `ILanguageAdapter` for C#, emit core artifacts  
**Target Platform**: Windows/PowerShell primary, VS Code + GitHub Copilot Chat UX

## Project Structure & Organization

**Root Level (Speckit Only)**
- `.specify/` - Templates, scripts, and workflow infrastructure
- `specs/` - Feature specifications and documentation  
- `.github/` - GitHub integration (Copilot prompts, workflows)
- `.vscode/` - VS Code configuration

**Documentron Subfolder (All Implementation)**
ALL implementation code, artifacts, and deliverables reside in `Documentron/`:
- `core/` - Main system modules (inspection, artifacts, synthesis, verification)
- `adapters/` - Language-specific implementations  
- `ux/` - User interfaces (VS Code extensions, CLI tools)
- `tests/` - All test artifacts
- `docs/` - Generated documentation

## File Patterns

- `.specify/memory/constitution.md` - Core principles and architecture
- `.specify/templates/` - Spec, plan, task, and checklist templates
- `.specify/scripts/powershell/` - Windows development workflow scripts
- `specs/###-feature-name/` - Feature documentation directories
- Feature files: `spec.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`

## Code Style & Conventions

- **C# first** with MSBuild/Roslyn integration
- Deterministic artifact schemas with versioning (`"schema": "symbol.graph@1.0.0"`)
- PowerShell scripts follow error handling and path resolution patterns
- JSON output modes for script automation
- Escape and validate all user inputs in string replacements

## Chat Shortcut

- `/appdoc` or `appdoc.run` should trigger the full workflow: inspect → convert → synthesize → verify → report. When possible, run the VS Code task `AppDoc: Run All` and stream output to chat. Use `Documentron/artifacts` for artifacts and `Documentron/docs` for docs.
