# Audit 2026-04-25 — Phase 5 Báo cáo CLI Tools & Operations Deep Audit

> **Phạm vi:** 12 file — Block XX (7 file: 20.0-20.6) + Block IX CLI/forensic (5 file: 9.4, 9.11, 9.14, 9.26, 9.27)
> **Trụ cột kỹ năng:** #3 Thành thạo CLI tool + đọc hiểu output
> **Skills kích hoạt:** search-first (tool verify), fact-checker (CLI syntax), web-fetcher (man page URL), document-design (Anatomy Template A quality)

---

## 1. Tổng quan

### 1.1. Quy mô cluster CLI/Ops

| Block | File | Tổng dòng | Trung bình |
|---|---|---|---|
| XX Operations | 7 | 7.999 | 1.143 |
| IX CLI + forensic | 5 | 6.925 | 1.385 |
| **Tổng** | **12** | **14.924** | **1.244** |

28% curriculum (14.924 / 52.649 dòng) tập trung ở 12 file CLI/Ops. Đây là cluster lớn nhất theo tỷ trọng dòng/file (trung bình 1.244 dòng so với toàn curriculum trung bình 453).

### 1.2. Cấu trúc metric 12 file

| File | Dòng | CodeBlk | OutBlk | Anatomy (verbose) | Anatomy Table | ManRefs |
|---|---|---|---|---|---|---|
| `20.0 - systematic-debugging.md` | 789 | 31 | 27 | 0 | 0 | 6 |
| `20.1 - security-hardening.md` | 1.335 | 83 | 34 | 0 | 0 | 3 |
| `20.2 - troubleshooting-deep-dive.md` | 1.628 | 69 | 44 | 4+ | 4 | 34 |
| `20.3 - ovn-daily-playbook.md` | 1.555 | 88 | 61 | 20+ | 20+ | 18 |
| `20.4 - ovs-daily-playbook.md` | 1.423 | 73 | 18+ | 15+ | 15+ | 19 |
| `20.5 - ovn-forensic-cases.md` | 843 | 25 | 12 | 5 | 5 | 2 |
| `20.6 - retrospective-2007-2024.md` | 433 | 1 | 0 | 0 | 0 | 0 |
| `9.4 - ovs-cli-playbook.md` | 1.407 | 38 | 7+ | 12 | 0 (dùng `từng dòng` variant) | 36 |
| `9.11 - ovs-appctl-reference.md` | 1.171 | 50 | 3+ | 22 | 0 | 13 |
| `9.14 - incident-decision-tree.md` | 1.495 | 70 | 16 | 6 | 2 | 3 |
| `9.26 - revalidator-forensic.md` | 1.186 | 44 | 33 | 2 | 2 | 13 |
| `9.27 - packet-journey-e2e.md` | 660 | 23 | 8 | 0 | 0 | 5 |

Ghi chú: "Anatomy (verbose)" đếm occurrences của bold pattern `**Anatomy ...:**`. "Anatomy Table" đếm bảng có header cột `| Line pattern | Giá trị mẫu | Ý nghĩa | Dấu hiệu đáng lưu ý |`. Mỗi file có thể dùng 1 style hoặc cả 2.

### 1.3. Phân loại theo Anatomy Template A adoption

**Exemplar (Anatomy ≥ 10 block):**
- 9.11 (22 Anatomy block). Reference playbook strongest.
- 9.4 (12 Anatomy block with line-by-line breakdown). CLI tools playbook.
- 20.3 (20+ Anatomy + table variants). OVN daily operator.
- 20.4 (15+ Anatomy table variants). OVS daily operator.

**Strong (Anatomy 2-9 block):**
- 20.2 (4 explicit Anatomy + many bold anatomy). OVN troubleshoot.
- 20.5 (5 Anatomy). OVN forensic case.
- 9.14 (6 Anatomy Template A per scenario). Incident decision tree.
- 9.26 (2 Anatomy + 33 output block). Revalidator forensic.

**Missing (0 Anatomy):**
- 20.0 systematic debugging (0 Anatomy). Foundation Block XX file.
- 20.1 security hardening (0 Anatomy). Despite 83 code block.
- 20.6 retrospective (0 Anatomy). Historical narrative, không cần Anatomy.
- 9.27 packet journey (0 Anatomy). Despite 23 code block cross-stack.

---

## 2. Sample quality deep-dive

### 2.1. `20.3 - ovn-daily-operator-playbook.md` (1.555 dòng) — EXEMPLAR

**Quan sát header + TOC:**
- Header block: 5 offline + 5 online man page reference.
- 5 Bloom objectives (Apply/Understand/Analyze/Apply/Create).
- 53 subsection level `###`. 10 task category × 4-8 subcommand.
- 5 workflow end-to-end (new tenant, teardown, maintenance, audit, backup).

