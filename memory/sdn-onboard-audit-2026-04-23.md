# Audit toàn bộ chương trình đào tạo `sdn-onboard/*` — 2026-04-23

> **Auditor:** Claude (skill stack: professor-style + document-design + fact-checker + web-fetcher).
> **Phạm vi:** 105 file `.md` (loại trừ `README.md`), 31.529 dòng content, 4 chiều audit.
> **Loại audit:** Quick scan toàn bộ (không phải deep audit từng file).
> **Mục đích:** Cung cấp bản đồ vi phạm + ưu tiên fix cho session 25+.

---

## 1. Tổng quan curriculum

| Số liệu | Giá trị |
|--------|---------|
| Tổng file `.md` | 105 (loại README) + 1 README + 11 file offline `doc/` |
| Tổng dòng content | 31.529 |
| Block phân bố | Block 0 (3), I (3), II (5), III (3), IV (8), V (3), VI (2), VII (6), VIII (4), **IX (25)**, X (7), XI (5), XII (3), **XIII (14)**, XIV (3), XV (3), XVI (3), XVII (1), XVIII (1), XIX (1), XX (2) |
| File lớn nhất | `19.0 - ovn-multichassis-binding-and-pmtud.md` (1379 dòng) |
| Top 5 dòng | 19.0 (1379), 17.0 (1180), 4.7 (764), 9.24 (672), 9.25 (636) |
| URL tham chiếu | 844 references, 502 unique URLs, 106 file có URL |

Block IX (OVS deep dive — 25 file) và Block XIII (OVN architecture — 14 file) chiếm 37% tổng số file. Đây là core curriculum, hợp lý vì OVS/OVN là focus chính của series.

---

## 2. Audit cấu trúc và navigation

### 2.1. Dead links và orphan files

**Dead links (TOC tham chiếu file không tồn tại):** 0/91 entries. Sạch.

**Orphan files (file tồn tại nhưng không có trong TOC):** 14 file.

| File | Phân loại | Hành động đề xuất |
|------|-----------|-------------------|
| `0.2 - end-to-end-packet-journey.md` | Block 0 expansion | Thêm vào TOC dưới Block 0 |
| `4.7 - openflow-programming-with-ovs.md` | Block IV expansion | Thêm vào TOC Block IV |
| `9.6 - bonding-and-lacp.md` | Block IX expansion | Thêm vào TOC Block IX |
| `9.7 - port-mirroring-and-packet-capture.md` | Block IX expansion | Thêm vào TOC |
| `9.8 - flow-monitoring-sflow-netflow-ipfix.md` | Block IX expansion | Thêm vào TOC |
| `9.9 - qos-policing-shaping-metering.md` | Block IX expansion | Thêm vào TOC |
| `9.10 - tls-pki-hardening.md` | Block IX expansion | Thêm vào TOC |
| `9.11 - ovs-appctl-reference-playbook.md` | Block IX expansion | Thêm vào TOC |
| `9.12 - upgrade-and-rolling-restart.md` | Block IX expansion | Thêm vào TOC |
| `9.13 - libvirt-docker-integration.md` | Block IX expansion | Thêm vào TOC |
| `9.14 - incident-response-decision-tree.md` | Block IX expansion | Thêm vào TOC |
| `11.3 - gre-tunnel-lab.md` | Phase D expansion | Thêm vào TOC Block XI |
| `11.4 - ipsec-tunnel-lab.md` | Phase D expansion | Thêm vào TOC Block XI |
| `13.13 - ovs-to-ovn-migration-guide.md` | Block XIII expansion | Thêm vào TOC Block XIII |

Nguyên nhân: các file mới được tạo trong Phase B/D nhưng `README.md` TOC chưa cập nhật. `CLAUDE.md` Rule 2 (Cross-File Sync) bị vi phạm 14 lần.

### 2.2. Header block (`> **Trạng thái:**`)

**Tuân thủ:** 94/105 file có header block (89.5%).

**11 file thiếu header block:**

