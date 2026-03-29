# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-03-29
**Branch:** `fix-haproxy-readme-audit`
**Base:** `main`

### Đã hoàn thành

1. **Commit `3d82766`** — fix(haproxy): correct factual errors and add missing dependency in README TOC
   - Sửa lỗi factual trong Part 1 và bổ sung dependency thiếu trong TOC

2. **Commit `10c3a17`** — docs(haproxy): add document-design structure and fix cross-references in Part 1
   - Áp dụng document-design skill vào Part 1 (header block, learning objectives, Bloom's Taxonomy)

3. **Commit `3535f14`** — fix(haproxy): update version refs to HAProxy 2.0 and enhance Part 1 with professor-style review
   - Sửa version references 3.2 → 2.0 ở CẢ parent README và haproxy-onboard README
   - 6 cải tiến professor-style cho Part 1 (context paragraph, SO_REUSEPORT, misconception box, LVS/IPVS link, forward references, production readiness)
   - 12 technical claims fact-checked (all passed)
   - 9 URLs verified (all HTTP 200)

4. **Commit `919341b`** — feat(haproxy): add version evolution tracker for cross-version changes
   - Tạo `haproxy-onboard/references/haproxy-version-evolution.md` (52 entries, 12 categories)
   - Thêm section Version Evolution Tracker vào `haproxy-onboard/README.md`
   - Thiết lập inline annotation convention: `> **Lưu ý phiên bản:**`

5. **Commit `bdbff8f`** — fix(haproxy): update knowledge dependency map with 7 corrected edges
   - Sửa Mermaid dependency graph: bỏ P7→P19, thêm P8→P19, P4→P17, P6→P24, P5→P27, P25/P26/P27→P28, P1→P29
   - Cập nhật reading path description

### Chưa hoàn thành (Pending)

- [ ] **Push branch**: `git push origin fix-haproxy-readme-audit` (sandbox không có GitHub auth, user cần chạy trên local)
- [ ] **Tạo PR** cho branch `fix-haproxy-readme-audit` → merge vào main
- [ ] **File untracked**: `references/` ở repo root chứa "The Linux Programming Interface.pdf" — chưa được track (file lớn, cân nhắc .gitignore)
- [ ] **Animation file**: `context-switching-animation.html` — untracked, chưa reference từ Part 1
- [ ] **Tạo CLAUDE.md + memory system** — đang thực hiện trong session này
- [ ] **Tạo quality-gate skill** — đang thực hiện trong session này

### Git State khi kết thúc

```
Branch: fix-haproxy-readme-audit
Status: clean (sau commit bdbff8f) + đang tạo CLAUDE.md và memory/
Commits ahead of main: 5
Remote push: CHƯA push (cần chạy trên local)
```

### Lệnh cần chạy trên local

```bash
cd network-onboard
git push origin fix-haproxy-readme-audit
```

---

## Lịch sử sessions trước

_(Thêm entry mới ở trên, đẩy entry cũ xuống đây. Giữ tối đa 5 entries.)_