**Quan sát Anatomy pattern (sample §20.3.1.1 `ovn-nbctl show`):**
1. "Bối cảnh khi chạy" paragraph. 1-2 câu lý do.
2. "Command và output" markdown code block với real sample (MAC/IP mock).
3. "Anatomy block cấu trúc" markdown table với 4 cột: `Line pattern | Giá trị mẫu | Ý nghĩa | Dấu hiệu đáng lưu ý`.
4. "Kịch bản bẻ gãy" bullet list 3-5 failure scenarios.
5. "Upstream nguồn" man page link.

Đây là **template xuất sắc** nên được apply đồng loạt cho 20.0/20.1/20.4/9.27 để thống nhất style.

### 2.2. `9.11 - ovs-appctl-reference-playbook.md` (1.171 dòng) — EXEMPLAR

**Quan sát:**
- Header với 4 offline source + 5 upstream reference (man page + OVS docs).
- Bloom 5 objective: Liệt kê / Áp dụng / Đọc hiểu / Chẩn đoán / Tổng hợp.
- 18 nhóm target `ovs-appctl` với 22 Anatomy block.
- TOC đầy đủ: grammar → introspection → L2 → link agg → STP → BFD/CFM → ofproto → dpctl/dpif → dpif-netdev → tunnel → upcall/revalidator → OVSDB cluster.
- Phần 9.11.0 Grammar + target discovery cung cấp mental model trước deep-dive.

Đây là **reference strongest** trong curriculum cho CLI runtime introspection. Output interpretation đầy đủ với "red flag" signal cho từng counter.

### 2.3. `20.1 - ovs-ovn-security-hardening.md` (1.335 dòng) — WEAKNESS

**Quan sát:**
- 0 Anatomy block explicit marker.
- 83 code block nhưng không có "Anatomy block cấu trúc" table sau output.
- 3 interpretation marker (red flag/cảnh báo/critical signal). Thấp.
- 3 man page reference. Thấp so với 20.3 (18) hoặc 9.4 (36).

Lý do: 20.1 tập trung vào security policy/audit script chứ không phải observational CLI. Nhưng khi có output (ACL log, conntrack event, cert expiry check), vẫn cần Anatomy để đọc hiểu. Gap này thể hiện trong trụ cột #3.

### 2.4. `20.0 - ovs-ovn-systematic-debugging.md` (789 dòng) — WEAKNESS

**Quan sát:**
- 0 Anatomy block marker.
- 31 code block + 27 output block. High ratio code.
- 6 man page reference. OK.
- 1 interpretation marker. Thấp.

20.0 là foundation Block XX. Methodology 5-layer isolation, ovn-trace/ofproto/trace/ovn-detrace. Nhưng không có Anatomy block giải thích output của từng tool trace. Cần retrofit.

### 2.5. `9.27 - ovs-ovn-packet-journey-end-to-end.md` (660 dòng) — WEAKNESS

**Quan sát:**
- 0 Anatomy block.
- 23 code block, 8 output block.
- 5 man page.
- 5 POE (từ Phase 4 scan).

9.27 là Phase G.1.2 cross-stack debug playbook. Structural nature khác: nhiều fault injection scenario, không phải reference command. Nhưng vẫn nên có Anatomy cho `ovn-trace` output + `ofproto/trace` output + Geneve TLV parse output.

---

## 3. Phân tích từng file

### 3.1. Block XX Operations (7 file)

| File | Đánh giá | Điểm mạnh | Điểm yếu |
|---|---|---|---|
| 20.0 systematic-debugging | **MED** | 5-layer isolation methodology rõ ràng; 27 output block | 0 Anatomy; thiếu output interpretation table |
| 20.1 security-hardening | **MED** | 83 code block (rất nhiều CLI scenario); 4-layer audit trail architecture | 0 Anatomy; 3 man page reference (thấp) |
| 20.2 troubleshoot-deep-dive | **STRONG** | 44 output block; 34 man page reference; 4 Anatomy table; 16 bold Anatomy; 3-layer debug framework | Các bold Anatomy không đồng nhất style với Anatomy table |
| 20.3 ovn-daily-playbook | **STRONG** | 61 output block; 20+ Anatomy table; 18 man page; 5 workflow end-to-end | — |
| 20.4 ovs-daily-playbook | **STRONG** | 15+ Anatomy table; 19 man page; 4-CLI layer distinction | Ít hơn 20.3 về workflow count (tail end chưa expand) |
| 20.5 ovn-forensic-cases | **STRONG** | 3 case study với Anatomy + remediation 4-tier; cross-case takeaway | Chỉ 2 man page reference. Offline focus |
| 20.6 retrospective | N/A | Narrative historical 40 section | 0 CLI/Anatomy (by design). Assess ở Phase 6 |

