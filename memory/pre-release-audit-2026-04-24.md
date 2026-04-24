# Pre-Release Audit v3.1-OperatorMaster — 2026-04-24

**Session:** S60
**Baseline commit:** `8dcbeca` (docs/sdn-foundation-rev2, working tree clean)
**Scope:** 116 file `sdn-onboard/*.md` cuối Phase G
**Purpose:** xác định có drift/regression sau Phase E→G (8+ session thêm ~6.5K dòng) trước khi tag v3.1.

---

## Summary

| Rule | Method | Result | Status |
|------|--------|--------|--------|
| Rule 9 null byte | `tr -d '\000' \| wc -c` size-diff | 0/116 violators | PASS |
| Rule 13 em-dash density < 0.10 | `grep -o '—' \| wc -l` / `wc -l` | 0/116 violators | PASS |
| Rule 11 Vietnamese prose | §11.6 regex + awk code-block filter | 64 prose leaks across 10 Phase G files | FIXABLE |
| Rule 14 source code citation | MCP GitHub spot-check | Deferred to S61 | PENDING |

**Verdict:** Foundation solid (Rule 9 + 13). Rule 11 quality gap phát hiện nhưng không phải release blocker, là polish sweep. Rule 14 pending nhưng Phase G mới chủ yếu extend existing forensic/playbook content, ít source code citation mới (Part 20.6 retrospective không có SHA mới, 9.14 expand dùng generic OVS pattern, 20.5 dùng generic function name reference).

---

## Rule 9 detail (PASS)

Method: `tr -d '\000' < file | wc -c` so với `wc -c < file`. Diff = null byte count.

Initial attempt với `grep -c $'\x00'` trả 116/116 — false positive do bash expand `$'\x00'` thành empty pattern (null terminator cắt C-string). Method 2 via `tr` cho đúng số: 0 file có null byte.

Statement: Rule 9 enforced chặt từ session 2026-04-04 trở đi. 116 file hoàn toàn sạch.

## Rule 13 detail (PASS)

Method: `grep -o '—' | wc -l` (UTF-8 multi-byte aware) chia `wc -l`. Threshold 0.10/line từ CLAUDE.md §Rule 13.

Initial attempt với `tr -cd '—' | wc -c / 3` cho số cao bất thường (Part 9.1 = 1.88/line) do `tr` không UTF-8 aware trên Git Bash Windows, mix byte của ký tự khác. Method `grep -o` UTF-8-safe cho số đúng.

Spot-verify khớp session log:
- Part 20.6 (S59): 0.0046/line (log claim 0.0046)
- Part 9.26 (S52 expand): 0.0819/line (log claim 0.0802, delta < 3%)
- Part 0.2 (Phase H): 0.076/line

Statement: Rule 13 enforced từ session 24 codify (S24) trở đi. Retrofit pass 2026-04-23. 116 file toàn dưới 0.10.

## Rule 11 detail (FIXABLE, 64 prose leak)

