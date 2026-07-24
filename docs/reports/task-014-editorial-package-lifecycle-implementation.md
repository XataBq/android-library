# Task 014 — Editorial Package Lifecycle implementation report

## Final result

**PASS**

Task 014 defines one repository-wide editorial lifecycle and exact-version
promotion criteria for source, canonical competency, learning-sequence,
competency-to-topic mapping, and educational topic packages. No package was
promoted and no machine contract changed.

## Files

Created:

- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`;
- this implementation report.

Updated:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`;
- `docs/ARCHITECTURE.md`;
- `tasks/014-define-editorial-package-lifecycle.md`.

## Lifecycle decisions

- Architecture, package editorial, task, and generated-artifact statuses are
  independent.
- Acceptance applies to one exact package version.
- An older accepted or published version may coexist with a newer version in
  `review`.
- Accepted and published versions must not be silently rewritten.
- Stable accepted dependencies are the conservative default; exceptions
  require documented rationale and human approval.
- Generated derivatives remain traceable, non-canonical outputs.
- The human repository owner is the final promotion authority. ChatGPT may
  recommend, and Codex may implement an approved promotion but may not decide
  one independently.

## Schema-support audit

The status enums were read from the current schemas:

| Package/schema | Machine-supported values |
|---|---|
| `competency-source.schema.json` | `draft`, `review`, `approved`, `deprecated` |
| `canonical-competency-set.schema.json` | `draft`, `review`, `approved`, `deprecated` |
| `learning-sequence.schema.json` | `draft`, `review`, `approved`, `deprecated` |
| `competency-topic-mapping.schema.json` | `draft`, `review`, `approved`, `deprecated` |
| `topic.schema.json` | `draft`, `review`, `published`, `deprecated` |

For the four competency-related schemas, `approved` is the machine-supported
representation of conceptual `accepted`; `published` is unsupported. The topic
schema supports `published` but no distinct `accepted` or `approved` state.
No schema supports `superseded`. All schemas support `draft`, `review`, and
`deprecated`.

No status enum or other schema content was changed.

## Package-status audit

The two source packages, version 2 canonical competency package, first
learning-sequence package, and three educational topic packages all remain in
`review`. No production competency-to-topic mapping package exists. No source,
canonical competency, sequence, mapping, or topic data changed.

## Phase 2 closure audit

Phase 2 remains `Near completion`; Phase 3 remains current. Promotion criteria
are now defined. The remaining Phase 2 work is editorial review and disposition
of the first learning sequence, followed by formal closure.

## Validation

```text
python -B scripts/validate_content.py
PASS — 3 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

All created and modified Markdown files decode as strict UTF-8 without BOM and
contain none of the checked mojibake sequences. All repository-relative
Markdown links in Task 014 documentation resolve to existing files.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 M docs/ARCHITECTURE.md
 A docs/EDITORIAL_PACKAGE_LIFECYCLE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-014-editorial-package-lifecycle-implementation.md
 A tasks/014-define-editorial-package-lifecycle.md
?? 014-codex-prompt.md
?? 014-review.diff
```

## Deferred work

The first learning-sequence editorial disposition, Phase 2 formal closure,
package promotion actions, machine support for lifecycle gaps, release tooling,
and rollback automation remain deferred to future approved tasks.

## Recommended commit message

```text
docs: define editorial package lifecycle
```
