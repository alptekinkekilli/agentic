#!/usr/bin/env bash
set -uo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
script="$repo_root/scripts/queue-status.sh"
fixture_dir="$repo_root/tests/fixtures/queue"

pass=0
fail=0

assert() {
    local name="$1"
    local result="$2"
    if [[ "$result" == "ok" ]]; then
        echo "PASS: $name"
        pass=$((pass + 1))
    else
        echo "FAIL: $name ($result)"
        fail=$((fail + 1))
    fi
}

# Assertion 1: script exits 0 on valid fixture dir
output="$(bash "$script" --dir "$fixture_dir" 2>/dev/null)"
rc=$?
if [[ $rc -eq 0 ]]; then
    assert "exit 0 on valid fixture dir" "ok"
else
    assert "exit 0 on valid fixture dir" "exit code $rc"
fi

# Assertion 2: output contains all four section headers
missing_headers=""
for header in "PENDING" "IN-PROGRESS" "DONE" "FAILED"; do
    if ! grep -q "=== $header ===" <<<"$output"; then
        missing_headers+=" $header"
    fi
done
if [[ -z "$missing_headers" ]]; then
    assert "output contains all four section headers" "ok"
else
    assert "output contains all four section headers" "missing:$missing_headers"
fi

# Assertion 3: each stub's id appears in output
missing_ids=""
for id in "fixture-pending-001" "fixture-inprogress-001" "fixture-done-001" "fixture-failed-001"; do
    if ! grep -q "$id" <<<"$output"; then
        missing_ids+=" $id"
    fi
done
if [[ -z "$missing_ids" ]]; then
    assert "all fixture ids appear in output" "ok"
else
    assert "all fixture ids appear in output" "missing:$missing_ids"
fi

# Assertion 4: script exits 1 when given a nonexistent dir
bogus_dir="$repo_root/tests/fixtures/queue-does-not-exist-$$"
bash "$script" --dir "$bogus_dir" >/dev/null 2>&1
rc=$?
if [[ $rc -eq 1 ]]; then
    assert "exit 1 on missing dir" "ok"
else
    assert "exit 1 on missing dir" "got exit code $rc"
fi

# Assertion 5: script exits 1 with a clear error when jq is unavailable
tmp_bin="$(mktemp -d)"
cat >"$tmp_bin/bash" <<'BASH_WRAPPER'
#!/bin/bash
exec /bin/bash "$@"
BASH_WRAPPER
cat >"$tmp_bin/basename" <<'BASENAME_WRAPPER'
#!/bin/bash
exec /usr/bin/basename "$@"
BASENAME_WRAPPER
chmod +x "$tmp_bin/bash" "$tmp_bin/basename"
jq_error="$(PATH="$tmp_bin" bash "$script" --dir "$fixture_dir" 2>&1 >/dev/null)"
rc=$?
rm -rf "$tmp_bin"
if [[ $rc -eq 1 && "$jq_error" == *"jq is required"* ]]; then
    assert "exit 1 when jq is unavailable" "ok"
else
    assert "exit 1 when jq is unavailable" "exit code $rc, stderr: $jq_error"
fi

echo
echo "Summary: $pass passed, $fail failed"

if [[ $fail -gt 0 ]]; then
    exit 1
fi
exit 0
