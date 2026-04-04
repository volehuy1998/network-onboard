# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-04-04 (session 2 — tiếp nối)
**Branch:** `feat/fd-exercise-redesign-background-child`
**Remote:** `origin/feat/fd-exercise-redesign-background-child` tại `d25e7ce`

### Đã hoàn thành (session 2)

1. **Lab verification exercises 1, 2, 4** trên `huyvl-lab-fd`:
   - Exercise 1: Real PIDs 578 (CHILD), 587 (CHILD2), job notifications `[1] 578`, `[2] 587`
   - Exercise 2: Real PID 558, file content `AAABBB6789` → `XXXBBB6789` → `XXXBBBDD89`
   - Exercise 4: Real PID 566, pos: 5→0→3 confirmed
   - Commit `1c8212e`: replaced all placeholder output with real lab output

2. **SVG factual error fixes** — commit `398d7e9` (rebased to `d25e7ce`):
   - `fd-exercise2-dup-write.svg` (Fig 1-6): Removed FD 5 (doesn't exist at Part E)
   - `fd-exercise2-open-write.svg` (Fig 1-7): OFD "X" flags `0100000` → `0100002` (exec 5<> = O_RDWR)
   - `fd-exercise2-fork-write.svg` (Fig 1-8): OFD "X" flags `0100000` → `0100002` + file content `AAA` → `XXX` (Part F overwrote before Part G)
   - `fd-exercise4-lseek-cross-process.svg` (Fig 1-10): pos=5 marker x=308 → x=296
   - `fd-exercise3-status-flags-sharing.svg` (Fig 1-9): Verified correct — no changes needed

3. **Orphan cleanup:**
   - Deleted `images/fd-exercise2-write-ofd-sharing.svg` (untracked, old multi-panel)
   - Deleted `copy-professor-style-skill.html` (untracked temp)
   - Deleted `professor-style-SKILL-updated.md` (untracked temp)

4. **Experiment plan created:** `memory/experiment-plan.md`
   - Inventory: 7/9 exercises verified, 2/9 cần lab (strace TCP, FD limit lab)
   - 5 phases planned: A (lab verification), B (WCAG), C (FD expansion), D (HAProxy Parts 2-5), E (Network)

### Chưa hoàn thành (Pending) — xem chi tiết tại `memory/experiment-plan.md`

- [ ] **Phase A1: Exercise 7 (strace TCP server, line 900)**: "Output kỳ vọng" still placeholder — runbook sẵn sàng
- [ ] **Phase A2: Exercise 8 (FD limit lab, line 941)**: Cần quyết định inline output hay reference section
- [ ] **PR merge**: `feat/fd-exercise-redesign-background-child` → `master` (đã có PR trên GitHub)
- [ ] **Phase B: WCAG spacing fixes**: 3 pre-existing SVGs (30 phút)
- [ ] **Phase C: FD doc expansion**: epoll practical (C1), signalfd/eventfd/timerfd (C2), /proc/sys/fs monitoring (C3)
- [ ] **Phase D: HAProxy Parts 2-5**: Block I labs chi tiết (installation, config, connection mgmt, timeout)
- [ ] **Phase E: Network onboard**: Chưa có content (sau Block I HAProxy)

### Clarification từ user trong session này

- **Exercise 3 (status flags)** không cần lab mới vì KHÔNG có fork() — chỉ thao tác trên shell
  hiện tại. Output đã khớp thực tế từ trước khi redesign. Đây là lý do chỉ exercises 1, 2, 4
  được redesign sang background child pattern, còn exercise 3 giữ nguyên.
- **User muốn kế hoạch "tối đa"** — đã tạo 5 phases (A→E) với runbooks chi tiết, commands
  copy-paste-ready cho `huyvl-lab-fd`, effort estimates, và lab environment requirements.

### Git State khi kết thúc

```
Branch: feat/fd-exercise-redesign-background-child (clean)
Remote: origin/feat/fd-exercise-redesign-background-child tại d25e7ce
Commits trên branch (so với master):
  - 5405c6c docs(linux): redesign FD exercises with background child + /proc inspection
  - 7a7b3e1 ci: add file integrity check workflow (null byte prevention)
  - 1c8212e docs(linux): replace placeholder output with real lab output from huyvl-lab-fd
  - d25e7ce fix(linux): correct factual errors in 4 exercise SVG diagrams
Working tree: clean (cả sandbox lẫn local)
```

### Bài học rút ra

1. **Real output > placeholder**: Output của user là bằng chứng thực nghiệm — placeholder chỉ là giả thuyết. Commit placeholder TRƯỚC rồi sửa SAU = double work
2. **SVG factual errors cascade**: Khi exercise flow thay đổi state (Part E → F → G), SVG ở mỗi phase phải reflect state SAU phase trước, không phải state ban đầu. Lỗi `AAA` thay vì `XXX` trong fork-write SVG là ví dụ
3. **OFD flags phải match access mode**: `exec N<>` = O_RDWR = 0100002, `exec N<` = O_RDONLY = 0100000. Sai flags trong SVG là sai factual
4. **pos marker alignment**: Monospace font-size 12 → character width ≈ 7.2px. Marker phải tính từ text x-origin + (position × glyph_width)
5. **Rule 7 (Terminal Output Fidelity)**: Đã enforce thành công — mọi output đều copy nguyên văn từ lab

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
