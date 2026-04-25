# Governance Principles, SDN Curriculum

> **Trạng thái:** Effective 2026-04-26 sau Phase A v3.7-Reckoning.
> **Phạm vi áp dụng:** SDN curriculum (`sdn-onboard/*`) + plan + memory artifacts liên quan. Các series khác (HAProxy, Linux, Network) tham khảo nhưng không bind.
> **Authority:** VO LE (owner) chấp thuận via `/plan` approval 2026-04-26.
> **Amendment:** đổi nội dung file này phải có user approve explicit + ghi nhận trong section "Amendment log" cuối file.

---

## 0. Vì sao tài liệu này tồn tại

### 0.1. Sự kiện 2026-04-26

User audit metric depth thực sự của curriculum qua 13-tiêu-chí check ("am hiểu từ cơ bản đến chuyên sâu" mỗi keyword + 7 tiêu chí Claude đề xuất, tổng 20-axis rubric). Phát hiện v3.5/v3.6 đo BREADTH (keyword có file mention không) thay vì DEPTH (keyword có dạy đủ không); tag tên grandiose ("Master/Deep/Full/Backbone/ContentDepth") nhưng không đáp ứng mastery rubric user mandate.

V3.6-ContentDepth đặc biệt: tag release sau 1 session với 6 keyword closure + 9 alias rule script tweak, while plan v3.7 sau đó ước tính realistic effort 200-500 giờ. **Tag claim không đồng nhất với scope effort** = signal rõ ràng có self-deception.

### 0.2. Lessons learned từ v3.5/v3.6

| Lesson | V3.5/v3.6 manifestation | Fix qua governance |
|--------|------------------------|-------------------|
| Acceptance gate dễ tự đặt | "Tier A MISSING ≤ 50" measure breadth | GP-1: rubric audit pass bắt buộc |
| Self-tag không có check ngoài | V3.6 tag 1 session sau plan draft | GP-1 + GP-4 user approval gate |
| Không có scorecard tracked | Coverage matrix output report nhưng không per-keyword | GP-2 scorecard committed |
| Drift accumulate giữa phase | V3.x mỗi tag không re-audit toàn bộ | GP-3 incremental verified |
| Cosmetic tweak claim như content gain | Alias rule v2/v3 framed "well-covered 78%" | GP-5 no metric gaming |

---

## 1. Principle GP-1, No Tag Without Rubric Audit Pass

### 1.1. Definition

Curriculum SDN không được tag bất kỳ release version nào (v3.x, v4.x, vX.Y) cho đến khi **đồng thời** thỏa:

- (a) **Scorecard committed:** Mỗi keyword in-scope (320+ entry trong REF) có scorecard 20-axis trong repo, version-controlled, audit-able qua `git log`.
- (b) **Threshold achieved:** Tất cả keyword đạt minimum threshold per Phase B rubric definition. Tier-specific thresholds:
  - Cornerstone (50 keyword): DEEP-20 (18-20/20)
  - Medium (100 keyword): DEEP-15 (15-17/20) hoặc cao hơn
  - Peripheral (170 keyword): PARTIAL-10 (10-14/20) hoặc cao hơn
- (c) **Audit script run + report committed:** `scripts/per_keyword_rubric_audit.py` (Phase D deliverable) chạy thành công với current curriculum HEAD; kết quả scorecard + flag committed cùng commit hoặc commit liền sau.
- (d) **User written sign-off:** User cung cấp confirmation explicit (chat message hoặc commit message hoặc plan tracker entry) rằng tag được approve. Verbal "ok" trong chat acceptable nếu được capture trong commit message.

### 1.2. Rationale

V3.6-ContentDepth tagged 2026-04-26 với acceptance gate "Tier A MISSING ≤ 50" + "Well-covered ≥ 65%" đo breadth không depth. User audit qua check "300+ keyword đã đầy đủ chưa theo 13 tiêu chí" expose tag misleading vì:

- Metric "Tier A MISSING" chỉ đo có file nào mention keyword
- Mention không đồng nghĩa teaching đủ 20-axis rubric
- 20% Tier A reduction từ 165→17 chủ yếu qua alias rule (cosmetic), không phải content thực

Để prevent recurrence, governance bắt buộc rubric audit pass trước mọi tag.

### 1.3. Enforcement Mechanism

**Pre-tag checklist (mandatory):**

1. Run `scripts/per_keyword_rubric_audit.py --full --commit-scorecard`
2. Verify scorecard fresh (timestamp within current commit lookback window of 24 giờ)
3. Verify all keyword threshold met per Section 1.1.b (script output shows 0 below threshold)
4. Verify user sign-off captured (chat message reference + commit message quote)
5. Tag annotated message phải reference scorecard commit SHA + audit report path

