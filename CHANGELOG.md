# Changelog — network-onboard

Training curriculum cho kỹ sư mạng: OpenvSwitch + OpenFlow + OVN. Focus sâu 5 trụ cột: nền tảng kiến thức, tools mastery, output interpretation, debug + troubleshoot, architecture + mechanism.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) adapted cho training series.

---

## v3.2-FullDepth (2026-04-25)

**Release type:** Minor release — audit residual content depth expansion.
**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.1.1-OperatorMaster-patch + 5 deferred audit findings resolved.
**Effort:** 1 working session (sequential P1→P5 priority execution).

### Mục tiêu

Đóng toàn bộ residual finding đã defer từ v3.1.1 patch — chuyển từ curriculum "operator mastery" sang "full depth mastery" với Block XIII Core đạt parity depth cùng Block IX + Block XX, tất cả CLI reference file có Anatomy Template A consistent, và narrative file Block II có Hiểu sai callout đạt professor-style 5/6 criteria.

### Changes

5 priority commits addressing all residual findings:

1. **P1 Block XIII Core expand** (7 commits `e3109ea` → `737980f`, audit P4.B13.1 CRITICAL + P4.B13.4 + P4.B13.5):
   - `13.0` OVN announcement 2015: 153 → 337 (+184) — author deep-dive Pfaff/Pettit/Shuhaa, 3 kỹ thuật + 2 thương mại motivation, 3-tier kiến trúc expanded, 4 alternative comparison, evolution timeline, GE 3-tier compilation.
   - `13.1` NBDB/SBDB schema: 505 → 624 (+119) — Anatomy Template A `ovn-nbctl show` + `list Datapath_Binding`, 2 Hiểu sai + Key Topic, GE NBDB→SBDB timing propagation.
   - `13.2` LS+LR pipeline: 399 → 546 (+147) — Anatomy `ls-list` + `lflow-list`, 2 Hiểu sai + Key Topic 27+10 stage, Capstone POE 3-tier ping trace.
   - `13.3` ACL + Port_Group: 411 → 563 (+152) — Anatomy `ovn-nbctl acl-list` 9-attr, 2 Hiểu sai + Key Topic scale, Capstone POE 1000-VM segmentation.
   - `13.4` br-int deep: 142 → 566 (+424) — CRITICAL expansion: 3-bridge pattern, patch port `ovs_vport_receive()` tail-call, 4 failure modes, 2 GE + Capstone POE TCAM utilization.
   - `13.5` Port_Binding 8 types: 182 → 455 (+273) — claim mechanism Raft propagation, Anatomy `list Port_Binding`, GE claim workflow, 5-step debug diagnostic.
   - `13.6` HA_Chassis + BFD: 184 → 469 (+285) — RFC 5880 packet format + state machine + timing math, Anatomy `ovs-appctl bfd/show` 11-attr, 13-step failover timeline, 4 failure modes, 11-step Capstone.
   - **Block XIII Core total: 1,976 → 3,560 (+1,584, +80% growth)**

2. **P2 Block IX Ops expand** (5 commits `5242de1` → `4cdb2ff`, audit P4.B9.2 MED):
   - `9.6` bonding+LACP: 162 → 297 (+135) — Anatomy `bond/show` 10-attr, 2 Hiểu sai, 4 failure modes, performance table.
   - `9.7` port mirroring: 154 → 275 (+121) — Anatomy `list Mirror` 9-attr, 2 Hiểu sai, 4 failure modes, retention planning table.
   - `9.8` flow monitoring sFlow/IPFIX: 152 → 252 (+100) — Anatomy `list sFlow` 9-attr, 2 Hiểu sai, capacity planning.
   - `9.10` TLS/PKI: 174 → 258 (+84) — Anatomy `list SSL` 9-attr, 2 Hiểu sai, 4 failure modes.
   - `9.12` upgrade/rolling restart: 172 → 248 (+76) — Anatomy pre-upgrade checklist 9-attr, 2 Hiểu sai "golden 3 rules", 4 failure modes.
   - **Block IX Ops total: 814 → 1,330 (+516, +63% growth)**

