<!--
Sync Impact Report:
- Version change: v1.0 → v2.0.0
- Modified principles: Added principle 9 "Workflow integrity through testing"
- Added sections: Project Structure with Documentron subfolder organization
- Removed sections: None
- Templates requiring updates:
  ✅ Updated: plan-template.md, spec-template.md (folder structure references)
  ⚠ Pending: tasks-template.md (project structure alignment)
- Follow-up TODOs: None
- Ratification Date: 2025-11-03
- Last Amended Date: 2025-11-03
-->

# Documentron — Speckit Constitution (v2.0.0)

**Ratification Date**: 2025-11-03  
**Last Amended Date**: 2025-11-03  
**Amendment Authority**: Project maintainers via RFC process  
**Review Cycle**: Quarterly or upon major architectural changes  

**Purpose**
Create a lean, repeatable system that inspects legacy C# codebases, emits deterministic artifacts, and synthesizes human-readable documentation via LLMs—without bloat. Design for **C# first**, while keeping **adapter points** for future languages. Primary UX is **VS Code + GitHub Copilot Chat**; secondary UX is **CLI-first LLM interfaces**.

---

## 1) Mission & Non-Goals

**Mission**
Turn messy repos into reliable, human-usable docs by enforcing a tight loop: **inspect → produce artifacts → synthesize docs → verify → publish**.

**Non-Goals**

* Not a full static analyzer or build system.
* No “do everything for every language.” Adapters only when justified.
* No monolith prompts or fragile mega-workflows.
* No undocumented heuristics; every heuristic must be named, versioned, and testable.

---

## 2) Scope & Targets

**MVP Scope**

* Target: **C# (.NET)** repositories that build via MSBuild.
* Inputs: repo path/branch, solution/project files, optional config.
* Outputs: machine-readable artifacts + human docs.

**Out-of-Scope (v1.x)**

* Runtime tracing, dynamic analysis, whole-fleet SARIF aggregation, auto-fix PRs.

**Future (v2.x+)**

* Language adapters (Java, TS) via a stable **`ILanguageAdapter`** interface.
* Runtime truth (API contracts, probes) and portal connectors.

---

## 3) Principles (Use to say "no")

1. **Determinism over cleverness.** Same input → same artifacts.
2. **Artifacts first.** LLMs read artifacts, not raw repos.
3. **Tight interfaces.** Every module has a minimal contract.
4. **Budgeted complexity.** New feature must pass size & latency budgets.
5. **Replaceable adapters.** Language-specific code isolated behind interfaces.
6. **Inspect > infer.** Prefer analyzers, ASTs, symbols over regex or grep.
7. **Test as guardrail.** Feature without tests is not a feature.
8. **Docs as product.** Doc synthesis is validated and versioned like code.
9. **Workflow integrity through testing.** All Speckit commands MUST be tested by running the complete workflow against this repository itself. Test cases derive from actual usage patterns and edge cases discovered during self-application.

---

## 4) Project Structure & Organization

**Root Level (Speckit Only)**
The repository root contains ONLY Speckit methodology artifacts:
* `.specify/` - Templates, scripts, and workflow infrastructure
* `specs/` - Feature specifications and documentation
* `.github/` - GitHub integration (Copilot prompts, workflows)
* `.vscode/` - VS Code configuration

**Documentron Subfolder (All Implementation)**
ALL implementation code, artifacts, and deliverables MUST reside in `Documentron/`:

```
Documentron/
├── core/
│   ├── inspection/     # C# inspectors (Roslyn/MSBuild)
│   ├── artifacts/      # schemas, validators, writers
│   ├── synthesis/      # prompt builders, LLM runners
│   └── verification/   # structural checks, doc coverage
├── adapters/
│   └── csharp/        # concrete ILanguageAdapter for C#
├── ux/
│   ├── vscode/        # Copilot Chat recipes, tasks
│   └── cli/           # deterministic commands
├── tests/             # All test artifacts
├── docs/              # Generated documentation
└── artifacts/         # Runtime inspection outputs
```

This separation ensures:
- Clean distinction between methodology (root) and implementation (Documentron/)
- Easy methodology reuse for other projects
- Clear boundaries for testing scope

