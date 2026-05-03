#!/usr/bin/env python3
from __future__ import annotations

import argparse

from queue_lib import QueueError, move_task, parser_with_task_id, read_json, task_path, validate_task


def main() -> int:
    parser = parser_with_task_id("Claim a pending task and move it to .queue/in-progress/.")
    parser.add_argument("--agent", required=True, help="Agent name claiming the task")
    parser.add_argument("--role", help="Optional role guard, for example coder")
    args = parser.parse_args()

    try:
        source = task_path("pending", args.task_id)
        data = read_json(source)
        validate_task(data)
        if args.role and data["role"] != args.role:
            raise QueueError(f"Task role is {data['role']}, not {args.role}")
        data["claimed_by"] = args.agent
        target = move_task("pending", "in-progress", args.task_id, data)
    except QueueError as exc:
        print(f"error: {exc}")
        return 1

    print(f"claimed: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
