---

# Tasks: Repository Inspection and Artifact Generation

**Input**: Design documents from `/specs/001-repo-inspection/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project structure in Documentron/core/, Documentron/adapters/csharp/, Documentron/artifacts/
- [X] T002 Initialize Python environment with pythonnet, jsonschema, pytest
- [X] T003 [P] Initialize C# project for Roslyn/MSBuild analyzers in Documentron/adapters/csharp/
- [X] T004 [P] Configure VS Code workspace and Copilot Chat prompt for orchestration
- [X] T005 [P] Create initial test suite in Documentron/tests/

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T006 Implement CLI entry point for Python orchestrator in Documentron/core/inspection/
- [X] T007 Implement C# analyzer CLI for Roslyn/MSBuild in Documentron/adapters/csharp/
- [X] T008 [P] Implement JSON schema validation utilities in Documentron/core/artifacts/
- [X] T009 [P] Implement pytest and xUnit test runners in Documentron/tests/
- [X] T010 [P] Implement artifact writers for build.info.json, symbol.graph.json, api.surface.json, deps.map.json, quality.report.json in Documentron/artifacts/
- [X] T011 [P] Implement OpenAPI endpoint /inspect in Documentron/adapters/csharp/

---

## Phase 3: User Story 1 - Basic Repository Analysis (Priority: P1) 🎯 MVP

**Goal**: Analyze C# solution and emit canonical artifacts
**Independent Test**: Run Copilot Chat prompt and verify all five artifacts are generated and schema-valid

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement solution discovery logic in Documentron/adapters/csharp/
- [X] T013 [P] [US1] Implement project discovery logic in Documentron/adapters/csharp/
- [X] T014 [US1] Implement symbol extraction logic in Documentron/adapters/csharp/
- [X] T015 [US1] Implement API surface extraction in Documentron/adapters/csharp/
- [X] T016 [US1] Implement dependency mapping in Documentron/adapters/csharp/
- [X] T017 [US1] Integrate Python orchestrator with C# analyzer CLI
- [X] T018 [US1] Write build.info.json, symbol.graph.json, api.surface.json, deps.map.json, quality.report.json to Documentron/artifacts/
- [X] T019 [US1] Validate all artifacts against schemas using jsonschema
- [X] T020 [US1] Add pytest/xUnit tests for artifact generation and schema validation

---

## Phase 4: User Story 2 - Quality Budget Validation (Priority: P2)

**Goal**: Validate symbol resolution, project discovery, and latency budgets
**Independent Test**: Run analysis on known repo and verify metrics in quality.report.json

### Implementation for User Story 2

- [X] T021 [P] [US2] Implement quality metric calculation in Documentron/core/verification/
- [X] T022 [US2] Integrate budget checks into Python orchestrator
- [X] T023 [US2] Add pytest/xUnit tests for budget validation
- [X] T024 [US2] Implement error handling for budget violations in Documentron/core/verification/

---

## Phase 5: User Story 3 - Schema Validation and Deterministic Output (Priority: P3)

**Goal**: Validate schema conformance and deterministic output
**Independent Test**: Run multiple analyses and verify identical artifact checksums

### Implementation for User Story 3

- [X] T025 [P] [US3] Implement schema validation logic in Documentron/core/artifacts/
- [X] T026 [US3] Implement checksum calculation and comparison in Documentron/core/verification/
- [X] T027 [US3] Add pytest/xUnit tests for determinism and schema validation
- [X] T028 [US3] Implement error handling for schema validation failures

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T029 [P] Documentation updates in Documentron/docs/
- [X] T030 Code cleanup and refactoring
- [X] T031 Performance optimization across all phases
- [X] T032 [P] Additional unit tests in Documentron/tests/
- [X] T033 Security hardening for CLI and API endpoints
- [X] T034 Run quickstart.md validation

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

## Parallel Example: User Story 1

- [ ] T012 [P] [US1] Implement solution discovery logic in Documentron/adapters/csharp/
- [ ] T013 [P] [US1] Implement project discovery logic in Documentron/adapters/csharp/

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
