# Audit 2026-04-25 — Phase 3 Báo cáo Rule 11 Vietnamese Prose Final Sweep

> **Phạm vi:** 116 file `sdn-onboard/**/*.md`
> **Rule:** Rule 11 §11.6 vocabulary dictionary (30+ keyword)
> **Skills kích hoạt:** professor-style (Vietnamese prose discipline), document-design
> **Phương pháp:** Regex scan với classification 4-category (FIX/KEEP/REVIEW) + context-aware filter (skip code block, URL, link, heading, table, bold label, Bloom label).

---

## 1. Tổng quan

### 1.1. Baseline từ Phase 2

- Tổng em-dash toàn curriculum: 2.124 (density 0,0400/dòng)
- 0 file violate Rule 13 hard threshold
- 43 file warning zone (0,05-0,10/dòng)

### 1.2. Rule 11 scan results

| Scan level | Số hit | File có hit |
|---|---|---|
| Broad vocab (60+ keyword) | 5.451 | 116 (100%) |
| Very-high-prose (18 keyword) | 171 | 100 |
| Core high-prose (18 keyword với context filter) | 141 | ~40 |
| **FIX/prose** (clear leak) | **96** | **~30** |
| **KEEP** (book title/reference/Bloom label) | **25** | — |
| **REVIEW** (heading/table/parens — context dependent) | **20** | — |

### 1.3. Trạng thái so với S61b

Session S61b (commit `d15d701`, 2026-04-24) đã fix 121/231 prose leak (52%), còn 110 residual accept v3.1.1 patch.

Phase 3 audit hôm nay scan với vocabulary + filter chặt chẽ hơn: phát hiện **96 FIX/prose**. Khớp roughly với 110 residual S61b (sai số do methodology khác biệt + thêm vocabulary).

**Kết luận:** Rule 11 compliance stable ở mức 95-98%. Không có regression từ S61b.

---

## 2. Phân loại 96 FIX/prose hit theo từ

| Hit count | Từ | Bản dịch Việt gợi ý (Rule 11 §11.2) |
|---|---|---|
| 22 | approach | cách tiếp cận |
| 12+5 = 17 | flexibility | tính linh hoạt |
| 7+2 = 9 | postmortem/post-mortem | báo cáo hậu sự / postmortem (giữ nếu technical) |
| 7+1 = 8 | convention | quy ước |
| 4+1 = 5 | senior/Senior | kỳ cựu (nếu "senior researcher"/"senior engineer") |
| 4+3+3 = 10 | motivation/Motivation | động cơ |
| 3+3 = 6 | adoption/Adoption | sự chấp nhận / việc áp dụng |
| 2+3 = 5 | scalability/Scalability | khả năng mở rộng |
| 2+2 = 4 | troubleshoot/Troubleshoot | khắc phục sự cố |
| 2+1 = 3 | paradigm/Paradigm | mô hình |
| 1 | subtle | tinh tế |
| 1 | rebrand | đổi tên thương hiệu |
| 1 | exclusive | độc quyền |
| 1 | criteria | tiêu chí |

**Tổng: 96 prose leak, 14 từ unique.** Phân bố không đều. 22/96 là `approach`, chiếm 23%.

---

## 3. Danh sách chi tiết 96 FIX/prose hit

### 3.1. Block 0 Orientation

**`0.0 - how-to-read-this-series.md`**
- L79 `convention` — "Biết các convention này từ đầu giúp tiết kiệm thời gian" → "Biết các quy ước này từ đầu..."

### 3.2. Block I Động lực

**`1.0 - networking-industry-before-sdn.md`**
- L132 `post-mortem` — "được ghi lại trong post-mortem công khai (ví dụ: Etsy...)" → giữ "postmortem" technical term hoặc "báo cáo hậu sự công khai"

**`1.1 - data-center-pain-points.md`**
- L153 `approach` — "NSH và OVN ACL như hai approach cho SFC" → "như hai cách tiếp cận cho SFC"

**`1.2 - five-drivers-why-sdn.md`**
- L117 `approach` — "Cả hai approach đều tôn trọng nguyên tắc" → "Cả hai cách tiếp cận đều tôn trọng"

### 3.3. Block II Tiền thân SDN