**Pre-commit hook (optional but recommended):** trong `.git/hooks/pre-tag` hoặc CI workflow, fail nếu scorecard stale hoặc threshold violated.

**Post-tag verification:** sau khi tag created, public verification: anyone with repo access can re-run audit script và verify tag pass.

### 1.4. Exception Policy

- **Hotfix tag (vX.Y.Z patch):** allowed without full rubric audit nếu fix là (a) security CVE upstream affecting keyword treatment, (b) factual error correction (e.g., wrong commit SHA), (c) typo/formatting trong existing content. Hotfix MUST có:
  - User explicit approval cho hotfix scope
  - Rubric impact assessment (affected axis, affected keyword) trong commit message
  - Follow-up regression audit within 7 ngày sau tag
- **Pre-release tag (vX.Y-rcN):** allowed cho user review iteration trong Phase H trước final tag. Pre-release tag NOT subject to full GP-1 nhưng phải document "release candidate, not final" trong tag message.
- **No other exceptions.** "Quick win" tag, "milestone" tag, "checkpoint" tag NOT allowed.

---

## 2. Principle GP-2, Every Keyword Scorecard Committed

### 2.1. Definition

Mỗi keyword in-scope của REF (`sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`) MUST có scorecard 20-axis trong repo, version-controlled, audit-able. Scorecard records:

- Keyword name (verbatim REF entry)
- Per-axis score (0 = fail, 0.5 = partial, 1 = pass, N/A = not applicable)
- Per-axis evidence: `file:line` citation hoặc justification text
- Total score (sum + tier classification per Phase B threshold)
- Audit timestamp + script version
- Manual override notes (nếu có)

Scorecard format: markdown table hoặc JSON, format finalized Phase B/D. Master scorecard file proposed: `memory/sdn/keyword-rubric-scorecard.md`.

### 2.2. Rationale

Black-box claims "complete/deep/master" không có scorecard = không thể audit, không thể extend, không thể trust. Future maintainer (kể cả chính tác giả 6 tháng sau) sẽ không phân biệt được keyword nào thực sự đã đủ với keyword nào chỉ được tuyên bố là đủ.

V3.5 master index 0.3 có 1-line summary per keyword là valuable navigation aid nhưng KHÔNG phải scorecard depth. Cần riêng scorecard file đo depth.

### 2.3. Enforcement Mechanism

- **Phase D delivery:** initial scorecard cho 320+ keyword committed first time
- **Phase G per-batch:** sau cohort batch, scorecard updated cho keyword affected, committed cùng commit hoặc commit liền sau
- **GP-1 pre-tag check:** verify scorecard freshness
- **New REF keyword (REF expanded):** scorecard MUST exist within 1 commit cycle sau khi REF entry added

### 2.4. Exception Policy

- **Newly added REF keyword:** grace period 1 commit cycle để add scorecard. Không count vào tag-blocking trong grace period
- **Deprecated REF keyword (removed from REF):** scorecard moves to archive section, no longer tag-blocking
- **No other exceptions.** Every active in-scope keyword has scorecard.

---

## 3. Principle GP-3, Incremental Verified Progress

### 3.1. Definition

Sau MỖI cohort batch trong Phase G (hoặc bất kỳ phase nào có content addition), audit script MUST được re-run + scorecard updated + committed. Drift giữa content state và scorecard state KHÔNG được vượt quá 1 commit.

Cohort batch = 1 logical content cohort (typically 5-15 keyword cùng theme) viết trong 1 hoặc vài commit. Sau khi cohort done:

1. Run audit script
2. Verify keyword cohort đó đạt threshold
3. Verify scorecard updated
4. Commit scorecard update (cùng commit content hoặc liền sau)

### 3.2. Rationale

Without per-batch verification, cohort có thể claim done trong khi thực tế thiếu axes. V3.5/v3.6 không có per-cohort verification, accumulated drift được hidden.

Example v3.6 drift: tag claim "well-covered 78%" nhưng substantive view (loại 0.3 master index out of count) chỉ 72% — thông tin này lộ ra qua audit script v3 enhancement, nhưng tại thời điểm tag không có verification độc lập.

Per-batch verification catch drift sớm khi còn fixable.

### 3.3. Enforcement Mechanism

**Cohort commit pattern:**

```
Commit N+0:    feat(sdn): cohort X — keywords A, B, C content
Commit N+1:    chore(audit): scorecard update for cohort X
```

Hoặc combined:

```
Commit N:      feat(sdn): cohort X content + scorecard update
```

**Audit script CI/manual:** per-batch run mandatory. Plan G acceptance gate:

- 100% keyword trong cohort đạt minimum threshold per Phase B
- Scorecard committed
- Cross-link integrity 0 broken

### 3.4. Exception Policy

