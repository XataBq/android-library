# Task 016 — Android Domain Layer and Use Cases implementation report

## Final result

**PASS**

Task 016 adds the fourth production Android app architecture topic in `review`.
It teaches a responsibility-first decision model for the optional Domain layer
and focused use cases without creating a competency mapping or changing any
existing package.

## Files

Created the six canonical files under
`content/android/app-architecture/android-domain-layer-and-use-cases/` and this
implementation report. Updated `README.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, the one stale topic-count phrase in
`docs/ARCHITECTURE.md`, and Task 016 status.

## Source and evidence audit

- `android-developers-app-architecture` supplies the primary statement that the
  Domain layer is optional and is added for complex logic or reuse across state
  holders.
- `android-developers-architecture-recommendations` reinforces large-app and
  ViewModel-simplification context, coroutine/Flow communication, testing with
  fakes, and conditional layer-specific models.
- The topic uses the official Guide, Domain layer, Recommendations, Data layer,
  and UI layer URLs already represented in repository sources or existing
  production topics.
- The existing production-topic reference convention and its recorded
  `2026-07-23` access date were reused. No new access date was invented.

## Canonical coverage

Primary:

- `evaluate-optional-domain-layer`.

Reinforced without redefining:

- `apply-separation-of-concerns`;
- `explain-ui-layer-responsibilities`;
- `design-data-layer-around-repositories`;
- `explain-repository-responsibilities`;
- `use-coroutines-and-flows-across-layers`;
- `evaluate-layer-specific-models`.

No competency or production mapping was created or modified.

## Prerequisite and duplication audit

The topic pins all three existing architecture topics as prerequisites. The
validated prerequisite graph is acyclic. Theory assumes their UI/UDF,
repository/SSOT, synchronization, and architecture foundations and only recaps
them to establish the Domain boundary.

The new package owns optionality, focused application operations,
ViewModel/use-case/repository placement, multi-repository coordination,
framework-independent Domain code, caller-owned coroutine lifetime, and Domain
testing. It does not reteach the prerequisite topics in full.

## Content audit and counts

- Package files: exactly 6.
- Numbered theory sections: exactly 16.
- Practice exercises: exactly 4.
- Interview questions: exactly 18.
- Test questions: exactly 10.

Theory includes a focused suspending use case, Flow-returning use case,
multi-repository coordination, pass-through counterexample, fake-based unit
test, and an end-to-end checkout example. It excludes `GlobalScope`, hidden
unmanaged work, Android `Context` in Domain code, direct DAO/Retrofit use,
mandatory Hilt, universal result wrappers, and mechanical use-case generation.

## Metadata and references

- ID/path: `android-domain-layer-and-use-cases`.
- Difficulty/status: `foundation` / `review`.
- Estimated time/content version: 120 minutes / 1.
- Prerequisites: all three existing Android architecture topics.
- References: 5 official Android Developers pages.

## Validation

```text
python -B scripts/validate_content.py
PASS — 4 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

All new and modified Markdown/YAML files decode as strict UTF-8 without BOM and
contain none of the checked mojibake sequences. No absolute local path exists
in the new topic package.

## Deferred work

Editorial acceptance or publication, production competency-to-topic mappings,
further topics, catalog generation, CI, web and Android clients, and AI
services remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/app-architecture/android-domain-layer-and-use-cases/cheat-sheet.md
 A content/android/app-architecture/android-domain-layer-and-use-cases/interview.md
 A content/android/app-architecture/android-domain-layer-and-use-cases/practice.md
 A content/android/app-architecture/android-domain-layer-and-use-cases/test.yaml
 A content/android/app-architecture/android-domain-layer-and-use-cases/theory.md
 A content/android/app-architecture/android-domain-layer-and-use-cases/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-016-android-domain-layer-and-use-cases-implementation.md
 A tasks/016-add-domain-layer-and-use-cases-topic.md
?? 016-codex-prompt.md
?? 016-review.diff
```

## Recommended commit message

```text
feat(content): add Android Domain layer topic
```
