# NASA-SE Codebase Assessment Rubric

## 1. Purpose And Scope

This is a NASA-SE-aligned assessment rubric for evaluating an existing software codebase against NASA Systems Engineering Handbook principles adapted to software and agentic coding.

Required caveat: This is a NASA-SE-aligned assessment rubric. It is not official NASA certification, NASA compliance approval, or proof that a codebase or agent performs well. Source grounding is not proof of performance.

Use this rubric to inspect a real repository and score the evidence it contains or can produce. The target may be an application, library, service, agent framework, plugin, or multi-package repo. The rubric is not a replacement for tests, code review, security review, product discovery, user research, or operational validation.

## 2. Source Basis

The rubric was built from local repo artifacts indexed in `rubrics/source_scavenge_index.md`. Key local anchors include:

- `sources/nasa_systems_engineering_handbook_0.pdf`
- `extraction/source_index.md`
- `extraction/table_index.md`
- `extraction/figure_index.md`
- `extraction/pages/page_015.md`
- `extraction/pages/page_016.md`
- `extraction/pages/page_017.md`
- `extraction/pages/page_020.md`
- `extraction/pages/page_021.md`
- `extraction/pages/page_055.md`
- `extraction/pages/page_060.md`
- `extraction/pages/page_063.md`
- `extraction/pages/page_064.md`
- `extraction/pages/page_069.md`
- `extraction/pages/page_070.md`
- `extraction/pages/page_073.md`
- `extraction/pages/page_076.md`
- `extraction/pages/page_080.md`
- `extraction/pages/page_084.md`
- `extraction/pages/page_088.md`
- `extraction/pages/page_089.md`
- `extraction/pages/page_096.md`
- `extraction/pages/page_097.md`
- `extraction/pages/page_101.md`
- `extraction/pages/page_104.md`
- `extraction/pages/page_107.md`
- `extraction/pages/page_110.md`
- `extraction/pages/page_115.md`
- `extraction/pages/page_141.md`
- `extraction/pages/page_144.md`
- `extraction/pages/page_146.md`
- `extraction/pages/page_149.md`
- `extraction/pages/page_151.md`
- `extraction/pages/page_152.md`
- `extraction/pages/page_155.md`
- `extraction/pages/page_161.md`
- `extraction/pages/page_162.md`
- `extraction/pages/page_168.md`
- `extraction/pages/page_169.md`
- `extraction/pages/page_170.md`
- `extraction/pages/page_175.md`
- `extraction/pages/page_181.md`
- `extraction/pages/page_208.md`
- `extraction/pages/page_212.md`
- `extraction/pages/page_214.md`
- `extraction/pages/page_224.md`
- `extraction/pages/page_226.md`
- `extraction/pages/page_247.md`
- `extraction/pages/page_261.md`
- `extraction/pages/page_262.md`
- `extraction/pages/page_263.md`
- `.agents/skills/conops-builder/references/source-grounding.md`
- `.agents/skills/requirements-distiller/references/source-grounding.md`
- `.agents/skills/requirements-auditor/references/source-grounding.md`
- `.agents/skills/integration-planner/references/source-grounding.md`
- `.agents/skills/verification-planner/references/source-grounding.md`
- `.agents/skills/validation-planner/references/source-grounding.md`
- `.agents/skills/decision-analysis/references/source-grounding.md`
- `.agents/skills/technical-assessment-loop/references/source-grounding.md`
- `templates/requirements_matrix.yaml`
- `templates/verification_matrix.yaml`
- `templates/validation_matrix.yaml`
- `templates/interface_contract.yaml`

High-value table anchors used: Table 2.1-1, Table 4.2-1, Table 4.2-2, Table 5.3-1, Table 6.8-1, Table D-1, and Table E-1.

The source basis supports the assessment vocabulary and evidence categories. It does not establish that any assessed codebase follows those practices.

## 3. Evidence Required Before Scoring

Do not score from memory or repo reputation. Inspect the codebase and record the commit, branch, commands, and evidence paths.

Evidence checklist:

