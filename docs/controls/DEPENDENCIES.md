# Runtime Dependencies

This file records operational dependency decisions for local helper scripts.

## queue-status helper

Script:

- `scripts/queue-status.sh`

Required runtime dependencies:

- `bash`
- `jq`
- `basename`

## Failure Policy

### Missing queue directory

Decision: hard failure.

Behavior:

- Exit `1`
- Print a clear error to stderr

Reason:

- A missing queue root means the agent coordination surface is unavailable.

### Missing jq

Decision: hard failure.

Behavior:

- Exit `1`
- Print a clear error to stderr

Reason:

- The helper depends on JSON parsing to report task IDs and roles correctly.

### Invalid task JSON

Decision: warning/readability failure for now.

Behavior:

- Continue processing other task files
- Display `<unreadable>` for unreadable fields

Reason:

- One malformed task should not hide the rest of the queue during operational inspection.

Future decision:

- Revisit after more live-agent usage and decide whether invalid queue JSON should become a hard failure.
