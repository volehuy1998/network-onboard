# Rubric Leak Baseline 2026-04-27 (Plan v3.9 Phase S0)

> **Generated:** 2026-04-27 by `python scripts/rubric_leak_check.py --all --report`
> **Hook version:** rubric_leak_check.py v2 (20 patterns total = 13 v1 + 7 v2)
> **Purpose:** Establish baseline state pre-Phase-S2/S3/S6 phrase scrub. Compare delta after subsequent phases close.
> **Plan:** [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md) Phase S0
> **Governance:** GP-11 / CLAUDE.md Rule 16

---

## 1. Aggregate

| Metric | Value |
|--------|------:|
| Total curriculum file scanned | 167 |
| Total violation | 108 |
| File with at least 1 violation | 16 |
| File with zero violation | 151 |

---

## 2. Per-pattern breakdown

| Pattern name | Hit count | V1/V2 | Severity |
|--------------|----------:|-------|----------|
| `axis-numbered-vn-heading` | 75 | V2 | FAIL |
| `tier-cornerstone-informal` | 24 | V2 | FAIL |
| `phase-session-reference` | 7 | V2 | FAIL |
| `cohort-cornerstone-phrase` | 1 | V2 | FAIL |
| `cohort-batch-stamp-leftover` | 1 | V2 | FAIL |
| `tier-importance-bold-label` | 0 | V2 | FAIL |
| `stale-phase-compat-note` | 0 | V2 | FAIL |
| `axis-bold-label` | 0 | V1 | FAIL |
| `cohort-label` | 0 | V1 | FAIL |
| `phase-plan-reference` | 0 | V1 | FAIL |
| `tier-label-deep` | 0 | V1 | FAIL |
| `tier-label-partial` | 0 | V1 | FAIL |
| `rubric-meta-term` | 0 | V1 | FAIL |
| `anti-gaming-meta` | 0 | V1 | FAIL |
| `governance-principle-reference` | 0 | V1 | FAIL |
| (other v1 patterns) | 0 | V1 | FAIL |

**Observation:** All 108 leaks captured by V2 patterns (V1 patterns clean). Confirms V3.8 Phase R0.7 cleanup successfully eliminated V1-detectable leaks. The 108 baseline reveals **V2 blind spots** that R0.7 missed.

**Top contributing patterns (98% of leaks):**
1. `axis-numbered-vn-heading` (75 = 69% of total) — heavy in 13.18, 13.19, 9.32, 3.5
2. `tier-cornerstone-informal` (24 = 22%) — distributed across 11 file
3. `phase-session-reference` (7 = 6%) — `Phase H session` in 5+ file `**Trạng thái:**` headers

---

## 3. Scope split: OVS (v3.9 fix) vs non-OVS (v3.10+ defer)

### 3.1. OVS scope (Plan v3.9 Phase S2/S3/S6 fix targets)

**Subtotal:** 35 violations across 7 file (32% of total).

| Rank | Lines | File | Phase fix |
|---:|---:|------|-----------|
| 1 | 25 | `sdn-onboard/9.32 - ovs-classifier-internals-deep.md` | **S3** (cleanup §9.32.1+§9.32.2 axis-numbered + line 526 cohort-batch) |
| 2 | 4 | `sdn-onboard/9.2 - ovs-kernel-datapath-megaflow.md` | **S2** commit 1 (cohort-cornerstone heading + Tier 1 phrasing) |
| 3 | 2 | `sdn-onboard/9.1 - ovs-3-component-architecture.md` | **S2** commit 1 OR new (line 337 + 623 `cornerstone tier 1 tuyệt đối`) |
| 4 | 1 | `sdn-onboard/10.1 - ovsdb-raft-clustering.md` | **S2** commit ? (line 414 `cornerstone tier 1`) |
| 5 | 1 | `sdn-onboard/9.11 - ovs-appctl-reference-playbook.md` | **S2** commit 1 (line 3 `Phase H session`) |
| 6 | 1 | `sdn-onboard/9.24 - ovs-conntrack-stateful-firewall.md` | **S2** commit 2 (line 684 `Tier 1 cornerstone`) |
| 7 | 1 | `sdn-onboard/9.4 - ovs-cli-tools-playbook.md` | **S2** commit 1 OR new (line 3 `Phase H session`) |

