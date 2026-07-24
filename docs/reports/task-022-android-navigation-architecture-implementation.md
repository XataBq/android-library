# Task 022 — Android Navigation Architecture implementation report

## Final result

**PASS**

Task 022 adds the tenth production educational topic in `review`. It teaches
navigation as owned back-stack state and separates framework execution,
presentation decisions, application data, saved inputs, and authorization.

## Changed files

Created the six canonical files under
`content/android/navigation/android-navigation-architecture/` and this report.
Updated `README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and Task 022 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test-infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the version 2 canonical
Android app architecture competency set, the nine preceding production
topics, and Tasks 017–021 were inspected.

The primary canonical evidence is `design-single-activity-navigation`.
`explain-ui-layer-responsibilities`, `design-viewmodel-ui-state`,
`apply-separation-of-concerns`, and repository/lifecycle competencies reinforce
the ownership, state, and restoration boundaries. Navigation 3 remains a
source-specific implementation detail rather than canonical identity.

Current official Android Developers documentation was inspected for the
Navigation overview, Compose navigation, Navigation 2 type-safe routes, nested
graphs, stack options, multiple back stacks, results, Fragment Result API,
deep links, verified App Links, saved state, testing, and unsafe deep-link
risks. All 15 metadata references are official Android Developers pages and
use the actual inspection date `2026-07-24`.

## Navigation ownership audit

The back stack owns navigation state, and the active UI/navigation host owns
`NavController` and executes transitions. ViewModel owns presentation state and
may expose an intent or explicitly governed effect. Repositories and optional
use cases return data or business outcomes and never navigate.

Direct callbacks, best-effort effects, acknowledged pending effects, and
durable outcomes are compared without prescribing one universal event wrapper.
Loss, replay, stale effects, acknowledgement identity, and recreation-driven
duplicates are explicit.

## Back-stack and scope audit

Destination, route, graph, entry, and current destination are distinguished.
Push, pop, top entry, replace-like stack policies, Back versus Up, entry
lifecycle, configuration change, and process recreation are covered.

Concrete examples cover `popUpTo`, `inclusive`, `launchSingleTop`,
`saveState`, and `restoreState`. Nested graphs are UI navigation structure,
not automatic domain/module/security boundaries. Destination, graph, and
Activity ViewModel scopes are compared by lifetime and clearing behavior.
Multiple top-level back stacks cover independent history, reselect policy,
duplicate avoidance, state restoration, and memory implications.

## Arguments and results audit

Routes carry bounded reconstruction inputs, preferably stable IDs. Destinations
reload authoritative data from repositories, and possession of an ID never
implies authorization. Mutable entities, services, secrets, and large payloads
are rejected as route arguments.

Navigation 2 type-safe Compose/Kotlin DSL routes are marked version-sensitive
and require 2.8.0+. XML/Safe Args, older routes, and Navigation 3 are
acknowledged as different valid API families.

Previous-entry `SavedStateHandle`, Fragment Result API, graph-scoped shared
ViewModel, direct callback, and repository-mediated durable results are
compared by lifetime and ownership. One-time results require consumption.

## Deep-link and security audit

Explicit and implicit deep links cover route reconstruction, bounded parsing,
missing prerequisites, deleted data, unsupported routes, and authentication
gates. Verified App Links improve routing association but do not establish
parameter trust or resource access.

Exported Activities and intent filters are explicit audit points. External
inputs require scheme/host/path/shape validation, authentication, and
resource-level authorization. Internal-only routes and sensitive URL data are
addressed. Navigation, typed routes, IDs, verified links, and `PendingIntent`
do not replace authorization.

## Restoration and testing audit

Navigation may restore eligible entries, arguments, and small saved state.
Recreated ViewModels use those inputs to reload current repository data.
In-memory entities, coroutines, network calls, repositories, and large object
graphs are not restored automatically.

Compose and Fragment examples keep the same ownership boundary while showing
their different APIs. Tests cover pure route validation, presentation
decisions, graph structure, typed or ID destinations, Back/Up and stack
clearing, multiple histories, results, external entries, authorization, and
recreation. Screenshot tests are not treated as proof of navigation behavior.

## API version and maturity audit

- Navigation 2 type-safe routes and `SavedStateHandle.toRoute`: 2.8.0+.
- Multiple back-stack support: 2.4.0+.
- Navigation saved-state results: 2.3.0+.
- Fragment Result API: Fragment 1.3.0+.
- Typed `popUpTo`, typed entry lookup, and typed test helpers are explicitly
  version-sensitive.

No experimental or preview API is required by the examples. Learners are told
to verify API signatures, maturity, serialization setup, and test helpers
against the installed AndroidX artifacts. No API family is presented as
universal.

## Junior Core progress audit

Junior Core status after Task 022:
10 of 17 mandatory topics implemented as production packages in review.
7 mandatory topics remain.

The remaining mandatory topics are Android Networking Architecture, Dependency
Injection and Scoping, Android Testing Foundations, Android Security
Foundations, Local Persistence with Room, Background Work and WorkManager, and
Compose Foundations.

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grading schema, production mapping, or catalog
output was introduced.

## Exact counts and metadata

- Package files: 6.
- Numbered theory sections: 23.
- Meaningful Kotlin code blocks/categories in theory: 22.
- Practice exercises: 4.
- Interview questions: 22.
- Test questions: 10.
- Official references: 15.
- Taxonomy: `android` / `navigation`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 210 minutes.
- Prerequisites: 5.

The preferred taxonomy, difficulty, metadata, and prerequisites are
schema-valid. The prerequisite graph remains acyclic.

## Validation

```text
python -B scripts/validate_content.py
PASS — 10 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

## UTF-8 and mojibake audit

All 12 new or modified repository Markdown/YAML source files decode as strict
UTF-8 without BOM. They contain none of the checked mojibake sequences. The new
topic and review diff contain no absolute local path.

## Deferred work

The seven remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, and AI tutor remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/navigation/android-navigation-architecture/cheat-sheet.md
 A content/android/navigation/android-navigation-architecture/interview.md
 A content/android/navigation/android-navigation-architecture/practice.md
 A content/android/navigation/android-navigation-architecture/test.yaml
 A content/android/navigation/android-navigation-architecture/theory.md
 A content/android/navigation/android-navigation-architecture/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-022-android-navigation-architecture-implementation.md
 A tasks/022-add-android-navigation-architecture-topic.md
?? 022-codex-prompt.md
?? 022-review.diff
```

## Recommended commit message

```text
feat(content): add Android navigation architecture topic
```
