# Audit 2026-04-25 — Phase 7 Báo cáo Cross-cutting Coherence

> **Phạm vi:** 116 file sdn-onboard + README.md parent + memory/file-dependency-map.md
> **Mục tiêu:** Cross-ref integrity + TOC alignment + dependency map coverage + URL integrity broader + reading path consistency
> **Skills kích hoạt:** search-first (file audit), web-fetcher (URL verify), professor-style (TOC quality)

---

## 1. Tổng quan

### 1.1. Các chỉ số coherence

| Chỉ số | Giá trị |
|---|---|
| File filesystem | 116 |
| TOC link trong `sdn-onboard/README.md` | 115 (không kể self) + 1 external `../CHANGELOG.md` |
| TOC phantom (link thiếu file) | 0 |
| TOC orphan (file thiếu link) | 0 |
| Parent `README.md` link đến sdn-onboard | 4 (README + 3 advanced Part 17-19) |
| Dependency map entries (`memory/file-dependency-map.md`) | 72 entry |
| File thiếu dependency map entry | 44 (37,9%) |
| Anchor link trong cùng file | Broken: 0 |
| Part cross-ref scan | 17 "broken" Part refs (tất cả đều là section refs hợp lệ) |
| URL unique toàn curriculum | 584 URLs |
| URL mentions | 1.080 |
| URL tested (sample 20) | 15 OK / 5 broken (25% fail) |

### 1.2. Phân bố URL theo domain

| Domain | URL count |
|---|---|
| `github.com` | 85 |
| `www.rfc-editor.org` | 52 |
| `docs.openvswitch.org` | 48 |
| `opennetworking.org` | 29 |
| `man7.org` | 28 |
| `dl.acm.org` | 17 |
| `datatracker.ietf.org` | 14 |
| `www.ovn.org` | 13 |
| `www.openvswitch.org` | 12 |
| `docs.kernel.org` | 11 |

Upstream tập trung vào `github.com` (source code), `docs.openvswitch.org` + `man7.org` + `opennetworking.org` (docs official). Phù hợp yêu cầu user "tài liệu online chính hãng chính chủ".

---

## 2. TOC alignment check

### 2.1. `sdn-onboard/README.md` TOC vs filesystem

| Chỉ số | Kết quả |
|---|---|
| Link trong TOC | 116 (115 sdn-onboard + 1 CHANGELOG.md parent) |
| File thực | 116 (bao gồm README tự) |
| Orphan file (có file, không có link) | **0** |
| Phantom link (có link, không có file) | **0** |

PASS. TOC ↔ Filesystem 100% consistent.

### 2.2. Heading count inconsistency (P1.C1-C3 đã flag)

| Location | Claim | Actual | Action |
|---|---|---|---|
| README line 183 | "Block IX (Part 9, **27 file**)" | 28 file | Fix → 28 |
| README line 322 | "Block XX (Part 20, **6 file**)" | 7 file | Fix → 7 |
| README line 97 | "13 Block foundation + 3 Block Expert Extension + 3 Part advanced" | +1 Block XX = 20 block total | Add "+ 1 Block Operational Excellence" = 20 block |

### 2.3. Parent `README.md` coverage

Parent (`/README.md`) liệt kê SDN series với 4 link:
- `sdn-onboard/README.md` (main TOC)
- `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md`
- `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md`
- `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md`

Đây là historical selection từ pre-rev2 (khi Part 17/18/19 là main advanced). Rev 4 đã add Block XIV-XVI + 20.x nhưng parent README chưa update reference.

### Phát hiện P7.T1

| ID | Mức | Mô tả |
|---|---|---|
| P7.T1 | MED | Parent `README.md` chỉ link 3 Part advanced Block XVII-XIX + README. Không link Part 20.x Operational Excellence + Block XIV-XVI Expert Extension + Part 9.26/9.27 forensic. Nên update parent README với 1 đoạn tóm tắt Block XX + link Phụ lục sdn-onboard/README.md để reader có entry point đầy đủ. |

