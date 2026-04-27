"""Unit tests for scripts/rubric_leak_check.py v2.

Coverage:
  - V1 regression: 3 patterns must still detect (axis-bold-label, cohort-label,
    tier-label-deep).
  - V2 new patterns: 7 patterns must detect their target leak (axis-numbered-vn-heading,
    cohort-cornerstone-phrase, tier-cornerstone-informal, tier-importance-bold-label,
    phase-session-reference, cohort-batch-stamp-leftover, stale-phase-compat-note).
  - Negative cases: memory/plan files exempt, code blocks skipped, total pattern count.

Run:
  pytest scripts/tests/test_rubric_leak_check.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import rubric_leak_check as rlc  # noqa: E402


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #


@pytest.fixture
def tmp_curriculum_file(tmp_path: Path) -> Path:
    """Create a temp file path emulating sdn-onboard/ curriculum layout.

    Note: scan_file() resolves is_curriculum() against REPO_ROOT, so to
    exercise the curriculum-detect branch we must monkey-patch REPO_ROOT
    via the path layout: tmp_path/sdn-onboard/<file>.md and override
    rlc.REPO_ROOT to tmp_path for the test duration.
    """
    sdn_dir = tmp_path / "sdn-onboard"
    sdn_dir.mkdir()
    return sdn_dir / "X.Y - test-leak.md"


@pytest.fixture(autouse=True)
def patch_repo_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Force scan_file() to treat tmp_path as REPO_ROOT so sdn-onboard/...
    layout is recognised as curriculum."""
    monkeypatch.setattr(rlc, "REPO_ROOT", tmp_path)


# --------------------------------------------------------------------------- #
# V1 regression tests (must still PASS after v2 additions)
# --------------------------------------------------------------------------- #


