# Test Workflow

Tester is the validation gate after Coder and Reviewer.

## Inputs

Tester tasks must reference:

- The completed Coder task ID
- The related review task or report
- Validation commands to run
- Expected pass/fail criteria

## Output

Tester writes a test report under `docs/tests/` and completes the queue task.

Test reports must include:

- Commands run
- Pass/fail result
- Failure reproduction steps when applicable
- Coverage gaps
- Follow-up recommendations

## Boundaries

Tester may add or edit tests only when the task explicitly allows it. Tester does not edit implementation files.
