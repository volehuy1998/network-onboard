# Governance Principles, SDN Curriculum

> **Status:** Effective 2026-04-26 after Phase A of plan v3.7-Reckoning. Amended on 2026-04-26 to add GP-6 to GP-11 (v1.1 per plan v3.8-Remediation), on 2026-04-27 to add GP-12 (v1.2 per plan v3.9 Phase S8.4), and on 2026-04-28 to add GP-13 (v1.3 per plan v3.9.1 Phase Q12).
> **Scope:** the SDN curriculum (`sdn-onboard/*`), related plan files, and related memory artefacts. Other series (HAProxy, Linux, Network) reference this document but are not bound.
> **Authority:** VO LE (the owner) approved this file via `/plan` approval 2026-04-26.
> **Amendment:** changing this file requires explicit user approval and an entry in the "Amendment log" section at the end.
> **Language status:** Fully English (post-v3.9.1 Phase Q12, 2026-04-28). The pre-v1.3 Vietnamese version is preserved in git history for auditability.

---

## 0. Why this document exists

### 0.1. Event of 2026-04-26

The user audited the curriculum's actual depth using a 13-criteria check ("understands from foundation to deep expertise" for each keyword, plus 7 criteria proposed by Claude, totalling a 20-axis rubric). The audit found that v3.5 and v3.6 measured BREADTH (does any file mention the keyword) rather than DEPTH (does the curriculum teach the keyword fully). The tag names were grandiose ("Master / Deep / Full / Backbone / ContentDepth"), but they did not meet the mastery rubric the user mandated.

The v3.6-ContentDepth tag is a special case: the release tag was issued after one session that closed 6 keywords plus 9 alias-rule script tweaks, while the subsequent plan v3.7 estimated a realistic effort of 200 to 500 hours. **The tag claim was not consistent with the scope of effort**, which is a clear self-deception signal.

### 0.2. Lessons learned from v3.5 and v3.6

| Lesson | How v3.5 and v3.6 manifested | Fix through governance |
|--------|-----------------------------|-----------------------|
| Acceptance gates are easy to self-set | "Tier A MISSING <= 50" measured breadth | GP-1: rubric audit pass is mandatory |
| Self-tag without an external check | v3.6 tagged one session after the plan draft | GP-1 plus GP-4 user-approval gate |
| No tracked scorecard | The coverage matrix had per-file output but no per-keyword scorecard | GP-2: scorecard committed |
| Drift accumulated between phases | Each v3.x tag did not re-audit the full curriculum | GP-3: incremental verification |
| Cosmetic tweaks claimed as content gain | Alias-rule v2 and v3 framed as "well-covered 78%" | GP-5: no metric gaming |

---

## 1. Principle GP-1, No Tag Without Rubric Audit Pass

### 1.1. Definition

The SDN curriculum cannot receive any release tag (v3.x, v4.x, vX.Y) until **all** of the following are met simultaneously:

- (a) **Scorecard committed.** Every in-scope keyword (more than 320 entries in REF) has a 20-axis scorecard in the repo, version controlled, and auditable through `git log`.
- (b) **Threshold achieved.** Every keyword meets the minimum threshold per the Phase B rubric definition. Tier-specific thresholds:
  - Cornerstone (50 keywords): DEEP-20 (18 to 20 out of 20)
  - Medium (100 keywords): DEEP-15 (15 to 17 out of 20) or higher
  - Peripheral (170 keywords): PARTIAL-10 (10 to 14 out of 20) or higher
- (c) **Audit script run, report committed.** `scripts/per_keyword_rubric_audit.py` (a Phase D deliverable) ran successfully against the current curriculum HEAD; the resulting scorecard and flag list are committed in the same commit or in the immediately following commit.
- (d) **User written sign-off.** The user gives explicit confirmation (a chat message, a commit message, or a plan tracker entry) that the tag is approved. A verbal "ok" in chat is acceptable if the chat is captured in the commit message.

### 1.2. Rationale

The v3.6-ContentDepth tag was created on 2026-04-26 with the acceptance gate "Tier A MISSING <= 50" plus "well-covered >= 65%", which measured breadth, not depth. The user audit through the question "are 300+ keywords adequately covered against 13 criteria" exposed the tag as misleading because:

- The "Tier A MISSING" metric only measured whether any file mentions the keyword.
- A mention does not equal teaching against the full 20-axis rubric.
- The 20 percent Tier A reduction from 165 to 17 came mostly from alias rule changes (cosmetic), not from real content.

To prevent recurrence, governance requires a rubric audit pass before any tag.

### 1.3. Enforcement

**Pre-tag checklist (mandatory):**

1. Run `scripts/per_keyword_rubric_audit.py --full --commit-scorecard`.
2. Verify the scorecard is fresh (within a 24-hour lookback from the current commit).
3. Verify every keyword meets the threshold per Section 1.1.b (the script reports zero below threshold).
4. Verify user sign-off is captured (chat message reference plus commit message quote).
5. The annotated tag message must reference the scorecard commit SHA and the audit report path.

**Pre-commit hook (optional but recommended):** in `.git/hooks/pre-tag` or in a CI workflow, fail when the scorecard is stale or when a threshold is violated.

**Post-tag verification:** after the tag is created, anyone with repo access can re-run the audit script and verify the tag passes.

### 1.4. Exception Policy

- **Hotfix tag (vX.Y.Z patch):** allowed without a full rubric audit when the fix is (a) a security CVE upstream affecting keyword treatment, (b) a factual error correction (for example, a wrong commit SHA), or (c) a typo or formatting fix in existing content. Every hotfix must have:
  - User explicit approval for the hotfix scope.
  - A rubric impact assessment (affected axes, affected keywords) in the commit message.
  - A follow-up regression audit within 7 days of the tag.