| File | Lý do giả định |
|------|----------------|
| `0.0 - how-to-read-this-series.md` | Intro file, có format khác |
| `0.1 - lab-environment-setup.md` | Intro file |
| `17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | Pre-existing trước Architecture Phase |
| `18.0 - ovn-arp-responder-and-bum-suppression.md` | Pre-existing |
| `19.0 - ovn-multichassis-binding-and-pmtud.md` | Pre-existing |
| `9.18 - ovs-native-l3-routing.md` | Phase B content (cần backfill) |
| `9.19 - ovs-flow-table-granularity.md` | Phase B content |
| `9.20 - ovs-vlan-access-trunk.md` | Phase B content |
| `9.22 - ovs-multi-table-pipeline.md` | Phase D session 22+23 |
| `9.23 - ovs-stateless-acl-firewall.md` | Phase D session 22+23 |
| `9.25 - ovs-flow-debugging-ofproto-trace.md` | Phase D session 24 |

Intro file (0.0, 0.1) có thể chấp nhận format riêng. 9 file còn lại nên backfill header block (trạng thái, block, prerequisites, ebook mapping) để consistency.

### 2.3. Naming convention

105/105 file tuân thủ pattern `X.Y - kebab-case.md`. Các file `4.0 - openflow-1.1-multi-table-groups.md` chứa `1.1` trong slug là version number, không phải vi phạm convention.

---

## 3. Audit Rule 11 (Vietnamese Prose Discipline)

Quick scan dùng regex `§11.6` mở rộng (paradigm/architecture/approach/deployment/adoption/trade-off/.../tracking/monitor/event) trên 105 file.

**Tổng hits raw:** 2.300 (sau khi loại trừ code block + URL + markdown link).

**Phân bổ:**

| Mức nghiêm trọng | Số file | Threshold |
|------------------|---------|-----------|
| Critical (>50 hits) | 7 | 19.0, 3.2, 17.0, 2.1, 3.1, 6.0, 4.6 |
| High (30-49 hits) | 17 | 2.4, 5.0, 3.0, 4.1, 5.2, 4.4, 0.2, 4.7, 15.1, 2.2, 2.3, 1.2, 7.2, 14.0, 4.0, 4.2, 4.3 |
| Medium (10-29 hits) | 49 | (xem phụ lục) |
| Low (<10 hits) | 32 | OK, hits chủ yếu là technical concept |

**Cảnh báo:** Quick scan này KHÔNG phân biệt được giữa "concept name (giữ English)" và "prose violation (dịch Việt)". Cần human review per file.

### 3.1. Sample violations xác nhận trong top file

File `19.0 - ovn-multichassis-binding-and-pmtud.md`:

| Dòng | Pattern | Phân loại | Suggested fix |
|------|---------|-----------|----------------|
| 99 | "Bảng đọc theo chiều **trade-off**" | Prose violation | "đánh đổi" |
| 362 | "behavior" | Prose | "hành vi" |
| 484 | "OVN không **bypass** các rule này" | Prose | "né các rule này" |
| 348 | "tận dụng fabric cho **performance**" | Prose | "hiệu năng" |
| 348 | "không thể mix **version**" | Prose | "phiên bản" |
| 502 | "Bản vá 6 dòng là workaround" | Prose | "biện pháp tạm thời" |

File `3.2 - onf-formation-and-governance.md`:

| Dòng | Pattern | Phân loại | Suggested fix |
|------|---------|-----------|----------------|
| 35 | "operator-driven model là **unusual** và **significant** cho **industry dynamics**" | Multiple violations | "mô hình do người vận hành dẫn dắt là bất thường và có ý nghĩa lớn cho động lực ngành" |
| 49 | "Advocate for and **promote the adoption of** SDN" | Prose | "thúc đẩy sự chấp nhận của" (giữ trong dấu ngoặc kép vì là quote chính thức ONF — quote thì giữ English) |
| 61 | "Operator **worry** rằng spec sẽ bị **bent** để **favor** vendor" | Prose | "lo ngại rằng spec sẽ bị bẻ cong để ưu ái" |

### 3.2. Khuyến nghị

Phân loại 7 file Critical theo nguồn gốc:

- `19.0`, `17.0`, `18.0` (3 file Block XVII-XIX): pre-existing trước Rule 11 (session 13). **Cần retrofit toàn bộ.**
- `3.2`, `3.1`, `3.0`, `2.1`, `2.4`, `4.6`, `5.0`, `6.0`: viết trong Phase B Block II-VI, **đã từng retrofit ở session 13** (commit `c78cb39`, `739db7f`, `3a92e27`) nhưng vẫn còn nhiều prose violations. Cần audit pass thứ 2.
- `0.2`, `4.7`, `15.1`: viết trong Phase B nhưng dictionary §11.2 còn thiếu một số từ (ví dụ: "consumer", "buy-in", "shepherd"). Cần bổ sung dictionary trong CLAUDE.md.

**Effort estimate:** 7 Critical files × ~30 phút audit/file = ~3.5 giờ. 17 High files × ~15 phút = ~4 giờ. Tổng ~8 giờ retrofit.

---

## 4. Audit Rule 13 (Em-dash Discipline)

Quy tắc: target < 0.10 em-dash/dòng, threshold violation > 0.10.

**Tổng em-dash:** 2.072 trên 31.529 dòng. Mật độ trung bình toàn curriculum: 0.066 (chấp nhận được).

**Phân bổ:**

| Phân loại | Số file | % |
|-----------|---------|---|
| OK (< 0.05) | 40 | 38.1% |
| Warning (0.05-0.10) | 34 | 32.4% |
| **Violation (> 0.10)** | **31** | **29.5%** |

### 4.1. Top 10 violators (cần fix priority)

| File | Em-dash | Lines | Ratio | Note |
|------|--------|-------|-------|------|
| `13.8 - ovn-northd-translation.md` | 78 | 261 | **0.299** | Worst offender |
| `0.2 - end-to-end-packet-journey.md` | 75 | 343 | 0.219 | Cũng vi phạm Rule 11 |
| `9.0 - ovs-history-2007-present.md` | 53 | 259 | 0.205 | |
| `7.3 - vendor-controllers-aci-contrail.md` | 38 | 192 | 0.198 | |
| `13.7 - ovn-controller-internals.md` | 63 | 335 | 0.188 | |
| `13.10 - ovn-dhcp-dns-native.md` | 44 | 273 | 0.161 | |
| `9.19 - ovs-flow-table-granularity.md` | 44 | 279 | 0.158 | |
| `13.11 - ovn-gateway-router-distributed.md` | 42 | 269 | 0.156 | |
| `7.2 - onos-service-provider-scale.md` | 23 | 159 | 0.145 | |
| `9.20 - ovs-vlan-access-trunk.md` | 48 | 338 | 0.142 | |

### 4.2. Cụm vi phạm theo block

- **Block VII (controllers):** 4/6 file violation (7.0, 7.1, 7.2, 7.3) — pattern viết kế thừa giữa 4 file.
- **Block IX (9.x):** 7/25 file violation, tập trung 9.0, 9.1, 9.2, 9.3, 9.15-9.20 — Phase B content lúc đó chưa có Rule 13.
- **Block XIII (OVN extended):** 5/14 file violation (13.7-13.12) — viết liên tục cùng pattern session 17, chưa retrofit Rule 13.
- **Block XIV-XVI (P4/DPDK):** 5/9 file violation — viết cùng style.

### 4.3. Khuyến nghị retrofit

Áp dụng pattern script đã dùng cho 9.22-9.25 (session 24, commit `66b4a64`+`85e6cbd`):

```bash
# Pass 1: bullet definition "- X — Y" → "- X: Y"
# Pass 2: Vietnamese sentence split (period + capital Việt)
# Pass 3: comma split khi continuation
# Manual review cho dangling markup
```

Effort estimate: 31 file × ~10 phút (do có script automation) = ~5 giờ tổng.

---

## 5. Audit URL validity và technical spot-check

### 5.1. URL coverage

- 502 unique URLs, top 10 domains chiếm 80% references.
- Domain phân bố healthy: man7.org (89), github.com (87), docs.openvswitch.org (82), rfc-editor.org (77), opennetworking.org (70), ovn.org (27), kernel.org (15).

### 5.2. Sample HTTP verification (26 URL từ critical domains)

| Status | Count | Notes |
|--------|-------|-------|
| 200 OK | 25 | 96.2% pass rate |
| **404** | 1 | `https://docs.openvswitch.org/en/latest/intro/install/upgrade/` |

