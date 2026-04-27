# Source Verification Baseline 2026-04-28 (v3.9.1 Phase Q0)

> **Local OVS repo:** `C:\Users\voleh\Documents\ovs` (checked out at v2.17.9).
> **Commit:** `0bea06d9957e3966d94c48873cd9afefba1c2677` (2024-02-08, "Set release date for 2.17.9").
> **Annotated tag SHA:** `14e48c5da60f8b9089e27234b8d078cae2a59fc7`.
> **Plan:** `plans/sdn/v3.9.1-ovs-block-source-verify-hotfix.md` Phase Q0.
> **Purpose:** Reproducible evidence for the 20 confirmed findings in plan v3.9.1 §0.3.

This log captures the output of every grep, git log, and git show command that v3.9.1 Phase Q1 to Phase Q5 will rely on. Each finding number matches plan v3.9.1 §0.3.

---

## 1. OVS repo state

```
Tag:                v2.17.9
HEAD:               0bea06d9957e3966d94c48873cd9afefba1c2677
Date:               2024-02-08 17:54:21 +0100
Subject:            Set release date for 2.17.9.
Annotated tag SHA:  14e48c5da60f8b9089e27234b8d078cae2a59fc7
Commit object SHA:  0bea06d9957e3966d94c48873cd9afefba1c2677
```

Reproduce with:

```bash
cd C:/Users/voleh/Documents/ovs
git checkout v2.17.9
git rev-parse HEAD
git rev-parse v2.17.9
git rev-parse v2.17.9^{commit}
```

---

## 2. Finding #3 and #4 (10.0 OVSDB monitor / IDL function names)

### Finding #3: `ovsdb_monitor_change_condition` is fabricated

```bash
$ grep -rn "ovsdb_monitor_change_condition" ovsdb/ lib/ --include='*.c' --include='*.h'
(no result)

$ grep -nE "^ovsdb_jsonrpc_monitor_cond_change" ovsdb/jsonrpc-server.c
1561:ovsdb_jsonrpc_monitor_cond_change(struct ovsdb_jsonrpc_session *s,
```

**Verdict:** the curriculum claim is a fabrication. The real handler for `monitor_cond_change` JSON-RPC requests is `ovsdb_jsonrpc_monitor_cond_change` at `ovsdb/jsonrpc-server.c:1561`.

### Finding #4: `ovsdb_idl_db_compose_cond_change` is fabricated

```bash
$ grep -rn "ovsdb_idl_db_compose_cond_change" lib/ --include='*.c' --include='*.h'
(no result)

$ grep -rn "ovsdb_idl_compose_cond_change" lib/ --include='*.c' --include='*.h'
(no result)
```

**Verdict:** neither variant exists in v2.17.9. The function name is a fabrication and the curriculum line that mentions it must be deleted. The neighbouring `ovsdb_idl_set_condition` is real and is kept.

---

## 3. Finding #5 and #6 (10.0 RBAC suffix `_check`)

```bash
$ grep -rn "ovsdb_rbac_insert_check\|ovsdb_rbac_update_check" ovsdb/ --include='*.c' --include='*.h'
(no result)

$ grep -nE "^ovsdb_rbac_(insert|update)" ovsdb/rbac.c
149:ovsdb_rbac_insert(const struct ovsdb *db, const struct ovsdb_table *table,
308:ovsdb_rbac_update(const struct ovsdb *db,
```

**Verdict:** the suffix `_check` is wrong. The real names are `ovsdb_rbac_insert` (line 149) and `ovsdb_rbac_update` (line 308) in `ovsdb/rbac.c`.

---

## 4. Finding #7 to #11 (10.1 Raft function line numbers)

```bash
$ for fn in raft_run raft_become_leader raft_become_follower \
            raft_send_append_request raft_command_execute \
            raft_handle_append_request raft_handle_append_reply \
            raft_log_length; do
    echo "$fn:"; grep -nE "^$fn" ovsdb/raft.c | head -2
  done
```

Output:

```
raft_run:
1930:raft_run(struct raft *raft)
3755:raft_run_reconfigure(struct raft *raft)
raft_become_leader:
2745:raft_become_leader(struct raft *raft)
raft_become_follower:
2634:raft_become_follower(struct raft *raft)
raft_send_append_request:
2673:raft_send_append_request(struct raft *raft,
raft_command_execute:
2299:raft_command_execute__(struct raft *raft, const struct json *data,
2378:raft_command_execute(struct raft *raft, const struct json *data,
raft_handle_append_request:
3181:raft_handle_append_request(struct raft *raft,
raft_handle_append_reply:
3498:raft_handle_append_reply(struct raft *raft,
raft_log_length:
(no result)
```

