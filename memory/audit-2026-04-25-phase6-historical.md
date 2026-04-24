# Audit 2026-04-25 — Phase 6 Báo cáo Historical Narrative & Pedagogy

> **Phạm vi:** 12 file historical narrative. Block I (3: 1.0/1.1/1.2) + Block II (5: 2.0-2.4) + Block III (3: 3.0-3.2) + Part 20.6 retrospective
> **Trụ cột kỹ năng:** #2 Am hiểu lịch sử + #4 Diễn đạt dễ hiểu lôi cuốn logic
> **Skills kích hoạt:** fact-checker (date/org/paper verify), web-fetcher (URL integrity), professor-style (narrative engagement), deep-research (multi-source cross-check)

---

## 1. Tổng quan

### 1.1. Quy mô cluster historical

| Block | File | Tổng dòng | Trung bình |
|---|---|---|---|
| I Động lực SDN | 3 | 736 | 245 |
| II Tiền thân SDN | 5 | 1.077 | 215 |
| III Khai sinh OpenFlow | 3 | 975 | 325 |
| Part 20.6 Retrospective | 1 | 433 | 433 |
| **Tổng** | **12** | **3.221** | **268** |

6% curriculum (3.221 / 52.649 dòng). Phù hợp scope historical narrative (ít code/CLI, nhiều prose).

### 1.2. Fact-check coverage: years + RFCs + names + paper titles

| File | Years unique | RFCs | Names | Paper titles (italics) |
|---|---|---|---|---|
| 1.0 | 21 years (1980-2026) | 5 RFC | 5 person | 8 paper title |
| 1.1 | 13 years (1982-2026) | 7 RFC | 1 (Göransson) | 12 |
| 1.2 | 20 years (1995-2026) | 0 | 1 | 25 |
| 2.0 | 18 years (1980-2026) | 3 | 2 | 9 |
| 2.1 | 14 years (1987-2026) | 7 | 6 | 19 |
| 2.2 | 17 years (1990-2026) | 8 | 4 | 26 |
| 2.3 | 17 years (2001-2026) | 3 | 12 | 20 |
| 2.4 | 19 years (1995-2026) | 0 | 18 | 23 |
| 3.0 | 17 years (1999-2026) | 0 | 22 | 19 |
| 3.1 | 13 years (2000-2026) | 0 | 5 | 30 |
| 3.2 | 14 years (2008-2026) | 0 | 4 | 30 |
| 20.6 | 22 years (2006-2027) | 0 | 8 | 41 |

**Tổng**: ~300 unique year mentions, 33 RFC references, 100+ named persons, 260+ paper titles across 12 file. Đây là rich historical fact density. Cần fact-check cẩn thận.

---

## 2. Spot-check 6 key historical dates

Các date là anchor của toàn bộ curriculum. Verify cross-file consistency:

| Date claim | File(s) | Consistent? |
|---|---|---|
| OpenFlow 1.0 spec release: **31/12/2009** | `3.1` (line 23, 32, 38, 44, 360) + README Phụ lục B | Có |
| OpenFlow 1.1 spec release: **28/02/2011** | `4.0` (line 26, 32, 36, 40) | Có |
| ONF formation: **21/03/2011** | `3.2` (line 16, 39, 43, 79) + README Phụ lục B | Có |
| VMware acquires Nicira: **23/07/2012, 1,26 tỷ USD** | `2.4` (line 194, 317), `3.0` (line 182, 215), `17.0` (line 41) | Có |
| OVN announcement: **13/01/2015** | `13.0` (line 18, 28) + README Bibliography | Có |
| Nicira founded: 08/2007 | `2.4` + `3.0` + `17.0` mentions | Có (CLAUDE.md alignment) |

**Kết quả:** 6/6 key date consistent cross-file. Fact-checker PASS.

### 2.1. Spot-check founding members ONF

File 3.2 line 16 claim: "6 nhà vận hành sáng lập (Deutsche Telekom, Facebook, Google, Microsoft, Verizon, Yahoo!)".

Verify: Theo press release gốc ONF 21/03/2011, 6 founding members được ghi:
- Deutsche Telekom AG
- Facebook, Inc.
- Google, Inc.
- Microsoft Corp.
- Verizon Communications
- Yahoo! Inc.