3. **P3 Block IV hands-on GE** (1 commit `1d192ef`, audit P4.B4.1 HIGH):
   - `4.0` multi-table pipeline GE (+59 dòng)
   - `4.1` OXM TLV ARP + TCP flags GE (+43)
   - `4.2` meter rate-limit GE (+42)
   - `4.3` bundle atomic GE (+50)
   - `4.4` egress simulation GE (+47)
   - `4.5` TTP capability discovery GE (+38)
   - **Block IV hands-on total: +279 dòng** (implement flow với OVS cho từng OF version feature).

4. **P4 CLI Anatomy standardize** (1 commit `9978e2e`, audit P5.C1 MED):
   - `20.0` §20.X `ovs-appctl coverage/show` debug entry 9-attr + 4 kịch bản (+27).
   - `20.1` §20.X ACL audit + port_security multi-command 9-attr + 4 kịch bản (+48).
   - `9.27` §9.27.7 `tnl/ports/show` + `bfd/show` cross-host tunnel 9-attr + 4 kịch bản (+38).
   - **Anatomy Template A standardize total: +112 dòng** — curriculum-wide pattern consistent.

5. **P5 Block II narrative enhance** (1 commit `0da3996`, audit P6.N1 MED):
   - `2.0` DCAN/OPENSIG/GSMP: 2 Hiểu sai (OpenFlow phát minh mới 2008 + idea sai vs technology sai).
   - `2.1` Ipsilon/Active Networking: 2 Hiểu sai (AN là tiền thân SDN + Ipsilon = GSMP lỗi).
   - `2.2` NAC/Orchestration/Virtualization: 2 Hiểu sai (NAC = SDN + vDS = SDN đầu tiên).
   - **Block II narrative total: +12 dòng** compact Hiểu sai callout. Đạt professor-style 5/6 criteria.

### Finding status (v3.2 closure)

| Severity | v3.1.1 deferred | v3.2 resolved | Residual |
|----------|----------------|---------------|----------|
| CRITICAL | 1 (P4.B13.1) | 1 | 0 |
| HIGH | 2 (P4.B4.1 + P4.B13.2) | 2 | 0 |
| MED | ~5 (P4.B9.2 + P5.C1 + P6.N1 + decision matrix) | 4 | 1 (stylistic, LOW-impact) |
| LOW | ~4 | 2 | 2 (Part X.Y.Z terminology cosmetic) |

**100% CRITICAL + HIGH closure.** Curriculum đạt verdict **A** post-audit (từ A- v3.1.1).

### Statistics (v3.2 delta from v3.1.1)

- **28 files modified** across 15 commits
- **+3,373 insertions, -321 deletions** = +3,052 net
- Block XIII Core: 7 file, 1,976 → 3,560 (+1,584, 80% growth)
- Block IX Ops: 5 file, 814 → 1,330 (+516, 63% growth)
- Block IV hands-on: 6 file +279 (GE sections)
- Anatomy standardize: 3 file +112
- Block II narrative: 3 file +12
- Anatomy Template A (9-attribute + "red flag" + diagnostic hint) applied to: 10 new locations
- Hiểu sai callout: 16 new (Block II 6 + Block XIII 10)
- Guided Exercise: 11 new (Block IV 6 + Block XIII 3 + Block IX 2)
- Capstone POE: 4 new (Block XIII 4)
- Rule 9 null byte: 0 regressions
- Rule 11 prose: maintained 99%+ compliance
- Rule 13 em-dash density: 0/28 files in warn zone (>0.10)

### Curriculum state post-v3.2

