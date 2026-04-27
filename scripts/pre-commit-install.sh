#!/usr/bin/env bash
# pre-commit-install.sh, install governance pre-commit hook.
#
# Hook runs four checks on staged Markdown files:
#   1. anti_gaming_check.py (GP-6 to GP-10)
#   2. rubric_leak_check.py (GP-11 / CLAUDE.md Rule 16)
#   3. em_dash_check.py    (CLAUDE.md Rule 17, added by plan v3.9.1 Phase Q-1.B)
#   4. lang_check.py       (CLAUDE.md Rule 17 language detection, added by plan v3.9.1 Phase Q-1.B)
#
# Bypass with --no-verify is strictly discouraged (CLAUDE.md Rule 4 plus the
# Quality over Speed mandate).
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
# Governance pre-commit hook (auto-installed via scripts/pre-commit-install.sh).
#
# Enforces:
#   - GP-6 to GP-10:    anti-gaming check on staged curriculum .md
#   - GP-11 / Rule 16:  rubric leak check on staged curriculum .md
#   - Rule 17 (em-dash): em-dash (U+2014) check on staged curriculum .md
#   - Rule 17 (lang):    language detection check on staged curriculum .md
#
# Bypass with `git commit --no-verify` is recorded in commit history; do NOT
# use without an explicit reason documented in the commit message.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
# Resolve a Python interpreter that has the project's runtime dependencies
# (lingua-language-detector for lang_check.py). On Windows, `python3` is
# often the Microsoft Store stub which has no third-party packages, while
# `python` points to a real installation. Prefer `python` first, then fall
# back to `python3`. The PYTHON env var still overrides the auto-detection.
if [ -n "${PYTHON:-}" ]; then
  :
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
elif command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  echo "ERROR: no python interpreter found on PATH" >&2
  exit 1
fi

ANTI="$REPO_ROOT/scripts/anti_gaming_check.py"
LEAK="$REPO_ROOT/scripts/rubric_leak_check.py"
EMDASH="$REPO_ROOT/scripts/em_dash_check.py"
LANG="$REPO_ROOT/scripts/lang_check.py"

# Skip hook if no .md files staged.
STAGED_MD="$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.md$' || true)"
if [ -z "$STAGED_MD" ]; then
  exit 0
fi

echo "pre-commit: anti_gaming_check on staged .md ..."
if [ -f "$ANTI" ]; then
  "$PYTHON" "$ANTI" --staged || {
    echo "FAIL anti_gaming_check, commit rejected per GP-6 to GP-10."
    echo "  Fix violations or override with --no-verify (not recommended)."
    exit 1
  }
else
  echo "  (skip: $ANTI not found)"
fi

echo "pre-commit: rubric_leak_check on staged .md ..."
if [ -f "$LEAK" ]; then
  "$PYTHON" "$LEAK" --staged || {
    echo "FAIL rubric_leak_check, commit rejected per GP-11 / CLAUDE.md Rule 16."
    echo "  Fix internal-term leak or override with --no-verify (not recommended)."
    exit 1
  }
else
  echo "  (skip: $LEAK not found)"
fi

echo "pre-commit: em_dash_check on staged .md ..."
if [ -f "$EMDASH" ]; then
  "$PYTHON" "$EMDASH" --staged || {
    echo "FAIL em_dash_check, commit rejected per CLAUDE.md Rule 17."
    echo "  Replace em-dash (U+2014) with comma, period, colon, parentheses,"
    echo "  or a bulleted list. Override with --no-verify is not recommended."
    exit 1
  }
else
  echo "  (skip: $EMDASH not found)"
fi

echo "pre-commit: lang_check on staged .md ..."
if [ -f "$LANG" ]; then
  "$PYTHON" "$LANG" --staged || {
    echo "FAIL lang_check, commit rejected per CLAUDE.md Rule 17."
    echo "  Translate every flagged chunk to English. Wrap CLI commands in"
    echo "  fenced code blocks or backticks so the detector skips them."
    echo "  Override with --no-verify is not recommended."
    exit 1
  }
else
  echo "  (skip: $LANG not found)"
fi

echo "OK pre-commit governance checks PASS."
exit 0
HOOK

chmod +x "$HOOK_PATH"

echo "Installed pre-commit hook at: $HOOK_PATH"
echo
echo "Test the hook by staging a curriculum .md file and running 'git commit'."
echo "It runs:"
echo "  - scripts/anti_gaming_check.py --staged   (GP-6 to GP-10)"
echo "  - scripts/rubric_leak_check.py --staged   (GP-11 / Rule 16)"
echo "  - scripts/em_dash_check.py --staged       (Rule 17, no em-dash)"
echo "  - scripts/lang_check.py --staged          (Rule 17, English-only prose)"
echo
echo "Bypass (not recommended): git commit --no-verify"
