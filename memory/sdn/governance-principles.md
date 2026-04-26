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
| v1.1 | 2026-04-26 | Claude | GP-6 đến GP-11 added per Plan v3.8-Remediation Section 3 + Section 11.3. Anti-gaming infrastructure mandatory. User approve via /plan "tự đưa ra plan kỹ lưỡng + tự quyết" 2026-04-26 |

### 8.3. Compatibility

GP-1 đến GP-5 binding cho v3.7 plan + future plans. GP-6 đến GP-11 binding cho v3.8 plan + future plans. Past plans (v3.1-v3.6) governed by their own (loose) acceptance gates, không retroactive.

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
| Commit per-keyword content | GP-6 (Form A 1kw/commit hoặc Form B ≤5kw/commit) |
| Cohort 5-axis × N keyword stamp | GP-7 (forbidden, count = 0 axis per kw) |
| Cross-link table marking "DONE" cosmetic | GP-8 (forbidden, count = 0 progress) |
| Threshold dòng per keyword | GP-9 (cornerstone 50, medium 30, peripheral 15) |
| Pre-commit anti-gaming verification | GP-10 (mandatory script run, exit 0) |
| Internal axis/cohort/phase label leak vào curriculum | GP-11 (forbidden trong reader-facing file) |
| Propose new plan | All 11 GP (reference + comply) |

---

## 11. Principle GP-6, Per-Keyword Commit Pattern (mandatory)

### 11.1. Definition

Mỗi content commit Phase R2-R4 (hoặc bất kỳ phase per-keyword work nào tương lai) MUST có **một** trong 2 form sau:

**Form A (preferred):** 1 keyword full 20-axis treatment trong 1 commit:

- Cornerstone: min 50 dòng substantive content per keyword
- Medium: min 30 dòng per keyword
- Peripheral: min 15 dòng per keyword

**Form B (acceptable):** Small group ≤ 5 keyword cùng commit, mỗi keyword:

- Có header section riêng (`### keyword name` hoặc `## §X.Y keyword`)
- Có 20-axis explicit per keyword (không gộp axis)
- Min lines per tier như Form A

**Form FORBIDDEN:**

- Cohort table 5-axis × N keyword (1 line "5 axis covered" cho 6+ keyword)
- Cosmetic cross-link consolidation (table marking cohort "DONE/COVERED/STAMPED" mà không add per-keyword axis content)
- "Group inheritance" (1 axis statement covers multiple keyword without per-keyword evidence)

### 11.2. Rationale

V3.7 Phase G gaming pattern: cohort batch dồn 6-15 keyword vào 1 commit với 5-axis stamp table → đếm 5 axis cho mỗi keyword trong cohort, thực tế mỗi keyword chỉ ~0.83 axis từ batch + baseline 5-7 axis = ~6-8 axis ≠ DEEP-15. Per-keyword commit pattern force granular evidence + ngăn chặn gaming.

### 11.3. Enforcement Mechanism

- **Pre-commit hook** (`scripts/anti_gaming_check.py`): scan staged file detect cohort-stamp pattern
- **Commit message convention**: `feat(sdn): R{N} keyword <name> DEEP-{tier}` (Form A) hoặc `feat(sdn): R{N} cohort <name> ≤5 keyword DEEP-{tier}` (Form B)
- **Strict audit script** (`scripts/per_keyword_strict_audit.py`): per-keyword section detection + score with file:line evidence

### 11.4. Exception Policy

None. Cohort-level multi-keyword commit FORBIDDEN trong R2-R4. Form B 5-keyword cap là maximum.

---

## 12. Principle GP-7, Cohort Stamp Forbidden

### 12.1. Definition

Single axis statement covering > 1 keyword = **counted as 0 axis per keyword** (zero progress, không partial). Pattern điển hình:

```
| Keyword | Axis 1 | Axis 2 | Axis 3 | Axis 4 | Axis 5 |
|---------|--------|--------|--------|--------|--------|
| kw1     | done   | done   | done   | done   | done   |
| kw2     | done   | done   | done   | done   | done   |
| kw3     | done   | done   | done   | done   | done   |
```

5 axis covered cho 3 keyword qua single header line "All cohort keyword share these axes" = GP-7 violation.

### 12.2. Rationale

Header-stamp tiết kiệm bytes nhưng không tạo per-keyword evidence. Engineer reader đọc kw3 specifically không có content riêng cho kw3 axes 1-5; chỉ có table claim. Future audit không thể verify kw3 axis 8 (mechanism) khác kw1 axis 8 ra sao. Per GP-5 (no metric gaming): table-claim ≠ content delta.

### 12.3. Enforcement Mechanism

- `anti_gaming_check.py` regex detect: table với row ≥ 4 + column header chứa "Axis N", flag for review
- Strict audit: per-keyword section MUST have ≥ tier-min lines explicit content per axis claimed
- Commit reject if table-stamp dominant (> 50% axis coverage qua table-only)

### 12.4. Exception Policy