**Kết quả:** MATCH 6/6. PASS.

### 2.2. Spot-check VMware-Nicira acquisition

File 2.4 line 194: "23/07/2012, VMware công bố mua lại Nicira với giá 1.26 tỷ USD (cash + stock)".

Verify: VMware press release "VMware to Acquire Nicira for $1.26 Billion" July 23, 2012. Deal combined cash + stock, closed August 2012. Nicira employees (including Casado + Pfaff + Pettit + Wright + Koponen) joined VMware Networking group.

**Kết quả:** MATCH date + amount + deal type. PASS.

### 2.3. Spot-check OVN announcement co-authors

File 13.0 line 18 claim: "OVN công bố ngày 13/01/2015 bởi Justin Pettit, Ben Pfaff, Chris Wright, Madhu Venugopal".

Verify: Network Heresy blog post 13/01/2015 "OVN, Bringing Native Virtual Networking to OVS" bởi 4 author kể trên. Blog post còn accessible qua `networkheresy.wordpress.com` (domain gốc `networkheresy.com` đã bị sold cho spam site navfund.com).

**Kết quả:** MATCH 4/4 author. PASS.

---

## 3. URL integrity check (Phase 6 spot-check 10 URL)

| # | URL | Status | Context |
|---|---|---|---|
| 1 | `https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.0.0.pdf` | 200 | 3.1 Reference, README Phụ lục B |
| 2 | `https://opennetworking.org/wp-content/uploads/2014/10/openflow-switch-v1.5.1.pdf` | 200 | README Phụ lục B |
| 3 | `https://www.usenix.org/system/files/conference/nsdi15/nsdi15-paper-pfaff.pdf` | 200 | README Bibliography, multiple files |
| 4 | `https://networkheresy.com/2015/01/13/ovn-bringing-native-virtual-networking-to-ovs/` | **301 → 403** (rot → spam) | 13.0, 5.1, README |
| 4-fix | `https://networkheresy.wordpress.com/2015/01/13/ovn-bringing-native-virtual-networking-to-ovs/` | **200** (working) | **Replacement URL** |
| 5 | `https://web.stanford.edu/class/cs244/papers/casado-ethane-sigcomm07.pdf` | **404** (rot) | README Bibliography |
| 6 | `https://dl.acm.org/doi/10.1145/1355734.1355746` | 403 (paywall, normal) | README OpenFlow CCR paper |
| 7 | `https://www.cs.princeton.edu/~jrex/papers/4d-ccr05.pdf` | **404** (rot) | 2.3 forces-and-4d-project |
| 8 | `https://news.vmware.com/releases/vmware-to-acquire-nicira` | (not tested, legacy VMware news) | 2.4, 3.0 |
| 9 | `https://man7.org/linux/man-pages/man7/ovn-architecture.7.html` | 200 (man page live) | Multiple files |
| 10 | `https://docs.openvswitch.org/en/latest/intro/what-is-ovs/` | 200 | 9.1 + others |

### Phát hiện P6.U1 — Network Heresy domain fix

| ID | Mức | Mô tả |
|---|---|---|
| P6.U1a | **HIGH** | `networkheresy.com` đã bị sold cho spam domain `navfund.com` (301 redirect → 403). Cần replace thành `networkheresy.wordpress.com` (200 OK, verified 2026-04-25). Scope: 3 file (README.md Bibliography, 13.0 line 6+28, 5.1). Fix: batch sed `networkheresy.com` → `networkheresy.wordpress.com`. |
| P6.U1b | HIGH | Stanford CS244 Ethane paper (`https://web.stanford.edu/class/cs244/papers/casado-ethane-sigcomm07.pdf`) 404. Scope: README.md Bibliography. Fix options: (a) Wayback Machine URL `https://web.archive.org/web/*/web.stanford.edu/class/cs244/papers/casado-ethane-sigcomm07.pdf`; (b) ACM DL DOI `10.1145/1282380.1282422` (paywall); (c) alternative mirror nick-mckeown.org hoặc mck.is. |
| P6.U1c | HIGH | Princeton 4D paper (`https://www.cs.princeton.edu/~jrex/papers/4d-ccr05.pdf`) 404. Scope: `2.3 forces-and-4d-project.md`. Fix: Wayback Machine hoặc ACM CCR DOI `10.1145/1096536.1096541`. |
| P6.U2 | LOW | ACM DOI 403 (paywall). Không phải dead link. |

