# Task 024 — Android Dependency Injection and Scoping implementation report

## Implementation summary

**PASS**

Task 024 adds the twelfth production educational topic in `review`. It teaches
dependency injection as explicit graph construction and ownership: constructors
declare dependencies, a composition root selects implementations, scopes define
lifetime and reuse, and an owner controls graph destruction.

## Changed files

Created the six canonical files under
`content/android/architecture/android-dependency-injection-and-scoping/` and
this report. Updated `README.md`, `docs/ARCHITECTURE.md`,
`docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and Task 024 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test-infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the version 2 canonical
Android app architecture competency set, all eleven preceding production
topics, and Tasks 016–023 were inspected.

Primary canonical coverage:

- `apply-separation-of-concerns`;
- `isolate-android-framework-dependencies`;
- `select-ui-state-holders-by-scope`.

Strongly reinforced:

- `design-viewmodel-ui-state`;
- `design-data-layer-around-repositories`;
- `evaluate-optional-domain-layer`;
- `explain-android-component-lifecycle-constraints`.

UI-layer responsibility and coroutine/Flow boundaries are contextually
reinforced. No competency or production competency-to-topic mapping changed.

Current official Android Developers and Dagger documentation was inspected for
DI principles, manual DI, Hilt component lifetimes and scopes, ViewModel and
navigation ownership, qualifiers, multibindings, assisted injection, and test
replacement. All 12 metadata references are official or primary documentation
and use the actual inspection date `2026-07-24`. Stable DI concepts are
distinguished from version-sensitive Hilt, Dagger, and Navigation APIs.

## DI and composition-root audit

The topic starts from explicit construction, replacement, and ownership rather
than annotations. Constructor injection is the default because it exposes
required collaborators and creates complete objects. Dependency inversion is
kept separate from the wiring technique: higher-level policy depends on stable
contracts, while infrastructure implements those contracts.

Manual `AppContainer` and feature-graph examples make the composition root,
nodes, edges, transitive dependencies, graph owner, and destruction boundary
visible. The service-locator comparison shows why consumer-side lookup hides
dependencies. Framework examples are confined to wiring boundaries and do not
claim that a DI framework chooses architecture.

## Scope, lifetime, and owner audit

Scope is consistently defined through four questions: owner, creation
boundary, reuse boundary, and destruction boundary. Provider, lazy, factory,
scoped reuse, and unscoped creation are separate contracts. Unscoped objects
still have owners and finite reachability; scoped identity is never described
as immortality.

The application example describes `@Singleton` as one instance per Hilt
`SingletonComponent` in one process. Mutable session data still requires an
explicit synchronized owner and reset contract. The examples avoid global
registries, hidden container lookup, mutable process-global test state, and
mechanical over-scoping.

## Android component scope audit

The topic distinguishes:

- process/Application ownership;
- one Activity instance;
- an Activity-retained component across configuration recreation;
- Fragment instance versus Fragment View lifetime;
- ViewModel lifetime under its actual `ViewModelStoreOwner`;
- navigation workflow lifetime under a `NavBackStackEntry`.

`@ActivityScoped` is not claimed to survive recreation.
`ActivityRetainedComponent` is not given an Activity instance binding. Fragment
scope is not treated as Fragment View scope. Navigation sharing uses the back
stack entry as the ViewModel owner and does not invent a general-purpose Hilt
navigation-graph component. Hilt ViewModels are obtained through ViewModel APIs,
not injected directly.

## Qualifier, multibinding, and assisted-injection audit

Qualifiers select same-type bindings with different semantics; they do not
create scopes. Set multibinding assembles independently contributed handlers
without depending on iteration order, and the text requires an explicit
priority or selection policy when order matters.

Assisted injection is reserved for graph dependencies combined with deliberate
runtime input. The topic directs small restorable route input to
`SavedStateHandle`, notes that assisted values are not automatically restored
after process death, and rejects shorter-lived UI owners as assisted ViewModel
arguments. Version-sensitive Hilt ViewModel creation callbacks are not
presented as universal DI semantics.

## Context and leak audit

Long-lived dependencies receive Application Context only when a platform
adapter genuinely needs it. Activity or themed Context stays within a matching
UI owner and is never placed in a process-scoped binding. ViewModel examples do
not retain Activity, Fragment, View, NavController, adapter, or listener
instances.

The leak audit also rejects process-scoped UI callbacks, mutable globals,
oversized mixed-ownership modules, provider chains used to conceal cycles, and
container APIs crossing into Domain or repository contracts.

## Testing and replacement audit

Plain unit tests construct the subject directly with fresh fakes. Hilt
integration tests replace bindings at the graph boundary, with
`@TestInstallIn`, `@UninstallModules`, and `@BindValue` identified as distinct,
version-sensitive tools with different build and isolation trade-offs.

Every test owns a fresh object graph. Production global state is not mutated to
swap dependencies, and integration graph tests do not replace focused unit
tests.

## Junior Core progress audit

Junior Core status after Task 024:
12 of 17 mandatory topics implemented as production packages in review.
5 mandatory topics remain.

The remaining mandatory topics are:

13. Android Testing Foundations
14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grading schema, production mapping, or catalog
output was introduced.

## Exact counts

- Package files: 6.
- Numbered theory sections: 24.
- Meaningful Kotlin code blocks/categories in theory: 25.
- Practice exercises: 4.
- Interview questions: 24.
- Test questions: 10.
- Official/primary references: 12.
- Taxonomy: `android` / `architecture`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 210 minutes.
- Prerequisites: 7.
- Production topic packages after Task 024: 12.
- Mandatory Junior Core topics remaining: 5.

The preferred taxonomy, metadata, and prerequisites are schema-valid. The
prerequisite graph remains acyclic.

## Validation

```text
python -B scripts/validate_content.py
PASS — 12 topic packages, 2 templates, 4 schema fixtures

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

The five remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, and AI tutor remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/architecture/android-dependency-injection-and-scoping/cheat-sheet.md
 A content/android/architecture/android-dependency-injection-and-scoping/interview.md
 A content/android/architecture/android-dependency-injection-and-scoping/practice.md
 A content/android/architecture/android-dependency-injection-and-scoping/test.yaml
 A content/android/architecture/android-dependency-injection-and-scoping/theory.md
 A content/android/architecture/android-dependency-injection-and-scoping/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-024-android-dependency-injection-and-scoping-implementation.md
 A tasks/024-add-android-dependency-injection-and-scoping-topic.md
?? 024-codex-prompt.md
?? 024-review.diff
```

## Recommended commit message

```text
feat(content): add Android dependency injection and scoping topic
```