- **Catalog summary table** OK (1 axis only, e.g., "Loại" column trong taxonomy table) — không phải multi-axis stamp
- **Cross-link reverse-index table** OK (Phần X.Y → file Z) — không claim axis coverage

---

## 13. Principle GP-8, Cosmetic Stamp Forbidden

### 13.1. Definition

Cross-link consolidation tables marking cohort "DONE/COVERED/STAMPED" mà KHÔNG add per-keyword axis content = **counted as 0 progress**.

Pattern điển hình (V3.7 Phase G batch 20 violation):

```
| Cohort | Keyword count | Status | Cross-link |
|--------|---------------|--------|------------|
| P1 | 8 | STAMPED | 9.28 + 9.31 |
| P2 | 15 | STAMPED | 9.4 |
| ... | ... | STAMPED | ... |
```

165 keyword "stamped" qua 1 table = 0 substantive axis fill, ≠ "PARTIAL-10 reached".

### 13.2. Rationale

Cross-link là useful navigation aid nhưng không phải content depth. Stamping cohort "DONE" qua cross-link inflate metric mà không tăng engineer learning. Per GP-5: tooling/cosmetic improvement không count as content gain.

### 13.3. Enforcement Mechanism

- `anti_gaming_check.py`: detect "STAMPED/DONE/COVERED" trong cohort-level table without dedicated keyword section
- Strict audit: only count axis với evidence = file:line citation in dedicated keyword section
- Commit message convention: `chore(meta): cross-link X` for navigation-only commits, NOT `feat(sdn): cohort X DONE`

### 13.4. Exception Policy

None. Cross-link/navigation commits OK nhưng MUST use `chore(meta):` prefix and KHÔNG claim tier achievement.

---

## 14. Principle GP-9, Min Lines Per Keyword

### 14.1. Definition

Substantive content lines per keyword (excluding shared boilerplate, table header, cross-link line):

| Tier | Min lines per keyword |
|------|----------------------|
| Cornerstone | 50 dòng |
| Medium | 30 dòng |
| Peripheral | 15 dòng |

Below threshold = treatment NOT counted toward tier target. Keyword classified down 1 tier.

### 14.2. Rationale

20-axis treatment với mỗi axis 1-2 sentences = ~30-40 sentences = ~50 dòng natural minimum cho cornerstone. Compact treatment dưới 30 dòng cho cornerstone = insufficient depth per axis. Threshold force minimum substantive engagement với keyword.

### 14.3. Counting rules

**Counted:**

- Prose sentences explaining concept/mechanism/role
- CLI command + output sample
- Table rows với content (không chỉ header)
- Code citation (file:line + brief description)
- Lab step instruction
- Anatomy template attribute filled

**NOT counted:**

- Section heading itself
- Empty separator lines
- Cross-link bullet "See Phần X.Y"
- Boilerplate disclaimer
- Table header row alone

### 14.4. Enforcement Mechanism

- Strict audit count substantive lines per keyword section
- Pre-commit warning if keyword section < tier-min (allow override với justification)

### 14.5. Exception Policy

- **N/A axis high count** (e.g., keyword với 3+ axis N/A theo Section 23 rubric): threshold scale per effective denominator (50 × (20-N_NA)/20)
- **Keyword shared section** (e.g., 2 closely-related keyword treated together): combined section line count threshold = sum of individual thresholds, with explicit per-keyword sub-headings

---

## 15. Principle GP-10, Pre-Commit Verification Mandatory

### 15.1. Definition

Audit script `scripts/anti_gaming_check.py` MUST run pre-commit on staged files trước mỗi content commit Phase R2-R4. Reject commit (non-zero exit) on violation.

### 15.2. Verification scope

Script checks:

1. **Cohort-stamp detection** (GP-7): table column header chứa "Axis N" + row ≥ 4 → flag
2. **Cosmetic-stamp detection** (GP-8): "STAMPED/DONE/COVERED" trong cohort table without dedicated section
3. **Min lines per keyword** (GP-9): per-keyword section line count ≥ tier-min
4. **Form compliance** (GP-6): Form A (1 kw) hoặc Form B (≤5 kw with explicit per-kw header)
5. **Rubric leak** (GP-11): forbidden internal terms via `rubric_leak_check.py`

### 15.3. Override mechanism

Manual override via flag `--allow-meta` cho:

- Memory file commits (`memory/*`)
- Plan file commits (`plans/*`)
- CHANGELOG.md "Reckoning" sections
- Tooling/script commits không touch curriculum content
- Master keyword index (`0.3 - master-keyword-index.md`) status code update

Override MUST be documented trong commit message: `(anti-gaming-override: <reason>)`.

### 15.4. Hook installation

```bash
# Install once per clone:
bash scripts/pre-commit-install.sh
```

Hook runs on every `git commit` automatically. Bypass với `--no-verify` STRICTLY discouraged (CLAUDE.md Rule 4 git workflow + violates user "Quality > Speed" mandate).

### 15.5. Enforcement

- Hook pre-commit reject violation
- Tag pre-tag check verify all R2-R4 commits passed anti-gaming check
- Future plan acceptance gates reference GP-10 compliance

