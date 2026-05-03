#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
}

SELF_ALLOWLIST = {
    Path("scripts/public_safety_check.py"),
    Path("tests/test_public_safety_check.py"),
}

FORBIDDEN_TEXT = [
    "agentic-devteam",
    "alptekins-projects",
    "teamSlug",
    "OPENAI_API_KEY",
    "code-davinci",
    "gh repo create",
    "private fork",
    "Vercel",
]

FORBIDDEN_PATH_PARTS = [
    ("docs", "sessions"),
    ("docs", "patches"),
    ("docs", "research"),
]

FORBIDDEN_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    reason: str

    def format(self) -> str:
        return f"{self.path}: {self.reason}"


def relative_to_root(path: Path, root: Path) -> Path:
    return path.resolve().relative_to(root.resolve())


def should_skip(path: Path, root: Path) -> bool:
    rel = relative_to_root(path, root)
    if rel in SELF_ALLOWLIST:
        return True
    return any(part in SKIP_DIRS for part in rel.parts)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if should_skip(path, root):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def has_forbidden_path_part(rel: Path) -> bool:
    parts = rel.parts
    for forbidden in FORBIDDEN_PATH_PARTS:
        for index in range(0, len(parts) - len(forbidden) + 1):
            if parts[index : index + len(forbidden)] == forbidden:
                return True
    return False


def scan_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        rel = relative_to_root(path, root)
        if rel.name in FORBIDDEN_FILE_NAMES:
            findings.append(Finding(rel, "environment file must not be committed to public core"))
        if has_forbidden_path_part(rel):
            findings.append(Finding(rel, "private operational history path is not public-core safe"))
        if rel.parts[:2] == (".queue", "done") and rel.suffix == ".json":
            findings.append(Finding(rel, "completed queue history must not be committed to public core"))
        if rel.parts[:2] == (".queue", "failed") and rel.suffix == ".json":
            findings.append(Finding(rel, "failed queue history must not be committed to public core"))
    return findings


def scan_text(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        rel = relative_to_root(path, root)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in FORBIDDEN_TEXT:
            if marker in content:
                findings.append(Finding(rel, f"forbidden public-core marker found: {marker}"))
    return findings


def run_check(root: Path) -> list[Finding]:
    return scan_paths(root) + scan_text(root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that the repository is safe to publish as public core.")
    parser.add_argument("--root", default=str(ROOT), help="Repository root to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = run_check(root)
    if findings:
        for finding in findings:
            print(f"error: {finding.format()}")
        return 1

    print("public safety check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
