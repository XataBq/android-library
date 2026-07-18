# Development Workflow

## Participants

### Human owner and developer

Responsibilities:

- makes final product and architecture decisions;
- studies the educational material;
- reviews and understands changes;
- runs or approves agent tasks;
- merges accepted changes;
- implements selected parts personally.

### ChatGPT

Responsibilities:

- acts as teacher, architect, product analyst, and reviewer;
- explains topics;
- proposes roadmaps and domain models;
- prepares educational topic packages;
- prepares precise implementation tasks for Codex;
- reviews diffs, code, and architecture;
- tracks conceptual consistency in the conversation.

ChatGPT does not directly control Codex execution from a normal conversation.

### Codex

Responsibilities:

- implements approved tasks;
- works within the repository;
- creates and edits files;
- writes boilerplate and tests;
- runs available checks;
- reports results.

Codex does not independently define product scope or architecture.

## Standard task lifecycle

1. **Discuss**
   - Define the problem and expected outcome.

2. **Design**
   - Clarify the domain model, boundaries, and trade-offs.

3. **Approve**
   - Human owner confirms the direction.

4. **Write task**
   - ChatGPT prepares a task file with acceptance criteria.

5. **Execute**
   - Human starts the task in Codex.

6. **Inspect**
   - Human reviews the diff and checks that the implementation is understood.

7. **Review**
   - ChatGPT reviews code, structure, and compliance when provided with the diff or repository access.

8. **Fix**
   - Codex or the human developer applies requested changes.

9. **Validate**
   - Run automated checks and manually verify the result.

10. **Merge**
    - Human merges or commits the accepted implementation.

11. **Record**
    - Update documentation, task status, and ADRs when necessary.

## Branching

Recommended task branch format:

```text
task/000-foundation
task/001-content-model
feature/web-topic-page
fix/content-validator-links
```

For the earliest local setup, direct work on `main` is acceptable only for the initial foundation commit. After that, focused branches are preferred.

## Commit messages

Recommended format:

```text
docs: add project foundation
feat(content): add topic metadata schema
feat(web): render topic theory
fix(validation): reject duplicate topic ids
test(content): cover invalid prerequisites
```

## Definition of done

A task is done only when:

- acceptance criteria are satisfied;
- relevant checks pass;
- no unrelated changes are included;
- documentation is updated where required;
- assumptions and limitations are reported;
- the human owner understands the result.

## Task status

Task files may use:

- `DRAFT`
- `READY`
- `IN_PROGRESS`
- `REVIEW`
- `DONE`
- `BLOCKED`

The human owner controls status changes.
