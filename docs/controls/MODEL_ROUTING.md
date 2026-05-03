# Model Routing

Model routing controls agent cost, speed, and quality without coupling the repo to a specific provider.

## Routing Matrix

| Role | Tier | Alias | Intent |
| --- | --- | --- | --- |
| Architect | fast | fast-planner | Quick task decomposition and architecture notes |
| Coder | premium | premium-coder | Highest quality implementation work |
| Reviewer | fast | fast-reviewer | Fast scope and risk checks |
| Tester | economy | economy-tester | Routine validation and reports |
| Ops | economy | economy-ops | Routine deployment, verification, and rollback notes |

## Why Aliases

Provider model names change. The repo stores durable aliases and tiers, not hard-coded vendor names.

Examples:

- `premium-coder` can map to a Claude Opus-like or GPT-5-class coding model outside this repo.
- `fast-planner` and `fast-reviewer` can map to a Haiku-like or mini-class model.
- `economy-tester` and `economy-ops` can map to the cheapest reliable routine model.

## Enforcement

Run:

```bash
python3 scripts/control_check.py
```

The control check validates:

- Every role has a model route.
- Every route references a known tier.
- Premium usage is limited to approved roles.
- Optional task-level `model_tier` and `model_alias` match the role route.
