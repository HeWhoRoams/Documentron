# Documentron

A lean, deterministic C# codebase inspection and documentation system that emits structured artifacts for LLM consumption.

## Overview

Documentron inspects legacy C# codebases, produces machine-readable artifacts, and synthesizes human-readable documentation using LLMs. It enforces strict determinism, traceability, and quality budgets.

## Features

- **Inspection**: Analyze C# projects and generate artifacts (build info, symbol graphs, API surfaces, dependencies, quality reports)
- **Synthesis**: Generate Diátaxis-aligned docs (overview, architecture, API reference, dependencies, maintenance notes) from artifacts
- **Verification**: Validate docs for coverage, provenance, and hallucination
- **Determinism**: Same inputs produce identical outputs
- **Traceability**: Every claim cites artifact sources

## Quick Start

### Prerequisites

- .NET 6+ (for C# inspection)
- Python 3.11+ (for doc synthesis)
- VS Code with GitHub Copilot Chat (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HeWhoRoams/Documentron.git
   cd Documentron
   ```

2. Set up Python environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install markdown jsonschema pytest
   ```

3. Build C# components:
   ```bash
   dotnet build Documentron.sln
   ```

### Usage

#### One-liner (end-to-end)

```bash
# From repo root
python Documentron/ux/cli/appdoc.py
# or on Windows PowerShell
./appdoc.ps1

# Steps run: inspect → convert → synthesize → verify → report
# Artifacts: Documentron/artifacts
# Docs:      Documentron/docs
```

#### Run specific steps only

```bash
python Documentron/ux/cli/appdoc.py --steps inspect
python Documentron/ux/cli/appdoc.py --steps synthesize report
python Documentron/ux/cli/appdoc.py --skip verify
```

### VS Code Integration

Use GitHub Copilot Chat with the prompt in `.github/prompts/appdoc.prompt.md`, or run the task:
- Command Palette → `Tasks: Run Task` → `AppDoc: Run All`
- Copilot Chat: “/appdoc … run the 'AppDoc: Run All' task and stream output.”

## Architecture

- **adapters/csharp/**: C# inspection logic
- **core/synthesis/**: Python doc synthesis
- **core/artifacts/**: Doc writers and schemas
- **ux/vscode/**: VS Code extensions
- **ux/cli/**: Command-line tools

## Current Implementation Status

**Note**: The quality.report.json artifact currently contains placeholder metric values until real computation is implemented. The JSON includes a `"placeholder": true` flag and explanatory note. Metrics will be computed from actual analyzer/runtime data in future updates:

- `symbol_resolution_rate`: Ratio of successfully resolved symbols to total symbols
- `project_discovery_rate`: Ratio of discovered projects to expected projects  
- `ms_per_kloc`: Milliseconds per thousand lines of code (performance metric)

## Contributing

Follow the Speckit workflow:
1. `/speckit.specify` - Define feature
2. `/speckit.plan` - Plan implementation
3. `/speckit.tasks` - Break down tasks
4. `/speckit.implement` - Build feature
5. `/speckit.clarify` - Handle clarifications

## License

[Add license information]
