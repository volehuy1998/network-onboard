# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-03-30 (session 2 — tiếp nối sau PR #25)
**Branch:** `master` (dirty — audit changes chưa commit)
**Base:** `master` tại `f3256f9`

### Đã hoàn thành

1. **Audit toàn diện cấu trúc HAProxy + Part 1** (user request trước khi bắt đầu Part 2)
   - Kích hoạt 4 skills: professor-style, document-design, fact-checker, web-fetcher
   - Phát hiện và sửa 3 lỗi factual trong Part 1 (stack memory, nbproc deprecation, nbthread auto-detect)
   - Verify 10 URLs — tất cả alive
   - Thêm Quiz section (4 câu multiple-choice) vào Part 1

2. **Tích hợp Version Evolution Tracker vào Phụ lục A**
   - Di chuyển 52 entries (12 categories) từ `references/haproxy-version-evolution.md` vào cuối `haproxy-onboard/README.md`
   - File gốc cần `git rm` trên local (sandbox không cho phép xóa)

3. **Sửa Knowledge Dependency Graph** (4 edges)
   - P4→P11 → P3→P11 (LB algorithms cần core concepts, không cần connection model)
   - P7→P22 → P6→P22 (Lua extends fetches/converters, không phải ACL)
   - +P5→P24 (logging cần timeout knowledge)
   - +P3→P21 (HTTP cache cần config structure)

4. **Thu gọn root README** — HAProxy section từ ~245 dòng → 3 dòng (pointer)

5. **Đồng bộ haproxy-series-state.md** — sửa 27/29 tên Part cho khớp README (source of truth)

6. **Cập nhật CLAUDE.md Rule 1** — mở rộng trigger sang "audit/review", thêm lesson-learned callout

7. **Thêm Checklist F** vào quality-gate — dành cho audit/review operations

8. **Cập nhật memory files** — file-dependency-map.md (remove version-evolution refs), CLAUDE.md Current State table

### Chưa hoàn thành (Pending)

- [ ] **Commit audit changes** → feature branch → PR (theo git-workflow skill)
- [ ] **`git rm haproxy-onboard/references/haproxy-version-evolution.md`** trên local machine
- [ ] **HAProxy Parts 2-29**: Chưa bắt đầu (28/29 remaining)
- [ ] **Linux FD doc — thêm sections**: epoll edge-triggered, signalfd, eventfd
- [ ] **Cleanup**: `document-design.skill` và `pr-body.txt` trong repo root

### Git State khi kết thúc

```
Branch: master
Status: dirty (nhiều files modified, chưa commit)
Remote: master up to date tại f3256f9
Modified files:
  - haproxy-onboard/README.md (Phụ lục A, dependency graph, inline annotation fix)
  - haproxy-onboard/1.0 - haproxy-history-and-architecture.md (3 fact fixes, Quiz, callout)
  - README.md (root — thu gọn HAProxy section)
  - CLAUDE.md (Rule 1 update, Current State table)
  - memory/haproxy-series-state.md (sync 27 Part names)
  - memory/file-dependency-map.md (remove version-evolution refs)
  - memory/session-log.md (file này)
  - .claude-skills/quality-gate/SKILL.md (Checklist F)
```

### Lệnh cần chạy trên local

```bash
# SAU KHI commit và push trên Cowork/Claude Desktop:
git rm haproxy-onboard/references/haproxy-version-evolution.md
# Hoặc nếu commit trên local:
git checkout -b audit/haproxy-structure-and-part1
git add -A && git commit -m "docs(haproxy): audit structure, fix Part 1 facts, integrate version tracker"
git push -u origin audit/haproxy-structure-and-part1
```

### Bài học rút ra từ session này

1. **4 skills LUÔN kích hoạt** — không có ngoại lệ kể cả audit/review (sai lầm: chỉ dùng 2/4)
2. **Audit = viết** trong ngữ cảnh quality-gate — cần fact-checker + web-fetcher dù "chỉ đọc"
3. **Cross-file sync discipline** — dependency map phải cập nhật ngay khi thay đổi cấu trúc file

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
