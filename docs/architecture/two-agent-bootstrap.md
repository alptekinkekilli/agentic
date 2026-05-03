# Two-Agent Bootstrap Architecture

## Validated State

The project has a shared queue, role prompts, queue helper scripts, patch registry, task list, session log, and hardening controls.

## Active Agents

Phase 1 activates only:

- Architect
- Coder

Reviewer, Tester, and Ops stay defined but inactive until the two-agent loop is validated.

## Workflow

1. Architect creates a bounded task in `.queue/pending/`.
2. Coder claims only tasks with `"role": "coder"`.
3. Coder edits only paths listed in `allowed_paths`.
4. Coder completes the task with changed files and validation evidence.
5. Control check validates the queue and role boundaries.
6. Session close records patch registry, task list, and session log updates.

## Isolation Rules

- Agents do not share private context.
- Agents communicate only through task JSON, docs, and recorded artifacts.
- Every task must state owner role, allowed paths, acceptance criteria, validation, and out-of-scope items.
- A task is not considered closed unless it is in `.queue/done/` or `.queue/failed/`.

## Next Coder Task

Create a dry Coder task that makes a narrow, reversible code change inside `agentic/` or `src/`, then validates it through the queue lifecycle and `scripts/control_check.py`.
