# File Dependency Map

> Bản đồ phụ thuộc giữa các file trong repo. Khi sửa file A, PHẢI kiểm tra tất cả
> file mà A tham chiếu hoặc được tham chiếu bởi — để tránh lỗi đồng bộ.
>
> **Cách dùng:** Trước khi commit, tra bảng dưới → tìm file đang sửa → kiểm tra cột "Related Files".

---

## Bảng phụ thuộc chính

### Tầng 1: README files (TOC và navigation)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `README.md` (root) | Entry point repo, liệt kê tất cả series (Linux, Cisco, SDN, HAProxy) | `haproxy-onboard/README.md`, `sdn-onboard/README.md`, `linux-onboard/`, `network-onboard/` |
| `haproxy-onboard/README.md` | TOC 29 Parts, Knowledge Dependency Map, Phụ lục A (Version Evolution Tracker — 52 entries, 12 categories) | `README.md` (root — version refs), MỌI file Part `*.md` (tên Part phải khớp TOC), `memory/haproxy-series-state.md` (tên Part phải khớp) |
| `sdn-onboard/README.md` | TOC 2 Parts, dependency graph, log file metadata | `README.md` (root — SDN section), `sdn-onboard/1.0`, `sdn-onboard/2.0` (section titles phải khớp TOC) |

### Tầng 2: Content files (Parts)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `haproxy-onboard/1.0 - haproxy-history-and-architecture.md` | Part 1: history, architecture, process model | `haproxy-onboard/README.md` (TOC entry, dependency graph, Phụ lục A nếu có version-specific content), `README.md` (root — summary) |
| `linux-onboard/file-descriptor-deep-dive.md` | FD deep-dive: TLPI 3-table, epoll, CLOEXEC (1261 lines, 14 figures) | 14 SVGs trong `images/fd-*.svg` (Tầng 5), `README.md` (root — nếu có link) |

> **Template cho Parts mới:** Copy dòng trên và điều chỉnh. Mỗi Part mới phải được thêm vào bảng này.

### Tầng 3: Reference files

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| _(Không còn file riêng — Version Evolution Tracker đã tích hợp vào `haproxy-onboard/README.md` Phụ lục A)_ | — | — |

> **Lưu ý:** `haproxy-onboard/references/haproxy-version-evolution.md` đã được migrate vào Phụ lục A của `haproxy-onboard/README.md` (session 2026-03-30). File gốc cần xóa trên local (`git rm`).

### Tầng 4: Memory và config files

| File | Nội dung chính | Related Files |
|------|---------------|---------------|
| `CLAUDE.md` | Working memory, rules, current state | `memory/session-log.md`, `memory/haproxy-series-state.md`, `memory/experiment-plan.md` |
| `memory/session-log.md` | Log session gần nhất | `CLAUDE.md` (Current State section) |
| `memory/haproxy-series-state.md` | Trạng thái từng Part | `haproxy-onboard/README.md` (TOC) |
| `memory/experiment-plan.md` | Kế hoạch thí nghiệm 5 phases (A→E) | `CLAUDE.md`, `linux-onboard/file-descriptor-deep-dive.md` (exercise inventory) |

### Tầng 2b: SDN onboard series

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/README.md` | TOC SDN series, dependency graph, log file metadata | `README.md` (root — SDN section), `sdn-onboard/1.0`, `sdn-onboard/2.0`, `sdn-onboard/3.0` (section titles phải khớp TOC) |
| `sdn-onboard/1.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | OVN L2 Forwarding, FDB Poisoning case study VLAN 3808, multichassis/claim high-level, FDP-620 trigger conditions (1178 lines sau khi trim §1.6 deep-dive sang Part 3 ngày 2026-04-20, production log forensics) | `README.md` (root — SDN section), `sdn-onboard/README.md` (TOC), `sdn-onboard/2.0` nếu 2.0 cross-reference 1.0, `sdn-onboard/3.0` (cross-refs bidirectional: Part 1 § 1.6 liên kết tới Part 3 §3.2/3.4/3.5/3.6) |
| `sdn-onboard/2.0 - ovn-arp-responder-and-bum-suppression.md` | OVN ARP Responder, BUM suppression (496 lines, rewritten 2026-04-10) | `sdn-onboard/README.md` (TOC), `sdn-onboard/1.0` (cross-references đến tunnel key, localnet port, MC_FLOOD từ Part 1) |
| `sdn-onboard/3.0 - ovn-multichassis-binding-and-pmtud.md` | OVN multichassis binding lifecycle + Geneve PMTUD bug FDP-620 root cause + RARP activation-strategy + 3 Labs (1379 lines) | `sdn-onboard/README.md` (TOC), `sdn-onboard/1.0` (live migration trigger, localnet, Chassis/Claim baseline), `README.md` (root — SDN section) |

