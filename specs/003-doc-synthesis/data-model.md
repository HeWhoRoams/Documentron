# Data Model: Doc Synthesis

## Entities

### Artifact
- Fields: file_name, json_pointer, type, hash
- Relationships: Used as source for documentation sections

### Documentation
- Fields: doc_type (overview, architecture, api-reference, dependencies, maintenance-notes), content, citations, provenance, confidence_signals, hash
- Relationships: Generated from one or more Artifacts

### API
- Fields: name, description, coverage_status, exclusion_reason
- Relationships: Referenced in api-reference.md, cross-checked with api.surface.json

## Validation Rules
- Every documentation section must cite at least one artifact (file + JSON pointer)
- All claims must be traceable to artifacts
- API coverage must be ≥90% or exclusions justified
- Provenance and confidence signals required for every doc
- Hashes must match for identical input runs

## State Transitions
- Artifacts → Documentation (via synthesis)
- Documentation → Verification (via report)
