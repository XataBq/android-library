# Task 013 — Reframe Project Roadmap Around Content Production, Automation, and Product Validation

Status: DONE

## Objective

Update the repository roadmap and current-state documentation so they reflect the actual project maturity after Tasks 012.1–012.3.

The repository now has:

- accepted canonical competency architecture;
- two Android Developers source packages;
- a versioned canonical competency set;
- a learning-sequence model;
- competency-to-topic mapping infrastructure;
- three production educational topics;
- working validators and tests;
- a stable AI-assisted authoring and review workflow.

The roadmap must distinguish:

1. canonical knowledge foundation;
2. learning-content production;
3. content automation and compilation;
4. product validation and distribution;
5. user-state infrastructure;
6. AI learning services;
7. Android client development;
8. monetization and B2B expansion.

This task changes documentation only.

## Scope

Update:

- `docs/ROADMAP.md`
- `docs/PROJECT_STATE.md`
- `README.md`

Review and update only if necessary:

- `docs/PROJECT_VISION.md`

Do not change competencies, sequences, mappings, topic packages, schemas, validators, tests, ADRs, or application code.

## Required roadmap structure

### Phase 0 — Project Foundation

Status: `Completed`

Purpose: establish project rules, ownership, architectural boundaries, AI collaboration rules, workflow, ADR usage, and task format.

### Phase 1 — Structured Content Foundation

Status: `Completed`

Purpose: define stable machine-readable educational-topic contracts and validation infrastructure.

Deliverables:

- topic metadata schema;
- test schema;
- canonical topic package;
- templates;
- fixtures;
- repository-local content validation;
- semantic validation;
- prerequisite cycle detection;
- validator unit tests.

### Phase 2 — Canonical Knowledge Foundation

Status: `Near completion`

Purpose: create a provenance-preserving and source-independent knowledge foundation.

Implemented:

- competency source model;
- two Android Developers source packages in `review`;
- canonical competency model accepted as repository architecture;
- version 2 Android app architecture competency set in `review`;
- evidence references and normalization workflow;
- canonical relation research with production relations deferred;
- minimal learning-sequence model;
- first learning sequence in `review`;
- competency-to-topic mapping infrastructure;
- no production mapping packages yet.

Remaining:

- complete editorial review of the first learning sequence;
- define promotion criteria for `review`, `accepted`, and `published`;
- formally close Phase 2;
- keep canonical competency relations deferred unless a real use case requires them.

### Phase 3 — Learning Content MVP

Status: `Current`

Purpose: make the repository useful as a standalone learning product before building a client.

Implemented baseline:

- `android-app-architecture-foundations`;
- `android-ui-layer-and-unidirectional-data-flow`;
- `android-data-layer-repositories-and-synchronization`.

Target deliverables:

- 10–15 reviewed production topics;
- one coherent reviewed learning path;
- production competency-to-topic mappings;
- generated topic catalog;
- usable Markdown navigation;
- internal link validation;
- source and reference audit;
- freshness metadata;
- CI workflow;
- editorial release rules.

Planning candidates only:

- Domain Layer and Use Cases;
- ViewModel and UI State;
- Android Lifecycle and State Restoration;
- Kotlin Coroutines Foundations;
- Structured Concurrency;
- Networking Architecture;
- Dependency Injection;
- Navigation;
- Testing;
- Android Security Foundations.

### Phase 4 — Content Automation and Compiler

Status: `Planned`

Purpose: transform repository-authored Markdown/YAML into stable machine-readable publication artifacts.

Deliverables:

- generated catalog;
- content compiler;
- normalized JSON bundle;
- versioned content releases;
- content manifest;
- asset manifest;
- checksums;
- search index;
- prerequisite graph export;
- competency coverage export;
- CI build artifacts;
- publication validation.

Conceptual flow:

```text
Markdown / YAML
        ↓
Validation
        ↓
Content compiler
        ↓
Versioned bundle
        ↓
Web / Android / Telegram / AI
```

Clients must consume stable publication contracts rather than repository paths.

### Phase 5 — Distribution MVP

Status: `Planned`

Purpose: validate real demand and content usefulness through lightweight channels.

Web deliverables:

- topic catalog;
- topic page;
- prerequisite navigation;
- theory and cheat-sheet rendering;
- tests;
- search;
- anonymous or local progress;
- analytics;
- feedback.

Telegram deliverables:

- generated drafts;
- short topic series;
- quiz format;
- question of the day;
- links to web content;
- publication analytics.

Metrics:

- topic views;
- completion;
- test attempts;
- return rate;
- topic-to-topic navigation;
- Telegram-to-web conversion.

