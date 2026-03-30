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
| `README.md` (root) | Entry point repo, liệt kê tất cả series, HAProxy version refs | `haproxy-onboard/README.md` (version refs phải khớp), `linux-onboard/`, `network-onboard/` |
| `haproxy-onboard/README.md` | TOC 29 Parts, Knowledge Dependency Map, Phụ lục A (Version Evolution Tracker — 52 entries, 12 categories) | `README.md` (root — version refs), MỌI file Part `*.md` (tên Part phải khớp TOC), `memory/haproxy-series-state.md` (tên Part phải khớp) |

### Tầng 2: Content files (Parts)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `haproxy-onboard/1.0 - haproxy-history-and-architecture.md` | Part 1: history, architecture, process model | `haproxy-onboard/README.md` (TOC entry, dependency graph, Phụ lục A nếu có version-specific content), `README.md` (root — summary) |
| `linux-onboard/file-descriptor-deep-dive.md` | FD deep-dive: TLPI 3-table, epoll, CLOEXEC (791 lines) | 5 SVGs trong `images/fd-*.svg` (Tầng 5), `README.md` (root — nếu có link) |

> **Template cho Parts mới:** Copy dòng trên và điều chỉnh. Mỗi Part mới phải được thêm vào bảng này.

### Tầng 3: Reference files

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| _(Không còn file riêng — Version Evolution Tracker đã tích hợp vào `haproxy-onboard/README.md` Phụ lục A)_ | — | — |

> **Lưu ý:** `haproxy-onboard/references/haproxy-version-evolution.md` đã được migrate vào Phụ lục A của `haproxy-onboard/README.md` (session 2026-03-30). File gốc cần xóa trên local (`git rm`).

### Tầng 4: Memory và config files

| File | Nội dung chính | Related Files |
|------|---------------|---------------|
| `CLAUDE.md` | Working memory, rules, current state | `memory/session-log.md`, `memory/haproxy-series-state.md` |
| `memory/session-log.md` | Log session gần nhất | `CLAUDE.md` (Current State section) |
| `memory/haproxy-series-state.md` | Trạng thái từng Part | `haproxy-onboard/README.md` (TOC) |

### Tầng 5: Image files (SVG → Markdown captions)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `images/fd-kernel-3-table-model.svg` | Figure 1-1: TLPI Three-Table Model (pure, no fork/exec) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~140, Exam Prep table ~738) |
| `images/fd-fork-exec-cloexec.svg` | Figure 1-1b: fork()+exec() extension, HAProxy CLOEXEC scenario | `linux-onboard/file-descriptor-deep-dive.md` (caption tại section 1.10 ~598, Exam Prep table ~739) |
| `images/fd-epoll-architecture.svg` | Figure 1-2: Kiến trúc epoll — Interest List, Ready List, Kernel Callback | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~398, Exam Prep table ~743) |
| `images/fd-select-poll-vs-epoll.svg` | Figure 1-3: So sánh select(), poll() và epoll | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~414, Exam Prep table ~744) |
| `images/fd-leak-and-cloexec.svg` | Figure 1-4: FD leak comparison (with/without CLOEXEC) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại section 1.10 ~604, Exam Prep table ~747) |

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
