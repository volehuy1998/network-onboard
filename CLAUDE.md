# Project Memory — network-onboard

> **CRITICAL**: Đọc toàn bộ file này TRƯỚC KHI thực hiện bất kỳ thao tác nào.
> File này là working memory của project, được commit vào git và sync qua mọi thiết bị.

## Owner

VO LE (volehuy1998@gmail.com) — Computer Network Engineer, OpenStack/kolla-ansible, SDN/OVN/OVS researcher.

## Repository Structure

```
network-onboard/                    ← Repo root (GitHub: volehuy1998/network-onboard)
├── CLAUDE.md                       ← FILE NÀY — working memory
├── README.md                       ← Parent README (entry point cho toàn bộ repo)
├── memory/                         ← Deep memory — session log, state tracking
│   ├── session-log.md              ← Log của session gần nhất
│   ├── file-dependency-map.md      ← Bản đồ phụ thuộc giữa các file
│   └── haproxy-series-state.md     ← Trạng thái từng Part trong series
├── haproxy-onboard/                ← HAProxy onboard series (29 Parts, 6 Blocks)
│   ├── README.md                   ← TOC + Knowledge Dependency Map + Version Tracker link
│   ├── 1.0 - haproxy-history-and-architecture.md  ← Part 1 (DONE)
│   ├── references/
│   │   └── haproxy-version-evolution.md  ← Version Evolution Tracker (52 entries)
│   └── images/
├── linux-onboard/                  ← Linux/RHCSA onboard series
├── network-onboard/                ← Network/CCNA onboard series
├── references/                     ← Shared references (The Linux Programming Interface, etc.)
└── images/                         ← Shared images
```

## Mandatory Rules — Đọc trước khi làm bất kỳ điều gì

### Rule 1: Skill Activation Sequence (BẮT BUỘC)

Khi viết hoặc sửa file `.md` trong bất kỳ onboard series nào, PHẢI kích hoạt skills theo thứ tự:

```
1. professor-style    → Kiểm soát giọng văn, cấu trúc khái niệm (6 mục: 2.1-2.6)
2. document-design    → Kiểm soát bố cục, heading, learning elements
3. fact-checker       → Xác minh MỌI technical claim trước khi commit
4. web-fetcher        → Xác minh MỌI URL trước khi đưa vào tài liệu
```

**KHÔNG được viết content trước rồi review sau.** Phải đọc skill TRƯỚC → viết → self-audit.

### Rule 2: Cross-File Sync (BẮT BUỘC)

Trước khi commit, kiểm tra `memory/file-dependency-map.md` để xác định file nào bị ảnh hưởng.

Ví dụ thực tế đã xảy ra: sửa `haproxy-onboard/README.md` (version 3.2 → 2.0) nhưng QUÊN sửa `README.md` (parent) — vẫn còn references đến HAProxy 3.2. Nguyên nhân: không có dependency map.

**Quy trình bắt buộc:**
```
1. Xác định file đang sửa
2. Tra dependency map → liệt kê related files
3. Kiểm tra related files có cần cập nhật không
4. Sửa TẤT CẢ related files trong CÙNG commit
```

### Rule 3: Version Annotation Convention

Khi viết nội dung có sự khác biệt giữa các phiên bản HAProxy:

```markdown
> **Lưu ý phiên bản:** <nội dung khác biệt>
```

Đồng thời cập nhật `haproxy-onboard/references/haproxy-version-evolution.md` với entry mới.

### Rule 4: Git Workflow

- **Protected branch**: KHÔNG push trực tiếp lên main/master
- **Commit convention**: Conventional Commits (`feat()`, `fix()`, `docs()`)
- **Branching**: GitHub Flow (main + feature branches)
- Đọc `git-workflow` skill trước mọi thao tác git

### Rule 5: Session Handoff Protocol

Khi KẾT THÚC session (hoặc khi user nói "dừng", "tạm dừng", "kết thúc"):

```
1. Cập nhật memory/session-log.md với:
   - Ngày, thời gian
   - Những gì đã làm (commits, files changed)
   - Những gì CHƯA làm (pending tasks)
   - Branch hiện tại và trạng thái (clean/dirty)
   - Lệnh cần chạy trên local (nếu có, ví dụ: git push)
2. Cập nhật memory/haproxy-series-state.md nếu Part nào thay đổi status
3. Commit memory changes
```