---

## 3. Dependency map coverage (Rule 2 Cross-File Sync)

### 3.1. Baseline

P1.D1 (Phase 1) ghi nhận: 72 entry trong map, 44 file content thiếu (37,9%).

### 3.2. Block-by-block gap

| Block | Total file | Có map | Thiếu map | % coverage |
|---|---|---|---|---|
| 0 | 3 | 3 | 0 | 100% |
| I | 3 | 3 | 0 | 100% |
| II | 5 | 5 | 0 | 100% |
| III | 3 | 3 | 0 | 100% |
| IV | 10 | 8 | 2 (4.8, 4.9) | 80% |
| V | 3 | 1 | 2 (5.1, 5.2) | 33% |
| VI | 2 | 2 | 0 | 100% |
| VII | 6 | 0 | **6 toàn bộ** | 0% |
| VIII | 4 | 0 | **4 toàn bộ** | 0% |
| IX | 28 | 21 | 7 (9.16-9.21, 9.23) | 75% |
| X | 7 | 2 | 5 (10.0, 10.3-10.6) | 29% |
| XI | 5 | 3 | 2 (11.0, 11.2) | 60% |
| XII | 3 | 0 | **3 toàn bộ** | 0% |
| XIII | 14 | 11 | 3 (13.0, 13.9, 13.13) | 79% |
| XIV | 3 | 0 | **3 toàn bộ** | 0% |
| XV | 3 | 0 | **3 toàn bộ** | 0% |
| XVI | 3 | 1 | 2 (16.0, 16.2) | 33% |
| XVII-XIX | 3 | 3 | 0 | 100% |
| XX | 7 | 5 | 2 (20.5, 20.6) | 71% |

### 3.3. Blocks 100% missing (P1.D2 đã flag)

- Block VII (Controller ecosystem): 6 file 0%
- Block VIII (Linux primer): 4 file 0%
- Block XII (DC Topology): 3 file 0%
- Block XIV (P4): 3 file 0%
- Block XV (Service Mesh + K8s): 3 file 0%

### Phát hiện P7.D1

| ID | Mức | Mô tả |
|---|---|---|
| P7.D1 | HIGH | 5 block (VII/VIII/XII/XIV/XV) 0% coverage trong dependency map. Total 19 file missing entirely. Cần backfill entire blocks. Rule 2 Cross-File Sync strictly phụ thuộc map này. |
| P7.D2 | MED | Tính tổng: 44/116 file (37,9%) thiếu map. Nên backfill mass trong v3.1.1. |

---

## 4. Cross-ref integrity

### 4.1. Scan "Part X.Y" references

Scan 116 file cho pattern `Part \d+\.\d+`. Tổng phát hiện 17 "broken" refs nhưng phân loại lại:

| Category | Count | Đánh giá |
|---|---|---|
| Section ref misnamed "Part" (thực chất `§X.Y.Z`) | **15/17** | Terminology only. Technical valid. Ví dụ "Part 4.0.5" là section 4.0.5 inside Part 4.0. |
| Historical mention of removed Part (Part 6.2 Intent-Based Networking) | **1/17** | README line 348, rev 3 changelog context. Valid historical reference. |
| Section ref inside same Part (Part 20.13/20.14 inside 20.1) | **1/17** | 20.1 tự chứa § 20.13 + § 20.14 (Audit Trail + RBAC). Misnamed "Part". |

### Phát hiện P7.R1

| ID | Mức | Mô tả |
|---|---|---|
| P7.R1 | LOW | 15 section refs dùng "Part X.Y.Z" thay vì "§X.Y.Z". Terminology lỏng. Không phải lỗi chức năng. Fix: batch sed `Part (\d+\.\d+\.\d+)` → `§$1` nếu muốn chuẩn. Low priority cosmetic. |

### 4.2. Anchor links

Scan `[link](#anchor)` trong 116 file. Kết quả: 0 broken anchor. PASS.

---

## 5. URL integrity broader scan

