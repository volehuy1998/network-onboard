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

Khi **viết, sửa, hoặc audit/review** file `.md` trong bất kỳ onboard series nào, PHẢI kích hoạt skills theo thứ tự:

> **Bài học từ lỗi thực tế (session 2026-03-30):** Audit Part 1 + cấu trúc series nhưng chỉ
> kích hoạt 2/4 skills (professor-style, document-design), bỏ qua fact-checker và web-fetcher.
> Kết quả: phát hiện lỗi cấu trúc nhưng bỏ sót lỗi factual và dead links.
> Nguyên nhân: diễn giải sai "viết hoặc sửa" → coi audit là "chỉ đọc" → bỏ qua verification.
> **Quy tắc: 4 skills LUÔN kích hoạt cho MỌI tương tác với file .md — không có ngoại lệ.**

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

**Checklist B — TRƯỚC KHI viết/sửa/audit file .md HOẶC .svg (BẮT BUỘC):**
```
□ 1. Kích hoạt professor-style SKILL → nắm 6 criteria (2.1-2.6)
□ 2. Kích hoạt document-design SKILL → nắm chapter template, heading rules, Rule 8
□ 3. Xác định file đang sửa
□ 4. Tra memory/file-dependency-map.md → liệt kê related files (kể cả Tầng 5: SVG↔markdown)
□ 5. Đọc related files để biết content hiện tại
□ 5b. NẾU sửa SVG: grep tất cả .md tham chiếu SVG → đọc caption hiện tại → ghi nhận entity
□ 6. BẮT ĐẦU viết/sửa (KHÔNG viết trước bước 1-5b)
□ 6b. NẾU sửa SVG: update caption NGAY SAU khi hoàn thành SVG — trước bất kỳ task khác
```

**Checklist C — TRƯỚC KHI commit (BẮT BUỘC):**
```
□ 1. Fact-check: liệt kê MỌI technical claims → verify từng claim
□ 2. URL check: liệt kê MỌI URLs → verify bằng web-fetcher hoặc curl
□ 3. Cross-file sync: tra dependency map → kiểm tra related files
□ 4. Version annotation: nếu có cross-version content → thêm callout + update tracker
□ 5a. SVG spacing+diacritics: nếu có SVG mới/sửa → chạy svg-audit.py + diacritics-audit.py (Rule 6). 0 violation.
□ 5b. SVG-caption consistency: chạy svg-caption-consistency.py cho mỗi SVG đã sửa (Rule 8). 0 mismatch.
□ 6. Git workflow skill: đọc trước khi commit
□ 7. Self-audit professor-style: chạy 6 criteria (2.1-2.6) lên content vừa viết
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

### Rule 7: Terminal Output Fidelity (BẮT BUỘC)

> Nguồn gốc: session 2026-04-04. Viết unified FD exercise, tự ý cắt output `fdinfo` chỉ giữ `pos:`,
> bỏ `flags:` và `mnt_id:`. User đưa output thật đầy đủ 3 dòng và yêu cầu "không được cắt bớt một
> chữ nào" — nhưng Claude vẫn tuyên bố "khớp hoàn hảo" vì chỉ so giá trị `pos` mà không đếm số dòng.
> Nguyên nhân gốc: không có quy tắc nào trong CLAUDE.md hoặc skills bắt buộc giữ nguyên output.

**Quy tắc:**

Khi user cung cấp terminal output thực để thay thế vào tài liệu:

```
1. KHÔNG được cắt bớt, rút gọn, hoặc lược bỏ bất kỳ dòng nào
2. KHÔNG được sắp xếp lại thứ tự các dòng
3. KHÔNG được thay đổi spacing, indentation, hoặc ký tự nào trong output
4. Khi đối chiếu output: so sánh TỪNG DÒNG (line-by-line diff), không chỉ so giá trị quan tâm
5. Nếu cần rút gọn output vì quá dài: PHẢI hỏi user trước, nêu rõ dòng nào muốn bỏ và lý do
```

Quy tắc này áp dụng cho mọi loại output: `fdinfo`, `lsof`, `ss`, `strace`, `tcpdump`, `haproxy -vv`, log files, và bất kỳ terminal output nào user cung cấp. Output thực là bằng chứng thực nghiệm — cắt bớt bằng chứng là phá hỏng tính xác minh được (reproducibility) của tài liệu.

## Current State

| Key | Value |
|-----|-------|
| Active branch | `master` (dirty — audit changes chưa commit) |
| Base version | HAProxy 2.0 on Ubuntu 20.04 (Canonical repo) |
| Parts completed | Part 1 only (fact-checked, 3 corrections, Quiz added) |
| Parts total | 29 (6 Blocks) |
| Last merged PR | PR #25 — `f3256f9` (squash merge vào master 2026-03-30) |
| Pending push | Có — audit changes cần commit → feature branch → PR |
| Pending PR | Không |
| Version tracker | Tích hợp vào `haproxy-onboard/README.md` Phụ lục A (52 entries, 12 categories). File `references/haproxy-version-evolution.md` cần `git rm` trên local |
| Dependency graph | 4 edges sửa trong session này: P3→P11, P6→P22, +P5→P24, +P3→P21 |
| Root README | HAProxy section thu gọn từ ~245 dòng → 3 dòng (pointer tới haproxy-onboard/README.md) |
| Linux FD doc | `linux-onboard/file-descriptor-deep-dive.md` — 791 lines, 5 SVG figures |
| SVG audit infra | Rule 8 (document-design), svg-caption-consistency.py, Tầng 5 dependency map |
| Installed skill | `document-design.skill` — đã cài Rule 8 (SVG-Caption Atomic Consistency) |

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
