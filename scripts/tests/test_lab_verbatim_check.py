"""Tests for scripts/lab_verbatim_check.py.

Plan v3.13 R0a, 2026-04-29.

The check script enforces CLAUDE.md Rule 18 (Lab Output Verbatim
Integrity) on Markdown lab transcripts under ``sdn-onboard/labs/``.
These tests confirm:

- A clean transcript with a matching typescript passes.
- A transcript with a verbatim block that diverges from the typescript
  is reported with file path, line number, and offending content.
- The verbatim-source header must be present.
- The referenced typescript must exist and be non-empty.
- Out-of-scope files (outside ``sdn-onboard/labs/``) are skipped.
- The ``[N other lines omitted, context: ...]`` marker is allowed.
- Files staged via ``--staged`` are scoped correctly.
- The ``--all`` mode walks every tracked Markdown file under the
  labs prefix.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "lab_verbatim_check.py"
LABS = "sdn-onboard/labs"


def run_script(
    args: list[str], cwd: Path
) -> subprocess.CompletedProcess[str]:
    """Invoke the script under test in ``cwd``."""
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.fixture
def tmp_git_repo(tmp_path: Path) -> Path:
    """Initialise a tiny git repository in ``tmp_path``. The repo
    contains the ``sdn-onboard/labs/`` directory pre-created so tests
    can drop transcripts into it.
    """
    subprocess.run(["git", "init", "--quiet"], cwd=str(tmp_path), check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(tmp_path),
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=str(tmp_path), check=True
    )
    (tmp_path / LABS).mkdir(parents=True, exist_ok=True)
    return tmp_path


def write_typescript(repo: Path, name: str, content: str) -> Path:
    """Drop a typescript file under the labs directory and return its
    path.
    """
    p = repo / LABS / name
    p.write_text(content, encoding="utf-8")
    return p


def write_md(repo: Path, name: str, body: str) -> Path:
    """Drop a Markdown file under the labs directory and return its
    path.
    """
    p = repo / LABS / name
    p.write_text(body, encoding="utf-8")
    return p


def test_clean_transcript_passes(tmp_git_repo: Path) -> None:
    """A transcript whose verbatim block lines all appear in the
    typescript passes with exit 0.
    """
    write_typescript(
        tmp_git_repo,
        "v3.13-R0-baseline.typescript",
        "Script started on 2026-04-29\n"
        "root@lab-openvswitch:~# hostname\n"
        "lab-openvswitch\n"
        "root@lab-openvswitch:~# uname -r\n"
        "5.15.0-173-generic\n"
        "Script done on 2026-04-29\n",
    )
    write_md(
        tmp_git_repo,
        "v3.13-R0-baseline.md",
        "# R0 baseline\n"
        "\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0-baseline.typescript`\n"
        "\n"
        "```text\n"
        "root@lab-openvswitch:~# hostname\n"
        "lab-openvswitch\n"
        "root@lab-openvswitch:~# uname -r\n"
        "5.15.0-173-generic\n"
        "```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0-baseline.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_diverged_block_reports_line(tmp_git_repo: Path) -> None:
    """A verbatim block that anonymises an IP fails with the line
    number of the offence.
    """
    write_typescript(
        tmp_git_repo,
        "v3.13-R0-baseline.typescript",
        "root@lab-openvswitch:~# ip a | grep inet\n"
        "    inet 192.168.1.250/24 brd 192.168.1.255 scope global ens33\n",
    )
    write_md(
        tmp_git_repo,
        "v3.13-R0-baseline.md",
        "# R0\n"
        "\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0-baseline.typescript`\n"
        "\n"
        "```text\n"
        "root@lab-openvswitch:~# ip a | grep inet\n"
        "    inet <LAB_IP>/24 brd <LAB_BROADCAST> scope global ens33\n"
        "```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0-baseline.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 1
    assert "FAIL" in result.stdout
    assert "v3.13-R0-baseline.md" in result.stdout
    assert "<LAB_IP>" in result.stdout


def test_missing_header_is_rejected(tmp_git_repo: Path) -> None:
    """A Markdown file without the verbatim-source header fails."""
    write_typescript(
        tmp_git_repo, "v3.13-R0.typescript", "root@lab:~# hostname\nlab\n"
    )
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0 (no header)\n\n```text\nroot@lab:~# hostname\nlab\n```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 1
    assert "missing" in result.stdout
    assert "Verbatim source" in result.stdout


def test_missing_typescript_is_rejected(tmp_git_repo: Path) -> None:
    """If the header references a typescript file that does not exist,
    the check fails.
    """
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/missing.typescript`\n\n"
        "```text\nroot@lab:~# hostname\n```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 1
    assert "does not exist" in result.stdout


def test_empty_typescript_is_rejected(tmp_git_repo: Path) -> None:
    """An empty typescript file fails the check."""
    write_typescript(tmp_git_repo, "empty.typescript", "")
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/empty.typescript`\n\n"
        "```text\nroot@lab:~# hostname\n```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 1
    assert "is empty" in result.stdout


def test_no_verbatim_block_is_rejected(tmp_git_repo: Path) -> None:
    """A Markdown file with the header and a typescript but no fenced
    code block fails because there is no verbatim content to check.
    """
    write_typescript(
        tmp_git_repo, "v3.13-R0.typescript", "root@lab:~# hostname\nlab\n"
    )
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "Just prose, no code block.\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 1
    assert "no verbatim fenced code block" in result.stdout


def test_omitted_lines_marker_is_allowed(tmp_git_repo: Path) -> None:
    """The ``[N other lines omitted, context: ...]`` marker lets a
    block skip ahead in the typescript without failing.
    """
    typescript = (
        "root@lab:~# dmesg | tail\n"
        "[ 1.000] kernel boot line one\n"
        "[ 1.001] kernel boot line two\n"
        "[ 1.002] kernel boot line three\n"
        "[ 1.003] kernel boot line four\n"
        "[ 1.004] kernel boot line five\n"
    )
    write_typescript(tmp_git_repo, "v3.13-R0.typescript", typescript)
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "```text\n"
        "root@lab:~# dmesg | tail\n"
        "[ 1.000] kernel boot line one\n"
        "[3 other lines omitted, context: routine boot lines]\n"
        "[ 1.004] kernel boot line five\n"
        "```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_readme_under_labs_is_exempt(tmp_git_repo: Path) -> None:
    """``sdn-onboard/labs/README.md`` (and any nested ``README.md``
    under the labs directory) is a directory-index file, not a lab
    transcript. The check exempts it from the verbatim-source-header
    requirement.
    """
    write_md(
        tmp_git_repo,
        "README.md",
        "# Open vSwitch lab transcripts\n\n"
        "This is the directory index. No verbatim source needed.\n",
    )
    result = run_script(
        ["--files", f"{LABS}/README.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SKIP" in result.stderr or "PASS" in result.stdout


def test_out_of_scope_file_is_skipped(tmp_git_repo: Path) -> None:
    """A file outside ``sdn-onboard/labs/`` is skipped (not in scope of
    Rule 18). The check passes because nothing was actually checked.
    """
    other_dir = tmp_git_repo / "plans" / "sdn"
    other_dir.mkdir(parents=True, exist_ok=True)
    (other_dir / "draft.md").write_text(
        "# Some plan, not a lab transcript.\n", encoding="utf-8"
    )
    result = run_script(
        ["--files", "plans/sdn/draft.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SKIP" in result.stderr
    assert "PASS" in result.stdout


def test_all_mode_walks_tracked_files(tmp_git_repo: Path) -> None:
    """``--all`` finds every tracked .md file under
    ``sdn-onboard/labs/``.
    """
    write_typescript(
        tmp_git_repo, "v3.13-R0.typescript", "root@lab:~# hostname\nlab\n"
    )
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "```text\nroot@lab:~# hostname\nlab\n```\n",
    )
    subprocess.run(
        ["git", "add", f"{LABS}/v3.13-R0.md", f"{LABS}/v3.13-R0.typescript"],
        cwd=str(tmp_git_repo),
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "fixture"],
        cwd=str(tmp_git_repo),
        check=True,
    )
    result = run_script(["--all"], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_staged_mode_only_checks_staged(tmp_git_repo: Path) -> None:
    """``--staged`` only checks files in the current git index."""
    write_typescript(
        tmp_git_repo, "v3.13-R0.typescript", "root@lab:~# hostname\nlab\n"
    )
    bad = write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "```text\nroot@lab:~# hostname\nDIFFERENT_HOST\n```\n",
    )
    # Not staged, so --staged mode should not complain.
    result = run_script(["--staged"], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout + result.stderr
    # Stage it, now the bad content should be flagged.
    subprocess.run(
        ["git", "add", str(bad.relative_to(tmp_git_repo))],
        cwd=str(tmp_git_repo),
        check=True,
    )
    result = run_script(["--staged"], cwd=tmp_git_repo)
    assert result.returncode == 1
    assert "DIFFERENT_HOST" in result.stdout


def test_osc_title_escapes_in_typescript_are_stripped(
    tmp_git_repo: Path,
) -> None:
    """bash emits ``\\x1b]0;<title>\\x07`` to set the terminal title
    before each prompt. The OSC sits on the same typescript line as
    the prompt, so the check must strip it before comparing.
    """
    title_then_prompt = (
        "\x1b]0;root@lab-openvswitch: ~\x07"
        "root@lab-openvswitch:~# hostname\n"
        "lab-openvswitch\n"
    )
    write_typescript(tmp_git_repo, "v3.13-R0.typescript", title_then_prompt)
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "```text\n"
        "root@lab-openvswitch:~# hostname\n"
        "lab-openvswitch\n"
        "```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_ansi_escapes_in_typescript_are_stripped(tmp_git_repo: Path) -> None:
    """Coloured prompts in the raw typescript do not cause false
    positives; the check normalises ANSI codes before comparing.
    """
    coloured = (
        "\x1b[32mroot@lab-openvswitch\x1b[0m:~# hostname\n"
        "lab-openvswitch\n"
    )
    write_typescript(tmp_git_repo, "v3.13-R0.typescript", coloured)
    write_md(
        tmp_git_repo,
        "v3.13-R0.md",
        "# R0\n\n"
        "> **Verbatim source:** `sdn-onboard/labs/v3.13-R0.typescript`\n\n"
        "```text\n"
        "root@lab-openvswitch:~# hostname\n"
        "lab-openvswitch\n"
        "```\n",
    )
    result = run_script(
        ["--files", f"{LABS}/v3.13-R0.md"], cwd=tmp_git_repo
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
