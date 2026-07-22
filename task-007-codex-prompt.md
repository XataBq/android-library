Implement Task 007 in the `android-library` repository.

Before editing:

1. Read `AGENTS.md`.
2. Read `tasks/007-import-android-architecture-recommendations.md`.
3. Read the source model and import workflow.
4. Read the normalization workflow only to understand what must remain deferred.
5. Inspect the existing Android Developers source package and its review report as structural precedents.
6. Inspect the real repository state and recent Git history.
7. Confirm Task 006.2 is committed.

Import exactly this live English publication:

```text
https://developer.android.com/topic/architecture/recommendations?hl=en
```

Create:

```text
competencies/sources/android-developers-architecture-recommendations/source.yaml
competencies/sources/android-developers-architecture-recommendations/items.yaml
competencies/reports/android-developers-architecture-recommendations-review.md
```

Core rules:

- Inspect the complete live page.
- Record the actual retrieval date and visible update label.
- Keep the source boundary to that one page.
- Do not import linked pages.
- Preserve every source-declared recommendation priority in `declared_level`.
- Preserve conditions, exceptions, application-size qualifications, and technology-specific scope.
- Treat the page's recommendations as recommendations, not universal requirements.
- Use one item per independently meaningful recommendation.
- Keep inseparable bullets and qualifications with their recommendation.
- Do not extract code examples as separate items.
- Use stable semantic source-level IDs.
- Use durable heading-based locators.
- Use concise faithful transcriptions or summaries compatible with `citation-only`.
- Do not normalize, deduplicate, attach evidence, or modify canonical competencies.
- Do not modify the existing source package or canonical package.
- Do not modify schemas, validators, or tests unless a genuine existing defect is discovered; stop and report before doing so.
- Update only the minimum factual state documentation.
- Keep all new package statuses at `review`.
- Keep the canonical model `PROPOSED`.
- Do not commit or push.

The review report must account for every in-scope page section and list all item IDs, priorities, exclusions, ambiguities, and candidate overlap areas for the next task.

Potential overlap is only a review aid. Do not make final equivalence decisions in Task 007.

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Verify no forbidden existing data changed:

```bash
git diff -- competencies/sources/android-developers-app-architecture/
git diff -- competencies/normalized/
git diff -- schemas/ scripts/ tests/ content/ templates/
```

Return:

- files changed;
- verified source metadata;
- exact source boundary;
- total items;
- counts by section and priority;
- extraction decisions;
- excluded linked material;
- candidate overlaps for Task 008;
- validation output;
- immutability confirmation;
- final `git status --short`;
- confirmation that no commit was created.

Then stage and export:

```bash
git add README.md docs/PROJECT_STATE.md competencies/sources/android-developers-architecture-recommendations competencies/reports/android-developers-architecture-recommendations-review.md tasks/007-import-android-architecture-recommendations.md
git diff --cached > ..\task-007-review.diff
```

Do not create a commit.
