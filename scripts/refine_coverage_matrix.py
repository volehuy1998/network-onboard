#!/usr/bin/env python3
"""J.1 Step 2b: Refine coverage matrix with alternative-name grep.

REF uses descriptive entry names like:
  - "Connection tracking (ct)"
  - "UFID (Unique Flow ID)"
  - "Interface type: internal"
  - "VLAN bridge modes (Port.vlan_mode)"

Plain grep on the full descriptive name returns 0 hits even when the
core concept (ct, UFID, vlan_mode) is well-covered. This second-pass
extracts short-name candidates and re-greps.

Output: memory/keyword-coverage-matrix.md (overwrite with refined data)
"""

from __future__ import annotations
import re
import subprocess
from pathlib import Path
from collections import defaultdict

REPO = Path(r"C:\Users\voleh\Documents\network-onboard")
REF = REPO / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
CURRICULUM_DIR = REPO / "sdn-onboard"
OUT = REPO / "memory" / "keyword-coverage-matrix.md"


# Reuse parser
def is_banned(name: str, context: str) -> bool:
    text = (name + " " + context).lower()
    return any(re.search(pat, text, re.IGNORECASE) for pat in [
        r"\bdpdk\b", r"\bpmd\b", r"\bemc\b", r"\bsmc\b",
        r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd",
        r"\bhugepage\b",
    ])


def detect_section(line, current):
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


def detect_entry(line, next_line=""):
    m = re.match(r"^- \*\*([^*]+)\*\*\s*[—\-–|]?\s*(.*)$", line)
    if m:
        name = m.group(1).strip()
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, m.group(2).strip())
    m = re.match(r"^\*\*([^*]+)\*\*$", line)
    if m:
        name = m.group(1).strip()
        if name in ("Problem.", "Layered checklist.", "Likely root-cause categories.",
                    "Note.", "Warning.", "Source:", "Example:", "Synopsis:"):
            return None
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, next_line.strip())
    return None


def detect_subsection_heading(line):
    m = re.match(r"^#### `?([^`]+)`?$", line)
    if m:
        return (m.group(1).strip().rstrip("`"), "CLI tool")
    return None


def detect_scenario(line):
    m = re.match(r"^### (\d+)\. (.+)$", line)
    if m:
        return (f"Scenario {m.group(1)}: {m.group(2).strip()}", "production troubleshoot")
    return None


