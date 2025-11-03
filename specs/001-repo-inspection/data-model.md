# Data Model: Repository Inspection and Artifact Generation

## Entities

### Solution
- Fields: name, path, version, projects[]
- Relationships: contains projects

### Project
- Fields: name, path, targets, dependencies[]
- Relationships: belongs to solution, depends on other projects/packages

### Symbol
- Fields: id, kind (class/interface/method/etc), members[], access
- Relationships: belongs to project, references other symbols

### API Surface
- Fields: public interfaces/classes/methods
- Relationships: exposed by project

### Dependency
- Fields: from, to, kind (project/package), version
- Relationships: project-to-project, package-to-project

### Quality Metric
- Fields: symbol_resolution_rate, project_discovery_rate, ms_per_kloc
- Relationships: attached to analysis run

## Validation Rules
- All entities must be present in artifacts
- All relationships must be resolvable via Roslyn/MSBuild
- All metrics must meet constitutional budgets
