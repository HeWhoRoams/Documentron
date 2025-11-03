# Feature Specification: Asset Conversion

**Feature Branch**: `002-asset-conversion`  
**Created**: 2025-11-03  
**Status**: Draft  
**Input**: User description: "Convert non-code assets (docx/xlsx/vdx) into normalized artifacts"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Convert Supported Assets (Priority: P1)

Detect and convert all supported non-code files (docx, xlsx, vdx) in the repository into normalized, machine-readable JSON artifacts with provenance and stable IDs.

**Why this priority**: Enables downstream documentation and synthesis workflows by providing structured, citeable asset data.

**Independent Test**: Run asset conversion on a sample repo and verify that all supported files produce valid JSON artifacts with correct provenance and stable IDs.

**Acceptance Scenarios**:

1. **Given** a repo with docx/xlsx/vdx files, **When** conversion is run, **Then** all supported files produce normalized JSON with provenance and stable IDs.
2. **Given** a rerun on the same repo, **When** conversion is run, **Then** asset IDs remain stable.

---

### User Story 2 - Handle Unsupported or Oversized Files (Priority: P2)

Detect unsupported or oversized files and report actionable reasons for skipping them.

**Why this priority**: Ensures robustness and transparency, preventing workflow failures and informing users of issues.

**Independent Test**: Run conversion on a repo with unsupported/oversized files and verify that skipped files are reported with actionable reasons.

**Acceptance Scenarios**:

1. **Given** a repo with password-protected or malformed files, **When** conversion is run, **Then** files are skipped with clear reasons (e.g., "encrypted", "parse_error").
2. **Given** a repo with files exceeding size limits, **When** conversion is run, **Then** files are skipped and reported as "oversized".

---

### User Story 3 - Enforce Budgets and Limits (Priority: P3)

Enforce asset conversion budgets (max file size, total asset count, latency per file) and report violations.

**Why this priority**: Maintains system performance and prevents resource exhaustion.

**Independent Test**: Run conversion on a large repo and verify that budget violations are detected and reported.

**Acceptance Scenarios**:

1. **Given** a repo exceeding asset count or file size limits, **When** conversion is run, **Then** violations are reported and conversion halts or skips as appropriate.
2. **Given** a repo with slow conversion, **When** conversion is run, **Then** latency violations are reported in the output.

---

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- Detect all supported non-code files (docx, xlsx, vdx) in the repository, excluding bin/ and obj/ directories.
- Convert each supported file to a normalized JSON artifact with provenance (original path, sha256, extractor version).
- Write all artifacts to out/assets/ with stable IDs and schemas per file type.
- Generate out/assets.index.json listing all converted files and their stable IDs.
- Report and skip unsupported, malformed, password-protected, or oversized files with actionable reasons.
- Enforce budgets: max file size 20MB, max total assets 500, max latency 5000ms per file.
- Provide CLI and VS Code recipes for asset conversion and verification.
- Support CI workflows for automated asset conversion and verification.

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

## Key Entities *(include if feature involves data)*

- AssetFile: { original_path, sha256, extractor_version, type, metadata }
- AssetIndex: { assets: [ { id, type, path, status, reason } ] }

## Assumptions

- Supported file types are limited to docx, xlsx, vdx as specified.
- Stable IDs are based on file path and sha256 hash.
- Extractor version is recorded for provenance.
- Asset conversion is deterministic given the same input files.
- CI and CLI workflows use the same conversion logic.

## Dependencies

- Requires access to all files in the repository except bin/ and obj/ directories.
- Relies on extractor tools for docx, xlsx, vdx conversion.
- Schema definitions for asset.docx@1.0.0, asset.xlsx@1.0.0, asset.vdx@1.0.0 must be available.

## Out of Scope

- Conversion of unsupported file types (e.g., pdf, pptx, images).
- Manual asset editing or annotation.
- Asset storage outside out/assets/ directory.