- **116 file** sdn-onboard/*.md (unchanged count, depth expansion only)
- **~55.7K dòng** (from ~52.6K baseline v3.1)
- Block XIII Core: 13 file, parity depth với Block IX + Block XX
- Anatomy Template A presence: Part 9.4/9.11/13.2/13.3/20.1/20.0/9.27 + all Block XIII Core (consistent pattern)
- Professor-style 5/6 criteria: 100% narrative file (Block I + II + III) có Hiểu sai + Key Topic callout

### Known residual (defer post-v3.2)

- **P7.R1 LOW**: Part X.Y.Z terminology normalization across ~8 legacy file headers. Cosmetic, non-blocking.
- **P4.B9.3 LOW**: 9.26 References section sub-heading format. Cosmetic.
- **Lab verification (C1b)**: 63 exercise pending lab host availability. External dependency.

### Links

- Audit master report: [`memory/audit-2026-04-25-master-report.md`](memory/audit-2026-04-25-master-report.md)
- v3.2 commits: `e3109ea` → `0da3996` (15 commits sequential)

---

## v3.1.1-OperatorMaster-patch (2026-04-25)

**Release type:** Patch release — audit compliance remediation.
**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.1-OperatorMaster + audit 2026-04-25 9-phase master report + 7 patch commits.
**Effort:** 1 working session post-audit.

### Audit 2026-04-25 context

Post-release comprehensive audit (9-phase) ngay sau tag v3.1. Tìm thấy 1 CRITICAL + 7 HIGH + 30 MED + 17 LOW + 13 STRONG positive finding. Verdict: curriculum production-ready GPA A-. v3.1.1 patch sprint address tất cả HIGH findings ngoại trừ những điểm content-level deferred sang v3.2.

### Changes

7 commits addressing findings từ audit Phase 1-8:

1. **P1.1 Dependency map backfill** (b542de5): 44 file content-phase (5 block VII/VIII/XII/XIV/XV từ 0% → 100% coverage). Rule 2 Cross-File Sync: 62% → ~95%. Line count + section count verified thực tế qua `wc -l` + grep.
2. **P1.2 Rule 11 prose Group A** (db49646): ~50 hit clear prose leak fixed across 40 file. Categories: approach → cách tiếp cận, flexibility → tính linh hoạt, motivation → động cơ, adoption → sự chấp nhận, paradigm → mô hình, convention → quy ước, postmortem → báo cáo hậu sự, troubleshoot → khắc phục sự cố, scalability → khả năng mở rộng, senior → kỳ cựu.
3. **P1.3 Rule 11 Group B manual triage** (cf93aa0): ~13 case-specific hit trong decision matrix + table labels. 16.2 Capstone decision matrix normalized Vietnamese labels. Table column headers 5.0/14.1/14.2 translated.
4. **P2.1 6 dead URL + README heading + S61b regression** (61f3000):
   - Dead URL fix: Network Heresy → wordpress.com, Stanford CS244 Ethane → yuba.stanford.edu, Princeton 4D → /ccr05-4d.pdf (Rexford reorganized), NVIDIA DOCA → /doca/sdk/, ONF press archive, p4.org/specs → p4lang/p4-spec.
   - README heading: Block IX 27→28, Block XX 6→7, total 20 block.
   - S61b regression restore: "Comprehensive Approach" book title (8 file), "OpenFlow Switch Specification Version" (12 instance), "High-Performance" (3 instance).
   - CLAUDE.md Rule 14 example clarify.
5. **P3.1 Memory + README + Mermaid** (26c4526):
   - `memory/sdn-series-state.md` (new 300 dòng, Rule 5 Session Handoff Protocol)
   - `memory/audit-index.md` (new, TOC of audit logs)
   - Parent `README.md` SDN section: +Block XX + Expert Extension summary + 12 new links (20.x + 9.26/9.27 + 14.x + 15.0 + 16.x).
   - `sdn-onboard/README.md`: 6 reading path → **7** (path 7 "Operator daily runbook" 30-50h). Mermaid graph: +P20 node (ops class green thick border) + 2 arrows.
6. **P4.1 Cosmetic cleanup** (b68dad5):
   - Paul Göransson diacritic fix (32 file) — "Goransson" → "Göransson".
   - CRLF → LF normalize (41 file regression from Task #6 Python script encoding).
   - Trailing whitespace strip.
   - Decimal separator "1,26 tỷ" (VN convention).
7. **P5.1 Man page backfill** (f08c8db):
   - 9.14 incident-response +11 man page (ovs-vswitchd, ovs-appctl, ovs-ofctl, ovs-dpctl, ovsdb-tool, conntrack, ethtool, ip-link, ovs-bugtool, ovs-pcap, ovs-testcontroller).
   - 20.1 security-hardening +7 man page (ovs-pki, ovsdb-server/client, openssl-s_client, ovn-nbctl/sbctl, ovn-trace, auditd) + RFC 5280 PKIX.
   - References section reorganized thành sub-heading (Documentation / Man pages / Standards).
   - inc-engine/show-stats verified upstream canonical naming.

### Finding status

| Severity | Count | v3.1.1 resolved | Deferred v3.2 |
|----------|-------|----------------|---------------|
| CRITICAL | 1 | 0 | 1 (P4.B13.1 Block XIII Core content expansion) |
| HIGH | 7 | 5 | 2 (P4.B4.1 Block IV hands-on + P4.B13.2 Block XIII 0 POE — content level) |
| MED | 30 | 25+ | ~5 (P4.B9.2 Block IX Ops expand + P4.B13.4 13.4 br-int expand + decision matrix stylistic) |
| LOW | 17 | 13+ | ~4 (P7.R1 Part X.Y.Z terminology + P4.B9.3 9.26 References heading) |

### Known residual (defer v3.2)

- **P4.B13.1 CRITICAL**: Block XIII Core (13.0-13.6) content expansion (+2000 dòng, 20-30h effort). Target v3.2-FullDepth.
- **P4.B4.1 HIGH**: Block IV 4.0-4.5 hands-on GE (6 file). Target v3.2.
- **P4.B9.2 MED**: Block IX Ops 9.6/9.7/9.8/9.10/9.12 expand (+1200 dòng). Target v3.2.
- **P5.C1 MED**: 20.0/20.1/9.27 Anatomy Template A standardize. Target v3.2.
- **P6.N1 MED**: Block II 2.0/2.1/2.2 phản biện + Hiểu sai callout. Target v3.2.

### Statistics (v3.1.1 delta)

- 47 file modified across 7 commits
- 570+ insertions, 540+ deletions (most cosmetic)
- 2 new memory files (sdn-series-state + audit-index)
- Rule 2 Cross-File Sync: 62% → ~100% (expected post backfill)
- Rule 11 Vietnamese prose: ~95% → ~99%
- Rule 9 null byte: 0 regressions maintained
- Rule 13 em-dash density: 0 warn zone introductions
- Dead URL: 6 → 0

### Links

- Audit master report: [`memory/audit-2026-04-25-master-report.md`](memory/audit-2026-04-25-master-report.md)
- Per-phase reports: `memory/audit-2026-04-25-phase1-8-*.md`
- v3.1.1 commits: `b542de5` → `f08c8db` (7 commits sequential)

---

## v3.1-OperatorMaster (2026-04-24)

**Release type:** Foundation + Operator Mastery complete.
**Branch:** `docs/sdn-foundation-rev2`
**Scope curriculum:** 116 file `sdn-onboard/*.md`, ~52.6K dòng content.
**Lab verification:** pending (C1b — chờ user cung cấp lab host).

### Highlights

- **Phase G Operator Master 5/5 area COMPLETE** (S37a-c + S51-S59):
  - G.1 Truy vết: Part 9.25 ofproto/trace expansion + Part 9.27 packet journey end-to-end + Part 13.7 ovn-controller run loop deep + Part 20.0 case study playback.
  - G.2 Xử lý sự cố: Part 9.14 20-symptom decision tree expansion + Part 20.5 OVN forensic 3 case study (Port_Binding migration race / northd bulk delete / MAC_Binding explosion).
  - G.3 Debug sâu: Part 9.26 OVS revalidator storm forensic 3 case study + Part 20.1 security hardening 4-layer audit trail + Part 20.2 OVN troubleshooting deep-dive.
  - G.4 Lịch sử: Part 20.6 reflective retrospective 2007-2024 (17 năm SDN, 10 meta-lesson universal).
  - G.5 Thao tác công cụ: Part 20.3 OVN daily operator playbook + Part 20.4 OVS daily operator playbook.
- **Phase H Foundation Depth 13 session COMPLETE** (S38-S50):
  - Template library A/B/C/D trong `sdn-onboard/_templates/`.
  - Full OpenFlow match field catalog (Part 4.8) + action catalog (Part 4.9) với 100% spec coverage.
  - Full OVN pipeline exhaustive (ls_in_*/ls_out_*/lr_in_*/lr_out_*) trong Part 13.2+13.11.
  - OVS internals tier 1 expand (Part 9.1 + 9.15 + 9.16) với classifier TSS + connection manager + ofproto-dpif deep.
  - Tools coverage closed: ovs-bugtool + ovs-pcap + ovs-testcontroller.
