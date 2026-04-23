# Template C — Per-action block cho OpenFlow / OVS extension action

> **Mục đích:** định nghĩa một action (output, drop, ct, learn, resubmit, conjunction, multipath, v.v.) theo pattern chuẩn của `ovs-actions(7)`.
> **Upstream baseline:** man `ovs-actions(7)`, ~40 action, avg 40-60 dòng, core action (ct, learn, resubmit, output) 140-200 dòng.
> **Tối thiểu:** 40 dòng per action (core action thì 80-150).

## Skeleton

```markdown
### Action `<action_name>`

| Attribute | Giá trị |
|---|---|
| **Syntax** | `<name>(<arg1>[, <arg2>[, ...]])` hoặc `<name>:<value>` |
| **Category** | Output / Encap-Decap / Field-Modification / Metadata / Firewall-CT / Control / Miscellaneous |
| **OpenFlow version** | 1.0 / 1.1 / 1.3 / 1.5 / NXM extension / Nicira-only |
| **Prerequisites field** | `<match_field>=<value>` required trong flow match |
| **Semantics** | <2-5 dòng mô tả action làm gì với packet + pipeline state> |
| **Parameters chi tiết** | <list từng arg với type + range + default> |
| **Side effects** | <action thay đổi state ngoài packet: counter, conntrack table, learn-to-table, v.v.> |
| **Conformance** | Đúng spec / Nicira extension / Sử dụng hardware offload / Chỉ userspace datapath |
| **Errors có thể** | `OFPET_BAD_ACTION` / `OFPET_BAD_INSTRUCTION` khi nào |

**Ngữ nghĩa đầy đủ:**

<5-10 dòng giải thích action này ảnh hưởng packet+pipeline ra sao. Có modify packet không? Có clone packet không? Có tiếp tục pipeline sau hay terminate? Có tương tác với action khác trong action_set không?>.

**Ví dụ use case thực tế:**

\`\`\`shell
# Ví dụ 1: <tóm tắt>
$ ovs-ofctl add-flow br0 "<match>,actions=<action với value>"

# Ví dụ 2: <tóm tắt>
$ ovs-ofctl add-flow br0 "<match>,actions=<action variant>"

# Ví dụ 3: <combined với action khác>
$ ovs-ofctl add-flow br0 "<match>,actions=<a1>,<action>,<a2>"
\`\`\`

**Trace output khi action execute:**

\`\`\`
$ ovs-appctl ofproto/trace br0 "<match>"
Flow: <...>
bridge("br0")
-----------
 0. <match>, priority 100
    <action display trong trace>
Final flow: <thay đổi sau action>
Datapath actions: <resulting datapath action>
\`\`\`

**Anatomy của trace line hiển thị action:**

| Thành phần | Ý nghĩa |
|---|---|
| `<parameter>` | <...> |
| `<result>` | <...> |

**Kịch bản bẻ gãy:**

- **Quên prerequisites:** nếu dùng action này mà flow match thiếu `<required field>` → OpenFlow controller nhận `OFPT_ERROR` với code `<...>`.
- **Interaction nguy hiểm:** kết hợp với `<action Y>` trong cùng action_set → <behavior không mong đợi>.
- **Performance cost:** action này có slow path fallback không? Trigger upcall không?

**Liên hệ với action khác:**

- `<related_action>`: tương tự, khác ở `<điểm>`.
- `<opposite_action>`: ngược lại action này.

**Upstream:**
- man `ovs-actions(7)` §`<section>`
- OVS source `ofproto/ofproto-dpif-xlate.c` function `<xlate_X>()`
- OpenFlow spec 1.5 §`<section>` nếu đúng spec
```

## Nhóm action foundation cần cover

**Category 1, Output actions (5 action):** `output`, `group`, `controller` (CONTROLLER reserved port), `local`, `in_port`, `normal`, `flood`, `all`, `table`.

**Category 2, Encap-Decap actions (6 action):** `push_vlan`, `pop_vlan`, `push_mpls`, `pop_mpls`, `push_pbb`, `pop_pbb`, `encap`, `decap`.

**Category 3, Field modification (14 action):** `set_field`, `mod_dl_src`, `mod_dl_dst`, `mod_nw_src`, `mod_nw_dst`, `mod_tp_src`, `mod_tp_dst`, `mod_nw_ttl`, `mod_nw_tos`, `mod_nw_ecn`, `mod_vlan_vid`, `mod_vlan_pcp`, `dec_ttl`, `dec_mpls_ttl`, `copy_ttl_in`, `copy_ttl_out`.

**Category 4, Metadata actions (3 action):** `write_metadata`, `set_tunnel`, `set_tunnel64`.

**Category 5, Firewall/CT actions (3 action):** `ct(commit,zone=N,nat,force,exec=...,alg=...)`, `ct_clear`, `check_pkt_larger`.

**Category 6, Control/pipeline actions (6 action):** `resubmit`, `learn`, `conjunction`, `multipath`, `bundle`, `note`, `clone`.

**Category 7, Misc/enqueue/meter (3 action):** `enqueue`, `set_queue`, `meter`.

Tổng ~40 action. Priority Phase H:

**Tier 1, core foundation (bắt buộc):** `output`, `drop`, `normal`, `flood`, `all`, `controller`, `set_field`, `mod_*`, `dec_ttl`, `ct()`, `resubmit`, `goto_table` (instruction), `learn`, `conjunction`.

**Tier 2, encap+QoS:** `push_vlan`/`pop_vlan`, `push_mpls`/`pop_mpls`, `set_queue`/`enqueue`, `meter`.

**Tier 3, advanced control:** `multipath`, `bundle`, `clone`, `note`.

## Nhóm instruction (OpenFlow 1.1+)

Khác action ở chỗ instruction là **pipeline control** tại table level, còn action là **packet transformation** trong action_set hoặc apply_actions.

Có 6 instruction:
1. `Apply-Actions`: execute ngay, thay đổi packet + pipeline state.
2. `Clear-Actions`: clear action set hiện tại.
3. `Write-Actions`: merge vào action set (execute khi packet exit pipeline).
4. `Write-Metadata`: update metadata match field.
5. `Goto-Table`: chuyển pipeline sang table khác (table number phải lớn hơn current).
6. `Meter`: apply meter trước khi forward.

Template C phải cover cả 6 instruction này (không chỉ action thường).