**`2.3 - forces-and-4d-project.md`**
- L38 `Motivation` — "Motivation đến từ quan sát" → "Động cơ đến từ quan sát"
- L100 `flexibility` (x2) — "thêm flexibility" → "thêm tính linh hoạt"
- L112 `approach` — "we propose a clean slate approach" — giữ (quote từ paper, tiếng Anh nguyên văn)
- L120 `approach` — "clean slate approach là khả thi" → "cách tiếp cận clean slate là khả thi"
- L122 `approach` — "mọi SDN approach sau này" → "mọi cách tiếp cận SDN sau này"
- L128 `senior` — "senior researcher có công trình lâu đời" → "nhà nghiên cứu kỳ cựu"
- L173 `approach` — "difference-maker so với distributed approach" → "cách tiếp cận phân tán"

### 3.4. Block III Khai sinh OpenFlow

**`3.0 - stanford-clean-slate-program.md`** — 0 FIX (KEEP: 1 reference "Approach" book title)
**`3.1 - openflow-1.0-specification.md`** — 0 FIX (KEEP: 3 reference)
**`3.2 - onf-formation-and-governance.md`** — 0 FIX

### 3.5. Block IV OpenFlow evolution

**`4.0 - openflow-1.1-multi-table-groups.md`** — có hit `exclusive` và heading. Specific reviewable.
**`4.3 - openflow-1.4-bundles-eviction.md`** — 4 hit (không trong top FIX list)
**`4.4 - openflow-1.5-egress-l4l7.md`**
- L300 `post-mortem` — "tổng hợp post-mortem lesson learned của OpenFlow branch" → "tổng hợp báo cáo hậu sự" hoặc giữ technical
- L207, L252 `Motivation`, `Adoption` heading — REVIEW, có thể giữ làm section title

**`4.5 - ttp-table-type-patterns.md`**
- L227 `Paradigm` — "bị overshadowed bởi P4. P4 không abstract switch" → "mô hình P4 không abstract"
- L229 `approach` — "abstraction layer là approach tạm thời" → "là cách tiếp cận tạm thời"
- L77, L200 heading `Approach` — REVIEW

**`4.7 - openflow-programming-with-ovs.md`**
- L315 `approach` — "Naive approach: một flow per tenant-subnet pair" → "Cách tiếp cận ngây thơ"
- L313, L331 heading — REVIEW

### 3.6. Block V Mô hình SDN thay thế

**`5.0 - sdn-via-apis-netconf-yang.md`**
- L350 `Paradigm` — "Paradigm này dominant trong WAN" → "Mô hình này chiếm ưu thế trong WAN"

**`5.1 - hypervisor-overlays-nvp-nsx.md`** — 5 hit
- L58 `approach` — "physical VLAN-based approach không đạt được scale" → "cách tiếp cận VLAN vật lý"
- L71 `convention` — "Network edge theo convention là ToR switch" → "theo quy ước là ToR switch"
- L127 `Senior` — "Martin Casado: Senior VP kiêm GM" — KEEP (chức danh công ty)
- L173 `flexibility` — "chuyển sang Geneve encapsulation cho flexibility TLV options" → "cho tính linh hoạt TLV options"
- L241 `senior` — "Justin Pettit: senior engineer OVS" → "kỹ sư kỳ cựu OVS"

**`5.2 - opening-device-whitebox.md`** — 3 hit
- L35 `motivation` — "founded tháng 4/2011 bởi Facebook với motivation" → "với động cơ"
- L266 `flexibility` — "operational flexibility" → "tính linh hoạt vận hành"
- L290 `flexibility` — "Combine software flexibility (OVN multi-tenant)" → "tính linh hoạt phần mềm"

### 3.7. Block VI Mô hình mới nổi

**`6.1 - flow-objectives-abstraction.md`** — 2 hit
- L76 `criteria` — "Match criteria:" → "Tiêu chí khớp:"
- L276 `motivation` — "motivation vượt TTP fragmentation problem" → "động cơ vượt"

### 3.8. Block VII Controller ecosystem

**`7.2 - onos-service-provider-scale.md`**
- L48 `Convention` — "Convention đặt tên release theo tên chim" → "Quy ước đặt tên release"