**Note:** Master audit Agent C identified 9.22 as having 5 GP-11 leak instances at lines 492/630/636/954/1072 (`Tier importance: cornerstone tuyệt đối`). The v2 hook does NOT detect these because the actual phrasing in 9.22 likely differs from the regex (e.g., uses different word order or surrounding markdown). **Action:** S2 phase will manually re-grep 9.22 + verify; if hits exist, augment v2 regex tier-importance-bold-label pattern in S0 follow-up commit before S2 starts.

### 3.2. NON-OVS scope (deferred to Plan v3.10+ per GP-12 cadence)

**Subtotal:** 73 violations across 9 file (68% of total).

| Rank | Lines | File | Defer plan |
|---:|---:|------|------------|
| 1 | 46 | `sdn-onboard/13.18 - ovn-mlf-regbit-catalog.md` | OVN audit (v3.10) |
| 2 | 10 | `sdn-onboard/13.19 - ovn-pipeline-stage-catalog.md` | OVN audit (v3.10) |
| 3 | 8 | `sdn-onboard/3.5 - openflow-message-catalog.md` | OF audit (v3.11) |
| 4 | 2 | `sdn-onboard/13.5b - port-binding-type-catalog.md` | OVN audit |
| 5 | 2 | `sdn-onboard/4.8 - openflow-match-field-catalog.md` | OF audit |
| 6 | 2 | `sdn-onboard/README.md` | Cross-block audit |
| 7 | 1 | `sdn-onboard/13.6 - ha-chassis-group-and-bfd.md` | OVN audit |
| 8 | 1 | `sdn-onboard/4.9 - openflow-action-catalog.md` | OF audit |
| 9 | 1 | `sdn-onboard/_templates/template-d-per-table.md` | Cross-block audit |

**Significance:** v3.9 audit scope (45 OVS file) does NOT cover these. Per GP-12 cadence, master block-level audit cho OVN block (T+7 day from v4.0.1 tag if issued) sẽ surface these as primary findings. Plan v3.10 (OVN block hotfix) sẽ scope cleanup tương tự v3.9 S2/S3.

---

## 4. Per-pattern detail (each pattern × occurrence)

### 4.1. `axis-numbered-vn-heading` (75 hits)

Pattern: `^### N. <axis name>` where N=1..20 and axis name is one of 22 VN/EN labels.

| File | Line count |
|------|-----------:|
| `13.18 - ovn-mlf-regbit-catalog.md` | 46 |
| `9.32 - ovs-classifier-internals-deep.md` | 23 |
| `3.5 - openflow-message-catalog.md` | 6 |

**Cleanup approach (Phase S3 + future v3.10/v3.11):** Replace `### N. Axis-name` → `### Axis-name` (drop axis number). Per Rule 16 §16.2 replacement table, no information lost; reader-facing curriculum should not expose internal rubric numbering.

### 4.2. `tier-cornerstone-informal` (24 hits)

Pattern: `Tier N cornerstone` OR `cornerstone tier N tuyệt đối`.

| File | Line count |
|------|-----------:|
| `13.19 - ovn-pipeline-stage-catalog.md` | 10 |
| `9.2 - ovs-kernel-datapath-megaflow.md` | 3 |
| `3.5 - openflow-message-catalog.md` | 2 |
| `13.5b - port-binding-type-catalog.md` | 2 |
| `9.1 - ovs-3-component-architecture.md` | 2 |
| `13.6 - ha-chassis-group-and-bfd.md` | 1 |
| `4.8 - openflow-match-field-catalog.md` | 1 |
| `9.32 - ovs-classifier-internals-deep.md` | 1 |
| `9.24 - ovs-conntrack-stateful-firewall.md` | 1 |
| `10.1 - ovsdb-raft-clustering.md` | 1 |

**Cleanup approach (Phase S2):** Drop `Tier N cornerstone` informal phrasing entirely. Reader-facing curriculum không cần author tier-stamp; importance khi cần được expose qua prose ("cốt lõi", "trụ cột") trong axis 7 Tầm quan trọng section.