- Clean checkout instructions and dependency installation commands.
- Build, test, lint, and run commands with observed results.
- Product intent artifact: stakeholder statement, PRD, ConOps, roadmap brief, issue epic, or equivalent.
- Requirements or acceptance criteria with owners, IDs, rationale, sources, and verification methods where available.
- Traceability between intent, requirements, implementation, tests, and release/change records.
- Architecture decomposition: modules, responsibilities, data flow, dependency graph, or diagrams.
- Interface evidence: APIs, schemas, protocols, database migrations, event contracts, CLI contracts, external service dependencies, and error behavior.
- Design decision evidence: ADRs, RFCs, trade studies, dependency choice records, migration proposals, or issue discussions with alternatives.
- Build and reuse evidence: lockfiles, dependency policy, generated artifact policy, vendored code notes, SBOM or equivalent when available.
- Integration evidence: integration plan, CI workflow, migration sequence, deployment steps, compatibility tests, rollback path, and anomaly logs.
- Verification evidence: automated tests, inspection records, analysis scripts, demonstrations, CI artifacts, coverage where meaningful, and requirement-to-test mapping.
- Validation evidence: user acceptance, realistic workflow demos, beta feedback, production telemetry, support outcomes, or ConOps scenario evidence.
- Risk and resilience evidence: risk register, threat model, fault handling, incident records, backup/recovery, degraded-mode behavior, and mitigation closure.
- Configuration, technical data, and assessment evidence: tags, release notes, changelog, artifact retention, docs ownership, review minutes, health dashboards, and corrective actions.

## 4. 0-5 Scoring Scale

Use this 0-5 scoring scale for each criterion:

- 0: No credible evidence, or evidence contradicts the criterion.
- 1: Ad hoc fragments exist, but they are incomplete, stale, or disconnected from the current codebase.
- 2: Partial evidence exists for some components or workflows, with important gaps in traceability, ownership, or execution.
- 3: Adequate evidence exists for core workflows and major components; gaps are known and bounded.
- 4: Strong evidence is current, traceable, executed in normal work, and covers most high-risk paths.
- 5: Excellent evidence is current, traceable, regularly exercised, reviewed, and used to drive corrective action.

Documentation existence is not proof that the process is used. Tests are not automatically validation. A passing build is not enough to score high outside implementation/build criteria.

## 5. 100-Point Weighted Scorecard

Calculate weighted points as `weight * rating / 5`, then apply the critical caps.

| Criterion | Weight |
| --- | ---: |
| Stakeholder intent, mission need, and ConOps | 8 |
| Technical requirements definition quality | 12 |
| Requirements traceability and change management | 8 |
| Logical decomposition and architecture | 8 |
| Interface management | 10 |
| Design solution and decision analysis | 8 |
| Implementation, build, and reuse discipline | 6 |
| Integration planning and evidence | 8 |
| Verification | 12 |
| Validation | 8 |
| Technical risk, resilience, and fault handling | 6 |
| Configuration, technical data, and assessment loop | 6 |
| **Total** | **100** |

## 6. Critical Caps

Apply all relevant caps after calculating the weighted score. The final score is the lower of the weighted score and all applicable caps.

- Max 50 if the codebase cannot be built or run from a clean checkout.
- Max 60 if there is no explicit stakeholder intent, ConOps, PRD, or equivalent.
- Max 65 if there is no meaningful automated verification evidence.
- Max 70 if validation is claimed but only developer tests exist.
- Max 75 if major external interfaces are undocumented.
- Max 80 if there is no decision record for major architecture or dependency choices.
- Max 85 if risk, configuration, or change management is absent.
- Max 90 if scoring relies on documents that are not tied to current code, CI, release, or issue evidence.

## 7. Full Criteria Definitions

### Stakeholder intent, mission need, and ConOps

