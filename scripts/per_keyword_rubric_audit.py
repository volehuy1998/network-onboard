#!/usr/bin/env python3
"""v3.7 Phase D: Per-keyword 20-axis rubric audit.

Score each REF keyword on 20-axis depth rubric per
``memory/sdn/rubric-20-per-keyword.md`` Section 22.

Inputs:
  - REF: ``sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md``
  - Curriculum: ``sdn-onboard/*.md``
  - Rubric: ``memory/sdn/rubric-20-per-keyword.md``

Outputs:
  - ``memory/sdn/keyword-rubric-scorecard.md`` master scorecard
  - ``memory/sdn/keyword-rubric-flags.md`` low-confidence flag for manual review

Auto-detection per axis is heuristic. Per pilot Phase C average 75%
confidence. Manual override expected ~25% via ``manual-overrides.csv``.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(r"C:\Users\voleh\Documents\network-onboard")
REF = REPO / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
CURRICULUM_DIR = REPO / "sdn-onboard"
SCORECARD_OUT = REPO / "memory" / "sdn" / "keyword-rubric-scorecard.md"
FLAGS_OUT = REPO / "memory" / "sdn" / "keyword-rubric-flags.md"

LOOKUP_SPINE_FILES = {"0.3 - master-keyword-index.md"}
TROUBLESHOOT_FILES = {f"20.{i} -" for i in range(8)} | {"9.14 -", "9.25 -", "9.26 -", "19.0 -", "17.0 -"}
LAB_FILES = {"9.21 -", "11.3 -", "11.4 -", "9.7 -"}


BANNED_REGEXES = [
    r"\bdpdk\b", r"\bpmd\b", r"\bemc\b", r"\bsmc\b",
    r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd",
    r"\bhugepage\b",
]


@dataclass
class KeywordEntry:
    name: str
    section: str = ""
    subsection: str = ""
    bucket: str = ""
    banned: bool = False
    ref_line: int = 0


@dataclass
class AxisScore:
    axis_id: int
    axis_name: str
    score: float = 0.0
    is_na: bool = False
    confidence: str = "low"
    evidence: list[str] = field(default_factory=list)


@dataclass
class KeywordScorecard:
    keyword: str
    entry: KeywordEntry
    aliases: list[str]
    files_matched: list[str]
    axis_scores: list[AxisScore]
    total: float = 0.0
    effective_denominator: float = 20.0
    normalized: float = 0.0
    tier: str = "PLACEHOLDER"


# ---------------------------------------------------------------------------
# REF parsing (reuse pattern từ refine_coverage_matrix_v2.py)
# ---------------------------------------------------------------------------


SKIP_BOLD_LABELS = {
    "Problem.", "Layered checklist.", "Likely root-cause categories.",
    "Note.", "Warning.", "Source:", "Example:", "Synopsis:",
}


def is_banned(name: str, context: str) -> bool:
    text = (name + " " + context).lower()
    return any(re.search(pat, text, re.IGNORECASE) for pat in BANNED_REGEXES)


def detect_section(line: str, current: dict) -> dict:
    m = re.match(r"^## (\d)\. (.+)$", line)
    if m:
        current["section"] = m.group(1)
        current["section_name"] = m.group(2).strip()
        current["subsection"] = ""
        current["subsection_name"] = ""
        return current
    m = re.match(r"^### (\d)\.(\d) (.+)$", line)
    if m:
        current["subsection"] = f"{m.group(1)}.{m.group(2)}"
        current["subsection_name"] = m.group(3).strip()
    return current


def detect_entry(line: str, next_line: str = "") -> tuple[str, str] | None:
    m = re.match(r"^- \*\*([^*]+)\*\*\s*[—\-–|]?\s*(.*)$", line)
    if m:
        name = m.group(1).strip()
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, m.group(2).strip())
    m = re.match(r"^\*\*([^*]+)\*\*$", line)
    if m:
        name = m.group(1).strip()
        if name in SKIP_BOLD_LABELS:
            return None
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, next_line.strip())
    return None


def detect_subsection_heading(line: str) -> tuple[str, str] | None:
    m = re.match(r"^#### `?([^`]+)`?$", line)
    if m:
        return (m.group(1).strip().rstrip("`"), "CLI tool")
    return None


def detect_scenario(line: str) -> tuple[str, str] | None:
    m = re.match(r"^### (\d+)\. (.+)$", line)
    if m:
        return (f"Scenario {m.group(1)}: {m.group(2).strip()}", "production troubleshoot")
    return None


def parse_ref() -> list[KeywordEntry]:
    lines = REF.read_text(encoding="utf-8").splitlines()
    entries: list[KeywordEntry] = []
    state = {"section": "", "section_name": "", "subsection": "", "subsection_name": ""}
    seen = set()
    for i, line in enumerate(lines):
        state = detect_section(line, state)
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        entry = (
            detect_entry(line, next_line)
            or detect_subsection_heading(line)
            or detect_scenario(line)
        )
        if not entry:
            continue
        name, context = entry
        key = (name, state.get("section", ""))
        if key in seen:
            continue
        seen.add(key)
        bucket_match = re.search(r"Bucket[:\s|]+(\w+)", context)
        bucket = bucket_match.group(1) if bucket_match else state.get("section_name", "")
        entries.append(KeywordEntry(
            name=name,
            section=state.get("section", ""),
            subsection=state.get("subsection", ""),
            bucket=bucket,
            banned=is_banned(name, context),
            ref_line=i + 1,
        ))
    return entries


# ---------------------------------------------------------------------------
# Alias generation (reuse v2 logic)
# ---------------------------------------------------------------------------


def extract_aliases(name: str) -> list[str]:
    candidates: list[str] = [name]
    stripped = re.sub(r"^(Action|Instruction|Match field|Field):\s+", "", name)
    if stripped != name:
        candidates.append(stripped)
    no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", stripped).strip()
    if no_paren and no_paren not in candidates:
        candidates.append(no_paren)
    no_tool = re.sub(
        r"^(ovn-nbctl|ovn-sbctl|ovn-appctl|ovn-ic-nbctl|ovn-ic-sbctl|"
        r"ovs-vsctl|ovs-ofctl|ovs-appctl|ovs-dpctl|ovsdb-tool|ovsdb-client)\s+",
        "", no_paren,
    )
    if no_tool != no_paren and no_tool not in candidates:
        candidates.append(no_tool)
    no_table_suffix = re.sub(r"\s+table$", "", no_paren, flags=re.IGNORECASE).strip()
    if no_table_suffix != no_paren and no_table_suffix and no_table_suffix not in candidates:
        candidates.append(no_table_suffix)
    for src in (name, stripped, no_paren):
        if "/" in src and "(" not in src:
            for part in src.split("/"):
                p = part.strip()
                if p and p not in candidates and len(p) >= 3:
                    candidates.append(p)
    GENERIC_BLACKLIST = {"of", "it", "is", "as", "at", "to", "in", "on", "or", "no", "ct"}
    filtered = []
    for c in candidates:
        cs = c.strip()
        if not cs:
            continue
        if cs.lower() in GENERIC_BLACKLIST:
            continue
        if len(cs) < 3:
            if not any(ch.isupper() or ch.isdigit() for ch in cs):
                continue
        filtered.append(cs)
    return filtered if filtered else [name]


def grep_curriculum(alias: str, files: list[Path]) -> list[tuple[str, int, str]]:
    """Return [(filename, line_no, line_text), ...] for alias matches."""
    matches: list[tuple[str, int, str]] = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for ln, line in enumerate(content.split("\n"), 1):
                if alias in line:
                    matches.append((f.name, ln, line))
        except Exception:
            continue
    return matches


# ---------------------------------------------------------------------------
# Axis scoring heuristics
# ---------------------------------------------------------------------------


def _has_pattern(matches: list[tuple[str, int, str]], pattern: str, flags: int = 0,
                 context_window: int = 0, all_lines: dict[str, list[str]] | None = None) -> tuple[bool, list[str]]:
    """Check if pattern present in any matched line OR within window."""
    rx = re.compile(pattern, flags)
    evidence = []
    for fname, ln, line in matches:
        if rx.search(line):
            evidence.append(f"{fname}:{ln}")
    if context_window > 0 and all_lines:
        for fname, ln, _ in matches:
            file_lines = all_lines.get(fname, [])
            lo = max(0, ln - 1 - context_window)
            hi = min(len(file_lines), ln - 1 + context_window + 1)
            for ctx_ln in range(lo, hi):
                if rx.search(file_lines[ctx_ln]):
                    evidence.append(f"{fname}:{ctx_ln + 1}(ctx)")
                    break
    return (bool(evidence), evidence[:3])


def score_axis(axis_id: int, name: str, matches: list[tuple[str, int, str]],
               file_lines: dict[str, list[str]], substantive_files: list[str]) -> AxisScore:
    """Score 1 axis based on heuristic patterns + matches."""
    axis_names = {
        1: "Concept", 2: "History", 3: "Placement", 4: "Role",
        5: "Motivation", 6: "Problem", 7: "Importance",
        8: "Mechanism", 9: "Engineer-op", 10: "Taxonomy",
        11: "Workflow", 12: "Troubleshoot", 13: "Coupling",
        14: "Version drift", 15: "Verification",
        16: "Source code", 17: "Incident", 18: "Lab",
        19: "Failure mode", 20: "Cross-domain",
    }
    sc = AxisScore(axis_id=axis_id, axis_name=axis_names[axis_id])

    if not matches:
        sc.score = 0
        sc.confidence = "high"
        return sc

    has_substantive = bool(substantive_files)

    if axis_id == 1:
        has_def = bool(re.search(r"là\s+(một|cái|loại|một loại)?\s*\w+", " ".join(m[2] for m in matches[:5]), re.IGNORECASE))
        if substantive_files and len(substantive_files) >= 1:
            sc.score = 1.0 if has_def else 0.5
            sc.confidence = "high"
            sc.evidence = [f"{f}:bucket" for f in substantive_files[:2]]
        elif matches:
            sc.score = 0.5
            sc.evidence = [f"{matches[0][0]}:{matches[0][1]}"]

    elif axis_id == 2:
        present, ev = _has_pattern(matches, r"(OVS|OVN|OF|OpenFlow)\s+\d\.\d+|20\d{2}|Nicira|Pfaff|Stanford", re.IGNORECASE)
        sc.score = 1.0 if present and len(ev) >= 2 else (0.5 if present else 0)
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 3:
        present, ev = _has_pattern(matches, r"(kernel datapath|userspace|ovsdb-server|ofproto-dpif|control plane|br-int|chassis-side|centralize)", re.IGNORECASE)
        sc.score = 1.0 if present else 0.5 if matches else 0
        sc.evidence = ev
        sc.confidence = "high"

    elif axis_id == 4:
        present, ev = _has_pattern(matches, r"(vai trò|role|function|nhiệm vụ|đóng góp)", re.IGNORECASE)
        sc.score = 1.0 if present and has_substantive else 0.5 if matches else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 5:
        present, ev = _has_pattern(matches, r"(vì sao|motivation|lý do|pain point|trước đó|before|ra đời)", re.IGNORECASE)
        sc.score = 1.0 if present and len(ev) >= 1 and has_substantive else 0.5 if present else 0
        sc.evidence = ev
        sc.confidence = "low"

    elif axis_id == 6:
        present, ev = _has_pattern(matches, r"(vấn đề|problem|giải quyết|solves|address)", re.IGNORECASE)
        sc.score = 1.0 if present and has_substantive else 0.5 if present else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 7:
        present, ev = _has_pattern(matches, r"(trụ cột|cốt lõi|central|foundation|tier 1|tuyệt đối|must know|critical)", re.IGNORECASE)
        sc.score = 1.0 if present else 0.5 if has_substantive and len(matches) >= 5 else 0
        sc.evidence = ev
        sc.confidence = "low"

    elif axis_id == 8:
        present, ev = _has_pattern(matches, r"(cơ chế|mechanism|nguyên lý|algorithm|hash|TSS|invariant|state machine|transition)", re.IGNORECASE)
        sc.score = 1.0 if present and has_substantive else 0.5 if matches else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 9:
        anatomy_present, ev = _has_pattern(matches, r"(Anatomy|Guided Exercise|GE|Capstone|decision tree|skill)", re.IGNORECASE)
        sc.score = 1.0 if anatomy_present and len(ev) >= 1 else 0.5 if has_substantive else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 10:
        present, ev = _has_pattern(matches, r"(Loại:|Type:|Category:|Bucket\s*\|)", re.IGNORECASE)
        sc.score = 1.0 if present else 0.5 if has_substantive else 0
        sc.evidence = ev
        sc.confidence = "high"

    elif axis_id == 11:
        present, ev = _has_pattern(matches, r"(Step\s*\d|Workflow|^\d\.|Best practice|Anti-pattern)", re.MULTILINE | re.IGNORECASE)
        sc.score = 1.0 if present and has_substantive else 0.5 if matches else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 12:
        in_troubleshoot = any(any(t in f for t in TROUBLESHOOT_FILES) for f in substantive_files)
        present, ev = _has_pattern(matches, r"(Khi nào|symptom|sự cố|failure|troubleshoot)", re.IGNORECASE)
        sc.score = 1.0 if in_troubleshoot and present else 0.5 if in_troubleshoot or present else 0
        sc.evidence = ev + [f"{f}:troubleshoot-file" for f in substantive_files if any(t in f for t in TROUBLESHOOT_FILES)][:2]
        sc.confidence = "low"

    elif axis_id == 13:
        present, ev = _has_pattern(matches, r"(Cross-link|Cross-reference|Liên quan|tightly coupled|phụ thuộc|→\s*Phần|§\d)", re.IGNORECASE)
        sc.score = 1.0 if present and len(ev) >= 2 else 0.5 if present else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 14:
        version_count = sum(1 for m in matches if re.search(r"(OVS|OVN|OF|OpenFlow)\s+\d\.\d+", m[2], re.IGNORECASE))
        if version_count >= 3:
            sc.score = 1.0
        elif version_count >= 1:
            sc.score = 0.5
        else:
            sc.score = 0
        sc.evidence = [f"{m[0]}:{m[1]}" for m in matches[:3] if re.search(r"\d\.\d+", m[2])]
        sc.confidence = "high"

    elif axis_id == 15:
        present, ev = _has_pattern(matches, r"(\$ ovs-|\$ ovn-|dpctl/|ofproto/trace|appctl|dump-flows|list\s+\w+)")
        sc.score = 1.0 if present and len(ev) >= 1 else 0.5 if has_substantive else 0
        sc.evidence = ev
        sc.confidence = "high"

    elif axis_id == 16:
        present, ev = _has_pattern(matches, r"(lib/|controller/|northd/|include/|net/netfilter|\w+\.c\b|\w+\.h\b)")
        sc.score = 1.0 if present and len(ev) >= 1 else 0.5 if has_substantive else 0
        sc.evidence = ev
        sc.confidence = "high"

    elif axis_id == 17:
        in_forensic = any(any(t in f for t in {"19.0 -", "17.0 -", "20.5 -", "9.26 -"}) for f in substantive_files)
        present, ev = _has_pattern(matches, r"(case study|production|FDP-|forensic|incident)", re.IGNORECASE)
        sc.score = 1.0 if in_forensic and present else 0.5 if in_forensic or present else 0
        sc.evidence = ev
        sc.confidence = "low"

    elif axis_id == 18:
        in_lab = any(any(t in f for t in LAB_FILES) for f in substantive_files)
        present, ev = _has_pattern(matches, r"(Mininet|GE\d|Lab\s*\d|Guided Exercise|topology)", re.IGNORECASE)
        sc.score = 1.0 if in_lab and present else 0.5 if in_lab or present else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 19:
        present, ev = _has_pattern(matches, r"(Failure mode|Hiểu sai|Anti-pattern|recovery|fix:|signal:)", re.IGNORECASE)
        sc.score = 1.0 if present and len(ev) >= 2 else 0.5 if present else 0
        sc.evidence = ev
        sc.confidence = "medium"

    elif axis_id == 20:
        present, ev = _has_pattern(matches, r"(iptables|Cisco|NSX|Linux bridge|tương tự|≈|cross-domain|so sánh.*Linux)", re.IGNORECASE)
        sc.score = 1.0 if present and len(ev) >= 1 else 0.5 if present else 0
        sc.evidence = ev
        sc.confidence = "low"

    return sc


def classify_tier(normalized: float) -> str:
    if normalized >= 18.0:
        return "DEEP-20"
    if normalized >= 15.0:
        return "DEEP-15"
    if normalized >= 10.0:
        return "PARTIAL-10"
    if normalized >= 5.0:
        return "REFERENCE-5"
    return "PLACEHOLDER"


def audit_keyword(entry: KeywordEntry, files: list[Path],
                  file_lines: dict[str, list[str]]) -> KeywordScorecard:
    aliases = extract_aliases(entry.name)
    all_matches: list[tuple[str, int, str]] = []
    files_matched: set[str] = set()
    for alias in aliases:
        m = grep_curriculum(alias, files)
        all_matches.extend(m)
        files_matched.update(x[0] for x in m)
    files_matched_list = sorted(files_matched)
    substantive_files = [f for f in files_matched_list if f not in LOOKUP_SPINE_FILES]

    axis_scores: list[AxisScore] = []
    for axis_id in range(1, 21):
        axis_scores.append(score_axis(axis_id, entry.name, all_matches, file_lines, substantive_files))

    total = sum(a.score for a in axis_scores if not a.is_na)
    effective = sum(1 for a in axis_scores if not a.is_na)
    normalized = total / effective * 20 if effective > 0 else 0
    tier = classify_tier(normalized)

    return KeywordScorecard(
        keyword=entry.name,
        entry=entry,
        aliases=aliases,
        files_matched=files_matched_list,
        axis_scores=axis_scores,
        total=total,
        effective_denominator=effective,
        normalized=normalized,
        tier=tier,
    )


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def emit_scorecard(scorecards: list[KeywordScorecard]) -> None:
    SCORECARD_OUT.parent.mkdir(parents=True, exist_ok=True)
    out: list[str] = []
    out.append("# Keyword Rubric Scorecard (v3.7 Phase D output)")
    out.append("")
    out.append("> **Auto-generated** by `scripts/per_keyword_rubric_audit.py`.")
    out.append(f"> **Total keyword:** {len(scorecards)}")
    out.append(f"> **Rubric:** `memory/sdn/rubric-20-per-keyword.md` v1.0")
    out.append(f"> **Confidence:** auto-detect heuristic ~75%, manual override ~25% via `manual-overrides.csv` (Phase D2 manual review).")
    out.append("")

    tier_counts: dict[str, int] = defaultdict(int)
    for s in scorecards:
        tier_counts[s.tier] += 1

    out.append("## Tier distribution")
    out.append("")
    out.append("| Tier | Count | % | Threshold |")
    out.append("|------|-------|---|-----------|")
    total = len(scorecards)
    for tier, threshold in [
        ("DEEP-20", "≥ 18/20"),
        ("DEEP-15", "15-17.5/20"),
        ("PARTIAL-10", "10-14.5/20"),
        ("REFERENCE-5", "5-9.5/20"),
        ("PLACEHOLDER", "< 5/20"),
    ]:
        c = tier_counts[tier]
        pct = f"{c * 100 / total:.1f}%" if total else "0%"
        out.append(f"| {tier} | {c} | {pct} | {threshold} |")
    out.append("")

    avg = sum(s.normalized for s in scorecards) / total if total else 0
    out.append(f"**Aggregate average:** {avg:.2f}/20 ({avg / 20 * 100:.1f}%)")
    out.append("")
    out.append("---")
    out.append("")

    grouped: dict[str, list[KeywordScorecard]] = defaultdict(list)
    for s in scorecards:
        key = f"{s.entry.section}.{s.entry.subsection}" if s.entry.subsection else s.entry.section
        grouped[key].append(s)

    for section_key in sorted(grouped.keys()):
        sec_entries = grouped[section_key]
        if not sec_entries:
            continue
        out.append(f"## REF Section {section_key} ({len(sec_entries)} keyword)")
        out.append("")
        out.append("| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |")
        out.append("|---------|-------|------|-------|---------------|---------------|")
        for s in sec_entries:
            name_safe = s.keyword.replace("|", "\\|")[:60]
            pass_axes = sorted([a for a in s.axis_scores if a.score >= 0.5],
                              key=lambda x: -x.score)[:3]
            fail_axes = [a for a in s.axis_scores if a.score == 0][:3]
            pass_str = ",".join(str(a.axis_id) for a in pass_axes)
            fail_str = ",".join(str(a.axis_id) for a in fail_axes)
            out.append(f"| `{name_safe}` | {s.normalized:.1f}/20 | {s.tier} | {len(s.files_matched)} | {pass_str} | {fail_str} |")
        out.append("")

    SCORECARD_OUT.write_text("\n".join(out), encoding="utf-8")


def emit_flags(scorecards: list[KeywordScorecard]) -> None:
    out: list[str] = []
    out.append("# Keyword Rubric Flags (low-confidence axis scores)")
    out.append("")
    out.append("> **Auto-generated** for manual review per Section 25.1 rubric.")
    out.append("> **Trigger:** axis confidence == 'low' OR score == 0.5 (partial)")
    out.append("")
    out.append("## Flagged entries")
    out.append("")
    out.append("| Keyword | Axis | Score | Confidence | Evidence |")
    out.append("|---------|------|-------|------------|----------|")
    for s in scorecards:
        for a in s.axis_scores:
            if a.confidence == "low" or (a.score == 0.5 and a.confidence == "medium"):
                ev_safe = ", ".join(a.evidence[:2]).replace("|", "\\|") if a.evidence else "-"
                kw_safe = s.keyword.replace("|", "\\|")[:50]
                out.append(f"| `{kw_safe}` | {a.axis_id} {a.axis_name} | {a.score} | {a.confidence} | {ev_safe} |")
    FLAGS_OUT.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    print("Parsing REF...")
    entries = parse_ref()
    in_scope = [e for e in entries if not e.banned]
    print(f"  REF entries total: {len(entries)}, in-scope: {len(in_scope)}, banned: {len(entries) - len(in_scope)}")

    print("Loading curriculum files...")
    files = sorted(CURRICULUM_DIR.glob("*.md"))
    file_lines: dict[str, list[str]] = {}
    for f in files:
        try:
            file_lines[f.name] = f.read_text(encoding="utf-8", errors="ignore").split("\n")
        except Exception:
            file_lines[f.name] = []
    print(f"  Curriculum files: {len(files)}")

    print("Auditing per keyword (this may take 1-2 minutes)...")
    scorecards: list[KeywordScorecard] = []
    for i, e in enumerate(in_scope):
        sc = audit_keyword(e, files, file_lines)
        scorecards.append(sc)
        if (i + 1) % 50 == 0:
            print(f"  Audited {i + 1}/{len(in_scope)}")

    print("Emitting outputs...")
    emit_scorecard(scorecards)
    emit_flags(scorecards)

    avg = sum(s.normalized for s in scorecards) / len(scorecards) if scorecards else 0
    print(f"\nResult:")
    print(f"  Total in-scope keyword: {len(scorecards)}")
    print(f"  Aggregate avg: {avg:.2f}/20 ({avg / 20 * 100:.1f}%)")
    tier_counts: dict[str, int] = defaultdict(int)
    for s in scorecards:
        tier_counts[s.tier] += 1
    for tier in ["DEEP-20", "DEEP-15", "PARTIAL-10", "REFERENCE-5", "PLACEHOLDER"]:
        print(f"  {tier}: {tier_counts[tier]} ({tier_counts[tier] * 100 / len(scorecards):.1f}%)")

    print(f"\nWrote: {SCORECARD_OUT}")
    print(f"Wrote: {FLAGS_OUT}")


if __name__ == "__main__":
    main()