**Dead URL khẳng định:** `docs.openvswitch.org/en/latest/intro/install/upgrade/` xuất hiện trong:

- `9.12 - upgrade-and-rolling-restart.md`
- `10.2 - ovsdb-backup-restore-compact-rbac.md`

**URL thay thế đề xuất:** Trang upgrade hiện tại tại OVS docs đã đổi cấu trúc. Cần kiểm tra `https://docs.openvswitch.org/en/latest/topics/upgrades/` hoặc `https://docs.openvswitch.org/en/latest/intro/install/general/`.

### 5.3. Technical spot-check (sample claims)

| Claim | Source | Verdict |
|-------|--------|---------|
| ONF founding date 21/03/2011 | 6 file (2.4, 3.0, 3.1, 3.2, 7.x) | ✅ Verified vs `opennetworking.org/news-and-events/press-releases/open-networking-foundation-established/` |
| 6 founding operators (DT, FB, Google, MS, Verizon, Yahoo) | 3.2 dòng 16, 77-83 | ✅ Verified |
| OVS 2.17.9 + OVN 22.03.8 trong Ubuntu 22.04 jammy-updates | 0.1 dòng 50, 98-100 | ✅ Match Canonical pocket (verified via Launchpad) |
| OVN 22.09 multichassis | 19.0 dòng 362, 348 | ✅ Match commit `10398c1f51d54d5c3f8ec391a0f8de0bc76a927d` cited |
| OpenFlow 1.0 spec 31/12/2009 | 3.1 dòng 42 | ✅ Match ONF archive |
| Stanford Clean Slate 2006-2012 | 3.0 dòng 200 | ✅ Verified |
| `man7.org/linux/man-pages/man8/ovn-trace.8.html` | Multi files | ✅ 200, content present (có thể giữ man7.org thay vì ovn.org) |