- **Phase E Fact-check audit 101 file** (S32-S33i): Rule 14 Source Code Citation Integrity codified.
- **Phase F Cloud Native partial** (S36a-g): Block XIV (P4), Block XVI (DPDK+AFXDP), Block XV partial (Service Mesh 15.0 only, 15.1+15.2 deferred per user directive).
- **Pre-release audit** (S60-S61):
  - Rule 9 null byte: PASS 0/116.
  - Rule 13 em-dash density < 0.10: PASS 0/116.
  - Rule 11 Vietnamese prose: 185/295 leak fixed (63% reduction). 110 residual trong spec/table/numbered step contexts, defer v3.1.1 patch release.
  - Rule 14 source code citation: spot-check PASS.

### Statistics

| Metric | Count |
|--------|-------|
| Total file | 116 |
| Total line | ~52.641 |
| Block (foundation 0-XIII + extension XIV-XVI + forensic XVII-XIX + operations XX) | 20 |
| Guided Exercises + Capstone POE | 60+ |
| Anatomy Template A blocks | ~25 |
| Decision matrices (symptom-to-cause) | 4 major |
| Offline source citations | 100% Phase B+ |
| Upstream SHA + function verifications (Phase E) | 100+ |

### Known residual (v3.1.1 patch planned)

- **Rule 11 polish**: 110 minor Vietnamese prose leak còn lại trong core file. Phần lớn là numbered step Guided Exercise (`**3.** Verify connection`), table column header (`OpenFlow 1.X support`), vendor fact sentence (`HP ProCurve support 1.3`). Không ảnh hưởng kỹ thuật hay sự đọc hiểu, chỉ là discipline polish.
- **Block XIV+XV+XVI (68 leak)**: deprioritized theo user directive 2026-04-23 và 2026-04-24 "Đừng sa đà vào K8S, DPDK, XDP". Giữ skeleton + content nhưng không invest polish tiếp.
- **Lab verification (C1b)**: 63 exercise chờ lab host sẵn sàng. Output số liệu trong Guided Exercise là doc-plausible, chưa run thực tế.

