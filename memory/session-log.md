# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-04-04
**Branch:** `master` (dirty — major exercise redesign + 6 new SVGs + figure renumbering)
**Base:** `master` tại `e92ef0f`

### Đã hoàn thành

1. **Exercise redesign — background child + /proc inspection** (6-phase plan, phases 1-6):
   - **Phase 1**: Fix i-node text overflow trong `fd-exercise1-read-offset-sharing.svg` (viewBox 660→676, downstream elements +16px)
   - **Phase 2**: Redesign 3/4 exercises trong `file-descriptor-deep-dive.md`:
     - Exercise 1 Phần C+D: blocking subshell → background child `( ...; sleep 300 ) &` + `/proc/$CHILD/fdinfo/N`
     - Exercise 2 Phần G: same pattern cho fork write
     - Exercise 4 steps 2-5: same pattern cho lseek xuyên process
     - Exercise 3: không sửa (không có fork)
   - **Phase 3**: Tạo 6 SVG mới (individual diagrams thay vì multi-panel):
     - `fd-exercise1-initial-open-read.svg` (baseline, pos=5)
     - `fd-exercise1-after-dup.svg` (FD 3,4 → OFD "A", pos=8)
     - `fd-exercise1-after-open-independent.svg` (2 OFDs)
     - `fd-exercise2-dup-write.svg`, `fd-exercise2-open-write.svg`, `fd-exercise2-fork-write.svg`
   - **Phase 4**: Renumber all 14 figures sequentially (1-1 through 1-14):
     - Inserted 3 new SVG refs in Exercise 1 (after step 2, after Phần A, after Phần B)
     - Inserted 3 new SVG refs in Exercise 2 (after each Part E, F, G)
     - Deleted old multi-panel Exercise 2 reference (`fd-exercise2-write-ofd-sharing.svg`)
     - Renamed 7 existing figures in both markdown AND SVG internal `<text>` titles
     - Updated Key Topics table (Table 1-3) with all 14 figure entries
   - **Phase 5**: Full audit:
     - 0 null bytes across all 14 SVGs + markdown
     - SVG-caption consistency: 14/14 match
     - All 14 SVG file references resolve to existing files
     - Fact-check: 17/17 technical claims PASS (man page refs, bash syntax, expected output)
   - **Phase 6**: Updated memory files (this file, dependency map)

2. **professor-style SKILL update**: Added POE method (2.7), Part 8 (International Pedagogical Framework), packaged as `.skill` file

### Chưa hoàn thành (Pending)

- [ ] **Commit + push + PR** cho toàn bộ redesign (sandbox lock — cần chạy trên local)
- [ ] **WCAG spacing fixes**: 3 pre-existing SVGs have minor text spacing violations (0.5-2.5px shortfall): fd-fork-exec-cloexec.svg, fd-kernel-3-table-model.svg, fd-select-poll-vs-epoll.svg
- [ ] **Orphan cleanup**: `git rm images/fd-exercise2-write-ofd-sharing.svg` (old multi-panel, no longer referenced)
- [ ] **Lab verification**: User cần chạy redesigned exercises trên huyvl-lab-fd và cung cấp real output để thay thế expected output (PID 2847 là placeholder)
- [ ] **HAProxy Parts 2-29**: Chưa bắt đầu (28/29 remaining)
- [ ] **Linux FD doc — mở rộng**: epoll advanced topics, signalfd/eventfd/timerfd
- [ ] **Cleanup trên local**: `git rm haproxy-onboard/references/haproxy-version-evolution.md`

### Git State khi kết thúc

```
Branch: master (dirty)
Remote: origin/master tại e92ef0f
Modified files (chưa commit):
  - linux-onboard/file-descriptor-deep-dive.md (exercises redesigned, 14 figures renumbered, 1261 lines)
  - images/fd-exercise1-initial-open-read.svg (NEW)
  - images/fd-exercise1-after-dup.svg (NEW)
  - images/fd-exercise1-after-open-independent.svg (NEW)
  - images/fd-exercise2-dup-write.svg (NEW)
  - images/fd-exercise2-open-write.svg (NEW)
  - images/fd-exercise2-fork-write.svg (NEW)
  - images/fd-exercise1-read-offset-sharing.svg (title 1-6→1-5, viewBox fix)
  - images/fd-exercise3-status-flags-sharing.svg (title 1-8→1-9)
  - images/fd-exercise4-lseek-cross-process.svg (title 1-9→1-10)
  - images/fd-epoll-architecture.svg (title 1-2→1-11)
  - images/fd-select-poll-vs-epoll.svg (title 1-3→1-12)
  - images/fd-fork-exec-cloexec.svg (title 1-1b→1-13)
  - images/fd-leak-and-cloexec.svg (title 1-4→1-14)
  - memory/file-dependency-map.md (updated Tầng 5 for 14 SVGs)
  - memory/session-log.md (this file)
Lock files: .git/index.lock có thể tồn tại trong sandbox — cần xóa trên local
```

### Lệnh cần chạy trên local

