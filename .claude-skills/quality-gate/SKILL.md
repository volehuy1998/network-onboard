---
name: quality-gate
description: |
  Pre-flight checklist bắt buộc trước MỌI thao tác viết, sửa, hoặc commit trong hệ thống tài liệu
  onboard (haproxy-onboard, linux-onboard, network-onboard). PHẢI kích hoạt skill này TRƯỚC KHI
  bắt đầu viết bất kỳ nội dung nào. Skill này đảm bảo: (1) CLAUDE.md và memory files đã được đọc,
  (2) tất cả required skills đã được kích hoạt, (3) cross-file dependencies đã được xác định,
  (4) session context đã được nắm bắt. Kích hoạt khi: bắt đầu session mới, viết/sửa file .md,
  commit changes, thêm Part mới, sửa version references, sửa dependency graph, hoặc bất kỳ thao tác
  nào có thể ảnh hưởng đến nhiều file. Đặc biệt quan trọng: skill này NGĂN lỗi đồng bộ giữa các
  file — lỗi phổ biến nhất trong các session trước. Nếu không chắc có cần kích hoạt hay không,
  CỨ KÍCH HOẠT — overhead nhỏ nhưng ngăn được lỗi lớn.
---

# Quality Gate — Pre-flight Checklist cho mọi thao tác

## Tại sao skill này tồn tại

Trong 3 sessions đầu tiên của project haproxy-onboard, các lỗi sau đã xảy ra dù đã có đầy đủ skills (professor-style, fact-checker, document-design):

**Lỗi 1 — Version desync:** Sửa HAProxy 3.2 → 2.0 ở `haproxy-onboard/README.md` nhưng quên `README.md` (root). Phát hiện muộn, phải sửa thêm ở commit sau.

**Lỗi 2 — Skill activation order sai:** Viết xong Part 1 rồi mới chạy professor-style review → phát hiện 6 vấn đề → phải sửa lại toàn bộ. Đáng lẽ đọc skill trước khi viết.

**Lỗi 3 — Missing cross-references:** Dependency graph thiếu 6 edges vì không cross-check nội dung từng Part khi vẽ graph.

Root cause chung: **không có pre-flight checklist bắt buộc**. Skills tồn tại nhưng không có cơ chế enforcement.

---

## Checklist A — Bắt đầu session mới

Khi bắt đầu session (hoặc khi context bị reset):

```
□ 1. Đọc CLAUDE.md (repo root) → nắm rules và current state
□ 2. Đọc memory/session-log.md → biết session trước làm gì, pending tasks
□ 3. Đọc memory/haproxy-series-state.md → biết Part nào đã viết
□ 4. Chạy: git status, git branch, git log --oneline -5
□ 5. Thông báo cho user: "Context loaded. Session trước: [tóm tắt]. Pending: [danh sách]."
```

## Checklist B — Trước khi viết/sửa file .md

Áp dụng cho MỌI thao tác tạo hoặc sửa file markdown trong onboard series:

```
□ 1. Đọc professor-style SKILL → nắm 6 criteria (2.1-2.6)
□ 2. Đọc document-design SKILL → nắm chapter template, heading rules
□ 3. Xác định file đang sửa
□ 4. Tra memory/file-dependency-map.md → liệt kê related files
□ 5. Đọc related files để biết content hiện tại
□ 6. BẮT ĐẦU viết/sửa (không viết trước bước 1-5)
```

## Checklist C — Trước khi commit

```
□ 1. Fact-check: liệt kê MỌI technical claims → search & verify từng claim
□ 2. URL check: liệt kê MỌI URLs → verify bằng web-fetcher hoặc curl
□ 3. Cross-file sync: tra dependency map → kiểm tra related files
      → Nếu sửa version refs: kiểm tra TẤT CẢ file có version refs
      → Nếu sửa TOC: kiểm tra tên Part khớp với file .md
      → Nếu sửa dependency graph: kiểm tra reading path description
□ 4. Version annotation: nếu có cross-version content → thêm callout + update tracker
□ 5. Git workflow skill: đọc trước khi commit → conventional commits, đúng branch
□ 6. Self-audit professor-style: chạy 6 criteria (2.1-2.6) lên content vừa viết
```

## Checklist D — Trước khi kết thúc session

```
□ 1. Cập nhật memory/session-log.md (đã làm gì, chưa làm gì, git state)
□ 2. Cập nhật memory/haproxy-series-state.md (nếu Part nào thay đổi)
□ 3. Cập nhật CLAUDE.md → Current State table
□ 4. Commit memory changes
□ 5. Thông báo user lệnh cần chạy trên local (push, PR, etc.)
```

## Checklist E — Khi thêm Part mới

```
□ 1. Chạy Checklist B (trước khi viết)
□ 2. Tạo file theo convention: X.0 - <name>.md
□ 3. Include header block (môi trường, tham khảo) theo document-design
□ 4. Include learning objectives (Bloom's Taxonomy) theo document-design
□ 5. Cập nhật haproxy-onboard/README.md:
      - TOC entry
      - Mermaid dependency graph (thêm edges cho Part mới)
      - Reading path description (nếu cần)
□ 6. Cập nhật memory/haproxy-series-state.md → status = IN PROGRESS
□ 7. Cập nhật memory/file-dependency-map.md → thêm entry Part mới
□ 8. Nếu có version-specific content: cập nhật version-evolution.md
□ 9. Chạy Checklist C (trước khi commit)
```

---

## Nguyên tắc áp dụng

Checklist này không phải bureaucracy — nó là safety net. Giống như phi công phải chạy pre-flight check dù đã bay 10,000 giờ, Claude phải chạy checklist dù đã có kinh nghiệm với project. Lý do: mỗi session mới, context bị reset; lỗi đồng bộ xảy ra ở chính xác những chỗ tưởng đã kiểm tra rồi.

Overhead của checklist: khoảng 2-3 phút đọc files. Chi phí của lỗi đồng bộ: phải sửa lại ở session sau, tốn thêm commit, có thể bỏ sót nếu không ai review.
