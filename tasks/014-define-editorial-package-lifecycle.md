# Task 014 — Define Editorial Package Lifecycle and Promotion Criteria

Status: DONE

## Objective

Define one repository-wide editorial lifecycle for versioned knowledge and learning packages.

The repository currently uses statuses such as `review`, and the roadmap now requires explicit promotion criteria for:

- `review`;
- `accepted`;
- `published`.

The project also distinguishes:

- architecture decisions;
- package editorial status;
- implementation task status;
- generated publication artifacts.

These concepts must not be conflated.

This task is documentation-first. It defines policy and review requirements. It must not promote any existing package and must not change package data.

---

## Problem

The repository already contains:

- imported source packages;
- a canonical competency package;
- a learning-sequence package;
- educational topic packages;
- competency-to-topic mapping infrastructure;
- architecture documents with statuses such as `ACCEPTED`;
- task files with statuses such as `READY`, `REVIEW`, and `DONE`.

However, there is no single explicit policy that answers:

1. What does `review` mean for a package?
2. What evidence is required before a package becomes `accepted`?
3. What additional conditions are required before a package becomes `published`?
4. Who approves promotion?
5. What happens when a source or dependency changes?
6. Does architecture acceptance promote package content?
7. Can a package remain accepted while a newer version is in review?
8. How should deprecated or superseded versions be treated?
9. Which statuses belong to packages, tasks, architecture decisions, and generated outputs?

Without this policy, Phase 2 cannot be formally closed and future production mappings cannot safely reference reviewed versions.

---

## Scope

Create:

- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`

Update:

- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- relevant authoring or workflow documentation only where a direct link is required.

Create an implementation report according to repository conventions.

Do not change:

- source package YAML;
- canonical competency package YAML;
- learning-sequence YAML;
- competency-to-topic mapping data;
- topic packages;
- schemas;
- validators;
- tests;
- ADR status;
- task history;
- any package status.

---

## Required status model

Define the following package editorial states.

### `draft`

Meaning:

- package is incomplete or actively being authored;
- references may be unstable;
- validation may fail;
- package must not be used as a production dependency;
- content is not ready for formal review.

Clarify whether the current schemas support this value. If schemas do not support it, document it as a lifecycle concept without modifying schemas in this task.

### `review`

Meaning:

- package is structurally complete enough for review;
- required automated validation passes;
- content may still change materially;
- package is not yet approved for stable downstream reliance;
- references to it must explicitly acknowledge review-stage risk.

### `accepted`

Meaning:

- the exact package version has passed editorial and technical review;
- required evidence and references have been checked;
- scope and semantics are considered stable enough for downstream use;
- acceptance applies to one exact package version;
- later edits require a new version or a return to review, according to the domain rules;
- acceptance does not mean public release.

### `published`

Meaning:

- an accepted package version has been approved for learner-facing or external distribution;
- publication artifacts can be generated from it;
- release metadata and visibility requirements are satisfied;
- published content must remain traceable to the exact accepted package version;
- publication does not make generated derivatives canonical.

### `deprecated`

Meaning:

- package version remains historically addressable;
- new downstream work should not target it;
- replacement or migration guidance should be recorded when available;
- deprecation does not erase provenance or historical learner records.

### `superseded`

Meaning:

- a newer package version is the preferred continuation;
- the older version remains immutable and traceable;
- existing exact-version references remain historically valid unless explicitly migrated.

If current schemas do not support `draft`, `deprecated`, or `superseded`, clearly distinguish:

- editorial lifecycle concepts;
- currently machine-supported package status values.

Do not modify status enums in this task.

---

## Required domain-specific criteria

The lifecycle document must define promotion checks for each domain.

### Source package

For `review` → `accepted`, require at least:

- identifiable source and version;
- stable provenance;
- valid locators;
- faithful source-item extraction or paraphrase;
- completeness review against the declared scope;
- no invented claims;
- validator success;
- extraction review record;
- reviewer approval.

For `accepted` → `published`, explain whether source packages are normally externally published or remain internal evidence artifacts. Do not assume all accepted source packages must become public.

### Canonical competency package

For `review` → `accepted`, require at least:

- valid evidence for every competency;
- stable identifiers;
- source-independent wording;
- duplicate and near-duplicate review;
- merge/split decisions explained;
- scope and granularity review;
- cross-source normalization review;
- validator success;
- explicit editorial approval.

Clarify that acceptance of the canonical competency model architecture does not accept a canonical competency package.

### Learning-sequence package

For `review` → `accepted`, require at least:

- references to one exact canonical competency-set version;
- all referenced competencies exist;
- stage ordering has a clear pedagogical rationale;
- no implication that sequence order creates canonical competency relations;
- target audience and outcome are coherent;
- omissions and scope are documented;
- validator success;
- editorial review.

For `accepted` → `published`, require learner-facing readiness and an approved presentation context.

### Competency-to-topic mapping package

For `review` → `accepted`, require at least:

- exact canonical competency-set version;
- exact topic content versions;
- valid many-to-many references;
- mapping rationale;
- coverage audit;
- no relation semantics imported from learning sequences or prerequisites;
- validator success;
- reviewer approval.

Clarify that no production mapping package currently exists.

### Educational topic package

For `review` → `accepted`, require at least:

- valid metadata;
- exact prerequisite references;
- learning outcomes;
- theory;
- cheat sheet;
- practice;
- interview material;
- assessment;
- references;
- consistency between all six canonical files;
- technical accuracy review;
- editorial clarity review;
- validator success;
- no unresolved blocking review comments.

For `accepted` → `published`, require at least:

- learner-facing formatting;
- release version;
- publication readiness;
- valid internal links;
- source/reference audit;
- freshness review;
- approved distribution context.

---

## Cross-domain rules

Define these rules explicitly.

### Exact-version acceptance

Acceptance applies to an exact package version, not to an ID forever.

### Immutable accepted versions

Accepted or published versions should not be silently rewritten.

If corrections are required, document the expected approach:

- new version;
- correction release;
- explicit return to review;
- migration note;

depending on future domain policy.

Do not design a full release system in this task.

### Dependency status

A downstream package may be authored against a `review` dependency, but it cannot become `accepted` unless dependency policy is satisfied.

Define a conservative initial rule:

- an accepted package should normally depend only on accepted exact-version canonical dependencies;
- exceptions require explicit documented rationale;
- published learner-facing material should not depend on unresolved review-stage canonical packages.

### Parallel versions

Allow:

- version N accepted or published;
- version N+1 in review.

Do not imply that a new review version automatically invalidates the accepted version.

### Architecture versus editorial status

State clearly:

```text
Architecture status answers:
"Is this model or decision the repository's approved design?"