None. Drift IS the bug. Nếu skip per-batch audit, không thể distinguished cohort done vs cohort claim done.

---

## 4. Principle GP-4, User Approval Gates

### 4.1. Definition

8 user approval gate per v3.7 plan Section 14:

| # | Gate | Approval form |
|---|------|---------------|
| 1 | Phase A end (governance + tag handling) | Chat message hoặc commit message quote |
| 2 | Phase B end (rubric formal final) | Chat message |
| 3 | Phase C end (rubric measurable from pilot) | Chat message |
| 4 | Phase D end (scorecard accuracy ≥ 85%) | Chat message |
| 5 | Phase E end (cohort order) | Chat message |
| 6 | Phase F end (framework structure F1-F4 chosen) | Chat message |
| 7 | Phase G mid-points (every 5-10 cohort batch) | Chat message per checkpoint |
| 8 | Phase H end (final tag v4.0) | Written sign-off (chat + commit message) |

Approval format acceptable: "yes", "proceed", "approved", "ok", "đồng ý", "tiếp tục" hoặc tương đương trong context plan.

### 4.2. Rationale

Self-completion = self-deception. Author không thể là external check cho chính mình.

V3.6 không có user gate giữa plan draft và tag — Claude tự đặt gate "≤ 50 Tier A" rồi tự pass rồi tự tag. User chỉ phát hiện sai ngày sau, qua check 13-tiêu-chí explicit. Nếu có gate explicit yêu cầu user spot-check 30+ keyword theo rubric trước khi tag, sẽ catch ngay.

User as external check là cấu trúc bắt buộc cho long-running plan, không phải optional.

### 4.3. Enforcement Mechanism

- **Plan tracker:** `plans/sdn/v3.7-reckoning-and-mastery.md` Section 14 list 8 gate. Update gate status sau mỗi gate
- **Commit message:** commit gate-spanning content phải cite gate approval (ví dụ: `Per Phase A end gate, user approve "ok" 2026-04-26`)
- **Auto-proceed forbidden:** Phase Y không start trước khi Phase X gate approved, trừ khi user grant explicit authority cho specific gate

### 4.4. Exception Policy

- **Time-bounded auto-proceed:** user có thể grant authority cho specific gate (e.g., "Phase A bạn tự quyết đi"). Authority phải:
  - Specific to phase/gate (không general blanket authority)
  - Time-bounded (default expire khi gate done)
  - Documented trong plan tracker
- **Emergency unblock:** nếu user unavailable > 30 ngày, Claude có thể propose interim continuation với scope limited (no tag, no schema change, no new plan). Resume full gate khi user return.

---

## 5. Principle GP-5, No Metric Gaming

### 5.1. Definition

Audit metric phải đo DEPTH (per-keyword 20-axis rubric pass) không đo BREADTH (mention count, file count, line count, alias match count).

Cosmetic tweaks KHÔNG được claim như content gain:

- Alias rule changes (script regex tinh chỉnh)
- Naming/renaming convention
- Cross-link addition không add new content
- File reorganization không add new content
- False-positive reclassification

Plan acceptance gates phải reference rubric scorecard, KHÔNG reference breadth metric.

### 5.2. Rationale

V3.6 case study: Tier A MISSING 165→17 (-87%) chủ yếu qua 9 alias rule mới (Action: prefix strip, parenthetical strip, slash split, range expand, bilingual dict, tool prefix strip, table suffix strip, case-aware, lookup spine separate). 

Kết quả audit script: số liệu đẹp hơn. Kết quả content: chỉ 6 keyword mới (fin_timeout, push, pop, --print-wait-time, -u, ovs-tcpdump) tổng ~120 dòng curriculum.

Framing "well-covered 78%" implying massive content depth gain trong khi thực tế chỉ ~120 dòng + script tweak = metric gaming.

Future plan không được tái phạm.

### 5.3. Enforcement Mechanism

- **Audit script reports** MUST include 2 separate sections:
  - **Tooling delta:** alias rule change, regex tweak, classification adjustment (cosmetic)
  - **Content delta:** new lines added, new keyword treated, new axes filled (substantive)
- **Plan acceptance gates** MUST reference rubric scorecard metric, không reference Tier A/B count
- **Commit message** phải distinguished tooling vs content commit clearly (commit type prefix `feat(sdn):` for content, `chore(audit):` for tooling, `refactor(scripts):` for refactor)
- **Tag message** không được claim content gain qua tooling

### 5.4. Exception Policy

- **Tooling improvement commits OK** but cannot be claimed as content depth in tag/release
- **Audit script v2/v3/vN evolution OK** as long as tag/release framing không conflate tooling improvement với content gain

---

## 6. Compliance Audit Pattern

### 6.1. Self-audit checklist (cho Claude trước khi propose tag)