### 4.3. `phase-session-reference` (7 hits)

Pattern: `Phase [HIJKLS]\d* session\b`.

| File | Line | Context |
|------|-----:|---------|
| `4.8 - openflow-match-field-catalog.md` | 3 | header `**Trạng thái:**` line |
| `4.9 - openflow-action-catalog.md` | 3 | header `**Trạng thái:**` line |
| `9.4 - ovs-cli-tools-playbook.md` | 3 | header `**Trạng thái:**` line |
| `9.11 - ovs-appctl-reference-playbook.md` | 3 | header `**Trạng thái:**` line |
| `_templates/template-d-per-table.md` | 172 | template guidance |
| `README.md` | 155 | mention trong intro |
| `README.md` | 156 | mention trong intro |

**Cleanup approach (Phase S2 + S6):** Replace `Phase H session SN` → `(mở rộng 2026-04)` hoặc skip line nếu meta-status không cần thiết. Header `**Trạng thái:**` line concentrate này — 4/7 file expose Phase H session ngay dòng 3 (file metadata).

### 4.4. `cohort-cornerstone-phrase` (1 hit)

| File | Line | Context |
|------|-----:|---------|
| `9.2 - ovs-kernel-datapath-megaflow.md` | 870 | section heading `## 9.2.14 Bổ sung chuyên sâu cohort cornerstone OVS datapath` |

**Cleanup approach (Phase S2 commit 1):** Heading `## 9.2.14 Bổ sung chuyên sâu cohort cornerstone OVS datapath` → `## 9.2.14 Bổ sung chuyên sâu OVS datapath`.

### 4.5. `cohort-batch-stamp-leftover` (1 hit)

| File | Line | Context |
|------|-----:|---------|
| `9.32 - ovs-classifier-internals-deep.md` | 526 | `### 9-20. (compact treatment per cohort batch limit)` |

**Cleanup approach (Phase S3 commit 2):** Delete entire line + adjacent blank lines. Phần content sau line này thuộc §9.32.4 dpif đã planned expand 20→80+ dòng.

### 4.6. Patterns với 0 hit (clean)

V1 patterns không phát hiện leak nào trong curriculum hiện tại (R0.7 cleanup từ v3.8 effective):
- `axis-bold-label`, `axis-numbered-reference`, `cohort-label` (strict C/M/P\d format), `phase-plan-reference`, `phase-batch-reference`, `tier-label-deep`, `tier-label-partial`, `tier-label-reference`, `tier-label-placeholder`, `rubric-meta-term`, `anti-gaming-meta`, `governance-principle-reference`, `form-ab-reference`

V2 patterns chưa thấy hit:
- `tier-importance-bold-label` (0 hit) — Master audit Agent C claimed 9.22 lines 492/630/... có. Phase S2 sẽ verify.
- `stale-phase-compat-note` (0 hit) — Master audit Agent B claimed 9.9:58 có. Có thể formatting thực khác regex pattern. Phase S2 sẽ verify.

---

## 5. Pattern-vs-Audit reconciliation

Master audit OVS block 2026-04-27 (5 agent parallel) reported 12+ GP-11 violations xuyên 7 file. V2 hook detected 35 OVS-scope leak. Reconciliation:

### 5.1. Confirmed (audit + hook agree)

- 9.32 axis-numbered §9.32.1/§9.32.2 (Agent C) → hook detected 23 hit
- 9.32 line 526 cohort-batch (Agent C) → hook detected 1 hit
- 9.2:870 cohort cornerstone heading (Agent A) → hook detected 1 hit
- 9.2 lines 941/1118 + 1336 `cornerstone tier 1` (Agent A) → hook detected 3 hit (337/623 cũng được ghi)
- 9.1 lines 337/623 `cornerstone tier 1 tuyệt đối` (Agent A) → hook detected 2 hit
- 9.4:3 `Phase H session` (Agent B) → hook detected 1 hit
- 9.11 §9.11.X `Phase H session S39` (Agent B) → hook detected 1 hit
- 9.24:684 `Tier 1 cornerstone` (Agent C) → hook detected 1 hit
- 10.1:414 `cornerstone tier 1` (Agent D) → hook detected 1 hit (NEW finding, not in master audit explicit list)

