#!/usr/bin/env python3
from __future__ import annotations

import argparse

from queue_lib import QueueError, move_task, read_json, task_path, validate_task


def main() -> int:
    parser = argparse.ArgumentParser(description="Complete an in-progress task and move it to .queue/done/.")
    parser.add_argument("task_id", help="Task id without .json suffix")
    parser.add_argument("--summary", required=True, help="Short completion summary")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed file path. May be repeated.")
    parser.add_argument("--validation", action="append", default=[], help="Validation command or result. May be repeated.")
    args = parser.parse_args()

    try:
        source = task_path("in-progress", args.task_id)
        data = read_json(source)
        validate_task(data)
        data["result"] = {
            "summary": args.summary,
            "changed_files": args.changed_file,
            "validation": args.validation,
        }
        target = move_task("in-progress", "done", args.task_id, data)
    except QueueError as exc:
        print(f"error: {exc}")
        return 1

    print(f"completed: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