- **Pre-release tag (vX.Y-rcN):** allowed for user review iteration during Phase H before the final tag. A pre-release tag is not subject to full GP-1 but must say "release candidate, not final" in the tag message.
- **No other exceptions.** "Quick win" tags, "milestone" tags, and "checkpoint" tags are not allowed.

---

## 2. Principle GP-2, Every Keyword Scorecard Committed

### 2.1. Definition

Every in-scope keyword in REF (`sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`) must have a 20-axis scorecard in the repo, version controlled, and auditable. Each scorecard records:

- Keyword name (verbatim from the REF entry).
- Per-axis score (0 = fail, 0.5 = partial, 1 = pass, N/A = not applicable).
- Per-axis evidence: a `file:line` citation or justification text.
- Total score (sum, plus tier classification per the Phase B threshold).
- Audit timestamp and script version.
- Manual override notes (if any).

Scorecard format: a Markdown table or JSON, with the format finalized in Phase B and Phase D. The proposed master scorecard file is `memory/sdn/keyword-rubric-scorecard.md`.

### 2.2. Rationale

A black-box claim of "complete / deep / master" without a scorecard cannot be audited, cannot be extended, and cannot be trusted. A future maintainer (including the original author six months later) cannot tell which keywords are actually adequate from those that were merely declared adequate.

The v3.5 master index (`0.3 - master-keyword-index.md`) has a one-line summary per keyword, which is a valuable navigation aid but NOT a depth scorecard. A separate scorecard file is needed to measure depth.

### 2.3. Enforcement

- **Phase D delivery:** the initial scorecard for the more than 320 keywords is committed for the first time.
- **Phase G per batch:** after each cohort batch, the scorecard is updated for affected keywords and committed in the same commit or in the immediately following commit.
- **GP-1 pre-tag check:** verify scorecard freshness.
- **New REF keyword (REF expanded):** a scorecard must exist within one commit cycle after the REF entry is added.

### 2.4. Exception Policy

- **Newly added REF keyword:** a grace period of one commit cycle to add a scorecard. The keyword is not tag-blocking during the grace period.
- **Deprecated REF keyword (removed from REF):** the scorecard moves to an archive section and is no longer tag-blocking.
- **No other exceptions.** Every active in-scope keyword has a scorecard.

---

## 3. Principle GP-3, Incremental Verified Progress

### 3.1. Definition

After each cohort batch in Phase G (or in any phase that adds content), the audit script must be re-run, the scorecard must be updated, and the update must be committed. Drift between content state and scorecard state must not exceed one commit.

A cohort batch is one logical content cohort (typically 5 to 15 keywords sharing a theme) written across one or several commits. After the cohort is done:

1. Run the audit script.
2. Verify each keyword in the cohort meets the threshold.
3. Verify the scorecard is updated.
4. Commit the scorecard update (in the same commit as the content or immediately after).

### 3.2. Rationale

Without per-batch verification, a cohort can be claimed as done while in reality some axes are missing. v3.5 and v3.6 had no per-cohort verification, so accumulated drift was hidden.

Example v3.6 drift: the tag claimed "well-covered 78%" but a substantive view (excluding the master index 0.3 from the count) showed only 72%. This information emerged through the v3 audit script enhancement, but at tag time there was no independent verification.

Per-batch verification catches drift early, while it is still fixable.

### 3.3. Enforcement

**Cohort commit pattern:**

```
Commit N+0: feat(sdn): cohort X content for keywords A, B, C
Commit N+1: chore(audit): scorecard update for cohort X
```

Or combined:

```
Commit N: feat(sdn): cohort X content plus scorecard update
```

**Audit script (CI or manual):** per-batch run is mandatory. Plan G acceptance gate:

- 100 percent of keywords in the cohort meet the minimum threshold per Phase B.
- Scorecard committed.
- Cross-link integrity: zero broken links.

### 3.4. Exception Policy

None. Drift is the bug. Skipping per-batch audit makes "cohort done" indistinguishable from "cohort claimed done".

---

## 4. Principle GP-4, User Approval Gates

### 4.1. Definition

Eight user approval gates per plan v3.7 Section 14:

| # | Gate | Approval form |
|---|------|--------------|
| 1 | Phase A end (governance plus tag handling) | Chat message or commit message quote |
| 2 | Phase B end (rubric formal final) | Chat message |
| 3 | Phase C end (rubric measurable from pilot) | Chat message |
| 4 | Phase D end (scorecard accuracy >= 85%) | Chat message |
| 5 | Phase E end (cohort order) | Chat message |
| 6 | Phase F end (framework structure F1 to F4 chosen) | Chat message |
| 7 | Phase G mid-points (every 5 to 10 cohort batches) | Chat message per checkpoint |
| 8 | Phase H end (final tag v4.0) | Written sign-off (chat plus commit message) |

Acceptable approval text: "yes", "proceed", "approved", "ok", or any equivalent in plan context.

### 4.2. Rationale

Self-completion is self-deception. The author cannot serve as the external check on themselves.

v3.6 had no user gate between the plan draft and the tag. Claude self-set the gate "<= 50 Tier A", self-passed it, and self-tagged. The user only discovered the issue days later through an explicit 13-criteria check. An explicit gate that required the user to spot-check 30 or more keywords against the rubric before the tag would have caught the issue immediately.

A user as external check is a required structure for a long-running plan, not optional.

### 4.3. Enforcement

