# Plan: Tách topic Multichassis + PMTUD khỏi SDN 1.0

> **Trạng thái:** Draft — revision 3 (2026-04-20), chờ user phê duyệt S1–S8.
> **Tạo:** 2026-04-20 (rev 1)
> **Cập nhật rev 2:** 2026-04-20 — absorb 4 file .md user upload thay thế 4 artifact URL HTTP 403.
> **Cập nhật rev 3:** 2026-04-20 — reference tường minh các tiêu chuẩn quốc tế từ skills (ISO/IEEE/WCAG/ANSI + framework sư phạm) + 3 quyết định của user (branch, staging lab, RARP vs GARP deep).
> **Owner:** VO LE
> **Skills active:** professor-style, document-design, fact-checker, web-fetcher, flow-graph, blueprint
> **Mode:** direct edit (không git branch tới khi user duyệt phạm vi)

**Thay đổi rev 3:**
- Thêm **Phần 0 — Tiêu chuẩn quốc tế áp dụng** liệt kê tường minh mọi standard từ skills + vị trí áp dụng.
- Cập nhật **toàn bộ Step S1–S8** để enforce standards cụ thể: S1 (skeleton ISO 2145+WCAG+DITA+IEC 82079-1+Merrill+Bloom), S2 (Conceptual Change+ISO 704+DITA Concept), S3 (ANSI Z535.6+DITA Reference+Cognitive Load+RFC-first), S4 (Conceptual Change cho 4 lý do RARP+ISO 704 monosemy+Merrill integration), S4b (POE+Falsificationism+Evidence numbering+Rule 7 terminal fidelity), S5 (IEC 82079-1 §6.7 cross-ref+Rule 8 SVG-caption), S6 (link integrity+Cross-File Sync), S7 (Block A Checklist C + Block B 9 standards check + Block C 5 fact-check), S8 (Q3 branch confirmed).
- User decisions: branch `feat/sdn-restructure-multichassis-pmtud` from master (Q3 ✓), có staging lab (Q5 ✓ → Lab output sẽ verify real), RARP vs GARP deep ~150 dòng (Q6 ✓).
- Q1 (tách 3.0+4.0 hay giữ 1 file) chưa trả lời → default giữ 1 file, trigger tách nếu > 1500 dòng trong S4b.