- Weight: 8
- NASA-SE source basis: SE engine and stakeholder expectations in `extraction/pages/page_015.md`, `extraction/pages/page_016.md`, `extraction/pages/page_055.md`, `extraction/pages/page_060.md`, `extraction/pages/page_063.md`; Concept of Operations Annotated Outline in `extraction/pages/page_261.md`, `extraction/pages/page_262.md`, `extraction/pages/page_263.md`; skill grounding in `.agents/skills/conops-builder/references/source-grounding.md`.
- What to evaluate in a software repo: Whether the repo states who the product serves, what operational problem it solves, which workflows matter, and which nominal/off-nominal scenarios define intended use.
- Evidence to inspect: PRD, ConOps, README intent section, issue epic, user journey, runbook, support scenario, UX flow, acceptance notes.
- Score 0 condition: No stakeholder, user, mission, or intended-use artifact exists.
- Score 3 condition: Core user need and primary workflows are documented, with some assumptions, constraints, and off-nominal paths.
- Score 5 condition: Stakeholder expectations, ConOps scenarios, interfaces, assumptions, constraints, modes, degraded paths, and success measures are current and traceable to requirements and validation.
- Common failure modes: Goals are vague; user roles are missing; operational context is replaced by implementation notes; off-nominal cases are absent; documents are stale.
- Recommended corrective actions: Write a lightweight ConOps/PRD; identify actors and environments; label nominal and off-nominal scenarios; record assumptions and constraints; link scenarios to requirements and validation.
- Example artifacts: `templates/conops.md`, issue epic, product brief, operational scenario matrix, support playbook.
- Red flags: "Build feature X" with no user or operating context; scenario docs that mention only happy paths; claimed validation with no ConOps.
- Related skills/playbooks if applicable: `conops-builder`, `requirements-distiller`, `validation-planner`.

### Technical requirements definition quality

- Weight: 12
- NASA-SE source basis: Technical Requirements Definition in `extraction/pages/page_064.md`, `extraction/pages/page_066.md`; Table 4.2-1 and Table 4.2-2 in `extraction/pages/page_069.md`; requirements validation steps in `extraction/pages/page_070.md`; Appendix C checklist in `extraction/pages/page_208.md`; grounding in `.agents/skills/requirements-distiller/references/source-grounding.md` and `.agents/skills/requirements-auditor/references/source-grounding.md`.
- What to evaluate in a software repo: Whether requirements are singular, testable, feasible, unambiguous, implementation-free unless constrained with rationale, and tied to acceptance criteria.
- Evidence to inspect: Requirements matrix, tickets, acceptance criteria, product specs, API requirements, nonfunctional requirements, glossary, rationale.
- Score 0 condition: Work is described only as tasks, goals, or implementation choices with no testable requirements.
- Score 3 condition: Most core requirements have clear acceptance criteria and some rationale, but metadata or edge cases are incomplete.
- Score 5 condition: Requirements have IDs, source, owner, rationale, assumptions, verification method, trace links, and review evidence; goals/objectives are not requirements; requirements are not implementation choices.
- Common failure modes: Compound requirements; unverifiable words; hidden design choices; no rationale; requirements mixed with operations or personnel tasks; duplicated or conflicting statements.
- Recommended corrective actions: Split compound statements; add IDs and rationale; separate goals, constraints, requirements, and design decisions; define acceptance criteria and verification methods.
- Example artifacts: `templates/requirements_matrix.yaml`, requirement issue template, acceptance criteria table, glossary.
- Red flags: "Use Postgres" listed as a requirement with no constraint rationale; "fast" or "easy" without measurable criteria; tasks treated as product requirements.
- Related skills/playbooks if applicable: `requirements-distiller`, `requirements-auditor`.

### Requirements traceability and change management

- Weight: 8
- NASA-SE source basis: Requirements metadata in Table 4.2-2 at `extraction/pages/page_069.md`; requirements traceability and management in `extraction/pages/page_070.md`, `extraction/pages/page_141.md`, `extraction/pages/page_144.md`; Table D-1 in `extraction/pages/page_212.md`.
- What to evaluate in a software repo: Whether requirements trace to stakeholder intent, design, implementation, verification, validation, and approved changes.
- Evidence to inspect: Trace matrix, issue links, PR references, changelog, ADR links, baseline tags, release notes, change requests, scope decisions.
- Score 0 condition: No traceability exists from intent or requirements to code/tests/releases.
- Score 3 condition: Core requirements trace to issues, PRs, and tests; change history is understandable but not complete.
- Score 5 condition: Bidirectional traceability is maintained across intent, requirements, design, code, verification, validation, releases, and change approvals.
- Common failure modes: Requirements creep; undocumented scope changes; orphan tests; orphan features; stale requirement IDs; change impacts not assessed.
- Recommended corrective actions: Add trace IDs; link PRs/tests/releases to requirements; document change authority; assess impact before accepting new scope.
- Example artifacts: Trace matrix, requirements dashboard, linked GitHub issues, release scope board.
- Red flags: Major feature appears in code with no requirement; requirements changed in PR comments only; no owner for requirement updates.
- Related skills/playbooks if applicable: `requirements-auditor`, `technical-assessment-loop`.

