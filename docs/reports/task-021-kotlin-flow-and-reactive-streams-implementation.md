# Task 021 — Kotlin Flow and Reactive Streams implementation report

## Final result

**PASS**

Task 021 adds the ninth production educational topic in `review`. It teaches
Flow through subscription, cancellation, value-loss, pairing, sharing, and
delivery semantics while preserving Android lifecycle and layer ownership.

## Files

Created the six canonical files under
`content/kotlin/flow/kotlin-flow-and-reactive-streams/` and this report.
Updated `README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and Task 021 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the canonical Android app
architecture competency package, all eight preceding production topics, and
Tasks 019–020 were inspected.

Repository evidence primarily supports
`use-coroutines-and-flows-across-layers`, with ViewModel UI state, UDF,
repository boundaries, and Compose lifecycle work strongly reinforced.
Persistent-data, separation, and UI-layer competencies provide contextual
ownership boundaries.

Current official Kotlin documentation was inspected for Flow execution,
context preservation, `flowOn`, exception transparency, operators, StateFlow,
SharedFlow, Channel, `stateIn`, `shareIn`, and `SharingStarted`. Current Android
guidance was inspected for hot flows, lifecycle-aware View and Compose
collection, and Flow testing. All 12 references are official Kotlin or Android
Developers pages and use the actual inspection date `2026-07-24`.

## Canonical competency coverage

Primary:

- `use-coroutines-and-flows-across-layers`.

Strongly reinforced:

- `design-viewmodel-ui-state`;
- `explain-unidirectional-data-flow`;
- `design-data-layer-around-repositories`;
- `handle-compose-lifecycle-work`.

Contextually reinforced:

- `explain-ui-layer-responsibilities`;
- `explain-persistent-data-models`;
- `apply-separation-of-concerns`.

No competency or production competency-to-topic mapping changed.

## Cold and hot semantics audit

The topic distinguishes one-shot suspend results from streams and explains that
a cold upstream starts independently for every collector. StateFlow is current
state, SharedFlow is configured broadcast, and Channel is send/receive
coordination with competing receivers.

Repeated cold collection, subscriber timing, current-value conflation, replay,
buffering, and rendezvous behavior are explicit. No primitive is presented as
a global owner or guaranteed durable delivery mechanism.

## Operator and backpressure audit

Intermediate and terminal operators, sequential execution, context
preservation, and the upstream-only effect of `flowOn` are explicit. The
content compares:

- `map`, `filter`, `transform`, and `onEach`;
- `buffer`, `conflate`, and `collectLatest`;
- `combine`, `zip`, and `merge`;
- `flatMapLatest` latest-wins switching.

Error examples translate only expected upstream failures and explicitly
rethrow `CancellationException`. Retry is limited by failure type and attempt
count. No ordinary `runCatching` wraps suspend or Flow work.

## Preview and experimental API audit

The current Kotlin Flow API documentation marks `debounce` as `FlowPreview` and
`flatMapLatest` as `ExperimentalCoroutinesApi`. The primary search example uses
`@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)`, and the second
conceptually compilable `flatMapLatest` example opts in at its class boundary.

Theory and the cheat sheet tell learners to verify annotations against the
kotlinx.coroutines version installed in their project because API status may
change between releases. Practice, interview, and test wording reinforces that
version check once at the relevant decision point without changing their item
counts.

## StateFlow, SharedFlow, and Channel audit

StateFlow examples use a truthful initial state and expose an immutable view.
SharedFlow examples define replay, extra capacity, overflow, and late-subscriber
limitations. Channel examples describe rendezvous, buffering, and
single-element consumption by competing receivers.

`stateIn` and `shareIn` require explicit scopes. `Eagerly`, `Lazily`, and
`WhileSubscribed` are described without prescribing one universal timeout.
Sharing does not transfer repository data ownership to ViewModel or UI.

## Lifecycle and ownership audit

Fragment View collection uses
`viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED)` with parallel
child collectors. Compose uses `collectAsStateWithLifecycle`.

The UI owns its lifecycle threshold, ViewModel owns presentation-state sharing,
repositories retain application-data ownership, and an optional Domain use
case may expose a focused Flow contract. Mutable flows and lifecycle types do
not cross those boundaries.

## Layer-boundary audit

Data owns source integration and normalized application streams. Domain is
optional and owns reusable application logic only. ViewModel converts those
contracts to immutable UiState. UI renders and collects lifecycle-aware.

The examples do not create repository-owned ad hoc scopes, expose mutable
producers, create a global event bus, or claim that hot streams are durable.

## Junior Core progress audit

The Junior Core target remains exactly 17 mandatory topics. After Task 021,
9 of 17 topics exist as complete production packages in `review`; 8 remain:
Android Navigation Architecture, Android Networking Architecture, Dependency
Injection and Scoping, Android Testing Foundations, Android Security
Foundations, Local Persistence with Room, Background Work and WorkManager, and
Compose Foundations.

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grade schema or machine-readable grading model
was introduced.

## Exact counts and metadata

- Package files: 6.
- Numbered theory sections: 24.
- Kotlin code blocks in theory: 27.
- Practice exercises: 4.
- Interview questions: 24.
- Test questions: 10.
- Official references: 12.
- Taxonomy: `kotlin` / `flow`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 210 minutes.
- Prerequisites: 2.

Both preferred taxonomy values and the preferred difficulty are schema-valid;
no adaptation was required.

## Validation

```text
python -B scripts/validate_content.py
PASS — 9 topic packages, 2 templates, 4 schema fixtures

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

The eight remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, and AI tutor remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/cheat-sheet.md
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/interview.md
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/practice.md
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/test.yaml
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/theory.md
 A content/kotlin/flow/kotlin-flow-and-reactive-streams/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-021-kotlin-flow-and-reactive-streams-implementation.md
 A tasks/021-add-kotlin-flow-and-reactive-streams-topic.md
?? 021-codex-prompt.md
?? 021-review.diff
```

## Recommended commit message

```text
feat(content): add Kotlin Flow and reactive streams topic
```