**Thay đổi rev 2:**
- Bỏ rủi ro "artifact không fetch được" (risk #4) — 4 file markdown đã thay thế.
- Mở rộng kiến trúc SDN 3.0: thêm Lịch sử 3 thời kỳ, RARP vs GARP analysis, 6-kịch bản packet path (E-W/N-S/egress × steady/migrate), 3-lớp duplicate anatomy, timeline T0-T9, playbook 6-layer verification, commit anchor `7084cf43`, code excerpts từ `consider_port_binding()` + `consider_mc_group()`.
- Đổi line count estimate SDN 3.0: ~700 → ~1100–1300.
- Re-group H2 để không vượt limit 7 H2/Part của document-design.

---

## 0. Tiêu chuẩn quốc tế áp dụng (NEW rev 3)

Bảng này tra cứu mọi standard nhúng trong các skills, ánh xạ sang section trong SDN 3.0 cần tuân thủ. Mỗi standard là nguồn gốc của một rule cụ thể trong document-design/professor-style/flow-graph — không phải best practice tự đặt.

### 0.1 Nhóm tài liệu kỹ thuật (Normative — bắt buộc)

| Tiêu chuẩn | Phạm vi | Áp dụng trong SDN 3.0 |
|---|---|---|
| **IEC/IEEE 82079-1:2019** | Tài liệu kỹ thuật — nguyên tắc và yêu cầu chung | §5.2 terminology → 11.x; §5.3 audience identification → header block; §6.5 findability → evidence numbering (Evidence #1-N trong Lab); §6.7 cross-reference → mỗi link "xem SDN 3.x" phải có text mô tả đích, không chỉ link trần; §7 evaluation → Step S7 quality gate |
| **ISO/IEC/IEEE 26514:2022** | Thiết kế tài liệu cho người dùng phần mềm | §7.3 content organization → §4 kiến trúc 7 H2; §7.4 information chunking → giới hạn 30 dòng/code block; §7.6 terminology → tránh dịch "multichassis" sang "đa khung gầm"; §8 four-level review → S7; §9 version management → Changelog |
| **ISO 2145:1978** | Đánh số phân mục trong tài liệu | Giới hạn chiều sâu ≤4 cấp (3.1 → 3.1.1 → 3.1.1.1); 4 mục đích đánh số: trình tự, tìm kiếm, trích dẫn, tham chiếu nội bộ → mọi evidence/lab step phải có số thứ tự (Evidence #1, Step 1.1...) |
| **OASIS DITA 1.3** | Information typing | Phân biệt Concept (§3.1 lịch sử), Task (Lab playbook), Reference (bảng 6 kịch bản, RFC list); mỗi section thuần 1 type — không trộn concept + task + reference trong 1 H2 |

### 0.2 Nhóm accessibility (Normative — bắt buộc)

| Tiêu chuẩn | Phạm vi | Áp dụng trong SDN 3.0 |
|---|---|---|
| **WCAG 2.1 SC 1.3.1** (Info and Relationships) | Semantic hierarchy | H1 → H2 → H3 liên tục, không skip level; table phải có `<th>` hàng header |
| **WCAG 2.1 SC 1.4.12** (Text Spacing) | Text readability | Áp dụng cho mọi SVG flow diagram: line-height ≥1.5×font-size, letter-spacing ≥0.12×font-size, word-spacing ≥0.16×font-size. Chạy `svg-audit.py` trước commit (Checklist C Rule 6.5a). |
| **WCAG 2.1 SC 1.1.1** (Non-text content) | Alt text | Mỗi SVG diagram cần `<title>` + `<desc>` element; mỗi bảng cần caption mô tả |
| **WCAG 2.2 draft** (Table complexity) | Simple tables | Max 7 cột/bảng; bảng 6 kịch bản §3.3.4 có 4 cột → OK; bảng timeline T0-T9 có 4 cột → OK |
| **EN 301 549:2021** | EU accessibility | Bao trùm WCAG 2.1 AA → áp dụng toàn file |

### 0.3 Nhóm safety message (Normative — bắt buộc cho callout cảnh báo)

| Tiêu chuẩn | Phạm vi | Áp dụng trong SDN 3.0 |
|---|---|---|
| **ANSI Z535.6** | Safety information signal words | 3 signal words: DANGER / WARNING / CAUTION. Callout §3.3.5 "tcpdump bond0 im lặng ≠ outage" → **WARNING** (có thể dẫn đến misdiagnosis production). Callout §3.5.4 "DPDK port kẹt block" → **WARNING**. Callout §3.6.3 "MTU < 1558 → drop gói jumbo" → **CAUTION** (hư hỏng operational) |
| **ANSI Z535.6 5-element rule** | Safety message structure | Mỗi callout WARNING/CAUTION phải có: (1) signal word, (2) mô tả nguy hiểm, (3) hậu quả, (4) cách phòng tránh, (5) biểu tượng (markdown ⚠️ / 🛑) |
| **ISO 3864-2** | Tần suất safety message | Không lạm dụng callout; ước lượng SDN 3.0 cần 5-8 callout (3-5 WARNING + 2-3 CAUTION), không quá 12 |

### 0.4 Nhóm terminology (Informative — khuyến nghị cao)

| Tiêu chuẩn | Phạm vi | Áp dụng trong SDN 3.0 |
|---|---|---|
| **ISO 704:2022** | Terminology principles | Monosemy (1 thuật ngữ = 1 nghĩa): "multichassis port" và "additional_chassis" dùng nhất quán, không hoán đổi; consistency xuyên file; transparency (thuật ngữ phản ánh concept) |
| **ISO 10241-1:2011** | Glossary entry format | Mỗi term trong Exam Prep có format: `term (acronym) — definition [source]`. Ví dụ: `RARP (Reverse Address Resolution Protocol) — giao thức ngược ARP hỏi IP từ MAC [RFC 903]` |
| **Acronym rule** | First-use expansion | Mọi acronym expand lần đầu: PMTUD (Path MTU Discovery), TLV (Type-Length-Value), OVN (Open Virtual Network)... |

### 0.5 Nhóm sư phạm quốc tế (từ professor-style)

| Framework | Tác giả / Năm | Áp dụng trong SDN 3.0 |
|---|---|---|
| **Merrill's First Principles of Instruction** | M. D. Merrill, 2002, ETR&D 50 | Principle 1 "real-world problem first" → §3.1 mở đầu bằng bài toán blackhole, không bằng định nghĩa; Principle 4-5 → §3.6 + §3.7 Production readiness |
| **Bloom's Revised Taxonomy** | Anderson & Krathwohl, 2001 | 7 LOs viết theo động từ Bloom (Understand/Analyze/Apply/Evaluate/Create) — không dùng "Know", "Learn" |
| **Conceptual Change Theory** | Posner et al., 1982, Science Education 66(2) | Mỗi H2 có sub-section "Misconceptions" cho concept mới — bác bỏ giả thuyết sai trước khi trình bày đúng (ví dụ: "gói cũ trong virtio queue được transfer cùng memory" bị bác ở §3.2.3) |
| **Gagné's Event #3** | Gagné, 1965 | "Stimulate recall of prior knowledge" → mỗi H2 mở đầu bằng "Liên hệ ngược: xem SDN 1.x" |
| **4C/ID Model** | van Merriënboer, 1997 | Whole-task sequencing: §3.1 overview → §3.2-3.6 mechanism → §3.7 integration → Lab practice |
| **Cognitive Load Theory** | Sweller, 1988, Cognitive Science 12(2) | Giới hạn 7 H2/Part, 30 dòng/code block, 6-8 câu/đoạn — minimize extraneous load |
| **Predict-Observe-Explain + Falsificationism** | White & Gunstone 1992; Popper 1959 | Lab playbook 6 lớp có phase "predict output mẫu" trước khi chạy CLI → POE cycle |

### 0.6 Nhóm protocol/network (từ fact-checker + flow-graph)

| Tiêu chuẩn | Phạm vi | Áp dụng trong SDN 3.0 |
|---|---|---|
| **RFC 8926** | Geneve encapsulation | Verify overhead math 58 byte; IANA Option Class 0x0102 |
| **RFC 1191** | Path MTU Discovery | PMTUD pipeline §3.4; mtu_expires recovery §3.6.2 |
| **RFC 903** | Reverse ARP | RARP frame layout §3.5.3; opcode 3/4 |
| **RFC-first citation** | fact-checker §3.2 | RFC > vendor doc > blog; dùng URL `rfc-editor.org/rfc/rfcN` không dùng mirror |
| **flow-graph visual-standards.md** | Color palette per protocol layer | Mọi SVG flow diagram trong Lab playbook phải dùng palette này: Ethernet (lớp 2) màu riêng, IP (lớp 3) màu riêng, Geneve (overlay) màu riêng, OpenFlow control màu riêng |

---

---

## 1. Bối cảnh và động lực tách

SDN 1.0 hiện đang gánh ba dòng kiến thức trong một file 1227 dòng:

Thứ nhất, L2 forwarding cơ bản trong OVN — localnet, MC_FLOOD/UNKNOWN, FDB learning, MAC_Binding (mục 1.1–1.5, lines 22–588).

Thứ hai, case study FDB poisoning trên VLAN 3808 — narrative pháp y và 3 trụ bằng chứng (mục 1.6, lines 589–910 cho phần "thuần FDB").

Thứ ba, ba cơ chế multichassis + PMTUD độc lập về mặt khái niệm nhưng đang nằm xen kẽ trong 1.6: cơ chế binding `requested-chassis` + `lport_can_bind_on_this_chassis()` (lines 912–941), Geneve overhead 58-byte + pipeline `check_pkt_larger` + `reply_icmp_error_if_pkt_too_big()` (lines 943–982), và `live_migration_activation_strategy` "rarp" vs "chassis" + jumbo frame mitigation (lines 984–990).

Vấn đề: nhóm thứ ba có giá trị tự thân — chúng giải thích cách OVN xử lý PMTUD trong môi trường multichassis, áp dụng cho mọi scenario (không chỉ FDB poisoning). Đặt chúng trong case study 1.6 khiến (a) người tìm tài liệu về PMTUD/live migration không tìm được vì file mang tên "fdb-poisoning"; (b) section 1.6 dài 442 dòng vượt limit document-design (Part 1500–4000 từ); (c) vi phạm nguyên tắc "concept before application" — cơ chế đang được trình bày SAU case study sử dụng nó.

Sau tách: SDN 1.0 giữ vai trò "L2 forwarding + FDB poisoning case study" với section 1.6 thu gọn còn ~250 dòng (chỉ FDB narrative + production log + 3-pillar evidence), tham chiếu chéo sang SDN 3.0 cho deep-dive cơ chế. SDN 3.0 mới đứng độc lập như một topic về xử lý packet trong môi trường multichassis.

## 2. Cấu trúc file sau tách

| File | Dòng (sau) | Vai trò | Đối tượng đọc |
|---|---|---|---|
| `1.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | ~950 | L2 forwarding + FDB + FDP-620 case study | Engineer cần hiểu hijack VLAN 3808 |
| `2.0 - ovn-arp-responder-and-bum-suppression.md` | 496 (giữ nguyên) | ARP responder + BUM suppression | Engineer cần hiểu broadcast handling |
| `3.0 - ovn-multichassis-binding-and-pmtud.md` | ~1100–1300 (mới) | Lịch sử 3 thời kỳ + multichassis binding + 6-kịch bản packet path + Geneve overhead + PMTUD/FDP-620 + RARP vs GARP + duplicate anatomy + activation-strategy + verification playbook | Engineer thiết kế live migration / debug multichassis / chọn MTU |

Lý do gộp binding + PMTUD trong cùng SDN 3.0 (không tách thành 3.0 + 4.0): hai cơ chế gắn kết qua chuỗi nhân quả `multichassis enforce_tunneling → tunnel overhead → check_pkt_larger → reply_icmp_error_if_pkt_too_big`. Tách sẽ buộc người đọc nhảy file giữa hai mảnh của cùng một flow.

## 3. Bản đồ di chuyển nội dung (Content Migration Map)

### 3.1 SDN 1.0 — phần GIỮ trong file

| Mục cũ | Lines | Hành động | Ghi chú |
|---|---|---|---|
| 1.1 OVN history | 22–124 | Giữ nguyên | Không đổi |
| 1.2 Localnet port | 125–214 | Giữ nguyên | Không đổi |
| 1.3 MC_FLOOD/UNKNOWN | 215–370 | Giữ nguyên | Không đổi |
| 1.4 FDB learning | 371–520 | Giữ nguyên | Không đổi |
| 1.5 MAC_Binding | 521–588 | Giữ nguyên | Không đổi |
| 1.6 Topology + cấu hình | 593–622 | Giữ nguyên | |
| 1.6 Cơ chế poisoning + ARP/bond3/aging/gateway | 623–702 | Giữ nguyên | Core narrative |
| 1.6 Fix ngắn hạn + dài hạn | 704–724 | Giữ + bổ sung kolla-build UCA workflow từ PDF (mới) | |
| 1.6 OVN FDB bug đã biết — 3 trụ bằng chứng | 725–744 | Giữ nguyên | |
| 1.6 Live migration trigger + production log | 745–910 | Giữ nguyên (giữ Rule 7+6.4 log integrity) | |
| 1.7 Design lessons | 1032–1090 | Giữ + 1 đoạn mới về MTU recovery (mục 3.3) | |
| Exam Prep + Phụ lục + References | 1091–1227 | Cập nhật theo phần mới | Xem step S5 |

### 3.2 SDN 1.0 — phần CHUYỂN sang SDN 3.0

| Mục cũ | Lines | Đích trong 3.0 | Lý do |
|---|---|---|---|
| Tại sao chỉ live migration tạo multichassis — `requested-chassis`, `lport_can_bind_on_this_chassis()`, `CAN_BIND_AS_MAIN/ADDITIONAL`, bảng 9 nova operations | 912–941 | Mục 3.2 (Multichassis binding lifecycle) | Cơ chế binding áp dụng cho mọi scenario, không riêng FDB |
| Geneve overhead 58 byte — bảng 5 thành phần, IANA Class 0x0102, OFTABLE_OUTPUT_LARGE_PKT_DETECT, action sequence của `reply_icmp_error_if_pkt_too_big`, fix Ales Musil 6 dòng `MFF_LOG_INPORT/OUTPORT` | 943–982 | Mục 3.3 (Geneve encapsulation overhead) + 3.4 (PMTUD pipeline + FDP-620 mechanism) | Topic độc lập về encap math |
| Jumbo frame 9000 → 8942 + `live_migration_activation_strategy` "rarp" vs "chassis" + Launchpad #2092250 | 984–990 | Mục 3.5 (Jumbo frame mitigation) + 3.6 (Activation strategy) | Topic về tuning operational |
| Lab 3 (FDB poisoning) | 992–1031 | GIỮ trong 1.0 — đây vẫn là lab về FDB poisoning, không phải về PMTUD | |

### 3.3 SDN 1.0 — phần CHUYỂN sang SDN 3.0 trong dạng tham chiếu chéo

Tại các vị trí cũ trong 1.6 (bug class explanation, line 627), thay deep-dive bằng one-liner + cross-ref:

```
Bước 1b: OVN pipeline swap eth.src ↔ eth.dst mà không sync inport ↔ outport.
Cơ chế chi tiết của hàm `reply_icmp_error_if_pkt_too_big()`, vị trí
trong pipeline (OFTABLE_OUTPUT_LARGE_PKT_DETECT/PROCESS), và bản vá
6-dòng của Ales Musil được trình bày ở phần SDN 3.4 — Pipeline PMTUD
và bản chất bug FDP-620.
```

Tương tự cho `enforce_tunneling_for_multichassis_ports()` → cross-ref tới SDN 3.2.

### 3.4 PDF FPT Cloud — nội dung mới đưa vào tài liệu

| Nội dung từ PDF | Đích | Ghi chú |
|---|---|---|
| Sự cố VLAN 1047 (sgn10osp02gld28, 5/12/2025) | SDN 1.0 mục 1.6 (thêm sub-section "Tiền lệ: VLAN 1047") | Củng cố pattern, không phải one-off |
| `kolla-build --template-override` + UCA Proposed pocket → deploy OVN 24.03.6 | SDN 1.0 mục 1.6 fix dài hạn (mở rộng) | Fix triệt để trong môi trường kolla-ansible |
| `net.ipv4.route.mtu_expires=600` recovery | SDN 3.0 mục 3.5 hoặc 3.7 (operational notes) | Liên quan PMTUD cache, không liên quan FDB |
| Reproduction lab: `ping -s 6000` trigger bug | SDN 3.0 — Lab N | Lab xác minh PMTUD pipeline trên môi trường thực |

### 3.5 Nội dung mới từ 4 file markdown user upload (thay thế 4 artifact claude.ai HTTP 403)

User đã cung cấp 4 file .md thay thế 4 URL `claude.ai/public/artifacts/*` mà WebFetch không truy cập được (HTTP 403 do Cloudflare bot management). 4 file overlap mạnh về chủ đề nhưng bổ sung lẫn nhau; tổng hợp content mới (chưa có trong SDN 1.0) cần absorb vào SDN 3.0:

| Nội dung | File nguồn | Đích trong SDN 3.0 | Đánh giá |
|---|---|---|---|
| Lịch sử 3 thời kỳ: pre-22.09 blackhole → 22.09 multichassis → rarp | Doc 3 §1 | Mục 3.1 (Lịch sử & động lực) — **section mới** | Cần thiết để đặt bối cảnh cho toàn Part |
| Timeline T0-T9 với/không activation-strategy | Doc 1 + Doc 3 §4.2 | Mục 3.2 (Binding lifecycle) — table mới | Trực quan hóa cửa sổ duplicate |
| 3-lớp duplicate anatomy (fabric/OVS/guest) | Doc 3 §4 | Mục 3.2 (Binding lifecycle) — sub-section | Debug aid: biết tầng nào thực sự duplicate |
| Commit anchor `7084cf437421` "Always funnel multichassis port traffic through tunnels" | Doc 4 §6 | Mục 3.3 (enforce_tunneling) — code anchor | Verifiable via upstream git |
| Code excerpt `consider_port_binding()` nhánh `PORT_LOCALNET && !always_tunnel` | Doc 4 §1 | Mục 3.3 — code block C | Giải thích vì sao steady state đi localnet |
| Code excerpt `consider_mc_group()` — comment "Add remote chassis only when localnet port not exist" | Doc 4 §5.5 | Mục 3.3 — code block C | Giải thích vì sao ARP broadcast đi fabric, không tunnel |
| Ma trận 6-kịch bản (E-W/N-S/egress × steady/migrate) | Doc 4 §5 | Mục 3.3 — bảng trung tâm | Corrective: sửa trực giác "egress không bị tunnel-enforce" |
| RARP vs GARP architectural reasoning | Doc 3 §3 | Mục 3.5 (activation-strategy) — sub-section | Giải thích design decision, không chỉ ghi "dùng RARP" |
| 60-byte RARP frame layout (RFC 903) | Doc 1 | Mục 3.5 — appendix technical | Reference |
| Playbook 6-layer verification (Port_Binding → dump flow → ofproto/trace → tcpdump → counter → tái tạo) | Doc 2 + Doc 3 §6 | **Lab N — section riêng** | Lab chính của Part |
| Edge case: MTU, race claim, transport zone, flow-based tunnels | Doc 3 §6.8 + Doc 2 §8 | Mục 3.7 (Design lessons) — callout | Operational gotchas |
| Khuyến nghị kolla-ansible operational | Doc 2 §7 | Mục 3.7 — sub-section | Audience alignment (kolla-ansible user) |
| Bug references: Launchpad #2092407 (DPDK), #1933517, #2069718 | Doc 2 + Doc 3 §2.3 | Mục 3.5 — bug reference | Traceability |

**Kết luận mapping:** 4 file .md cover đủ topic cần thiết cho SDN 3.0 hoàn chỉnh. Không cần thêm artifact. Tuy nhiên cần **fact-check lại** các claim kỹ thuật trong 4 file (đặc biệt: default `txqueuelen` 500-1000, commit hash `7084cf437421`, bảng tính Geneve overhead, QEMU `announce_self` behavior với DPDK) trước khi đưa vào SDN 3.0 — xem Step S7.

## 4. Kiến trúc SDN 3.0 (file mới)

```
3.0 - ovn-multichassis-binding-and-pmtud.md  (~1100–1300 dòng)

Header: môi trường (Ubuntu 22.04 + UCA Caracal, OVN 24.03.x).
Tham khảo chính: ovn-org/ovn source, RFC 8926 (Geneve), RFC 1191 (PMTUD),
RFC 903 (RARP), commit 7084cf437421, Launchpad #2092250 / #2092407 /
#1933517 / #2069718, OVS Conf 2022 talk Hrachyshka & Siddique.

Learning Objectives (Bloom):
  1. Giải thích (Understand) 3 thời kỳ tiến hóa live migration trong
     OVN và lý do mỗi thời kỳ tồn tại.
  2. Phân tích (Analyze) đường đi packet ở 6 kịch bản (E-W/N-S/egress
     × steady/migrate) trên topology kolla-ansible localnet.
  3. Giải thích (Understand) tại sao QEMU dùng RARP chứ không GARP và
     hệ quả OpenFlow của lựa chọn này.
  4. Tính toán (Apply) Geneve overhead 58-byte cho mọi physical MTU.
  5. Chẩn đoán (Apply) cửa sổ multichassis bằng playbook 6 lớp:
     Port_Binding → dump-flows → ofproto/trace → tcpdump → counter
     → reproduce.
  6. Đánh giá (Evaluate) trade-off giữa activation-strategy "rarp"
     vs "chassis" cho workload virtio-net vs DPDK vhost-user.
  7. Thiết kế (Create) MTU policy cho production OpenStack overlay
     đảm bảo bond1.vlanX ≥ bond0 + 58 byte.

Prerequisites: SDN 1.1 (OVN NB→SB→OVS), SDN 1.2 (localnet), CCNA L3
(IP fragmentation, PMTUD), MTU concept, OpenFlow action model.

═══════════════════════════════════════════════════════════════════════
## 3.1 — Lịch sử ba thời kỳ live migration trong OVN
═══════════════════════════════════════════════════════════════════════
   3.1.1 Bối cảnh: bài toán live migration ở lớp mạng
         - Pre-copy memory (QEMU) vs cutover ~100ms — tại sao mạng khó
         - Ba tầng cần đồng bộ: ovn-northd, ovn-controller, physical fabric
   3.1.2 Thời kỳ 1 (pre-22.09): single-chassis binding + blackhole tất yếu
         - Update binding TRƯỚC cutover → drop ở dst (VM chưa ready)
         - Update binding SAU cutover → drop ở src (VM đã rời)
         - Benchmark: ~13% loss, downtime "multiple seconds" (1607 packet test)
   3.1.3 Thời kỳ 2 (OVN 22.09): multichassis binding diệt blackhole, sinh duplicate
         - Cột additional_chassis mới trong Port_Binding
         - OVN clone gói tới TẤT CẢ chassis trong chassis + additional_chassis
         - Slide OVS Con 2022 Hrachyshka: "+94 duplicates over 1153 packets"
         - CAP analogy: không thể vừa consistency vừa availability khi binding đổi
   3.1.4 Thời kỳ 3 (activation-strategy=rarp): VM tự báo hiệu cutover hoàn tất
         - Tận dụng QEMU announce_self() (Marcelo Tosatti, 2009)
         - Benchmark: ~4ms loss, 0 duplicate
   📌 Bảng so sánh 3 thời kỳ: downtime, duplicate, complexity, dependency

═══════════════════════════════════════════════════════════════════════
## 3.2 — Multichassis port binding lifecycle (cơ chế + timeline + duplicate anatomy)
═══════════════════════════════════════════════════════════════════════
   3.2.1 Cơ chế claim: requested-chassis="hv1,hv2"
         - lport_can_bind_on_this_chassis() → CAN_BIND_AS_MAIN/ADDITIONAL
         - ovn-northd translate NB → SB Port_Binding
         - Bảng 9 nova operations: chỉ live-migrate tạo multichassis
   3.2.2 Timeline T0–T9: hành trình của một gói qua cửa sổ migrate
         - Bảng so sánh phase × hành vi × có/không activation-strategy
         - Hai chi tiết dễ bỏ qua:
           (a) tap hv2 tạo ngay ở T2 (Prepare phase), trước memory transfer
           (b) Nova event network-vif-plugged không chờ ovn-controller apply
               → bug Launchpad #1933517, #2069718
   3.2.3 Three-layer duplicate anatomy: ở đâu thực sự duplicate?
         - Lớp 1 (fabric/tunnel): KHÔNG duplicate — clone đúng 2 gói riêng biệt
         - Lớp 2 (OVS/tap trên cùng hv): KHÔNG duplicate — mỗi hv 1 bản
         - Lớp 3 (VM guest TCP/IP stack): DUPLICATE thực sự — 2 QEMU instance
           tạm thời cùng MAC trong cửa sổ cutover
         - Bác giả thuyết "gói cũ trong virtio queue được transfer cùng memory":
           virtio_net_can_receive() trả false khi vm_running=false; gói đọng
           sk_buff queue của tap (kernel object), không nằm trong memory image
   📌 Sơ đồ T0-T9 ASCII

═══════════════════════════════════════════════════════════════════════
## 3.3 — enforce_tunneling + 6-kịch bản packet path trên localnet
═══════════════════════════════════════════════════════════════════════
   3.3.1 Code anchor: consider_port_binding() trong controller/physical.c
         ```c
         } else if (access_type == PORT_LOCALNET && !ctx->always_tunnel) {
             /* Remote port connected by localnet port */
             put_resubmit(OFTABLE_LOCAL_OUTPUT, ofpacts_p);
         }
         ...
         enforce_tunneling_for_multichassis_ports(...);
         ```
         - Điều kiện rẽ nhánh localnet vs tunnel
         - NB_Global.options:always_tunnel — Neutron mặc định không set
   3.3.2 Commit anchor: 7084cf437421 "Always funnel multichassis port
         traffic through tunnels" (OVN 22.09.0)
         - Thay đổi hành vi: multichassis port enforce tunnel CẢ ingress + egress
         - Quote Hrachyshka: "enforcement of tunneling of egress AND ingress"
   3.3.3 consider_mc_group() — vì sao ARP broadcast đi localnet, không tunnel
         ```c
         } else if (!get_localnet_port(...)) {
             /* Add remote chassis only when localnet port not exist,
              * otherwise multicast will reach remote ports through localnet */
         }
         ```
         - MAC learning: dựa vào physical fabric, không qua MAC_Binding
   3.3.4 Bảng 6 kịch bản: E-W/N-S/Egress × Steady/Migrate
         | Hướng | Steady (đi đâu) | Migrate (đi đâu) | Ghi chú |
         | E-W (VM→VM cùng VLAN) | bond0 | bond1.vlanX (Geneve) | Clone 2 gói |
         | N-S (ext→VM) | bond0 hv1 | bond0 hv1 + Geneve hv1→hv2 | hv1 = relay |
         | Egress (VM→ext) | bond0 hv1 | tunnel-enforced! | Sửa trực giác |
         | E-W broadcast | localnet flood | localnet + tunnel clone | MC_FLOOD |
   3.3.5 ⚠️ Callout cảnh báo (Doc 4 §4.2): trong cửa sổ migrate,
         tcpdump trên bond0 hv1 có thể IM LẶNG cho MAC_VM-A vài trăm ms
         dù VM còn chạy ở hv1. Đây không phải outage — egress đã bị
         tunnel-enforce. Quan sát một chassis sẽ cho diagnose sai.
   📌 Sơ đồ ASCII đường đi packet 6 kịch bản

═══════════════════════════════════════════════════════════════════════
## 3.4 — Geneve overhead + PMTUD pipeline + bug FDP-620
═══════════════════════════════════════════════════════════════════════
   3.4.1 Geneve overhead toán học chính xác 58 byte
         - Bảng 5 thành phần: outer Eth 14 + IPv4 20 + UDP 8 + Geneve base 8 + OVN TLV 8
         - IANA Option Class 0x0102, RFC 8926
         - Tại sao OVN không dùng VXLAN/GRE: cần 24+15+16=55 bit metadata
         - Bảng tính sẵn: physical MTU [1500, 1600, 9000] → effective [1442, 1542, 8942]
   3.4.2 PMTUD pipeline trong OVN
         - OFTABLE_OUTPUT_LARGE_PKT_DETECT (table 41) — check_pkt_larger
         - OFTABLE_OUTPUT_LARGE_PKT_PROCESS (table 42) — reply ICMP
         - Action sequence của reply_icmp_error_if_pkt_too_big()
   3.4.3 Bug FDP-620: thiếu swap inport↔outport
         - Symptom: ICMP Frag Needed quay ngược về OVN router thay vì sender
         - Root cause: pipeline swap eth.src↔eth.dst nhưng không sync inport↔outport
         - Bản vá Ales Musil 6 dòng — MFF_LOG_INPORT/OUTPORT push/pop
         - TODO upstream FDP-748 (kernel datapath PMTUD)
   3.4.4 Cross-ref ngang SDN 1.6: hệ quả FDP-620 khi gặp FDB poisoning
   📌 Bảng pipeline location + action sequence

═══════════════════════════════════════════════════════════════════════
## 3.5 — activation-strategy: tín hiệu đồng bộ ba tầng
═══════════════════════════════════════════════════════════════════════
   3.5.1 Cơ chế "rarp" — 3 OpenFlow flows đóng vai "cửa khóa"
         - Flow 1 (priority 1000, OFTABLE_LOG_TO_PHY): drop tới tap
         - Flow 2 (priority 1000, OFTABLE_PHY_TO_LOG): drop từ tap
         - Flow 3 (priority 1010, OFTABLE_PHY_TO_LOG, dl_type=0x8035):
           controller(userdata=ACTIVATION_STRATEGY_RARP)
         - Khoảnh khắc QEMU phát RARP → pinctrl set
           options:additional-chassis-activated → unlock + resubmit
   3.5.2 ⚠️ Tại sao RARP mà không phải GARP — architectural decision
         - RARP không cần IP nguồn (chỉ cần MAC) → QEMU không phải dò IP guest
         - GARP: ethertype 0x0806 chung với mọi ARP → match tốn `arp_op=1` +
           điều kiện `arp_spa==arp_tpa` mà OpenFlow standard không hỗ trợ
           → buộc trap toàn bộ ARP lên controller (hàng nghìn pkt/s slow-path)
         - RARP: match duy nhất `dl_type=0x8035` — đúng 1 dòng, 1 packet/migrate
         - GARP phụ thuộc guest OS phát; RARP do hypervisor (QEMU) phát → bất biến
         - Bonus: 0x8035 lỗi thời → signal clean, không nhiễu traffic thật
   3.5.3 60-byte RARP frame layout (RFC 903) — appendix technical
   3.5.4 "rarp" vs "chassis" trade-off
         - "rarp" default: zero duplicate nhưng đòi virtio-net kernel datapath
         - "chassis": port available ngay khi claim, có duplicate ngắn
         - DPDK vhost-user: announce_self() mất chỗ bám → port kẹt block
         - Launchpad #2092407: bug DPDK + activation-strategy=rarp
         - Commit 949b098626b7, Launchpad #2092250, Hrachyshka
   3.5.5 OVN 25.03 + Neutron 2024.1 (Caracal) mở rộng:
         - activation-strategy chấp nhận `rarp,garp,na` (danh sách phẩy)
         - [ovn]ovn_live_migration_activation_strategy config option
   📌 Bảng tóm tắt: RARP vs GARP vs NA, ưu/nhược/dependency

═══════════════════════════════════════════════════════════════════════
## 3.6 — Operational tuning: Jumbo frame + MTU cache recovery
═══════════════════════════════════════════════════════════════════════
   3.6.1 Jumbo frame mitigation — không phải fix
         - MTU 9000 → effective 8942 → check_pkt_larger(8942) trả false
           cho gói VM 1500 → bug FDP-620 không trigger
         - Đây là mitigation, không phải fix — bug vẫn còn trong codebase
         - Yêu cầu: mọi switch trong path hỗ trợ jumbo
         - Red Hat OSP report: throughput +300% với jumbo + Geneve
   3.6.2 PMTUD cache recovery sau khi cluster patched
         - Linux client cache PMTUD entry trong route cache
         - net.ipv4.route.mtu_expires (default 600s) — RFC 1191 §6.3
         - Workaround: ip route flush cache (kiểm tra hành vi trên kernel mới)
         - PDF FPT Cloud reference
   3.6.3 Yêu cầu MTU cứng cho multichassis (kolla-ansible)
         - bond1.vlanX MTU ≥ bond0 MTU + 58 (tốt nhất + 100 dự phòng)
         - Trong inventory: neutron_tunnel_interface_mtu ≥ neutron_external_interface_mtu + 100

═══════════════════════════════════════════════════════════════════════
## 3.7 — Design lessons + Khuyến nghị vận hành
═══════════════════════════════════════════════════════════════════════
   3.7.1 Pattern: tận dụng bất biến có sẵn (QEMU announce_self 13 năm)
   3.7.2 Pattern: dùng chính data plane làm tín hiệu đồng bộ control plane
   3.7.3 Operational gotchas (Doc 3 §6.8 + Doc 2 §8):
         - MTU race
         - Race claim sau requested-chassis update
         - Transport zone mismatch giữa hv
         - Counter lag (stats_update OVS 2-3s)
         - Flow-based tunnels (experimental, default false)
   3.7.4 Monitoring: Port_Binding.additional_chassis != [] kéo dài >60s
         là dấu hiệu live migration hang
   3.7.5 Debug protocol: log filter ovn-controller "claiming lport" /
         "releasing lport" để thấy lifecycle claim

═══════════════════════════════════════════════════════════════════════
## ▶ Lab 1 — Verification playbook 6 lớp (CHÍNH)
═══════════════════════════════════════════════════════════════════════
   Lớp 1: ovn-sbctl list Port_Binding → verify additional_chassis ≠ []
   Lớp 2: ovs-ofctl dump-flows br-int trên hv3 → verify flow có 2 output:
   Lớp 3: ovs-appctl ofproto/trace → verify Datapath actions có 2 set(tunnel(...))
   Lớp 4: tcpdump trên bond1.vlanX → verify 2 Geneve cho 1 ICMP
   Lớp 5: counter tuyệt đối — n_packets tăng đúng N gói
   Lớp 6: tái tạo không cần Nova/libvirt — ovn-nbctl lsp-set-options +
          ovs-vsctl add-port fakeA-hv2 với external_ids:iface-id

▶ Lab 2 — Reproduce FDP-620 bằng ping -s 6000 trên multichassis port
   (yêu cầu lab cluster với OVN < 24.03.4 — optional)

▶ Lab 3 — Đo Geneve overhead bằng tcpdump + wireshark dissector
   (chứng minh 58 byte trên wire)

═══════════════════════════════════════════════════════════════════════
## Exam Preparation Tasks
═══════════════════════════════════════════════════════════════════════
   - Review All Key Topics
   - Define Key Terms (multichassis port, requested-chassis,
     CAN_BIND_AS_MAIN/ADDITIONAL, OFTABLE_REMOTE_OUTPUT,
     OFTABLE_OUTPUT_LARGE_PKT_*, RARP activation, GARP, PMTUD,
     mtu_expires, additional-chassis-activated, always_tunnel,
     localnet_learn_fdb)
   - Command Reference (ovn-sbctl find Port_Binding,
     ovn-appctl ofproto/trace, ovs-ofctl dump-flows br-int,
     kolla-build --template-override, sysctl net.ipv4.route.mtu_expires,
     ovn-nbctl lsp-set-options ... activation-strategy=rarp)

═══════════════════════════════════════════════════════════════════════
## Tài liệu tham khảo
═══════════════════════════════════════════════════════════════════════
   - Source code: ovn-org/ovn — controller/physical.c
     (consider_port_binding, put_remote_port_redirect_overlay,
      enforce_tunneling_for_multichassis_ports, consider_mc_group);
     controller/binding.c (claim logic); northd/northd.c
   - Tests: tests/ovn.at keyword "multi-chassis" và "requested-chassis"
   - Commit: 7084cf437421 "Always funnel multichassis port traffic
     through tunnels" (OVN 22.09.0); patch v17 "Implement RARP
     activation strategy for ports" (Hrachyshka, 6/2022); commit
     949b098626b7 (configurable activation-strategy)
   - RFC: 8926 (Geneve), 1191 (PMTUD), 903 (RARP)
   - Tài liệu: ovn-nb(5) Logical_Switch_Port options;
     ovn-architecture(7) Logical Patch Ports + Distributed Tunneling
   - Conference: OVS+OVN Conf 2022 "Live migration with OVN"
     (Hrachyshka & Siddique)
   - Bug references: Neutron Launchpad #1933517, #2069718, #2092250,
     #2092407
   - QEMU: commit 2009 "Send a RARP packet after migration"
     (Marcelo Tosatti) — gốc announce_self
   - Blog: ihar.dev/posts/ovn-chassis-binding-walkthru/
   - PDF FPT Cloud (workaround production)
```

**H2 count check:** 7 H2 (3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7) + 1 ▶ Lab block + Exam Prep + References = đúng limit document-design "Part 1500-4000 từ" với 7 H2 chính. Lab và Exam Prep không tính H2 chính.

## 5. Các bước thực thi (Construction Steps)

Mỗi step là một self-contained brief — agent chạy cold step nào cũng đủ context.

### Step S1 — Tạo skeleton SDN 3.0 (enforce ISO 2145 + WCAG + DITA)

**Brief:** Tạo file mới `sdn-onboard/3.0 - ovn-multichassis-binding-and-pmtud.md` với toàn bộ heading skeleton (mục 4), header block, learning objectives (7 LOs viết theo **Bloom's Revised Taxonomy** với động từ Understand/Analyze/Apply/Evaluate/Create), prerequisites — chưa điền nội dung body.

**Chuẩn áp dụng tại skeleton:**
- **ISO 2145:1978** — Đánh số ≤4 cấp: 3.1 → 3.1.1 → 3.1.1.1; không có 3.1.1.1.1.
- **WCAG 2.1 SC 1.3.1** — Heading liên tục H1→H2→H3→H4, không skip level.
- **ISO/IEC/IEEE 26514:2022 §7.4** — Information chunking: mỗi H2 có 3-5 H3; giới hạn 30 dòng/code block trong body.
- **OASIS DITA 1.3** — Mỗi H2 có marker type ở comment ẩn: `<!-- type: concept|task|reference -->` để tracker không trộn type. §3.1 = concept, §3.2-3.6 = concept+reference, Lab = task, References = reference.
- **IEC/IEEE 82079-1:2019 §5.3** — Header block gồm: Audience (engineer OpenStack/kolla-ansible), Scope (multichassis binding + PMTUD + activation-strategy), Prerequisites, Version (OVN 24.03.x, Neutron 2023.1+).
- **Merrill Principle 1** — §3.1 mở đầu bằng bài toán (blackhole live migration), không bằng định nghĩa.

Skeleton bao gồm: 7 H2 (3.1–3.7), 3 ▶ Lab blocks, Exam Prep, References. Mỗi H2 có comment DITA type + stub text "[CONTENT — Step Sx]" để S2-S4b biết lấp vào đâu.

**Verify:**
- `grep -c "^## " sdn-onboard/3.0*.md` = 7 H2 chính (chưa tính Lab/Exam/Refs).
- `grep -c "^### " ≥ 30` (mỗi H2 có 3-5 H3).
- Không có `^##### ` (WCAG hierarchy — không skip, không xuống cấp 5).
- `grep -c "<!-- type:"` ≥ 7 (DITA type marker).
- Header block có đủ 4 field (Audience/Scope/Prerequisites/Version).
- 7 LOs bắt đầu bằng động từ Bloom (không có "Know", "Learn").

**Dependencies:** Không.

**Rollback:** `rm sdn-onboard/3.0*.md`.

### Step S2 — Section 3.1 (Lịch sử 3 thời kỳ) + 3.2 (Binding lifecycle + duplicate anatomy)

**Brief:** Section 3.1 hoàn toàn MỚI — không có trong SDN 1.0. Nguồn chính: **Doc 3 §1** (3 thời kỳ tiến hóa) + **Doc 1** (60-byte RARP frame) + benchmark OVS Con 2022 (13.25% → 0.3% loss). Cấu trúc theo professor-style 2.1 (vấn đề trước, giải pháp sau) **và Merrill Principle 1** (Phần 0.5): bài toán blackhole đặt ở câu đầu, không bắt đầu bằng định nghĩa. Áp dụng **Gagné Event #3** (Phần 0.5): câu mở đầu §3.1 trích lại 1 dòng từ SDN 1.x về MC_FLOOD/localnet để kích hoạt recall. Ba thời kỳ trình bày dưới dạng **DITA Concept type** (Phần 0.1) — không trộn Task steps. Bảng so sánh 3 thời kỳ ở cuối (4 cột: thời kỳ / OVN version / duplicate behaviour / packet loss) — tuân **WCAG 2.2 draft ≤7 cột** (Phần 0.2).

Section 3.2 ghép: lines 912–941 từ SDN 1.0 (binding mechanism) + **Doc 3 §4.2** (timeline T0-T9 đầy đủ với cột "không activation-strategy" vs "có rarp") + **Doc 3 §4** (3-lớp duplicate anatomy: fabric/OVS/guest, bác giả thuyết virtio queue transfer). Áp dụng **Conceptual Change Theory Posner 1982** (Phần 0.5): §3.2.3 tạo sub-heading "Misconception — Gói cũ trong virtio queue được transfer cùng memory" và bác bỏ bằng `virtio_net_can_receive()` evidence TRƯỚC khi trình bày cơ chế đúng. Thêm professor 2.3 misconception "nova boot cũng tạo multichassis state" → bác bỏ bằng bảng 9 nova operations. Áp dụng **ISO 704 monosemy** (Phần 0.4): thống nhất `multichassis port` (không dùng "multi-chassis" / "multi chassis"), `additional_chassis` (không dịch). Áp dụng **ISO 2145** (Phần 0.1): depth tối đa 3.2.3.1 — không được xuống 3.2.3.1.1. Hai chi tiết highlight: (a) tap hv2 tạo ngay ở T2 (Prepare), (b) Nova event `network-vif-plugged` không chờ ovn-controller apply. Code block `lport_can_bind_on_this_chassis()` giữ ≤30 dòng (**ISO 26514 §7.4 chunking**, Phần 0.1).

**Verify:** Fact-check theo **fact-checker RFC-first** (Phần 0.6): (1) `lport_can_bind_on_this_chassis` signature + return type qua source `controller/binding.c` — link permalink GitHub; (2) bảng 9 nova operations qua nova source `nova/compute/manager.py`; (3) `virtio_net_can_receive()` semantics qua QEMU source `hw/net/virtio-net.c`; (4) default `txqueuelen` 500-1000 — verify qua kernel source `net/core/dev.c` hoặc `man tc`. Nếu không verify được claim nào → để TODO inline (tuân **IEC 82079-1 §7 evaluation** — không khẳng định sai). Standards compliance self-check: `grep -c "multi-chassis\|multi chassis"` = 0; heading depth `grep -cE "^##### "` = 0.

**Dependencies:** S1.

**Rollback:** Revert file 3.0 về skeleton sau S1.

### Step S3 — Section 3.3 (enforce_tunneling + 6 kịch bản) + 3.4 (Geneve + PMTUD + FDP-620)

**Brief:** Section 3.3 dùng **Doc 4** làm nguồn chính. Code excerpt 2 đoạn từ `controller/physical.c`: (a) nhánh `PORT_LOCALNET && !always_tunnel`, (b) comment trong `consider_mc_group()`. Mỗi code block giới hạn ≤30 dòng (**ISO 26514 §7.4**, Phần 0.1). Commit anchor `7084cf437421` "Always funnel multichassis port traffic through tunnels" — verify hash qua `git log` của ovn-org/ovn. Quote trực tiếp Hrachyshka từ ovs-dev mailing list: "enforcement of tunneling of egress AND ingress traffic" — kèm **IEC 82079-1 §6.7 cross-reference** (Phần 0.1): link ovs-dev archive message ID cụ thể, không chỉ "ovs-dev mailing list". Bảng 6 kịch bản (E-W/N-S/Egress × Steady/Migrate) từ **Doc 4 §5** — 4 cột (scenario / path chosen / rationale / tcpdump capture point), tuân **WCAG 2.2 ≤7 cột** (Phần 0.2). Áp dụng **DITA Reference type** (Phần 0.1) cho bảng 6 kịch bản — thuần tra cứu, tách khỏi Concept explanation. **Callout WARNING** (Doc 4 §4.2) theo **ANSI Z535.6 5-element** (Phần 0.3): (1) signal word WARNING, (2) mô tả nguy hiểm "tcpdump bond0 hv1 im lặng dù VM chạy hv1", (3) hậu quả "engineer misdiagnose VM down", (4) phòng tránh "capture bond1.vlanX tunnel endpoint thay vì bond0 provider", (5) biểu tượng ⚠️. Áp dụng **Cognitive Load Theory** (Phần 0.5): §3.3 có ≥3 concept mới (enforce_tunneling, consider_mc_group, 6 kịch bản) → dùng bảng 6 kịch bản làm schema tổng kết cuối section, giảm extraneous load.

Section 3.4 ghép: lines 943–982 từ SDN 1.0 (Geneve overhead + PMTUD pipeline + FDP-620) — giữ nguyên content, không cần absorb gì mới. Tách thành: (a) overhead math với bảng 3 mức MTU (**DITA Reference**), (b) pipeline location table 41/42 (**DITA Concept**), (c) action sequence `reply_icmp_error_if_pkt_too_big` (**DITA Concept**), (d) bug FDP-620 + bản vá Ales Musil 6 dòng (**DITA Task/Concept**), (e) cross-ref tới SDN 1.6. Citations theo **RFC-first** (Phần 0.6): RFC 8926 cho Geneve, RFC 1191 cho PMTUD — URL `rfc-editor.org/rfc/rfc8926`, không dùng mirror. Acronym expand lần đầu (**Phần 0.4**): PMTUD (Path MTU Discovery), TLV (Type-Length-Value), FDP (Red Hat bug tracker prefix).

**Verify:** (1) Toán Geneve 14+20+8+8+8=58 — verify **RFC 8926 §3.1**; (2) IANA OUI 0x0102 qua RFC 8926 errata + IANA Geneve registry; (3) commit hash `7084cf437421` qua `git log --grep="Always funnel"` trên repo ovn-org/ovn (permalink); (4) commit Ales Musil qua git log mailing list (đã verify session 2026-04-08); (5) quote text Hrachyshka qua ovs-dev archive search (message ID). Nếu commit hash không match → để TODO inline cho user provide. Standards compliance self-check: code block line count ≤30; bảng cột ≤7; ANSI Z535.6 checklist 5 thành phần cho callout mới.

**Dependencies:** S1.

**Rollback:** Revert.

### Step S4 — Section 3.5 (activation-strategy + RARP vs GARP) + 3.6 (Operational tuning) + 3.7 (Lessons)

**Brief:** Section 3.5 ghép (user decision Q6 confirmed — **deep ~150 dòng**): lines 984–990 từ SDN 1.0 (mention strategy briefly) + **Doc 3 §3** (RARP vs GARP architectural deep-dive — 4 lý do đầy đủ: (a) IP independence, (b) OpenFlow match cost, (c) hypervisor vs guest dependency, (d) ethertype 0x8035 clean signal) + **Doc 1** (60-byte RARP frame layout RFC 903) + **Doc 2/Doc 3** (Launchpad #2092407 DPDK bug, OVN 25.03 + Neutron 2024.1 mở rộng `rarp,garp,na`). Quote trực tiếp Marcelo Tosatti commit message 2009 qua QEMU git log nếu fetch được. 3 OpenFlow flows "cửa khóa" với priority + match + action chính xác — code block giữ ≤30 dòng (**ISO 26514 §7.4**). Cấu trúc 4 lý do theo **Conceptual Change** (Phần 0.5): mỗi lý do bắt đầu bằng câu "có người nghĩ GARP cũng được vì..." rồi bác bỏ — thúc đẩy chuyển đổi concept. Áp dụng **ISO 704 monosemy** (Phần 0.4): nhất quán "RARP frame" (không "RARP packet"), "activation-strategy" (không "activation strategy" hoặc "activation_strategy"). Callout WARNING §3.5.4 DPDK theo **ANSI Z535.6 5-element**: (1) WARNING, (2) "activation-strategy=rarp trên DPDK port", (3) "port kẹt ở `up=false` → VM không gửi được sau migration", (4) "tạm thời fallback activation-strategy=chassis cho DPDK compute; theo dõi Launchpad #2092407", (5) ⚠️.

Section 3.6: lines 984–990 SDN 1.0 (jumbo) + PDF FPT Cloud (`net.ipv4.route.mtu_expires`) + **Doc 2 §7** (yêu cầu MTU cứng kolla-ansible). Callout CAUTION §3.6.3 "MTU < 1558 → drop gói jumbo" theo **ANSI Z535.6**. Citations **RFC-first** (Phần 0.6): RFC 1191 cho PMTUD cache semantics. Cảnh báo: `mtu_expires` áp dụng cho PMTUD route cache, hành vi `ip route flush cache` trên kernel mới phải verify trước commit.

Section 3.7: design lessons từ SDN 1.0 lines 1032–1090 (giữ kernel) + **Doc 3 §6.8** (5 edge case: MTU race, race claim, transport zone, counter lag, flow-based tunnels) + **Doc 2 §8** (operational gotchas + monitoring + debug protocol). Áp dụng **Merrill Principle 4-5** (Phần 0.5) "integration phase" — §3.7 tổng kết toàn Part 3.0, cross-ref forward tới SDN 2.0 ARP responder và backward tới SDN 1.6 FDB poisoning. Áp dụng **4C/ID whole-task integration** (Phần 0.5): §3.7 list khuyến nghị vận hành production (≤10 bullet) — map sang 3 phase triển khai (pre-deploy check / migration / post-migration verify).

**Verify:** (1) RARP opcode 3/4 + ethertype 0x8035 qua **RFC 903** (rfc-editor.org permalink); (2) commit `949b098626b7` qua git log ovn-org/ovn; (3) Launchpad #2092250, #2092407, #1933517, #2069718 qua web-fetcher (skip nếu launchpad chặn, để TODO); (4) `net.ipv4.route.mtu_expires` semantics qua kernel `net/ipv4/route.c` + `man ip-sysctl`; (5) QEMU `announce_self` qua QEMU source `migration/savevm.c` hoặc `hw/net/virtio-net.c` + Marcelo Tosatti commit 2009 (git log). Chưa verify → TODO inline (tuân **IEC 82079-1 §7**). Standards compliance self-check: callout WARNING/CAUTION có 5 thành phần ANSI Z535.6; term "activation-strategy" nhất quán (ISO 704); heading depth ≤4 (ISO 2145).

**Dependencies:** S1.

**Rollback:** Revert.

### Step S4b — Lab playbook 6 lớp verification (CHÍNH)

**Brief:** Section ▶ Lab 1 chiếm ~250–300 dòng — đây là Lab chính của Part. Nguồn: **Doc 2 §6** + **Doc 3 §6** (hai bản playbook giống nhau ~95%, gộp thành 1). Áp dụng **DITA Task type** (Phần 0.1) cho toàn bộ Lab — 6 sub-section là 6 task, không trộn concept vào giữa. Áp dụng **Predict-Observe-Explain + Falsificationism** (Phần 0.5): mỗi lớp có 3 phase — (i) **Predict** ("trước khi chạy, bạn kỳ vọng thấy gì"), (ii) **Observe** (lệnh CLI + output thật), (iii) **Explain** (diễn giải + falsification criteria: "nếu output khác thế này → giả thuyết sai"). Áp dụng **Gagné Event #3** đầu Lab: nhắc lại concept 3.2-3.5. Mỗi sub-section gồm: (a) mục đích (Predict), (b) lệnh CLI chính xác (Observe), (c) output mẫu đánh số **Evidence #N** (**IEC 82079-1 §6.5 findability**, Phần 0.1), (d) cách diễn giải kết quả (Explain), (e) trap thường gặp (WARNING theo **ANSI Z535.6**).

Lớp 1: `ovn-sbctl list Port_Binding` → verify `additional_chassis ≠ []`. Lệnh setup ENV var (LSP, DP_KEY, PORT_KEY, COOKIE) đặt ở đầu Lab. Evidence #1.

Lớp 2: `ovs-ofctl dump-flows br-int | grep cookie=...` → verify flow có 2 `output:` action. Evidence #2.

Lớp 3: `ovs-appctl ofproto/trace br-int "in_port=...,..."` → verify Datapath actions có 2 khối `set(tunnel(...))` với `dst=` khác nhau. Evidence #3.

Lớp 4: `tcpdump -i bond1.vlanX -nn 'udp port 6081...'` → verify 2 Geneve cho 1 ICMP request, cùng inner ICMP id/seq, khác outer dst. Evidence #4.

Lớp 5: counter tuyệt đối — `n_packets` tăng đúng N gói trên hv3 + N gói trên hv1 + N gói trên hv2. Evidence #5.

Lớp 6: tái tạo không cần Nova/libvirt — `ovn-nbctl lsp-set-options $LSP requested-chassis=hv1,hv2 activation-strategy=rarp` + `ovs-vsctl add-port br-int fakeA-hv2 ... external_ids:iface-id=$LSP`. Evidence #6. Đây là "production debug shortcut" giá trị cao.

Bonus: Edge case section với 5 mục (MTU, race claim, transport zone, counter lag, flow-based tunnels) — cấu trúc **DITA Reference** (lookup table 5 cột ≤7: edge case / symptom / cause / detection / mitigation).

**Verify (user Q5 confirmed — có staging lab):** Chạy **thật** Lớp 1–6 trên staging của user, capture output bằng `script` hoặc `ts` để có timestamp, replace output mẫu bằng output thật. **Xóa marker "expected output, chưa verify"** sau khi có output thật. Áp dụng **Rule 7 CLAUDE.md** (Terminal Output Fidelity): không cắt bớt dòng nào, so sánh line-by-line. Output thật phải mask thông tin nhạy cảm (IP production, chassis UUID) theo quy ước `ACAB-CDEF...` — ghi rõ trong Lab preamble. Edge case cần test ≥2 mục (MTU race + counter lag). Standards self-check: **ISO 26514 §7.4** code/output block ≤30 dòng mỗi block (tách nếu dài); **WCAG 1.1.1** Evidence #N có caption text mô tả; **ANSI Z535.6** trap callout có 5 thành phần.

**Dependencies:** S2, S3, S4 hoàn tất (Lab references concept đã được giới thiệu ở 3.2-3.5).

**Rollback:** Revert.

### Step S5 — Trim SDN 1.0 mục 1.6, thay bằng cross-ref

**Brief:** Trong SDN 1.0, xóa lines 912–941 (binding mechanism), 943–982 (Geneve + PMTUD), 984–990 (jumbo + activation). Tại vị trí cũ chèn 3 đoạn cross-ref ngắn (mỗi đoạn 4–6 dòng) tóm tắt one-liner + chỉ tới mục SDN 3.x tương ứng. **IEC 82079-1 §6.7 cross-reference** (Phần 0.1): mỗi cross-ref phải có anchor text mô tả đích, không dùng "xem here" hoặc link trần. Định dạng chuẩn: `xem [SDN 3.4 — Geneve overhead và pipeline PMTUD FDP-620](./3.0 - ovn-multichassis-binding-and-pmtud.md#34-geneve-overhead--pmtud-pipeline)` — relative path + section slug. Áp dụng **ISO 26514 §7.4 chunking** (Phần 0.1): cross-ref block ≤6 dòng để không vỡ narrative flow của 1.6. Áp dụng **ISO 704 consistency** (Phần 0.4): terminology trong cross-ref summary (1.0) phải khớp terminology trong đích (3.x) — không paraphrase tạo biến thể.

Tại line 627 (bug class explanation trong "Cơ chế poisoning"), thêm cross-ref một câu sang SDN 3.4 cho deep-dive bản vá. Cập nhật đoạn "Fix ngắn hạn + dài hạn" (lines 704–724) — bổ sung kolla-build UCA workflow từ PDF (multi-line bash recipe ≤30 dòng theo **ISO 26514 §7.4**) như fix triệt để cho kolla-ansible deployment.

**Verify:** SDN 1.0 sau trim phải còn ~950 dòng; chạy `grep -c "^## " sdn-onboard/1.0*.md` còn 7 H2 sections (không thêm/bớt). Đọc lại mục 1.6 từ đầu cuối, đảm bảo narrative FDB poisoning vẫn liền mạch (không có hole logic — **IEC 82079-1 §5.4 completeness**). Đếm cross-ref: phải có ít nhất 3 reference tới SDN 3.x, tất cả dùng anchor text mô tả (không "click here"). Áp dụng **Rule 8 document-design — SVG-caption atomic consistency**: nếu cross-ref đi tới section chứa SVG, verify caption SVG gốc không đổi (chạy `svg-caption-consistency.py`). Kiểm tra link integrity: `grep -oE "\]\(\./3\.0[^\)]+\)" sdn-onboard/1.0*.md` → mỗi anchor phải match section slug thực trong 3.0.

**Dependencies:** S2, S3, S4, S4b hoàn tất (vì SDN 1.0 cross-ref tới SDN 3.x — phải tồn tại 3.x trước khi ref, theo **IEC 82079-1 §6.7**: link phải trỏ tới đích tồn tại).

**Rollback:** `git checkout sdn-onboard/1.0*.md` (chưa commit).

### Step S6 — Cập nhật README + dependency map + state

**Brief:** Cập nhật `sdn-onboard/README.md` (nếu tồn tại — Read tool kiểm tra trước) hoặc `network-onboard/README.md` thêm entry SDN 3.0 với: (a) tên đầy đủ, (b) line count, (c) prerequisite SDN 1.x, (d) anchor link tới 7 H2 sections. Áp dụng **IEC 82079-1 §6.5 findability** (Phần 0.1): README entry phải có 1-sentence summary giúp người đọc quyết định mở hay không. Áp dụng **ISO/IEC/IEEE 26514 §9 version management** (Phần 0.1): bất kỳ version number nào nhắc trong summary (OVN 22.09/24.03.x/25.03) phải đồng bộ với `haproxy-onboard/references/haproxy-version-evolution.md` nếu có cross-technology reference.

Cập nhật `memory/file-dependency-map.md` thêm **Tầng 5 entries** (per CLAUDE.md Rule 6 Checklist B bước 4): SDN 1.0 ↔ SDN 3.0 (cross-ref bi-directional), SDN 3.0 → SDN 2.0 (forward ref), SDN 3.0 → references/ (RFC 8926/1191/903, PDF FPT Cloud). Mỗi entry format: `FILE_A [section] --[direction]--> FILE_B [section] | reason`.

Cập nhật `CLAUDE.md` Current State table: thêm row `SDN 3.0 doc` với line count + topic; đánh dấu `SDN 1.0 doc` trimmed (~950 dòng). Cập nhật `memory/session-log.md` theo **Rule 5 Session Handoff** — ghi rõ commits tạo ra, branch state, pending lab verification.

**Verify:** Đọc lại 4 file đã sửa, đảm bảo line count khớp thực tế (`wc -l` cho 3.0 và 1.0). **Link integrity check** (**IEC 82079-1 §6.7**, Phần 0.1): chạy script kiểm tra mọi relative link trong README + dependency map:
```bash
grep -oE "\]\([^\)]+\.md[^\)]*\)" sdn-onboard/README.md memory/file-dependency-map.md | \
  awk -F'[(]|[)]' '{print $2}' | \
  while read link; do [ -e "${link%#*}" ] || echo "BROKEN: $link"; done
```
Kỳ vọng output rỗng. Áp dụng **Rule 2 Cross-File Sync**: sau khi update, grep 4 file này cho tên cũ (nếu có rename section) → phải = 0 residual reference.

**Dependencies:** S5 hoàn tất.

**Rollback:** Revert 4 file.

### Step S7 — Quality gate — Checklist C + standards compliance

**Brief:** Chạy đầy đủ Checklist C (CLAUDE.md Rule 6) **cộng với** 7 check standards từ Phần 0:

**Block A — Checklist C (CLAUDE.md Rule 6):**
- A1. Fact-check: liệt kê technical claim mới trong SDN 3.0 — verify từng claim qua OVN source/Launchpad/RFC.
- A2. URL check: web-fetcher mọi URL mới (RFC 8926, RFC 1191, RFC 903, kolla-ansible docs, Launchpad #2092250/#2092407/#1933517/#2069718, commit hash `7084cf43`).
- A3. Cross-file sync: tra dependency map (đã tạo S6).
- A4. Version annotation: SDN 3.0 mention OVN 22.09/24.03.x/25.03, Neutron 2023.1/2024.1 — đảm bảo callout `**Lưu ý phiên bản:**` đầy đủ.
- A5. SVG audit (Rule 6.5a): chạy `svg-audit.py` + `diacritics-audit.py` cho mọi SVG (Lab diagrams, timeline T0-T9). **0 violation WCAG 2.1 SC 1.4.12.**
- A6. SVG-caption consistency (Rule 6.5b): chạy `svg-caption-consistency.py`. **0 mismatch.**
- A7. Null byte check (Rule 9): `python3 -c "print(open(FILE,'rb').read().count(b'\x00'))"` = 0 cho cả 3.0 và 1.0.
- A8. Self-audit professor-style 6 criteria (2.1–2.6) lên SDN 3.0.

**Block B — Standards compliance (Phần 0):**
- B1. **ISO 2145:1978** — chạy `grep -c "^##### "` = 0 (không có H5). Max depth 4.
- B2. **WCAG 2.1 SC 1.3.1** — không skip heading level. Dùng script:
  ```bash
  awk '/^#/ {level=length($1); if (prev && level > prev+1) print "SKIP at line "NR": "$0; prev=level}' FILE
  ```
  Kỳ vọng output rỗng.
- B3. **WCAG 2.2 draft** — mọi bảng ≤7 cột. Đếm `|` trong dòng header: `awk -F'|' '/^\|.*\|$/ && !/---/ {print NR": "NF" cols"}' FILE` → không dòng nào >9 (7 cột + 2 cho pipe đầu/cuối).
- B4. **ANSI Z535.6 5-element** — cho mỗi callout WARNING/CAUTION, verify có 5 thành phần: signal word + mô tả nguy hiểm + hậu quả + cách phòng + ⚠️/🛑. Grep `⚠️\|🛑\|WARNING\|CAUTION` và manual review từng match (ước lượng 5-8 callout).
- B5. **ISO 3864-2** — total callout ≤12. Count: `grep -cE "^> ⚠️|^> 🛑"` + manual count.
- B6. **ISO 704 monosemy** — term "multichassis port", "additional_chassis", "activation-strategy" dùng nhất quán. Dùng script tìm variation:
  ```bash
  grep -c "multi-chassis\|multi chassis\|multichasis" FILE  # phải = 0
  grep -c "multichassis" FILE  # phải = N
  ```
- B7. **ISO 10241-1 glossary format** — mọi entry trong Exam Prep `Define Key Terms` phải có format `term (acronym) — definition [source]`.
- B8. **Bloom's Taxonomy** — 7 LOs verify không có động từ "Know", "Learn", "Understand how". Grep `^\s*\d+\.\s*(Know|Learn)` = 0 match.
- B9. **flow-graph visual-standards** — mọi SVG Lab diagram dùng palette từ `.claude/skills/flow-graph/references/visual-standards.md` (verify color hex values với palette).

**Block C — Fact-check critical claims (từ Risk register):**
- C1. `txqueuelen` default 500-1000 — verify qua `ip link show` output mẫu trên Ubuntu 22.04 + kernel source `drivers/net/tun.c`.
- C2. Commit hash `7084cf437421` — verify qua `git log --grep="Always funnel"` trên clone ovn-org/ovn hoặc github API.
- C3. QEMU `announce_self` DPDK behavior — verify claim "announce_self không fire với vhost-user DPDK" qua QEMU source + Launchpad #2092407.
- C4. Quote Hrachyshka "enforcement of tunneling of egress AND ingress" — verify qua ovs-dev archive search.
- C5. `net.ipv4.route.mtu_expires` default 600s semantics — verify qua kernel `net/ipv4/route.c` + `man ip-sysctl`.

**Verify:** 0 violation across A1-A8, B1-B9, C1-C5. Nếu Ci fail (claim không verify được) → để TODO inline trong SDN 3.0 thay vì commit sai.

**Dependencies:** S6 hoàn tất.

**Rollback:** Quay lại S5/S6 sửa lỗi.

### Step S8 — Commit + push

**Brief:** Đọc git-workflow skill (CLAUDE.md Skill Quick Reference). **User decision Q3 confirmed**: tạo nhánh mới `feat/sdn-restructure-multichassis-pmtud` from `master` (không piggyback `feat/fd-exercise-redesign-background-child`).

Workflow:
1. `git checkout master && git pull origin master` — sync base.
2. `git checkout -b feat/sdn-restructure-multichassis-pmtud`
3. Stage theo nhóm logic (per Rule 6 git safety: tránh `git add -A`, dùng path cụ thể):
   - `git add sdn-onboard/3.0\ -\ ovn-multichassis-binding-and-pmtud.md` → commit (a)
   - `git add sdn-onboard/1.0\ -\ ovn-l2-forwarding-and-fdb-poisoning.md` → commit (b)
   - `git add memory/file-dependency-map.md memory/session-log.md memory/haproxy-series-state.md CLAUDE.md sdn-onboard/README.md network-onboard/README.md` → commit (c)
4. Commit theo **Conventional Commits** (CLAUDE.md Rule 4):
   - (a) `docs(sdn): add Part 3.0 — multichassis binding and PMTUD pipeline`
   - (b) `docs(sdn): trim Part 1.0 case study, cross-ref to Part 3.0`
   - (c) `docs(memory): update dependency map and session log for SDN 3.0`
5. `git push -u origin feat/sdn-restructure-multichassis-pmtud` (Rule 4: không push main/master).
6. `gh pr create` với title + body theo template (skill `git-workflow`).

**Verify:** `git log --oneline -3` (3 commit đúng thứ tự); `git status` clean; `gh pr view` trả URL PR; nhánh không có file ngoài scope (cross-check với `git diff --stat master...HEAD`).

**Dependencies:** S7 PASS (Block A + B + C all green).

**Rollback:** `git reset --hard HEAD~3` nếu chưa push (cảnh báo CLAUDE.md Rule 4: destructive op — chỉ chạy khi user xác nhận); nếu đã push → `git revert <SHA>` từng commit theo thứ tự ngược.

## 6. Dependency Graph

```
S1 (skeleton)
  ├── S2 (Lịch sử 3.1 + Binding 3.2)          ┐
  ├── S3 (enforce+6-kịch-bản 3.3 + PMTUD 3.4) ┤
  ├── S4 (activation 3.5 + Ops 3.6 + Lessons 3.7)├── parallel
  └── S4b (Lab playbook 6 lớp)                ┘
                                                ↓
                                                S5 (trim 1.0 + cross-ref)
                                                ↓
                                                S6 (README + memory)
                                                ↓
                                                S7 (quality gate)
                                                ↓
                                                S8 (commit + push)
```

S2/S3/S4/S4b chạy parallel được — khác section của cùng file (3.0), không tranh chấp. S4b bắt đầu sau S2/S3/S4 có skeleton content tối thiểu để tham chiếu concept. S5 phải sau S2+S3+S4+S4b.

## 7. Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Section 1.6 narrative bị đứt khi xóa 3 cụm subsection | Medium | High | S5 verify "đọc liền mạch"; nếu đứt → giữ 1–2 câu setup tại vị trí cũ thay vì xóa hết |
| Cross-ref dày đặc làm SDN 1.0 khó đọc | Low | Medium | Giới hạn ≤3 cross-ref tới SDN 3.x trong section 1.6 |
| `mtu_expires` semantics chưa verify được | Medium | High | S4 — viết TODO inline thay vì viết sai; verify trước commit |
| ~~Artifact claude.ai (4 link) HTTP 403~~ | ~~High~~ | ~~Medium~~ | **✓ Resolved rev 2** — 4 file .md user upload đã thay thế (§3.5) |
| Content 4 file .md user upload chứa claim kỹ thuật chưa verify (default txqueuelen 500-1000, commit hash 7084cf437421, QEMU announce_self DPDK behavior, quote Hrachyshka ovs-dev) | High | High | S2+S3+S4+S7 — fact-check từng claim qua upstream source; claim nào không verify → để TODO inline hoặc bỏ |
| 4 file .md overlap mạnh về content (Doc 1+2+3+4 đều nói về activation-strategy) — nguy cơ duplicate trong SDN 3.0 | Medium | Medium | Mapping absorbable ở §3.5 chỉ rõ mỗi nội dung đi về section nào, tránh paste cùng đoạn 2 lần |
| Lab playbook 6 lớp chưa được chạy trên lab thật | High | Medium | S4b — đánh dấu output mẫu "expected, chưa verify trên production" nếu không có lab; khuyến khích user chạy Lớp 1+5 trước khi commit |
| Lab "ping -s 6000" yêu cầu môi trường OVN < 24.03.4 — user có thể không có | Medium | Low | Đánh dấu lab "optional — yêu cầu lab cluster với OVN unpatched" |
| SDN 3.0 vượt 7 H2 khi absorb quá nhiều content (vi phạm document-design 1.1) | Medium | Medium | Đã re-group ở §4: 7 H2 chính + ▶ Lab blocks riêng. Nếu viết xong vẫn dài → cân nhắc tách 3.0 → 3.0 + 4.0 |

## 8. Estimated effort

| Step | Estimate (Claude tool calls) |
|---|---|
| S1 | 1 Write |
| S2 | 2 Read (1.0 + Doc 1+3) + 2-3 Edit (3.0) — nội dung MỚI 3.1 + ghép 3.2 |
| S3 | 2 Read (1.0 + Doc 4) + 2-3 Edit (3.0) — code excerpts + bảng 6 kịch bản |
| S4 | 2 Read (1.0 + Doc 1+3) + 2-3 Edit (3.0) — RARP vs GARP + jumbo + lessons |
| S4b | 2 Read (Doc 2 + Doc 3 §6) + 3-4 Edit (3.0 Lab section) — playbook 6 lớp |
| S5 | 1 Read + 3-5 Edit (1.0) |
| S6 | 4 Edit |
| S7 | 8–15 verification calls (web-fetcher, fact-check 4 claim trong Risk register) |
| S8 | 5 git commands |

Total: ~35–50 tool calls, không tính fact-checker iteration nếu phát hiện sai sót. Tăng so với rev 1 (~25–35) do absorb 4 file .md với nhiều content mới phải verify.

## 9. Mở đầu cần user quyết định

Trước khi vào S1, cần user xác nhận:

1. **PENDING** — Cấu trúc 3 file (1.0 trim, 2.0 giữ, 3.0 mới) có đúng ý không, hay user muốn tách thành 3.0 + 4.0 (binding riêng / PMTUD riêng). **Lưu ý rev 2:** SDN 3.0 đã phình ~1100–1300 dòng sau absorb 4 file .md — nếu user muốn giới hạn 900 dòng/Part, phải tách. **Default rev 3:** giữ 1 file 3.0; nếu sau S4b file vượt 1500 dòng thực tế → trigger split-decision với user trước khi vào S5.
2. ~~Cho phép mình paste content từ 4 artifact?~~ **✓ Resolved rev 2** — 4 file .md user upload đã đủ.
3. ~~Branch strategy~~ **✓ Resolved rev 3** — user xác nhận tạo `feat/sdn-restructure-multichassis-pmtud` từ `master`.
4. Lab "ping -s 6000" có đưa vào SDN 3.0 không (cần lab cluster OVN < 24.03.4), hay chỉ giữ làm "thí nghiệm tham khảo" trong appendix.
5. ~~Lab playbook chạy thật?~~ **✓ Resolved rev 3** — user có staging lab; S4b sẽ verify output 6 lớp trên thật, xóa marker "expected, chưa verify".
6. ~~RARP vs GARP độ sâu?~~ **✓ Resolved rev 3** — user chọn deep ~150 dòng (Doc 3 §3 đầy đủ 4 lý do).

## 10. Changelog plan

| Revision | Ngày | Thay đổi |
|---|---|---|
| rev 1 | 2026-04-20 | Draft ban đầu, dựa vào SDN 1.0 hiện có + PDF FPT Cloud |
| rev 2 | 2026-04-20 | Absorb 4 file .md user upload: thêm §3.5 content mapping, expand §4 kiến trúc (3.1 Lịch sử, 3.2 Binding+T0-T9+duplicate anatomy, 3.3 enforce+6-kịch-bản, 3.5 RARP vs GARP deep-dive, Lab playbook 6 lớp), thêm S4b (Lab), cập nhật risk register (resolve #4, thêm 3 risk mới), cập nhật effort estimate, mở 2 câu hỏi mới (#5, #6) |
| rev 3 | 2026-04-20 | (1) Thêm Phần 0 — Tiêu chuẩn quốc tế áp dụng (6 sub-section): IEC/IEEE 82079-1:2019, ISO/IEC/IEEE 26514:2022, ISO 2145:1978, OASIS DITA 1.3, WCAG 2.1/2.2, EN 301 549:2021, ANSI Z535.6, ISO 3864-2, ISO 704:2022, ISO 10241-1:2011, RFC 8926/1191/903 + 7 framework sư phạm (Merrill, Bloom, Posner, Gagné, 4C/ID, Sweller, POE+Falsificationism). (2) Cập nhật MỌI step S1–S8 enforce standards cụ thể: S1 (ISO 2145+WCAG+DITA+IEC 82079-1+Merrill+Bloom), S2 (Conceptual Change+Merrill+Gagné+ISO 704+DITA Concept), S3 (ANSI Z535.6 5-element+DITA Reference+Cognitive Load+RFC-first), S4 (Conceptual Change cho 4 lý do RARP+ISO 704 monosemy+Merrill integration), S4b (POE+Falsificationism+IEC 82079-1 §6.5 Evidence numbering+Rule 7 terminal output fidelity), S5 (IEC 82079-1 §6.7 cross-reference+Rule 8 SVG-caption), S6 (link integrity check+Rule 2 Cross-File Sync), S7 (3 blocks A/B/C: Checklist C + 9 standards check + 5 fact-check), S8 (Q3 branch confirmed). (3) User decisions Q3/Q5/Q6 confirmed, Q1 còn pending (default giữ 1 file, trigger split nếu >1500 dòng). |
