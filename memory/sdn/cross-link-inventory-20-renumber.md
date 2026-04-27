# Cross-Link Inventory Pre-Renumber 20.x (Plan v3.9 Phase S4.1)

> **Generated:** 2026-04-27
> **Purpose:** Document all `Phần 20.X` cross-block references before renumbering
> 20.0 + 20.1 file headings (per Plan v3.9 Phase S4 Section S4.3).
> **Plan:** [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md)
> Phase S4.

---

## 1. Aggregate

- Total `Phần 20.\d+` references cross-block: **121 hits across 37 files**
- Source command: `grep -rn "Phần 20\." sdn-onboard/`

## 2. Reference categorization

### 2.1. Category CLEAR (file reference, no rename needed)

References từ ngoài files 20.0/20.1 trỏ đến **sibling files** (e.g., 20.2, 20.3, ..., 20.7, 20.8). Sibling file
exists as standalone curriculum file:
- `20.0 - ovs-ovn-systematic-debugging.md` (renamed internal headings to 20.0.N)
- `20.1 - ovs-ovn-security-hardening.md` (renamed internal headings to 20.1.N)
- `20.2 - ovn-troubleshooting-deep-dive.md`
- `20.3 - ovn-daily-operator-playbook.md`
- `20.4 - ovs-daily-operator-playbook.md`
- `20.5 - ovn-forensic-case-studies.md`
- `20.6 - ovs-openflow-ovn-retrospective-2007-2024.md`
- `20.7 - packet-flow-tracing-tutorial-gradient.md`
- `20.8 - ovn-troubleshoot-keyword-reverse-index.md`

Reference like `Phần 20.7` từ ngoài 20.0 (e.g., `0.2 - end-to-end-packet-journey.md:215`)
referring to file 20.7 packet-flow-tracing — **keep unchanged**.

Estimated count: ~110/121.

### 2.2. Category INTERNAL (heading reference inside same file, needs rename)

References trong 20.0 trỏ đến 20.0's own headings:

| File:line | Reference | Replacement |
|-----------|-----------|-------------|
| 20.0:554 | `Phần 20.5 liệt kê 8 kịch bản` | `Phần 20.0.5 liệt kê 8 kịch bản` |
| 20.0:554 | `Phần 20.7 playback 3 incident` | `Phần 20.0.7 playback 3 incident` |

References trong 20.1 trỏ đến 20.1's own headings:

| File:line | Reference | Replacement |
|-----------|-----------|-------------|
| 20.1:470 | `Phần 20.10 giới thiệu ACL logging` | `Phần 20.1.10 giới thiệu ACL logging` |
| 20.1:638 | `Phần 20.13 là investigation playbook` | `Phần 20.1.13 là investigation playbook` |
| 20.1:751 | `Phần 20.14 đi sâu schema RBAC_Role` | `Phần 20.1.14 đi sâu schema RBAC_Role` |

Estimated count: 5/121.

### 2.3. Category FILE-METADATA (self-reference in header block, no rename)

Lines saying `**Phần:** Phần 20.1` (file metadata field).

| File:line | Context |
|-----------|---------|
| 20.1:5 | `> **Phần:** Phần 20.1` (header block self-id) |
| 20.1:46 | `Phần 20.1 này tập trung toàn bộ vào lớp 3` (file self-reference) |
| 20.1:1085 | `**Chuẩn bị:** Phần 20.1 setup với ACL logging bật` (file self-reference) |

Estimated count: 3/121.

### 2.4. Category EXTERNAL-NESTED (refers to nested heading in sibling file)

References like `Phần 20.2 §20.2.6` — refers to specific sub-section inside sibling file 20.2.
The sibling file 20.2 has its own §20.2.X headings (independent namespace, not affected by 20.0/20.1 renumber).

| File:line | Reference |
|-----------|-----------|
| 20.1:542 | `Phần 20.2 §20.2.6 status check` |
| 20.1:1321 | `Phần 20.3 §20.3.10 + Phần 20.4 §20.4.10 daily audit script` |

These remain unchanged because file 20.2/20.3/20.4 are sibling files with their own namespace.

Estimated count: ~3/121.

### 2.5. Anchor link `#20-X-Y` references

Grep `#20-[0-9]` cross-block: **0 hits** found. No anchor links to update.

## 3. Renumber plan

### 3.1. Inside 20.0 file (heading rename)

| Current | New |
|---------|-----|
| `## 20.1 Triết lý chẩn đoán` | `## 20.0.1 Triết lý chẩn đoán` |
| `## 20.2 Mô hình 5 lớp kiểm tra` | `## 20.0.2 Mô hình 5 lớp kiểm tra` |
| `## 20.3 Công cụ chẩn đoán OVS` | `## 20.0.3 Công cụ chẩn đoán OVS` |
| `## 20.4 Công cụ chẩn đoán OVN` | `## 20.0.4 Công cụ chẩn đoán OVN` |
| `## 20.5 Tám kịch bản lỗi phổ biến` | `## 20.0.5 Tám kịch bản lỗi phổ biến` |
| `## 20.6 Guided Exercise` | `## 20.0.6 Guided Exercise` |
| `## 20.7 Case study playback` | `## 20.0.7 Case study playback` |
| `### 20.5.1` to `### 20.5.8` (8 sub) | `### 20.0.5.1` to `### 20.0.5.8` |
| `## 20.X Anatomy Template A` | unchanged (literal X, not numeric) |
| `## 20.0.X Backfill v3.5` | unchanged (already 20.0 prefix) |

### 3.2. Inside 20.1 file (heading rename)

| Current | New |
|---------|-----|
| `## 20.7 Ba lớp bảo mật` | `## 20.1.7 Ba lớp bảo mật` |
| `## 20.8 port_security` | `## 20.1.8 port_security` |
| `## 20.9 ACL default-deny` | `## 20.1.9 ACL default-deny` |
| `## 20.10 ACL audit logging` | `## 20.1.10 ACL audit logging` |
| `## 20.11 10-point security posture checklist` | `## 20.1.11 10-point security posture checklist` |
| `## 20.12 Audit trail architecture` | `## 20.1.12 Audit trail architecture` |
| `## 20.13 Port_security forensic` | `## 20.1.13 Port_security forensic` |
| `## 20.14 RBAC OVSDB deep-dive` | `## 20.1.14 RBAC OVSDB deep-dive` |
| `## 20.15 mTLS + certificate rotation` | `## 20.1.15 mTLS + certificate rotation` |
| `## 20.16 Security incident response` | `## 20.1.16 Security incident response` |

Plus all `### 20.X.Y` sub-headings inside 20.1 → `### 20.1.X.Y` (estimated ~30 sub-headings).

### 3.3. Internal reference updates

20.0 line 554: 2 internal refs to renumber.
20.1 lines 470, 638, 751: 3 internal refs to renumber.

## 4. Verification post-renumber

After renumber:
1. Re-grep `Phần 20\.\d+` cross-block → spot-check 10 sample references resolvable
2. In-file Mục lục (table of contents) of 20.0/20.1: check if exists + update
3. Markdown link `[text](20.X)` integrity: spot-check 5 links

## 5. References

- Plan: [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md) Phase S4
- Master audit Agent E §3 + §11.1 (Rule 6 §B violation finding)
- Rule 6 §B Cross-File Sync (CLAUDE.md)
- Rule 2 (CLAUDE.md memory file dependency)
