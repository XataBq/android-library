# AI Collaboration Model

## Purpose

This document defines how ChatGPT, Codex, and the human owner cooperate.

## Responsibility matrix

| Activity | Human | ChatGPT | Codex |
|---|---:|---:|---:|
| Final product decisions | Accountable | Consulted | Informed |
| Architecture design | Accountable | Responsible | Consulted |
| Learning roadmap | Accountable | Responsible | Informed |
| Topic explanation | Participates | Responsible | Not responsible |
| Topic package drafting | Approves | Responsible | Supports formatting |
| Repository implementation | Reviews | Specifies/reviews | Responsible |
| Code review | Accountable | Responsible | Supports fixes |
| Running tasks | Responsible | Cannot directly execute | Executes when started |
| Merge/commit approval | Responsible | Consulted | Not accountable |

## ChatGPT workflow

ChatGPT should:

1. understand the current phase and repository rules;
2. avoid proposing unnecessary future complexity;
3. distinguish approved decisions from hypotheses;
4. prepare copy-ready task specifications;
5. review implementation against acceptance criteria;
6. explain educational and architectural reasoning;
7. preserve continuity across the project.

## Codex workflow

Codex should:

1. read `AGENTS.md`;
2. read the assigned task;
3. inspect existing files before editing;
4. propose a concise plan;
5. implement only the approved scope;
6. run checks;
7. report changes and limitations;
8. leave final acceptance to the human owner.

## Human workflow

The human owner should:

1. decide what is approved;
2. start Codex tasks;
3. inspect every meaningful diff;
4. ask for explanations for code not understood;
5. avoid merging large unexplained changes;
6. complete the learning work rather than delegating it to AI;
7. provide repository state or diffs to ChatGPT for review.

## Anti-patterns

Do not:

- ask Codex to “build the whole platform”;
- generate hundreds of topics before validating one complete topic;
- merge code that the owner cannot explain;
- let AI silently change architecture;
- use AI-generated text without technical review;
- automate a workflow before it is stable manually.