### 3.2. Block IX CLI/forensic (5 file)

| File | Đánh giá | Điểm mạnh | Điểm yếu |
|---|---|---|---|
| 9.4 ovs-cli-playbook | **STRONG** | 12 Anatomy `từng dòng` variant; 38 code block; 36 man page; 6-layer troubleshooting | — |
| 9.11 ovs-appctl-reference | **EXEMPLAR** | 22 Anatomy; 50 code block; 13 man page; 18 target group × Anatomy | — |
| 9.14 incident-decision-tree | **STRONG** | 6 Anatomy; 70 code block; 16 output; 5 Capstone + 5 POE (Phase 4); 20-symptom matrix | 3 man page reference hơi thấp |
| 9.26 revalidator-forensic | **STRONG** | 33 output block; 13 man page; 2 Anatomy + 3 case study | References section heading non-standard |
| 9.27 packet-journey-e2e | **MED** | 5 POE + 1 Capstone; 3-tier diagnostic framework | 0 Anatomy; 5 man page reference |

---

## 4. Man page + upstream citation coverage

Trụ cột #3 yêu cầu người học biết đường link tới man page chính thức. Phân tích ManRefs count:

| File | ManRefs | Đánh giá |
|---|---|---|
| 9.4 | 36 | **Xuất sắc** |
| 20.2 | 34 | **Xuất sắc** |
| 20.4 | 19 | Tốt |
| 20.3 | 18 | Tốt |
| 9.26 | 13 | Tốt |
| 9.11 | 13 | Tốt |
| 20.0 | 6 | Trung bình |
| 9.27 | 5 | Trung bình |
| 20.1 | 3 | **Thấp** (security file nên có nhiều man page security ovs-pki, openssl) |
| 9.14 | 3 | **Thấp** (incident tree mà chỉ 3 man page) |
| 20.5 | 2 | **Thấp** (forensic case study) |
| 20.6 | 0 | N/A (retrospective narrative) |

**Phát hiện P5.M1 MED:** 20.1 security, 9.14 incident, 20.5 forensic có man page reference thấp (2-3). Cần backfill citation tới `ovs-pki(8)`, `ovn-appctl(8)`, `ovs-fields(7)`, `ovs-actions(7)`.

---

## 5. CLI command verification (spot-check)

Phương pháp: sample 10 CLI command từ 20.3 + 20.4 + 9.11 + 9.14. Verify exist trong man page hoặc docs.openvswitch.org.

| # | CLI command | File | Source verify |
|---|---|---|---|
| 1 | `ovn-nbctl show` | 20.3 | man `ovn-nbctl(8)`. Có section `show` |
| 2 | `ovn-sbctl show` | 20.3 | man `ovn-sbctl(8)`. Có section `show` |
| 3 | `ovn-sbctl --bare --columns=chassis_name,nb_cfg_timestamp list Chassis_Private` | 20.3 | `ovn-sbctl(8)` + `ovn-sb(5)` schema. Pattern valid |
| 4 | `ovs-appctl upcall/show` | 9.11 | man `ovs-vswitchd(8)`. Runtime Management Commands |
| 5 | `ovs-appctl coverage/show` | 9.11 | man `ovs-vswitchd(8)`. OK |
| 6 | `ovs-appctl bond/show` | 9.11 | man `ovs-vswitchd(8)`. OK |
| 7 | `ovs-appctl fdb/show` | 9.11 | man `ovs-vswitchd(8)`. OK |
| 8 | `ovs-vsctl show` | 20.4 | man `ovs-vsctl(8)`. OK |
| 9 | `ovs-ofctl dump-flows br-int` | 20.4 | man `ovs-ofctl(8)`. OK |
| 10 | `ovn-appctl -t ovn-controller inc-engine/show-state` | 20.2 | man `ovn-controller(8)`. Cần verify version |

**Kết quả spot-check:** 9/10 commands verified. Lệnh #10 đặc biệt (inc-engine introspection) cần check tồn tại từ OVN 22.03.

### Phát hiện P5.V1

| ID | Mức | Mô tả |
|---|---|---|
| P5.V1 | LOW | CLI command `ovn-appctl -t ovn-controller inc-engine/show-state` cần verify version availability. Check OVN 22.03 vs OVN 22.06+ availability. |

---

## 6. Phát hiện tổng hợp Phase 5

### 6.1. Thống kê

| Mức | Số phát hiện | Chi tiết |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 0 | — |
| MED | 3 | P5.C1, P5.C2, P5.M1 |
| LOW | 2 | P5.C3, P5.V1 |
| STRONG | 2 | P5.S1, P5.S2 |

### 6.2. Danh sách phát hiện

