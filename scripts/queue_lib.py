#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".queue"
VALID_ROLES = {"architect", "coder", "reviewer", "tester", "ops"}
VALID_STATUSES = {"pending", "in-progress", "done", "failed"}


class QueueError(Exception):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def queue_dir(status: str) -> Path:
    if status not in VALID_STATUSES:
        raise QueueError(f"Invalid status: {status}")
    return QUEUE / status


def task_path(status: str, task_id: str) -> Path:
    safe_id = task_id.strip()
    if not safe_id or "/" in safe_id or "\\" in safe_id:
        raise QueueError(f"Invalid task id: {task_id!r}")
    return queue_dir(status) / f"{safe_id}.json"


def read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise QueueError(f"Task file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QueueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise QueueError(f"Task must be a JSON object: {path}")
    return data


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".json.tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")
    os.replace(temp_path, path)


def move_task(source_status: str, target_status: str, task_id: str, data: dict[str, Any]) -> Path:
    source = task_path(source_status, task_id)
    target = task_path(target_status, task_id)
    if target.exists():
        raise QueueError(f"Target task already exists: {target}")
    data["status"] = target_status
    write_json_atomic(target, data)
    source.unlink()
    return target


def validate_task(data: dict[str, Any]) -> None:
    required = [
        "id",
        "title",
        "role",
        "status",
        "created_at",
        "objective",
        "allowed_paths",
        "acceptance_criteria",
    ]
    missing = [field for field in required if field not in data]
    if missing:
        raise QueueError(f"Missing required fields: {', '.join(missing)}")
    if data["role"] not in VALID_ROLES:
        raise QueueError(f"Invalid role: {data['role']}")
    if data["status"] not in VALID_STATUSES:
        raise QueueError(f"Invalid status: {data['status']}")
    for field in ("allowed_paths", "acceptance_criteria"):
        if not isinstance(data[field], list) or not all(isinstance(item, str) for item in data[field]):
            raise QueueError(f"{field} must be a list of strings")
    validate_allowed_paths(data["allowed_paths"])


def validate_allowed_paths(paths: list[str]) -> None:
    for path in paths:
        candidate = Path(path)
        if candidate.is_absolute():
            raise QueueError(f"allowed_paths must be relative: {path}")
        if any(part == ".." for part in candidate.parts):
            raise QueueError(f"allowed_paths cannot contain '..': {path}")
        if path.strip() != path or not path.strip():
            raise QueueError(f"allowed_paths entry is empty or has edge whitespace: {path!r}")


def parser_with_task_id(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("task_id", help="Task id without .json suffix")
    return parser


def fail(message: str) -> int:
    print(f"error: {message}")
    return 1