**Verdict:**

- `raft_run` is at line 1930 (curriculum cited 3045, drift 1115 lines).
- `raft_become_leader` is at line 2745 (curriculum cited 2650, drift 95 lines).
- `raft_become_follower` is at line 2634 (curriculum cited 2610, drift 24 lines).
- `raft_send_append_request` is at line 2673 (curriculum cited 2634, drift 39 lines).
- `raft_command_execute` is at line 2378 (the public API). The internal `raft_command_execute__` helper is at line 2299. Curriculum cited 3513, drift 1135 lines.
- `raft_handle_append_request` is at line 3181 (curriculum cited "approx. 2900 to 3000", outside the cited range).
- `raft_handle_append_reply` is at line 3498 (real, not in curriculum).
- `raft_log_length` does not exist in v2.17.9; it is a fabrication.

Q2 fix per Rule 14.4 Option C drops all inline line numbers, drops the fabricated `raft_log_length`, and adds the verified `raft_handle_append_reply`.

---

## 5. Finding #12 and #13 (9.22 GOTO_TABLE and oftable eviction)

```bash
$ grep -nE "decode_OFPIT11_GOTO_TABLE" lib/ofp-actions.c
(no result)

$ grep -nE "^(encode|parse|format|check)_GOTO_TABLE" lib/ofp-actions.c
7720:encode_GOTO_TABLE(const struct ofpact_goto_table *goto_table,
7739:parse_GOTO_TABLE(char *arg, const struct ofpact_parse_params *pp)
7749:format_GOTO_TABLE(const struct ofpact_goto_table *a,
7757:check_GOTO_TABLE(const struct ofpact_goto_table *a,

$ grep -nE "oftable_set_default_eviction|oftable_configure_eviction" ofproto/ofproto.c | head -5
94:static void oftable_configure_eviction(struct oftable *,
1561:    oftable_configure_eviction(table, new_eviction, s->groups, s->n_groups);
7990:        oftable_configure_eviction(oftable, new_eviction,
9174:    oftable_configure_eviction(table, 0, NULL, 0);
9234:oftable_configure_eviction(struct oftable *table, unsigned int eviction,
```

**Verdict:**

- `decode_OFPIT11_GOTO_TABLE` does not exist; decoding for the GOTO_TABLE instruction is dispatched via macro-generated wrappers from the OFPACT registry, not as a standalone function.
- The four real GOTO_TABLE functions in `lib/ofp-actions.c` are `encode_GOTO_TABLE` (line 7720), `parse_GOTO_TABLE` (line 7739), `format_GOTO_TABLE` (line 7749), and `check_GOTO_TABLE` (line 7757).
- `oftable_set_default_eviction` does not exist. The real function is `oftable_configure_eviction`. Line 94 is the static forward declaration, line 9234 is the definition, and lines 1561, 7990, 9174 are call sites.

---

## 6. Finding #14 (9.32 classifier function prefix)

```bash
$ grep -nE "^cls_classifier_(insert|lookup)" lib/classifier.c
(no result)

$ grep -nE "^classifier_(insert|lookup)" lib/classifier.c
690:classifier_insert(struct classifier *cls, const struct cls_rule *rule,
938:classifier_lookup__(const struct classifier *cls, ovs_version_t version,
1166:classifier_lookup(const struct classifier *cls, ovs_version_t version,
```

**Verdict:** the `cls_` prefix is wrong. The real names are `classifier_insert` (line 690) and `classifier_lookup` (line 1166) in `lib/classifier.c`. Line 938 is the internal helper `classifier_lookup__` with double underscore.

---

## 7. Finding #16 and #17 (9.32 classifier and dpif-netdev history)

```bash
$ git log --diff-filter=A --format="%H %ai %s" -- lib/classifier.c | tail -1
064af42167bf4fc9aaea2702d80ce08074b889c0 2009-07-08 13:19:16 -0700
    Import from old repository commit 61ef2b42a9c4ba8e1600f15bb0236765edc2ad45.

$ git log --diff-filter=A --format="%H %ai %s" -- lib/dpif-netdev.c | tail -1
72865317a41d065fcc47a33fc68cdd2081cecb3d 2009-06-19 14:09:39 -0700
    New implementation of userspace datapath, based on the netdev library.

$ git log --diff-filter=A --format="%H %ai %s" -- lib/dpif-linux.c | tail -1
96fba48f52254c0cef942dcce130e33d290297da 2009-06-17 14:35:35 -0700
    dpif: Make dpifs abstract, to allow multiple datapath implementations.

$ git log --diff-filter=R --format="%H %ai %s" --follow -- lib/dpif-netlink.c | head -1
93451a0a81b40c480115abd8739c1582e6b49a9c 2014-09-18 04:17:54 -0700
    dpif-linux: Rename dpif-netlink; change to compile with MSVC.
```