Khi BẮT ĐẦU session mới:
```
1. Đọc CLAUDE.md (file này)
2. Đọc memory/session-log.md → biết context từ session trước
3. Đọc memory/haproxy-series-state.md → biết trạng thái series
4. Kiểm tra git status, git branch, git log
5. Thông báo cho user: "Tôi đã đọc context. Session trước [tóm tắt]. Pending: [danh sách]."
```

### Rule 6: Quality Gate — Pre-flight Checklist (BẮT BUỘC)

> Nguồn gốc: `.claude-skills/quality-gate/SKILL.md` — tích hợp trực tiếp vào đây để enforcement.
> Lý do: skill nằm trong repo nhưng ngoài danh sách registered skills → không bao giờ được trigger tự động.
> Bài học: session trước đã viết section 1.10 (close-on-exec) mà bỏ qua quality-gate hoàn toàn.

**Checklist B — TRƯỚC KHI viết/sửa file .md (BẮT BUỘC):**
```
□ 1. Kích hoạt professor-style SKILL → nắm 6 criteria (2.1-2.6)
□ 2. Kích hoạt document-design SKILL → nắm chapter template, heading rules
□ 3. Xác định file đang sửa
□ 4. Tra memory/file-dependency-map.md → liệt kê related files
□ 5. Đọc related files để biết content hiện tại
□ 6. BẮT ĐẦU viết/sửa (KHÔNG viết trước bước 1-5)
```

**Checklist C — TRƯỚC KHI commit (BẮT BUỘC):**
```
□ 1. Fact-check: liệt kê MỌI technical claims → verify từng claim
□ 2. URL check: liệt kê MỌI URLs → verify bằng web-fetcher hoặc curl
□ 3. Cross-file sync: tra dependency map → kiểm tra related files
□ 4. Version annotation: nếu có cross-version content → thêm callout + update tracker
□ 5. Git workflow skill: đọc trước khi commit
□ 6. Self-audit professor-style: chạy 6 criteria (2.1-2.6) lên content vừa viết
```

**Checklist E — Khi thêm Part mới (BẮT BUỘC):**
```
□ 1. Chạy Checklist B
□ 2. Tạo file theo convention: X.0 - <name>.md
□ 3. Include header block + learning objectives theo document-design
□ 4. Cập nhật README.md (TOC, dependency graph)
□ 5. Cập nhật memory/haproxy-series-state.md
□ 6. Cập nhật memory/file-dependency-map.md
□ 7. Chạy Checklist C
```

**Nguyên tắc:** Checklist không phải bureaucracy — giống pre-flight check phi công. Overhead 2-3 phút. Chi phí lỗi đồng bộ: phải sửa lại session sau, tốn thêm commit, có thể bỏ sót.

## Current State

| Key | Value |
|-----|-------|
| Active branch | `fix-haproxy-readme-audit` |
| Base version | HAProxy 2.0 on Ubuntu 20.04 (Canonical repo) |
| Parts completed | Part 1 only |
| Parts total | 29 (6 Blocks) |
| Last commit | `bdbff8f` — fix knowledge dependency map |
| Pending push | `git push origin fix-haproxy-readme-audit` |
| Pending PR | Chưa tạo PR cho branch `fix-haproxy-readme-audit` |

## Skill Quick Reference

| Skill | Khi nào dùng |
|-------|-------------|
| professor-style | MỌI nội dung giảng dạy, viết .md, giải thích kỹ thuật |
| document-design | MỌI file .md trong onboard series |
| fact-checker | MỌI technical claim, CLI command, config directive |
| web-fetcher | MỌI URL cần fetch hoặc verify |
| git-workflow | MỌI thao tác git: commit, push, branch, PR |
| flow-graph | Sequence diagram, protocol flow, handshake diagram |
| quality-gate | MỌI thao tác viết/sửa/commit — pre-flight checklist (Rule 6 ở trên) |

## Preferences

- Accuracy first — double-check everything, cross-reference multiple sources
- No AI writing patterns — professor/PhD teaching style
- No emoji in technical content
- Real examples with verifiable output
- Concise but deep — analyst/engineer tone, not mechanical
- Vietnamese language for documentation content