### 5.1. Kết quả spot-check 20 URLs

Mở rộng từ Phase 6 (10 URLs) với 10 URLs thêm = 20 total URLs tested.

| # | URL | Status |
|---|---|---|
| 1-10 | From Phase 6 | 8 PASS + 3 DEAD (Network Heresy redirect, Stanford CS244, Princeton 4D) |
| 11 | `https://docs.nvidia.com/doca/sdk/ovs-doca/index.html` | **404** (new dead link) |
| 12 | `https://opennetworking.org/news-and-events/press-releases/open-networking-foundation-established/` | **404** (new dead link) |
| 13 | `https://p4.org/specs/` | **404** (new dead link) |
| 14 | `https://docs.openvswitch.org/en/latest/howto/dpdk/` | 200 |
| 15 | `https://docs.openvswitch.org/en/latest/intro/what-is-ovs/` | 200 |
| 16 | `https://docs.openvswitch.org/en/latest/howto/qos/` | 200 |
| 17 | `https://docs.ovn.org/en/latest/tutorials/ovn-sandbox.html` | 200 |
| 18 | `https://mail.openvswitch.org/pipermail/ovs-dev/2023-May/404718.html` | 200 |
| 19 | `https://github.com/opennetworkinglab/onos` | 200 |
| 20 | `https://www.kernel.org/doc/html/latest/admin-guide/mm/hugetlbpage.html` | 200 |

### 5.2. Tổng kết URL integrity

| Category | Count (trong 20 sample) | Estimate toàn curriculum |
|---|---|---|
| Working (200) | 15 | ~485/584 (83%) |
| Dead (404) | 4 | ~80/584 (14%) |
| Paywall (403) | 1 | ~30/584 (5%) |
| Rot (redirect → spam) | 1 (Network Heresy) | ~5/584 (1%) |

### Phát hiện P7.U1 — URL gặp mới

| ID | Mức | File | URL | Action |
|---|---|---|---|---|
| P7.U1a | MED | `9.5 hw-offload-switchdev-asap2-doca.md` | `https://docs.nvidia.com/doca/sdk/ovs-doca/index.html` (404) | Thay bằng NVIDIA DOCA 3.0 docs hoặc Wayback |
| P7.U1b | MED | `2.4 ethane-the-direct-ancestor.md` | `https://opennetworking.org/news-and-events/press-releases/open-networking-foundation-established/` (404) | Thay bằng Wayback Machine hoặc `https://opennetworking.org/press-release/` chính xác |
| P7.U1c | MED | `README.md` + `14.1 tofino-pisa-silicon.md` | `https://p4.org/specs/` (404) | Thay bằng `https://p4.org/p4-spec/` hoặc GitHub `p4lang/p4-spec` |

Cộng với Phase 6 P6.U1a/b/c:
- Total 6 dead URL finding across curriculum.
- Breakdown: 3 paper (Ethane, 4D, Network Heresy migration) + 3 product docs (NVIDIA DOCA, ONF press release, P4 specs index).

---

## 6. Reading path consistency

### 6.1. 6 reading paths trong README (lines 85-94)

| # | Path | Scope check |
|---|---|---|
| 1 | Linear foundation 0→1→...→19 | 50-80 giờ. Block 0+I+II+III+IV+V+VI+VII+VIII+IX+X+XI+XII+XIII+XVII+XVIII+XIX. Không kể Block XX + XIV-XVI. |
| 2 | Historian 0→1→...→7 | Stop ở Block VII. Bỏ qua code-heavy. |
| 3 | OVS-only 0→1→4→8→9→10→11 | Bỏ OVN. |
| 4 | OVN-focused 0→3→5.1→9→11→13→17→18→19 | Path OVN standalone. |
| 5 | Incident responder 0→13→17→18→19 | Advanced đi thẳng. |
| 6 | Expert Extension: P4 / K8s / Performance | 3 parallel tracks XIV/XV/XVI. |

