# Review Workflow

Reviewer is the first quality gate after Coder.

## Inputs

Reviewer tasks must reference:

- The completed Coder task ID
- Files changed by that task
- Validation evidence from the Coder result
- Acceptance criteria to check

## Output

Reviewer writes a review report under `docs/reviews/` and completes the queue task.

Review reports must include:

- Decision: approved, changes requested, or blocked
- Findings ordered by severity
- File references when possible
- Missing tests or residual risks
- Follow-up task recommendations

## Boundaries

Reviewer does not edit implementation files. If a fix is required, Reviewer creates or recommends a Coder follow-up task instead.