```bash
# 0. Xóa lock file nếu tồn tại
cd network-onboard
rm -f .git/index.lock .git/HEAD.lock

# 1. Tạo branch mới từ master
git checkout master
git pull origin master
git checkout -b feat/fd-exercise-redesign-background-child

# 2. Stage all changes
git add linux-onboard/file-descriptor-deep-dive.md
git add images/fd-exercise1-initial-open-read.svg
git add images/fd-exercise1-after-dup.svg
git add images/fd-exercise1-after-open-independent.svg
git add images/fd-exercise2-dup-write.svg
git add images/fd-exercise2-open-write.svg
git add images/fd-exercise2-fork-write.svg
git add images/fd-exercise1-read-offset-sharing.svg
git add images/fd-exercise3-status-flags-sharing.svg
git add images/fd-exercise4-lseek-cross-process.svg
git add images/fd-epoll-architecture.svg
git add images/fd-select-poll-vs-epoll.svg
git add images/fd-fork-exec-cloexec.svg
git add images/fd-leak-and-cloexec.svg
git add memory/file-dependency-map.md
git add memory/session-log.md

# 3. Remove orphan SVG
git rm images/fd-exercise2-write-ofd-sharing.svg

# 4. Null byte check (Rule 9)
for f in $(git diff --cached --name-only); do
  if [ -f "$f" ]; then
    nullcount=$(python3 -c "print(open('$f','rb').read().count(b'\x00'))")
    if [ "$nullcount" -gt 0 ]; then echo "BLOCKED: $f has $nullcount null bytes"; fi
  fi
done

# 5. Commit
git commit -m "docs(linux): redesign FD exercises with background child + /proc inspection

- Redesign exercises 1/2/4 to use background child pattern:
  ( commands; sleep 300 ) & + /proc/\$CHILD/fdinfo/N inspection
  Replaces blocking subshell that required separate terminal
- Create 6 new individual SVG diagrams for exercise intermediate states
  (baseline, after-dup, after-open, dup-write, open-write, fork-write)
- Renumber all 14 figures sequentially (1-1 through 1-14)
  in both markdown and SVG internal <text> titles
- Update Key Topics table with all 14 figure entries
- Remove old multi-panel Exercise 2 SVG (replaced by 3 individual diagrams)
- Fix i-node text overflow in Exercise 1 final SVG (viewBox 660→676)
- Update memory: dependency map (14 SVG entries), session log

Fact-checked: 17/17 technical claims PASS (man page refs, bash syntax)
Null bytes: 0 across all files
SVG-caption consistency: 14/14 match

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# 6. Push
git push -u origin feat/fd-exercise-redesign-background-child

# 7. Create PR
gh pr create --base master \
  --title "docs(linux): redesign FD exercises with background child + /proc inspection" \
  --body "## Summary
- Redesign exercises 1/2/4: blocking subshell → background child \`( ...; sleep 300 ) &\` + \`/proc/\$CHILD/fdinfo/N\`
- 6 new individual SVG diagrams for exercise intermediate states
- All 14 figures renumbered sequentially (1-1 through 1-14)
- Old multi-panel Exercise 2 SVG removed

## Audit results
- 17/17 technical claims fact-checked PASS
- 0 null bytes across all files
- 14/14 SVG-caption consistency

## Test plan
- [ ] Markdown renders correctly on GitHub (14 SVG embeds)
- [ ] Run redesigned exercises on lab machine (PID values are placeholders)
- [ ] Verify figure numbering sequential with no gaps
- [ ] Check SVG renders in both GitHub and VS Code preview"
```

### Bài học rút ra từ session này

1. **Individual SVGs > multi-panel SVGs** cho exercises — mỗi bước thay đổi có diagram riêng giúp người đọc theo dõi tốt hơn
2. **Background child + /proc inspection** pattern: `( commands; sleep 300 ) & CHILD=$!; sleep 1` cho phép quan sát đồng thời parent và child từ cùng terminal — loại bỏ yêu cầu "mở terminal thứ hai"
3. **Figure renumbering requires 3 locations per figure**: markdown alt-text `![Figure X-Y]`, markdown caption `*Figure X-Y*`, SVG internal `<text>`. Bỏ sót 1 trong 3 gây inconsistency

---

## Lịch sử sessions trước

### Session 2026-04-03

**Branch:** `master` (dirty)
**Đã hoàn thành:** Thí nghiệm 6A/6B (CLOEXEC), cập nhật sections 1.4, 1.9, 1.10 với real lab output.

### Session 2026-04-02

**Branch:** `fix/fd-doc-audit-corrections` (clean — commit `6ecfb07`)
**Đã hoàn thành:** Full 6-phase audit FD doc (13 claims fact-checked, 2 corrected: HAProxy ET/LT, HAProxy CLOEXEC conditional), verify 11 URLs, replace lab output placeholder.

### Session 2026-03-30 (session 2)

**Branch:** `master` (dirty — audit changes)
**Đã hoàn thành:** Audit HAProxy structure + Part 1, tích hợp Version Evolution Tracker vào Phụ lục A, sửa Knowledge Dependency Graph (4 edges), thu gọn root README.

### Session 2026-03-29

**Branch:** `fix-haproxy-readme-audit`
**Đã hoàn thành:** 5 commits (3d82766, 10c3a17, 3535f14, 919341b, bdbff8f), tạo CLAUDE.md + memory system.

_(Giữ tối đa 5 entries.)_
