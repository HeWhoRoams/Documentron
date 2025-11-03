
# Feature Specification: Doc Synthesis

**Feature Branch**: `feature/03-doc-synthesis`  
**Created**: 2025-11-03  
**Status**: Proposed  
**Input**: Generate human-readable docs grounded in deterministic artifacts

## Purpose
Use only deterministic artifacts (code + converted assets) to synthesize Diátaxis-aligned, human-readable documentation with explicit provenance and confidence signals.

## User Stories

### User Story 1 - Deterministic Doc Synthesis (Priority: P1)
**As a** technical writer or developer,
**I want** to generate documentation strictly from machine-generated artifacts,
**So that** all claims are traceable, reproducible, and grounded in authoritative sources.

**Why this priority**: Ensures trust, reproducibility, and compliance with project constitution.
**Independent Test**: Run synthesis on provided artifacts; verify docs cite artifact paths and include provenance/confidence signals.

**Acceptance Scenarios**:
1. **Given** all required artifacts exist, **When** synthesis is run, **Then** docs are generated with citations and provenance.
2. **Given** identical input artifacts, **When** synthesis is run twice, **Then** docs are byte-identical or have identical semantic hashes.

### User Story 2 - Hallucination Guarding (Priority: P2)
**As a** reviewer,
**I want** the system to flag or omit any uncited or uncertain claims,
**So that** documentation does not contain hallucinated or unverifiable information.

**Why this priority**: Prevents misinformation and increases reliability of generated docs.
**Independent Test**: Inject "phantom API" into repo notes; verify it is flagged as uncertain or omitted.

**Acceptance Scenarios**:
1. **Given** adversarial input with phantom API, **When** synthesis is run, **Then** phantom API is flagged or omitted with rationale.

### User Story 3 - API Coverage Reporting (Priority: P3)
**As a** project owner,
**I want** to ensure ≥90% public APIs are documented or explicitly excluded with reason,
**So that** API reference docs are comprehensive and exclusions are justified.

**Why this priority**: Ensures completeness and transparency of API documentation.
**Independent Test**: Run coverage report; verify ≥90% public APIs are documented or excluded with rationale.

**Acceptance Scenarios**:
1. **Given** api.surface.json and api-reference.md, **When** coverage is checked, **Then** ≥90% APIs are documented or exclusions are justified.

### Edge Cases
- Missing or malformed artifacts
- Docs missing citations or provenance
- Hallucinated claims not flagged

## Functional Requirements
- System MUST synthesize documentation only from provided machine-generated artifacts
- System MUST cite artifact file paths and JSON pointers for every claim
- System MUST include provenance and confidence signals in every doc section
- System MUST ensure docs are byte-identical or have identical semantic hashes for identical inputs
- System MUST flag or omit hallucinated or uncited claims
- System MUST report API coverage and justify exclusions if <90%
- System MUST include 'Where this may be wrong' section in each doc

## Key Entities
- **Artifact**: file_name, json_pointer, type, hash
- **Documentation**: doc_type, content, citations, provenance, confidence_signals, hash
- **API**: name, description, coverage_status, exclusion_reason

## Success Criteria
- All docs render, contain citations to artifacts, and include 'Where this may be wrong'
- No uncited normative claims about APIs or dependencies
- Two consecutive runs with same inputs produce byte-identical docs OR identical semantic hashes
- API coverage ≥90% or exclusions justified

## Assumptions
- All required artifacts are present and valid
- LLM temperature is set to 0.2 for determinism
- Optional assets may be included if present

## Dependencies and Constraints
- Inputs: out/build.info.json, out/symbol.graph.json, out/api.surface.json, out/deps.map.json, out/quality.report.json, optional out/assets/
- Outputs: docs/overview.md, docs/architecture.md, docs/api-reference.md, docs/dependencies.md, docs/maintenance-notes.md
- Budgets: max_docs=6, max_tokens_per_doc=4000, retry_policy: 2 attempts, 500ms backoff

## Notes
- Documentation must be strictly grounded in artifacts; no invention of APIs, flows, or dependencies
- Every section must cite artifact paths and keys
- Each doc must include a 'Where this may be wrong' section

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]
**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]
---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]
**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---
**Acceptance Scenarios**:


### Edge Cases
-->


## Requirements *(mandatory)*
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