- **Plan tracker:** `plans/sdn/v3.7-reckoning-and-mastery.md` Section 14 lists the 8 gates. Update gate status after each gate.
- **Commit message:** a commit that spans a gate must cite the gate approval (for example: `Per Phase A end gate, user approve "ok" 2026-04-26`).
- **Auto-proceed forbidden:** Phase Y must not start before Phase X gate approval, unless the user grants explicit authority for a specific gate.

### 4.4. Exception Policy

- **Time-bounded auto-proceed:** the user may grant authority for a specific gate (for example, "you decide Phase A on your own"). The authority must be:
  - Specific to the phase or gate (not general blanket authority).
  - Time-bounded (default expires when the gate is done).
  - Documented in the plan tracker.
- **Emergency unblock:** if the user is unavailable for more than 30 days, Claude may propose an interim continuation with limited scope (no tag, no schema change, no new plan). Resume full gate behaviour when the user returns.

---

## 5. Principle GP-5, No Metric Gaming

### 5.1. Definition

Audit metrics must measure DEPTH (per-keyword 20-axis rubric pass), not BREADTH (mention count, file count, line count, alias-match count).

Cosmetic tweaks must NOT be claimed as content gain:

- Alias rule changes (regex tweaks).
- Naming or renaming convention changes.
- Cross-link additions that do not add new content.
- File reorganization that does not add new content.
- False-positive reclassification.

Plan acceptance gates must reference the rubric scorecard, NOT a breadth metric.

### 5.2. Rationale

v3.6 case study: Tier A MISSING dropped from 165 to 17 (-87 percent), mostly through 9 new alias rules (action prefix strip, parenthetical strip, slash split, range expand, bilingual dictionary, tool prefix strip, table suffix strip, case-aware match, lookup spine separation).

Result on the audit script: better-looking numbers. Result on content: only 6 new keywords (`fin_timeout`, `push`, `pop`, `--print-wait-time`, `-u`, `ovs-tcpdump`), totalling about 120 lines of curriculum.

Framing this as "well-covered 78%" implies a massive content depth gain, while in reality the work was about 120 lines plus a script tweak. That is metric gaming.

Future plans must not repeat this.

### 5.3. Enforcement

- **Audit script reports** must include two separate sections:
  - **Tooling delta:** alias rule changes, regex tweaks, classification adjustments (cosmetic).
  - **Content delta:** new lines added, new keywords treated, new axes filled (substantive).
- **Plan acceptance gates** must reference the rubric scorecard metric, not the Tier A or B count.
- **Commit messages** must clearly distinguish tooling commits from content commits (`feat(sdn):` for content, `chore(audit):` for tooling, `refactor(scripts):` for refactor).
- **Tag messages** must not claim content gain through tooling.

### 5.4. Exception Policy

- **Tooling improvement commits are OK** but cannot be claimed as content depth in a tag or release.
- **Audit script v2, v3, vN evolution is OK** as long as the tag or release framing does not conflate tooling improvement with content gain.

---

## 6. Compliance Audit Pattern

### 6.1. Self-audit checklist (for Claude before proposing a tag)

Before proposing a tag, Claude must complete this checklist:

- [ ] **GP-1.a Scorecard committed:** `git log --oneline memory/sdn/keyword-rubric-scorecard.md` shows a recent update.
- [ ] **GP-1.b Threshold met:** `python scripts/per_keyword_rubric_audit.py --check-threshold` exits 0.
- [ ] **GP-1.c Audit report committed:** the report path exists in the repo.
- [ ] **GP-1.d User sign-off:** the chat message reference is recorded.
- [ ] **GP-2 Scorecard fresh:** scorecard timestamp within 24 hours of HEAD.
- [ ] **GP-3 No drift:** content commits since the last scorecard update equal 0, or the scorecard update is queued.
- [ ] **GP-4 Gate approved:** Phase H gate user sign-off captured.
- [ ] **GP-5 No metric gaming:** the tag message describes the content gain accurately and separates the tooling delta.

### 6.2. External audit workflow (for the user to verify)

The user may spot-check at any time:

1. `cat memory/sdn/keyword-rubric-scorecard.md` to view the latest scorecard.
2. Pick a random sample of keywords (for example, 30 entries).
3. Compare the scorecard claim against the actual content in the curriculum file.
4. Identify any mismatch.
5. Report the mismatch, then Claude fixes it with a GP-3 incremental commit.

### 6.3. Periodic full audit (recommended)

- After every major Phase end (Phase D, Phase G mid-points, Phase H).
- At least every quarter (3 months), even when there is no Phase boundary.
- When REF expands (REF version bump).

---

## 7. Application and Workflow

### 7.1. When writing a content cohort (Phase G)

1. Read the scorecard for the cohort keywords.
2. Identify missing axes.
3. Research and write to fill the missing axes.
4. Re-run the audit script.
5. Verify the cohort meets the threshold (GP-3).
6. Commit content plus scorecard update.
7. Cite the cohort review log entry.

### 7.2. When proposing a new plan

1. The plan must reference these governance principles.
2. Acceptance gates must measure depth (rubric scorecard), not breadth (count).
3. Plan effort estimates must be realistic (per the Phase D scorecard pilot).
4. The plan must list approval gates per GP-4.

### 7.3. When tagging a release

1. Pre-tag checklist Section 6.1 complete.
2. Audit script run, scorecard fresh.
3. User sign-off captured.
4. Tag message references the scorecard commit SHA and the audit report.
5. Tag is NOT pushed to remote until the user explicitly signs off at the Phase H end.

### 7.4. When auditing content

1. Run the audit script.
2. Manual spot-check on a sample (10 percent of random keywords).
3. Identify drift or mismatch.
4. Document in an audit report.
5. Propose a fix when drift exceeds the threshold.

---

## 8. Version and Amendment Policy

### 8.1. Amendment requirement

