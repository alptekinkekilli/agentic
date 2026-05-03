# Ops Workflow

Ops is the release and runtime gate after implementation, review, and test validation.

## Inputs

Ops tasks must reference:

- The completed Coder task ID
- The related review report
- The related test report
- Deployment target
- Verification commands
- Rollback plan

## Output

Ops writes an operations report under `docs/ops/` and completes the queue task.

Operations reports must include:

- Deployment target
- Commands planned or run
- Verification result
- Rollback plan
- Follow-up recommendations

## Boundaries

Ops does not edit implementation files. If deployment requires code changes, Ops creates or recommends a Coder follow-up task.