> **Quy tắc:** Khi sửa SDN 1.0, kiểm tra SDN 2.0 có references đến localnet/MC_UNKNOWN không, và SDN 3.0 có cross-ref đến live migration/multichassis của Part 1 không. Khi sửa SDN 2.0, kiểm tra SDN 1.0 có concepts nào được tái sử dụng không. Khi sửa SDN 3.0, kiểm tra consistency với Part 1 section 1.2 (Chassis/Claim) và section 1.6 (live migration trigger).

### Tầng 5: Image files (SVG → Markdown captions)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `images/fd-kernel-3-table-model.svg` | Figure 1-1: TLPI Three-Table Model (pure, no fork/exec) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~141) |
| `images/fd-exercise1-initial-open-read.svg` | Figure 1-2: Guided Exercise 2 baseline — 1 FD, 1 OFD, pos=5 | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~195) |
| `images/fd-exercise1-after-dup.svg` | Figure 1-3: Guided Exercise 2 sau dup() — FD 3,4 → OFD "A" | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~228) |
| `images/fd-exercise1-after-open-independent.svg` | Figure 1-4: Guided Exercise 2 sau open() độc lập — 2 OFDs | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~250) |
| `images/fd-exercise1-read-offset-sharing.svg` | Figure 1-5: Guided Exercise 2 final — open()+dup()+fork() | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~346) |
| `images/fd-exercise2-dup-write.svg` | Figure 1-6: Guided Exercise 3 Phần E — dup write nối tiếp | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~402) |
| `images/fd-exercise2-open-write.svg` | Figure 1-7: Guided Exercise 3 Phần F — open write đè dữ liệu | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~427) |
| `images/fd-exercise2-fork-write.svg` | Figure 1-8: Guided Exercise 3 Phần G — fork write xuyên process | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~457) |
| `images/fd-exercise3-status-flags-sharing.svg` | Figure 1-9: Guided Exercise 4 — Status flags sharing qua OFD | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~545) |
| `images/fd-exercise4-lseek-cross-process.svg` | Figure 1-10: Guided Exercise 5 — lseek xuyên process | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~623) |
| `images/fd-epoll-architecture.svg` | Figure 1-11: Kiến trúc epoll — Interest List, Ready List, Kernel Callback | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~823) |
| `images/fd-select-poll-vs-epoll.svg` | Figure 1-12: So sánh select(), poll() và epoll | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~839) |
| `images/fd-fork-exec-cloexec.svg` | Figure 1-13: fork()+exec() trên FD table, CLOEXEC | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~1017) |
| `images/fd-leak-and-cloexec.svg` | Figure 1-14: FD leak comparison (with/without CLOEXEC) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~1023) |

> **Quy tắc Tầng 5 (document-design Rule 8):** Khi sửa SVG, PHẢI đọc và update caption trong CÙNG batch thao tác. KHÔNG được giao SVG mà chưa verify caption. Chạy `svg-caption-consistency.py` trước commit.

> **Bài học từ lỗi thực tế:** Session 2026-03-30, `fd-kernel-3-table-model.svg` được rewrite từ combined diagram (fork+exec+socket) sang pure TLPI model, nhưng caption vẫn mô tả fork() và socket:443. Nguyên nhân: Tầng 5 chưa tồn tại → cross-file sync check bỏ sót hoàn toàn.

---

## Quy tắc đồng bộ cụ thể

### Khi thay đổi version references (HAProxy version, Ubuntu version)

Phải kiểm tra TẤT CẢ file sau:
1. `README.md` (root) — section HAProxy
2. `haproxy-onboard/README.md` — TOC descriptions + Phụ lục A (Version Evolution Tracker)
3. MỌI Part file đã viết — inline version annotations (`> **Lưu ý phiên bản:**`)

**Bài học từ lỗi thực tế:** Session ngày 2026-03-29, sửa `haproxy-onboard/README.md` từ HAProxy 3.2 → 2.0 nhưng QUÊN `README.md` (root) vẫn còn "HAProxy 3.2". Phát hiện nhờ professor-style review, sửa trong commit `3535f14`.

### Khi thêm Part mới

1. Tạo file Part: `haproxy-onboard/X.0 - <name>.md`
2. Cập nhật `haproxy-onboard/README.md` — TOC entry + Mermaid dependency graph + reading path
3. Cập nhật `memory/haproxy-series-state.md` — thêm dòng mới
4. Cập nhật `memory/file-dependency-map.md` (file này) — thêm entry Part mới
5. Nếu có version-specific content: cập nhật Phụ lục A trong `haproxy-onboard/README.md`

### Khi sửa Mermaid dependency graph

1. Sửa graph trong `haproxy-onboard/README.md`
2. Cập nhật reading path description (cùng file, ngay dưới graph)
3. Kiểm tra `memory/haproxy-series-state.md` — prerequisites column có consistent không
