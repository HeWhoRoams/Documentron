
# Tasks: Doc Synthesis

## Organization
- Tasks are grouped by user story (P1, P2, etc.)
- Each task is independently actionable and testable
- Checklist format, with parallel opportunities marked [P]
- Tests written FIRST (must fail before implementation)

---

### User Story 1 - Deterministic Doc Synthesis (Priority: P1)

**Goal:** Synthesize documentation from machine-generated artifacts with strict determinism, provenance, and coverage.

#### Tasks
- [ ] Write failing test: Synthesis produces docs only from provided artifacts, with citations and provenance
- [ ] Write failing test: API coverage ≥90% or exclusions justified in api-reference.md
- [ ] Write failing test: Docs are byte-identical for identical inputs (hash check)
- [ ] Implement synthesis command (`/synthesize` API):
	- [ ] Accept artifacts, profile, out_dir, max_docs, temperature, seed
	- [ ] Generate docs: overview.md, architecture.md, api-reference.md, dependencies.md, maintenance-notes.md
	- [ ] Ensure every doc section cites at least one artifact (file + JSON pointer)
	- [ ] Include provenance and confidence signals in every doc
	- [ ] Enforce hash-based determinism for identical input runs
	- [ ] Flag/omit hallucinated or uncited claims
- [ ] [P] Implement artifact loader and normalizer
- [ ] [P] Implement citation and provenance generator
- [ ] [P] Implement hash-based output comparison
- [ ] [P] Implement hallucination/uncertainty trap logic
- [ ] [P] Implement API coverage cross-checker
- [ ] Write passing tests for all above

---

### User Story 2 - Doc Verification & Reporting (Priority: P2)

**Goal:** Verify synthesized docs for coverage, provenance, and hallucination; generate human-readable report.

#### Tasks
- [ ] Write failing test: Report verifies all docs have citations, provenance, and 'Where this may be wrong' sections
- [ ] Write failing test: Report confirms API coverage ≥90% or exclusions justified
- [ ] Write failing test: Report flags hallucinated/uncited claims
- [ ] Implement report command (`/report` API):
	- [ ] Accept artifacts, docs, format
	- [ ] Verify docs for citations, provenance, confidence signals
	- [ ] Check API coverage and exclusions
	- [ ] Flag hallucinated/uncited claims
	- [ ] Output human-readable report (markdown)
- [ ] [P] Implement doc verifier (citations, provenance, hallucination)
- [ ] [P] Implement API coverage/exclusion checker
- [ ] [P] Implement report generator
- [ ] Write passing tests for all above

---

### Edge Cases & Polish
- [ ] Write failing test: Synthesis fails gracefully if required artifacts missing
- [ ] Write failing test: Report fails gracefully if docs missing or malformed
- [ ] Implement error handling and edge case logic for all commands
- [ ] Polish: Documentation, code comments, README updates

---

## Parallel Opportunities
- Artifact loader/normalizer, citation/provenance generator, hash comparison, hallucination trap, and API coverage checker can be implemented in parallel (P1)
- Doc verifier, API coverage checker, and report generator can be implemented in parallel (P2)

## MVP Scope
- All P1 tasks (deterministic synthesis, provenance, coverage, hallucination trap, tests)
- P2 tasks (verification/reporting) are next after MVP

## Test-First Principle
- All implementation tasks are blocked until corresponding failing tests are written

---


# Tasks: Doc Synthesis

## Phase 1: Setup
- [X] T001 Create project structure in Documentron/core/synthesis/, Documentron/artifacts/docs/, Documentron/tests/synthesis/
- [X] T002 Initialize Python environment with markdown, jsonschema, pytest
- [X] T003 [P] Create initial test suite in Documentron/tests/synthesis/

## Phase 2: Foundational
- [X] T004 Implement CLI entry point for doc synthesis in Documentron/core/synthesis/
- [X] T005 Implement artifact loader and validator in Documentron/core/synthesis/
- [X] T006 Implement Markdown doc writer with citation support in Documentron/artifacts/docs/
- [X] T007 Implement provenance and confidence signal logic in Documentron/core/synthesis/
- [X] T008 Implement error handling for missing, malformed, or adversarial artifacts in Documentron/core/synthesis/

## Phase 3: User Story 1 - Deterministic Doc Synthesis (Priority: P1)
**Goal**: Synthesize docs strictly from artifacts, with citations, provenance, and confidence signals.
**Independent Test**: Run synthesis on sample artifacts; verify docs cite artifact paths and include provenance/confidence signals.
- [X] T009 [P] [US1] Implement overview.md synthesis logic in Documentron/artifacts/docs/
- [X] T010 [P] [US1] Implement architecture.md synthesis logic in Documentron/artifacts/docs/
- [X] T011 [P] [US1] Implement api-reference.md synthesis logic in Documentron/artifacts/docs/
- [X] T012 [P] [US1] Implement dependencies.md synthesis logic in Documentron/artifacts/docs/
- [X] T013 [P] [US1] Implement maintenance-notes.md synthesis logic in Documentron/artifacts/docs/
- [X] T014 [US1] Add pytest tests for doc synthesis and provenance in Documentron/tests/synthesis/

## Phase 4: User Story 2 - Hallucination Guarding (Priority: P2)
**Goal**: Flag or omit uncited/uncertain claims in docs.
**Independent Test**: Inject "phantom API" into repo notes; verify it is flagged as uncertain or omitted.
- [X] T015 [US2] Implement hallucination/uncertainty flagging logic in Documentron/core/synthesis/
- [X] T016 [US2] Add pytest tests for hallucination traps in Documentron/tests/synthesis/

## Phase 5: User Story 3 - API Coverage Reporting (Priority: P3)
**Goal**: Ensure ≥90% public APIs appear in api-reference.md or are explicitly excluded with reason.
**Independent Test**: Run coverage report; verify ≥90% public APIs are documented or excluded with rationale.
- [X] T017 [US3] Implement API coverage measurement and reporting in Documentron/core/synthesis/
- [X] T018 [US3] Add pytest tests for API coverage in Documentron/tests/synthesis/

## Phase 6: Polish & Cross-Cutting Concerns
- [X] T019 Documentation updates in Documentron/docs/
- [X] T020 Code cleanup and refactoring
- [X] T021 Performance optimization across all phases
- [X] T022 Additional unit tests in Documentron/tests/synthesis/
- [X] T023 Security hardening for CLI and doc outputs
- [X] T024 Run quickstart.md validation

## Dependencies
- User Story 1 (P1) is MVP and must be completed first
- User Story 2 (P2) and User Story 3 (P3) can proceed in parallel after P1

## Parallel Opportunities
- Tasks marked [P] can be executed in parallel

## Implementation Strategy
- MVP: Complete all P1 tasks for deterministic doc synthesis
- Incremental: Add hallucination guarding and API coverage reporting after MVP
