# Agentic

Agentic is a minimal queue-first project skeleton for experimenting with isolated AI development agents.

The core idea is simple:

- agents do not share conversation context
- tasks move through `.queue/pending`, `.queue/in-progress`, `.queue/done`, and `.queue/failed`
- role files under `agents/` define responsibilities
- helper scripts under `scripts/` validate and move tasks
- docs record the operating model, hardening rules, and review/test/ops workflows

This repository is the public minimal core. Product-specific automation, private dashboards, long-running agents, and organization-specific memory should live in a private derived repository.

## Quick Start

```bash
python3 scripts/control_check.py
python3 scripts/enqueue.py docs/tasks/example.architect-task.json
python3 scripts/claim_task.py task-0001 --agent local-architect --role architect
python3 scripts/complete_task.py task-0001 --summary "Reviewed example task" --validation "manual smoke check"
```

## CLI Smoke Test

```bash
python3 -m agentic.cli
```

## Tests

```bash
pytest
bash tests/test_queue_status.sh
python3 scripts/control_check.py
```

## Project Layout

- `agents/`: role instructions for Architect, Coder, Reviewer, Tester, and Ops
- `.queue/`: file-based task lifecycle
- `scripts/`: queue and control helpers
- `docs/`: public-safe architecture, hardening, workflow, and checklist docs
- `tests/`: focused smoke and queue helper tests

## Status

This is an intentionally small core. Keep it generic, dependency-light, and safe to fork.
