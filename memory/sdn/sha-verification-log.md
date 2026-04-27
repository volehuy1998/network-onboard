# SHA Verification Log (Plan v3.9 Phase S7.C)

> **Generated:** 2026-04-27 by `gh api repos/openvswitch/ovs/commits/<sha>` MCP verification.
> **Plan:** [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md) Phase S7.C
> **Purpose:** Verify ~10 commit SHA cited cross-block in OVS curriculum theo Rule 14 §14.1.
> **Method:** `gh api repos/openvswitch/ovs/commits/<sha>` for each SHA; record author + date + message.

---

## 1. Summary

| Status | Count | SHA list |
|--------|------:|----------|
| Verified existing | 5 | 180ab2fd635e, 464bc6f9, 0d9dc8e9, 978427a5, 8b7ea2d4 |
| Not found via API | 3 | 5ca1ba9 (truncated 7-char), 8e53fe8e22, cd278bd35e |

5/8 = 63% verified. 3 unverified flagged for curriculum follow-up action.

---

## 2. Verified SHA (existing in upstream repo)

### 2.1. `180ab2fd635e`

- **Cited in:** `9.2:573, 1601, 1631, 1635, 1643`, `9.26:13, 43, 62, 107, 121, 208`, `16.1:347`
- **Verified verbatim:**
  - Author: Eelco Chaudron
  - Date: 2024-08-29T07:00:06Z
  - Message: "ofproto-dpif-upcall: Avoid stale ukeys leaks."
- **Status:** VERIFIED. Citation accurate.
- **Note:** Master audit Agent A flagged này là "soft-verify needed"; now confirmed via gh api. Per Rule 14.1, full 40-char SHA should be cited eventually.

### 2.2. `464bc6f9`

- **Cited in:** `9.26:14, 359`
- **Verified verbatim:**
  - Author: Ilya Maximets
  - Date: 2024-11-28T13:18:16Z
  - Message: "ofproto-dpif-upcall: Fix use of uninitialized missed dumps counter."
- **Status:** VERIFIED. Citation accurate.

### 2.3. `0d9dc8e9`

- **Cited in:** `9.26:15, 208`
- **Verified verbatim:**
  - Author: Ilya Maximets
  - Date: 2025-07-08T11:34:02Z
  - Message: "dpif-netlink: Provide original upcall pid in 'execute' commands."
- **Status:** VERIFIED. Citation accurate.

### 2.4. `978427a5`

- **Cited in:** `9.8:281` (`cache_active_timeout` IPFIX 2013)
- **Verified verbatim:**
  - Author: Romain Lenglet
  - Date: 2013-08-21T20:49:04Z
  - Message: "ipfix: implement flow caching and aggregation in exporter"
- **Status:** VERIFIED. Citation accurate (matches "OVS 2.0 IPFIX import" claim).

### 2.5. `8b7ea2d4`

- **Cited in:** `9.8:359` (IPFIX `Flow_Sample_Collector_Set` 2015 / OVS 2.4)
- **Verified verbatim:**
  - Author: Wenyu Zhang
  - Date: 2014-08-18T03:19:36Z
  - Message: "Extend OVS IPFIX exporter to export tunnel headers"
- **Status:** VERIFIED EXISTS. **Citation date discrepancy**: curriculum claims 2015 OVS 2.4, but commit date is 2014-08-18. OVS 2.4 was released 2015-08, so feature work happened earlier. Citation accurate for "OVS 2.4 path" but year reference 2015 should ideally be 2014 (commit) hoặc 2015 (release).

---

## 3. SHA NOT verified (curriculum action needed)

### 3.1. `5ca1ba9` (truncated 7-character)

