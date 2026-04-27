"""Tests for scripts/em_dash_check.py.

Plan v3.9.1 Phase Q-1.B, 2026-04-28.

The check script enforces CLAUDE.md Rule 17 (no em-dash anywhere). These tests
confirm:

- A clean .md file passes.
- A .md file containing one or more em-dashes is reported with file path,
  line number, and line content.
- The ``--files`` mode works on a list of paths.
- The ``--all`` mode walks every tracked .md file.
- A non-UTF-8 .md file is reported as a failure (not a silent pass).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "em_dash_check.py"
EM_DASH = chr(0x2014)


def run_script(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.fixture
def tmp_git_repo(tmp_path: Path) -> Path:
    """Initialise a tiny git repo in ``tmp_path`` and return the path."""
    subprocess.run(
        ["git", "init", "--quiet"], cwd=str(tmp_path), check=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(tmp_path),
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(tmp_path),
        check=True,
    )
    return tmp_path


def test_clean_file_passes(tmp_git_repo: Path) -> None:
    """A .md file without any em-dash returns exit 0 and a PASS message."""
    f = tmp_git_repo / "clean.md"
    f.write_text("# Heading\n\nThis sentence is fine, no em-dash here.\n", encoding="utf-8")
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0
    assert "PASS" in result.stdout
    assert "FAIL" not in result.stdout


def test_em_dash_detected_with_line_number(tmp_git_repo: Path) -> None:
    """A .md file with an em-dash returns exit 1, names the file, line, and shows the content."""
    f = tmp_git_repo / "dirty.md"
    f.write_text(
        "# Heading\n\nThis sentence has a forbidden " + EM_DASH + " character.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "dirty.md" in result.stdout
    assert "L3" in result.stdout
    assert "FAIL" in result.stdout


def test_multiple_em_dashes_each_reported(tmp_git_repo: Path) -> None:
    """Multiple em-dashes across multiple lines are each reported."""
    f = tmp_git_repo / "multi.md"
    f.write_text(
        "Line one " + EM_DASH + " has one em-dash.\n"
        "Line two is clean.\n"
        "Line three " + EM_DASH + " also has one " + EM_DASH + " em-dash.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "L1" in result.stdout
    assert "L3" in result.stdout
    # The "(N em-dash hit)" header should report 2 lines (line 1 and line 3),
    # not 3, because the per-line print is one per line that contains at
    # least one em-dash.
    assert "(2 em-dash hit)" in result.stdout


def test_files_mode_with_mix_of_clean_and_dirty(tmp_git_repo: Path) -> None:
    """Mixed clean and dirty files: exit 1, only dirty files reported."""
    clean = tmp_git_repo / "clean.md"
    clean.write_text("All good.\n", encoding="utf-8")
    dirty = tmp_git_repo / "dirty.md"
    dirty.write_text("Bad " + EM_DASH + " here.\n", encoding="utf-8")
    result = run_script(["--files", str(clean), str(dirty)], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "dirty.md" in result.stdout
    assert "clean.md" not in result.stdout


def test_all_mode_scans_tracked_md(tmp_git_repo: Path) -> None:
    """--all walks every tracked .md file in the repo."""
    clean = tmp_git_repo / "clean.md"
    clean.write_text("Clean file.\n", encoding="utf-8")
    dirty = tmp_git_repo / "dirty.md"
    dirty.write_text("Dirty " + EM_DASH + " file.\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "clean.md", "dirty.md"],
        cwd=str(tmp_git_repo),
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "initial"],
        cwd=str(tmp_git_repo),
        check=True,
    )
    result = run_script(["--all"], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "dirty.md" in result.stdout


def test_staged_mode_only_staged_files(tmp_git_repo: Path) -> None:
    """--staged only reads staged files, not unstaged ones."""
    staged = tmp_git_repo / "staged.md"
    staged.write_text("Staged " + EM_DASH + " content.\n", encoding="utf-8")
    unstaged = tmp_git_repo / "unstaged.md"
    unstaged.write_text("Unstaged " + EM_DASH + " content.\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "staged.md"], cwd=str(tmp_git_repo), check=True
    )
    result = run_script(["--staged"], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "staged.md" in result.stdout
    # The unstaged file must not appear because --staged filters it out.
    assert "unstaged.md" not in result.stdout


def test_non_utf8_file_reported_as_failure(tmp_git_repo: Path) -> None:
    """A .md file that is not valid UTF-8 fails rather than silently passing."""
    bad = tmp_git_repo / "binary.md"
    bad.write_bytes(b"\xff\xfe\x00\x01 not utf-8")
    result = run_script(["--files", str(bad)], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "binary.md" in result.stdout
    assert "not valid UTF-8" in result.stdout


def test_en_dash_is_allowed(tmp_git_repo: Path) -> None:
    """U+2013 EN DASH is allowed (used for numeric ranges)."""
    f = tmp_git_repo / "en_dash.md"
    f.write_text("OVS 2.5–2.6 has the feature.\n", encoding="utf-8")
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0
    assert "PASS" in result.stdout


def test_hyphen_is_allowed(tmp_git_repo: Path) -> None:
    """Plain ASCII hyphen-minus is allowed."""
    f = tmp_git_repo / "hyphen.md"
    f.write_text("Use comma-separated values.\n", encoding="utf-8")
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0
    assert "PASS" in result.stdout
