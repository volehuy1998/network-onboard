#!/usr/bin/env python3
"""J.1 Step 1: Parse REF (doc/ovs-openflow-ovn-keyword-reference.md) into structured inventory.

Output: memory/keyword-inventory.md flat list with schema:
  { name, ref_section, bucket, status (placeholder), source_url }

Entry patterns identified in REF:
  Pattern A: `- **<name>** — Bucket: <bucket> | ...`        (OVS + OVN sections)
  Pattern B: `**<name>**` standalone heading                 (OpenFlow section 2.x)
  Pattern C: `#### <name>`                                   (CLI tool subsections in 1.4)
  Pattern D: `### <N>. <scenario>`                           (Section 4 troubleshoot)
"""

from __future__ import annotations
import re
from pathlib import Path

REPO = Path(r"C:\Users\voleh\Documents\network-onboard")
REF = REPO / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
OUT = REPO / "memory" / "keyword-inventory.md"

# BANNED keyword detection (DPDK/PMD/SMC/EMC/mempool family)
BAN_PATTERNS = [
    r"\bDPDK\b", r"\bPMD\b", r"\bMicroflow.*EMC\b", r"\bEMC\b.*Cache",
    r"\bSMC\b", r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd",
    r"hugepage", r"NUMA tuning",
]

def is_banned(name: str, context: str) -> bool:
    """Return True if entry is in PERMANENT BAN list (DPDK/PMD/SMC/EMC/mempool)."""
    text = (name + " " + context).lower()
    if any(re.search(pat, text, re.IGNORECASE) for pat in [
        r"\bdpdk\b", r"\bpmd\b", r"\bemc\b", r"\bsmc\b",
        r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd",
        r"\bhugepage\b",
    ]):
        return True
    return False


def detect_section(line: str, current: dict) -> dict:
    """Track which section/subsection we're in."""
    # Top-level: ## 1. Open vSwitch (OVS)
    m = re.match(r"^## (\d)\. (.+)$", line)
    if m:
        current["section"] = m.group(1)
        current["section_name"] = m.group(2).strip()
        current["subsection"] = ""
        current["subsection_name"] = ""
        return current
    # Subsection: ### 1.1 Architecture & daemons
    m = re.match(r"^### (\d)\.(\d) (.+)$", line)
    if m:
        current["subsection"] = f"{m.group(1)}.{m.group(2)}"
        current["subsection_name"] = m.group(3).strip()
        return current
    return current


def detect_entry(line: str, next_line: str = "") -> tuple[str, str] | None:
    """Detect entry name + brief context from a line.

    Returns (name, context) or None if not an entry line.
    """
    # Pattern A: `- **<name>** — <context>` or `- **<name>** ...`
    m = re.match(r"^- \*\*([^*]+)\*\*\s*[—\-–|]?\s*(.*)$", line)
    if m:
        name = m.group(1).strip()
        context = m.group(2).strip()
        # Skip if name is empty or just punctuation
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, context)
    # Pattern B: `**<name>**` standalone (OpenFlow section)
    m = re.match(r"^\*\*([^*]+)\*\*$", line)
    if m:
        name = m.group(1).strip()
        # Combine with next line context if available
        context = next_line.strip() if next_line else ""
        # Filter out non-keyword bold (like **Problem.** or **Layered checklist.**)
        if name in ("Problem.", "Layered checklist.", "Likely root-cause categories.",
                    "Note.", "Warning.", "Source:", "Example:", "Synopsis:"):
            return None
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, context)
    return None


def detect_subsection_heading(line: str) -> tuple[str, str] | None:
    """Detect Pattern C: `#### <name>` (CLI tool subsections)."""
    m = re.match(r"^#### `?([^`]+)`?$", line)
    if m:
        name = m.group(1).strip().rstrip("`")
        return (name, "CLI tool")
    return None