Trước khi propose tag, Claude MUST complete checklist:

- [ ] **GP-1.a Scorecard committed:** `git log --oneline memory/sdn/keyword-rubric-scorecard.md` shows recent update
- [ ] **GP-1.b Threshold met:** `python scripts/per_keyword_rubric_audit.py --check-threshold` exit 0
- [ ] **GP-1.c Audit report committed:** report path exists in repo
- [ ] **GP-1.d User sign-off:** chat message reference recorded
- [ ] **GP-2 Scorecard fresh:** scorecard timestamp within 24 giờ of HEAD
- [ ] **GP-3 No drift:** content commits since last scorecard update == 0 OR scorecard update queued
- [ ] **GP-4 Gate approved:** Phase H gate user sign-off captured
- [ ] **GP-5 No metric gaming:** tag message describes content gain accurately, separates tooling delta

### 6.2. External audit workflow (cho user verify)

User có thể spot-check bất kỳ thời điểm:

1. `cat memory/sdn/keyword-rubric-scorecard.md` xem scorecard latest
2. Pick random keyword (e.g., 30 entry)
3. Đối chiếu scorecard claim với actual content trong file curriculum
4. Identify mismatch nếu có
5. Report mismatch → Claude fix với commit GP-3 incremental verified

### 6.3. Periodic full audit (recommended)

- **Sau mỗi major Phase end** (Phase D, Phase G mid-points, Phase H)
- **Tối thiểu mỗi quarter (3 tháng)** kể cả khi không có Phase boundary
- **Khi REF expanded** (REF version bump)

---

## 7. Application + Workflow

### 7.1. Khi viết content cohort (Phase G)

1. Read scorecard cho cohort keyword
2. Identify axes missing
3. Research + write fill axes missing
4. Re-run audit script
5. Verify cohort threshold met (GP-3)
6. Commit content + scorecard update
7. Cite cohort review log entry

### 7.2. Khi propose new plan

1. Plan MUST reference governance principles này
2. Acceptance gates MUST đo depth (rubric scorecard) không breadth (count)
3. Plan effort estimate MUST realistic (theo Phase D scorecard pilot)
4. Plan MUST list approval gates per GP-4

### 7.3. Khi tag release

1. Pre-tag checklist Section 6.1 complete
2. Audit script run, scorecard fresh
3. User sign-off captured
4. Tag message reference scorecard commit SHA + audit report
5. Tag NOT pushed remote until user explicit sign-off Phase H end

### 7.4. Khi audit content

1. Run audit script
2. Manual spot-check sample (10% random keyword)
3. Identify drift hoặc mismatch
4. Document trong audit report
5. Propose fix nếu drift > threshold

---

## 8. Version + Amendment Policy

### 8.1. Amendment requirement

Đổi nội dung file này phải có:

- User approve explicit
- Rationale documented
- Effective date
- Version bump (semantic v1.x)

### 8.2. Amendment log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| v1.0 | 2026-04-26 | Claude | Initial 5 GP per Phase A v3.7. User approve via /plan "ok" 2026-04-26 |

### 8.3. Compatibility

GP-1 đến GP-5 binding cho v3.7 plan + future plans. Past plans (v3.1-v3.6) governed by their own (loose) acceptance gates, không retroactive.

V3.7 plan + v4.0 release MUST comply 100%. Subsequent v4.x, v5.x, ... MUST comply unless governance amended.

---

## 9. References

- **Plan v3.7:** `plans/sdn/v3.7-reckoning-and-mastery.md`
- **CHANGELOG reckoning:** `CHANGELOG.md` section "Reckoning 2026-04-26"
- **REF source-of-truth:** `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`
- **Master index 0.3:** `sdn-onboard/0.3 - master-keyword-index.md`
- **Future scorecard (Phase D):** `memory/sdn/keyword-rubric-scorecard.md`
- **Future rubric formal (Phase B):** `memory/sdn/rubric-20-per-keyword.md`
- **CLAUDE.md Rule 15:** No Self-Tag (mirror GP-1 trong CLAUDE.md mandatory rules)

---

## 10. Quick Reference Card

| Cần làm | GP áp dụng |
|---------|-----------|
| Tag release | GP-1 (audit pass) + GP-4 (user gate) |
| Add scorecard cho keyword mới | GP-2 (scorecard committed) |
| Cohort batch done | GP-3 (re-audit) |
| Skip phase/gate | GP-4 (user authority bắt buộc) |
| Claim content gain qua script tweak | GP-5 (forbidden) |
| Propose new plan | All 5 GP (reference + comply) |

> **Đơn giản:** 5 GP + 8 user gate + scorecard ground truth + no metric gaming + reckoning past errors. Future plan không tái phạm v3.5/v3.6 mistakes.