---

## 5) Operating Model (Speckit)

**Phases**

* **Constitution** → **Spec** → **Plan** → **Implement**

**Stage Gates**

* **G1: Spec Ready:** Artifacts and schemas defined, budgets set.
* **G2: Plan Ready:** Tasks, tests, prompts, acceptance criteria locked.
* **G3: Implement Complete:** CI green, quality metrics met, docs generated.
* **G4: Release Ready:** Versioned artifacts + docs, changelog, checksum.

**Gate Rules**

* Failing a gate halts merge; only Product/Tech lead can waive with rationale file.

---

## 6) Architecture (High-Level)

**Modules**

* `Documentron/core/inspection`: C# inspectors (Roslyn/MSBuild), collectors, normalizers.
* `Documentron/core/artifacts`: schemas, validators, writers (JSON/YAML).
* `Documentron/core/synthesis`: prompt builders, LLM runners, reducers, post-processors.
* `Documentron/core/verification`: structural checks, doc coverage, hallucination guards.
* `Documentron/adapters/csharp`: concrete `ILanguageAdapter` for C#.
* `Documentron/adapters/*`: future languages.
* `Documentron/ux/vscode`: Copilot Chat recipes, tasks, code lenses.
* `Documentron/ux/cli`: deterministic commands mirroring chat recipes.
* `Documentron/ci`: pipelines, budgets, gate checks.

**ILanguageAdapter (contract)**

```csharp
public interface ILanguageAdapter {
  bool CanOpen(string repoPath);
  BuildInfo DiscoverBuildUnits(string repoPath);      // solutions, projects
  SymbolGraph AnalyzeSymbols(BuildInfo build);        // types, members, refs
  ApiSurface ExtractApis(SymbolGraph graph);
  DependencyMap ResolveDependencies(BuildInfo build); // intra/inter-project
  IEnumerable<Finding> CollectHeuristics(SymbolGraph graph); // smells, risks
}
```

---

## 7) Artifacts (Authoritative Truth)

**Required**

* `build.info.json` – solutions/projects/targets.
* `symbol.graph.json` – types, members, relations (call/uses/inherits).
* `api.surface.json` – public APIs, visibility, obsolescence.
* `deps.map.json` – project/package/dependency edges + version pins.
* `risk.findings.json` – smells (with rule id, evidence, severity).
* `doc.plan.json` – which docs to generate and from what sections.
* `quality.report.json` – metrics (budgets, coverage, latencies).

**Schema Rules**

* Version each schema: `"schema": "symbol.graph@1.0.0"`.
* Artifacts validated before any LLM step; invalid → fail the run.

---

## 8) Quality Budgets & Metrics (Hard Stops)

* **Build discoverability:** ≥ 98% projects load via MSBuildWorkspace.
* **Symbol resolution:** ≥ 97% named symbols resolved.
* **API coverage in docs:** ≥ 90% of public APIs mentioned or intentionally excluded.
* **Latency:** ≤ 30s per 1k LOC for inspect+artifact (cold cache, mid-spec machine).
* **LLM determinism:** temperature ≤ 0.2; seed pinned when supported.
* **Hallucination rate:** ≤ 1 critical factual error per 50k tokens (verified).
* **Binary size growth:** Module adds ≤ 300 LOC net without budget review.
* **Prompt set size:** ≤ 12 primary prompts; require RFC to add more.

Failing any **hard stop** blocks merge until corrected or waived with written rationale.

---

## 9) LLM Governance

* **Input**: Only artifacts + minimal code excerpts (cited).
* **Prompt Structure**: system → constraints → artifacts → task → format spec.
* **Determinism**: low temp, max tokens capped, retry with jitter x2 then fail.
* **Provenance**: every output carries `inputs[]` hashes + prompt version.
* **Safety**: no repo exfiltration; redact secrets; model IDs logged.
* **Grounding**: require “citation lines” back to artifact path + key.

---

## 10) Verification & Tests