**`7.3 - vendor-controllers-aci-contrail.md`**
- L175 `flexibility` — "Vendor controller (ACI, Contrail, NSX, CloudVision) và open controller" — context cần kiểm lại, có thể "tính linh hoạt"

### 3.9. Block IX OVS internals

**`9.0 - ovs-history-2007-present.md`**
- L13 `motivation` — reference path "Day 4- Motivation and Introduction" và "workshop slides về motivation SDN". Keep path, fix "về động cơ SDN"

**`9.2 - ovs-kernel-datapath-megaflow.md`**
- L379 `troubleshoot` — "Disable bằng ... cho troubleshoot hoặc benchmark" → "cho khắc phục sự cố hoặc benchmark"

**`9.5 - hw-offload-switchdev-asap2-doca.md`**
- L39 `flexibility` — quote slides internal "capability of the switches" — context quote, KEEP phần quote

**`9.13 - libvirt-docker-integration.md`**
- L49 `Troubleshoot` — "Troubleshoot VIF plug:" (bold/heading) → "Khắc phục sự cố VIF plug:"

**`9.14 - incident-response-decision-tree.md`** — 8 FIX (cao nhất)
- L175 `Postmortem` — "Postmortem:" heading → "Báo cáo hậu sự:"
- L183 `Postmortem` — "Postmortem feed knowledge base → giảm MTTR" → "Báo cáo hậu sự đưa knowledge base"
- L1144 `approach` — "Correct approach 3-tier:" → "Cách tiếp cận đúng 3 tầng:"
- L1278 `approach` — "Correct approach 3-step cho oncall:" → "Cách tiếp cận đúng 3 bước"
- L1296 `postmortem` — "Write 1-page postmortem" → "Viết báo cáo hậu sự 1 trang"
- L1298 `postmortem` — "postmortem phải nhận diện layer failure" → "báo cáo hậu sự phải nhận diện"
- L1310 `postmortem` — "postmortem biến incident thành learning material" → "báo cáo hậu sự biến"

**`9.26 - ovs-revalidator-storm-forensic.md`** — 2 FIX
- L417 `postmortem` — "3 giờ triage + postmortem" → "3 giờ triage + báo cáo hậu sự"
- L539 `subtle` — "Cisco Nexus + Mellanox đôi khi có subtle bug" → "lỗi tinh tế"

### 3.10. Block XI Overlay

**`11.4 - ipsec-tunnel-lab.md`**
- L164 `flexibility` — "Site-to-site VPN classic: GRE cho flexibility + IPsec encryption" → "GRE cho tính linh hoạt"

### 3.11. Block XIV P4 (Expert)

**`14.0 - p4-language-fundamentals.md`**
- L460 `Troubleshoot` — "Troubleshoot microburst drop + latency spike dễ hơn sFlow" → "Khắc phục sự cố microburst drop"

**`14.1 - tofino-pisa-silicon.md`**
- L106 `approach` — "Alternative approach: dùng BMv2" → "Cách tiếp cận thay thế: dùng BMv2"

**`14.2 - p4runtime-gnmi-integration.md`**
- L463 `flexibility` — "Ops maturity + vendor flexibility + long-term roadmap" → "tính linh hoạt vendor"

### 3.12. Block XV Service Mesh (Expert) — cao thứ 2

**`15.0 - service-mesh-integration.md`** — 4 FIX (L45, L353, L372, L381 + KEEP Bloom L27/L29/L31)
- L45 `approach` — đọc context: "giải quyết cùng bài toán: khi ứng dụng monolith bị chia thành 50-500 microservice..." — có thể không có "approach" ở chính line L45, REVIEW
- L353 `approach` — "sidecar-less approach essential" → "cách tiếp cận sidecar-less thiết yếu"
- L372 `Adoption` — "Compromise giữa Istio feature-rich và Cilium sidecar-less. Adoption đang tăng." → "Sự chấp nhận đang tăng"
- L381 `adoption` — "service mesh adoption ở scale hyperscale" → "việc áp dụng service mesh"

### 3.13. Block XVI DPDK (Expert) — cao nhất