---

## 16. Principle GP-11, Internal-vs-Reader-Facing Language Separation

### 16.1. Definition

Curriculum content (file `sdn-onboard/*.md`, `haproxy-onboard/*.md`, `linux-onboard/*.md`, `network-onboard/*.md` là reader-facing cho engineer) MUST KHÔNG chứa internal terminology của plan/rubric/governance.

**Forbidden in reader-facing content:**

| Term pattern | Reason | Replacement |
|-------------|--------|-------------|
| `**Axis N <category>.**` | Reader không biết "axis" | `**<category VN name>.**` |
| `Axis 1 Concept`, `Axis 2 History`, ... | Internal rubric label | "Khái niệm", "Lịch sử + bối cảnh", ... |
| `cohort C7`, `cohort M5`, `cohort P21` | Internal triage label | Skip hoặc "nhóm <description>" |
| `Phase G batch N`, `Phase R2/R3/R4` | Internal plan reference | Skip hoặc "expansion 2026-04" |
| `DEEP-20`, `DEEP-15`, `PARTIAL-10`, `REFERENCE-5`, `PLACEHOLDER` | Internal scoring tier | Skip hoặc prose "đầy đủ", "khá đầy đủ" |
| `rubric 20-axis`, `rubric 13-tiêu-chí` | Internal plan term | Skip |
| `gaming pattern`, `anti-gaming`, `cosmetic stamp` | Internal governance | Skip |
| `GP-1` đến `GP-11` reference | Internal governance | Skip |

### 16.2. Replacement table for 20 axis

Reader-facing curriculum dùng natural Vietnamese heading thay rubric label:

| Internal axis label | Reader-facing VN heading |
|---------------------|-------------------------|
| Axis 1 Concept | Khái niệm |
| Axis 2 History | Lịch sử + bối cảnh |
| Axis 3 Placement | Vị trí trong kiến trúc |
| Axis 4 Role | Vai trò |
| Axis 5 Motivation | Vì sao sinh ra |
| Axis 6 Problem | Vấn đề giải quyết |
| Axis 7 Importance | Tầm quan trọng |
| Axis 8 Mechanism | Cơ chế hoạt động |
| Axis 9 Engineer-op | Cách kỹ sư vận hành thành thạo |
| Axis 10 Taxonomy | Phân loại |
| Axis 11 Workflow | Quy trình sử dụng |
| Axis 12 Troubleshoot | Khi xảy ra sự cố |
| Axis 13 Coupling | Liên quan mật thiết |
| Axis 14 Version drift | Khác biệt giữa các phiên bản |
| Axis 15 Verification | Cách quan sát + xác minh |
| Axis 16 Source code | Source code tham chiếu |
| Axis 17 Incident | Trường hợp sự cố thực tế |
| Axis 18 Lab | Bài tập synthetic |
| Axis 19 Failure mode | Lỗi thường gặp + tín hiệu chẩn đoán |
| Axis 20 Cross-domain | So sánh với hệ khác |

### 16.3. Rationale

Curriculum tồn tại để teach engineer SDN/OVS/OVN internals. Internal plan + governance tooling là cho author. Reader (kỹ sư VN học SDN) đọc thấy "**Axis 7 importance**" sẽ confuse vì không biết axis là gì, không quen với internal scoring system. Mixing 2 layer = noise + confusion + reduce learning effectiveness.

### 16.4. Allowed exceptions

Forbidden patterns OK trong:

- `memory/*` (working/meta files, internal audience)
- `plans/*` (plan documents, internal audience)
- `CLAUDE.md` (project meta + Rule definitions)
- `CHANGELOG.md` "Reckoning" sections (meta history audience)
- `0.3 - master-keyword-index.md` MAY use status code `DEEP/BREADTH/SHALLOW/MISSING/PLACEHOLDER` per existing convention (NOT 20-axis tier system; status code là pre-existing breadth taxonomy không phải rubric)
- Commit messages (internal audit log audience)

### 16.5. Enforcement Mechanism

- **Pre-commit hook** (`scripts/rubric_leak_check.py`): regex scan staged files, reject commit on violation in non-exempt path
- **CLAUDE.md Rule 16**: mirror GP-11 binding cho all session work
- **Curriculum cleanup pass** (Phase R0.7): replace existing leaked terms in ~25 files modified Phase G v3.7

### 16.6. Exception Policy

- **Quoted plan reference inside callout** (e.g., `> See plan v3.8 R2 for treatment depth`) acceptable nếu quoted as external reference, không integrate vào teaching prose
- **Migration-period grandfather**: existing leak trong files chưa cleanup (pre-Phase R0.7) NOT counted as new violation; Phase R0.7 sẽ scrub all
- **No other exceptions.** Author convenience không justify reader confusion.

---

> **Đơn giản:** 11 GP + 8 user gate + scorecard ground truth + no metric gaming + per-keyword granular commit + anti-gaming pre-commit verification + reader-vs-internal language separation + reckoning past errors. V3.8 plan không tái phạm v3.5/v3.6/v3.7 mistakes.