Changing this file requires:

- Explicit user approval.
- A documented rationale.
- An effective date.
- A version bump (semantic v1.x).

### 8.2. Amendment log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| v1.0 | 2026-04-26 | Claude | Initial 5 GP per Phase A v3.7. User approve via /plan "ok" 2026-04-26. |
| v1.1 | 2026-04-26 | Claude | GP-6 to GP-11 added per plan v3.8-Remediation Section 3 plus Section 11.3. Anti-gaming infrastructure mandatory. User approve via /plan "carefully made plan plus self-decide" 2026-04-26. |
| v1.2 | 2026-04-27 | Claude | GP-12 Post-Tag Regression Audit Cadence added per plan v3.9-OVSBlockHotfix Section 3 plus S8.4 ratification. T+7 day master block-level audit mandatory for every comprehensive tag. User approve via "finish S8 and close plan v3.9" instruction 2026-04-27. |
| v1.3 | 2026-04-28 | Claude | GP-13 English as the Mandatory Explanation Language added per plan v3.9.1 Phase Q12. The pre-v1.3 Vietnamese version is preserved in git history. User directive 2026-04-28: "every file modified by v3.9.1 must have its prose explanation rewritten in English"; "no em-dash allowed"; "CLAUDE.md and all training documents must be in English without Vietnamese". |

### 8.3. Compatibility

GP-1 to GP-5 are binding for plan v3.7 plus future plans. GP-6 to GP-11 are binding for plan v3.8 plus future plans. GP-12 is binding for v4.0+ tags. GP-13 is binding for any plan written after 2026-04-28. Past plans (v3.1 to v3.6) are governed by their own (loose) acceptance gates and are not retroactive.

The v3.7 plan plus the v4.0 release must comply 100 percent. Subsequent v4.x, v5.x, and so on must comply unless governance is amended.

---

## 9. References

- **Plan v3.7:** `plans/sdn/v3.7-reckoning-and-mastery.md`.
- **Plan v3.9.1:** `plans/sdn/v3.9.1-ovs-block-source-verify-hotfix.md`.
- **CHANGELOG reckoning:** `CHANGELOG.md` section "Reckoning 2026-04-26".
- **REF source of truth:** `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`.
- **Master index 0.3:** `sdn-onboard/0.3 - master-keyword-index.md`.
- **Future scorecard (Phase D):** `memory/sdn/keyword-rubric-scorecard.md`.
- **Future rubric formal (Phase B):** `memory/sdn/rubric-20-per-keyword.md`.
- **CLAUDE.md Rule 15:** No Self-Tag (mirror of GP-1 in CLAUDE.md mandatory rules).
- **CLAUDE.md Rule 16:** Internal-vs-Reader-Facing Language Separation (mirror of GP-11).
- **CLAUDE.md Rule 17:** English as the Mandatory Explanation Language (mirror of GP-13).
- **English style guide:** `memory/shared/english-style-guide.md`.

---

## 10. Quick Reference Card

| What you are doing | GP that applies |
|---------|----------|
| Tagging a release | GP-1 (audit pass) plus GP-4 (user gate) |
| Adding a scorecard for a new keyword | GP-2 (scorecard committed) |
| Cohort batch done | GP-3 (re-audit) |
| Skipping a phase or gate | GP-4 (user authority required) |
| Claiming content gain through script tweaks | GP-5 (forbidden) |
| Committing per-keyword content | GP-6 (Form A 1 keyword per commit, or Form B at most 5 keywords per commit) |
| Stamping cohort 5 axes by N keywords | GP-7 (forbidden, counted as 0 axes per keyword) |
| Cross-link table marking "DONE" cosmetically | GP-8 (forbidden, counted as 0 progress) |
| Per-keyword line-count threshold | GP-9 (cornerstone 50, medium 30, peripheral 15) |
| Pre-commit anti-gaming verification | GP-10 (mandatory script run, exit 0) |
| Internal axis, cohort, or phase label leaking into curriculum | GP-11 (forbidden in reader-facing files) |
| Writing prose in any non-English language inside CLAUDE.md, sdn-onboard, haproxy-onboard, plans, or memory | GP-13 (forbidden; English-only) |
| Proposing a new plan | All 13 GP (reference plus comply) |

---

## 11. Principle GP-6, Per-Keyword Commit Pattern (mandatory)

### 11.1. Definition

Every content commit in Phase R2 to R4 (or in any future per-keyword phase) must take **one** of two forms:

**Form A (preferred):** one keyword with full 20-axis treatment in one commit.

- Cornerstone: at least 50 lines of substantive content per keyword.
- Medium: at least 30 lines per keyword.
- Peripheral: at least 15 lines per keyword.

**Form B (acceptable):** a small group of at most 5 keywords in one commit, where each keyword:

- Has its own header section (`### keyword name` or `## §X.Y keyword`).
- Has explicit per-keyword 20-axis treatment (axes are not merged across keywords).
- Meets the per-tier minimum lines like Form A.

**Forbidden form:**

- A cohort table with 5 axes per N keywords (one line "5 axes covered" for 6 or more keywords).
- Cosmetic cross-link consolidation (a table marking the cohort "DONE / COVERED / STAMPED" without adding per-keyword axis content).
- "Group inheritance" (one axis statement covering several keywords without per-keyword evidence).

### 11.2. Rationale

The v3.7 Phase G gaming pattern packed 6 to 15 keywords into one commit with a 5-axis stamp table. Counting 5 axes for each keyword in the cohort produced a wrong-looking number; in reality, each keyword received about 0.83 axes from the batch plus a baseline 5 to 7 axes, totalling about 6 to 8 axes, far short of DEEP-15. The per-keyword commit pattern forces granular evidence and prevents this gaming.