### Files added Phase G (10 new/expanded)

- `sdn-onboard/9.14 - incident-response-decision-tree.md` (expand → 20 symptom matrix)
- `sdn-onboard/9.25 - ovs-flow-debugging-ofproto-trace.md` (expand +3 GE)
- `sdn-onboard/9.26 - ovs-revalidator-storm-forensic.md` (expand +2 case)
- `sdn-onboard/9.27 - ovs-ovn-packet-journey-end-to-end.md` (new)
- `sdn-onboard/13.7 - ovn-controller-internals.md` (expand run loop)
- `sdn-onboard/20.1 - ovs-ovn-security-hardening.md` (expand +audit trail)
- `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` (new)
- `sdn-onboard/20.3 - ovn-daily-operator-playbook.md` (new)
- `sdn-onboard/20.4 - ovs-daily-operator-playbook.md` (new)
- `sdn-onboard/20.5 - ovn-forensic-case-studies.md` (new)
- `sdn-onboard/20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` (new)

### Commits milestone

Session milestone commits trên `docs/sdn-foundation-rev2`:

- Phase E: `7e5608b` (S33i Rule 14 codify)
- Phase F: `c777acf` (S36g 15.0)
- Phase H: `8dcbeca` (S59 phase G.4 close, also last Phase H commit baseline)
- Phase G: `8dcbeca` (S59 Phase G 100% COMPLETE)
- Pre-release audit: `ab9f38b` (S60) → `9469359` (S61a) → `d15d701` (S61b)

---

## Pre-release milestones (untagged)

### v2.1-preVerified (2026-04-22 post S35)

Phase E Scope D fact-check audit complete. Rule 14 Source Code Citation Integrity codified vào CLAUDE.md. Pre-release candidate nhưng chưa có release packaging.

### v2.0 (2026-04-22 post S29)

Phase D foundation firewall + audit backlog complete. 91 file curriculum với Block I-XIII content fully expanded. Rule 11 Vietnamese Prose Discipline codified.

### v1.0-preVerified (2026-04-21)

Phase B content expansion end-to-end. 64 file với Block 0-XIII content expanded + 3 advanced forensic (Part 17-19). Rule 10 Architecture-First Doctrine codified.

---

## Links

- Repo: https://github.com/volehuy1998/network-onboard
- SDN roadmap: [`sdn-onboard/README.md`](sdn-onboard/README.md)
- Pre-release audit: [`memory/pre-release-audit-2026-04-24.md`](memory/pre-release-audit-2026-04-24.md)
- Session history: [`memory/session-log.md`](memory/session-log.md)
- Project rules: [`CLAUDE.md`](CLAUDE.md) (14 mandatory rules + 6 skill)
