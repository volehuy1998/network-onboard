"""Tests for scripts/lang_check.py.

Plan v3.9.1 Phase Q-1.B follow-up, 2026-04-28.

The check script enforces CLAUDE.md Rule 17 (every prose chunk must be in
English; strict mode rejects any chunk detected as Vietnamese with non-zero
confidence). These tests confirm:

- A clean English .md file passes.
- A .md file with a Vietnamese paragraph fails.
- A .md file with Vietnamese-without-diacritics fails (the binary
  English vs Vietnamese detector still identifies it).
- CLI commands inside fenced code blocks do not trigger false positives.
- CLI commands inside inline code spans do not trigger false positives.
- Short identifier lines do not trigger detection.
- A lab fixture (typical curriculum content with mixed prose and code
  blocks) passes.
- The ``--all`` mode walks tracked .md files.
- The ``--staged`` mode only reads staged files.
- A non-UTF-8 file fails rather than passing silently.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "lang_check.py"


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


def test_pure_english_passes(tmp_git_repo: Path) -> None:
    """A .md file with English-only prose returns exit 0."""
    f = tmp_git_repo / "english.md"
    f.write_text(
        "# Heading\n\n"
        "OVS classifier uses Tuple Space Search to partition rules by mask. "
        "Each mask becomes a subtable. Lookup runs in linear time over the "
        "number of subtables. The trade-off works well in practice.\n\n"
        "The kernel forwards the packet through the megaflow cache to "
        "userspace when it cannot match a flow.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_vietnamese_paragraph_fails(tmp_git_repo: Path) -> None:
    """A Vietnamese paragraph triggers FAIL with line number and detection scores."""
    f = tmp_git_repo / "vi.md"
    f.write_text(
        "# Heading\n\n"
        "Phần này mô tả cách OVS classifier hoạt động trên kernel datapath. "
        "Lưu lượng đi vào sẽ được phân loại dựa trên mask của flow rule.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "vi.md" in result.stdout
    assert "VIETNAMESE" in result.stdout
    assert "FAIL" in result.stdout


def test_vietnamese_without_diacritics_fails(tmp_git_repo: Path) -> None:
    """Vietnamese transliterated without diacritics is also caught when the
    sentence is plain Vietnamese (no English identifier mix).

    Limitation note: a sentence that mixes diacritic-free Vietnamese with
    many English technical identifiers (for example, OVS, classifier,
    kernel, datapath) can flip the binary detector toward English. The
    diacritic form remains the reliable trigger. In practice every legacy
    Vietnamese curriculum section uses diacritics, so this corner case is
    not a blocker.
    """
    f = tmp_git_repo / "vi_no_diac.md"
    f.write_text(
        "# Heading\n\n"
        "Phan nay mo ta cach he thong hoat dong tren may chu. "
        "Luu luong di vao duoc phan loai theo dieu kien.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "VIETNAMESE" in result.stdout


def test_cli_in_fenced_code_block_does_not_trigger(tmp_git_repo: Path) -> None:
    """CLI commands inside fenced code blocks must not be language-detected."""
    f = tmp_git_repo / "lab.md"
    f.write_text(
        "# Lab\n\n"
        "Run the commands below to set up the bridge. Each step is "
        "idempotent and safe to re-run on a clean lab host.\n\n"
        "```bash\n"
        "sudo ovs-vsctl add-br br0\n"
        "sudo ovs-vsctl add-port br0 tap1 -- set Interface tap1 type=internal\n"
        "sudo ip link set tap1 up\n"
        "sudo ip addr add 10.99.0.1/24 dev tap1\n"
        "```\n\n"
        "Verify by running the show command and inspecting the output.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_inline_code_does_not_trigger(tmp_git_repo: Path) -> None:
    """Inline code spans like `ovs-vsctl show` must not trigger detection."""
    f = tmp_git_repo / "inline.md"
    f.write_text(
        "# Inline\n\n"
        "Use `ovs-vsctl show` to list bridges. The command `ovs-appctl "
        "dpif/show` returns the per-bridge datapath state. Inspect "
        "`MFF_CT_ZONE` per `ct_zone` field via the OFPACT registry.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_short_identifier_lines_skipped(tmp_git_repo: Path) -> None:
    """Lines that are too short or are identifier-only are skipped."""
    f = tmp_git_repo / "short.md"
    f.write_text(
        "# Title\n\n"
        "ovs-vsctl\n"
        "br0\n"
        "MFF_CT_ZONE\n"
        "OK\n\n"
        "This is a real prose paragraph that should pass the language "
        "check because it has enough English signal to be detected.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_lab_fixture_with_mixed_prose_and_code_passes(tmp_git_repo: Path) -> None:
    """A typical curriculum lab section with prose, fenced code, inline
    code, and expected output passes the check."""
    f = tmp_git_repo / "lab_full.md"
    f.write_text(
        "# Lab 1\n\n"
        "## Setup steps\n\n"
        "Start by creating the bridge. Run the command below from a root "
        "shell on the test host.\n\n"
        "```bash\n"
        "sudo ovs-vsctl add-br br0\n"
        "sudo ovs-vsctl add-port br0 tap1 -- set Interface tap1 type=internal\n"
        "```\n\n"
        "Now verify the bridge exists. Run `ovs-vsctl show` and check that "
        "`br0` is listed in the output.\n\n"
        "## Verification\n\n"
        "Use `ovs-appctl dpif/show` to inspect the per-bridge datapath "
        "state. The command returns the backend type, the port list, and "
        "the flow count.\n\n"
        "```\n"
        "system@ovs-system: hit:0 missed:0\n"
        "  flows: cur: 0 avg: 0 max: 0 hash 0\n"
        "  port 1: br0 (internal)\n"
        "  port 2: tap1 (internal)\n"
        "```\n\n"
        "When the lab runs successfully, the line "
        "`port 2: tap1 (internal)` appears in the output.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_all_mode_scans_tracked_md(tmp_git_repo: Path) -> None:
    """--all walks every tracked .md file in the repo."""
    clean = tmp_git_repo / "clean.md"
    clean.write_text(
        "Clean English prose paragraph that should pass the language "
        "check without any issues.\n",
        encoding="utf-8",
    )
    dirty = tmp_git_repo / "dirty.md"
    dirty.write_text(
        "Phần này mô tả tình huống bị lỗi. Lưu lượng giảm đột ngột.\n",
        encoding="utf-8",
    )
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
    assert result.returncode == 1, result.stdout
    assert "dirty.md" in result.stdout


def test_staged_mode_only_staged_files(tmp_git_repo: Path) -> None:
    """--staged only reads staged files, not unstaged ones."""
    staged = tmp_git_repo / "staged.md"
    staged.write_text(
        "Phần này được stage và phải bị reject bởi lang_check.\n",
        encoding="utf-8",
    )
    unstaged = tmp_git_repo / "unstaged.md"
    unstaged.write_text(
        "Phần này không được stage nên không nên bị check.\n",
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", "staged.md"], cwd=str(tmp_git_repo), check=True
    )
    result = run_script(["--staged"], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "staged.md" in result.stdout
    assert "unstaged.md" not in result.stdout


def test_non_utf8_file_reported_as_failure(tmp_git_repo: Path) -> None:
    """A .md file that is not valid UTF-8 fails rather than passing silently."""
    bad = tmp_git_repo / "binary.md"
    bad.write_bytes(b"\xff\xfe\x00\x01 not utf-8")
    result = run_script(["--files", str(bad)], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "binary.md" in result.stdout
    assert "not valid UTF-8" in result.stdout


def test_mixed_english_and_vietnamese_fails_on_vi_only(tmp_git_repo: Path) -> None:
    """A file with both English and Vietnamese paragraphs fails. Only the
    Vietnamese chunks appear in the failure list."""
    f = tmp_git_repo / "mixed.md"
    f.write_text(
        "# Mixed\n\n"
        "This is a clean English paragraph that explains how OVS handles "
        "packets through the megaflow cache.\n\n"
        "Phần này thuộc legacy curriculum và chưa được dịch sang tiếng Anh "
        "trong plan v3.12.\n",
        encoding="utf-8",
    )
    result = run_script(["--files", str(f)], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "VIETNAMESE" in result.stdout
    # Make sure the English chunk is not in the failure block.
    assert "megaflow cache" not in result.stdout


def test_staged_diff_only_flags_added_vietnamese(tmp_git_repo: Path) -> None:
    """--staged scans only added or modified lines.

    A pre-existing legacy Vietnamese paragraph that the staged change
    does not touch must NOT be flagged. This is the diff-only behavior
    required by plan v3.9.1 §11.5 and the §8.3 mixed-language transition
    policy. The test commits a legacy Vietnamese paragraph, then stages
    a small English-only change to a different section. The result must
    PASS because the legacy Vietnamese was not added by this changeset.
    """
    f = tmp_git_repo / "legacy.md"
    initial = (
        "# Heading\n"
        "\n"
        "This English line is fine and stays in place.\n"
        "\n"
        "Phần này thuộc legacy curriculum và chưa được dịch sang tiếng Anh "
        "trong plan v3.12.\n"
        "\n"
        "Last English line is also fine and stays in place.\n"
    )
    f.write_text(initial, encoding="utf-8")
    subprocess.run(
        ["git", "add", "legacy.md"], cwd=str(tmp_git_repo), check=True
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "initial"],
        cwd=str(tmp_git_repo),
        check=True,
    )

    # Modify only the first English line; do not touch the Vietnamese
    # paragraph in the middle.
    updated = (
        "# Heading\n"
        "\n"
        "This English line is fine, slightly reworded but still English.\n"
        "\n"
        "Phần này thuộc legacy curriculum và chưa được dịch sang tiếng Anh "
        "trong plan v3.12.\n"
        "\n"
        "Last English line is also fine and stays in place.\n"
    )
    f.write_text(updated, encoding="utf-8")
    subprocess.run(
        ["git", "add", "legacy.md"], cwd=str(tmp_git_repo), check=True
    )

    result = run_script(["--staged"], cwd=tmp_git_repo)
    # The legacy Vietnamese paragraph is not in the staged diff, so the
    # result must PASS.
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout


def test_staged_diff_flags_added_vietnamese_chunk(tmp_git_repo: Path) -> None:
    """--staged flags Vietnamese prose on a newly added line."""
    f = tmp_git_repo / "legacy.md"
    initial = (
        "# Heading\n"
        "\n"
        "This English line is fine and stays in place.\n"
    )
    f.write_text(initial, encoding="utf-8")
    subprocess.run(
        ["git", "add", "legacy.md"], cwd=str(tmp_git_repo), check=True
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "initial"],
        cwd=str(tmp_git_repo),
        check=True,
    )

    updated = (
        "# Heading\n"
        "\n"
        "This English line is fine and stays in place.\n"
        "\n"
        "Đây là đoạn tiếng Việt mới được thêm vào curriculum và phải bị "
        "lang_check từ chối ngay tại commit này.\n"
    )
    f.write_text(updated, encoding="utf-8")
    subprocess.run(
        ["git", "add", "legacy.md"], cwd=str(tmp_git_repo), check=True
    )

    result = run_script(["--staged"], cwd=tmp_git_repo)
    assert result.returncode == 1, result.stdout
    assert "VIETNAMESE" in result.stdout
    # The newly added line is line 5 in the post-edit file.
    assert "L5" in result.stdout