### 11.3. Enforcement

- **Pre-commit hook** (`scripts/anti_gaming_check.py`): scans staged files to detect cohort-stamp patterns.
- **Commit message convention**: `feat(sdn): R{N} keyword <name> DEEP-{tier}` (Form A) or `feat(sdn): R{N} cohort <name> <=5 keyword DEEP-{tier}` (Form B).
- **Strict audit script** (`scripts/per_keyword_strict_audit.py`): per-keyword section detection plus scoring with `file:line` evidence.

### 11.4. Exception Policy

None. A cohort-level multi-keyword commit is forbidden in R2 to R4. The Form B 5-keyword cap is the maximum.

---

## 12. Principle GP-7, Cohort Stamp Forbidden

### 12.1. Definition

A single axis statement covering more than one keyword is **counted as 0 axes per keyword** (zero progress, not partial). The typical pattern:

```
| Keyword | Axis 1 | Axis 2 | Axis 3 | Axis 4 | Axis 5 |
|---------|--------|--------|--------|--------|--------|
| kw1     | done   | done   | done   | done   | done   |
| kw2     | done   | done   | done   | done   | done   |
| kw3     | done   | done   | done   | done   | done   |
```

Five axes covered for three keywords through the single header line "All cohort keywords share these axes" is a GP-7 violation.

### 12.2. Rationale

A header stamp saves bytes but does not produce per-keyword evidence. A reader reading kw3 specifically does not see content for kw3 axes 1 to 5; only the table claim. A future audit cannot verify how kw3 axis 8 (mechanism) differs from kw1 axis 8. Per GP-5 (no metric gaming): a table claim is not a content delta.

### 12.3. Enforcement

- `anti_gaming_check.py` regex detect: a table with at least 4 rows plus column headers containing "Axis N" is flagged for review.
- Strict audit: each per-keyword section must have at least the tier-minimum lines of explicit content per axis claimed.
- The commit is rejected when table stamp is dominant (more than 50 percent of the axis coverage is table-only).

### 12.4. Exception Policy

- **Catalog summary table** is OK (single-axis, for example a "Type" column in a taxonomy table); not a multi-axis stamp.
- **Cross-link reverse-index table** is OK (Section X.Y to file Z); does not claim axis coverage.

---

## 13. Principle GP-8, Cosmetic Stamp Forbidden

### 13.1. Definition

A cross-link consolidation table marking the cohort "DONE / COVERED / STAMPED" without adding per-keyword axis content is **counted as 0 progress**.

The typical pattern (a v3.7 Phase G batch 20 violation):

```
| Cohort | Keyword count | Status   | Cross-link |
|--------|---------------|----------|------------|
| P1     | 8             | STAMPED  | 9.28 + 9.31 |
| P2     | 15            | STAMPED  | 9.4         |
| ...    | ...           | STAMPED  | ...         |
```

165 keywords "stamped" through one table equals zero substantive axis fill, not "PARTIAL-10 reached".

### 13.2. Rationale

A cross-link is a useful navigation aid but is not content depth. Stamping a cohort "DONE" through a cross-link inflates the metric without improving engineer learning. Per GP-5: tooling and cosmetic improvements do not count as content gain.

### 13.3. Enforcement

- `anti_gaming_check.py` detects "STAMPED / DONE / COVERED" inside a cohort-level table without a dedicated keyword section.
- Strict audit: only count an axis when the evidence is a `file:line` citation in a dedicated keyword section.
- Commit message convention: `chore(meta): cross-link X` for navigation-only commits, NOT `feat(sdn): cohort X DONE`.

### 13.4. Exception Policy

None. Cross-link and navigation commits are OK but must use the `chore(meta):` prefix and must NOT claim tier achievement.

---

## 14. Principle GP-9, Min Lines Per Keyword

### 14.1. Definition

Substantive content lines per keyword (excluding shared boilerplate, table headers, and cross-link lines):

| Tier | Minimum lines per keyword |
|------|---------------------------|
| Cornerstone | 50 lines |
| Medium | 30 lines |
| Peripheral | 15 lines |

A treatment below the threshold is NOT counted toward the tier target. The keyword is classified down one tier.

### 14.2. Rationale

A 20-axis treatment with one to two sentences per axis comes to about 30 to 40 sentences, which is roughly 50 lines as a natural minimum for a cornerstone. A compact treatment below 30 lines for a cornerstone is insufficient depth per axis. The threshold forces a minimum substantive engagement with the keyword.

### 14.3. Counting rules

**Counted:**

- Prose sentences explaining concept, mechanism, or role.
- CLI command plus output sample.
- Table rows with content (not just the header).
- Code citation (file:line plus a brief description).
- Lab step instruction.
- Anatomy template attribute filled.

**NOT counted:**

- Section heading itself.
- Empty separator lines.
- Cross-link bullet "See Section X.Y".
- Boilerplate disclaimer.
- Table header row alone.

### 14.4. Enforcement

- The strict audit counts substantive lines per keyword section.
- A pre-commit warning fires when a keyword section is below the tier minimum (an override is allowed with a justification).

### 14.5. Exception Policy

- **High count of N/A axes** (for example, a keyword with 3 or more axes marked N/A per Section 23 of the rubric): the threshold scales by the effective denominator (50 times (20 minus N_NA) divided by 20).
- **Shared keyword section** (for example, two closely related keywords treated together): the combined section line count threshold equals the sum of the individual thresholds, with explicit per-keyword sub-headings.

---

## 15. Principle GP-10, Pre-Commit Verification Mandatory

### 15.1. Definition

