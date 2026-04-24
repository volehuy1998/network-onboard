# Audit 2026-04-25 — Phase 1 Báo cáo kiểm kê (Inventory & Baseline)

> **Branch:** `docs/sdn-foundation-rev2` · **HEAD:** `0fa0687` · **Tag:** `v3.1-OperatorMaster` (2026-04-24)
> **Phạm vi audit:** `sdn-onboard/**/*.md` trừ `doc/`, `_templates/`, `images/`, `references/`
> **Skill kích hoạt Phase 1:** search-first (inventory), professor-style (formatting)

---

## 1. Tổng quan baseline

| Chỉ số | Giá trị |
|---|---|
| Tổng số file `.md` content (trừ README) | **115** |
| README.md (sdn-onboard/) | 1 |
| Tổng cộng | **116** |
| Tổng số dòng content (bao gồm README) | **52.649** |
| Tổng số dòng content (trừ README) | 52.119 |
| Dòng trung bình/file | 453 |
| File lớn nhất | `20.2 - ovn-troubleshooting-deep-dive.md` (1.627 dòng) |
| File nhỏ nhất | `2.0 - dcan-open-signaling-gsmp.md` (140 dòng) |
| File ≥ 1.000 dòng | 11 file |
| File < 200 dòng | 18 file |

Baseline này khớp với tuyên bố trong `CHANGELOG.md` và `CLAUDE.md` Current State (116 file, ~52,6K dòng).

---

## 2. Phân bố theo Block

| Block | Tên | Số file | Tổng dòng | Trung bình | Trạng thái |
|---|---|---|---|---|---|
| 0 | Orientation | 3 | 830 | 277 | Khớp TOC |
| I | Động lực ra đời SDN | 3 | 736 | 245 | Khớp TOC |
| II | Tiền thân SDN | 5 | 1.077 | 215 | Khớp TOC |
| III | Khai sinh OpenFlow | 3 | 973 | 324 | Khớp TOC |
| IV | OpenFlow evolution | 10 | 5.477 | 548 | Khớp TOC |
| V | Mô hình SDN thay thế | 3 | 983 | 328 | Khớp TOC |
| VI | Mô hình SDN mới nổi | 2 | 652 | 326 | Khớp TOC |
| VII | Controller ecosystem | 6 | 1.498 | 250 | Khớp TOC |
| VIII | Linux networking primer | 4 | 837 | 209 | Khớp TOC |
| IX | OpenvSwitch internals | **28** | **13.104** | 468 | Cảnh báo: TOC heading nói 27 file |
| X | OVSDB management | 7 | 1.995 | 285 | Khớp TOC |
| XI | Overlay encapsulation | 5 | 2.196 | 439 | Khớp TOC |
| XII | SDN trong Data Center | 3 | 483 | 161 | Khớp TOC |
| XIII | OVN foundation | 14 | 4.574 | 327 | Khớp TOC |
| XIV | P4 Programmable (Expert) | 3 | 1.354 | 451 | Khớp TOC |
| XV | Service Mesh + K8s (Expert) | 3 | 1.090 | 363 | Khớp TOC |
| XVI | Kernel+DPDK (Expert) | 3 | 1.630 | 543 | Khớp TOC |
| XVII | OVN L2 FDB advanced | 1 | 1.196 | 1.196 | Khớp TOC |
| XVIII | OVN ARP BUM advanced | 1 | 499 | 499 | Khớp TOC |
| XIX | OVN Multichassis PMTUD advanced | 1 | 1.389 | 1.389 | Khớp TOC |
| XX | Operational Excellence | **7** | **7.999** | 1.143 | Cảnh báo: TOC heading nói 6 file |
| README | — | 1 | 530 | — | — |
| **Tổng** | | **116** | **52.649** | — | — |

### Phát hiện Phase 1 — coherence

| ID | Mức | Mô tả |
|---|---|---|
| P1.C1 | MED | README dòng 183: "Block IX (Part 9, **27 file**)". Thực tế 28 file (9.0-9.27 = 28). Lệch 1. |
| P1.C2 | MED | README dòng 322: "Block XX Operational Excellence (Part 20, **6 file**)". Thực tế 7 file (20.0-20.6 = 7). Lệch 1. |
| P1.C3 | MED | README dòng 97: heading "13 Block foundation + 3 Block Expert Extension + 3 Part advanced". Không kể Block XX. Tổng thực = 13+3+3+1 = 20 block. |
| P1.C4 | LOW | README dòng 3 + `CLAUDE.md` Current State ghi "116 file". Khớp thực tế. |

