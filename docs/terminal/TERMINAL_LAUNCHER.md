# Terminal Launcher Strategy

This project uses separate terminals for context isolation.

## Principle

Each agent runs in its own terminal session with:

- One role prompt from `agents/<role>.md`
- One model alias from `docs/controls/model_routing.json`
- Shared queue access through `.queue/`
- No shared private context

## Commands

Print launch commands:

```bash
./orchestrator.sh commands
```

The output is intentionally copy-paste oriented. It does not launch agents automatically.

## Role Mapping

| Role | Prompt | Model Alias |
| --- | --- | --- |
| Architect | `agents/architect.md` | `fast-planner` |
| Coder | `agents/coder.md` | `premium-coder` |
| Reviewer | `agents/reviewer.md` | `fast-reviewer` |
| Tester | `agents/tester.md` | `economy-tester` |
| Ops | `agents/ops.md` | `economy-ops` |

## Startup Order

Start in this order:

1. Architect
2. Coder
3. Reviewer
4. Tester
5. Ops

For first live validation, start only Architect and Coder.

## Agent Instruction

Each terminal should receive one operating instruction:

```text
Continuously watch .queue/pending/ and claim only tasks matching your AGENT_ROLE. Communicate only through queue files and recorded artifacts.
```

## Safety

- Do not paste API keys into chat or task files.
- Do not share terminal context between agents.
- Do not start all five agents until Architect + Coder has completed one live task.
- Run `python3 scripts/control_check.py` before ending a session.