The audit script `scripts/anti_gaming_check.py` must run pre-commit on staged files before every content commit in Phase R2 to R4. The commit is rejected (non-zero exit) on violation.

### 15.2. Verification scope

The script checks:

1. **Cohort-stamp detection** (GP-7): a table with column header containing "Axis N" plus at least 4 rows is flagged.
2. **Cosmetic-stamp detection** (GP-8): "STAMPED / DONE / COVERED" inside a cohort table without a dedicated section.
3. **Min lines per keyword** (GP-9): per-keyword section line count is at or above the tier minimum.
4. **Form compliance** (GP-6): Form A (1 keyword) or Form B (at most 5 keywords with explicit per-keyword headers).
5. **Rubric leak** (GP-11): forbidden internal terms detected through `rubric_leak_check.py`.

In addition, every commit on or after 2026-04-28 also runs:

6. **Em-dash check** (GP-13 plus CLAUDE.md Rule 17): `scripts/em_dash_check.py --staged` rejects any U+2014 em-dash in newly added or modified lines.
7. **Language detection check** (GP-13 plus CLAUDE.md Rule 17): `scripts/lang_check.py --staged` runs the lingua language detector on each added prose chunk and rejects any chunk detected as non-English with non-zero confidence.

### 15.3. Override mechanism

Manual override through the flag `--allow-meta` for:

- Memory file commits (`memory/*`).
- Plan file commits (`plans/*`).
- CHANGELOG.md "Reckoning" sections.
- Tooling or script commits that do not touch curriculum content.
- Master keyword index (`0.3 - master-keyword-index.md`) status code update.

The override must be documented in the commit message: `(anti-gaming-override: <reason>)`.

### 15.4. Hook installation

```bash
# Install once per clone:
bash scripts/pre-commit-install.sh
```

