# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-03-30
**Branch:** `master` (sau khi merge PR #25)
**Base:** `master`

### Đã hoàn thành

1. **PR #25 merged** — feat: add Linux FD deep-dive, HAProxy Part 1 restructure, and SVG audit infrastructure
   - Squash merge commit: `f3256f9`
   - 9 commits gộp thành 1

2. **Linux FD Deep-Dive** (`linux-onboard/file-descriptor-deep-dive.md`)
   - 791 dòng, TLPI Section 5.4 three-table model
   - Các chủ đề: FD table, Open File Table, i-node table, dup(), fork(), exec(), CLOEXEC, epoll
   - 5 SVG figures: fd-kernel-3-table-model, fd-fork-exec-cloexec, fd-epoll-architecture, fd-select-poll-vs-epoll, fd-leak-and-cloexec

3. **SVG Audit Infrastructure** (tạo mới sau khi phát hiện SVG-caption inconsistency)
   - Root cause analysis: SVG rewritten nhưng caption không update
   - Tạo document-design Rule 8: SVG-Caption Atomic Consistency
   - Tạo `svg-caption-consistency.py` (entity extraction + mismatch detection)
   - Tạo Tầng 5 trong `memory/file-dependency-map.md` (image→markdown mapping)
   - Cập nhật Checklist B (§5b, §6b) và Checklist C (§5a, §5b) trong CLAUDE.md
   - Đã cài `document-design.skill` vào Claude Desktop

4. **HAProxy Part 1 restructure** (từ session trước, included trong PR #25)
   - Professor-style review, version correction 3.2→2.0
   - 52-entry version evolution tracker
   - Knowledge dependency map fixes (7 edges)

### Chưa hoàn thành (Pending)

- [ ] **HAProxy Parts 2-29**: Chưa bắt đầu (28/29 remaining)
- [ ] **Linux FD doc — thêm sections**: Có thể mở rộng thêm về epoll edge-triggered, signalfd, eventfd
- [ ] **Cleanup**: `document-design.skill` và `pr-body.txt` trong repo root (untracked, nên xóa)
- [ ] **references/ folder**: Chứa "The Linux Programming Interface.pdf" — chưa track (file lớn, cân nhắc .gitignore hoặc Git LFS)

### Git State khi kết thúc

```
Branch: master
Status: clean (tại f3256f9)
Remote: up to date with origin/master
Untracked files: .claude/, document-design.skill, pr-body.txt (tạm, không cần commit)
```

### Lệnh cần chạy trên local

```bash
# Không có lệnh pending — master đã push và PR đã merge
# Nếu muốn cleanup:
rm document-design.skill pr-body.txt
```

### Bài học rút ra từ session này

1. **SVG-caption phải sửa atomic**: Khi rewrite SVG, caption PHẢI update ngay trong cùng thao tác
2. **Root cause trước fix**: User yêu cầu đúng — điều tra nguyên nhân → tạo prevention → rồi mới fix
3. **PowerShell không hỗ trợ heredoc**: Dùng `--body-file` thay vì `--body` khi tạo PR từ PowerShell/VSCode terminal
4. **CRLF vs LF**: Windows tạo CRLF, git cần LF — cân nhắc `.gitattributes` để auto-normalize

---

## Lịch sử sessions trước

### Session 2026-03-29

**Branch:** `fix-haproxy-readme-audit`

**Đã hoàn thành:**
1. Commit `3d82766` — fix(haproxy): correct factual errors and add missing dependency in README TOC
2. Commit `10c3a17` — docs(haproxy): add document-design structure and fix cross-references in Part 1
3. Commit `3535f14` — fix(haproxy): update version refs to HAProxy 2.0 and enhance Part 1 with professor-style review
4. Commit `919341b` — feat(haproxy): add version evolution tracker for cross-version changes
5. Commit `bdbff8f` — fix(haproxy): update knowledge dependency map with 7 corrected edges
6. Tạo CLAUDE.md + memory system

_(Giữ tối đa 5 entries.)_