- **Cited in:** `9.8:214` ("active_timeout=-1 semantic disable thêm sau OVS 1.6 (commit `5ca1ba9` 2011)")
- **gh api result:** "No commit found for SHA: 5ca1ba9" (HTTP 422)
- **Verification attempt:** tried `5ca1ba9`, `5ca1ba9b`, `5ca1ba9c`, `5ca1ba9d` — all 404.
- **Hypothesis:** SHA prefix may be too short for unique ID at OVS repo size (~26K commits since 2009). Need ≥8 char minimum. Or original citation may have been from forked branch / wrong repo.
- **Recommended curriculum action:**
  - Option A (soft): keep prose "introduced after OVS 1.6 (2011 patch series)", drop specific SHA citation. Acceptable per Rule 14.1 for older history references (5+ year old).
  - Option B (firm): search OVS history for "active_timeout" + "NetFlow" / "IPFIX" 2011 commits to find correct SHA, then update citation.
- **Decision:** Option A — soften citation in S7.C follow-up edit (separate commit). Document here.

### 3.2. `8e53fe8e22` (10-character)

- **Cited in:** `9.24:668` ("commit chuẩn bị `8e53fe8e22` ngày 2015-08-04 trong `lib/ofp-actions.c`")
- **gh api result:** "No commit found for SHA: 8e53fe8e22" (HTTP 422)
- **Verification attempt:** tried `8e53fe8e22`, `8e53fe8e2272` — all 404.
- **Hypothesis:** Likely fabricated SHA (citation written from memory at curriculum authoring time, not verified at write). Master audit Agent C flagged 9.22 + 9.24 SHA citations as "cite SHA from memory (chưa MCP confirm)" — confirmed here.
- **Recommended curriculum action:**
  - Soften citation to prose: "preparation commit August 2015 in lib/ofp-actions.c" (drop specific SHA).
  - Per Rule 14.1: if SHA cannot be verified, must remove or replace with prose.

### 3.3. `cd278bd35e` (10-character)

- **Cited in:** `9.24:668` + `9.24:786` ("commit triển khai đầy đủ action `ct()` `cd278bd35e` đầu Q1/2016")
- **gh api result:** "No commit found for SHA: cd278bd35e" (HTTP 422)
- **Verification attempt:** tried `cd278bd35e` + several 12-char extensions — all 404.
- **Hypothesis:** Same as 8e53fe8e22 — fabricated SHA from memory.
- **Recommended curriculum action:**
  - Soften citation to "Nicira commit Q1/2016 introducing ct() action in lib/ofp-actions.c" (drop specific SHA).
  - Alternatively, search upstream for actual ct() introduction commit — `gh api search/commits?q=Add+conntrack+action+repo:openvswitch/ovs` returned mostly unrelated results; deeper investigation needed.

---

## 4. Curriculum follow-up action

Subsequent commit (S7.C follow-up): soften 3 unverified SHA citations in:
- `sdn-onboard/9.8 - flow-monitoring-sflow-netflow-ipfix.md:214` (5ca1ba9)
- `sdn-onboard/9.24 - ovs-conntrack-stateful-firewall.md:668` (8e53fe8e22, cd278bd35e)
- `sdn-onboard/9.24 - ovs-conntrack-stateful-firewall.md:786` (cd278bd35e)

Pattern: replace `commit \`<sha>\`` with prose date-only reference, OR mark "(SHA prefix unverifiable, cite by date + file path only)".

---

## 5. Reproduction

```bash
for sha in 180ab2fd635e 464bc6f9 0d9dc8e9 5ca1ba9 978427a5 8b7ea2d4 8e53fe8e22 cd278bd35e; do
  result=$(gh api "repos/openvswitch/ovs/commits/$sha" \
    --jq '{author: .commit.author.name, date: .commit.author.date, message: (.commit.message | split("\n")[0])}' 2>&1)
  echo "[$sha] $result"
done
```

Run from any host with `gh` CLI authenticated.

---

## 6. Cross-references

- Plan: [`plans/sdn/v3.9-ovs-block-hotfix.md`](../../plans/sdn/v3.9-ovs-block-hotfix.md) Phase S7.C
- Master audit Agent A §2.3 (180ab2fd635e soft-verify) — now confirmed
- Master audit Agent C §2.6 (9.22 + 9.24 SHA from memory unverified) — confirmed fabricated
- Master audit Agent B §2.3 (9.8 NetFlow/IPFIX SHA) — partially verified (3/4 SHA OK)
- Rule 14.1 commit SHA reference (CLAUDE.md)