### 5.2. Audit reported but hook missed (potential false-negative)

**9.22 lines 492/630/636/954/1072 `Tier importance: cornerstone tuyệt đối` (Agent C, 5 instances):**

V2 regex `tier-importance-bold-label` requires markdown bold form `**Tier importance: cornerstone**`. If 9.22 actual phrasing has variation (e.g., different surrounding markdown, line-break, capitalization), pattern misses.

**Action:** Pre-S2 verification — manually grep 9.22 và inspect each line. If actual format ≠ regex, update v2 regex in patch commit before S2 main work.

**9.9:58 `(reference, giữ tương thích content Phase B)` (Agent B):**

V2 regex `stale-phase-compat-note` requires exact phrase. If 9.9 actual phrasing has minor variation, pattern misses.

**Action:** Pre-S2 manual grep verify.

**9.9:58 stale Phase B (Agent B) — generic fact unverified by hook scan:**

If 9.9 actual file does NOT contain this string at line 58 (audit could be wrong), no fix needed. Pre-S2 will verify.

### 5.3. Hook found but audit missed

- **10.1:414 `cornerstone tier 1`** — 1 hit, NOT in master audit Agent D explicit list. 10.1 is mastery-grade per audit (DEEP-20 cornerstone strongest). This 1 leak is minor.

- **9.32:1336 `Tier 1 cornerstone`** (counted in 9.32 25-leak total) — Master audit covered §9.32.1/§9.32.2 + line 526 but didn't enumerate this specific instance.

**Action:** Phase S2 commit will sweep all hook-detected hits, regardless of master-audit enumeration.

---

## 6. Phase-fix mapping