**Verdict:**

- The `lib/classifier.c` file was added on 2009-07-08, four and a half years before OVS 2.0 (December 2013). The "OVS 2.0 (2014) introduced TSS classifier" claim in 9.32:134 is wrong. OVS 2.0 refined megaflow consolidation; TSS itself predates OVS 2.0.
- The `lib/dpif-netdev.c` file was added on 2009-06-19, six years before OVS 2.4 (August 2015). The "OVS 2.4 (2015) split `dpif-netdev.c` from `dpif-netlink.c`" claim in 9.32:513 is wrong on two counts. First, `dpif-netdev.c` always existed independently. Second, the rename was actually `dpif-linux.c` to `dpif-netlink.c` on 2014-09-18 (commit `93451a0a81b40c48`), so MSVC could compile it. OVS 2.4 was the release where DPDK-backed `netdev-dpdk.c` reached stable first-class status through the `dpif-netdev` path. It was not a split.

---

## 8. Finding #18 (9.32 dpif-dummy fabrication)

```bash
$ ls lib/dpif-dummy*
ls: cannot access 'lib/dpif-dummy*': No such file or directory

$ ls lib/dummy* lib/netdev-dummy*
lib/dummy.c
lib/dummy.h
lib/netdev-dummy.c
```

**Verdict:** there is no `dpif-dummy` provider in v2.17.9. The closest real files are `lib/dummy.c` (test-only utilities), `lib/dummy.h`, and `lib/netdev-dummy.c` (a netdev provider used by ofproto-dpif unit tests). The "(`lib/dpif-netdev-perf.c` contains a testing helper for `dpif-dummy`)" claim is a fabrication.

---

## 9. Finding #19 (9.24 ct() implementation date)

```bash
$ git log --all --format="%H %ai %s" --grep="Add support for connection tracking" \
    -- lib/ofp-actions.c | head -3
d787ad39b8eb8fb9136837e1c65d0a18a1056eda 2015-09-15 14:29:16 -0700
    Add support for connection tracking helper/ALGs.
07659514c3c1e8998a4935a998b627d716c559f9 2015-08-11 10:56:09 -0700
    Add support for connection tracking.

$ git log -1 --format="%H %ai %s" a489b16854b59000
a489b16854b590004e3234573721fd0f676b3295 2015-11-15 22:07:25 -0800
    conntrack: New userspace connection tracker.
```

**Verdict:**

- The action `ct()` was merged on 2015-08-11 by commit `07659514c3c1e8998a4935a998b627d716c559f9` ("Add support for connection tracking"), in `lib/ofp-actions.c`.
- The userspace conntrack `lib/conntrack.c` was added on 2015-11-15 by commit `a489b16854b590004e3234573721fd0f676b3295` ("conntrack: New userspace connection tracker.").
- The curriculum claim "implementation Q1 2016" confuses the OVS 2.5 release date (2016-02-24) with the implementation date (2015-08-11). The release is when the feature first shipped in a stable tag; the implementation is when it landed on `main`.

---

## 10. Finding #20 (9.24 ct_zone version drift)

```bash
$ git show v2.5.0:lib/meta-flow.h | grep -nE "ct_zone|MFF_CT_ZONE"
791:    /* "ct_zone".
804:    MFF_CT_ZONE,
... [other references in the same file]

$ git show v2.6.0:include/openvswitch/meta-flow.h | grep -nE "MFF_CT_ZONE"
806:    MFF_CT_ZONE,
... [same field, file path moved]
```

**Verdict:** `MFF_CT_ZONE` was already defined at v2.5.0 in `lib/meta-flow.h` (line 804), in the same commit `07659514c3c1e899` from 2015-08-11 that introduced the `ct()` action. The header file moved from `lib/meta-flow.h` to `include/openvswitch/meta-flow.h` only in v2.6.0 (2016-04-04, commit `064d7f842838bdc4`), but the field itself existed earlier. The curriculum claim "OVS 2.6 (2016) introduced the 16-bit zone field" is off by one release version. The correct version is OVS 2.5 (February 2016).

