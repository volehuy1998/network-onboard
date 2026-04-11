# Session Log

> File này ghi lại session gần nhất. Claude đọc file này ĐẦU TIÊN khi bắt đầu session mới
> để nắm bắt context mà không cần user giải thích lại.

---

## Session gần nhất

**Ngày:** 2026-04-11 (session 2)
**Branch:** `docs/sdn-onboard-rewrite` (dirty — uncommitted log integrity fixes)

### Đã hoàn thành

1. **Log integrity audit toàn diện trên SDN 1.0**:
   - Phát hiện và sửa 8 loại vi phạm Rule 7: UUID truncation, line merge, line deletion, timestamp alteration
   - Đối chiếu từng dòng log trong tài liệu với 3 file log gốc (ovn-controller, ovs-vswitchd, nova-compute)
   - Phát hiện nova-compute dùng UTC+7 (22:39:xx) trong khi OVN/OVS dùng UTC (15:39:xx)
   - Thêm 3 dòng "Claiming unknown" bị xóa, 3 unexpected events tại 15:39:52.xxx bị thiếu
   - Sửa OVS timestamp .948→.947, tách patch port entries thành 2 dòng đúng timestamp

2. **Đổi prefix labels trong timeline** (session 2, cùng ngày):
   - `[nova]` → `[nova-compute]`, `[ovs ]` → `[ovs-vswitchd]`, `[ovn ]` → `[ovn-controller]`
   - 37 occurrences thay đổi, bao gồm concept illustration block (lines 224-226)
   - Sửa dòng `[FDB ]` giả thành annotation format `──` để phân biệt với log thực

3. **Rule 7a added to CLAUDE.md**: "System Log Absolute Integrity (KHÔNG CÓ NGOẠI LỆ)" — 7 điều cấm tuyệt đối cho system log

4. **Skill updates packaged**:
   - `professor-style` SKILL.md: thêm section 6.4 (Absolute Log Integrity)
   - `fact-checker` SKILL.md: thêm Anti-Pattern #12 (Log Tampering) + 4 checklist items
   - Đóng gói thành `.skill` files và gửi cho user cài đặt

5. **Cập nhật memory/project files**: session-log, CLAUDE.md, file-dependency-map, README.md

### Chưa hoàn thành (Pending)

- [ ] **Commit log integrity fixes** trên branch `docs/sdn-onboard-rewrite`
- [ ] **PR merge**: `docs/sdn-onboard-rewrite` → `master` (3 commits + uncommitted changes)
- [ ] **Phase A1/A2**: FD exercises 7, 8 still need lab verification
- [ ] **Phases B-E**: Xem `memory/experiment-plan.md`

### Git State khi kết thúc

```
Branch: docs/sdn-onboard-rewrite (up to date with origin, dirty)
Last commit on branch: 2421ff9 (docs(sdn): add live migration FDB poisoning forensic analysis)
Files modified (uncommitted):
  - CLAUDE.md (Rule 7a added, Current State updated)
  - memory/file-dependency-map.md (SDN line counts updated)
  - memory/session-log.md (this file)
  - README.md (SDN onboard section added)
  - sdn-onboard/1.0 - ovn-l2-forwarding-and-fdb-poisoning.md (prefix labels + FDB annotation)
Untracked:
  - skill-updates/ (professor-style + fact-checker skill updates)
  - pidfd_getfd_demo.py (demo script from earlier session)
```

### Bài học rút ra

1. **System log = forensic evidence**: Bất kỳ thay đổi nào (truncate UUID, merge lines, sửa timestamp 1ms) đều phá hỏng reproducibility. Rule 7a ra đời từ lỗi này.
2. **Timezone awareness khi cross-correlate**: nova-compute (UTC+7) vs OVN/OVS (UTC) — search by instance UUID thay vì timestamp khi log sources dùng timezone khác nhau.
3. **Synthetic data phải tách biệt visual**: Dòng `[FDB ]` trông giống log thật nhưng là constructed data — gây nhầm lẫn. Annotation format `──` giải quyết vấn đề này.

---

## Lịch sử sessions trước

### Session 2026-04-11 (session 1)

**Branch:** `docs/sdn-onboard-rewrite`
**Đã hoàn thành:** Log integrity audit SDN 1.0 — phát hiện và sửa vi phạm Rule 7 trên OVN/OVS/nova entries. Thêm Rule 7a vào CLAUDE.md. Packaged skill updates.

### Session 2026-04-10

**Branch:** `docs/sdn-onboard-rewrite` (created, committed)
**Đã hoàn thành:** Full rewrite SDN 1.0 (920→1234 lines) và SDN 2.0 (496 lines) trong professor-style. Converted headings, expanded sparse sections, added forensic timeline with production logs.

### Session 2026-04-04 (session 2)

**Branch:** `feat/fd-exercise-redesign-background-child` (clean, pushed at `d25e7ce`)
**Đã hoàn thành:** Lab verification exercises 1-6 with real output, SVG factual error fixes (4 SVGs), orphan cleanup, experiment plan created (5 phases A→E). Null byte incident discovered and fixed (PR #35→#38).

### Session 2026-04-03

**Branch:** `master` (dirty)
**Đã hoàn thành:** Thí nghiệm 6A/6B (CLOEXEC), cập nhật sections 1.4, 1.9, 1.10 với real lab output.

### Session 2026-03-30 (session 2)

**Branch:** `master` (dirty)
**Đã hoàn thành:** Audit HAProxy structure + Part 1, tích hợp Version Evolution Tracker vào Phụ lục A, sửa Knowledge Dependency Graph (4 edges), thu gọn root README.

_(Giữ tối đa 5 entries.)_
