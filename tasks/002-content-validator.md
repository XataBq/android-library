# Task 002 — Implement the repository content validator

- Status: DONE
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Implement a small repository-local validation tool that validates educational content packages beyond what JSON Schema can enforce.

The validator must:

- discover topic packages under `content/`;
- validate `topic.yaml` and `test.yaml` against the existing JSON Schemas;
- enforce repository-wide identifier and relationship invariants;
- provide clear, deterministic diagnostics;
- return a non-zero exit code when validation fails;
- validate the existing templates and fixtures appropriately;
- remain independent from product applications and databases.

This task adds tooling only. It must not add real educational lessons or application code.

---

## Context

Task 001 established the author-facing content model:

- YAML for topic and test metadata;
- Markdown for educational material;
- JSON Schema Draft 2020-12 for structural validation;
- stable topic and question identifiers independent from filesystem paths;
- personal learner progress stored outside shared content.

JSON Schema intentionally does not enforce several repository-wide rules, including:

- global topic-ID uniqueness;
- topic/test identity consistency;
- prerequisite and related-topic existence;
- dependency cycles;
- answer IDs referencing declared options;
- duplicate question and option IDs;
- package completeness.

Task 002 must implement these checks as a focused validation tool.

---

## Required reading

Before making changes, read:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_VISION.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTENT_STRATEGY.md`
- `docs/CONTENT_MODEL.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/AI_COLLABORATION.md`
- `docs/ROADMAP.md`
- `docs/decisions/0001-content-and-progress-storage.md`
- `docs/decisions/0002-yaml-content-model-and-json-schema.md`
- `schemas/topic.schema.json`
- `schemas/test.schema.json`
- `templates/TASK_TEMPLATE.md`
- `tasks/001-content-model.md`

Inspect all existing templates and schema fixtures before implementing the validator.

---

## Approved technical direction

Use Python for the validator because the repository already confirmed the availability of:

- Python 3.12;
- PyYAML;
- jsonschema with Draft 2020-12 support.

Do not initialize a Python package manager.

Do not add dependencies.

Use only:

- the Python standard library;
- `yaml` from PyYAML;
- `jsonschema`.

The validator should be executable from the repository root.

Preferred entry point:

```text
scripts/validate_content.py
```

The implementation may be split into a small package under:

```text
tools/content_validator/
```

only if this materially improves readability and testing.

For the initial implementation, prefer a single well-structured script plus focused tests over speculative modularization.

---

## Canonical package discovery

Discover topic packages only under:

```text
content/<track>/<section>/<topic>/
```

A directory is considered a topic package when it contains either:

```text
topic.yaml
```

or:

```text
test.yaml
```

A valid package must contain all canonical files:

```text
topic.yaml
theory.md
cheat-sheet.md
practice.md
interview.md
test.yaml
```

The validator must report missing canonical files.

Do not treat directories under `templates/` or `schemas/fixtures/` as real content packages.

---

## Required validation phases

The validator should use explicit validation phases so diagnostics remain understandable.

Recommended order:

1. repository and schema loading;
2. topic package discovery;
3. YAML parsing;
4. JSON Schema validation;
5. package-local semantic validation;
6. repository-wide semantic validation;
7. dependency graph validation;
8. summary and exit code.

A malformed file must not crash the entire run. Continue validating other packages when practical.

---

## 1. Repository and schema loading

Load:

```text
schemas/topic.schema.json
schemas/test.schema.json
```

Requirements:

- parse both files as JSON;
- check both schemas against the Draft 2020-12 meta-schema;
- use Draft 2020-12 validators;
- enable format checking;
- report schema-loading errors clearly;
- fail validation when the schemas themselves are invalid.

Do not fetch remote schema resources over the network.

---

## 2. YAML parsing

Parse every discovered:

```text
topic.yaml
test.yaml
```

Requirements:

- use safe YAML loading;
- require the root value to be a mapping/object;
- report syntax and root-type errors with the file path;
- do not execute arbitrary YAML constructors.

---

## 3. JSON Schema validation

Validate:

- every real `topic.yaml` against `topic.schema.json`;
- every real `test.yaml` against `test.schema.json`;
- `templates/topic/topic.yaml`;
- `templates/topic/test.yaml`;
- valid schema fixtures.

Invalid fixtures must be checked separately and must fail their corresponding schemas.

Schema diagnostics should include, where available:

- file path;
- YAML property path;
- concise validation message.

Example diagnostic shape:

```text
ERROR [SCHEMA] content/kotlin/coroutines/coroutine-context/topic.yaml: learning_outcomes: [] should be non-empty
```

Exact punctuation is not prescribed, but output must be deterministic and readable.

---

## 4. Package-local semantic validation

For every topic package whose YAML parsed successfully, validate the following.

### Topic and test consistency

- `test.yaml.topic_id` equals `topic.yaml.id`;
- `test.yaml.content_version` equals `topic.yaml.content_version`.

### Question IDs

Within one `test.yaml`:

- question IDs must be unique.

### Option IDs

Within each choice question:

- option IDs must be unique.

### Answer references

For `single-choice`:

- `correct_option_id` must reference an existing option ID.

For `multiple-choice`:

- every value in `correct_option_ids` must reference an existing option ID;
- duplicate correct IDs are invalid even if schema validation should already reject them.

### Rubric points

For `free-text` and `code-analysis`:

- the sum of rubric item points must equal the question's `points`.

This creates a consistent scoring contract.

### Self references

For a topic:

- `prerequisites` must not contain its own ID;
- `related_topics`, when present, must not contain its own ID.

### Package path consistency

The package directory path must match topic metadata:

```text
content/<track>/<section>/<leaf-directory>/
```

Rules:

- path track equals `topic.yaml.track`;
- path section equals `topic.yaml.section`;
- the leaf directory name must equal `topic.yaml.id`.

This path rule improves navigability, but the stable ID remains conceptually independent from the path and must still be used for references.

Renaming a directory must not imply changing a published topic ID unless the metadata contract itself requires the canonical leaf-name match.

Document this distinction clearly.

---

## 5. Repository-wide semantic validation

Across all successfully parsed real topics, enforce:

### Topic ID uniqueness

- every `topic.yaml.id` must be globally unique.

Diagnostics must list all conflicting files.

### Referenced topic existence

Every ID listed in:

- `prerequisites`;
- `related_topics`;

must reference an existing real topic.

Do not resolve references against templates or fixtures.

### Question ID scope

Question IDs are required to be unique only within their topic.

Do not enforce global question-ID uniqueness.

### Removed IDs

Do not implement a removed-ID registry in this task.

Document it as a future extension.

---

## 6. Dependency graph validation

Construct a directed graph using:

```text
topic -> prerequisite
```

Detect prerequisite cycles.

Examples that must fail:

```text
a -> a
```

```text
a -> b
b -> a
```

```text
a -> b
b -> c
c -> a
```

Diagnostics should report at least one readable cycle path, for example:

```text
ERROR [DEPENDENCY_CYCLE] android-a -> kotlin-b -> java-c -> android-a
```

Related topics are not dependency edges and must not participate in cycle detection.

Use a deterministic algorithm and deterministic ordering.

---

## 7. CLI contract

The validator must support:

```bash
python scripts/validate_content.py
```

Optional arguments may be added only when useful.

Approved optional arguments:

```text
--root <path>
--verbose
```

Semantics:

- default root is the repository root inferred from the script location;
- `--root` allows testing against a temporary repository fixture;
- `--verbose` may print successfully validated files and phases.

Exit codes:

```text
0 = validation passed
1 = content validation failed
2 = validator usage or internal configuration error
```

Unhandled tracebacks must not be the normal user experience.

Unexpected internal failures may still print a traceback only in verbose/debug mode if implemented.

---

## 8. Deterministic diagnostics

Diagnostics must be:

- sorted deterministically;
- written to standard output or standard error consistently;
- prefixed with severity and a stable machine-readable code.

Recommended format:

```text
ERROR [DUPLICATE_TOPIC_ID] <path>: topic id 'example-topic' also appears in <other-path>
```

Diagnostic codes must be centralized as constants or an enum-like construct.

At minimum support codes for:

```text
SCHEMA_LOAD
YAML_PARSE
SCHEMA
MISSING_FILE
TOPIC_TEST_ID_MISMATCH
CONTENT_VERSION_MISMATCH
DUPLICATE_TOPIC_ID
DUPLICATE_QUESTION_ID
DUPLICATE_OPTION_ID
UNKNOWN_CORRECT_OPTION
RUBRIC_POINTS_MISMATCH
SELF_REFERENCE
UNKNOWN_TOPIC_REFERENCE
PATH_METADATA_MISMATCH
DEPENDENCY_CYCLE
```

Exact names may differ slightly if the implementation remains coherent and documented.

---

## 9. Tests

Add focused automated tests.

Preferred location:

```text
tools/content_validator/tests/
```

or:

```text
tests/content_validator/
```

Use the Python standard library `unittest`.

Do not add pytest.

Tests must use temporary directories and minimal synthetic repository fixtures.

Required test cases:

1. valid repository passes;
2. duplicate topic IDs fail;
3. missing canonical package file fails;
4. topic/test ID mismatch fails;
5. content-version mismatch fails;
6. duplicate question IDs fail;
7. duplicate option IDs fail;
8. unknown correct option fails;
9. rubric-point mismatch fails;
10. unknown prerequisite fails;
11. self prerequisite fails;
12. prerequisite cycle fails;
13. path/metadata mismatch fails;
14. malformed YAML fails without crashing;
15. invalid schema content produces a controlled failure.

Tests should assert:

- exit/result status;
- relevant diagnostic code;
- deterministic behavior where practical.

Do not copy large fixture trees into the repository. Generate small fixtures in test code or use compact dedicated fixtures.

---

## 10. Validation of schema fixtures

The validator or its test suite must confirm:

- valid topic fixture passes;
- valid test fixture passes;
- invalid topic fixture fails;
- invalid test fixture fails.

The main repository-content command must not treat intentionally invalid fixtures as errors in normal content validation.

A separate internal phase or test helper may validate fixture expectations.

---

## 11. Documentation

Create:

```text
docs/CONTENT_VALIDATION.md
```

Document:

- what the validator checks;
- what JSON Schema checks;
- what semantic checks add;
- how package discovery works;
- CLI usage;
- exit codes;
- diagnostic format;
- how to run tests;
- limitations and deferred checks.

Update:

```text
README.md
```

Add the validator command to the contributor/start-here workflow.

Update:

```text
docs/CONTENT_MODEL.md
```

Only where necessary to reference repository-wide validation rules.

Create ADR:

```text
docs/decisions/0003-repository-content-validator.md
```

The ADR must record:

- why validation is repository-local;
- why Python is used initially;
- why JSON Schema and semantic validation remain separate;
- why validation runs independently from product clients;
- consequences and known limitations.

Do not broadly rewrite existing documents.

---

## 12. Validation report

A successful run should end with a concise summary similar to:

```text
Content validation passed: 0 topic packages, 2 templates, 4 schema fixtures.
```

A failing run should end with a concise summary similar to:

```text
Content validation failed: 3 errors across 2 topic packages.
```

Exact wording may differ, but it must state:

- pass or fail;
- number of errors;
- number of discovered real topic packages.

---

## Acceptance criteria

- [ ] `scripts/validate_content.py` exists and is executable through Python.
- [ ] No new dependency or package manager is added.
- [ ] Draft 2020-12 schemas are loaded and meta-validated.
- [ ] Format checking is enabled.
- [ ] Real topic packages are discovered only under `content/`.
- [ ] Canonical package files are enforced.
- [ ] Topic and test YAML files are schema-validated.
- [ ] Templates and schema fixtures are validated appropriately.
- [ ] Topic/test IDs and content versions must match.
- [ ] Topic IDs are globally unique.
- [ ] Question IDs are unique within a topic.
- [ ] Option IDs are unique within each choice question.
- [ ] Correct option references are validated.
- [ ] Rubric points equal question points.
- [ ] Prerequisite and related-topic references must exist.
- [ ] Self references are rejected.
- [ ] Prerequisite cycles are detected.
- [ ] Path track, section, and topic leaf match metadata.
- [ ] Diagnostics are deterministic and have stable codes.
- [ ] Exit codes follow the approved contract.
- [ ] Required `unittest` cases exist and pass.
- [ ] `docs/CONTENT_VALIDATION.md` exists.
- [ ] ADR 0003 exists.
- [ ] README contains the validation command.
- [ ] Focused content-model documentation updates are made.
- [ ] No application, backend, Android, web, database, CI, or real lesson is added.
- [ ] `git diff --check` passes.

---

## Explicitly deferred

Do not implement:

- CI workflows;
- pre-commit hooks;
- editor plugins;
- database validation;
- learner-progress validation;
- Markdown prose quality analysis;
- Markdown heading enforcement;
- internal Markdown link checking;
- spell checking;
- executable code questions;
- test randomization;
- removed-ID registries;
- automatic content migrations;
- automatic path renaming;
- remote URL availability checks;
- semantic evaluation of free-text answers;
- global question-ID uniqueness.

These may be handled by later tasks.

---

## Forbidden changes

Do not:

- add dependencies;
- initialize Poetry, pipenv, uv, pip-tools, or another package manager;
- initialize web, Android, backend, or database code;
- add CI workflows;
- add real educational topics;
- modify schema semantics beyond what is necessary for validator compatibility;
- weaken existing schemas;
- introduce learner-progress fields;
- fetch network resources during validation;
- auto-fix content;
- rename topic directories automatically;
- commit changes.

---

## Validation

Run at minimum:

```bash
python scripts/validate_content.py
python -m unittest discover
git diff --check
git status --short
```

Use the available Python command on the local system if it is not named exactly `python`.

Also run direct JSON parsing and schema meta-validation if not already covered by tests.

---

## Deliverables

1. repository content validator;
2. focused `unittest` test suite;
3. `docs/CONTENT_VALIDATION.md`;
4. ADR 0003;
5. focused README and content-model updates;
6. Codex final report containing:
   - implementation summary;
   - architecture rationale;
   - alternatives considered and rejected;
   - complete changed-file list;
   - validation commands and results;
   - diagnostic and exit-code design;
   - limitations and deferred work;
   - assumptions;
   - unresolved issues;
   - explicit confirmation that no dependency, product code, database, CI workflow, or real educational lesson was added.

Do not change Task 002 status to `DONE`.
Do not commit.