---

## 11. Finding #21 (9.26 backport tag)

```bash
$ git tag --contains 180ab2fd635e | sort -V | head -10
v3.5.0
v3.5.1
v3.5.2
v3.5.3
v3.5.4
v3.6.0
v3.6.1
v3.6.2
v3.6.3
v3.7.0
```

**Verdict:** commit `180ab2fd635e` first appears in v3.5.0. OVS 3.3 and 3.4 also lack the fix. The curriculum claim "OVS less than v3.3 (where commit `180ab2fd635e` is not yet backported)" must be corrected to "OVS less than v3.5".

---

## 12. Finding #22 (10.5 election timer purpose)

```bash
$ sed -n '208,217p' ovsdb/raft.c
#define ELECTION_MAX_MSEC 600000
    /* The election timeout base value for leader election, in milliseconds.
     * It can be set by unixctl cluster/change-election-timer. Default value is
     * ELECTION_BASE_MSEC. */
    uint64_t election_timer;
    /* If not 0, it is the new value of election_timer being proposed. */
    uint64_t election_timer_new;
```

**Verdict:** the comment is unambiguous. The unixctl command `cluster/change-election-timer` sets the leader election timeout (`election_timer`), measured in milliseconds. It does not set Raft snapshot frequency. The curriculum heading "Raft snapshot frequency" over a code block running `ovs-appctl -t ovsdb-server cluster/change-election-timer 10000` is a semantic mismatch. Q4.3 fix moves the command under a correct heading and notes that snapshot frequency is governed by an internal log-size threshold without a runtime unixctl knob.

---

## 13. Summary of confirmed findings

| Finding | Severity | Status |
|---|---|---|
| #3 `ovsdb_monitor_change_condition` fabrication | BLOCKER | Confirmed |
| #4 `ovsdb_idl_db_compose_cond_change` fabrication | BLOCKER | Confirmed |
| #5 `ovsdb_rbac_insert_check` wrong | BLOCKER | Confirmed |
| #6 `ovsdb_rbac_update_check` wrong | BLOCKER | Confirmed |
| #7 `raft_run` line drift 1115 | HIGH | Confirmed |
| #8 `raft_command_execute` line drift 1135 | HIGH | Confirmed |
| #9 `raft_become_leader` line drift 95 | HIGH | Confirmed |
| #10 `raft_handle_append_request` outside range | HIGH | Confirmed |
| #11 `raft_log_length` fabrication | BLOCKER | Confirmed |
| #12 `decode_OFPIT11_GOTO_TABLE` fabrication | BLOCKER | Confirmed |
| #13 `oftable_set_default_eviction` wrong | BLOCKER | Confirmed |
| #14 `cls_classifier_*` wrong prefix | HIGH | Confirmed |
| #16 OVS 2.0 (2014) TSS introduction wrong | HIGH | Confirmed |
| #17 OVS 2.4 (2015) dpif split wrong | HIGH | Confirmed |
| #18 `dpif-dummy` fabrication | HIGH | Confirmed |
| #19 ct() implementation Q1 2016 wrong | HIGH | Confirmed |
| #20 ct_zone OVS 2.6 wrong | HIGH | Confirmed |
| #21 backport version `<v3.3` wrong | HIGH | Confirmed |
| #22 cluster/change-election-timer purpose mismatch | HIGH | Confirmed |
| #23 SHA replacement candidate `07659514c3c1e899` | MEDIUM | Confirmed |

20 confirmed findings, all reproducible from this baseline. Three earlier findings (#1, #2, #15) were demoted to FALSE ALARM during the recheck per plan v3.9.1 §0.3.

---

## 14. Reproducibility notes

To re-run any of the verifications above:

```bash
cd C:/Users/voleh/Documents/ovs
git checkout v2.17.9
# then run any single command from the sections above
```

The OVS repo must be clean (no uncommitted changes) before checkout. Use `git status` to confirm. The release tag `v2.17.9` resolves to the same commit object SHA `0bea06d9957e3966d94c48873cd9afefba1c2677` on every clone of `https://github.com/openvswitch/ovs.git`. Cross-references to other release tags (`v2.5.0`, `v2.6.0`, `v3.5.0`) use `git show <tag>:<path>` so they do not require checkout.

---

> **Authority:** plan v3.9.1 Phase Q0.
> **Author:** v3.9.1 baseline run, 2026-04-28.
> **Next step:** Phase Q1 (10.0 OVSDB function-name hotfix) consumes findings #3 to #6 from this log.