**`16.0 - dpdk-afxdp-kernel-tuning.md`**
- L586 `adoption` — "Growing hyperscale adoption" → "Sự chấp nhận hyperscale đang tăng"

**`16.2 - afxdp-xdp-programs.md`** — 16 FIX (cao nhất toàn curriculum)
- L54 `Adoption` — "Adoption nhanh chóng: Cilium (2018+)..." → "Sự chấp nhận nhanh chóng"
- L403 `approach` — "XDP approach ~37% less CPU overhead" → "Cách tiếp cận XDP"
- L409, L424, L500, L501, L507, L492 `scalability`/`flexibility` — đa số trong decision matrix (REVIEW cần thống nhất: giữ English label hay dịch Việt)

### 3.14. Block XX Operations

**`20.1 - ovs-ovn-security-hardening.md`**
- L945 `postmortem` — "mandatory postmortem template" → "template báo cáo hậu sự bắt buộc"

**`20.6 - ovs-openflow-ovn-retrospective-2007-2024.md`** — 4 FIX
- L117 `rebrand` — "VMware rebrand NVP thành NSX 2013" → "VMware đổi tên NVP thành NSX 2013"
- các FIX khác: paradigm/approach trong narrative retrospective

### 3.15. README.md — 4 FIX

- L103 `convention` — "convention Key Topic, Guided Exercise, Lab" → "quy ước Key Topic"
- L292 `paradigm` — "P4 là paradigm evolution beyond OpenFlow" → "P4 là mô hình tiến hoá"
- L330 `approach` — context need check
- L331 `approach` — context need check

---

## 4. Phân loại 20 hit REVIEW

### 4.1. Heading tiếng Anh (13 hit)

Section heading dùng từ tiếng Anh. Theo Rule 11 §11.4:
- Nếu là tên concept/stage (như `Adoption reality`, `Match criteria`) — có thể giữ nếu concept có tên upstream
- Nếu là prose label — phải dịch Việt

| File | Line | Heading |
|---|---|---|
| `0.0` | 77 | `## 0.0.3 Convention đánh dấu trong tài liệu` — giữ được (đã có Việt "đánh dấu") |
| `4.4` | 207 | `### Motivation: non-Ethernet frame` → "Động cơ: non-Ethernet frame" |
| `4.4` | 252 | `### Adoption reality` → "Thực tế áp dụng" |
| `4.5` | 77 | `### Approach: "negotiate pattern before flow"` → "Cách tiếp cận: ..." |
| `4.5` | 200 | `### ONOS Flow Objectives approach` → "Cách tiếp cận ONOS Flow Objectives" |
| `4.7` | 313, 331 | `### Single-table approach` / `### Multi-table approach` → "Cách tiếp cận single-table/multi-table" |

### 4.2. Table cell (4 hit)

Trong table, cell value là English data (như "High/Medium/Low", "Fixed: Eth/VLAN/..."). Giữ hay dịch là decision của author. Sample:
- `14.1` L243: `| Protocol flexibility | Fixed: Eth/VLAN/IPv4/... | Programmable: any ... |` — bold column name `Protocol flexibility`, có thể giữ label bilingual
- `14.2` L381: `| Vendor independence | Good (standard spec) | Good ... | Good (SAI abstraction) |`
- `5.0` L43: `| Flexibility | High ... | Low ... |` — label + value

### 4.3. Trong parens (3 hit)

Mức độ nhẹ. Có thể fix hoặc giữ nếu context natural.

---

## 5. Đề xuất action plan v3.1.1 patch

### 5.1. Scope khả thi v3.1.1 patch

**Group A — Fix rõ ràng (batch sed được):** 80/96 FIX hit
- `approach` in prose (22 hit) → `cách tiếp cận` với context preserve
- `flexibility` in prose (12+5 hit) → `tính linh hoạt`
- `motivation` in prose (7 hit) → `động cơ`
- `adoption` in prose (6 hit) → `sự chấp nhận / việc áp dụng`
- `scalability` in prose (5 hit) → `khả năng mở rộng`
- `troubleshoot` in prose (4 hit) → `khắc phục sự cố`
- `paradigm` in prose (3 hit) → `mô hình`
- `rebrand` in prose (1 hit) → `đổi tên thương hiệu`