* **Unit**: schema validators, adapter mocks, prompt builders.
* **Golden Files**: known repos → pinned artifact snapshots; diff on PR.
* **Doc Checks**: link checker, section presence, glossary references.
* **Hallucination Tests**: adversarial fixtures with traps; must be flagged.
* **Performance**: budget tests fail CI if thresholds exceeded.
* **Smoke (real repos)**: nightly run against 3 public C# samples.
* **Workflow Self-Testing**: Complete Speckit workflow (specify → plan → tasks → implement) MUST be tested against this repository itself. Test cases include:
  - Feature creation with edge-case names and descriptions
  - Plan generation with various technology stacks
  - Task breakdown for different project types
  - Template consistency validation
  - Script error handling and recovery scenarios
  - PowerShell script execution across different environments

---

## 11) Interfaces

### 11.1 VS Code + Copilot Chat (Primary UX)

**Recipes (names are stable API):**

* `appdoc.inspect` → produce artifacts only.
* `appdoc.summarize` → synthesize docs from current artifacts.
* `appdoc.verify` → run validators + budgets; print blockers.
* `appdoc.report` → generate human summary + links to artifacts.
* `appdoc.diff` → compare artifacts vs prior run; highlight deltas.

Each recipe maps 1:1 to a CLI command.

### 11.2 CLI (Secondary UX)

Commands (deterministic, no ambient state):

```
appdoc inspect --repo . --out ./out --adapter csharp --no-cache
appdoc synthesize --artifacts ./out --profile default --out ./docs
appdoc verify --artifacts ./out --strict
appdoc report --artifacts ./out --docs ./docs --format md
appdoc diff --old ./out_prev --new ./out
```

Exit codes: `0=ok, 2=quality-fail, 3=invalid-artifact, 4=adapter-missing, 5=timeout`.

---

## 12) Extensibility (Language Adapters)

* New adapter must implement `ILanguageAdapter` and provide:

  * `adapter.config.json` (capabilities, min schema versions).
  * **3 proof repos** + golden files.
  * Performance report vs budgets.
* Adapters loaded via discovery (MEF/reflection) with **sandboxing**.

---

## 13) Documentation Standards

* **Diátaxis** structure: Tutorials, How-to, Reference, Explanations.
* Every synthesized doc must:

  * Declare **scope**, **source artifacts**, **assumptions**, **limits**.
  * Include **“Where this may be wrong”** section.
* Changelog per release with schema & prompt versions.

---

## 14) Branching, Versioning, Releases

* **Branching**: `feature/*` per new spec; PR requires G1–G3 passes.
* **Versioning**: SemVer for product; independent SemVer for schemas & prompts.
* **Release (G4)** requires:

  * Checksums for artifacts.
  * Doc site build green.
  * “What changed / Why it’s safe” note.
  * Rollback command documented.

---

## 15) Security & Privacy

* Never send full repo to LLM; only redacted excerpts + artifacts.
* Secret scanners on inputs; block if secrets detected.
* Local model support preferred; cloud models must be configurable and logged.
* PII policy file respected; artifacts can mark fields `redacted: true`.

---

## 16) Decision Rubrics

A **new feature** merges only if:

* Cuts average doc production time OR improves doc accuracy measurably.
* Fits under **budgets** and **prompt count cap**.
* Is adapter-agnostic or strictly in an adapter.
* Has tests + golden files.
* Has a rollback plan.
  If “no” on any, reject or spin as experiment behind a flag.

---

## 17) Risks & Mitigations

* **Bloat creep** → Prompt cap, module LOC budget, quarterly prune.
* **Adapter sprawl** → Require 3-repo proofs + perf report.
* **LLM drift** → Pin model/version; periodic re-baselining runs.
* **Hallucinations** → Artifact-only grounding, adversarial tests, verifiers.
* **Latency spikes** → Budget tests fail CI; perf profiling required.

---

## 18) Minimal Config (per repo)

```json
{
  "appdoc": {
    "language": "csharp",
    "budgets": { "latency_ms_per_kloc": 30000 },
    "docs": { "profiles": ["default"] },
    "llm": { "provider": "local/azure/openai", "temperature": 0.2, "seed": 42 }
  }
}
```

---

## 19) Release Readiness Checklist

