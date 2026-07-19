# Educational Content Model

## Purpose

The content model defines the portable, author-facing files used for educational topics. Topic content is stored as YAML and Markdown in Git and is independent from web, Android, backend, database, and UI models.

The schemas are:

- `schemas/topic.schema.json` for `topic.yaml`;
- `schemas/test.schema.json` for `test.yaml`.

Both use JSON Schema Draft 2020-12.

## Canonical topic package

```text
content/<track>/<section>/<topic>/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

The directory names organize content for authors and mirror the topic's `track`, `section`, and stable `id`. They are not reference identities. Moving a published topic package must not silently change its topic or question IDs; the destination must still follow the canonical path contract.

Templates for all six files are available under `templates/topic/`.

## Topic metadata

Every `topic.yaml` contains these fields:

| Field | Meaning |
|---|---|
| `id` | Globally unique, stable topic ID. |
| `title` | Non-empty human-readable title. |
| `track` | Controlled top-level subject classification. |
| `section` | Lowercase kebab-case grouping within a track. |
| `difficulty` | Authored depth: `foundation`, `junior`, `middle`, or `advanced`. |
| `status` | Content publication state: `draft`, `review`, `published`, or `deprecated`. |
| `estimated_minutes` | Expected active study time; an integer from 5 through 600. |
| `content_version` | Positive integer version of educational meaning. |
| `prerequisites` | Unique stable topic IDs that should be learned first. |
| `learning_outcomes` | Unique, observable, non-empty learner outcomes. |
| `tags` | Unique lowercase kebab-case author tags. |
| `references` | Authored sources supporting the topic. |

Optional fields are `summary`, `android_connections`, `jvm_connections`, and `related_topics`. Connection fields contain explanatory text. `related_topics` contains unique stable topic IDs and does not imply a prerequisite relationship.

The controlled initial tracks are `computer-science`, `java`, `kotlin`, `jvm`, `algorithms`, `concurrency`, `coroutines`, `networking`, `databases`, `architecture`, `testing`, `security`, `android`, `system-design`, and `tools`.

## Stable identifiers

Topic and question IDs use lowercase kebab-case: lowercase letters and digits separated by single hyphens. Examples include `java-object-equality` and `equals-hashcode-contract`.

- A topic ID is globally unique across the repository.
- A question ID is unique within its topic.
- IDs describe concepts or questions, not UI screens or filesystem locations.
- IDs remain stable after publication and are not reused after removal.
- Renaming or moving a directory does not change an ID.

Option IDs also use lowercase kebab-case and are unique within their question so answer keys can refer to them clearly.

## Publication status and learner progress

`status` describes shared content publication only. `difficulty` describes authored depth only. Neither represents an individual learner.

Completion, attempts, answers, scores, mastery, review dates, bookmarks, and personal notes are personal state. They do not belong in topic packages and will be stored separately.

## Content versioning

New topics start with `content_version: 1`. Increment the integer when published educational meaning changes, including meaningful changes to explanations, outcomes, questions, or expected answers. Formatting-only edits do not require an increment.

`topic.yaml` and `test.yaml` each declare a content version. Repository validation requires their versions to be consistent.

## Tests and question types

Every `test.yaml` contains the stable `topic_id`, a positive integer `content_version`, an integer `passing_score_percent` from 1 through 100, and at least one question.

All questions require `id`, `type`, `prompt`, `difficulty`, positive integer `points`, and a non-empty post-evaluation `explanation`. The supported types are:

- `single-choice`: at least two `options` and one `correct_option_id`;
- `multiple-choice`: at least two `options` and one or more unique `correct_option_ids`;
- `true-false`: a Boolean `correct_answer`;
- `free-text`: a non-empty authored `rubric` and optional `sample_answer`;
- `code-analysis`: `language`, non-empty `code`, a non-empty authored `rubric`, and optional `sample_answer`.

Each option contains `id` and `text`. Each rubric item contains `criterion` and positive integer `points`. Code analysis supports `java`, `kotlin`, `xml`, `gradle-kotlin`, `bash`, and `sql`; code is content for analysis and is not executed.

## References

Each reference requires `title`, absolute `url`, and `type`. Supported types are `official-docs`, `specification`, `book`, `article`, `paper`, `video`, `course`, and `repository`.

Optional fields are `author`, `accessed_on`, and `notes`. Quote `accessed_on` as a `YYYY-MM-DD` YAML string so YAML parsers do not convert it to a date object.

## Validation boundaries

JSON Schema validates local file shape, required fields, controlled values, identifier patterns, basic ranges, and question-type-specific fields. With format checking enabled, it also validates reference URLs and access dates.

The repository validator adds checks for:

- globally unique topic IDs and question IDs within each topic;
- unique option IDs within each question;
- existence of prerequisite and related-topic IDs;
- prerequisite cycles and self-dependency;
- membership of answer-key option IDs in a question's options;
- consistency between topic and test IDs or content versions;
- rubric point totals;
- canonical package files and path/metadata consistency.

Run it with `python scripts/validate_content.py`; see `docs/CONTENT_VALIDATION.md` for its diagnostics and limitations. Removed-ID history, Markdown structure, and internal links remain deferred.

The schemas intentionally do not attempt to resolve these relationships across files or compare values between sibling fields.

## Author workflow

1. Copy `templates/topic/` to `content/<track>/<section>/<topic>/`.
2. Choose a globally unique concept-based topic ID and stable question IDs.
3. Replace every marked placeholder and keep the topic in `draft` status.
4. Add reviewed Markdown content, assessment answers, rubrics, and authoritative references.
5. Run `python scripts/validate_content.py` to validate schemas and repository-wide rules.
6. Submit the topic for human review before changing its publication status.