def parse_ref():
    lines = REF.read_text(encoding="utf-8").splitlines()
    entries = []
    state = {"section": "", "section_name": "", "subsection": "", "subsection_name": ""}
    for i, line in enumerate(lines):
        state = detect_section(line, state)
        next_line = lines[i+1] if i+1 < len(lines) else ""
        entry = detect_entry(line, next_line) or detect_subsection_heading(line) or detect_scenario(line)
        if not entry:
            continue
        name, context = entry
        bucket_match = re.search(r"Bucket[:\s|]+(\w+)", context)
        bucket = bucket_match.group(1) if bucket_match else state.get("section_name", "")
        entries.append({
            "name": name,
            "section": state.get("section", ""),
            "subsection": state.get("subsection", ""),
            "subsection_name": state.get("subsection_name", ""),
            "bucket": bucket,
            "banned": is_banned(name, context),
            "ref_line": i + 1,
        })
    seen = set()
    unique = []
    for e in entries:
        key = (e["name"], e["section"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


def extract_short_names(name: str) -> list[str]:
    """Extract candidate short names from a descriptive REF entry name.

    Examples:
      "Connection tracking (ct)" → ["Connection tracking", "ct"]
      "UFID (Unique Flow ID)" → ["UFID"]
      "Interface type: internal" → ["Interface type: internal", "internal"]
      "VLAN bridge modes (Port.vlan_mode)" → ["VLAN bridge modes", "vlan_mode", "Port.vlan_mode"]
      "openvswitch.ko (kernel datapath)" → ["openvswitch.ko"]
    """
    candidates = [name]

    # Pattern: "Foo (bar)" → also try "bar" if bar looks like identifier
    m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", name)
    if m:
        main = m.group(1).strip().rstrip("`").lstrip("`")
        paren = m.group(2).strip().strip("`")  # strip surrounding backticks
        if main and main not in candidates:
            candidates.append(main)
        # Paren content - if it looks like identifier (has _, ., -, /, or is short uppercase)
        if paren:
            # Strip any inline backticks too
            paren_clean = paren.replace("`", "").strip()
            if re.match(r"^[\w./_-]+$", paren_clean) and len(paren_clean) <= 40:
                candidates.append(paren_clean)
                # Also try rightmost segment after dot (vlan_mode from Port.vlan_mode)
                if "." in paren_clean:
                    candidates.append(paren_clean.rsplit(".", 1)[1])
                # Slash split (sctp_src/sctp_dst → sctp_src + sctp_dst)
                if "/" in paren_clean:
                    for part in paren_clean.split("/"):
                        if part.strip():
                            candidates.append(part.strip())
            # Multi-word in parens (e.g., "kernel datapath") - skip, not specific identifier

    # Pattern: "Foo: bar" → also try "bar" (e.g., "Interface type: internal")
    m = re.match(r"^(.+?):\s*(.+)$", name)
    if m:
        right = m.group(2).strip()
        if right and len(right) <= 30 and right not in candidates:
            candidates.append(right)

    # Strip trailing modifiers like "(8 bits, OF 1.2+)" common in match field entries
    m = re.match(r"^([\w._-]+(?:\s*/\s*[\w._-]+)*)\s+\(\d+\s*bits", name)
    if m:
        core = m.group(1).strip()
        if core and core not in candidates:
            candidates.append(core)
        # Split "tcp_src / tcp_dst" → ["tcp_src", "tcp_dst"] regardless of whether core was already in candidates
        if core and "/" in core:
            for part in core.split("/"):
                if part.strip() and part.strip() not in candidates:
                    candidates.append(part.strip())

    # Backtick: `ovs-vsctl` → ovs-vsctl
    m = re.match(r"^`([^`]+)`$", name)
    if m:
        bt = m.group(1).strip()
        if bt not in candidates:
            candidates.append(bt)

    # Filter aliases:
    # 1. Skip empty/whitespace
    # 2. Skip 2-char or shorter aliases (avoid "ct" matching "act", "fact"; "of" matching "of")
    # 3. Skip generic English words that aren't OVN/OVS-specific identifiers
    # Exception: keep multi-part (has _, ., /, digit, or contains uppercase letter)
    GENERIC_BLACKLIST = {
        "of", "it", "is", "as", "at", "to", "in", "on", "or", "no",
        "ct",  # too short, matches "act", "fact", etc.; ct_state/ct_zone are specific
    }
    filtered = []
    for c in candidates:
        cs = c.strip()
        if not cs:
            continue
        if cs.lower() in GENERIC_BLACKLIST:
            continue
        if len(cs) < 3:
            # Allow short if it has uppercase or digit (likely identifier like "OF", "L2")
            if not any(ch.isupper() or ch.isdigit() for ch in cs):
                continue
        filtered.append(cs)
    return filtered if filtered else [name]


def grep_keyword(keyword: str, files: list[Path]) -> tuple[int, list[str]]:
    """Grep keyword as fixed string across given files."""
    matched = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if keyword in content:
                matched.append(f.name)
        except Exception:
            continue
    return len(matched), matched


def grep_keyword_with_alternatives(name: str, files: list[Path]) -> tuple[int, list[str], str]:
    """Grep with alternatives, return best (most-files) result.

    Returns (file_count, file_list, matched_alias_used).
    """
    candidates = extract_short_names(name)
    best_count = 0
    best_files = []
    best_alias = candidates[0] if candidates else name

    for cand in candidates:
        count, files_matched = grep_keyword(cand, files)
        if count > best_count:
            best_count = count
            best_files = files_matched
            best_alias = cand
    return best_count, best_files, best_alias


def classify_depth(file_count: int) -> str:
    if file_count == 0:
        return "MISSING"
    if file_count <= 2:
        return "SHALLOW"
    if file_count <= 9:
        return "BREADTH"
    return "WIDE"


def classify_tier(entry: dict, depth: str) -> str:
    if entry["banned"]:
        return "D"
    return {"MISSING": "A", "SHALLOW": "B", "BREADTH": "C-OK", "WIDE": "C-DEEP"}[depth]


def main():
    print("Parsing REF...")
    entries = parse_ref()
    print(f"  Total: {len(entries)}, In-scope: {sum(1 for e in entries if not e['banned'])}")

    print("Grepping curriculum (with alternative-name fallback)...")
    files = sorted(CURRICULUM_DIR.glob("*.md"))
    print(f"  Curriculum file count: {len(files)}")

    matrix = []
    for i, e in enumerate(entries):
        count, matched, alias = grep_keyword_with_alternatives(e["name"], files)
        depth = classify_depth(count)
        tier = classify_tier(e, depth)
        matrix.append({
            **e,
            "file_count": count,
            "files": matched,
            "depth": depth,
            "tier": tier,
            "matched_via": alias,
        })
        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(entries)}")

    stats = defaultdict(int)
    for m in matrix:
        stats[m["tier"]] += 1
    print(f"  Tier A (MISSING in-scope): {stats['A']}")
    print(f"  Tier B (SHALLOW in-scope): {stats['B']}")
    print(f"  Tier C-OK (BREADTH 3-9 files): {stats['C-OK']}")
    print(f"  Tier C-DEEP (WIDE 10+ files): {stats['C-DEEP']}")
    print(f"  Tier D (BANNED): {stats['D']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = []
    out.append("# Keyword Coverage Matrix (J.1 output, refined)")
    out.append("")
    out.append(f"> **Source:** parsed from `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`")
    out.append(f"> **Curriculum scope:** `sdn-onboard/*.md` (top-level only, {len(files)} files)")
    out.append(f"> **Generated by:** scripts/refine_coverage_matrix.py")
    out.append("")
    out.append("## Refinement note")
    out.append("")
    out.append("REF entries use descriptive names like `Connection tracking (ct)` or `Interface type: internal`.")
    out.append("First-pass grep on full descriptive name returned high false-positive MISSING.")
    out.append("This refined matrix tries alternative aliases:")
    out.append("- Parenthetical content extracted as alias if looks like identifier (`ct` from `Connection tracking (ct)`)")
    out.append("- Colon-suffix extracted (`internal` from `Interface type: internal`)")
    out.append("- Slash-separated split (`tcp_src` + `tcp_dst` from `tcp_src / tcp_dst`)")
    out.append("- Backtick-stripped")
    out.append("Best (most-files) match wins. `matched_via` column shows which alias matched.")
    out.append("")
    out.append("## Depth classification")
    out.append("")
    out.append("- **MISSING** = 0 file mentions (no alias matched)")
    out.append("- **SHALLOW** = 1-2 files (likely passing mention, no Anatomy)")
    out.append("- **BREADTH** = 3-9 files (covered but spread thin; verify 5-axis exists)")
    out.append("- **WIDE** = 10+ files (central concept; very likely has DEEP treatment)")
    out.append("")
    out.append("## Tier classification (priority for v3.5 work)")
    out.append("")
    out.append("- **Tier A** (MISSING in-scope): TOP priority, build 5-axis from scratch")
    out.append("- **Tier B** (SHALLOW in-scope): MUST upgrade to 5-axis Anatomy")
    out.append("- **Tier C-OK** (BREADTH 3-9): verify 5-axis exists somewhere; add Anatomy if missing")
    out.append("- **Tier C-DEEP** (WIDE 10+): likely has 5-axis; spot-check during J.7")
    out.append("- **Tier D** (BANNED): skip per PERMANENT BAN directive")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append("| Tier | Count | % | Action |")
    out.append("|------|-------|---|--------|")
    total_inscope = sum(1 for m in matrix if not m["banned"])
    for t, _label in [("A", "MISSING in-scope"), ("B", "SHALLOW in-scope"),
                      ("C-OK", "BREADTH"), ("C-DEEP", "WIDE"), ("D", "BANNED")]:
        c = stats[t]
        if t == "D":
            pct = f"{c * 100 / len(matrix):.1f}%"
        else:
            pct = f"{c * 100 / total_inscope:.1f}%" if total_inscope else "N/A"
        action = {
            "A": "Build 5-axis from scratch (J.3-J.5)",
            "B": "Upgrade existing to 5-axis (J.3-J.5)",
            "C-OK": "Verify 5-axis; add if missing",
            "C-DEEP": "Spot-check J.7",
            "D": "Skip (PERMANENT BAN)",
        }[t]
        out.append(f"| {t} | {c} | {pct} | {action} |")
    out.append("")
    out.append(f"**Total in-scope:** {total_inscope}")
    out.append(f"**Build/upgrade work (Tier A + B):** {stats['A'] + stats['B']} keyword")
    out.append("")
    out.append("---")
    out.append("")

    grouped = defaultdict(list)
    for m in matrix:
        key = f"{m['section']}.{m['subsection']}" if m['subsection'] else m['section']
        grouped[key].append(m)

    for sec_key in sorted(grouped.keys()):
        sec_entries = grouped[sec_key]
        if not sec_entries:
            continue
        first = sec_entries[0]
        title = f"REF Section {sec_key}"
        if first.get("subsection_name"):
            title += f" — {first['subsection_name']}"
        out.append(f"## {title} ({len(sec_entries)} entries)")
        out.append("")
        sub_stats = defaultdict(int)
        for e in sec_entries:
            sub_stats[e["tier"]] += 1
        out.append(f"_Tier breakdown: A={sub_stats['A']}, B={sub_stats['B']}, "
                   f"C-OK={sub_stats['C-OK']}, C-DEEP={sub_stats['C-DEEP']}, D={sub_stats['D']}_")
        out.append("")
        out.append("| Keyword | Files | Depth | Tier | Matched via | First 3 files |")
        out.append("|---------|-------|-------|------|-------------|---------------|")
        for e in sec_entries:
            name_safe = e["name"].replace("|", "\\|").replace("`", "")
            via_safe = e["matched_via"].replace("|", "\\|").replace("`", "")
            files_brief = ", ".join(e["files"][:3])
            if len(e["files"]) > 3:
                files_brief += f", ... (+{len(e['files']) - 3})"
            via_show = via_safe if via_safe != name_safe else "(direct)"
            out.append(f"| `{name_safe}` | {e['file_count']} | {e['depth']} | {e['tier']} | {via_show} | {files_brief} |")
        out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
