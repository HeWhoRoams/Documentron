# Tasks: Asset Conversion

**Input**: Design documents from `/specs/002-asset-conversion/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project structure in Documentron/core/asset_conversion/, Documentron/artifacts/assets/, Documentron/tests/asset_conversion/
- [X] T002 Initialize Python environment with python-docx, openpyxl, defusedxml, pytest
- [X] T003 [P] Create initial test suite in Documentron/tests/asset_conversion/

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T004 Implement CLI entry point for asset conversion in Documentron/core/asset_conversion/
- [X] T005 Implement batch file discovery logic for docx/xlsx/vdx in Documentron/core/asset_conversion/
- [X] T006 Implement JSON schema validation utilities in Documentron/core/asset_conversion/
- [X] T007 Implement artifact writer for normalized JSON output in Documentron/artifacts/assets/
- [X] T008 Implement error handling for encrypted, malformed, or oversized files in Documentron/core/asset_conversion/

---

## Phase 3: User Story 1 - Convert Supported Assets (Priority: P1) 🎯 MVP

**Goal**: Detect and convert all supported non-code files (docx, xlsx, vdx) into normalized, machine-readable JSON artifacts with provenance and stable IDs.
**Independent Test**: Run asset conversion on a sample repo and verify that all supported files produce valid JSON artifacts with correct provenance and stable IDs.

### Implementation for User Story 1

- [X] T009 [P] [US1] Implement docx conversion logic in Documentron/core/asset_conversion/docx_converter.py
- [X] T010 [P] [US1] Implement xlsx conversion logic in Documentron/core/asset_conversion/xlsx_converter.py
- [X] T011 [US1] Implement vdx conversion logic (external tool or XML parser) in Documentron/core/asset_conversion/vdx_converter.py
- [X] T012 [US1] Implement provenance and stable ID generation in Documentron/core/asset_conversion/provenance.py
- [X] T013 [US1] Write normalized JSON artifacts to Documentron/artifacts/assets/
- [X] T014 [US1] Add pytest tests for asset conversion and provenance in Documentron/tests/asset_conversion/

---

## Phase 4: User Story 2 - Handle Unsupported or Oversized Files (Priority: P2)

**Goal**: Detect unsupported or oversized files and report actionable reasons for skipping them.
**Independent Test**: Run conversion on a repo with unsupported/oversized files and verify that skipped files are reported with actionable reasons.

### Implementation for User Story 2

- [X] T015 [US2] Implement detection and reporting for unsupported file types in Documentron/core/asset_conversion/
- [X] T016 [US2] Implement detection and reporting for oversized files in Documentron/core/asset_conversion/
- [X] T017 [US2] Add pytest tests for error handling and reporting in Documentron/tests/asset_conversion/

---

## Phase 5: User Story 3 - Enforce Budgets and Limits (Priority: P3)

**Goal**: Enforce asset conversion budgets (max file size, total asset count, latency per file) and report violations.
**Independent Test**: Run conversion on a large repo and verify that budget violations are detected and reported.

### Implementation for User Story 3

- [ ] T018 [US3] Implement enforcement of max file size and asset count in Documentron/core/asset_conversion/
- [ ] T019 [US3] Implement latency tracking and reporting in Documentron/core/asset_conversion/
- [ ] T020 [US3] Add pytest tests for budget enforcement in Documentron/tests/asset_conversion/

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T021 Documentation updates in Documentron/docs/
- [ ] T022 Code cleanup and refactoring
- [ ] T023 Performance optimization across all phases
- [ ] T024 Additional unit tests in Documentron/tests/asset_conversion/
- [ ] T025 Security hardening for CLI and artifact outputs
- [ ] T026 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1): No dependencies - can start immediately
- Foundational (Phase 2): Depends on Setup completion - BLOCKS all user stories
- User Stories (Phase 3+): All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- Polish (Final Phase): Depends on all desired user stories being complete

### User Story Dependencies
- User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
- User Story 2 (P2): Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- User Story 3 (P3): Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story
- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities
- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery
1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy
With multiple developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