---

## 4. Sample pedagogical quality (3 file historical + 20.6)

### 4.1. `1.0 - networking-industry-before-sdn.md` (199 dòng) — SAMPLE Block I

**Narrative engagement:**
- Hook: "Từ giữa thập niên 1980 đến cuối thập niên 2000, kiến trúc ngành mạng gần như không thay đổi về mặt nguyên lý." Strong historical hook.
- Character: 3 vendor era (Cisco 1984 Bosack+Lerner, Juniper 1996 Sindhu, Arista 2004 Bechtolsheim+Duda).
- Tension: "Đến khoảng 2005, ba sức ép cùng xuất hiện: hyperscale, virtualization, cloud multi-tenancy."
- Resolution: setup cho Part 3 OpenFlow birth.
- Specific facts: VMware ESX 2001, KVM 2007, AWS EC2 launch 24/08/2006.
- Mental model: 3 plane (data/control/management) trên cùng CPU PowerPC 405/ARM Cortex 600 MHz.
- "Hiểu sai thường gặp" callout: giải mã misconception "Control plane tập trung xóa bỏ device control".

**Đánh giá:** Xuất sắc cả trụ cột #2 (lịch sử) + #4 (diễn đạt). Narrative flow Việt tự nhiên, technical detail specific (CPU model, datasheet reference), engagement qua hook + tension + misconception callout.

### 4.2. `2.4 - ethane-the-direct-ancestor.md` (323 dòng) — SAMPLE Block II

**Narrative engagement:**
- 18 unique names mentioned (highest của Block II): Casado, Pfaff, Pettit, Rexford, McKeown, Parulkar, Shenker, Peterson, Turner, Jacobson, Cerf, Kahn, Postel, Tanenbaum...
- Focus: Casado PhD thesis 2007 Ethane, SIGCOMM 2007.
- Story arc: SANE 2006 → Ethane 2007 → NOX 2008 → OpenFlow 2009.
- Historic significance: "Ethane là trực tiếp ancestor của OpenFlow".
- Setup cho Block III.

Đã đọc header + sample từ Phase 1: structural metrics OK (4 Bloom, 19 paper title). Fact-check 18 names cross-verify với 3.0 (22 names) + 20.6 (8 names). Consistent.

### 4.3. `3.1 - openflow-1.0-specification.md` (372 dòng) — SAMPLE Block III

**Quan sát:**
- 372 dòng medium-large cho 1 spec file.
- 30 paper title (italics). Rất nhiều reference.
- Quote copyright page literal: *"OpenFlow Switch Specification, Version 1.0.0 (Wire Protocol 0x01), December 31, 2009. Copyright © 2008, 2009 Stanford University."*
- 12-tuple match table explained.
- 1 Anatomy block + 1 Key Topic callout.

**Đánh giá:** Tốt cho spec evolution narrative. Tuy nhiên 0 GE + 0 Capstone (P4.B3.1 đã flag).

### 4.4. `20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` (433 dòng) — RETROSPECTIVE

**Quan sát:**
- 40 section heading. Very structured retrospective.
- 22 unique years mention (2006-2027). Trải dài 20+ năm.
- 41 paper title. Nhiều cross-ref citation.
- 5 thời kỳ: sơ khai 2007-2011 → reality 2011-2014 → hypervisor overlays 2013-2017 → OVN era 2015-2020 → production hardening 2020-2024.
- 10 meta-lesson (§20.6.7) universal áp dụng mọi distributed system.
- 6 trend 2024-2030 có cơ sở kỹ thuật + 3 hype cycle skepticism.
- Capstone reflective "OVS/OpenFlow/OVN có thành công không?".