| ID | Mức | Mô tả |
|---|---|---|
| P5.C1 | MED | `20.0 systematic-debugging` + `20.1 security-hardening` + `9.27 packet-journey` thiếu Anatomy Template A table. 3 file Block XX + Block IX là foundation nhưng không tagged Anatomy. |
| P5.C2 | MED | Style Anatomy không đồng nhất: 20.3 dùng `**Anatomy block cấu trúc:**` + markdown table, 9.4 dùng `**Anatomy từng dòng:**`, 9.11 dùng `**Anatomy N:**`. Standardize template. |
| P5.C3 | LOW | `9.26` References heading format khác (`## Tài liệu tham khảo` vs `## References`). Regex không bắt. Đã note Phase 4. |
| P5.M1 | MED | 3 file (20.1, 9.14, 20.5) có man page reference thấp (2-3). Backfill man page URL. |
| P5.V1 | LOW | CLI `inc-engine/show-state` cần verify version compatibility. |
| P5.S1 | STRONG | 9.11 (22 Anatomy), 9.4 (12 Anatomy line-by-line), 20.3 (20+ Anatomy), 20.4 (15+ Anatomy) là **exemplar** CLI reference. |
| P5.S2 | STRONG | 20.2 OVN troubleshooting (44 output block + 34 man page) là OVN CLI + output strongest. Pair với 20.4 OVS daily cho full coverage 2-layer. |

### 6.3. Trụ cột #3 coverage assessment

| Phương diện | Đánh giá | File exemplar |
|---|---|---|
| Breadth CLI coverage | Xuất sắc | 9.4 + 9.11 cover `ovs-*` tools; 20.3 + 20.4 cover daily workflow |
| Output interpretation (Anatomy) | Mạnh ở 8/12 file | 9.11 + 9.4 + 20.3 + 20.4 |
| Man page citation | Không đồng đều (3-36) | 9.4 (36) + 20.2 (34) top |
| Upstream verification | OK via spot-check | 9/10 command verified |
| Operator workflow end-to-end | Mạnh | 20.3 + 20.4 có 2 workflow mỗi file |
| Forensic case study | Mạnh | 20.5 + 9.26 |
| Decision tree / incident | Mạnh | 9.14 + 20.0 |

**Đánh giá chung trụ cột #3:** Đạt yêu cầu user "thành thạo sử dụng và hiểu output". 4 file exemplar (9.11, 9.4, 20.3, 20.4) đủ để thay thế tài liệu chính hãng upstream cho operator trung cấp. Gap nhỏ: standardize Anatomy style + backfill man page reference cho 3 file weak.

---

## 7. Đề xuất action

### 7.1. v3.1.1 patch (cosmetic cleanup, 2-4 giờ)

1. **P5.C2 MED**: Standardize Anatomy style. Chọn 1 trong 3 template (20.3 table variant đề xuất) và apply cho 9.4, 9.11, 20.2, 20.4 + các file tương lai.
2. **P5.M1 MED**: Backfill 5-10 man page reference cho 20.1 + 9.14 + 20.5.
3. **P5.V1 LOW**: Verify `inc-engine/show-state` command version trong 20.2 và add note.

### 7.2. v3.2 content expansion (1 sprint)

1. **P5.C1 MED**: Add Anatomy Template A (table variant) cho:
   - 20.0 systematic-debugging (27 output block cần Anatomy)
   - 20.1 security-hardening (34 output block cần Anatomy)
   - 9.27 packet-journey (8 output block cần Anatomy cross-stack)
   - Estimate: +200-300 dòng per file, tổng ~800 dòng.

---

## 8. Kết luận Phase 5

Cluster CLI/Operations 12 file có chất lượng **xuất sắc** ở 8/12 file, **trung bình** ở 3/12 file. Trụ cột #3 "thành thạo CLI + hiểu output" được serve rất tốt:

- Breadth: 18 target group `ovs-appctl` + 10 daily category OVN + 10 daily category OVS + 80+ subcommand reference.
- Depth: Anatomy Template A với "Line pattern | Giá trị mẫu | Ý nghĩa | Dấu hiệu đáng lưu ý" pattern ở 4 exemplar file.
- Man page integration: 9.4 (36) + 20.2 (34) leading.
- Forensic case study: 20.5 (OVN 3-case) + 9.26 (OVS revalidator).
- Incident playbook: 9.14 (20-symptom matrix).

Gap duy nhất: 3 file (20.0, 20.1, 9.27) cần Anatomy Template A backfill trong v3.2 sprint. Không có CRITICAL hoặc HIGH finding ảnh hưởng mission core.

Master report Phase 9 sẽ tổng hợp.

---

**Next:** Phase 6 Historical Narrative & Pedagogy Audit. Block I (3) + Block II (5) + Block III (3) + Part 20.6 = 12 file historical. Trụ cột #2 + #4.
