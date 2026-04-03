# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-04-03
**Branch:** `master` (dirty — file-descriptor-deep-dive.md đã sửa, chưa commit)
**Base:** `master` tại `e92ef0f`

### Đã hoàn thành

1. **Thí nghiệm 6A/6B — CLOEXEC trên huyvl-lab-fd** (tiếp nối thí nghiệm 1-5 từ session trước)
   - 6A: `exec 3>/tmp/cloexec-test.txt` + `bash -c` → FD 3 LEAKED (PID 527→577)
   - 6B: Python `fcntl(3, F_SETFD, FD_CLOEXEC)` + `os.execlp()` → FD 3 closed by CLOEXEC
   - Edge case: `os.open()` trả FD 3, `dup2(3,3)` là no-op → `os.close(3)` đóng nhầm → sửa bằng `if fd != 3`

2. **Cập nhật `linux-onboard/file-descriptor-deep-dive.md`** (3 sections thay đổi):
   - **Section 1.4**: Thay placeholder bằng real output từ huyvl-lab-fd (PID 558, FD 3=socket:[20882], accept4 với SOCK_CLOEXEC, FD reuse). Thêm bước 1 kiểm tra môi trường sạch, bước 6 quan sát FD reuse.
   - **Section 1.9**: Thay placeholder strace output bằng real output (socket SOCK_CLOEXEC, accept4 SOCK_CLOEXEC).
   - **Section 1.10 Guided Exercise**: Thay hoàn toàn exercise cũ (Python script placeholder) bằng exercise mới 2 phần (A: FD leak, B: CLOEXEC ngăn chặn) với real terminal output.

### Chưa hoàn thành (Pending)

- [ ] **Commit + push + PR** cho thay đổi section 1.4 + 1.9 + 1.10 (sandbox bị lock file, cần chạy trên local)
- [ ] **PR cho experiments 1-4**: Branch `feat/fd-lab-3table-experiments` đã push, PR có thể chưa tạo (GitHub API timeout session trước)
- [ ] **HAProxy Parts 2-29**: Chưa bắt đầu (28/29 remaining)
- [ ] **Linux FD doc — mở rộng**: epoll advanced topics, signalfd/eventfd/timerfd
- [ ] **Cleanup trên local**: `git rm haproxy-onboard/references/haproxy-version-evolution.md`, xóa `document-design.skill` và `pr-body.txt`

### Git State khi kết thúc

```
Branch: master (dirty)
Remote: origin/master tại e92ef0f
Modified files (chưa commit):
  - linux-onboard/file-descriptor-deep-dive.md (sections 1.4, 1.9, 1.10 — real lab output)
Lock files: .git/index.lock tồn tại trong sandbox — cần xóa trên local
```

### Lệnh cần chạy trên local

```bash
# 0. Xóa lock file nếu tồn tại
cd network-onboard
rm -f .git/index.lock .git/HEAD.lock

# 1. Tạo branch mới từ master
git checkout master
git pull origin master
git checkout -b feat/fd-lab-strace-cloexec

# 2. Commit (file đã được sửa bởi Cowork — chỉ cần stage + commit)
git add linux-onboard/file-descriptor-deep-dive.md
git commit -m "docs(linux): add real lab output for FD experiments 5-6 (strace, CLOEXEC)

- Section 1.4: replace placeholder with real strace output from huyvl-lab-fd
  (PID 558, socket:[20882], accept4 with SOCK_CLOEXEC, FD reuse demo)
- Section 1.9: replace placeholder strace lifecycle output
- Section 1.10: rewrite Guided Exercise with real experiment output
  (Part A: FD leak without CLOEXEC, Part B: kernel closes FD with CLOEXEC)
- Add clean environment verification step (lesson from experiment 5 failure)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# 3. Push
git push -u origin feat/fd-lab-strace-cloexec

# 4. Tạo PR
gh pr create --base master --title "docs(linux): add real lab output for FD experiments 5-6" --body "## Summary
- Replace placeholder output in sections 1.4, 1.9, 1.10 with real terminal output from huyvl-lab-fd
- Section 1.4: strace showing accept4() with SOCK_CLOEXEC, FD reuse via lowest-available-number
- Section 1.9: strace socket lifecycle with SOCK_CLOEXEC flags
- Section 1.10: complete rewrite of Guided Exercise — Part A proves FD leak, Part B proves CLOEXEC prevents it

## Test plan
- [ ] Markdown renders correctly on GitHub
- [ ] Lab output consistent across sections (PID 527/558/577, huyvl-lab-fd hostname)
- [ ] Cross-reference: section 1.10 Key Topic correctly links to section 1.4 strace observation"
```

### Bài học rút ra từ session này

1. **Kiểm tra môi trường sạch trước mỗi thí nghiệm** — FD 3 còn sót từ thí nghiệm 3 gây experiment 5 thất bại (Python server nhận FD 4 thay vì FD 3)
2. **`dup2(fd, fd)` khi source == target** là POSIX no-op, nhưng `os.close(fd)` ngay sau sẽ đóng FD cần giữ → phải guard bằng `if fd != target`
3. **Sandbox lock file** vẫn là blocker — cần user xóa trên local trước khi git operations

---

## Lịch sử sessions trước

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
