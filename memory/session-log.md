# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-04-02
**Branch:** `fix/fd-doc-audit-corrections` (clean — commit `6ecfb07`)
**Base:** `master` tại `6573211`

### Đã hoàn thành

1. **Full 6-phase audit của `linux-onboard/file-descriptor-deep-dive.md`** (user request: "Tài liệu về FD này đúng chứ? Hãy dừng tất cả skill để audit nó")
   - Phase 1: Đọc toàn bộ 791 dòng, liệt kê 13 technical claims cần verify
   - Phase 2: Fact-check 13 claims — 11 CORRECT, 2 INCORRECT (đã sửa)
     - Sửa 1: HAProxy hybrid ET/LT (FD_ET_POSSIBLE), không phải purely LT
     - Sửa 2: HAProxy CLOEXEC conditional (accept4 + fcntl fallback), không phải "mọi socket/open"
   - Phase 3: Verify 11 URLs — tất cả HTTP 200
   - Phase 4: Document-design compliance — 12 H2 sections (vượt limit 7, nhưng chấp nhận cho standalone deep-dive), 7 Key Topics, 2 Misconceptions, learning elements đầy đủ
   - Phase 5: Professor-style compliance — 6 criteria (2.1-2.6) đạt
   - Phase 6: Commit fix trên feature branch

2. **Thay thế lab output placeholder bằng real output** (từ session trước, chưa commit)
   - Section 1.2 Guided Exercise: hostname `huyvl-lab-fd`, PIDs 35567/35571, `/dev/pts/2`, root user
   - Before You Begin: cập nhật quyền user/root

3. **Commit**: `6ecfb07` — `fix(linux): audit FD deep-dive — correct HAProxy claims, add real lab output`

### Chưa hoàn thành (Pending)

- [ ] **Push branch `fix/fd-doc-audit-corrections`** → tạo PR → merge (sandbox không có git auth)
- [ ] **HAProxy Parts 2-29**: Chưa bắt đầu (28/29 remaining)
- [ ] **Linux FD doc — mở rộng**: epoll advanced topics, signalfd/eventfd/timerfd (user nói "thực hành nó sau")
- [ ] **Cleanup trên local**: `git rm haproxy-onboard/references/haproxy-version-evolution.md`, xóa `document-design.skill` và `pr-body.txt` trong repo root

### Git State khi kết thúc

```
Branch: fix/fd-doc-audit-corrections (clean)
Remote: chưa push (sandbox không có git auth)
Base: master tại 6573211
Commit mới: 6ecfb07 — fix(linux): audit FD deep-dive
Modified files:
  - linux-onboard/file-descriptor-deep-dive.md (3 changes: real lab output, HAProxy ET/LT fix, HAProxy CLOEXEC fix)
```

### Lệnh cần chạy trên local

```bash
# Pull branch và push lên GitHub
cd network-onboard
git fetch origin
git checkout fix/fd-doc-audit-corrections
git push -u origin fix/fd-doc-audit-corrections

# Tạo PR
gh pr create --base master --title "fix(linux): audit FD deep-dive — correct HAProxy claims, add real lab output" --body "## Summary
- Full 6-phase audit of linux-onboard/file-descriptor-deep-dive.md before GitHub publication
- Correct 2 factual errors: HAProxy hybrid ET/LT (not purely LT), HAProxy CLOEXEC conditional (not unconditional)
- Replace placeholder lab output with real terminal output from huyvl-lab-fd

## Audit Results
- 13 technical claims fact-checked: 11 correct, 2 corrected
- 11 reference URLs verified: all HTTP 200
- Document-design and professor-style compliance: passed

## Test plan
- [ ] Markdown renders correctly on GitHub
- [ ] All 11 reference URLs accessible
- [ ] Lab output matches real machine output"

# Sau khi merge PR:
git checkout master
git pull origin master
```

### Bài học rút ra từ session này

1. **HAProxy source code verification** là bắt buộc khi claim về internal behavior — documentation và source code có thể khác nhau (hybrid ET/LT vs "LT by default")
2. **"trên mọi X" claims** cần verify cẩn thận — thực tế thường là conditional, có fallback

---

## Lịch sử sessions trước

### Session 2026-03-30 (session 2)

**Branch:** `master` (dirty — audit changes)
**Đã hoàn thành:** Audit HAProxy structure + Part 1, tích hợp Version Evolution Tracker vào Phụ lục A, sửa Knowledge Dependency Graph (4 edges), thu gọn root README, đồng bộ haproxy-series-state.md, cập nhật CLAUDE.md Rule 1, thêm Checklist F.

### Session 2026-03-29

**Branch:** `fix-haproxy-readme-audit`
**Đã hoàn thành:** 5 commits (3d82766, 10c3a17, 3535f14, 919341b, bdbff8f), tạo CLAUDE.md + memory system.

_(Giữ tối đa 5 entries.)_