The hook runs on every `git commit` automatically. Bypass with `--no-verify` is strictly discouraged (CLAUDE.md Rule 4 git workflow plus the user's "Quality over Speed" mandate).

### 15.5. Enforcement

- Pre-commit hook rejects the violation.
- Pre-tag check verifies that all R2 to R4 commits passed the anti-gaming check.
- Future plan acceptance gates reference GP-10 compliance.

---

## 16. Principle GP-11, Internal-vs-Reader-Facing Language Separation

### 16.1. Definition

Curriculum content (`sdn-onboard/*.md`, `haproxy-onboard/*.md`, `linux-onboard/*.md`, `network-onboard/*.md` are reader-facing for the engineer) MUST NOT contain internal terminology of the plan, rubric, or governance.

**Forbidden in reader-facing content:**

| Term pattern | Reason | Replacement |
|-------------|--------|-------------|
| `**Axis N <category>.**` | The reader does not know "axis" | `**<category English name>.**` |
| `Axis 1 Concept`, `Axis 2 History`, ... | Internal rubric label | "Concept", "History and background", ... |
| `cohort C7`, `cohort M5`, `cohort P21` | Internal triage label | Skip or "the group of <description>" |
| `Phase G batch N`, `Phase R2`, `Phase R3`, `Phase R4` | Internal plan reference | Skip or "expansion of 2026-04" |
| `DEEP-20`, `DEEP-15`, `PARTIAL-10`, `REFERENCE-5`, `PLACEHOLDER` | Internal scoring tier | Skip or "comprehensive coverage", "fairly comprehensive coverage" |
| `rubric 20-axis`, `rubric 13-criteria` | Internal plan term | Skip |
| `gaming pattern`, `anti-gaming`, `cosmetic stamp` | Internal governance | Skip |
| `GP-1` through `GP-13` reference | Internal governance | Skip |

### 16.2. Replacement table for the 20 axes (English headings, post-v3.9.1)

Per the language pivot to English (CLAUDE.md Rule 17 plus GP-13), reader-facing curriculum uses the natural English heading for each axis. This table replaces the pre-v3.9.1 Vietnamese-heading mapping.

| Internal axis label | Reader-facing English heading |
|---------------------|-------------------------------|
| Axis 1 Concept | Concept |
| Axis 2 History | History and background |
| Axis 3 Placement | Position in the architecture |
| Axis 4 Role | Role |
| Axis 5 Motivation | Why it exists |
| Axis 6 Problem | Problems it solves |
| Axis 7 Importance | Importance |
| Axis 8 Mechanism | How it works |
| Axis 9 Engineer-op | How an operator masters this |
| Axis 10 Taxonomy | Classification |
| Axis 11 Workflow | Usage workflow |
| Axis 12 Troubleshoot | When something goes wrong |
| Axis 13 Coupling | Tightly related to |
| Axis 14 Version drift | Version differences |
| Axis 15 Verification | Observation and verification |
| Axis 16 Source code | Source code reference |
| Axis 17 Incident | Real-world incident |
| Axis 18 Lab | Synthetic exercise |
| Axis 19 Failure mode | Common failures and diagnostic signals |
| Axis 20 Cross-domain | Comparison with other systems |

### 16.3. Rationale

The curriculum exists to teach engineers SDN, OVS, and OVN internals. The internal plan and governance tooling are for the author. A reader (a Vietnamese network engineer learning SDN) who sees "**Axis 7 importance**" is confused, because they do not know what "axis" means and are not familiar with the internal scoring system. Mixing the two layers adds noise, causes confusion, and reduces learning effectiveness.

### 16.4. Allowed exceptions

Forbidden patterns are OK in:

- `memory/*` (working and meta files, internal audience).
- `plans/*` (plan documents, internal audience).
- `CLAUDE.md` (project meta plus rule definitions).
- `CHANGELOG.md` "Reckoning" sections (meta history audience).
- `0.3 - master-keyword-index.md` MAY use the status code `DEEP / BREADTH / SHALLOW / MISSING / PLACEHOLDER` per the existing convention (this is a pre-existing breadth taxonomy, not the 20-axis tier system).
- Commit messages (internal audit log audience).

### 16.5. Enforcement

- **Pre-commit hook** (`scripts/rubric_leak_check.py`): regex scan of staged files; the commit is rejected on a violation in a non-exempt path.
- **CLAUDE.md Rule 16**: a mirror of GP-11 binding for all session work.
- **Curriculum cleanup pass** (Phase R0.7): replace existing leaked terms in about 25 files modified during Phase G v3.7.

### 16.6. Exception Policy

- **Quoted plan reference inside a callout** (for example, `> See plan v3.8 R2 for treatment depth`) is acceptable when quoted as an external reference, not integrated into teaching prose.
- **Migration-period grandfather**: existing leaks in files not yet cleaned up (pre-Phase R0.7) are NOT counted as a new violation; Phase R0.7 will scrub all of them.
- **No other exceptions.** Author convenience does not justify reader confusion.

---

## 17. Principle GP-12, Post-Tag Regression Audit Cadence

### 17.1. Definition

After each tag `v4.x-MasteryComplete`, `v4.x-FullDepth`, or any other "comprehensive" claim, a regression audit cycle is **mandatory**:

- **T+0 to T+7 days:** master block-level audit (multi-agent parallel) for at least one major block (OVS or OVN or OF). The audit must cover:
  - Per-file 20-axis tier verification (random subset of 20 to 30 percent of the files in the block).
  - Cross-file structural integrity (numbering collision, broken cross-link).
  - Systemic axis under-coverage detection (axis 17 incident, axis 20 cross-domain, axis 14 version drift across the block).
  - Editorial placeholder or botched-replacement scan (`XXXXXX`, `thị field`, `TODO`, `FIXME`).
  - Rule 14 source-citation verification (sample SHAs through MCP GitHub or `gh` CLI).

- **Findings categorized** by severity: CRITICAL, HIGH, MEDIUM, LOW.

- **CRITICAL or HIGH findings** trigger a hotfix plan (like v3.9) within 14 days.

- **MEDIUM or LOW findings** are logged in `memory/sdn/post-tag-audit-YYYY-MM-DD.md` for a future plan to address.

### 17.2. Rationale

In v3.8 R5, the user spot-checked 30 of 331 keywords (a 9 percent sample). Stratified random sampling does not catch:
- A sub-tooling gap (a regex pattern blind spot).
- A cross-file structural collision.
- A systemic decline pattern (axis 17, axis 20).

A master block-level multi-agent audit has depth per file, breadth across files, and systemic-pattern detection that spot-checks cannot achieve. The T+7 day cadence catches issues while context is still fresh.

The v4.0-MasteryComplete tag (2026-04-26) demonstrated the gap: the T+1 day master audit (2026-04-27) found 6 categories of violations within the verified scope of the tag claim. GP-12 codifies this pattern as mandatory.

### 17.3. Enforcement

- A plan tracker entry `memory/sdn/post-tag-audit-schedule.md` tracks the cadence.
- The annotated tag message references the scheduled audit date.
- The audit findings file is committed as `memory/sdn/post-tag-audit-<tag>-<date>.md`.
- CRITICAL or HIGH findings trigger a hotfix plan within 14 days OR an explicit deferral with justification.
- Hook check (optional, future): `scripts/post_tag_audit_due.py` warns when the tag is more than 7 days old without an audit file.

### 17.4. Exception Policy

- **Pre-release tag (vX.Y-rcN):** does not require a full block audit; only spot-check.
- **Hotfix tag (vX.Y.Z):** does not trigger a new cadence (it is already the result of an audit cycle).
- **Tag with explicit limited scope** (for example, `v3.6-AuditTooling` is tooling only): only audit the scope of the tag claim.
- **No other exceptions.** A comprehensive tag means a comprehensive audit follow-up.

### 17.5. Compliance audit pattern

Before issuing a new tag (post v4.0):

- [ ] Pre-tag audit: GP-1 4-condition check met.
- [ ] Annotated tag message: includes the scheduled GP-12 audit date (T+7 day).
- [ ] Post-tag (T+0 to T+7): execute the master block-level audit per GP-12 Section 17.1.
- [ ] CRITICAL or HIGH found: trigger a hotfix plan within 14 days.
- [ ] Audit report committed under `memory/sdn/post-tag-audit-<tag>-<date>.md`.

### 17.6. Origin

Plan v3.9-OVSBlockHotfix Section 3 proposed GP-12 pre-S0 (2026-04-27). Ratified in Phase S8.4 with implicit user approval through the instruction "finish S8 and close plan v3.9" (2026-04-27). Effective immediately for v4.0 and later tags.

---

## 18. Principle GP-13, English as the Mandatory Explanation Language

### 18.1. Definition

Every explanatory prose text written or modified in this repository, including curriculum files (`sdn-onboard/*.md`, `haproxy-onboard/*.md`), working files (CLAUDE.md, `memory/*`), plan files (`plans/*`), audit logs, and commit messages, must be written in plain technical English. The authoritative style guide is at `memory/shared/english-style-guide.md`.

**No Vietnamese in newly written content.** Inside the named scope (CLAUDE.md, `sdn-onboard/*.md`, `haproxy-onboard/*.md`, `memory/*`, `plans/*`), no Vietnamese prose, callout label, heading, or example is allowed in any newly written or modified content. Verbatim quotes of an owner directive that was originally given in Vietnamese are translated to English with the attribution "Translated from Vietnamese original, dated YYYY-MM-DD". The Vietnamese source text is preserved in git history (the commit before the translation) for auditability.

**One narrow scoped allowance.** The historical dictionary at `memory/shared/rule-11-dictionary.md` keeps its bilingual body as a one-way translation reference for the plan v3.12 legacy migration. Its header is in English and marks the file as frozen. The pre-commit `lang_check.py` allowlist exempts that exact path.

**Em-dash discipline.** The em-dash character (Unicode U+2014, the long horizontal dash with the width of approximately one M) is forbidden in any newly written or modified content. Use a comma, a period, a colon, parentheses, or a bulleted list instead. This supersedes the previous Rule 13 density-based discipline.

**Pre-commit enforcement.** Two scripts enforce GP-13 at commit time:

1. `scripts/em_dash_check.py --staged` rejects any em-dash on a newly added or modified line.
2. `scripts/lang_check.py --staged` runs the lingua language detector on each added prose chunk and rejects any chunk detected as Vietnamese with non-zero confidence (strict mode per the user directive 2026-04-28).

Both scripts run in diff-only mode in `--staged` mode (per plan v3.9.1 Phase Q-1.E). Pre-existing em-dashes or Vietnamese chunks on lines that the staged change does not touch are NOT flagged. The full repository audit happens at plan v3.12 closure with `--all` mode.

**Plan-level enforcement.** Every plan file under `plans/*` must include both scripts in its acceptance gate. The final-audit phase of any plan runs both scripts on `--all` and the plan cannot close until the count is zero across every Markdown file in scope.

**Pedagogical requirement.** The English prose must remain accessible to Vietnamese network engineers reading at CEFR B2 to C1 level. Use short declarative sentences. Use plain vocabulary. Do not abbreviate (`for example`, not `e.g.`; `that is`, not `i.e.`; `and so on`, not `etc.`). Preserve the why-before-what pedagogy from CLAUDE.md SECOND NORTH STAR.

### 18.2. Rationale

The user directive of 2026-04-28 was three consecutive instructions:
1. "Every file modified by v3.9.1 must have its prose explanation rewritten in English."
2. "No em-dash allowed."
3. "CLAUDE.md and all training documents must be written in English without Vietnamese."

The motivation is twofold. First, English is the canonical language of every upstream OVS, OVN, and OpenFlow specification, source comment, mailing list, and patch. A curriculum that explains internals in Vietnamese forces the reader to switch language every time they cross between curriculum and upstream source, which is friction that degrades learning. Second, the audience is engineers who already read upstream documentation in English; the prior bilingual framing (Vietnamese prose plus English identifiers) was a transitional convenience that has outlived its usefulness.

The em-dash ban is stricter than the previous Rule 13 density target (less than 0.10 per line). Zero is the rule. The reason is that em-dashes are a stylistic preference, not a technical requirement, and their inconsistent use across hundreds of files makes the repository visually noisy.

### 18.3. Enforcement

- **Pre-commit hooks** (Section 18.1): two scripts run on every commit.
- **CLAUDE.md Rule 17** mirrors GP-13 for session-by-session work.
- **Plan v3.9.1 Phase Q1 to Q5** translates the curriculum sections that contain hotfix violations to English in the same commit.
- **Plan v3.12** (curriculum-wide English migration, deferred) translates the remaining roughly 120 legacy curriculum files.

### 18.4. Exception Policy

- **Verbatim quote of an upstream artefact** (a commit message body, a NEWS file entry, an RFC, a man page) stays verbatim, including any non-English content. The quote must be wrapped in a fenced code block or a `>` blockquote and attributed.
- **Verbatim quote of a Vietnamese owner directive** in a plan or memory file is translated to English with the attribution "Translated from Vietnamese original, dated YYYY-MM-DD". The Vietnamese source text is preserved in git history.
- **Existing Vietnamese curriculum sections** in files that v3.9.1 does not modify remain valid until plan v3.12 closes. Files modified by v3.9.1 carry a `**Language status:**` callout immediately after the H1 heading, listing which sections are now English. Files not yet touched stay legacy Vietnamese without a marker; plan v3.12 will add markers and translations in batches.
- **The Rule 11 historical dictionary** at `memory/shared/rule-11-dictionary.md` keeps its bilingual body as a translation reference for plan v3.12. Its header is in English.
- **`linux-onboard/*` and `network-onboard/*`** are out of the active migration scope per the user directive of 2026-04-28 (focus is on the SDN training program). They may stay as-is.
- **No other exceptions.**

### 18.5. Compliance audit pattern

Every plan written after 2026-04-28 must include this checklist line in every phase that modifies Markdown:

```
- [ ] python scripts/em_dash_check.py --staged (or --all for full audit) returns exit 0 with PASS.
- [ ] python scripts/lang_check.py --staged (or --all for full audit) returns exit 0 with PASS.
```

The plan author is responsible for adding the explicit checklist line. The pre-commit hook coverage runs `--staged` automatically; the plan-level requirement uses `--all` for the entire repository.

### 18.6. Origin

Plan v3.9.1 Phase Q-1.C ratified GP-13 with user approval through the three directives of 2026-04-28. Phase Q12 of plan v3.9.1 wrote this section (2026-04-28). Effective immediately for any plan written after 2026-04-28 and for any file modified after 2026-04-28.

---

## 19. Closing summary

13 governance principles plus 8 user gates plus a scorecard ground truth plus no metric gaming plus per-keyword granular commits plus anti-gaming pre-commit verification plus reader-versus-internal language separation plus post-tag regression audit cadence plus an English-only language policy plus a reckoning of past errors. The v3.9 hotfix exposed the need for GP-12 to prevent recurrence on future v4.x tags. The v3.9.1 hotfix added GP-13 to lock in the English language pivot for the SDN training program.
