# Agent Instructions

These rules apply to every AI agent working in this repository.

## Required reading

Before making changes, read:

1. `docs/PROJECT_VISION.md`
2. `docs/PROJECT_PRINCIPLES.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DEVELOPMENT_WORKFLOW.md`
5. the task file assigned to the agent

## General rules

1. Work only within the scope of the assigned task.
2. Prefer minimal, reviewable changes.
3. Do not invent architecture, product requirements, or educational policy.
4. Do not add frameworks, services, libraries, or infrastructure without explicit approval.
5. Do not generate large volumes of educational content unless the task explicitly requires it.
6. Do not delete or rename existing content without explicit instruction.
7. Keep educational content independent from web, Android, and backend implementations.
8. Keep user progress separate from educational content.
9. Update documentation when implementation changes documented behavior.
10. Validate all YAML, JSON, Markdown links, and schemas affected by the task.
11. Report assumptions, unresolved questions, and trade-offs.
12. Never commit secrets, credentials, tokens, personal data, or environment-specific files.

## Task execution

Before implementation:

- summarize the task;
- inspect the relevant files;
- propose a concise plan;
- identify ambiguities.

After implementation:

- run available checks;
- list changed files;
- explain important decisions;
- report anything not completed;
- do not claim success when checks were not run or failed.

## Architecture authority

Architecture decisions require human approval.

An agent may propose an ADR, but must not silently introduce a major architectural decision.
