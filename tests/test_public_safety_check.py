import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from public_safety_check import run_check


def test_public_safety_check_passes_clean_tree(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.md").write_text("generic public core note\n", encoding="utf-8")
    (tmp_path / ".queue" / "done").mkdir(parents=True)
    (tmp_path / ".queue" / "done" / ".gitkeep").write_text("", encoding="utf-8")

    assert run_check(tmp_path) == []


def test_public_safety_check_flags_private_markers(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("deploy notes for Vercel\n", encoding="utf-8")

    findings = run_check(tmp_path)

    assert [finding.path for finding in findings] == [Path("README.md")]
    assert "Vercel" in findings[0].reason


def test_public_safety_check_flags_completed_queue_history(tmp_path):
    done_dir = tmp_path / ".queue" / "done"
    done_dir.mkdir(parents=True)
    history = done_dir / "bootstrap-0001.json"
    history.write_text("{}\n", encoding="utf-8")

    findings = run_check(tmp_path)

    assert [finding.path for finding in findings] == [Path(".queue/done/bootstrap-0001.json")]
    assert "completed queue history" in findings[0].reason


def test_public_safety_check_flags_private_history_dirs(tmp_path):
    session_dir = tmp_path / "docs" / "sessions"
    session_dir.mkdir(parents=True)
    session_file = session_dir / "SESSION_LOG.md"
    session_file.write_text("internal notes\n", encoding="utf-8")

    findings = run_check(tmp_path)

    assert [finding.path for finding in findings] == [Path("docs/sessions/SESSION_LOG.md")]
    assert "private operational history" in findings[0].reason
