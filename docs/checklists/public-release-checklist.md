# Public Release Checklist

Use this before pushing changes to the public core repository.

- [ ] Confirm the change is generic core functionality.
- [ ] Confirm no account-specific hosting, team, or repository details are included.
- [ ] Confirm `.queue/done/` and `.queue/failed/` contain no live task JSON history.
- [ ] Run `python3 scripts/public_safety_check.py`.
- [ ] Run `python3 scripts/control_check.py`.
- [ ] Run `pytest`.
- [ ] Run `bash tests/test_queue_status.sh`.
- [ ] Review `git status --short --branch`.
- [ ] Review `git diff --check`.
- [ ] Commit only the intended public-safe files.