Quan sát:
- Block XX Operational Excellence không xuất hiện trong bất kỳ reading path nào.
- Part 9.26/9.27 forensic + 20.x playbook là mission core per user 2026-04-24 directive nhưng không có reading path rõ.

### Phát hiện P7.P1

| ID | Mức | Mô tả |
|---|---|---|
| P7.P1 | MED | 6 reading paths không cover Block XX Operational Excellence (7 file mới từ Phase G). Cần thêm path 7: "Operator daily runbook" 20.0→20.3→20.4→20.2→20.1→20.5→20.6 hoặc integrate Block XX vào path 1 + 5. |

### 6.2. Dependency graph Mermaid (README lines 26-77)

Graph trỏ P0-P19 + P14-P16 Expert. Block XX không có node. Cần add `P20[Part 20: Ops Excellence]` với dependencies `P9 → P20 → P13` (cross-cutting ops).

### Phát hiện P7.P2

| ID | Mức | Mô tả |
|---|---|---|
| P7.P2 | MED | Dependency graph Mermaid không có Block XX node. Cần add 1 node + 2 arrow (P9→P20, P13→P20) để visualize Operations Excellence placement. |

---

## 7. Memory file coherence

### 7.1. Cross-reference trong memory/

| File | Updated for rev 4? | Note |
|---|---|---|
| `session-log.md` | Có (S59) | Log hiện tại |
| `file-dependency-map.md` | **Partial** (Block VII/VIII/XII/XIV/XV 0% coverage) | P7.D1 |
| `haproxy-series-state.md` | N/A | HAProxy series (sister) |
| `sdn-series-state.md` | **KHÔNG TỒN TẠI** (P1.M1) | Cần tạo |
| `lab-verification-pending.md` | Outdated (C1a pre-v3.1) | Cần revisit sau lab host available |
| `experiment-plan.md` | OK | Phase A→E plan |
| `pre-release-audit-2026-04-24.md` | S60 log | Latest official audit |
| `sdn-onboard-audit-*.md` | 3 log dates | Có thể rollup |

### Phát hiện P7.M1

| ID | Mức | Mô tả |
|---|---|---|
| P7.M1 | MED | Thiếu `memory/sdn-series-state.md` (đã flag P1.M1). Rule 5 Session Handoff Protocol yêu cầu tracking file tương tự haproxy-series-state.md. |
| P7.M2 | LOW | 3 audit log cùng prefix `sdn-onboard-audit-*` + 2 phase-*-audit. Nên tạo `memory/audit-index.md` làm TOC. |

---

## 8. Phát hiện tổng hợp Phase 7

### 8.1. Thống kê

| Mức | Số phát hiện | Chi tiết |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 1 | P7.D1 (dependency map 5 block 0% coverage) |
| MED | 7 | P7.T1, P7.D2, P7.U1a, P7.U1b, P7.U1c, P7.P1, P7.P2, P7.M1 |
| LOW | 2 | P7.R1, P7.M2 |
| PASS | 3 | TOC integrity (0 phantom 0 orphan), anchor links (0 broken), cross-ref (0 true broken) |

### 8.2. Danh sách phát hiện

| ID | Mức | Mô tả |
|---|---|---|
| P7.T1 | MED | Parent `README.md` chỉ link 3 Part advanced + sdn-onboard README. Cần update với Block XX + Expert Extension summary. |
| P7.D1 | HIGH | 5 block (VII/VIII/XII/XIV/XV) 0% coverage trong dependency map. Total 19 file missing entirely. |
| P7.D2 | MED | 44/116 file (37,9%) thiếu map entry. Backfill mass v3.1.1. |
| P7.U1a | MED | `9.5` dead link NVIDIA DOCA ovs-doca/index.html. |
| P7.U1b | MED | `2.4` dead link ONF press release. |
| P7.U1c | MED | `README.md` + `14.1` dead link p4.org/specs/. |
| P7.P1 | MED | 6 reading paths thiếu Block XX coverage. Thêm path 7 "Operator daily runbook". |
| P7.P2 | MED | Dependency graph Mermaid thiếu Block XX node. |
| P7.M1 | MED | Thiếu `memory/sdn-series-state.md`. Rule 5 violation. |
| P7.R1 | LOW | 15 section refs dùng "Part X.Y.Z" thay vì "§X.Y.Z". Terminology cosmetic. |
| P7.M2 | LOW | 5 audit log in `memory/` cùng prefix. Nên tạo `audit-index.md`. |