Package editorial status answers:
"Has this exact package version passed content review?"
```

One does not imply the other.

### Task status versus package status

Task `DONE` means implementation work was completed.

It does not mean any package created by the task is accepted or published.

### Generated artifacts

Generated catalog entries, web pages, Telegram posts, slides, audio, AI answers, and NotebookLM outputs are derived artifacts.

They:

- must reference source package/topic versions;
- do not become canonical knowledge automatically;
- have a separate publication/release lifecycle.

---

## Promotion authority

Define a minimal current authority model.

The human repository owner:

- makes the final promotion decision;
- may use AI and automated validation as evidence;
- remains accountable for status changes.

ChatGPT may:

- perform editorial and architectural review;
- recommend approval or changes;
- identify inconsistencies.

Codex may:

- implement approved status changes;
- run checks;
- prepare reports.

Codex must not independently promote packages.

---

## Promotion record

Define what must be recorded when a package is promoted:

- package ID;
- exact version;
- old status;
- new status;
- decision date if repository conventions later support it;
- reviewer/approver;
- validation results;
- review report;
- known limitations;
- replacement or migration notes when relevant.

Do not introduce mandatory dates into existing package files in this task.

Promotion records may initially live in repository reports or dedicated review documents.

---

## Rollback and correction policy

Define a minimal policy for accepted or published packages that later prove incorrect.

Possible actions:

- mark the affected version deprecated;
- publish a corrected version;
- record the defect and impact;
- update downstream mappings or publication artifacts;
- preserve historical traceability;
- do not silently delete evidence or rewrite history.

Do not implement rollback tooling.

---

## Phase 2 closure

Update roadmap and project state so that Task 014 satisfies the package-promotion-criteria milestone.

After Task 014:

Phase 2 must still remain open because editorial review of the first learning sequence has not yet been completed.

The remaining Phase 2 milestone should become:

- complete editorial review and disposition of the first learning sequence;
- then formally close Phase 2.

Do not close Phase 2 in this task.

---

## Documentation integration

### README

Add the lifecycle document to the recommended reading order.

Keep the current project phase as:

`Phase 3 — Learning Content MVP`

Mention that package promotion criteria are now defined, while the first learning sequence still requires editorial review.

### PROJECT_STATE

Record Task 014 as completed only after validation.

Update:

- completed capabilities;
- completed tasks;
- Phase 2 remaining work;
- next planned task.

The next logical task should be the editorial review of the first learning sequence.

### ROADMAP

Mark explicit promotion criteria as implemented.

Keep Phase 2 as `Near completion`.

Do not change Phase 3 current status.

### ARCHITECTURE

Add a concise distinction and link between:

- architecture acceptance;
- package editorial lifecycle.

Do not duplicate the full lifecycle document.

---

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Also verify:

- UTF-8;
- no mojibake;
- documentation links resolve;
- only documentation, task, and report files changed;
- no package status changed;
- no schema enum changed;
- no source, competency, sequence, mapping, or topic data changed.

---

## Acceptance criteria

- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md` exists.
- The document distinguishes architecture, package, task, and generated-artifact status.
- `review`, `accepted`, and `published` are defined.
- Draft, deprecated, and superseded concepts are documented without falsely claiming schema support.
- Promotion criteria exist for all package domains.
- Exact-version acceptance is explicit.
- Human promotion authority is explicit.
- No existing package is promoted.
- Phase 2 remains near completion.
- The remaining Phase 2 blocker is the first learning-sequence editorial review.
- README, PROJECT_STATE, ROADMAP, and ARCHITECTURE are synchronized.
- All validation commands pass.
- Task status becomes `DONE` only after validation succeeds.

---

## Expected implementation report

Return:

1. implementation summary;
2. files created and changed;
3. lifecycle model decisions;
4. schema-support audit;
5. package-status audit;
6. Phase 2 closure audit;
7. validation results;
8. UTF-8 and link audit;
9. literal `git status --short`;
10. recommended commit message.

Do not commit.