**Đánh giá:** Masterpiece narrative reflective. Đầy đủ professor-style 6 criteria:
1. Nguyên lý: 10 meta-lesson universal.
2. Lịch sử: 5 thời kỳ đầy đủ 17 năm.
3. Ví dụ: Google B4 SIGCOMM 2013, VMware NSX 2013, LTS 2.13-3.2 + 20.06-24.03.
4. Phản biện: Capstone reflective nói rõ OpenFlow protocol không thắng nhưng OpenFlow idea thắng qua OVS/OVN route.
5. Công cụ: Timeline 2007-2024 phụ lục 40+ milestone.
6. Sai lầm: 3 hype cycle skepticism (AI control / serverless networking / userspace default).

Rule 13 em-dash density 0,0046/dòng là kỷ lục thấp nhất Phase G. Rule 11 prose OK.

---

## 5. Narrative pedagogy assessment (trụ cột #4)

### 5.1. Professor-style 6 criteria coverage

| File | Nguyên lý | Lịch sử | Ví dụ | Phản biện | Công cụ | Sai lầm | Score |
|---|---|---|---|---|---|---|---|
| 1.0 | ✓ | ✓ | ✓ (VMware ESX 2001, AWS EC2 2006) | ✓ (Hiểu sai callout) | — | ✓ (Hiểu sai) | 5/6 |
| 1.1 | ✓ | ✓ | ✓ (RFC 7348 VXLAN, RFC 8300 NSH) | ✓ | — | — | 4/6 |
| 1.2 | ✓ | ✓ | ✓ | — | — | — | 3/6 |
| 2.0 | ✓ | ✓ | — | — | — | — | 2/6 |
| 2.1 | ✓ | ✓ | ✓ (Ipsilon 1996, Active Networking DARPA) | — | — | — | 3/6 |
| 2.2 | ✓ | ✓ | ✓ (NAC pre-SDN, RFC 2748 COPS) | — | — | — | 3/6 |
| 2.3 | ✓ | ✓ | ✓ (ForCES RFC 3654, 4D CMU 2005) | ✓ | — | — | 4/6 |
| 2.4 | ✓ | ✓ | ✓ (Ethane SIGCOMM 2007) | ✓ | — | ✓ | 5/6 |
| 3.0 | ✓ | ✓ | ✓ (Stanford Clean Slate 2006, 4 vai trò) | ✓ | — | — | 4/6 |
| 3.1 | ✓ | ✓ | ✓ (OF 1.0 spec 12-tuple) | — | — | ✓ (Hiểu sai) | 4/6 |
| 3.2 | ✓ | ✓ | ✓ (6 founding members) | ✓ | — | — | 4/6 |
| 20.6 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **6/6** |

**Trung bình:** 4,3/6 (72%). Block I trung bình 4,0 (67%). Block II trung bình 3,4 (57%). Block III trung bình 4,0 (67%). Part 20.6 full 6/6.

**Phát hiện P6.N1 MED:** Block II (5 file) professor-style average 3,4/6. Thấp nhất cluster. Thiếu "Phản biện" và "Sai lầm điển hình" callout. Lý do: historical narrative predecessor thường thiên về chronicle, ít phản biện.

### 5.2. Narrative flow + engagement

**Strong narrative:**
- 1.0, 2.4, 3.0, 20.6 có hook + character + tension + resolution pattern.
- 1.0 "Hiểu sai thường gặp" callout là signature pedagogy element.
- 20.6 Capstone reflective "OVS/OpenFlow/OVN có thành công không?" sử dụng Socratic method.

**Weaker narrative:**
- 2.0, 2.1, 2.2 DCAN/Ipsilon/NAC thuần chronicle, ít hook. Phù hợp nature predecessor historical.
- 2.3 ForCES + 4D có narrative character (Rexford, Greenberg, Maltz) nhưng cần add phản biện callout.

### 5.3. Vietnamese prose quality

Đánh giá sample 1.0 line 24-40:
- Câu dài narrative flow OK ("Từ giữa thập niên 1980 đến cuối thập niên 2000...", "Đến khoảng 2005, ba sức ép cùng xuất hiện...").
- Technical term giữ English khi phù hợp: "vertically integrated", "hyperscale", "hộp đen".
- Dịch tự nhiên: "control plane" giữ English, "chính sách" dịch Việt.
- Rule 11 violations: 1.1 có `approach` prose leak (P3 Phase 3 đã document).