### Logical decomposition and architecture

- Weight: 8
- NASA-SE source basis: Logical Decomposition Process in `extraction/pages/page_073.md`; SE engine recursive decomposition in `extraction/pages/page_016.md`; Figure 4.3-1 in `extraction/figure_index.md`.
- What to evaluate in a software repo: Whether functions, responsibilities, components, data flow, dependencies, and boundaries are decomposed coherently.
- Evidence to inspect: Architecture docs, dependency graph, module map, package boundaries, service diagrams, code organization, ownership map.
- Score 0 condition: Architecture is implicit and cannot be inferred safely from docs or structure.
- Score 3 condition: Major components and responsibilities are understandable; some dependencies or cross-cutting concerns are underdocumented.
- Score 5 condition: Architecture decomposes functions and responsibilities clearly, supports independent development, records dependencies/interfaces, and stays aligned with requirements.
- Common failure modes: Folder layout is mistaken for architecture; circular dependencies; unclear ownership; no data-flow view; cross-cutting concerns scattered.
- Recommended corrective actions: Create a component map; document responsibilities and dependencies; identify data/control flows; align architecture to requirements.
- Example artifacts: C4 diagram, package boundary doc, dependency graph, module ownership table.
- Red flags: One module owns unrelated behavior; no documented boundary for generated code; architecture decisions only discoverable by reading all source files.
- Related skills/playbooks if applicable: `integration-planner`, `technical-assessment-loop`.

### Interface management

- Weight: 10
- NASA-SE source basis: Interface Management Process in `extraction/pages/page_146.md`; Interface Requirements Document Outline in `extraction/pages/page_247.md`; interface metadata in `templates/interface_contract.yaml`.
- What to evaluate in a software repo: Whether internal and external interfaces have contracts, owners, versioning, data semantics, failure behavior, and change control.
- Evidence to inspect: API specs, schema files, event contracts, database migrations, CLI docs, SDK docs, service dependency docs, compatibility tests.
- Score 0 condition: Major interfaces are undocumented or only implicit in code.
- Score 3 condition: Primary interfaces are documented and tested, but ownership, versioning, or error behavior is incomplete.
- Score 5 condition: Interfaces have explicit contracts, owners, compatibility policy, change history, error/fault behavior, and verification at integration boundaries.
- Common failure modes: Database schema is the only contract; external service assumptions are not recorded; breaking changes lack migration plans; errors are undocumented.
- Recommended corrective actions: Add interface contract files; document owners and change process; add contract tests; record version and compatibility policy.
- Example artifacts: OpenAPI spec, protobuf schema, GraphQL schema, event catalog, `templates/interface_contract.yaml`.
- Red flags: Production integration depends on undocumented response fields; major external API has no timeout/retry/error policy; migrations are irreversible without plan.
- Related skills/playbooks if applicable: `integration-planner`, `verification-planner`.

### Design solution and decision analysis

- Weight: 8
- NASA-SE source basis: Design Solution Definition in `extraction/pages/page_076.md`, `extraction/pages/page_080.md`, `extraction/pages/page_084.md`; Decision Analysis Process in `extraction/pages/page_175.md`; Decision Report content in Table 6.8-1 at `extraction/pages/page_181.md`; grounding in `.agents/skills/decision-analysis/references/source-grounding.md`.
- What to evaluate in a software repo: Whether major architecture, dependency, data model, hosting, or integration choices record alternatives, criteria, risks, assumptions, and rationale.
- Evidence to inspect: ADRs, RFCs, design docs, trade studies, dependency evaluations, migration proposals, issue decision logs.
- Score 0 condition: Major decisions are undocumented or only visible as final code.
- Score 3 condition: Important decisions have rationale, but alternatives, criteria, risks, or revisit triggers are incomplete.
- Score 5 condition: Major decisions record problem, alternatives, evaluation criteria, weights or rationale, risks/benefits, recommendation, final decision, dissent when applicable, and revisit conditions.
- Common failure modes: Decision made before criteria; chosen dependency has no lifecycle/risk review; rejected options are lost; decision not updated after facts change.
- Recommended corrective actions: Add ADRs for major choices; capture alternatives and criteria; document assumptions and risks; define revisit triggers.
- Example artifacts: ADR, decision report, architecture RFC, dependency review.
- Red flags: "We chose X because it is popular"; high-risk vendor dependency with no exit path; no record for data architecture.
- Related skills/playbooks if applicable: `decision-analysis`, `technical-assessment-loop`.

