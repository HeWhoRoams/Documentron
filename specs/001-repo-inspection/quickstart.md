# Quickstart: Repository Inspection and Artifact Generation

## Prerequisites
- Windows 10+ with Python 3.11 and .NET SDK installed
- VS Code with Copilot Chat extension
- Repository containing one or more .sln files

## Steps
1. Open VS Code in the repository root
2. Run the Copilot Chat prompt: "Analyze C# project with Roslyn and MSBuild"
3. The workflow orchestrates Python scripts to invoke Roslyn/MSBuild analyzers
4. Artifacts are written to Documentron/artifacts/:
   - build.info.json
   - symbol.graph.json
   - api.surface.json
   - deps.map.json
   - quality.report.json
5. Validate artifacts using jsonschema
6. Run pytest/xUnit tests to verify outputs
7. Review quality budgets in quality.report.json

## Troubleshooting
- If no .sln files found, check repository structure
- If schema validation fails, review error messages in quality.report.json
- For performance issues, check ms_per_kloc metric
