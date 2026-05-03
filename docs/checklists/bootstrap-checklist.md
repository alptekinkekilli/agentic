# Bootstrap Checklist

## Phase 1: Architect + Coder

- [x] Create shared queue folders.
- [x] Create Architect prompt.
- [x] Create Coder prompt.
- [x] Define task JSON schema.
- [x] Create patch registry.
- [x] Create task list.
- [x] Create session close checklist.
- [x] Add queue helper scripts.
- [x] Run one Architect task through the queue.
- [x] Run one Coder task through the queue.

## Phase 2: Review Loop

- [x] Add Reviewer to queue flow.
- [x] Require review task after coder completion.
- [x] Record review findings in patch registry.

## Phase 3: Test Loop

- [x] Add Tester to queue flow.
- [x] Require validation command per coder task.
- [x] Record pass/fail outcomes.

## Phase 4: Ops Loop

- [x] Add Ops to queue flow.
- [x] Define deployment task contract.
- [x] Define rollback note format.
