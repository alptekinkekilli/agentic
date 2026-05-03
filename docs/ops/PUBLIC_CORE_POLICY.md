# Public Core Policy

This repository is the minimal public core for the Agentic queue-first agent model.

## Boundary

Keep public core generic, dependency-light, and safe to fork.

Allowed:

- queue lifecycle scripts
- generic role prompts
- generic architecture, control, review, test, and ops docs
- tests and fixtures that do not contain account-specific or product-specific details

Not allowed:

- account-specific hosting details
- organization-specific memory or session history
- completed or failed live queue history
- secrets, environment files, API keys, or model-provider credentials
- product-specific automation, dashboards, or long-running team workflows

## Promotion Rule

Work that starts in a derived development repository may enter public core only through an explicit promotion task.

The promotion task must run:

```bash
python3 scripts/public_safety_check.py
python3 scripts/control_check.py
pytest
bash tests/test_queue_status.sh
```

If any check fails, keep the work out of public core until the finding is fixed.

## Release Gate

Before pushing public core, verify:

- the working tree is clean except for intended public changes
- the safety check passes
- control checks pass
- tests pass
- queue history contains only placeholder files
- public docs do not include account-specific operational notes