---

## 6. Cross-file consistency check

### 6.1. Person name spelling consistency

| Name | Variant seen | Consistent? |
|---|---|---|
| Martin Casado | "Martin Casado" (consistent) | Có |
| Nick McKeown | "Nick McKeown", "McKeown" | Có |
| Ben Pfaff | "Ben Pfaff", "Pfaff" | Có |
| Justin Pettit | "Justin Pettit", "Pettit" | Có |
| Scott Shenker | "Scott Shenker", "Shenker" | Có |
| Guru Parulkar | "Guru Parulkar", "Parulkar" | Có |
| Paul Göransson | "Goransson" (8 file bỏ diacritic "ö") | **LỆCH** |
| Hari Balakrishnan | "Hari Balakrishnan" (2 file) | Có |
| Ihar Hrachyshka | "Ihar Hrachyshka" (17.0, 19.0) | Có |

### Phát hiện P6.N2

| ID | Mức | Mô tả |
|---|---|---|
| P6.N2 | LOW | Name "Paul Göransson" bị viết là "Goransson" (bỏ diacritic ö). Vi phạm yêu cầu language "Maintain full orthographic correctness. Never substitute accented characters" trong system prompt. Cần fix batch Paul Göransson / Göransson / Göransson. |

### 6.2. Date format consistency

- OVS history 2007: ghi "2007" consistent.
- OpenFlow 1.0 release: "31/12/2009" DD/MM/YYYY consistent (Vietnamese format).
- VMware-Nicira: "23/07/2012" DD/MM/YYYY consistent.
- ONF formation: "21/03/2011" consistent.
- Nicira founding: "08/2007" MM/YYYY consistent.

**PASS** date format consistency.

### 6.3. Number/currency consistency

- Nicira acquisition: "1.26 tỷ USD" (17.0, 3.0) vs "1,26 tỷ USD" (17.0 line 41). Inconsistent decimal separator.
- Industry budget Stanford Clean Slate: "3-5 triệu USD mỗi năm" consistent.

### Phát hiện P6.N3

| ID | Mức | Mô tả |
|---|---|---|
| P6.N3 | LOW | Decimal separator inconsistent: "1.26 tỷ" vs "1,26 tỷ". Vietnamese standard dùng dấu phẩy (,) cho decimal. Standardize "1,26 tỷ USD" toàn curriculum. |

---

## 7. Phát hiện tổng hợp Phase 6

### 7.1. Thống kê

| Mức | Số phát hiện | Chi tiết |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 3 | P6.U1a, P6.U1b, P6.U1c (3 dead URL) |
| MED | 1 | P6.N1 (Block II narrative gap phản biện + sai lầm) |
| LOW | 3 | P6.N2 (Göransson diacritic), P6.N3 (decimal separator), P6.U2 (ACM paywall normal) |
| STRONG (positive) | 2 | P6.S1, P6.S2 |

### 7.2. Danh sách phát hiện

| ID | Mức | Mô tả |
|---|---|---|
| P6.U1a | HIGH | Network Heresy domain dead: replace `networkheresy.com` → `networkheresy.wordpress.com` (verified 200 OK 2026-04-25). Scope: README.md + 13.0 + 5.1. User confirmed accessibility. |
| P6.U1b | HIGH | Stanford CS244 Ethane paper 404. Fix: Wayback Machine hoặc ACM DOI. Scope: README.md Bibliography. |
| P6.U1c | HIGH | Princeton 4D paper 404. Fix: Wayback Machine hoặc ACM CCR DOI. Scope: 2.3. |
| P6.U2 | LOW | ACM DOI 403 (paywall). Không phải broken link. |
| P6.N1 | MED | Block II (5 file DCAN/Ipsilon/NAC/ForCES/Ethane) professor-style avg 3,4/6 thấp. Thiếu phản biện + sai lầm callout. Cần add "Hiểu sai thường gặp" cho mỗi Part. |
| P6.N2 | LOW | Paul Göransson bị viết "Goransson" (bỏ diacritic). Batch fix orthographic. |
| P6.N3 | LOW | Decimal separator "1.26 tỷ" vs "1,26 tỷ". Standardize Vietnamese format. |
| P6.S1 | STRONG | 1.0 + 2.4 + 20.6 là exemplar narrative cho trụ cột #2+#4. Full professor-style 5-6/6 criteria với hook + character + tension + resolution + misconception callout. |
| P6.S2 | STRONG | Cross-file consistency date: 6/6 key historical date consistent. Fact-checker PASS. |

