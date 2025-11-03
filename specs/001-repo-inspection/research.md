# Research: Repository Inspection and Artifact Generation

## Unknowns & Clarifications

- Python orchestrates C# analysis via pythonnet; Roslyn and MSBuild are invoked via CLI and .NET APIs
- Artifact schemas are versioned and validated using jsonschema
- Testing uses pytest for Python orchestration and xUnit for C# analyzers
- All outputs are written to Documentron/artifacts/ for separation from methodology

## Decision Log

### Language/Version
- Chosen: Python 3.11 for orchestration, C# for analysis
- Rationale: Python enables flexible workflow scripting and integration with Copilot Chat; C# is required for Roslyn/MSBuild
- Alternatives: Bash, PowerShell, direct C# CLI

### Dependencies
- Chosen: pythonnet, Roslyn, MSBuild, jsonschema, pytest
- Rationale: pythonnet allows Python to invoke .NET APIs; Roslyn/MSBuild are industry standards for C# analysis; jsonschema ensures artifact validity; pytest provides robust test framework
- Alternatives: direct C# scripting, PowerShell, custom schema validation

### Testing
- Chosen: pytest (Python), xUnit (C#)
- Rationale: pytest is widely used for Python, xUnit for C#; both support CI/CD and golden file testing
- Alternatives: unittest, MSTest, custom test runners

### Integration Patterns
- Chosen: CLI entry points for orchestration, API boundaries for analysis
- Rationale: CLI enables easy invocation from Copilot Chat and CI/CD; API boundaries ensure modularity
- Alternatives: monolithic scripts, direct API calls without CLI

## Alternatives Considered
- Bash/PowerShell for orchestration: rejected due to limited cross-platform support and integration with Copilot Chat
- Direct C# CLI: rejected for lack of flexible orchestration and integration with Python ecosystem
- Custom schema validation: rejected in favor of jsonschema for standards compliance

## All clarifications resolved. No outstanding NEEDS CLARIFICATION markers.
