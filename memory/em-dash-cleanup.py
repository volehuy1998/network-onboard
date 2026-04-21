#!/usr/bin/env python3
"""
Em-dash cleanup cho session 9 skeleton files.
User feedback: dùng từ ngữ uyển chuyển thay vì em-dash "—".

Apply conservative replacements only. Leaves ambiguous cases for manual review.
"""
import re
import sys
from pathlib import Path

# Files to process (session 9 skeleton files + README + plan)
FILES = [
    # Block XIII expansion (P1)
    "sdn-onboard/13.4 - br-int-architecture-and-patch-ports.md",
    "sdn-onboard/13.5 - port-binding-types-ovn-native.md",
    "sdn-onboard/13.6 - ha-chassis-group-and-bfd.md",
    # Block IX expansion (P2)
    "sdn-onboard/9.6 - bonding-and-lacp.md",
    "sdn-onboard/9.7 - port-mirroring-and-packet-capture.md",
    "sdn-onboard/9.8 - flow-monitoring-sflow-netflow-ipfix.md",
    "sdn-onboard/9.9 - qos-policing-shaping-metering.md",
    "sdn-onboard/9.10 - tls-pki-hardening.md",
    "sdn-onboard/9.11 - ovs-appctl-reference-playbook.md",
    "sdn-onboard/9.12 - upgrade-and-rolling-restart.md",
    "sdn-onboard/9.13 - libvirt-docker-integration.md",
    "sdn-onboard/9.14 - incident-response-decision-tree.md",
    # Cross-Block (P3)
    "sdn-onboard/4.7 - openflow-programming-with-ovs.md",
    "sdn-onboard/10.2 - ovsdb-backup-restore-compact-rbac.md",
    "sdn-onboard/11.3 - gre-tunnel-lab.md",
    "sdn-onboard/11.4 - ipsec-tunnel-lab.md",
    # Refinement (P4a+P4b)
    "sdn-onboard/5.0 - sdn-via-apis-netconf-yang.md",
    "sdn-onboard/5.1 - hypervisor-overlays-nvp-nsx.md",
    "sdn-onboard/5.2 - opening-device-whitebox.md",
    "sdn-onboard/6.0 - p4-programmable-data-plane.md",
    "sdn-onboard/6.1 - flow-objectives-abstraction.md",
    "sdn-onboard/7.0 - nox-pox-ryu-faucet.md",
    "sdn-onboard/7.1 - opendaylight-architecture.md",
    "sdn-onboard/7.2 - onos-service-provider-scale.md",
    "sdn-onboard/7.3 - vendor-controllers-aci-contrail.md",
    "sdn-onboard/8.0 - linux-namespaces-cgroups.md",
    "sdn-onboard/8.1 - linux-bridge-veth-macvlan.md",
    "sdn-onboard/8.2 - linux-vlan-bonding-team.md",
    "sdn-onboard/8.3 - tc-qdisc-and-conntrack.md",
    "sdn-onboard/12.0 - dc-network-topologies-clos-leaf-spine.md",
    "sdn-onboard/12.1 - dc-overlay-integration-vxlan-evpn.md",
    "sdn-onboard/12.2 - micro-segmentation-service-chaining.md",
]

# Regex patterns, applied in order
PATTERNS = [
    # --- File/section headers: "# X.Y — Title" → "# X.Y. Title"
    (re.compile(r'^(# \d+\.\d+) — '), r'\1. '),
    # --- Metadata: "> **Trạng thái:** Skeleton (architecture phase — Rule 10)." → "(architecture phase, Rule 10)"
    (re.compile(r'\(architecture phase — Rule 10\)'), r'(architecture phase theo Rule 10)'),
    # --- Metadata: "> **Khối:** YYY — description" → "**Khối:** YYY, description"
    (re.compile(r'(\*\*Khối:\*\*[^\n]+?) — ([^\n]+)'), r'\1, \2'),
    # --- "*Placeholder — Phase B" → "*Placeholder cho Phase B"
    (re.compile(r'\*Placeholder — '), r'*Placeholder cho '),
    (re.compile(r'Placeholder — Phase B'), r'Placeholder cho Phase B'),
    # --- Inline parenthetical "(X — Y)" → "(X, Y)"
    (re.compile(r'\(([^)\n]{1,80}?) — ([^)\n]{1,80}?)\)'), r'(\1, \2)'),
    # --- "Lab — description" (end of line): ", description"
    # Not easy to match, skip
    # --- "X — nhưng Y" → "X nhưng Y"
    (re.compile(r' — (nhưng|tuy nhiên|trong khi) '), r' \1 '),
    # --- "X — vì Y" → "X vì Y"
    (re.compile(r' — (vì|do|bởi vì) '), r' \1 '),
    # --- "X — với Y" → "X với Y"
    (re.compile(r' — với '), r' với '),
    # --- "X — và Y" → "X và Y"
    (re.compile(r' — và '), r' và '),
    # --- "X — cần Y" → "X, cần Y"
    (re.compile(r' — cần '), r', cần '),
    # --- "X — nên Y" → "X, nên Y"
    (re.compile(r' — nên '), r', nên '),
    # --- "X — là Y" → "X, là Y" (appositive with explicit copula)
    (re.compile(r' — là '), r', là '),
    # --- "X — KHÔNG Y" or "X — TUYỆT ĐỐI Y" emphasis → "X. KHÔNG Y"
    (re.compile(r' — (KHÔNG|TUYỆT ĐỐI|DANGER|WARNING|CHÚ Ý)'), r'. \1'),
    # --- "X — (eg lowercase fragment)" default case → "X, ..."
    (re.compile(r' — ([a-zà-ỹ])'), r', \1'),
    # --- "X — (Capitalized fragment, likely new sentence)" → "X. Fragment"
    (re.compile(r' — ([A-ZÀ-Ỹ])'), r'. \1'),
    # --- "X — `code`" → "X, `code`"  (safer to use comma)
    (re.compile(r' — (`[^`]+`)'), r', \1'),
    # --- "X — *italic*" → "X, *italic*"
    (re.compile(r' — (\*[^*]+\*)'), r', \1'),
    # --- "X — [link]" → "X, [link]"
    (re.compile(r' — (\[)'), r', \1'),
    # --- "X — \"quoted\"" → "X. \"quoted\""
    (re.compile(r' — (")'), r', \1'),
    # --- Leftover double space cleanup
    (re.compile(r'  +'), ' '),
    # --- Cleanup: ". . " → ". "
    (re.compile(r'\. \. '), r'. '),
]

def clean(text):
    for pat, repl in PATTERNS:
        text = pat.sub(repl, text)
    return text

def main():
    root = Path("C:/Users/voleh/Documents/network-onboard")
    total_before = 0
    total_after = 0
    changed = 0
    for rel in FILES:
        p = root / rel
        if not p.exists():
            print(f"MISSING: {rel}")
            continue
        before = p.read_text(encoding='utf-8')
        before_count = before.count('—')
        after = clean(before)
        after_count = after.count('—')
        if before_count != after_count:
            p.write_text(after, encoding='utf-8')
            changed += 1
        total_before += before_count
        total_after += after_count
        print(f"{before_count:3d} -> {after_count:3d}  {rel}")
    print()
    print(f"Total em-dash: {total_before} -> {total_after} (reduced {total_before-total_after})")
    print(f"Files changed: {changed}/{len(FILES)}")

if __name__ == '__main__':
    main()