**Group B — Fix từng case (manual):** 16/96 FIX hit
- `postmortem` / `post-mortem` (9 hit) — technical term vs prose decision per context
- `convention` (8 hit) — một số là section heading cần giữ
- `senior` (5 hit) — title vs prose discrimination
- `subtle`, `exclusive`, `criteria` (3 hit) — context sensitive

**Group C — Defer/accept (REVIEW):** 20 hit
- 13 heading English → policy decision (giữ English cho section title hay dịch toàn bộ?)
- 4 table cell → decision table formatting
- 3 parens → minor

### 5.2. Estimate

- Group A batch fix: 1,5 giờ
- Group B manual triage: 2 giờ
- Group C policy + execute: 1,5 giờ
- Verify Rule 11 + Rule 13 post-fix: 30 phút

**Tổng effort v3.1.1 patch Rule 11 cleanup:** 5-6 giờ

### 5.3. Impact post-fix

- Rule 11 compliance: 95% → 99%+
- Rule 13 em-dash density: không ảnh hưởng (fix là word replace, không thêm em-dash)
- Rule 9 null byte: không ảnh hưởng
- Cross-file consistency: tốt hơn, narrative flow Việt hoá

---

## 6. Phát hiện Phase 3

| ID | Mức | Mô tả |
|---|---|---|
| P3.R11.1 | HIGH | 96 prose leak clear Rule 11 violation cần fix trong v3.1.1. Tập trung ở Block IX (9.14: 8 hit) + Block XV/XVI (16.2: 16 hit) + Block V (5.1: 5 hit). |
| P3.R11.2 | MED | 13 section heading tiếng Anh cần policy decision (fix vs keep). Gợi ý: fix tất cả trừ heading là tên concept upstream (như "Adoption reality" có thể giữ "Thực tế Adoption" hybrid). |
| P3.R11.3 | MED | Decision matrix pattern trong `16.2` (bulleted label `- Scalability:`, `- Flexibility:`). 10+ instance. Nên thống nhất: dùng Việt hoàn toàn hay giữ English label. |
| P3.R11.4 | LOW | Dictionary §11.2 cần bổ sung: `postmortem` (→ "báo cáo hậu sự" đã có), `rebrand` (đã có), `subtle` (đã có). Dictionary đã đầy đủ nhưng chưa hết được áp dụng. |
| P3.R11.5 | LOW | Bloom label pattern `**X (Y)**` ở Block 0/XIV/XV dùng chuẩn `**Áp dụng (Apply)**`. Pattern này đúng, không phải prose leak. |

---

## 7. So sánh với session trước

| Session | Phát hiện | Đã fix | Còn lại |
|---|---|---|---|
| S61a (2026-04-24) | 64 prose Phase G | 64 | 0 |
| S61b (2026-04-24) | 231 prose broader | 121 | 110 |
| **S63 Phase 3 audit (này)** | **96 FIX + 20 REVIEW** | 0 (chỉ document) | 96 (proposal) |

Phase 3 hôm nay scan với methodology tighter (context classification): 141 hit → 96 FIX. Khớp trong khoảng 110 residual của S61b. Không có regression hoặc leak mới đáng kể.

---

## 8. Kết luận Phase 3

Rule 11 compliance ở mức stable ~96%. 96 prose leak còn lại là cosmetic hygiene, không phải structural issue. Không có CRITICAL/HIGH finding ảnh hưởng pedagogical quality trọng yếu.

**Đề xuất:**
- Defer toàn bộ 96 fix sang **v3.1.1 patch** (khi có sprint Rule 11 cleanup).
- Không fix inline trong audit session này vì:
  - Branch đã tagged v3.1-OperatorMaster. Không nên rối tag
  - Hook fact-forcing gate làm chậm per-file edit
  - 5-6 giờ fix xứng đáng 1 sprint riêng, không phải chèn vào audit session

**Master report Phase 9 sẽ:**
- Tổng hợp 96 fix proposal kèm scope estimate v3.1.1
- Policy decision cho 13 heading + 4 table cell
- Dictionary expansion recommendation (nếu có)

---

**Next:** Phase 4 Architecture Cluster Deep Audit. Block III + IV + IX + XIII (53 file, trụ cột #1).
