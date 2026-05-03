# Hardening Controls

This project uses shared files instead of shared context. Hardening exists to keep that contract explicit and checkable.

## Control Layers

1. Queue lifecycle
   - Tasks move through `.queue/pending/`, `.queue/in-progress/`, `.queue/done/`, and `.queue/failed/`.
   - Agents do not pass private context to each other.

2. Role capabilities
   - `docs/controls/role_capabilities.json` defines what each role may edit.
   - A task's `allowed_paths` must stay inside that role's `may_edit` list.
   - A task's `allowed_paths` must not overlap that role's `must_not_edit` list.

3. Completion evidence
   - Done and failed tasks must include `result`.
   - Completion must record summary, changed files when applicable, and validation.

4. Session close
   - Every completed operation updates patch registry, task list, and session log.
   - A session can close only when there is a queue record in `done` or `failed`.

## Current Enforcement

Run:

```bash
python3 scripts/control_check.py
```

This validates all task JSON files in `.queue/` and `docs/tasks/` against role boundaries and completion evidence.
