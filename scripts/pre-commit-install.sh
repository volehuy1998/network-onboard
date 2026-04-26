#!/usr/bin/env bash
# pre-commit-install.sh — install v3.8 governance pre-commit hook.
#
# Hook runs:
#   1. anti_gaming_check.py (GP-6 to GP-10)
#   2. rubric_leak_check.py (GP-11 / CLAUDE.md Rule 16)
#
# Bypass with --no-verify is STRICTLY discouraged (CLAUDE.md Rule 4 + user
# Quality > Speed mandate).
#
# Usage:
#   bash scripts/pre-commit-install.sh
#
# Verify after install:
#   ls -la .git/hooks/pre-commit
#   cat .git/hooks/pre-commit

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HOOK_PATH="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "ERROR: not in a git repository (no .git directory at $REPO_ROOT)" >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/.git/hooks"

cat > "$HOOK_PATH" << 'HOOK'
#!/usr/bin/env bash
# v3.8 governance pre-commit hook (auto-installed via scripts/pre-commit-install.sh).
#
# Enforces:
#   - GP-6 to GP-10: anti-gaming check on staged curriculum .md
#   - GP-11 / Rule 16: rubric leak check on staged curriculum .md
#
# Bypass with `git commit --no-verify` is recorded in commit history; do NOT use
# without explicit reason documented in commit message.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python
fi

ANTI="$REPO_ROOT/scripts/anti_gaming_check.py"
LEAK="$REPO_ROOT/scripts/rubric_leak_check.py"

# Skip hook if no .md files staged.
STAGED_MD="$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.md$' || true)"
if [ -z "$STAGED_MD" ]; then
  exit 0
fi

echo "→ pre-commit: anti_gaming_check on staged .md ..."
if [ -f "$ANTI" ]; then
  "$PYTHON" "$ANTI" --staged || {
    echo "✗ anti_gaming_check FAIL — commit rejected per GP-6 to GP-10."
    echo "  Fix violations or override with --no-verify (NOT recommended)."
    exit 1
  }
else
  echo "  (skip: $ANTI not found)"
fi

echo "→ pre-commit: rubric_leak_check on staged .md ..."
if [ -f "$LEAK" ]; then
  "$PYTHON" "$LEAK" --staged || {
    echo "✗ rubric_leak_check FAIL — commit rejected per GP-11 / CLAUDE.md Rule 16."
    echo "  Fix internal-term leak or override with --no-verify (NOT recommended)."
    exit 1
  }
else
  echo "  (skip: $LEAK not found)"
fi

echo "✓ pre-commit governance checks PASS."
exit 0
HOOK

chmod +x "$HOOK_PATH"

echo "✓ Installed pre-commit hook at: $HOOK_PATH"
echo
echo "Test the hook by staging a curriculum .md file and running 'git commit'."
echo "It runs:"
echo "  - scripts/anti_gaming_check.py --staged   (GP-6 to GP-10)"
echo "  - scripts/rubric_leak_check.py --staged   (GP-11 / Rule 16)"
echo
echo "Bypass (NOT recommended): git commit --no-verify"