### 8.3. Summary theo trụ cột

| Trụ cột | Coherence assessment |
|---|---|
| #1 Kiến trúc | Reading path OK. Dependency graph thiếu Block XX (P7.P2). Cross-ref structural OK. |
| #2 Lịch sử | 3 dead paper URL + README Bibliography outdated (P6.U1 + P7.U1 combined). |
| #3 CLI tools | Block XX visible trong 20.x nhưng không có reading path dedicated (P7.P1). |
| #4 Diễn đạt | Parent README thiếu đoạn tóm tắt Block XX (P7.T1). |
| #5 Debug | 9.26 forensic + 9.27 debug + 9.14 incident cross-ref OK giữa nhau. |

---

## 9. Đề xuất action

### 9.1. v3.1.1 patch (4-6 giờ total)

**Priority 1 — Dependency map backfill (P7.D1 + P7.D2, 2-3 giờ):**
- Backfill 44 file entry vào `memory/file-dependency-map.md`. Focus 5 block 0% trước (19 file).
- Template: mỗi entry liệt kê prerequisites + related files trong cùng block.

**Priority 2 — Dead URL fix (P7.U1a/b/c + P6.U1a/b/c, 1-2 giờ):**
- Network Heresy: `networkheresy.com` → `networkheresy.wordpress.com` (3 file)
- Stanford CS244 Ethane: Wayback Machine hoặc ACM DOI
- Princeton 4D: Wayback Machine hoặc ACM CCR DOI
- NVIDIA DOCA: update link NVIDIA Docs 3.0 hoặc Wayback
- ONF press release: Wayback Machine hoặc opennetworking.org/press/
- p4.org/specs → `https://github.com/p4lang/p4-spec`

**Priority 3 — TOC/Heading sync (P7.T1 + P1.C1-C3, 30 phút):**
- README heading count fix: Block IX 27→28, Block XX 6→7, tổng block 20.
- Parent `README.md` update: thêm Block XX + XIV-XVI summary với link sdn-onboard/README.md.

**Priority 4 — Reading path enhancement (P7.P1 + P7.P2, 30 phút):**
- Add reading path 7 "Operator daily runbook" (Block XX focus).
- Add Block XX node + arrow vào Mermaid graph.

**Priority 5 — Memory file cleanup (P7.M1 + P7.M2, 30 phút):**
- Create `memory/sdn-series-state.md` template.
- Create `memory/audit-index.md` TOC.

### 9.2. v3.2 content expansion (already cover per Phase 4)

---

## 10. Kết luận Phase 7

Cross-cutting coherence là **tốt** ở mức structural (TOC, anchor, cross-ref) nhưng **yếu** ở dependency map + URL integrity + memory tracking:

- Strong: TOC 100% filesystem consistent, 0 phantom/orphan, 0 broken anchor.
- Medium: 6 dead URL (3 paper + 3 product docs). Parent README rev 2 era.
- Weak: 44/116 file thiếu dependency map (37,9%). Missing sdn-series-state.md.

Không có CRITICAL finding. 1 HIGH (P7.D1 dependency coverage gap) có giải pháp backfill 2-3 giờ. Các MED finding khác đều fix được trong 1-2 giờ/mỗi cái.

Master report Phase 9 sẽ đề xuất v3.1.1 sprint Priority 1-5 tổng ~5-6 giờ để đóng toàn bộ gap Phase 7.

---

**Next:** Phase 8 Anatomy + Guided Exercise + Capstone Sampling. Random sample 30 Anatomy block + 10 GE POE + 5 Capstone POE.