| Phase | Files | Hits | Pattern dominant |
|-------|-------|-----:|------------------|
| **S2 commit 1** | 9.2, 9.9, 9.11 | 4 + 1 + 1 = 6 | cohort-cornerstone, tier-cornerstone, phase-session, stale-phase-compat |
| **S2 commit 2** | 9.22, 9.24, 9.32 line 3 | 0 (9.22 manual) + 1 + 0 = 1+? | tier-importance, tier-cornerstone, meta-status |
| **S3 commit 1** | 9.32 §9.32.1 | ~10-13 | axis-numbered-vn-heading |
| **S3 commit 2** | 9.32 §9.32.2 + line 526 | ~10-13 + 1 | axis-numbered + cohort-batch |
| **S3 commit 3** | 9.32 §9.32.4 expansion | (no leak fix, content expand) | (creates new content) |
| **S0 follow-up** (if needed) | 9.1, 9.4, 10.1 cleanup | 2 + 1 + 1 = 4 | tier-cornerstone (small), phase-session (small) |
| **Future v3.10** | 13.18, 13.19, 13.5b, 13.6 | 46 + 10 + 2 + 1 = 59 | axis-numbered, tier-cornerstone (OVN scope) |
| **Future v3.11** | 3.5, 4.8, 4.9 | 8 + 2 + 1 = 11 | axis-numbered, tier-cornerstone, phase-session (OF scope) |
| **Future cross-block** | README.md, _templates/* | 2 + 1 = 3 | phase-session |

**Total v3.9 mandatory fix:** ~30 hits (9.32 §1+§2+line526 + 9.2 + 9.1 + 9.4 + 9.11 + 9.24 + 10.1).
**Total v3.9 + 9.22 manual:** 35 hits in OVS scope.
**Total deferred:** 73 hits in non-OVS scope.

---

## 7. Verbatim report excerpt (first 60 lines)

```
=== RUBRIC LEAK CHECK FAIL ===

--- sdn-onboard/10.1 - ovsdb-raft-clustering.md (1 leak) ---
  L414:28 [tier-cornerstone-informal] 'cornerstone tier 1'

--- sdn-onboard/13.18 - ovn-mlf-regbit-catalog.md (46 leak) ---
  L24:1 [axis-numbered-vn-heading] '### 1. Khái niệm'
  L30:1 [axis-numbered-vn-heading] '### 2. Lịch sử'
  L34:1 [axis-numbered-vn-heading] '### 3. Vị trí'
  L38:1 [axis-numbered-vn-heading] '### 4. Vai trò'
  L42:1 [axis-numbered-vn-heading] '### 5. Vì sao'
  L46:1 [axis-numbered-vn-heading] '### 6. Vấn đề'
  L54:1 [axis-numbered-vn-heading] '### 8. Cơ chế'
  L85:1 [axis-numbered-vn-heading] '### 10. Phân loại'
  ... 38 more

--- sdn-onboard/13.19 - ovn-pipeline-stage-catalog.md (10 leak) ---
  L45:21 [tier-cornerstone-informal] 'Tier 1 cornerstone'
  L151:21 [tier-cornerstone-informal] 'Tier 1 cornerstone'
  ... 8 more

--- sdn-onboard/3.5 - openflow-message-catalog.md (8 leak) ---
  L343:123 [tier-cornerstone-informal] 'Tier 1 cornerstone'
  L345:1 [axis-numbered-vn-heading] '### 8. Cơ chế'
  ... 6 more

--- sdn-onboard/9.1 - ovs-3-component-architecture.md (2 leak) ---
  L337:28 [tier-cornerstone-informal] 'cornerstone tier 1 tuyệt đối'
  L623:28 [tier-cornerstone-informal] 'cornerstone tier 1 tuyệt đối'

--- sdn-onboard/9.11 - ovs-appctl-reference-playbook.md (1 leak) ---
  L3:32 [phase-session-reference] 'Phase H session'

--- sdn-onboard/9.2 - ovs-kernel-datapath-megaflow.md (4 leak) ---
  L870:30 [cohort-cornerstone-phrase] 'cohort cornerstone'
  L941:28 [tier-cornerstone-informal] 'cornerstone tier 1'
  L1118:28 [tier-cornerstone-informal] 'cornerstone tier 1 tuyệt đối'
  L1336:21 [tier-cornerstone-informal] 'Tier 1 cornerstone'

--- sdn-onboard/9.24 - ovs-conntrack-stateful-firewall.md (1 leak) ---
  L684:21 [tier-cornerstone-informal] 'Tier 1 cornerstone'

--- sdn-onboard/9.32 - ovs-classifier-internals-deep.md (25 leak) ---
  L23:1 [axis-numbered-vn-heading] '### 1. Khái niệm'
  L27:1 [axis-numbered-vn-heading] '### 2. Lịch sử'
  L31:1 [axis-numbered-vn-heading] '### 3. Vị trí'
  ... 22 more

Total 108 leak across 16 file. Commit rejected per GP-11 / CLAUDE.md Rule 16.
```

---

## 8. Reproduction

```bash
cd C:/Users/voleh/Documents/network-onboard
PYTHONIOENCODING=utf-8 python -X utf8 scripts/rubric_leak_check.py --all --report
```

Expected exit code: **1** (FAIL — 108 violations).
Hook intentionally fails to enforce GP-11 / CLAUDE.md Rule 16.

To re-baseline post-S2/S3/S6 (incremental):

```bash
PYTHONIOENCODING=utf-8 python -X utf8 scripts/rubric_leak_check.py --all --report > memory/sdn/rubric-leak-baseline-<DATE>.txt
```

Compare delta:

```bash
diff <(grep "^Total" memory/sdn/rubric-leak-baseline-2026-04-27.md) \
     <(grep "^Total" memory/sdn/rubric-leak-baseline-<NEW-DATE>.md)
```

---

## 9. Cross-references

- **Plan:** [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md)
- **Hook script v2:** [`scripts/rubric_leak_check.py`](../../scripts/rubric_leak_check.py)
- **Test suite:** [`scripts/tests/test_rubric_leak_check.py`](../../scripts/tests/test_rubric_leak_check.py)
- **Governance:** [`memory/sdn/governance-principles.md`](governance-principles.md) GP-11
- **CLAUDE.md:** Rule 16 Internal-vs-Reader-Facing Language Separation
- **Replacement table:** [`plans/sdn/v3.8-remediation.md`](../../plans/sdn/v3.8-remediation.md) Section 11.4