Nguyên nhân: Block IX thêm Part 9.27 session S37b (Phase G.1.2) và Block XX thêm Part 20.6 session S59 (Phase G.4) sau khi viết README heading. Heading không cập nhật. Phase 7 sẽ fix.

---

## 3. Top 15 file lớn nhất (≥ 800 dòng)

Chứng minh tập trung của curriculum vào CLI tools, forensic case study và operational playbook. Khớp trụ cột kỹ năng #3 + #5.

| Hạng | File | Dòng | Block | Loại nội dung |
|---|---|---|---|---|
| 1 | `20.2 - ovn-troubleshooting-deep-dive.md` | 1.627 | XX | CLI + Output |
| 2 | `20.3 - ovn-daily-operator-playbook.md` | 1.554 | XX | CLI + Playbook |
| 3 | `4.9 - openflow-action-catalog.md` | 1.544 | IV | Architecture reference |
| 4 | `9.14 - incident-response-decision-tree.md` | 1.494 | IX | Debug playbook |
| 5 | `20.4 - ovs-daily-operator-playbook.md` | 1.422 | XX | CLI + Playbook |
| 6 | `9.4 - ovs-cli-tools-playbook.md` | 1.406 | IX | CLI reference |
| 7 | `19.0 - ovn-multichassis-binding-and-pmtud.md` | 1.389 | XIX | Forensic case study |
| 8 | `20.1 - ovs-ovn-security-hardening.md` | 1.334 | XX | Security + audit |
| 9 | `17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | 1.196 | XVII | Forensic case study |
| 10 | `9.26 - ovs-revalidator-storm-forensic.md` | 1.185 | IX | Forensic case study |
| 11 | `9.11 - ovs-appctl-reference-playbook.md` | 1.170 | IX | CLI reference |
| 12 | `9.25 - ovs-flow-debugging-ofproto-trace.md` | 1.046 | IX | Debug + Output |
| 13 | `4.8 - openflow-match-field-catalog.md` | 926 | IV | Architecture reference |
| 14 | `9.2 - ovs-kernel-datapath-megaflow.md` | 878 | IX | Architecture deep-dive |
| 15 | `11.4 - ipsec-tunnel-lab.md` | 871 | XI | Lab + output |

Tỉ lệ file lớn thuộc trụ cột CLI + Output + Forensic: 12/15 (80%). Phù hợp mục tiêu training của user.

---

## 4. Top 15 file nhỏ nhất (≤ 180 dòng)

Các file nhỏ thường là skeleton-refined theo Rule 10 Architecture-First Doctrine. Cần xác minh ở Phase 4 có nên expand sang content phase không.

| Hạng | File | Dòng | Block | Ghi chú |
|---|---|---|---|---|
| 1 | `2.0 - dcan-open-signaling-gsmp.md` | 140 | II | Skeleton historical |
| 2 | `13.4 - br-int-architecture-and-patch-ports.md` | 142 | XIII | Cảnh báo: kiến trúc core OVN nhưng ngắn |
| 3 | `12.0 - dc-network-topologies-clos-leaf-spine.md` | 143 | XII | Skeleton |
| 4 | `0.0 - how-to-read-this-series.md` | 148 | 0 | Meta |
| 5 | `9.8 - flow-monitoring-sflow-netflow-ipfix.md` | 152 | IX | Cảnh báo: Ops Part mà ngắn |
| 6 | `13.0 - ovn-announcement-2015-rationale.md` | 153 | XIII | Historical |
| 7 | `9.7 - port-mirroring-and-packet-capture.md` | 154 | IX | Cảnh báo: Ops Part mà ngắn |
| 8 | `11.2 - bgp-evpn-control-plane-overlay.md` | 157 | XI | Skeleton |
| 9 | `7.2 - onos-service-provider-scale.md` | 158 | VII | Controller landscape |
| 10 | `12.2 - micro-segmentation-service-chaining.md` | 162 | XII | Skeleton |
| 11 | `9.6 - bonding-and-lacp.md` | 162 | IX | Cảnh báo: Ops Part mà ngắn |
| 12 | `9.12 - upgrade-and-rolling-restart.md` | 172 | IX | Cảnh báo: Ops Part critical mà ngắn |
| 13 | `9.10 - tls-pki-hardening.md` | 174 | IX | Security |
| 14 | `12.1 - dc-overlay-integration-vxlan-evpn.md` | 178 | XII | Skeleton |
| 15 | `7.1 - opendaylight-architecture.md` | 180 | VII | Controller landscape |

### Phát hiện Phase 1 — dưới ngưỡng content

| ID | Mức | File | Ghi chú |
|---|---|---|---|
| P1.S1 | MED | `9.6` / `9.7` / `9.8` / `9.10` / `9.12` | 5 Part Ops Block IX < 180 dòng. Rất ngắn so với operator playbook khác (9.4 = 1.406 dòng, 9.11 = 1.170 dòng). Không cân đối. Cần cân nhắc expand trong Phase I OVS tier 2. |
| P1.S2 | MED | `13.4` | Kiến trúc core OVN (br-int + patch port) mà 142 dòng. Chắc chắn thiếu content về integration bridge internals. |
| P1.S3 | LOW | Block XII toàn bộ | 3/3 file < 180 dòng. Block này nhỏ cục bộ nhất curriculum. |

---

## 5. Độ phủ của `memory/file-dependency-map.md`

**Tổng số SDN entry trong dependency map:** 72 đường dẫn unique (bao gồm cả `sdn-onboard/doc/`, `sdn-onboard/0.0`, v.v.)

**Tổng số file SDN content thực tế:** 116 file

**Coverage gap:**

| Chỉ số | Giá trị |
|---|---|
| File có trong map | 72 (bao gồm một số reference tới `doc/`) |
| File content thực có map | ~72 (62,1%) |
| File content KHÔNG có map | **44 file (37,9%)** |

### 44 file thiếu mapping (ordered by block)

**Block IV (2 file):** 4.8, 4.9
**Block V (2 file):** 5.1, 5.2
**Block VII (6 file):** 7.0, 7.1, 7.2, 7.3, 7.4, 7.5 (toàn bộ)
**Block VIII (4 file):** 8.0, 8.1, 8.2, 8.3 (toàn bộ)
**Block IX (7 file):** 9.16, 9.17, 9.18, 9.19, 9.20, 9.21, 9.23
**Block X (5 file):** 10.0, 10.3, 10.4, 10.5, 10.6
**Block XI (2 file):** 11.0, 11.2
**Block XII (3 file):** 12.0, 12.1, 12.2 (toàn bộ)
**Block XIII (3 file):** 13.0, 13.9, 13.13
**Block XIV (3 file):** 14.0, 14.1, 14.2 (toàn bộ)
**Block XV (3 file):** 15.0, 15.1, 15.2 (toàn bộ)
**Block XVI (2 file):** 16.0, 16.2
**Block XX (2 file):** 20.5, 20.6

### Phát hiện Phase 1 — dependency map gap

| ID | Mức | Mô tả |
|---|---|---|
| P1.D1 | **HIGH** | 37,9% file content thiếu mapping. Vi phạm Rule 2 (Cross-File Sync). Khi sửa các file này, không có cách nào tra related files. |
| P1.D2 | MED | Toàn bộ Block VII (6 file), Block VIII (4 file), Block XII (3 file), Block XIV/XV (6 file) thiếu. Phần lớn curriculum tạo từ Phase B (S12-S15) và Phase F (S36) chưa được backfill vào map. |
| P1.D3 | MED | Block X có 5/7 file thiếu (core 10.0 + extended 10.3-10.6). Nguy hiểm vì đây là OVSDB backbone, cross-ref rất nhiều. |
| P1.D4 | LOW | 20.5 + 20.6 (forensic case study + retrospective) thiếu. Viết mới nhất session 58+59 Phase G. |

Remediation khuyến nghị (Phase 7): backfill 44 entry vào `memory/file-dependency-map.md` bằng batch update. Estimate 30-45 phút work.

---

## 6. Sự tồn tại của file memory hỗ trợ audit

| File | Tồn tại? | Mục đích |
|---|---|---|
| `memory/session-log.md` | Có | Log session |
| `memory/file-dependency-map.md` | Có (298 dòng) | Cross-file sync (Rule 2) |
| `memory/haproxy-series-state.md` | Có | HAProxy state (sister series) |
| `memory/sdn-series-state.md` | **KHÔNG** | Rule 5 Session Handoff Protocol yêu cầu file này |
| `memory/lab-verification-pending.md` | Có | C1b lab host chờ |
| `memory/experiment-plan.md` | Có | Experiment plan A→E |
| `memory/phase-f-audit-2026-04-23.md` | Có | Phase F audit log |
| `memory/phase-h-progress.md` | Có | Phase H tracker |
| `memory/pre-release-audit-2026-04-24.md` | Có | S60 audit log |
| `memory/sdn-onboard-audit-2026-04-23.md` | Có | Phase D audit log |
| `memory/sdn-onboard-audit-2026-04-24.md` | Có | Phase H audit log |
| `memory/fact-check-audit-2026-04-22.md` | Có | Phase E fact-check log |

### Phát hiện Phase 1 — missing memory file

| ID | Mức | Mô tả |
|---|---|---|
| P1.M1 | MED | `memory/sdn-series-state.md` không tồn tại dù Rule 5 yêu cầu tương tự như haproxy-series-state.md. Không có file tracking trạng thái Part SDN, chỉ có ghi lỏng trong CLAUDE.md Current State. |
| P1.M2 | LOW | Nhiều audit log chồng chéo (3 file sdn-onboard-audit-*, 1 pre-release-audit, 2 phase-*-audit, 1 fact-check-audit). Gây khó định vị. Nên tạo `memory/audit-index.md` làm TOC. |

---

## 7. Thống kê loại nội dung

Phân loại sơ bộ dựa trên tên file:

| Loại | Số file | % | Mục tiêu training |
|---|---|---|---|
| Architecture deep-dive | 22 | 19% | Trụ cột #1 Kiến trúc |
| Historical narrative | 9 | 8% | Trụ cột #2 Lịch sử |
| CLI + Output interpretation | 18 | 16% | Trụ cột #3 Thao tác |
| Engagement pedagogy (Part 0.x + skeleton) | 12 | 10% | Trụ cột #4 Diễn đạt |
| Debug + Forensic | 13 | 11% | Trụ cột #5 Debug |
| Operations playbook | 18 | 16% | Trụ cột #3 + #5 |
| Lab + Exercise | 6 | 5% | Trụ cột #5 + lab verify |
| Expert Extension (XIV-XVI) | 9 | 8% | Optional track |
| Conceptual foundations | 9 | 8% | Cross-cutting |
| **Tổng** | **116** | **100%** | — |

Đánh giá: curriculum phân bố cân đối giữa 5 trụ cột, không bị lệch về một hướng. Trụ cột #3 (CLI + Output) có 36 file (31%). Cao nhất. Phù hợp mục tiêu user đặt ra là "thành thạo sử dụng và hiểu output".

---

## 8. README.md TOC coverage

Đã đối chiếu từng file trong `sdn-onboard/` với TOC README.md. Kết quả:

| Chỉ số | Giá trị |
|---|---|
| File trong TOC | 115 (không kể README.md) |
| File thực tế | 115 |
| Phantom references (TOC có, file không có) | **0** |
| Orphan files (file có, TOC không có) | **0** |

PASS. TOC và filesystem 100% consistent ở level link. Các issue P1.C1/C2/C3 chỉ liên quan đếm heading, không phải missing link.

---

## 9. Tóm tắt phát hiện Phase 1

### Thống kê

| Mức | Số phát hiện | Chi tiết |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 1 | P1.D1 (dependency map gap 37,9%) |
| MED | 7 | P1.C1, P1.C2, P1.C3, P1.S1, P1.S2, P1.D2, P1.D3, P1.M1 |
| LOW | 3 | P1.C4, P1.S3, P1.D4, P1.M2 |

### Điểm cần hành động ngay

1. **P1.D1 HIGH**: Backfill 44 file vào `memory/file-dependency-map.md` (Phase 7)
2. **P1.C1/C2/C3 MED**: Sửa README heading count cho Block IX (27→28), Block XX (6→7), tổng block count (13+3+3→13+3+3+1)
3. **P1.M1 MED**: Tạo `memory/sdn-series-state.md` tương tự haproxy-series-state.md

### Điểm defer sang Phase 4-5

1. **P1.S1 MED**: 5 Part Block IX Ops ngắn (9.6/9.7/9.8/9.10/9.12) sẽ được verify trong Phase 5 CLI Tools audit
2. **P1.S2 MED**: `13.4 br-int` verify Phase 4 Architecture audit
3. **P1.S3 LOW**: Block XII 3 file defer Phase I content expansion

---

## 10. Kết luận Phase 1

Curriculum v3.1-OperatorMaster 116 file 52.649 dòng đứng vững ở cấp filesystem + TOC. Không có phantom references, không có orphan files. Tuy nhiên:

- Rule 2 (Cross-File Sync) đang ở trạng thái yếu với 37,9% file thiếu mapping.
- 3 heading count sai trong README (Block IX/XX/tổng block) là hệ quả cập nhật chậm sau S37b + S59.
- 5 Part Block IX Ops ngắn là tín hiệu cần xem xét expand trong Phase I v3.2.
- Missing `sdn-series-state.md` là gap so với pattern haproxy-series-state.md.

Phase 1 đã xác lập được baseline rõ ràng cho các Phase audit sâu tiếp theo. Tất cả finding được numbered (P1.X.N) để trace trong master report Phase 9.

---

**Next:** Phase 2 Structural Integrity Sweep. Rule 9 null byte + Rule 13 em-dash density + Rule 14 source citation spot-check.