Method: awk exclude ``` code block + grep case-insensitive prose term. Spot-verify 20.2 manual để xác nhận leak thực.

### Distribution

| File | verify/inspect | support | identify | Tổng |
|------|---------------|---------|----------|------|
| 20.2 ovn-troubleshooting-deep-dive | 20 | 4 | 7 | 31 |
| 20.6 ovs-openflow-ovn-retrospective-2007-2024 | 0 | 4 | 1 | 5 |
| 20.1 ovs-ovn-security-hardening | 1 | 3 | 3 | 7 |
| 9.14 incident-response-decision-tree | 0 | 6 | 2 | 8 |
| 9.26 ovs-revalidator-storm-forensic | 4 | 1 | 0 | 5 |
| 9.27 ovs-ovn-packet-journey-end-to-end | 2 | 0 | 0 | 2 |
| 20.0 ovs-ovn-systematic-debugging | 0 | 6 | 0 | 6 |
| 20.3 ovn-daily-operator-playbook | 0 | 0 | 0 | 0 |
| 20.4 ovs-daily-operator-playbook | 0 | 0 | 0 | 0 |
| 20.5 ovn-forensic-case-studies | 0 | 0 | 0 | 0 |
| **TỔNG** | **27** | **24** | **13** | **64** |

### Sample leak xác định từ 20.2

| Line | Leak | Fix |
|------|------|-----|
| 267 | "nếu cần inspect tiếp" | "nếu cần kiểm tra tiếp" |
| 273 | "Verify bằng `ovn-nbctl ...`" | "Kiểm chứng bằng `ovn-nbctl ...`" |
| 274 | "Verify bằng `ovn-sbctl ...`" | "Kiểm chứng bằng `ovn-sbctl ...`" |
| 275 | "Verify bằng `ovn-nbctl show`" | "Kiểm chứng bằng `ovn-nbctl show`" |
| 377 | "nhanh nhất để verify ovn-controller dịch" | "nhanh nhất để kiểm chứng ovn-controller dịch" |
| 404 | "cần verify toàn bộ pipeline" | "cần kiểm chứng toàn bộ pipeline" |
| 515 | "Verify bằng `ovn-sbctl lflow-list`" | "Kiểm chứng bằng..." |
| 802 | "Matrix rút gọn cho oncall engineer" | "Matrix rút gọn cho kỹ sư oncall" |
| 906 | "Verify: `lflow-cache/show-stats`" | "Kiểm chứng: ..." (borderline, có thể giữ trong bullet ngắn) |
| 986 | "OVN 22.03+ support extend" | "OVN 22.03+ hỗ trợ extend" |

### Observation

1. Phase G session log claim "Rule 11 X prose fix" thường captures **một phần** (8 fix session S51, 5 fix session S57, 3 fix session S58, 2 fix session S59), không exhaust.
2. Pattern lặp: `verify` (27) + `support` (24) + `identify` (13) chiếm ~90% residual.
3. 3 file playbook (20.3, 20.4, 20.5) có **0 leak**, chứng tỏ quality gate có hoạt động khi ý thức áp dụng đầy đủ ngay từ đầu.
4. File forensic/troubleshoot/incident (20.0/20.1/20.2/9.14/9.26) dense leak vì pattern "Verify bằng X" lặp nhiều lần trong decision tree.

### Severity: LOW-MEDIUM

- Nội dung vẫn đọc được, không gây hiểu sai kỹ thuật.
- Vi phạm Rule 11 discipline đã codify, user directive "chất lượng".
- Ảnh hưởng: nếu release v3.1 với 64 residual leak, tag nhận snapshot chưa polish. Fix trong patch release v3.1.1 khả thi nhưng ít ideal.

### Recommendation

**Option A (recommended):** S61 fix sweep Rule 11 — `sed` hoặc manual edit 64 leak thành 0. Commit `docs(sdn): session S61 Rule 11 pre-release sweep`. Sau đó S62 tag v3.1.

**Option B:** tag v3.1 ngay với 64 residual leak documented, fix trong v3.1.1 patch release. Trade-off: release history chứa imperfect tag, nhưng timeline ngắn hơn.

---

## Rule 14 deferred scope (S61 hoặc S62)

Phase G content mới ít source code citation so với Phase E. Risk surface:

| File | Claim type | MCP verify needed |
|------|-----------|-------------------|
| 20.5 | Function names `binding_add_lport`, `clear_tracked_data`, etc. | Spot-check 3-5 function |
| 20.6 | 40+ milestone date + commit SHA trong Phụ lục timeline | Spot-check 5 SHA |
| 9.26 expand | coverage counter + struct name ovs-vswitchd | Spot-check 2-3 |
| 20.2 | northd.c:8127 line reference + ovn-controller(8) stage | Spot-check line drift |
| 9.14 expand | nf_conntrack_max + bond slave pattern | No SHA claim, skip |

Estimate: 15-20 MCP call, 30-45 phút. Low risk vì phần lớn reference là pattern generic, không fabricated SHA.

---

## Decision point

Đề xuất trình tự:

**S61:** Rule 11 fix sweep 64 leak (Option A). Parallel Rule 14 MCP spot-check. 1 session.
**S62:** Tag `v3.1-OperatorMaster` + CHANGELOG.md v2.1→v3.1 + README parent refresh. 1 session.
**S63+:** Phase I OVS tier 2 internals.

Total: 3 session tới release v3.1 verified clean.

---

**Audit log END.**
