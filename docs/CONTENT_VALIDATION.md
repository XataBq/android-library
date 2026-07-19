# Content Validation

## Purpose

The repository validator checks educational topic packages before publication. It is local tooling and does not depend on web, Android, backend, database, or learner-progress code.

Run it from the repository root:

```bash
python scripts/validate_content.py
```

Use `--root <path>` to validate another repository-shaped directory. Use `--verbose` to print successful loading and discovery phases.

## Validation layers

JSON Schema Draft 2020-12 validates each `topic.yaml` and `test.yaml` independently. It checks required fields, types, controlled values, identifier shapes, formats, ranges, and question-type-specific fields. The validator enables format checking and meta-validates both schemas before reading content.

Repository semantic validation adds checks that require comparing fields or files:

- canonical package completeness;
- topic/test ID and content-version consistency;
- topic, question, and option ID uniqueness in their defined scopes;
- answer IDs referencing declared options;
- rubric points equalling question points;
- self references and unknown topic references;
- path track, section, and leaf consistency with topic metadata;
- prerequisite cycles.

These layers remain separate so structural schema errors and repository relationship errors have distinct diagnostics.

## Package discovery

Only directories shaped as `content/<track>/<section>/<topic>/` are considered. A directory at that depth is a topic package when it contains `topic.yaml` or `test.yaml`. Every discovered package must contain:

```text
topic.yaml
theory.md
cheat-sheet.md
practice.md
interview.md
test.yaml
```

Templates and schema fixtures are validated separately and never become real topics or reference targets. The two valid fixtures must pass their schemas; the two intentionally invalid fixtures must fail.

The canonical path mirrors `topic.yaml` values for navigability: track matches `track`, section matches `section`, and the leaf directory matches `id`. The stable topic ID remains the reference identity. Moving a package does not authorize changing a published ID; instead, the destination must continue to satisfy the canonical path contract.

## Diagnostics and exit codes

Diagnostics are sorted and use a stable code:

```text
ERROR [UNKNOWN_TOPIC_REFERENCE] content/tools/basics/example/topic.yaml: prerequisites: topic id 'missing-topic' does not exist
```

Exit codes are:

- `0`: validation passed;
- `1`: content validation failed;
- `2`: invalid CLI usage, schema/configuration failure, or unexpected internal failure.

The command reports the number of errors and discovered real topic packages. It does not modify content.

## Tests

Run the standard-library test suite from the repository root:

```bash
python -m unittest discover
```

Tests create compact repositories in temporary directories and cover successful validation, malformed input, schema failure, local relationships, repository references, path consistency, and dependency cycles.

## Limitations

The validator does not check Markdown structure or links, prose quality, spelling, remote URL availability, removed-ID history, global question-ID uniqueness, aggregate test scoring policy, or semantic correctness of educational answers. It does not execute code, migrate content, rename paths, or auto-fix errors.