def detect_scenario(line: str) -> tuple[str, str] | None:
    """Detect Pattern D: `### N. <scenario>` (Section 4 troubleshoot)."""
    m = re.match(r"^### (\d+)\. (.+)$", line)
    if m:
        return (f"Scenario {m.group(1)}: {m.group(2).strip()}", "production troubleshoot")
    return None


def extract_source_url(text: str) -> str:
    """Pull authoritative URL from entry context if present."""
    m = re.search(r"https?://[^\s\)]+", text)
    return m.group(0).rstrip(".,;)") if m else ""


def main():
    if not REF.exists():
        print(f"ERROR: REF not found at {REF}")
        return

    lines = REF.read_text(encoding="utf-8").splitlines()
    entries = []
    state = {"section": "", "section_name": "", "subsection": "", "subsection_name": ""}

    for i, line in enumerate(lines):
        state = detect_section(line, state)

        # Try each pattern
        next_line = lines[i+1] if i+1 < len(lines) else ""

        entry = detect_entry(line, next_line)
        if not entry:
            entry = detect_subsection_heading(line)
        if not entry:
            entry = detect_scenario(line)

        if not entry:
            continue

        name, context = entry
        # Look ahead a few lines for source URL
        url_search = " ".join(lines[i:min(i+5, len(lines))])
        url = extract_source_url(url_search)

        # Detect bucket from context
        bucket_match = re.search(r"Bucket[:\s|]+(\w+)", context)
        bucket = bucket_match.group(1) if bucket_match else state.get("section_name", "")

        banned = is_banned(name, context)

        entries.append({
            "name": name,
            "section": state.get("section", ""),
            "subsection": state.get("subsection", ""),
            "subsection_name": state.get("subsection_name", ""),
            "bucket": bucket,
            "context_brief": context[:120] + ("..." if len(context) > 120 else ""),
            "source_url": url,
            "ref_line": i + 1,
            "banned": banned,
        })

    # Dedup by name (keep first occurrence)
    seen = set()
    unique_entries = []
    for e in entries:
        key = (e["name"], e["section"])
        if key in seen:
            continue
        seen.add(key)
        unique_entries.append(e)

    # Group by section for output
    OUT.parent.mkdir(parents=True, exist_ok=True)

    out = []
    out.append("# Keyword Inventory (J.1 output)")
    out.append("")
    out.append(f"> **Source:** parsed from `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`")
    out.append(f"> **Total entries:** {len(unique_entries)}")
    out.append(f"> **Banned (DPDK/PMD/SMC/EMC/mempool):** {sum(1 for e in unique_entries if e['banned'])}")
    out.append(f"> **In-scope:** {sum(1 for e in unique_entries if not e['banned'])}")
    out.append(f"> **Generated by:** scripts/parse_ref_inventory.py")
    out.append("")
    out.append("## Schema")
    out.append("")
    out.append("Each entry: `name | section | subsection | bucket | banned | source URL | REF line`")
    out.append("")
    out.append("---")
    out.append("")

    # Group by section.subsection
    from collections import defaultdict
    grouped = defaultdict(list)
    for e in unique_entries:
        key = f"{e['section']}.{e['subsection']}" if e['subsection'] else e['section']
        grouped[key].append(e)

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
        out.append("| # | Keyword | Bucket | Banned | Source URL | REF line |")
        out.append("|---|---------|--------|--------|------------|----------|")
        for idx, e in enumerate(sec_entries, 1):
            ban = "BAN" if e["banned"] else ""
            url = e["source_url"][:50] + "..." if len(e["source_url"]) > 50 else e["source_url"]
            name_safe = e["name"].replace("|", "\\|")
            bucket_safe = e["bucket"].replace("|", "\\|")
            out.append(f"| {idx} | `{name_safe}` | {bucket_safe} | {ban} | {url} | {e['ref_line']} |")
        out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Total entries: {len(unique_entries)}")
    print(f"Banned: {sum(1 for e in unique_entries if e['banned'])}")
    print(f"In-scope: {sum(1 for e in unique_entries if not e['banned'])}")


if __name__ == "__main__":
    main()