### Implementation, build, and reuse discipline

- Weight: 6
- NASA-SE source basis: Product Implementation in `extraction/pages/page_088.md`, `extraction/pages/page_089.md`; reuse warning in Product Realization keys at `extraction/pages/page_088.md`.
- What to evaluate in a software repo: Whether the codebase can be built and run cleanly, implementation follows the design baseline, and bought/reused/generated components are controlled.
- Evidence to inspect: README commands, lockfiles, build scripts, CI setup, generated-code policy, dependency manifests, SBOM, vendored code records, local dev setup.
- Score 0 condition: A clean checkout cannot be installed, built, or run with documented steps.
- Score 3 condition: Build and run steps work for primary paths; reuse/dependency controls are partial.
- Score 5 condition: Build/run is reproducible, dependencies are pinned or governed, generated/reused code is identified, and implementation artifacts align with requirements and design.
- Common failure modes: Hidden environment variables; unpinned critical dependencies; generated files not reproducible; copied code without provenance; local-only build assumptions.
- Recommended corrective actions: Document clean setup; pin dependencies; add CI build; identify generated and vendored code; record reuse rationale and current verification.
- Example artifacts: Makefile, package lockfile, CI workflow, SBOM, generation script, dependency policy.
- Red flags: "Works on my machine" setup; production code depends on unreviewed snippets; reused component has no current verification in this repo.
- Related skills/playbooks if applicable: `verification-planner`, `technical-assessment-loop`.

### Integration planning and evidence

- Weight: 8
- NASA-SE source basis: Product Integration Process in `extraction/pages/page_096.md`, `extraction/pages/page_097.md`; Integration Plan Outline in `extraction/pages/page_224.md`; grounding in `.agents/skills/integration-planner/references/source-grounding.md`.
- What to evaluate in a software repo: Whether multi-component changes are sequenced, integrated, checked at boundaries, and supported by rollback/problem-resolution evidence.
- Evidence to inspect: CI integration jobs, end-to-end tests, release plan, deployment runbook, migration plan, compatibility matrix, incident/anomaly records.
- Score 0 condition: Components are merged or deployed without explicit integration evidence.
- Score 3 condition: Main integration path is tested and documented, but rollback, anomaly handling, or environment readiness is incomplete.
- Score 5 condition: Integration steps identify components, order, roles, resources, environment, interface checks, problem resolution, rollback, and captured results.
- Common failure modes: Unit tests are treated as integration proof; migrations lack sequencing; integration errors are not recorded; external systems are ignored.
- Recommended corrective actions: Write an integration checklist; add boundary tests; document migration/rollback; capture anomalies and corrective actions.
- Example artifacts: Integration plan, release checklist, migration runbook, CI workflow, compatibility test report.
- Red flags: Major schema/API change with no consumer plan; no staging evidence; no documented owner for integration failures.
- Related skills/playbooks if applicable: `integration-planner`, `verification-planner`.

### Verification