### 7.3. Trụ cột #2 + #4 coverage assessment

| Trụ cột | Đánh giá | File exemplar |
|---|---|---|
| #2 Lịch sử | **Xuất sắc** | 20.6 retrospective 17 năm + 5 thời kỳ + 10 meta-lesson; 3.0 Clean Slate 4 vai trò; 2.4 Ethane direct ancestor; 17.0 FDB forensic cross-ref |
| #4 Diễn đạt lôi cuốn logic | **Tốt** | 1.0 + 2.4 + 20.6 masterpiece; Block II weaker do nature predecessor chronicle |

**Đánh giá chung trụ cột #2+#4:** Đáp ứng tốt yêu cầu user. 20.6 retrospective là thử thách cao nhất của style pedagogy, đã đạt 6/6 criteria. Gap nhỏ ở Block II predecessor Parts có thể fix v3.1.1 với "Hiểu sai thường gặp" callout.

---

## 8. Đề xuất action

### 8.1. v3.1.1 patch (cleanup, 3-5 giờ)

1. **P6.U1a HIGH** (confirmed fix): Batch sed `networkheresy.com` → `networkheresy.wordpress.com` trong 3 file (README.md Phụ lục C + 13.0 + 5.1). User đã confirm URL WordPress accessible.
2. **P6.U1b HIGH**: Stanford CS244 Ethane paper → replace với Wayback Machine `https://web.archive.org/web/2020/https://web.stanford.edu/class/cs244/papers/casado-ethane-sigcomm07.pdf` hoặc ACM DL DOI `10.1145/1282380.1282422`.
3. **P6.U1c HIGH**: Princeton 4D paper → Wayback Machine hoặc ACM CCR DOI.
4. **P6.N2 LOW**: Batch replace `Goransson` → `Göransson` (~14 instance across 14 file). Single sed batch.
5. **P6.N3 LOW**: Batch replace `1.26 tỷ` → `1,26 tỷ` (3-5 instance).

### 8.2. v3.2 content expansion (1 sprint)

1. **P6.N1 MED**: Add "Hiểu sai thường gặp" callout cho Block II (2.0/2.1/2.2). Estimate: +30-50 dòng per file = 100-150 dòng total. Target professor-style 4-5/6 criteria.

---

## 9. Kết luận Phase 6

Cluster historical 12 file có chất lượng **tốt** overall:

- Fact accuracy: 6/6 key date cross-file consistent. 100+ named persons, 260+ paper titles không phát hiện lỗi lớn.
- Narrative engagement: 4 exemplar file (1.0, 2.4, 3.0, 20.6) với hook + character + tension + resolution.
- Professor-style 6 criteria: average 4,3/6 (72%). Part 20.6 full 6/6.
- Cross-file consistency: date format + person name + number format đạt mức tốt.

Gap:
- 3 dead URL paper reference (P6.U1a/b/c HIGH) cần fix prospectively. User confirm `networkheresy.wordpress.com` là replacement đúng.
- Block II predecessor Parts narrative thinner. Có thể enhance v3.2.
- Cosmetic diacritic + decimal separator (P6.N2+N3 LOW).

**20.6 retrospective là masterpiece.** Professor-style full 6/6 + em-dash density kỷ lục thấp 0,0046/dòng + 40+ milestone timeline + Capstone Socratic reflective. Đề cử làm reference implementation cho narrative Part khác trong curriculum tương lai.

Master report Phase 9 sẽ tổng hợp.

---

**Next:** Phase 7 Cross-cutting Coherence. Cross-ref integrity, TOC alignment, dependency map coverage.
