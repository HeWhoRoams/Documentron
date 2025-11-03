# Phase 0 Research Tasks: Doc Synthesis

## Unknowns to Resolve

1. Best practices for deterministic doc synthesis from artifacts
2. Provenance and confidence signal patterns for LLM-generated docs
3. Coverage measurement for API reference docs
4. Hallucination/uncertainty flagging in LLM outputs

## Research Tasks
- Research best practices for deterministic doc synthesis from machine artifacts
- Find patterns for provenance and confidence signals in LLM-generated documentation
- Research coverage measurement and reporting for API reference docs
- Research robust hallucination/uncertainty flagging in LLM outputs

## Decision Log

Decision: Use strict artifact-only input, enforce citation for all claims, use hash-based doc comparison for determinism, include explicit provenance and 'Where this may be wrong' in every doc, measure API coverage via artifact cross-check, flag/omit hallucinated or uncited claims.
Rationale: Maximizes reliability, traceability, and trust in generated docs; aligns with Diátaxis and project constitution.
Alternatives considered: Synthesis from raw code, manual provenance, non-deterministic LLM settings.

---

### 1. Best practices for deterministic doc synthesis from artifacts
Finding: Use only machine-generated artifacts as input, enforce citation for every claim, use hash-based comparison for output determinism.

### 2. Provenance and confidence signal patterns for LLM-generated docs
Finding: Include explicit provenance (artifact file + JSON pointer) for every section, add 'Where this may be wrong' to highlight uncertainty, use low temperature and seed for LLM runs.

### 3. Coverage measurement for API reference docs
Finding: Cross-check public APIs in api.surface.json against documented APIs in api-reference.md, report coverage percentage and exclusions with rationale.

### 4. Hallucination/uncertainty flagging in LLM outputs
Finding: Require LLM to mark any uncited or uncertain claims as 'uncertain' with rationale, omit phantom APIs, and include hallucination traps in tests.