- Weight: 12
- NASA-SE source basis: Product Verification distinction in `extraction/pages/page_021.md`; Product Verification Process in `extraction/pages/page_101.md`; Table 5.3-1 in `extraction/pages/page_104.md`; discrepancy handling in `extraction/pages/page_107.md`; Table D-1 Requirements Verification Matrix in `extraction/pages/page_212.md`; grounding in `.agents/skills/verification-planner/references/source-grounding.md`.
- What to evaluate in a software repo: Whether specified requirements are mapped to reproducible proof by test, inspection, analysis, or demonstration.
- Evidence to inspect: Unit/integration/e2e tests, CI logs, coverage rationale, static analysis, manual inspection reports, requirements-to-verification matrix, test data, discrepancy records.
- Score 0 condition: No meaningful verification evidence exists.
- Score 3 condition: Core requirements have automated or documented verification evidence, but mapping, success criteria, or discrepancy closure is incomplete.
- Score 5 condition: Requirements trace to verification method, success criteria, procedure/command, environment/configuration, results, owner, and discrepancy/reverification records.
- Common failure modes: Tests exist but do not map to requirements; snapshots assert implementation details only; failures are ignored; verification environment is undocumented.
- Recommended corrective actions: Build a requirements-to-verification matrix; add success criteria; record CI artifact links; close discrepancies with corrective actions and reverification.
- Example artifacts: `templates/verification_matrix.yaml`, CI run, test report, inspection checklist, static analysis report.
- Red flags: "All tests pass" with no requirement mapping; no CI; flaky tests accepted as normal; no evidence for critical nonfunctional requirements.
- Related skills/playbooks if applicable: `verification-planner`, `requirements-auditor`.

### Validation

- Weight: 8
- NASA-SE source basis: Verification/validation distinction in `extraction/pages/page_021.md`; Product Validation Process in `extraction/pages/page_110.md`; validation work products in `extraction/pages/page_115.md`; Table E-1 Validation Requirements Matrix in `extraction/pages/page_214.md`; grounding in `.agents/skills/validation-planner/references/source-grounding.md`.
- What to evaluate in a software repo: Whether the product has evidence that it supports intended use, users, environments, workflows, and ConOps fit.
- Evidence to inspect: User acceptance tests, scenario demos, beta feedback, usability findings, production telemetry, support outcomes, customer signoff, validation matrix.
- Score 0 condition: No intended-use or user/environment evidence exists.
- Score 3 condition: Primary workflow has realistic validation evidence, but user roles, environments, off-nominal scenarios, or objective success signals are incomplete.
- Score 5 condition: Validation scenarios map to stakeholder expectations and ConOps, involve representative users/operators or realistic proxies, record environment, objective evidence, gaps, corrective actions, and results.
- Common failure modes: Developer tests are called validation; demos ignore operational environment; success signals are subjective; validation gaps are not tracked.
- Recommended corrective actions: Define validation scenarios; involve real users or realistic proxies; record objective success signals; separate verification from validation in reports.
- Example artifacts: `templates/validation_matrix.yaml`, user trial script, acceptance report, telemetry review, support-readiness checklist.
- Red flags: "Validated by pytest"; no user-facing workflow evidence; production failures contradict claimed validation.
- Related skills/playbooks if applicable: `validation-planner`, `conops-builder`.

### Technical risk, resilience, and fault handling

- Weight: 6
- NASA-SE source basis: Risk triplet and Technical Risk Management in `extraction/pages/page_149.md`, `extraction/pages/page_151.md`, `extraction/pages/page_152.md`; risk template in `templates/risk_register.yaml`.
- What to evaluate in a software repo: Whether technical risks, fault scenarios, degraded modes, resilience controls, uncertainty, and mitigation triggers are explicit and current.
- Evidence to inspect: Risk register, threat model, incident reports, fault-handling tests, resilience tests, backups, rate-limit policy, retry/timeouts, monitoring alerts.
- Score 0 condition: Risks and failure modes are not documented or tested.
- Score 3 condition: Major risks and failure modes are identified with some mitigation evidence, but likelihood/consequence, triggers, or closure evidence is incomplete.
- Score 5 condition: Risks are stated as scenarios with likelihood, consequence, uncertainty, owner, mitigation/contingency, trigger, status, and verification/validation evidence for controls.
- Common failure modes: Risks are generic; security/reliability issues are tracked only as bugs; no degraded-mode behavior; no incident learning loop.
- Recommended corrective actions: Add risk register; write fault scenarios; add resilience tests; link mitigations to verification; review risks at release checkpoints.
- Example artifacts: `templates/risk_register.yaml`, incident postmortem, threat model, chaos test report, recovery runbook.
- Red flags: Critical external dependency has no outage behavior; no backup/restore evidence; known incidents lack corrective action.
- Related skills/playbooks if applicable: `technical-assessment-loop`, `decision-analysis`.

