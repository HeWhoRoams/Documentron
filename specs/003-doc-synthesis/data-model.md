# Data Model: Doc Synthesis

## Entities

### Artifact
- Fields: 
  - file_name: string, the artifact file name (e.g., "build.info.json")
  - json_pointer: string, JSONPath to the specific data element (e.g., "/apis/0")
  - type: string, semantic classification of the artifact content (allowed values: "build_info", "symbol_graph", "api_surface", "deps_map", "quality_report", "assets_json"). Rationale: Distinguishes artifact purposes for synthesis logic; consumers should use this to route processing (e.g., API docs from "api_surface" artifacts).
  - hash: string, SHA256 hash of the artifact content for provenance
- Relationships: Used as source for documentation sections

### Documentation
- Fields: doc_type (overview, architecture, api-reference, dependencies, maintenance-notes), content, citations, provenance, confidence_signals, hash
- Relationships: Generated from one or more Artifacts

### API
- Fields: 
  - name: string, API identifier (e.g., method or class name)
  - description: string, human-readable description
  - coverage_status: string enum, API documentation coverage status (allowed values: "covered" - fully documented with examples; "partial" - documented but incomplete; "excluded" - intentionally not documented; "unknown" - coverage not assessed). Non-nullable, default "unknown".
  - exclusion_reason: string, required only when coverage_status == "excluded" (optional/nullable otherwise). Max 500 characters, explains why the API is excluded (e.g., "internal use only").
- Relationships: Referenced in api-reference.md, cross-checked with api.surface.json. These rules must be reflected in api.surface.json schema and api-reference.md generation for consistency.

### Verification
- Type: Entity (data record of verification results)
- Purpose: Records the outcome of automated and manual checks on generated documentation for quality assurance
- Fields: id (string, unique verification run ID), status (string enum: "passed", "failed", "pending"), reporter (string, system or user who performed verification), timestamp (ISO 8601 string), related_document_id (string, ID of the Documentation entity being verified), result (object, detailed check results), notes (string, optional human notes)
- Lifecycle: Entered after Documentation generation (triggered by "verify" step in CLI); exits when status != "pending" (passed/failed)
- Relationships: One-to-one with Documentation (verifies a specific doc), generates Reports (quality.report.json)

## Validation Rules
- Every documentation section must cite at least one artifact (file + JSON pointer)
- All claims must be traceable to artifacts
- API coverage must be ≥90% or exclusions justified
- Provenance and confidence signals required for every doc
- Hashes must match for identical input runs

## State Transitions
- Artifacts → Documentation (via synthesis)
- Documentation → Verification (via report)
