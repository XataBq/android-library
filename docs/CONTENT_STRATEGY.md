# Content Strategy

## Purpose

Educational content must support understanding, application, interview preparation, and long-term retention.

## Topic lifecycle

1. Select a topic from the approved roadmap.
2. Identify prerequisites and expected depth.
3. Learn and discuss the topic with ChatGPT.
4. Answer diagnostic and control questions.
5. Complete practical exercises.
6. Produce a reviewed topic package.
7. Add the package to the repository through a focused task.
8. Validate and publish it.
9. Review the topic according to the repetition schedule.
10. Improve the material based on observed weak points.

## Standard topic package

A mature topic should contain:

- `topic.yaml` — identity, taxonomy, dependencies, depth, and metadata;
- `theory.md` — full explanation;
- `cheat-sheet.md` — concise recall material;
- `test.yaml` — structured questions and explanations;
- `practice.md` — exercises and coding tasks;
- `interview.md` — graded interview questions and expected answer points.

## Content ownership

### ChatGPT prepares

- structured explanations;
- learning outcomes;
- draft topic metadata;
- tests;
- practice tasks;
- interview questions;
- reference recommendations;
- revisions based on learner difficulties.

### Codex performs

- file creation;
- formatting;
- schema validation;
- index and roadmap updates;
- link checks;
- mechanical refactoring.

Codex must not silently rewrite educational meaning.

### Human owner performs

- active learning;
- factual and conceptual review;
- practical implementation;
- final approval;
- reporting unclear or weak explanations.

## Quality criteria

Content should be:

- technically accurate;
- explicit about version-specific behavior;
- structured from fundamentals to internals;
- clear about complexity and trade-offs;
- connected to Android and JVM when relevant;
- supported by primary or authoritative sources;
- free from unnecessary duplication;
- suitable for later rendering in web and Android clients.

## Personalization

Shared content should remain generally useful.

Learner-specific items such as personal weak points, private notes, and review history should not be committed to public shared content unless deliberately anonymized and generalized.