### Configuration, technical data, and assessment loop

- Weight: 6
- NASA-SE source basis: Configuration Management in `extraction/pages/page_155.md`; Technical Data Management in `extraction/pages/page_161.md`, `extraction/pages/page_162.md`; Technical Assessment Process and feedback loop in `extraction/pages/page_168.md`, `extraction/pages/page_169.md`, `extraction/pages/page_170.md`; grounding in `.agents/skills/technical-assessment-loop/references/source-grounding.md`.
- What to evaluate in a software repo: Whether baselines, change control, technical records, data ownership, status reporting, review findings, and corrective actions are managed.
- Evidence to inspect: Git tags, release notes, changelog, artifact retention, docs index, owner metadata, review minutes, quality dashboards, action item closure, retrospective records.
- Score 0 condition: No meaningful configuration, technical data, or assessment records exist.
- Score 3 condition: Releases and technical records are mostly traceable; periodic review exists but corrective action closure is partial.
- Score 5 condition: Baselines, technical data, reviews, measures, risks, decisions, findings, and corrective actions are current, owned, retrievable, and used in a recurring assessment loop.
- Common failure modes: Release tags without notes; documents with no owner; metrics without decisions; review findings never close; data retention unclear.
- Recommended corrective actions: Define technical data ownership; tag releases; keep changelog; add assessment cadence; track findings to closure.
- Example artifacts: Release notes, docs index, review minutes, dashboard, corrective-action tracker.
- Red flags: Cannot tell which code was released; no owner for critical docs; action items recur without closure.
- Related skills/playbooks if applicable: `technical-assessment-loop`, `requirements-auditor`, `decision-analysis`.

## 8. Final Report Template

```markdown
# NASA-SE Codebase Assessment Report

- Repository:
- Commit/branch:
- Assessment date:
- Assessor:
- Scope:
- Commands run:
- Build/run result:
- Critical caps applied:
- Final score:

## Executive Summary

## Evidence Reviewed

## Scorecard

| Criterion | Weight | Rating 0-5 | Weighted points | Evidence reviewed | Main gap | Corrective action |
| --- | ---: | ---: | ---: | --- | --- | --- |

## Critical Caps

## Findings

## Verification Evidence

## Validation Evidence

## Known Limitations

## Recommended Next Actions
```

## 9. Finding Template

```markdown
## Finding <ID>: <title>

- finding ID:
- title:
- criterion:
- severity: critical / high / medium / low
- evidence:
- gap:
- risk:
- NASA-SE principle involved:
- recommended corrective action:
- expected verification evidence:
- owner:
- status: open / in progress / accepted risk / resolved
```

## 10. Known Limitations

- This rubric adapts systems engineering concepts to software; it is not an official NASA method for judging ordinary software repositories.
- Scoring requires assessor judgment and should be calibrated across similar repos before comparing teams.
- NASA source anchors justify the assessment lens, not the quality of the assessed code.
- The rubric can over-reward documentation if the assessor does not inspect whether the documents are current and used.
- Lightweight projects may satisfy criteria through issues, PRs, tests, and README records rather than formal plans.
- Some validation evidence may be unavailable before deployment; score the gap and record the risk rather than inventing evidence.
- Security, privacy, accessibility, legal, and domain-specific compliance reviews may require additional rubrics.

## 11. How To Use This With Codex Or Another Coding Agent

1. Ask the agent to inspect the target repo from a clean checkout and record exact commands.
2. Require the agent to fill `rubrics/nasa_se_codebase_assessment_scorecard.md` with evidence paths from the target repo.
3. Require the agent to apply critical caps after weighted scoring.
4. Require findings to use `rubrics/nasa_se_codebase_assessment_findings_template.md`.
5. Tell the agent to preserve these distinctions:
   - goals/objectives are not requirements
   - requirements are not implementation choices
   - verification proves compliance with specified requirements
   - validation checks intended use / ConOps fit
   - source grounding is context, not behavioral proof
   - tests are not automatically validation
   - documentation existence is not proof that the process is used
6. Tell the agent not to edit the assessed repo unless remediation is explicitly requested.
7. For remediation, route to the related skills/playbooks listed under each criterion and verify the change with repo-specific evidence.