def test_v1_axis_bold_label_still_caught(tmp_curriculum_file: Path) -> None:
    tmp_curriculum_file.write_text(
        "**Axis 7 Importance.** Foo bar.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "axis-bold-label" for v in leaks), \
        f"Expected axis-bold-label leak, got: {[v.pattern_name for v in leaks]}"


def test_v1_cohort_label_still_caught(tmp_curriculum_file: Path) -> None:
    tmp_curriculum_file.write_text(
        "Members of cohort C7 include the following keywords.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "cohort-label" for v in leaks)


def test_v1_deep_tier_label_still_caught(tmp_curriculum_file: Path) -> None:
    tmp_curriculum_file.write_text(
        "This keyword reaches DEEP-20 tier classification.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "tier-label-deep" for v in leaks)


# --------------------------------------------------------------------------- #
# V2 new pattern tests (positive cases)
# --------------------------------------------------------------------------- #


def test_v2_axis_numbered_vn_heading_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches '### N. Khái niệm' style axis-numbered VN heading."""
    tmp_curriculum_file.write_text(
        "## §9.32.1 TSS classifier\n"
        "\n"
        "### 1. Khái niệm\n"
        "\n"
        "TSS là thuật toán tra cứu...\n"
        "\n"
        "### 7. Tầm quan trọng\n"
        "\n"
        "Đây là cốt lõi.\n"
        "\n"
        "### 20. Cross-domain comparison\n"
        "\n"
        "So sánh với P4...\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    matches = [v for v in leaks if v.pattern_name == "axis-numbered-vn-heading"]
    assert len(matches) == 3, \
        f"Expected 3 axis-numbered-vn-heading hits, got {len(matches)}: " \
        f"{[v.matched for v in matches]}"


def test_v2_cohort_cornerstone_phrase_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches 'cohort cornerstone' phrase in body."""
    tmp_curriculum_file.write_text(
        "## 9.2.14 Bổ sung chuyên sâu cohort cornerstone OVS datapath\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "cohort-cornerstone-phrase" for v in leaks)


def test_v2_tier_cornerstone_informal_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches 'Tier 1 cornerstone' / 'cornerstone tier 1 tuyệt đối'."""
    tmp_curriculum_file.write_text(
        "Đây là Tier 1 cornerstone của OVS classifier.\n"
        "Còn cái này là cornerstone tier 1 tuyệt đối.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    matches = [v for v in leaks if v.pattern_name == "tier-cornerstone-informal"]
    assert len(matches) >= 2, \
        f"Expected >=2 tier-cornerstone-informal hits, got {len(matches)}"


def test_v2_tier_importance_bold_label_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches '**Tier importance: cornerstone tuyệt đối**' label."""
    tmp_curriculum_file.write_text(
        "**Tier importance: cornerstone tuyệt đối** of multi-table pipeline.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "tier-importance-bold-label" for v in leaks)


def test_v2_phase_session_reference_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches 'Phase H session SN' embedded reference."""
    tmp_curriculum_file.write_text(
        "## §9.11.X (Phase H session S39 expansion)\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "phase-session-reference" for v in leaks)


def test_v2_cohort_batch_stamp_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches '(compact treatment per cohort batch limit)' leftover."""
    tmp_curriculum_file.write_text(
        "### 9-20. (compact treatment per cohort batch limit)\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "cohort-batch-stamp-leftover" for v in leaks)


def test_v2_stale_phase_compat_note_caught(tmp_curriculum_file: Path) -> None:
    """Pattern catches '(reference, giữ tương thích content Phase B)'."""
    tmp_curriculum_file.write_text(
        "Mục tiêu bài học cũ (reference, giữ tương thích content Phase B).\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert any(v.pattern_name == "stale-phase-compat-note" for v in leaks)


# --------------------------------------------------------------------------- #
# Negative tests (exempt / skip cases)
# --------------------------------------------------------------------------- #


def test_negative_memory_file_exempt(tmp_path: Path) -> None:
    """Files in memory/ should be exempt from check."""
    mem_dir = tmp_path / "memory" / "sdn"
    mem_dir.mkdir(parents=True)
    f = mem_dir / "tracker.md"
    f.write_text("**Axis 7 Importance.** Internal note.\n", encoding="utf-8")
    rel_str = "memory/sdn/tracker.md"
    assert any(rel_str.startswith(d) for d in rlc.EXEMPT_DIRS)


def test_negative_claude_md_exempt() -> None:
    """CLAUDE.md must be in EXEMPT_TOP_FILES."""
    assert "CLAUDE.md" in rlc.EXEMPT_TOP_FILES


def test_negative_codeblock_skipped(tmp_curriculum_file: Path) -> None:
    """Rubric vocabulary inside fenced code blocks must NOT trigger leak."""
    tmp_curriculum_file.write_text(
        "Normal text without leak.\n"
        "\n"
        "```python\n"
        "# This is a fake leak inside code: **Axis 7 Importance.**\n"
        "axis_count = 20\n"
        "# Also: cohort cornerstone, Tier 1 cornerstone, DEEP-20\n"
        "```\n"
        "\n"
        "More normal text without leak.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert len(leaks) == 0, \
        f"Expected 0 leak (all in code block), got {len(leaks)}: " \
        f"{[(v.pattern_name, v.matched) for v in leaks]}"


# --------------------------------------------------------------------------- #
# Integration: total pattern count + clean-file negative
# --------------------------------------------------------------------------- #


def test_total_pattern_count_v2() -> None:
    """V2 has 20 patterns total (13 v1 + 7 v2)."""
    assert len(rlc.LEAK_PATTERNS) == 20, \
        f"Expected 20 patterns, got {len(rlc.LEAK_PATTERNS)}"


def test_clean_curriculum_file_no_leak(tmp_curriculum_file: Path) -> None:
    """File with no rubric vocabulary should produce zero leak."""
    tmp_curriculum_file.write_text(
        "# 9.X - Open vSwitch foundation\n"
        "\n"
        "## Khái niệm\n"
        "\n"
        "OVS là một virtual switch implementation.\n"
        "\n"
        "## Cơ chế hoạt động\n"
        "\n"
        "- Kernel datapath: openvswitch.ko\n"
        "- Userspace daemon: ovs-vswitchd\n"
        "- Database: ovsdb-server\n"
        "\n"
        "Cross-link: Phần 9.2 megaflow, Phần 10.0 OVSDB.\n",
        encoding="utf-8",
    )
    leaks: list[rlc.Leak] = []
    rlc.scan_file(tmp_curriculum_file, leaks)
    assert len(leaks) == 0, \
        f"Expected 0 leak in clean file, got {len(leaks)}: " \
        f"{[(v.pattern_name, v.matched) for v in leaks]}"