**Coverage:** 7/7 critical claims spot-checked = OK. Quick scan, không exhaustive.

---

## 6. Tổng hợp ưu tiên fix

### 6.1. P0 — Pre-flight blocker (sửa trước commit tiếp theo)

1. **Cập nhật `sdn-onboard/README.md` TOC** — bổ sung 14 orphan file. Effort: 30 phút. Risk nếu bỏ: user mất navigation tới 14 file.
2. **Fix dead URL `docs.openvswitch.org/en/latest/intro/install/upgrade/`** ở 2 file. Effort: 15 phút.

### 6.2. P1 — High value retrofit (1-2 session)

3. **Backfill header block** cho 9 file Phase B/D (loại 0.0, 0.1). Effort: 1.5 giờ.
4. **Rule 13 em-dash retrofit** cho top 10 violators (>0.14 ratio). Có script reusable từ session 24. Effort: 2-3 giờ.

### 6.3. P2 — Major debt cleanup (3-5 session)

5. **Rule 11 prose retrofit pass 2** cho 7 Critical file (đặc biệt 19.0, 17.0, 18.0 chưa từng được audit Rule 11). Effort: 8 giờ.
6. **Rule 13 retrofit còn lại** 21 file violation (0.10-0.14 ratio). Effort: 3 giờ.
7. **Bổ sung dictionary §11.2** với từ mới phát hiện ("consumer", "buy-in", "shepherd", "worry", "favor", "bent"). Effort: 30 phút (cùng commit fix).

### 6.4. P3 — Continuous improvement

8. **Cập nhật `CLAUDE.md` "Current State" table** — đang stale, vẫn ghi HEAD `85e6cbd` nhưng git HEAD thực tế là `41f6533`. Bổ sung session 24 deltas (Part 9.21, 9.25, Rule 13 retrofit).
9. **Cập nhật `memory/session-log.md`** — chưa có entry session 24+25.
10. **Cập nhật `memory/file-dependency-map.md`** — chưa map orphan file mới.

---

## 7. Đánh giá tổng quan curriculum

**Điểm mạnh:**

- Quy mô lớn (105 file, ~32K dòng) với coverage end-to-end OVS/OpenFlow/OVN.
- Naming convention 100% tuân thủ.
- 0 dead links trong TOC (sau khi sửa URL encoding bug trong audit script).
- URL technical accuracy cao (96% pass rate trên sample).
- Technical claims cite được verify (ONF, OVS/OVN versions, OpenFlow timeline).
- Block IX (25 file) và Block XIII (14 file) cung cấp depth thực sự cho core topics.

**Điểm yếu cần fix:**

- 14 orphan file (Rule 2 violation) — cần update TOC.
- 31 file vi phạm Rule 13 (29.5% curriculum) — em-dash density trên ngưỡng.
- 7 file Critical Rule 11 prose violation — đặc biệt 19.0/17.0/18.0 chưa từng retrofit.
- 9 file thiếu header block convention.
- Memory files (CLAUDE.md, session-log.md) stale so với git HEAD thực tế.

**Mức độ trưởng thành:** Curriculum đã đạt **content completeness** (Phase B done) nhưng còn **consistency debt** từ các session trước khi Rule 11+13 ra đời. Tổng effort fix ước tính **~17-20 giờ** chia đều cho 3-4 session tới.

---

## 8. Phụ lục

### 8.1. Hit count Rule 11 — full list (105 file)

Dữ liệu raw lưu tại `/tmp/sdn-onboard-rule11-hits.txt`. Tóm tắt phân tầng đã trình bày §3.

### 8.2. Em-dash density — full list

Dữ liệu raw đã trình bày trong §4 với 31 violator + 34 warning + 40 OK.

### 8.3. URL list

502 unique URLs lưu tại `/tmp/sdn-urls.txt`. Đã verify mẫu 26 URL critical, dead rate 1/26 = 3.8%.

### 8.4. Skill stack đã sử dụng

| Skill | Vai trò trong audit |
|-------|---------------------|
| professor-style | Đánh giá giọng văn, cấu trúc khái niệm, tiêu chí Bloom |
| document-design | Đánh giá header block, naming convention, TOC integrity |
| fact-checker | Verify ONF date, OVN version, OVS package version |
| web-fetcher | HTTP HEAD check 26 URL critical |

---

**End of audit report.** Resume point: §6 ưu tiên P0 → P1 → P2 → P3 ở session 25.