* [ ] All artifacts valid, versioned, and checksummed.
* [ ] Quality report: all budgets pass.
* [ ] Docs built with provenance and citations.
* [ ] Changelog + upgrade notes.
* [ ] Rollback verified.

---

## 20) Copilot Chat Recipes (authoritative prompts)

**`appdoc.inspect` (system summary)**

* Role: strict inspector.
* Inputs: repo path, adapter config.
* Constraints: emit only artifacts; fail fast on invalid schema; no free-text.
* Output: list of generated files + metrics.

**`appdoc.summarize`**

* Role: technical writer.
* Inputs: artifacts (paths), glossary.
* Constraints: artifact-grounded, cite artifact keys, low temp.
* Output: Diátaxis-aligned MD files with “Where this may be wrong”.

**`appdoc.verify`**

* Role: auditor.
* Inputs: artifacts + budgets.
* Output: table of pass/fail; exit code semantics.

(Keep total primary recipes ≤ 12.)

---

## 21) Governance & Change Control

* **RFC** required to: add a primary prompt, raise budgets, or add an adapter.
* **Quarterly prune**: remove dead code, demote unused prompts, shrink deps.
* **Single owner** per module; bus factor ≥ 2 via documented runbooks.

---

## 22) Roadmap Guardrails

* **v1.0–1.2**: C# adapter, core artifacts, VS Code recipes, CLI parity, CI gates.
* **v1.3–1.5**: Hardening, golden repos, doc site v1, local-LLM path.
* **v2.x**: Additional language adapters via `ILanguageAdapter`, runtime truth.

---

## 23) Smallest Decisive Next Step

1. Scaffold `Documentron/core/*`, `Documentron/adapters/csharp`, `Documentron/ux/vscode`, `Documentron/ux/cli`, `Documentron/ci/`.
2. Implement `ILanguageAdapter` (C#) with **only**: `DiscoverBuildUnits`, `AnalyzeSymbols`, `ExtractApis`.
3. Emit and validate **four** artifacts: `build.info.json`, `symbol.graph.json`, `api.surface.json`, `quality.report.json`.
4. Wire `appdoc.inspect` recipe + CLI; add budgets; add golden test on one public C# repo.
5. **Test the Speckit workflow against this repository** to validate template consistency and script functionality.
   Stop if budgets fail—fix before moving on.

---

### Stop/Continue Criteria

* **Stop**: any PR increases prompt count or module LOC over caps without RFC.
* **Continue**: doc accuracy or time-to-doc measurably improves; budgets pass.

---

## Appendix A — Artifact Keys (thumbnail)

```json
// symbol.graph@1.0.0
{
  "schema":"symbol.graph@1.0.0",
  "assemblies":[{"name":"MyLib","version":"1.2.3"}],
  "types":[
    {"id":"T:MyLib.Service","kind":"class","members":["M:MyLib.Service.Run()"],"access":"public"}
  ],
  "relations":[{"from":"M:MyLib.Service.Run()","to":"M:MyLib.Util.Log()","kind":"calls"}]
}
```

---

## Appendix B — CLI Contract (deterministic)

* All commands accept `--json` to emit machine logs.
* All outputs write to a target directory; no stdout prose unless `report`.
* Artifacts include SHA256 and creation timestamps (UTC).

---

## Appendix C — Definition of Done (per feature)

* Tests (unit + golden) exist and pass.
* Budgets pass in CI.
* Docs updated (reference + how-to).
* No new primary prompts.
* Rollback plan documented.

---

### License of the Constitution

CC-BY-SA for the document text; code adheres to repo license.

---

**This constitution is intentionally lean.** If you feel the urge to add “one more thing,” run it through the **Decision Rubrics** and **Budgets** first. If it doesn’t make the system faster, clearer, or more accurate, it doesn’t ship.

---

**Smallest next commit to make this real:**
Create `ILanguageAdapter` + `Documentron/adapters/csharp` skeleton, wire `appdoc inspect` CLI to output `build.info.json`, `symbol.graph.json`, `api.surface.json`, and `quality.report.json`, with schema validation and a single golden-file test.