### Phase 6 — User Platform and Synchronized Progress

Status: `Planned`

Purpose: introduce persistent personal learning state.

Deliverables:

- authentication;
- user database;
- topic progress;
- attempts;
- answers;
- competency mastery;
- weak areas;
- review queue;
- bookmarks;
- notes;
- synchronization;
- product-event analytics.

Principle:

```text
Git = source of truth for canonical content
Database = source of truth for user state
```

### Phase 7 — AI Learning Services

Status: `Planned`

Purpose: support guided explanations, assessment, interview practice, and personalization.

Deliverables:

- retrieval over exact content versions;
- bounded AI context;
- guided explanations;
- free-text answer evaluation;
- rubric-based assessment;
- interview simulation;
- weak-area recommendations;
- additional question generation;
- safety and cost constraints;
- evaluation datasets;
- answer-quality monitoring;
- optional NotebookLM export packages;
- experimental audio, slide, and visualization outputs.

AI-generated output is derived presentation content and must not automatically modify canonical knowledge.

### Phase 8 — Android Client

Status: `Planned`

Purpose: provide an offline-first mobile learning client.

Deliverables:

- Compose UI;
- Room;
- content bundle synchronization;
- progress synchronization;
- topic reader;
- tests;
- review queue;
- notifications;
- offline assets;
- structured visualizations.

The client must consume stable publication contracts.

### Phase 9 — Monetization Experiments

Status: `Planned; experiments may begin earlier`

Purpose: validate willingness to pay before building large commercial infrastructure.

Candidate experiments:

- paid interview-preparation pack;
- AI interview subscription;
- premium learning paths;
- paid intensive;
- corporate onboarding pilot;
- content licensing.

Required outcomes:

- pricing tests;
- conversion metrics;
- willingness-to-pay feedback;
- basic unit-economics assumptions;
- selection of the first repeatable paid product.

Do not present monetization as validated.

### Phase 10 — B2B Platform and Custom Backend

Status: `Deferred until justified by product requirements`

Possible future capabilities:

- private knowledge spaces;
- private source packages;
- corporate competency models;
- role matrices;
- team analytics;
- white-label clients;
- advanced permissions;
- private AI services;
- integration API;
- SLA requirements;
- Kotlin/Ktor backend;
- PostgreSQL;
- OpenAPI;
- Docker;
- integration tests;
- observability.

A custom backend is not a goal by itself.

## README requirements

State that:

- Phase 2 is near completion;
- Phase 3 is the current active product phase;
- Tasks 012.1–012.3 form the current Android architecture foundation;
- no production mappings exist yet;
- no generated catalog, web client, database, AI tutor, or Android client exists yet.

Do not imply review-stage packages are accepted or published.

## PROJECT_STATE requirements

Update:

- current phase;
- completed capabilities;
- current focus;
- next planned work;
- deferred work.

Current phase:

`Phase 3 — Learning Content MVP`

Also record that Phase 2 still requires editorial review of the first learning sequence and explicit package-promotion criteria.

The completed task history must remain accurate.

## PROJECT_VISION requirements

Change only if existing wording conflicts with the new roadmap.

Do not turn it into a business plan.

Do not add unsupported claims about users, validation, revenue, or customers.

## Editorial rules

- Separate implemented work from planned work.
- Separate architecture acceptance from package editorial status.
- Do not mark `review` packages as `accepted` or `published`.
- Do not claim production mappings exist.
- Do not claim the catalog, web, database, AI tutor, Android client, or CI already exists.
- Do not turn roadmap phases into approved implementation tasks.
- Do not add dates or deadlines.
- Preserve repository terminology.

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Verify:

- UTF-8;
- no mojibake;
- documentation consistency;
- no non-documentation changes;
- no package status changes;
- no content or competency data changes.

## Acceptance criteria

- `docs/ROADMAP.md` uses the new phase structure.
- Phase 3 is current.
- Phase 2 is near completion, not completed.
- README and PROJECT_STATE are synchronized.
- PROJECT_VISION remains consistent.
- Implemented and planned capabilities are clearly separated.
- No package status changes.
- All validation commands pass.
- Diff is repository-relative.
- Task status becomes `DONE` only after validation succeeds.

## Expected implementation report

Return:

1. implementation summary;
2. files changed;
3. roadmap decisions applied;
4. implemented-vs-planned audit;
5. package-status audit;
6. validation results;
7. UTF-8 audit;
8. deferred work;
9. `git status --short`;
10. recommended commit message.

Do not commit.
