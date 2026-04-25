# OVS, OpenFlow & OVN — Keyword Reference

> **Purpose.** Backbone reference for engineer training on Open vSwitch (OVS), OpenFlow (OF), and Open Virtual Network (OVN). Every entry is classified along five axes — **Bucket | Context | Purpose | Activity | Mechanism** — and is anchored to an authoritative source: openvswitch.org / ovn.org / man7.org man pages, ONF OpenFlow specifications, vendor documentation (Red Hat, Canonical, Mirantis, SUSE, kolla-ansible), or named engineer write-ups.
>
> **Use it as.** (1) A glossary when reading OVS/OVN logs, (2) a CLI cheat-sheet during incident response, (3) a depth-first reading list when onboarding new operators.
>
> **Coverage discipline.** Where an option, default, or mechanism could not be tied to one of the whitelisted sources, it is omitted rather than guessed. Where official sources disagree across OpenFlow versions, the disagreement is flagged inline with version tags.

---

## 1. Open vSwitch (OVS)

### 1.1 Architecture & daemons

- **ovs-vswitchd** — Bucket: OVS | Context: long-running userspace daemon | Purpose: implements the switch — owns the OpenFlow pipeline, datapath flow programming, and bridge configuration | Activity: forwarding, learning, OpenFlow rule install, datapath upcall handling, OVSDB monitoring | Mechanism: subscribes to OVSDB via JSON-RPC for `Bridge`/`Port`/`Interface`/`Controller`/`Flow_Table` rows; manages handler threads (upcalls) and revalidator threads (flow validation); pushes flows into the kernel/userspace/DPDK datapath via `dpif`.
  - Example: `ovs-appctl -t ovs-vswitchd list-commands` enumerates runtime appctl commands.
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **ovsdb-server** — Bucket: OVS | Context: long-running daemon serving the configuration database via JSON-RPC | Purpose: persistent, transactional configuration store consumed by `ovs-vswitchd`, `ovn-northd`, `ovn-controller`, `ovs-vsctl`, and external orchestrators | Activity: schema enforcement, transaction commit, monitor/notify push to clients, RAFT log append (clustered) | Mechanism: Unix-domain socket (default `/run/openvswitch/db.sock`) plus optional `tcp:` / `ssl:` remotes; supports standalone, active-backup, and RAFT cluster modes.
  - Example: `ovsdb-server /etc/openvswitch/conf.db --remote=punix:/var/run/openvswitch/db.sock --pidfile --detach`
  - Source: https://man7.org/linux/man-pages/man1/ovsdb-server.1.html

- **ovs-monitor-ipsec** — Bucket: OVS | Context: Python helper daemon | Purpose: programs strongSwan/Libreswan to bring up IPsec on tunnel ports OVS exposes | Activity: tunnel-port lifecycle (add/delete), key/cert rollover | Mechanism: reads `Interface.options:remote_ip`, `:psk`, `:cert` from OVSDB and renders IKE config files.
  - Example: started by the system unit `openvswitch-ipsec.service`; manual launch `ovs-monitor-ipsec --pidfile`.
  - Source: https://docs.openvswitch.org/en/latest/howto/ipsec/

- **ovs-tcpdump** — Bucket: OVS | Context: thin wrapper around tcpdump that creates a transient mirror | Purpose: capture traffic on an OVS port without re-cabling | Activity: provisioning a temporary `Mirror` row, spawning `tcpdump`, tearing the mirror down on exit | Mechanism: writes mirror config into OVSDB, pipes the mirrored packets via a tap to tcpdump.
  - Example: `ovs-tcpdump -i tap0 -n 'tcp port 80'`
  - Source: https://man7.org/linux/man-pages/man8/ovs-tcpdump.8.html

- **Control socket / pidfile convention** — Bucket: OVS | Context: every OVS daemon | Purpose: lets `ovs-appctl` find the process at runtime without configuration | Activity: daemon writes `<rundir>/<program>.pid`; appctl listens on `<rundir>/<program>.<pid>.ctl` | Mechanism: pidfile + Unix-domain control socket; `--target` to `ovs-appctl` may be a path or a pidfile basename.
  - Example: `ovs-appctl -t /var/run/openvswitch/ovs-vswitchd.<pid>.ctl coverage/show`
  - Source: https://man7.org/linux/man-pages/man8/ovs-appctl.8.html

### 1.2 Datapath & forwarding internals

- **openvswitch.ko (kernel datapath)** — Bucket: OVS | Context: in-tree Linux kernel module | Purpose: fast-path packet matching, action execution, tunneling | Activity: per-packet flow lookup, on miss generates an upcall to userspace | Mechanism: `dp_flow` cache keyed by an exact match of all extracted fields plus a per-flow mask; supports kernel tunneling (Geneve, VXLAN, GRE, ERSPAN).
  - Example: `lsmod | grep openvswitch` then `ovs-vsctl get Bridge br-int datapath_type` (empty / `system` ⇒ kernel datapath).
  - Source: https://docs.openvswitch.org/en/latest/intro/what-is-ovs/

- **netdev / userspace datapath** — Bucket: OVS | Context: alternative datapath implementation in `ovs-vswitchd` | Purpose: skip the kernel module — required for DPDK and for portability to non-Linux hosts | Activity: PMD threads poll NIC queues; flow lookup happens entirely in userspace | Mechanism: bridges are created with `datapath_type=netdev`; with DPDK, ports are `type=dpdk`/`dpdkvhostuser`.
  - Example: `ovs-vsctl add-br br0 -- set Bridge br0 datapath_type=netdev`
  - Source: https://docs.openvswitch.org/en/latest/intro/install/dpdk/

- **DPDK datapath** — Bucket: OVS | Context: userspace datapath with the DPDK poll-mode driver framework | Purpose: line-rate forwarding on commodity NICs without kernel involvement | Activity: PMD threads pinned to CPU cores poll RX queues; vhost-user ports back guests | Mechanism: enable globally with `other_config:dpdk-init=true`, dedicate cores via `pmd-cpu-mask`, allocate hugepages.
  - Example: `ovs-vsctl set Open_vSwitch . other_config:dpdk-init=true other_config:pmd-cpu-mask=0x6`
  - Source: https://docs.openvswitch.org/en/latest/howto/dpdk/

- **ofproto / dpif layering** — Bucket: OVS | Context: internal architecture of `ovs-vswitchd` | Purpose: separate OpenFlow semantics (`ofproto`) from the datapath interface (`dpif`) so the same daemon drives kernel, userspace, and DPDK datapaths | Activity: `ofproto` translates OpenFlow flow tables into `dpif` flow installations | Mechanism: `dpif/show` exposes the dpif-level state, `ofproto/trace` traces the ofproto-level pipeline.
  - Example: `ovs-appctl dpif/show` and `ovs-appctl ofproto/trace br0 in_port=1,...`
  - Source: https://docs.openvswitch.org/en/latest/topics/datapath/

- **Megaflow** — Bucket: OVS | Context: kernel/userspace datapath flow cache | Purpose: cache one wildcarded entry per equivalence class of packets, instead of one per microflow | Activity: on miss, userspace computes the smallest mask sufficient for the OpenFlow lookup and installs that megaflow | Mechanism: each megaflow carries the original mask plus the resolved actions; subsequent matching packets bypass userspace.
  - Example: `ovs-appctl dpctl/dump-flows` shows megaflow rows including `recirc_id`, `in_port`, masked headers, and `actions:`.
  - Source: https://docs.openvswitch.org/en/latest/faq/openflow/

- **Microflow / EMC (Exact-Match Cache)** — Bucket: OVS | Context: per-PMD first-tier cache in the userspace/DPDK datapath | Purpose: O(1) lookup for hot flows before falling back to the megaflow classifier | Activity: each PMD checks EMC, then SMC, then megaflows | Mechanism: small fixed-size hash table keyed by an exact 5-tuple/extended hash.
  - Example: hits visible in `ovs-appctl dpif-netdev/pmd-stats-show`.
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **SMC (Signature Match Cache)** — Bucket: OVS | Context: optional second-tier cache between EMC and megaflow classifier | Purpose: catch flows that miss EMC but share signatures with the megaflow set | Activity: PMD-local signature hash lookup | Mechanism: enabled via `other_config:smc-enable=true`.
  - Example: `ovs-vsctl set Open_vSwitch . other_config:smc-enable=true`
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **Upcall** — Bucket: OVS | Context: kernel→userspace event when no datapath flow matches | Purpose: deliver the unmatched packet to `ovs-vswitchd` so it can consult the OpenFlow tables | Activity: handler threads dequeue upcalls, run the OpenFlow pipeline, install a megaflow, optionally re-inject the packet | Mechanism: netlink (`NLMSG`/`OVS_PACKET_CMD_MISS`) for kernel datapath; channel queues for netdev.
  - Example: `ovs-appctl upcall/show` reports per-handler queue depths and miss/lost counters.
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **Handler thread** — Bucket: OVS | Context: thread inside `ovs-vswitchd` | Purpose: process upcalls and install datapath flows | Activity: parse upcall payload, run xlate, write back via dpif | Mechanism: count tunable via `other_config:n-handler-threads`.
  - Example: `ovs-vsctl set Open_vSwitch . other_config:n-handler-threads=8`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **Revalidator thread** — Bucket: OVS | Context: thread inside `ovs-vswitchd` | Purpose: re-validate datapath flows after OpenFlow rule changes; expire idle flows | Activity: dump kernel flows, recompute their actions, delete or update | Mechanism: count tunable via `other_config:n-revalidator-threads`; revalidation pass is gated by max-idle and max-revalidator timers.
  - Example: `ovs-vsctl set Open_vSwitch . other_config:n-revalidator-threads=4`
  - Source: https://developers.redhat.com/articles/2022/10/19/open-vswitch-revalidator-process-explained

- **Recirculation (`recirc_id`)** — Bucket: OVS | Context: pipeline construct | Purpose: re-enter the pipeline after header rewrite (e.g. tunnel decap, MPLS, conntrack) | Activity: actions emit `recirc()`; the kernel feeds the packet back into the lookup with a non-zero `recirc_id` | Mechanism: `recirc_id` becomes a match field; megaflows are keyed including it.
  - Example: `ovs-appctl dpctl/dump-flows | grep 'recirc_id(0x'`
  - Source: https://docs.openvswitch.org/en/latest/faq/openflow/

- **Connection tracking (`ct`)** — Bucket: OVS | Context: kernel/userspace stateful firewall | Purpose: classify packets as `new`/`est`/`rel`/`inv`/`rpl`/`trk`; perform NAT; commit per-flow state | Activity: `ct(commit, zone=…, nat(...), alg=…)` action; `ct_state` match consumes the result after recirculation | Mechanism: kernel datapath uses Linux nf_conntrack; userspace datapath has its own implementation.
  - Example: `actions=ct(commit,zone=5,nat(src=10.0.0.1)),resubmit(,42)`
  - Source: https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/

- **`ct_state`** — Bucket: OVS | Context: NXM extension match field | Purpose: bitmask of conntrack state flags | Activity: read after `ct()` action; commonly matched as `+new+trk`, `+est+trk`, `+rel+trk`, `+inv+trk` | Mechanism: states `NEW`, `EST`, `REL`, `INV`, `RPL`, `TRK`, `SNAT`, `DNAT`.
  - Example: `table=42,ct_state=+new+trk,ip,actions=ct(commit,zone=5),output:LOCAL`
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

- **`ct_zone`** — Bucket: OVS | Context: 16-bit conntrack namespace | Purpose: isolate conntrack state per tenant or per logical router | Activity: passed to the `ct()` action; matched after recirc | Mechanism: each zone has its own table; OVN allocates zones per logical port.
  - Example: `ct(zone=NXM_NX_REG13[0..15],commit)`
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

- **`ct_mark`** — Bucket: OVS | Context: 32-bit per-connection tag | Purpose: stamp a connection so subsequent packets match without re-deriving | Activity: written via `ct(commit,exec(set_field:0x1->ct_mark))`; matched directly in flows | Mechanism: persisted in the kernel conntrack entry.
  - Example: `actions=ct(commit,exec(load:0x1->NXM_NX_CT_MARK[]))`
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

- **`ct_label`** — Bucket: OVS | Context: 128-bit per-connection label | Purpose: extra opaque metadata for stateful policy | Activity: read/written under `ct(...)` exec block | Mechanism: persisted alongside `ct_mark`.
  - Example: `actions=ct(commit,exec(set_field:0x1/0x1->ct_label))`
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

- **ALG (FTP/TFTP/SIP)** — Bucket: OVS | Context: conntrack helper | Purpose: track expected child connections (e.g. FTP data channel) and rewrite embedded addresses under NAT | Activity: enabled with `ct(alg=ftp,...)`, `ct(alg=tftp,...)` | Mechanism: helper parses the L7 control payload to spawn `RELATED` expectations.
  - Example: `actions=ct(commit,zone=1,alg=ftp)`
  - Source: https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/

- **NAT** — Bucket: OVS | Context: action sub-clause of `ct()` | Purpose: stateful source/destination address+port translation | Activity: `nat(src=...)`, `nat(dst=...)`, `nat(src=10.0.0.1:1024-2048,random)` | Mechanism: NAT mapping is established on commit and reused for the rest of the connection.
  - Example: `actions=ct(commit,nat(src=192.0.2.1))`
  - Source: https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/

- **`learn` action** — Bucket: OVS | Context: NXM extension action | Purpose: install a new flow at runtime triggered by a packet (used for L2 learning, ephemeral state) | Activity: action template references current packet fields to build the new flow | Mechanism: learned flow installed via the same path as ofctl `add-flow`.
  - Example: `actions=learn(table=20,priority=10,NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],load:NXM_OF_IN_PORT[]->NXM_NX_REG0[0..15])`
  - Source: https://man7.org/linux/man-pages/man7/ovs-actions.7.html

- **Megaflow wildcarding** — Bucket: OVS | Context: optimisation in the userspace classifier | Purpose: keep the kernel flow count low by masking out fields the OpenFlow lookup did not actually examine | Activity: `xlate` records "fields touched"; the unmasked fields are wildcarded in the resulting megaflow | Mechanism: poorly-written OpenFlow rules (or buggy actions) reduce wildcarding and explode the kernel flow count.
  - Example: with a single L2 forwarding rule on `in_port=1`, the kernel sees one megaflow `in_port(1),...` rather than one per src/dst pair.
  - Source: https://docs.openvswitch.org/en/latest/faq/openflow/

- **UFID (Unique Flow ID)** — Bucket: OVS | Context: 128-bit identifier in the dpif | Purpose: address a kernel flow without re-sending its entire match | Activity: dpif emits a UFID on flow install; later operations reference it | Mechanism: visible in `ovs-appctl dpctl/dump-flows --names ufid:`.
  - Example: `ovs-appctl dpctl/dump-flows -m system@ovs-system | grep ufid:`
  - Source: https://man7.org/linux/man-pages/man8/ovs-dpctl.8.html

- **Interface type: `internal`** — Bucket: OVS | Context: `Interface.type` in OVSDB | Purpose: create a kernel network device (tuntap) owned entirely by OVS — used as a bridge's local management interface, a loopback for OVSDB traffic, or a router gateway port | Activity: provisioning, management connectivity, in-band control path | Mechanism: OVS creates a kernel netdev of type `tun`; the bridge's own MAC is assigned from the OVS-generated or user-supplied `mac` option; traffic sent to the port's `ofport` enters the OVS pipeline as a normal packet.
  - Example: `ovs-vsctl add-port br-int mgmt0 -- set Interface mgmt0 type=internal && ip addr add 10.0.0.1/24 dev mgmt0 && ip link set mgmt0 up`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **Interface type: `patch`** — Bucket: OVS | Context: `Interface.type` in OVSDB | Purpose: create a virtual wire between two OVS bridges without involving the kernel networking stack — the canonical way to connect `br-int` to `br-ex` or `br-provider` in OVN deployments | Activity: provisioning, bridge chaining, inter-bridge forwarding | Mechanism: patch ports always come in pairs (each peer references the other via `options:peer=NAME`); a packet emitted to one port appears instantly on the peer's `ofport` in the partner bridge; no kernel `veth` or `net_device` is created.
  - Example: `ovs-vsctl -- add-port br-int int-to-ex -- set Interface int-to-ex type=patch options:peer=ex-to-int -- add-port br-ex ex-to-int -- set Interface ex-to-int type=patch options:peer=int-to-ex`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **VLAN bridge modes (`Port.vlan_mode`)** — Bucket: OVS | Context: `Port.vlan_mode` column in OVSDB | Purpose: control how 802.1Q frames are admitted and sent on a port | Activity: provisioning, VLAN segmentation | Mechanism: four values are supported:
  - `access` — port belongs to a single VLAN (`tag` column); incoming untagged frames are classified into that VLAN; outgoing frames are stripped of the tag. Incoming frames already tagged are **dropped** (default for VM-facing ports in OVN).
  - `trunk` — port carries traffic for the VLANs listed in `trunks` (or all VLANs when `trunks=[]`); frames must arrive tagged and leave tagged.
  - `native-tagged` — like `trunk`, but frames belonging to `tag` VLAN may arrive untagged and will be emitted tagged.
  - `native-untagged` — like `native-tagged` except frames for `tag` VLAN are emitted **untagged**; useful for uplinks that must interoperate with access-mode switches.
  - Example: `ovs-vsctl set Port eth0 vlan_mode=trunk trunks=[100,200,300]`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **Bond mode (`Port.bond_mode`)** — Bucket: OVS | Context: `Port.bond_mode` column for bonded ports | Purpose: select link-aggregation algorithm | Activity: provisioning, high availability, bandwidth aggregation | Mechanism:
  - `active-backup` — one slave forwards at a time; on link failure OVS switches to the next live slave (detected via LACPDU or carrier). No LACP required at the switch.
  - `balance-slb` (Source-Load-Balance) — distributes flows by source MAC + VLAN across slaves; no switch-side LACP required; slave selection changes when a link fails.
  - `balance-tcp` — distributes flows by 5-tuple (requires LACP mode 802.3ad with the upstream switch); provides the most granular load distribution and is the recommended mode for performance-sensitive deployments.
  - Example: `ovs-vsctl add-bond br0 bond0 eth1 eth2 -- set Port bond0 bond_mode=balance-tcp lacp=active`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html; https://docs.openvswitch.org/en/latest/topics/bonding/

### 1.3 Configuration database (OVSDB)

- **OVSDB schema** — Bucket: OVS | Context: JSON file describing tables, columns, types, indexes, and root tables | Purpose: define the data model for `ovs-vswitchd`, the VTEP database, OVN_Northbound, and OVN_Southbound | Activity: each daemon embeds a schema; `ovsdb-server` enforces it | Mechanism: schema version `x.y.z` is stored inside the database file; `ovsdb-tool convert` migrates.
  - Example: `/usr/share/openvswitch/vswitch.ovsschema`
  - Source: https://man7.org/linux/man-pages/man1/ovsdb-tool.1.html

- **Transactional model** — Bucket: OVS | Context: JSON-RPC `transact` operation | Purpose: ACID multi-row, multi-table updates | Activity: `ovs-vsctl` and `ovn-nbctl` build a single transaction per CLI invocation | Mechanism: server validates schema and constraints, then commits atomically.
  - Example: `ovs-vsctl -- add-br br0 -- add-port br0 eth0` is one transaction.
  - Source: https://docs.openvswitch.org/en/latest/ref/ovsdb-server.7/

- **RAFT clustering** — Bucket: OVS | Context: built-in cluster mode for `ovsdb-server` | Purpose: HA and read scale-out for OVSDB | Activity: leader handles writes; followers serve reads (subject to leader-only client option) | Mechanism: bootstrap with `ovsdb-tool create-cluster`; join with `join-cluster`.
  - Example: `ovsdb-tool create-cluster /etc/openvswitch/ovnsb_db.db OVN_Southbound tcp:10.0.0.1:6644`
  - Source: https://docs.ovn.org/en/latest/topics/high-availability.html

- **Active-backup replication** — Bucket: OVS | Context: legacy replication mode | Purpose: simple primary/standby HA without RAFT | Activity: backup server runs with `--sync-from=tcp:<primary>:<port>` | Mechanism: no automatic failover — promotion is operator-driven via `ovs-appctl -t ovsdb-server ovsdb-server/disconnect-active-ovsdb-server`.
  - Source: https://man7.org/linux/man-pages/man1/ovsdb-server.1.html

- **JSON-RPC monitor** — Bucket: OVS | Context: server→client push protocol | Purpose: every OVS/OVN daemon receives database change notifications instead of polling | Activity: client issues `monitor`/`monitor_cond` requests; server pushes `update`/`update2`/`update3` notifications | Mechanism: condition expressions reduce notification volume (`monitor_cond_change`).
  - Example: `ovsdb-client monitor unix:/var/run/openvswitch/db.sock Open_vSwitch Bridge`
  - Source: https://man7.org/linux/man-pages/man1/ovsdb-client.1.html

- **`Open_vSwitch` table (root)** — Bucket: OVS | Context: configuration database root table | Purpose: holds global toggles (`other_config`, `external_ids`), bridges, manager refs, SSL config, datapath info | Activity: queried by `ovs-vswitchd` on startup; updated by orchestration | Mechanism: single row referenced as `.`.
  - Example: `ovs-vsctl get Open_vSwitch . other_config`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Bridge` table** — Bucket: OVS | Context: per-bridge state | Purpose: defines an L2 switch instance with a datapath | Activity: lists controllers, mirrors, ports, OpenFlow protocol set, fail mode, datapath type | Mechanism: `datapath_type` column selects backend (`system`, `netdev`).
  - Example: `ovs-vsctl set Bridge br-int protocols=OpenFlow13,OpenFlow15`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Port` table** — Bucket: OVS | Context: per-port row referenced from a `Bridge` | Purpose: VLAN access/trunk config, bonding parameters, QoS attachment | Activity: bonded ports list multiple `Interface` rows | Mechanism: `tag`, `trunks`, `bond_mode`, `lacp`, `bond_active_slave`.
  - Example: `ovs-vsctl set Port eth1 tag=100`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Interface` table** — Bucket: OVS | Context: per-interface row | Purpose: low-level NIC/tunnel/patch state — type, options, `ofport`, statistics, MTU | Activity: tunnel ports use `type=geneve`/`vxlan`/`gre`/`stt` plus `options:remote_ip`, `key`, `dst_port` | Mechanism: `error` column surfaces creation failures.
  - Example: `ovs-vsctl get Interface tap0 ofport statistics`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Controller` table** — Bucket: OVS | Context: OpenFlow controller endpoint per bridge | Purpose: tcp/ssl/unix target for the OpenFlow channel; in-band/out-of-band; rate limit | Activity: `is_connected` reflects current state | Mechanism: `connection_mode=in-band` allows control over the bridge's own ports.
  - Example: `ovs-vsctl set-controller br-int tcp:127.0.0.1:6653`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Manager` table** — Bucket: OVS | Context: OVSDB management endpoint | Purpose: expose the local DB to remote orchestration | Activity: `ptcp:` / `pssl:` / `punix:` listeners | Mechanism: independent of OpenFlow `Controller`.
  - Example: `ovs-vsctl set-manager ptcp:6640:127.0.0.1`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Mirror` table** — Bucket: OVS | Context: per-bridge port mirror | Purpose: copy traffic to a destination port for capture/IDS | Activity: select by source/destination ports or VLAN; output to a port or to a VLAN | Mechanism: created and removed transactionally.
  - Example: `ovs-vsctl -- --id=@m create Mirror name=m0 select-all=true output-port=@p -- add Bridge br0 mirrors @m`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`NetFlow` / `sFlow` / `IPFIX`** — Bucket: OVS | Context: flow-export tables | Purpose: send NetFlow v5/v9, sFlow v5, IPFIX records to a collector | Activity: attached to a bridge via `bridge.netflow`/`sflow`/`ipfix` reference | Mechanism: sampling parameters configured per table.
  - Example: `ovs-vsctl -- --id=@s create sFlow targets=\"10.0.0.5:6343\" sampling=64 polling=10 -- set Bridge br0 sflow=@s`
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`QoS` / `Queue`** — Bucket: OVS | Context: traffic-shaping schema | Purpose: per-port HTB/HFSC queues with min/max/burst | Activity: `Queue` rows referenced from `QoS.queues`; QoS attached to a `Port` | Mechanism: `type=linux-htb` (kernel datapath) or `type=egress-policer` (DPDK).
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`SSL` table** — Bucket: OVS | Context: PKI configuration shared by Controller/Manager connections | Purpose: hold paths to CA cert, identity cert, private key, optional bootstrap CA | Activity: read on startup and on reload | Mechanism: single row.
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`Flow_Table` table** — Bucket: OVS | Context: per-bridge per-table OpenFlow configuration | Purpose: name tables, set `flow_limit`, `overflow_action`, `groups` for hashing | Activity: emergency overflow handled per `overflow_action` | Mechanism: associates with a `Bridge.flow_tables` map.
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

- **`CT_Zone` / `CT_Timeout_Policy`** — Bucket: OVS | Context: per-zone connection tracking tuning | Purpose: override default protocol timeouts per zone | Activity: orchestrator creates a `CT_Timeout_Policy`, references it from a `CT_Zone` | Mechanism: timeouts map keyed by `tcp_established`, `udp_first`, etc.
  - Source: https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html

### 1.4 CLI tools & every option

#### `ovs-vsctl`

- Bucket: OVS | Context: high-level OVSDB CLI for the `Open_vSwitch` schema | Purpose: bridge/port/interface lifecycle, controller/manager wiring, generic `get`/`set`/`add`/`remove` over any column | Activity: composes a single transaction per command line | Mechanism: talks to `ovsdb-server` over `--db=` (default `unix:/var/run/openvswitch/db.sock`).
- Synopsis: `ovs-vsctl [OPTIONS] -- COMMAND [ARG...] [-- COMMAND [ARG...]]...`
- Common option set (per `ovs-vsctl(8)`):
  - `--db=DATABASE` — explicit OVSDB target.
  - `--no-wait` — return without waiting for `ovs-vswitchd` to apply the change (use when vswitchd is down).
  - `--no-syslog` — suppress logging the transaction to syslog.
  - `--dry-run` — build the transaction but do not commit.
  - `-t SECS`, `--timeout=SECS` — abort after `SECS` (default: wait forever).
  - `--retry` — retry the connection until the timeout elapses.
  - `--oneline` — escape newlines so each command's output is on a single line.
  - `--bare` — equivalent to `--format=table --no-headings --data=bare`.
  - `--format={table|html|csv|json}`, `--data={string|bare|json}`, `--no-headings`, `--pretty`, `--columns=COLS` — table output controls.
  - `-v[SPEC]`, `--log-file[=FILE]`, `--syslog-target=HOST:PORT`, `--syslog-method=METHOD` — vlog-style logging.
  - `--id=@NAME` — declare a transaction-local UUID name to refer to a row created later in the same `--`-separated chain.
  - `--if-exists`, `--may-exist`, `--if-not-exists` — idempotency guards.
  - `-h`, `--help`, `-V`, `--version`.
- Example: `ovs-vsctl -- add-br br-int -- add-port br-int eth0 -- set Bridge br-int protocols=OpenFlow13`
- Source: https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html
- **Bridge subcommands**: `add-br BR [PARENT VLAN]`, `del-br BR`, `list-br`, `br-exists BR`, `br-to-vlan BR`, `br-to-parent BR`, `br-set-external-id BR KEY [VALUE]`, `br-get-external-id BR [KEY]`, `set-fail-mode BR [standalone|secure]`, `del-fail-mode BR`, `get-fail-mode BR`.
- **Port subcommands**: `add-port BR PORT [-- options]`, `add-bond BR PORT IFACE... [-- options]`, `del-port [BR] PORT`, `list-ports BR`, `port-to-br PORT`.
- **Interface subcommands**: `add-if BR IFACE [options]`, `del-if BR IFACE`, `list-ifaces BR`, `iface-to-br IFACE`.
- **Controller subcommands**: `set-controller BR TARGET...`, `del-controller [BR]`, `get-controller BR`, `set-fail-mode BR [standalone|secure]`.
- **Manager subcommands**: `set-manager TARGET...`, `del-manager`, `get-manager`.
- **SSL subcommands**: `set-ssl PRIVKEY CERT CA-CERT [options]`, `del-ssl`, `get-ssl`.
- **Generic database subcommands** (apply to any table/column):
  - `list TABLE [RECORD...]` — pretty-print rows.
  - `find TABLE [COLUMN[:KEY]=VALUE]...` — search rows; returns matching UUIDs/rows.
  - `get TABLE RECORD COLUMN[:KEY]` — retrieve one value.
  - `set TABLE RECORD COLUMN[:KEY]=VALUE...` — write one or more columns atomically.
  - `add TABLE RECORD COLUMN [KEY=]VALUE...` — append to a set or map.
  - `remove TABLE RECORD COLUMN [KEY=]VALUE...` — remove from a set or map.
  - `clear TABLE RECORD COLUMN...` — set column to empty/default.
  - `create TABLE COLUMN[:KEY]=VALUE...` — create a new row, print UUID.
  - `destroy TABLE RECORD...` — delete rows.
  - `wait-until TABLE RECORD [COLUMN[:KEY]=VALUE]...` — block until condition satisfied (useful in scripts).
- Example (find all ports with `type=internal`): `ovs-vsctl find Interface type=internal`
- Example (wait until controller connected): `ovs-vsctl wait-until -t 10 Controller . is_connected=true`

#### `ovs-ofctl`

- Bucket: OVS | Context: OpenFlow client speaking directly to a switch | Purpose: dump/add/modify/delete flows, groups, meters, ports; trace; monitor | Activity: opens an OpenFlow channel to a bridge — local Unix socket, TCP, or SSL | Mechanism: `--protocols=` selects OpenFlow versions for negotiation.
- Synopsis: `ovs-ofctl [OPTIONS] COMMAND [SWITCH] [ARGS]`
- Frequent commands: `show`, `dump-flows`, `add-flow`, `del-flows`, `mod-flows`, `add-group`, `dump-groups`, `add-meter`, `dump-meters`, `dump-ports`, `dump-tables`, `monitor`, `snoop`, `packet-out`, `replace-flows`.
- Common options (per `ovs-ofctl(8)`):
  - `-O`, `--protocols=PROTO[,PROTO...]` — restrict OpenFlow versions, e.g. `OpenFlow10,OpenFlow13,OpenFlow15`.
  - `--strict` — strict matching for `mod-flows`/`del-flows` (priority + match must match exactly).
  - `--names`/`--no-names` — display port names vs numbers.
  - `--stats`/`--no-stats` — include flow byte/packet counters.
  - `--bundle` — submit `add-flow`/`del-flows`/`replace-flows` in an atomic OpenFlow bundle (1.4+).
  - `-m`, `--more` — include extra fields (cookie, duration).
  - `--read-only` — open the channel in read-only mode.
  - `--sort[=FIELD]`, `--rsort[=FIELD]` — order dumped flows.
  - `--color[=auto|always|never]` — colorise output.
  - `-t`, `--timeout=SECS` — RPC timeout.
  - `-h`, `--help`, `-V`, `--version`, plus the standard `vlog`/`logging` options.
- Example: `ovs-ofctl -O OpenFlow15 dump-flows br-int table=0`
- Source: https://man7.org/linux/man-pages/man8/ovs-ofctl.8.html

#### `ovs-appctl`

- Bucket: OVS | Context: generic runtime control client over Unix domain `*.ctl` socket | Purpose: invoke daemon-specific commands (`coverage/show`, `vlog/set`, `dpif/show`, `ofproto/trace`, ...) without restart | Activity: serialises command, awaits reply | Mechanism: target discovered via `--target` (path or pidfile name).
- Options (per `ovs-appctl(8)`):
  - `-t`, `--target=TARGET` — daemon name or socket path (default `ovs-vswitchd`).
  - `-T`, `--timeout=SECS` — bound the wait; aborts with `SIGALRM`.
  - `-f`, `--format={text|json}` — output format; `json` may wrap text-only commands as `{"reply-format":"plain","reply":"..."}`.
  - `--pretty` — indent JSON (requires `--format=json`).
  - `-h`, `--help`, `-V`, `--version`.
- Common cross-daemon commands:
  - `list-commands`, `version`.
  - `vlog/list`, `vlog/list-pattern`, `vlog/set [SPEC]`, `vlog/set PATTERN:DEST:PATTERN`, `vlog/set FACILITY:FAC`, `vlog/close`, `vlog/reopen`.
- Example: `ovs-appctl -t ovs-vswitchd vlog/set ofproto:file:dbg`
- Source: https://man7.org/linux/man-pages/man8/ovs-appctl.8.html

#### `ovs-dpctl`

- Bucket: OVS | Context: low-level datapath manipulation | Purpose: directly inspect/modify kernel datapath state — useful for debugging and unsafe to mix with running `ovs-vswitchd` for the same datapath | Activity: enumerate datapaths, install/dump/delete flows, manage conntrack | Mechanism: most commands are also reachable via `ovs-appctl dpctl/...` against `ovs-vswitchd`.
- Common commands per `ovs-dpctl(8)`: `add-dp`, `del-dp`, `show`, `add-if`, `del-if`, `dump-flows`, `add-flow`, `mod-flow`, `del-flow`, `del-flows`, `dump-conntrack`, `flush-conntrack`, `ct-stats-show`, `ct-set-limits`, `ct-get-limits`, `ct-set-maxconns`, `ct-get-maxconns`.
- Options: `-s`/`--statistics`, `-m`/`--more`, `--names`/`--no-names`, `--clear`, `-t`/`--timeout=SECS`, `-v`/`--verbose[=SPEC]`, `--log-file[=FILE]`, `--syslog-target=HOST:PORT`, `--syslog-method=METHOD`, `-h`/`--help`, `-V`/`--version`.
- Example: `ovs-appctl dpctl/dump-flows system@ovs-system | wc -l`
- Source: https://man7.org/linux/man-pages/man8/ovs-dpctl.8.html

#### `ovs-pcap` / `ovs-tcpundump`

- Bucket: OVS | Context: helpers for offline packet handling | Purpose: `ovs-pcap` converts a pcap file to one hex-encoded packet per line (the format `ofproto/trace` accepts); `ovs-tcpundump` does the reverse, reconstructing pcap from `tcpdump -xx` output | Activity: piping captures into `ofproto/trace` for what-if analysis | Mechanism: pure reformatters — no kernel state.
- Example: `ovs-pcap capture.pcap | head -1 | xargs -I{} ovs-appctl ofproto/trace br-int "{}"`
- Source: https://man7.org/linux/man-pages/man1/ovs-pcap.1.html and https://man7.org/linux/man-pages/man1/ovs-tcpundump.1.html

#### `ovsdb-tool`

- Bucket: OVS | Context: offline OVSDB file utility | Purpose: create/convert/compact/inspect OVSDB files without a running server | Activity: bootstrap clusters, print transaction logs, compute checksums | Mechanism: opens the file directly — must NOT run against an active database.
- Per-`ovsdb-tool(1)` commands: `create`, `[--cluster-name=NAME] create-cluster [--election-timer=MS] DB CONTENTS LOCAL`, `join-cluster [--cid=UUID] DB NAME LOCAL REMOTE...`, `convert`, `needs-conversion`, `db-version`, `schema-version`, `db-cksum`, `schema-cksum`, `compare-versions A OP B`, `compact`, `query`, `transact`, `show-log [-m]`, `check-cluster DB...`, `db-name`, `schema-name`, `db-cid DB`, `db-sid DB`, `db-local-address DB`.
- Options: `-v`/`--verbose[=SPEC]`, `--log-file[=FILE]`, `-h`/`--help`, `-V`/`--version`.
- Example: `ovsdb-tool create-cluster /etc/openvswitch/ovnsb_db.db OVN_Southbound tcp:10.0.0.1:6644`
- Source: https://man7.org/linux/man-pages/man1/ovsdb-tool.1.html

#### `ovsdb-client`

- Bucket: OVS | Context: live OVSDB client over JSON-RPC | Purpose: introspect the running server, run transactions, monitor changes | Activity: `list-dbs`, `get-schema`, `get-schema-version`, `monitor`, `monitor-cond`, `transact`, `query`, `convert`, `dump`, `wait`, `lock`/`unlock` | Mechanism: connects via `unix:`, `tcp:`, or `ssl:` remotes.
- Options: `--format={json|csv|table}`, `--data={bare|pretty}`, `--no-headings`, `--columns=COLS`, `-t`/`--timeout=SECS`, plus standard logging/help flags.
- Example: `ovsdb-client monitor unix:/var/run/openvswitch/db.sock Open_vSwitch Bridge name,protocols`
- Source: https://man7.org/linux/man-pages/man1/ovsdb-client.1.html

#### Other utilities

- **`ovs-pki`** — Bucket: OVS | Context: helper for PKI used by Controller/Manager SSL — commands `init`, `req`, `sign`, `req+sign`, `fingerprint`, `self-sign`, `set-default`. Source: https://man7.org/linux/man-pages/man8/ovs-pki.8.html
- **`ovs-testcontroller`** — Bucket: OVS | Context: minimal in-tree OpenFlow controller; not for production. Source: https://man7.org/linux/man-pages/man8/ovs-testcontroller.8.html
- **`vtep-ctl`** — Bucket: OVS | Context: same syntax as `ovs-vsctl` but for the VTEP schema (hardware VXLAN gateways). Source: https://man7.org/linux/man-pages/man8/vtep-ctl.8.html

### 1.5 Observability & troubleshooting

- **`ovs-appctl coverage/show`** — Bucket: OVS | Context: instrumentation counter dump | Purpose: visibility into how many times a code path executed (flow installs, upcalls, conntrack ops, ofproto rewrites) | Activity: rate-of-change between two captures = work being done | Mechanism: lightweight thread-local counters compiled into every daemon.
  - Example: `ovs-appctl -t ovs-vswitchd coverage/show | head -40`
  - Source: https://docs.openvswitch.org/en/latest/topics/datapath/

- **`ovs-appctl dpif/show`** — Bucket: OVS | Context: per-datapath summary | Purpose: lookups vs. hits/misses/lost, port stats, megaflow count | Activity: a high `lost` value points at an upcall queue overflow | Mechanism: one row per datapath instance.
  - Example: `ovs-appctl dpif/show`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl dpif/dump-flows BR`** — Bucket: OVS | Context: bridge-scoped megaflow dump | Purpose: see exactly which megaflows are installed for a bridge, including last-used age | Activity: pair with `--names` for human ports | Mechanism: equivalent to `ovs-dpctl dump-flows` filtered by bridge.
  - Example: `ovs-appctl dpif/dump-flows br-int | head -10`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl ofproto/trace`** — Bucket: OVS | Context: simulate OpenFlow pipeline for a synthetic packet | Purpose: see which tables match, which actions fire, where the packet ends up | Activity: critical first step when "the rule is there but the packet doesn't go" | Mechanism: takes either a flow specification or a hex-encoded packet.
  - Example: `ovs-appctl ofproto/trace br-int in_port=1,dl_src=fa:16:3e:01:01:01,dl_dst=fa:16:3e:02:02:02,dl_type=0x0800,nw_src=10.0.0.10,nw_dst=10.0.0.20`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl fdb/show BR`** — Bucket: OVS | Context: bridge MAC-learning table | Purpose: confirm L2 learning is occurring on the right port/VLAN | Activity: blank rows for a chassis usually mean traffic isn't reaching `br-int` | Mechanism: aging governed by `Bridge.other_config:mac-aging-time`.
  - Example: `ovs-appctl fdb/show br-int`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl bond/show` / `lacp/show`** — Bucket: OVS | Context: bond and LACP state | Purpose: which slave is active, LACP partner sysid, churn counters | Activity: pair with `bond/list` and `lacp/list` to enumerate | Mechanism: data sourced from the in-memory bond and LACP state machines.
  - Example: `ovs-appctl bond/show bond0`
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl vlog/list` / `vlog/set`** — Bucket: OVS | Context: dynamic logging knob | Purpose: raise verbosity for a single subsystem (e.g. `dpif:file:dbg`) without restart | Activity: capture, then `vlog/set MODULE:DEST:warn` to revert | Mechanism: per-module per-destination log level.
  - Example: `ovs-appctl vlog/set dpif_netlink:file:dbg`
  - Source: https://man7.org/linux/man-pages/man8/ovs-appctl.8.html

- **`ovs-appctl memory/show`** — Bucket: OVS | Context: memory accounting | Purpose: leak hunting and capacity planning | Activity: shows ofproto handlers/revalidators sizes, OVSDB row counts, etc. | Mechanism: structured key=value report.
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl upcall/show`** — Bucket: OVS | Context: handler/revalidator queue stats | Purpose: detect upcall queue overflow (`lost`) and per-handler skew | Activity: high values indicate flow churn or insufficient handler threads | Mechanism: thread-local counters.
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl dpctl/dump-conntrack`** — Bucket: OVS | Context: live conntrack table dump | Purpose: see every active CT entry per zone | Activity: filter by `zone=N`; combine with `ovs-appctl dpctl/ct-get-limits` | Mechanism: kernel datapath uses nf_conntrack; userspace datapath uses its own table.
  - Example: `ovs-appctl dpctl/dump-conntrack zone=5 | head`
  - Source: https://man7.org/linux/man-pages/man8/ovs-dpctl.8.html

- **`ovs-appctl revalidator/wait` / `revalidator/purge`** — Bucket: OVS | Context: revalidator control commands | Purpose: force a revalidation pass or wait for one to settle (e.g. before assertions in tests) | Activity: complements `coverage/show`'s revalidator counters | Mechanism: thread synchronisation via per-revalidator condition variables.
  - Source: https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html

- **`ovs-appctl dpif-netdev/pmd-stats-show`** — Bucket: OVS | Context: DPDK/userspace-datapath PMD (Poll-Mode Driver) thread statistics | Purpose: per-PMD thread throughput, miss ratio, and idle cycles — primary performance baseline for DPDK deployments | Activity: performance tuning, PMD pinning verification | Mechanism: each PMD thread accumulates packets-processed, cycles-consumed, and miss counters; output includes per-RXQ queue assignment.
  - Example: `ovs-appctl dpif-netdev/pmd-stats-show` — shows each PMD's `numa_id`, `core_id`, `idle cycles`, `processing cycles`, `packets received`, and `missed`.
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **`ovs-appctl dpif-netdev/pmd-rxq-show`** — Bucket: OVS | Context: DPDK PMD per-RX-queue assignment | Purpose: show which PMD thread polls which NIC RX queue | Activity: performance tuning, NUMA-aware queue pinning | Mechanism: each physical port's RX queues are assigned to PMD threads; `pmd-rxq-rebalance` triggers re-assignment.
  - Example: `ovs-appctl dpif-netdev/pmd-rxq-show` — output lists each port's queues with their owning PMD core.
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **`ovs-appctl dpif-netdev/pmd-rxq-rebalance`** — Bucket: OVS | Context: DPDK PMD load balancer | Purpose: redistribute RX queues across available PMD threads based on measured load | Activity: runtime performance optimisation | Mechanism: OVS samples per-queue cycle cost over a configurable interval (`pmd-auto-lb-rebal-interval`); when imbalance exceeds `pmd-auto-lb-improvement-threshold`, rebalances.
  - Example: `ovs-appctl dpif-netdev/pmd-rxq-rebalance` (manual trigger); also auto-triggered when `other_config:pmd-auto-lb=true`.
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **`ovs-appctl dpif-netdev/pmd-perf-show`** — Bucket: OVS | Context: DPDK/userspace-datapath detailed PMD iteration-level metrics | Purpose: expose histogram of batch sizes, latency percentiles per PMD | Activity: latency investigation, burst-size tuning | Mechanism: ring-buffer of per-iteration stats; enabled by `other_config:pmd-perf-metrics=true`.
  - Example: `ovs-appctl dpif-netdev/pmd-perf-show --clear` clears then shows accumulated metrics.
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

- **`ovs-appctl netdev-dpdk/get-mempool-info`** — Bucket: OVS | Context: DPDK memory pool inspection | Purpose: show per-port DPDK mbuf pool statistics (in-use, available, total) — critical for diagnosing packet drops caused by mbuf exhaustion | Activity: DPDK capacity planning, drop investigation | Mechanism: each DPDK port has one or more `rte_mempool`; exhaustion causes RX drops silently at the PMD level.
  - Example: `ovs-appctl netdev-dpdk/get-mempool-info dpdk0`
  - Source: https://docs.openvswitch.org/en/latest/topics/dpdk/

- **OpenFlow protocol version negotiation** — Bucket: OVS | Context: handshake at OpenFlow channel setup | Purpose: select the highest protocol version both sides support | Activity: `Bridge.protocols` advertises versions; controller and `ovs-vswitchd` exchange `OFPT_HELLO` bitmaps | Mechanism: OF 1.3.1 introduced the explicit version-bitmap element.
  - Example: `ovs-vsctl set Bridge br-int protocols=OpenFlow13,OpenFlow15`
  - Source: https://docs.openvswitch.org/en/latest/faq/openflow/


---

## 2. OpenFlow

### 2.1 Pipeline model

**Pipeline Architecture**
- Bucket | Core | Purpose | Activity | Mechanism
  Pipeline execution begins at table 0 (ingress) after packet arrival; packets traverse tables in sequence or via explicit goto_table instructions; tables maintain independent flow entries and perform matching on packet headers and metadata, with results determining packet forwarding. Ingress tables (0-254) process arriving packets; egress tables (OF 1.5+) process packets during egress. Tables are stateless and execute independently.

  Example: `ovs-ofctl add-flow br0 "table=0,priority=100,in_port=1,actions=goto_table:1"`  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, openvswitch.org

**Table Chaining via goto_table**
- Bucket | Flow | Purpose | Activity | Mechanism
  goto_table instruction directs packet to another table for continued pipeline processing; only forward jumps (to higher-numbered table) are allowed in OpenFlow 1.3+; enables multi-stage filtering, classification, and transformations. Packet metadata and action set preserved during jump.

  Example: `table=0,actions=goto_table:2` or `table=1,priority=50,eth_type=0x0806,actions=goto_table:10`  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html, OpenFlow Switch Specification 1.3

**Packet Metadata Fields**
- Bucket | Context | Purpose | Activity | Mechanism
  Metadata maintained during pipeline traversal includes in_port (physical ingress port), in_phy_port (physical port after tunnel decapsulation), tunnel fields (tun_id, tun_src, tun_dst, tun_ipv6_src, tun_ipv6_dst, tun_gbp_id, tun_gbp_flags, tun_erspan_*, tun_gtpu_*), and tun_metadata0-63 (variable 124-byte tunnel metadata). Metadata field (8 bytes, writable) stores arbitrary state across pipeline stages; write_metadata instruction modifies it.

  Example: `match=tunnel_id=0x1234,actions=write_metadata:0xABCD/0xFFFF,goto_table:1`  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**Action Set vs Action List**
- Bucket | Flow | Purpose | Activity | Mechanism
  Action list is an ordered set of actions executed immediately during apply_actions instruction or at pipeline egress; action set is an unordered collection modified by write_actions and cleared by clear_actions instructions. Action set takes precedence at egress; when both present, action set executes (write_actions adds/replaces, does not append). Output, group, controller, and enqueue actions can appear in action set; meter, goto_table cannot.

  Example (action list): `actions=output:1,output:2`; (action set): `write_actions(output:3),output:1` results in output:3 only.  
  Source: OpenFlow Switch Specification 1.3, openvswitch.org

**write_metadata Instruction**
- Bucket | Instruction | Purpose | Activity | Mechanism
  Modifies packet metadata register during pipeline traversal using bitwise AND/OR; applies mask to specify which bits to update. 8-byte metadata field (per-packet state) survives table-to-table transitions and is readable in subsequent tables via metadata match field. Often precedes goto_table to pass state forward.

  Example: `write_metadata:0x5555/0xFFFF` sets metadata to 0x5555; `write_metadata:0x00/0x00FF` clears low byte.  
  Source: OpenFlow Switch Specification 1.3, man7.org/linux/man-pages/man7/ovs-actions.7.html

**Group Tables (all/select/indirect/fast_failover)**
- Bucket | Structure | Purpose | Activity | Mechanism
  Group tables enable multicast, load balancing, and failover without requiring multiple flow entries. Four group types: all (replicate packet to all buckets), select (hash-based load balance across buckets), indirect (single bucket, used for shared failover), fast_failover (active-backup; outputs to first live bucket). Each bucket contains actions (set_field, output, dec_ttl, etc.) and optional bucket-specific parameters (weight for select, watch_port/watch_group for failover).

  Example (all): `group_id=1,type=all,bucket=actions=output:1,bucket=actions=output:2`  
  Example (select): `group_id=2,type=select,bucket=weight=100,actions=output:1,bucket=weight=50,actions=output:2`  
  Example (fast_failover): `group_id=3,type=fast_failover,bucket=watch_port=1,actions=output:1,bucket=watch_port=2,actions=output:2`  
  Source: OpenFlow Switch Specification 1.3, man7.org/linux/man-pages/man8/ovs-ofctl.8.html

**Meter Table**
- Bucket | QoS | Purpose | Activity | Mechanism
  Meters apply rate limiting and burst control at packet level during pipeline; specified via meter instruction with meter_id. Each meter defines bands (drop, remark) with rates and burst sizes in kbps or packets/sec. Green, yellow, red colors assigned based on rate compliance. Meter tables introduced in OpenFlow 1.3; applied before group/output actions.

  Example: `meter=1` in action set triggers meter 1; meter definition: `meter_id=1,kbps,burst_size=1000,band=type=drop,rate=5000`  
  Source: OpenFlow Switch Specification 1.3

**Instructions vs Actions Distinction**
- Bucket | Semantic | Purpose | Activity | Mechanism
  Instructions (meter, apply_actions, clear_actions, write_actions, write_metadata, goto_table) are ordered, flow-level directives that modify pipeline state and action set; Actions (output, group, set_field, dec_ttl, etc.) are immediate operations executed within apply_actions or at egress. Instructions are processed sequentially; actions within apply_actions execute in order; action set (from write_actions) executes at egress and is unordered.

  Example: `meter:1,write_actions(output:2),apply_actions(output:1),goto_table:1` processes meter, sets action set to output:2, immediately outputs to 1, then jumps to table 1.  
  Source: OpenFlow Switch Specification 1.3, openvswitch.org

**Multipart Messages (OFPT_MULTIPART_REQUEST/REPLY)**
- Bucket | Protocol | Purpose | Activity | Mechanism
  Request/reply pairs split large data (flows, tables, meters, groups, ports) across multiple messages to avoid payload overflow. Common multipart types: FLOW (matching flows), AGGREGATE (stats summary), TABLE (table capabilities), PORT_STATS (per-port counters), GROUP (group configuration), METER (meter config), METER_FEATURES (meter limits), TABLE_FEATURES (table match/write/apply capabilities). Each reply carries flags (OFPMPF_REPLY_MORE) indicating continuation.

  Example: `ovs-ofctl dump-flows br0` sends MULTIPART_REQUEST(type=FLOW) and assembles MULTIPART_REPLY fragments.  
  Source: OpenFlow Switch Specification 1.3, man7.org/linux/man-pages/man8/ovs-ofctl.8.html

**OpenFlow Reserved Port Numbers**
- Bucket | Constants | Purpose | Activity | Mechanism
  Reserved ports (0xFFF8-0xFFFF) direct packets without physical port references. OFPP_IN_PORT (0xFFF8, 65528): output to ingress port. OFPP_TABLE (0xFFF9, 65529): resubmit to pipeline table 0. OFPP_NORMAL (0xFFFA, 65530): normal L2/L3 bridging/routing. OFPP_FLOOD (0xFFFB, 65531): output to all ports except ingress. OFPP_ALL (0xFFFC, 65532): multicast to all ports. OFPP_CONTROLLER (0xFFFD, 65533): send to controller as OFPT_PACKET_IN. OFPP_LOCAL (0xFFFE, 65534): local interface (bridge itself). OFPP_UNSET (0xFFF7, 65527): uninitialized state in some contexts.

  Example: `actions=output:OFPP_FLOOD` floods packet; `actions=output:OFPP_CONTROLLER:65535` sends entire packet to controller.  
  Source: OpenFlow Switch Specification 1.0/1.3, man7.org/linux/man-pages/man7/ovs-fields.7.html

**Table 0 Ingress Pipeline**
- Bucket | Core | Purpose | Activity | Mechanism
  Table 0 is mandatory ingress table where all packets enter after input port validation and port state checks. Packet headers extracted from wire format; in_port metadata set; prerequisite matching checks enforce eth_type, ip_proto dependencies. No egress tables before table 0. Packets failing table 0 matches drop by default; highest-priority matching flow entry determines actions.

  Example: `table=0,priority=200,in_port=1,eth_type=0x0800,actions=goto_table:1`  
  Source: OpenFlow Switch Specification 1.0/1.3, openvswitch.org


### 2.2 Match fields, instructions, actions

**in_port (16 bits, OpenFlow 1.0+)**
- Bucket | Match | Purpose | Activity | Mechanism
  Identifies physical OpenFlow port on which packet arrived; read-only metadata set at ingress from wire-level port index. Non-maskable (exact match only). Prerequisites: none. Prerequisite: OpenFlow 1.1+. NXM: NXM_OF_IN_PORT (0); OXM: (OpenFlow 1.2+ uses OXM_OF_IN_PORT, 4 bytes expanded).

  Example: `in_port=1` matches packets on port 1; `in_port=65528` matches OFPP_IN_PORT.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**in_phy_port (32 bits, OpenFlow 1.2+ / OVS 1.7+)**
- Bucket | Match | Purpose | Activity | Mechanism
  Physical port after tunnel decapsulation; distinguishes physical ingress from tunneled encapsulation. When packet arrives in tunnel, in_phy_port stores actual hardware port; in_port may point to tunnel port. Non-maskable. OXM field (OF 1.2+).

  Example: `in_phy_port=2` on VXLAN tunnel port identifies physical underlay port 2.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**eth_src / eth_dst (48 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | L2 | Purpose | Activity | Mechanism
  Source/destination MAC addresses; 6-byte Ethernet address. Maskable (CIDR/wildcard). Prerequisites: Ethernet (any eth_type). OXM (OF 1.2+); also aliased as dl_src/dl_dst (NXM). Read-write (settable with set_field).

  Example: `eth_src=00:11:22:33:44:55/FF:FF:FF:FF:00:00` matches OUI; `actions=set_field:aa:bb:cc:dd:ee:ff->eth_src`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**eth_type (16 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | L2 | Purpose | Activity | Mechanism
  EtherType field identifying L3 protocol (0x0800 IPv4, 0x86DD IPv6, 0x0806 ARP, 0x8847/0x8848 MPLS, 0x88CC LLDP). Non-maskable, non-writable. OXM (OF 1.2+); aliased as dl_type (NXM). Prerequisite field for IPv4, IPv6, ARP, MPLS matching.

  Example: `eth_type=0x0800` matches IPv4; `eth_type=0x86DD` matches IPv6.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**vlan_vid (12 bits, OF 1.2+ / OVS 1.7+)**
- Bucket | VLAN | Purpose | Activity | Mechanism
  VLAN ID (VID) in 802.1Q header (low 12 bits of 2-byte VLAN tag). Maskable. Matches untagged packets via vlan_vid=0xfffe (OFVPID_ANY); tagged packets matched by 0x1000-0x1fff range. Readable and writable. OXM (OF 1.2+).

  Example: `vlan_vid=0x1005` matches VLAN 5; `vlan_vid=0` matches untagged; `actions=set_field:0x1010->vlan_vid`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**vlan_pcp (3 bits, OF 1.2+ / OVS 1.7+)**
- Bucket | VLAN | Purpose | Activity | Mechanism
  VLAN Priority Code Point (PCP, 3 bits of priority); 0-7 queue priority levels. Non-maskable. Writable (set_field). Requires vlan_vid match to be meaningful. OXM (OF 1.2+).

  Example: `vlan_vid=0x1005,vlan_pcp=7` matches VLAN 5, highest priority; `actions=set_field:3->vlan_pcp`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**ip_dscp (6 bits, OF 1.2+ / OVS 1.7+)**
- Bucket | L3 QoS | Purpose | Activity | Mechanism
  Differentiated Services Code Point (DSCP) in IPv4 ToS or IPv6 Traffic Class (high 6 bits). Non-maskable. Writable. Prerequisites: IPv4 or IPv6 (eth_type=0x0800 or 0x86DD). OXM (OF 1.2+).

  Example: `eth_type=0x0800,ip_dscp=46` matches IPv4 DSCP 46 (Expedited Forwarding); `actions=set_field:24->ip_dscp`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**ip_ecn (2 bits, OF 1.2+ / OVS 1.7+)**
- Bucket | L3 QoS | Purpose | Activity | Mechanism
  Explicit Congestion Notification (ECN) field (low 2 bits of IPv4 ToS or IPv6 Traffic Class). Matches 0-3 congestion states. Non-maskable, writable. Prerequisites: IPv4/IPv6. OXM (OF 1.2+).

  Example: `eth_type=0x0800,ip_ecn=1` matches IPv4 ECT(1); `actions=set_field:3->ip_ecn` sets CE.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ip_proto (8 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | L3 | Purpose | Activity | Mechanism
  IPv4 Protocol or IPv6 Next Header field identifying L4 protocol (6=TCP, 17=UDP, 1=ICMP, 50=ESP, etc.). Non-maskable, non-writable. Prerequisites: IPv4/IPv6. OXM (OF 1.2+). Prerequisite match for TCP/UDP/SCTP/ICMP fields.

  Example: `eth_type=0x0800,ip_proto=6` matches IPv4 TCP; `eth_type=0x0800,ip_proto=17,actions=goto_table:2`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ipv4_src / ipv4_dst (32 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | IPv4 | Purpose | Activity | Mechanism
  Source/destination IPv4 address (dotted quad notation or CIDR). Maskable (CIDR). Writable. Prerequisites: IPv4 (eth_type=0x0800). OXM (OF 1.2+).

  Example: `eth_type=0x0800,ipv4_src=10.0.0.0/8` matches private RFC1918; `actions=set_field:192.168.1.1->ipv4_src`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**ipv6_src / ipv6_dst (128 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | IPv6 | Purpose | Activity | Mechanism
  Source/destination IPv6 address (colon-hex or compressed notation). Maskable (CIDR). Writable. Prerequisites: IPv6 (eth_type=0x86DD). OXM (OF 1.2+).

  Example: `eth_type=0x86dd,ipv6_src=2001:db8::/32` matches 2001:db8 prefix; `actions=set_field:fe80::1->ipv6_src`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**ipv6_flabel (20 bits, OF 1.2+ / OVS 1.11+)**
- Bucket | IPv6 QoS | Purpose | Activity | Mechanism
  IPv6 Flow Label (20-bit flow identifier for QoS/load balancing). Non-maskable, non-writable. Prerequisites: IPv6. OXM (OF 1.2+).

  Example: `eth_type=0x86dd,ipv6_flabel=0x12345` matches IPv6 flow label 0x12345.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ipv6_exthdr (16 bits, OF 1.2+ / OVS 1.11+)**
- Bucket | IPv6 | Purpose | Activity | Mechanism
  IPv6 Extension Header presence bitmap (bit 0=hop-by-hop, 1=routing, 2=fragment, 3=DSTOPTS, etc.). Maskable. Non-writable. Prerequisites: IPv6. OXM (OF 1.2+).

  Example: `eth_type=0x86dd,ipv6_exthdr=0x4` matches packets with IPv6 fragment header.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**tcp_src / tcp_dst (16 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | L4 | Purpose | Activity | Mechanism
  TCP source/destination port. Maskable (range). Writable. Prerequisites: TCP (eth_type=IPv4/IPv6, ip_proto=6). OXM (OF 1.2+); aliased as tp_src/tp_dst (NXM).

  Example: `eth_type=0x0800,ip_proto=6,tcp_dst=80` matches HTTP; `actions=set_field:8080->tcp_dst`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**udp_src / udp_dst (16 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | L4 | Purpose | Activity | Mechanism
  UDP source/destination port. Maskable. Writable. Prerequisites: UDP (eth_type=IPv4/IPv6, ip_proto=17). OXM (OF 1.2+).

  Example: `eth_type=0x0800,ip_proto=17,udp_dst=53` matches DNS; `actions=set_field:5353->udp_dst`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**sctp_src / sctp_dst (16 bits, OF 1.2+ / OVS 2.0+)**
- Bucket | L4 | Purpose | Activity | Mechanism
  SCTP source/destination port. Maskable. Writable. Prerequisites: SCTP (eth_type=IPv4/IPv6, ip_proto=132). OXM (OF 1.2+).

  Example: `eth_type=0x0800,ip_proto=132,sctp_src=132` matches SCTP.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**icmp_type / icmp_code (8 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | ICMP | Purpose | Activity | Mechanism
  ICMPv4 type (0=echo reply, 8=echo request, 11=time exceeded) and code. Non-maskable, writable. Prerequisites: ICMPv4 (eth_type=0x0800, ip_proto=1). OXM (OF 1.2+).

  Example: `eth_type=0x0800,ip_proto=1,icmp_type=8` matches ICMP echo (ping) request.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**arp_op (16 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | ARP | Purpose | Activity | Mechanism
  ARP opcode (1=request, 2=reply). Non-maskable, writable. Prerequisites: ARP (eth_type=0x0806 or 0x8035 RARP). OXM (OF 1.2+).

  Example: `eth_type=0x0806,arp_op=1` matches ARP request.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**arp_spa / arp_tpa (32 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | ARP | Purpose | Activity | Mechanism
  ARP sender/target protocol address (IPv4 address). Maskable (CIDR). Writable. Prerequisites: ARP. OXM (OF 1.2+).

  Example: `eth_type=0x0806,arp_spa=10.0.0.0/8` matches ARP from 10.0.0.0/8.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**arp_sha / arp_tha (48 bits, OF 1.2+ / OVS 1.1+)**
- Bucket | ARP | Purpose | Activity | Mechanism
  ARP sender/target hardware address (MAC). Maskable. Writable. Prerequisites: ARP. OXM (OF 1.2+).

  Example: `eth_type=0x0806,arp_sha=00:11:22:00:00:00/FF:FF:FF:00:00:00` matches OUI.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**mpls_label (20 bits, OF 1.2+ / OVS 1.11+)**
- Bucket | MPLS | Purpose | Activity | Mechanism
  MPLS label (20-bit identifier). Non-maskable, writable. Prerequisites: MPLS (eth_type=0x8847/0x8848). OXM (OF 1.2+).

  Example: `eth_type=0x8847,mpls_label=100` matches MPLS label 100.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**mpls_tc (3 bits, OF 1.2+ / OVS 1.11+)**
- Bucket | MPLS | Purpose | Activity | Mechanism
  MPLS Traffic Class (3-bit QoS level). Non-maskable, writable. Prerequisites: MPLS. OXM (OF 1.2+).

  Example: `eth_type=0x8847,mpls_tc=5` matches MPLS traffic class 5.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**mpls_bos (1 bit, OF 1.3+ / OVS 1.11+)**
- Bucket | MPLS | Purpose | Activity | Mechanism
  MPLS Bottom of Stack (BOS, 1 when label is last in stack). Non-maskable, non-writable. Prerequisites: MPLS. OXM (OF 1.3+).

  Example: `eth_type=0x8847,mpls_bos=1` matches last MPLS label in stack.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**tunnel_id / tun_id (64 bits, OF 1.3+ / OVS 1.1+)**
- Bucket | Tunnel | Purpose | Activity | Mechanism
  Tunnel ID (VNI/VXLAN ID, Geneve VNI, etc.); arbitrary 64-bit metadata for tunnel segmentation. Maskable, writable. Preserved across pipeline. OXM (OF 1.3+); also called tun_id. Prerequisites: none.

  Example: `tunnel_id=0x1234` matches VXLAN VNI 0x1234; `actions=set_field:0x5678->tunnel_id`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.3

**pbb_isid (24 bits, PB/VB)**
- Bucket | Provider Bridge | Purpose | Activity | Mechanism
  Provider Backbone Bridge I-SID (Service Instance ID). Maskable, writable. OXM support varies. Used in 802.1ah encapsulation.

  Example: `pbb_isid=0x123456` matches I-SID.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**metadata (64 bits, OF 1.2+ / OVS 1.8+)**
- Bucket | Pipeline | Purpose | Activity | Mechanism
  Arbitrary 64-bit per-packet state writable via write_metadata instruction; survives table-to-table transitions; used to pass state between pipeline stages without modifying packet headers. Maskable. OXM (OF 1.2+).

  Example: `write_metadata:0xABCD/0xFFFF` sets low 16 bits; `table=1,metadata=0xABCD/0xFFFF,actions=...`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html, OpenFlow Switch Specification 1.2

**reg0-reg15 (32 bits each, OVS 1.1+)**
- Bucket | NXM | Purpose | Activity | Mechanism
  Nicira extension register fields (16 × 32-bit registers); writable metadata for packet state. Maskable, read-write. Prerequisites: none. Intended for custom packet classification and forwarding state. OVS 1.1+.

  Example: `actions=load:0x12->reg0,goto_table:1` loads 0x12 into reg0; `table=1,reg0=0x12,actions=...`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**xreg0-xreg7 (64 bits each, OF 1.3+ / OVS 2.4+)**
- Bucket | NXM | Purpose | Activity | Mechanism
  Extended registers (8 × 64-bit, equivalent to paired reg0-1, reg2-3, etc.). Maskable, read-write. OXM (OF 1.3+). Provide wider state fields than 32-bit registers.

  Example: `actions=load:0x123456789ABCDEF0->xreg0`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**xxreg0-xxreg3 (128 bits each, OVS 2.6+)**
- Bucket | NXM | Purpose | Activity | Mechanism
  Ultra-extended registers (4 × 128-bit, equivalent to quad reg0-3, reg4-7, etc.). Maskable, read-write. OVS 2.6+. Provide widest state fields.

  Example: `actions=load:0xffffffffffffffffffffffffffffffff->xxreg0`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_state (32 bits, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Connection tracking state bitmap (trk=tracked, new=new connection, est=established, rel=related, rpl=reply direction, inv=invalid/untracked). Read-only (set by ct action). Non-maskable per spec but OVS allows matches. Prerequisites: none. NXM (OVS 2.5+).

  Example: `ct_state=+trk+est,actions=accept` matches tracked established connections; `actions=ct(table=1)` initiates tracking.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_zone (16 bits, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Connection tracking zone (logical firewall context); separate zone ID per logical network segment. Non-maskable, read-only. Set via ct action zone argument. Prerequisites: none. OVS 2.5+.

  Example: `actions=ct(zone=1,table=1)` tracks in zone 1; subsequent matches use `ct_zone=1`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_mark (32 bits, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Connection tracking mark (32-bit metadata per connection); useful for distinguishing connection types or rule hits. Maskable, writable. Set via ct action mark argument or set_field on packet during tracked state. OVS 2.5+.

  Example: `actions=ct(commit,mark=0x1234)` marks connection; `ct_mark=0x1234,actions=drop` drops marked connections.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_label (128 bits, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Connection tracking label (128-bit metadata per connection); wider than ct_mark for fine-grained labeling. Maskable, writable. OVS 2.5+.

  Example: `actions=ct(commit,label=0xabcdef0123456789abcdef0123456789)`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_nw_proto (8 bits, OVS 2.8+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Network protocol from original direction of tracked connection (IP protocol number). Read-only. Prerequisites: CT (connection tracked). OVS 2.8+.

  Example: `ct_state=+trk,ct_nw_proto=6,actions=...` matches tracked TCP connections.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**ct_tp_src / ct_tp_dst (16 bits, OVS 2.8+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Transport (L4) port from original direction of tracked connection. Read-only. Maskable. Prerequisites: CT. OVS 2.8+.

  Example: `ct_state=+trk,ct_tp_dst=80,actions=...` matches tracked HTTP connections.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**conj_id (32 bits, OVS 2.4+)**
- Bucket | Conjunctive Match | Purpose | Activity | Mechanism
  Conjunction ID for multipart matching (clause selection in n-way conjunctions). Read-only, non-maskable. Set implicitly during conjunction action evaluation. OVS 2.4+.

  Example: `actions=conjunction(1,1/2),conjunction(2,2/2)` sets up clauses; matched via `conj_id=1` or `conj_id=2`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**pkt_mark (32 bits, OVS 2.0+)**
- Bucket | Packet | Purpose | Activity | Mechanism
  Linux skb_mark field (32-bit OS-level packet metadata). Maskable, writable. Survives pipeline. Useful for interaction with kernel netfilter/tc. OVS 2.0+. Prerequisites: none.

  Example: `actions=set_field:0x1234->pkt_mark` marks packet for kernel tc; `pkt_mark=0x1234,actions=output:1`.  
  Source: man7.org/linux/man-pages/man7/ovs-fields.7.html

**tcp_flags (16 bits, OVS 2.1+ / NXM_NX_TCP_FLAGS)**
- Bucket: OVS | Context: NXM extension match field | Purpose: match individual TCP control bits (SYN, ACK, FIN, RST, PSH, URG, ECE, CWR, NS) independently or in combination | Activity: stateful firewall rules, SYN-flood detection, connection state steering | Mechanism: 16-bit bitmask; low 9 bits are standard TCP flags per RFC 793 and RFC 3168; maskable so only specified bits need to match.
  - Flag bit positions: bit 0 = FIN, bit 1 = SYN, bit 2 = RST, bit 3 = PSH, bit 4 = ACK, bit 5 = URG, bit 6 = ECE, bit 7 = CWR, bit 8 = NS.
  - Prerequisites: TCP (eth_type=0x0800 or 0x86DD, ip_proto=6). Read-only (not writable via set_field).
  - Example: `eth_type=0x0800,ip_proto=6,tcp_flags=0x002/0x002` matches all TCP SYN packets (bit 1 set); `tcp_flags=0x012/0x012` matches SYN-ACK (bits 1 and 4).
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

**dp_hash (32 bits, OVS 2.2+ / NXM_NX_DP_HASH)**
- Bucket: OVS | Context: NXM extension match field | Purpose: expose the datapath's internal packet hash for use in `select` group load-balancing and ECMP logic | Activity: select-group bucket selection, custom ECMP steering without explicit hash computation | Mechanism: populated by the `hash` action — `hash(l4,basis=N)` computes a 32-bit hash over L4-relevant fields; the result is written into `dp_hash` before resubmission; subsequent flows match on `dp_hash` modulo the bucket count.
  - Read-only from the flow's perspective after `hash` action executes; maskable.
  - Example: `actions=hash(l4,basis=0),resubmit(,10)` then `table=10,dp_hash=0x0/0x1,actions=output:1; table=10,dp_hash=0x1/0x1,actions=output:2` splits flows across two paths.
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html

**actset_output (32 bits, OVS 2.4+ / OF 1.5+)**
- Bucket: OVS/OpenFlow | Context: OXM field defined in OpenFlow 1.5 | Purpose: read the output port stored in the current action set (from a prior `write_actions(output:N)`) so that subsequent flow entries can match on the already-chosen output port | Activity: egress pipeline (OF 1.5 egress tables), output-conditional processing | Mechanism: populated by `write_actions`; match `actset_output=N` in an egress table to apply per-port transformations.
  - Read-only. Prerequisites: none, but meaningful only when an output action is in the action set.
  - Example (OF 1.5 egress): `table=64,actset_output=1,vlan_vid=0x1005,actions=pop_vlan` strips VLAN only when the final output is port 1.
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html; OpenFlow Switch Specification 1.5

**NSH fields (OVS 2.8+ / Network Service Header — RFC 8300)**
- Bucket: OVS | Context: NXM/OXM fields for Network Service Header processing | Purpose: match and rewrite NSH header fields for service-function chaining (SFC) — packet classification at each service function forwarder (SFF) | Activity: service chaining, SFC path classification, NSH-encapsulated VM/container networking | Mechanism: NSH is an encapsulation added between the outer transport header and inner payload; OVS 2.8+ can parse, match, and modify NSH headers via `decap`/`encap` actions.
  - Key fields:
    - `nsh_mdtype` (8 bits) — NSH MD-Type (1 = fixed-length, 2 = variable-length TLV). Maskable. Prerequisites: packet_type=0x894f (NSH Ethertype).
    - `nsh_np` (8 bits) — NSH Next Protocol (1=IPv4, 2=IPv6, 3=Ethernet, 4=NSH). Maskable.
    - `nsh_spi` (24 bits) — NSH Service Path Identifier (which SFC path). Maskable.
    - `nsh_si` (8 bits) — NSH Service Index (position within path; decremented at each hop). Maskable.
    - `nsh_c1`–`nsh_c4` (32 bits each) — NSH Context headers (carry per-path metadata such as tenant ID, VNI). Maskable, writable.
  - Example: `nsh_spi=0x100,nsh_si=0xff,actions=dec_nsh_si,output:OFPP_LOCAL` implements a service function that decrements the SI and forwards locally.
  - Source: https://man7.org/linux/man-pages/man7/ovs-fields.7.html; RFC 8300 (https://www.rfc-editor.org/rfc/rfc8300)

**Instruction: meter**
- Bucket | QoS | Purpose | Activity | Mechanism
  Specifies meter table entry by meter_id; applies rate limiting and burst control. Executes before actions. Green/yellow/red color determined by meter band rates (kbps or pps). Meter introduction: OpenFlow 1.3.

  Example: `meter=1` applies meter_id=1; meter definition `meter_id=1,kbps,burst_size=1000,band=type=drop,rate=5000`.  
  Source: OpenFlow Switch Specification 1.3

**Instruction: apply_actions**
- Bucket | Flow | Purpose | Activity | Mechanism
  Immediately executes ordered action list (output, set_field, dec_ttl, etc.); actions not added to action set. Execution at instruction point, not deferred to egress. Multiple apply_actions processed sequentially.

  Example: `apply_actions(set_field:aa:bb:cc:dd:ee:ff->eth_src,output:1)` immediately modifies and outputs.  
  Source: OpenFlow Switch Specification 1.3

**Instruction: clear_actions**
- Bucket | Flow | Purpose | Activity | Mechanism
  Empties action set (discards all prior write_actions). Commonly used before applying final action list. Allows action set replacement.

  Example: `write_actions(output:2),clear_actions,apply_actions(output:3)` results in output:3 only.  
  Source: OpenFlow Switch Specification 1.3

**Instruction: write_actions**
- Bucket | Flow | Purpose | Activity | Mechanism
  Adds/replaces actions in action set (unordered); executed at egress after all table processing. Multiple write_actions replace prior set (not cumulative). Action set limited to output, group, controller, enqueue, set_queue.

  Example: `write_actions(output:1),goto_table:2` sets output:1 in action set, then processes table 2; output:1 executes at egress.  
  Source: OpenFlow Switch Specification 1.3

**Instruction: write_metadata**
- Bucket | Flow | Purpose | Activity | Mechanism
  Modifies metadata register (8 bytes) via bitwise AND/OR with mask. Applies during pipeline; survives to next table via goto_table. Commonly paired with goto_table to pass state.

  Example: `write_metadata:0xFFFF/0xFFFF,goto_table:1` sets metadata to 0xFFFF; `table=1,metadata=0xFFFF,actions=...`.  
  Source: OpenFlow Switch Specification 1.3

**Instruction: goto_table**
- Bucket | Flow | Purpose | Activity | Mechanism
  Redirects packet to another table for continued processing. Only forward jumps (to higher-numbered table) allowed in OF 1.3+; some OVS versions allow arbitrary jumps. Packet metadata and action set preserved.

  Example: `goto_table:5` jumps to table 5; `table=0,priority=100,in_port=1,actions=goto_table:5`.  
  Source: OpenFlow Switch Specification 1.3

**Action: output**
- Bucket | Forwarding | Purpose | Activity | Mechanism
  Outputs packet to physical port or reserved port (OFPP_CONTROLLER, OFPP_FLOOD, etc.). Syntax: `output:port` or `output(port=N,max_len=nbytes)` for controller truncation. Port can be NXM field reference for dynamic routing.

  Example: `actions=output:1` outputs to port 1; `actions=output:OFPP_CONTROLLER:65535` sends to controller; `actions=output:NXM_NX_REG0[]` outputs to port in reg0.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: group**
- Bucket | Multicast/LB | Purpose | Activity | Mechanism
  Applies group table entry (multicast, load balancing, failover). Syntax: `group:group_id`. Group types: all (replicate), select (hash LB), indirect (single bucket), fast_failover (active-backup).

  Example: `actions=group:1` applies group_id=1 with type=all; buckets output to multiple ports.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: drop (implicit)**
- Bucket | Forwarding | Purpose | Activity | Mechanism
  Discards packet (no action or empty action list at table egress). Implicit; no explicit drop action syntax. Matched by absence of output/group/controller actions.

  Example: Table with no matching flow results in drop; explicit action list `actions=` (empty) drops packet.  
  Source: OpenFlow Switch Specification 1.3

**Action: set_field**
- Bucket | Modification | Purpose | Activity | Mechanism
  Modifies packet header/metadata field via write semantics. Syntax: `set_field:value->field` or `set_field(field:=value)`. Supports all writable OXM/NXM fields (eth_src/dst, ipv4_src/dst, tcp_src/dst, metadata, reg*, etc.).

  Example: `actions=set_field:192.168.1.1->ipv4_dst` rewrites destination IP; `actions=set_field:0xFFFF->metadata`.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: copy_field (OpenFlow 1.5+)**
- Bucket | Modification | Purpose | Activity | Mechanism
  Copies bits from src field to dst field. Syntax: `copy_field:src->dst` or `copy_field(src_offset:src_field,dst_offset:dst_field,n_bits)`. Enables dynamic field population.

  Example: `actions=copy_field:ipv4_src->ipv4_dst` copies source to destination; `actions=copy_field(0:reg0,0:eth_src,48)` copies 48 bits from reg0 to eth_src.  
  Source: OpenFlow Switch Specification 1.5, man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: push_vlan**
- Bucket | VLAN | Purpose | Activity | Mechanism
  Pushes VLAN tag on packet. Syntax: `push_vlan:ethertype` (0x8100 for standard, 0x9100 for QinQ). Increments eth_type depth; allows stacking.

  Example: `actions=push_vlan:0x8100,set_field:0x1005->vlan_vid` tags packet VLAN 5.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: pop_vlan**
- Bucket | VLAN | Purpose | Activity | Mechanism
  Removes outermost VLAN tag. Syntax: `pop_vlan`. Strips one level of 802.1Q header.

  Example: `actions=pop_vlan` removes VLAN tag; permits QinQ untag.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: push_mpls**
- Bucket | MPLS | Purpose | Activity | Mechanism
  Pushes MPLS label on packet. Syntax: `push_mpls:ethertype` (0x8847 for unicast, 0x8848 for multicast). Sets TTL and TC; can set label via set_field following push.

  Example: `actions=push_mpls:0x8847,set_field:100->mpls_label` pushes MPLS label 100.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: pop_mpls**
- Bucket | MPLS | Purpose | Activity | Mechanism
  Removes outermost MPLS label. Syntax: `pop_mpls:ethertype` where ethertype is post-pop payload type (0x0800 IPv4, 0x86DD IPv6, etc.).

  Example: `actions=pop_mpls:0x0800` removes MPLS label, revealing IPv4 packet.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: push_pbb**
- Bucket | Provider Bridge | Purpose | Activity | Mechanism
  Pushes Provider Backbone Bridge (802.1ah) header. Syntax: `push_pbb` or with I-SID via set_field.

  Example: `actions=push_pbb,set_field:0x123456->pbb_isid`.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: pop_pbb**
- Bucket | Provider Bridge | Purpose | Activity | Mechanism
  Removes PBB header. Syntax: `pop_pbb`.

  Example: `actions=pop_pbb`.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: set_queue**
- Bucket | QoS | Purpose | Activity | Mechanism
  Sets egress queue for output action. Syntax: `set_queue:queue_id`. Specifies QoS queue; output action follows queue selection.

  Example: `actions=set_queue:1,output:1` outputs to port 1, queue 1.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: dec_ttl**
- Bucket | L3 | Purpose | Activity | Mechanism
  Decrements IP TTL (IPv4) or Hop Limit (IPv6). Syntax: `dec_ttl`. Drops packet if TTL reaches 0 (except with OVS send-to-controller extensions). Prerequisites: IPv4/IPv6.

  Example: `actions=dec_ttl` decrements TTL; often used in routing rules.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: dec_mpls_ttl**
- Bucket | MPLS | Purpose | Activity | Mechanism
  Decrements outermost MPLS TTL. Syntax: `dec_mpls_ttl`. Drops if TTL reaches 0 (with OVS extensions). Prerequisites: MPLS.

  Example: `actions=dec_mpls_ttl` decrements MPLS TTL.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: set_mpls_ttl**
- Bucket | MPLS | Purpose | Activity | Mechanism
  Sets MPLS TTL explicitly. Syntax: `set_mpls_ttl:ttl`. Prerequisites: MPLS.

  Example: `actions=set_mpls_ttl:64` sets MPLS TTL to 64.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: copy_ttl_in**
- Bucket | TTL | Purpose | Activity | Mechanism
  Copies inner TTL (from IPv4/IPv6 under MPLS) to outer MPLS TTL. Syntax: `copy_ttl_in`. Used in MPLS tunneling.

  Example: `actions=copy_ttl_in` copies IPv4 TTL to MPLS outer TTL.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: copy_ttl_out**
- Bucket | TTL | Purpose | Activity | Mechanism
  Copies outer MPLS TTL to inner IP TTL. Syntax: `copy_ttl_out`. Used in MPLS pop.

  Example: `actions=pop_mpls:0x0800,copy_ttl_out` removes MPLS, copies outer TTL to IPv4.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: set_nw_ttl**
- Bucket | L3 | Purpose | Activity | Mechanism
  Sets IP TTL explicitly. Syntax: `set_nw_ttl:ttl`. Equivalent to dec_ttl in reverse (direct write). Prerequisites: IPv4/IPv6.

  Example: `actions=set_nw_ttl:128` sets TTL to 128 (typically used in response packets).  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: resubmit (Nicira extension, OVS 1.1+)**
- Bucket | Recirculation | Purpose | Activity | Mechanism
  Resubmits packet to table (default 0 or specified). Syntax: `resubmit` or `resubmit:table` or `resubmit(port:port,table:table)`. Restarts pipeline without goto_table; creates loop-detection counter to prevent infinite loops (default 32 hops). Used for multi-stage classification.

  Example: `actions=resubmit:10` resubmits to table 10; `actions=resubmit(port:OFPP_CONTROLLER,table:0)`.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html, openvswitch.org

**Action: learn (Nicira extension, OVS 1.11+)**
- Bucket | Learning | Purpose | Activity | Mechanism
  Dynamically installs flow entries based on matched traffic. Syntax: `learn(table:N,priority:P,match_field=value,action=...)`. Extracts fields from packet and creates flows; useful for MAC learning, ARP caching. OVS 1.11+.

  Example: `actions=learn(table=10,priority=32768,eth_src=eth_src,eth_dst=eth_dst,output:NXM_OF_IN_PORT[])` learns L2 switching rules.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: conjunction (Nicira extension, OVS 2.4+)**
- Bucket | Matching | Purpose | Activity | Mechanism
  Implements n-way conjunctive matching (all clauses must match). Syntax: `conjunction(id,i/n)` where id is conjunction ID, i is clause index, n is total clauses. Matched packets trigger conj_id match. OVS 2.4+.

  Example: `actions=conjunction(1,1/2),conjunction(1,2/2)` two-clause rule; matching both triggers conj_id=1 for further rules.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: ct (Nicira extension, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Connection tracking; initiates or commits tracked state. Syntax: `ct([argument]...)` with args: zone=N, mark=N, label=..., nat(type=src|dst|both|reverse), commit, force, table=N, timeout=N, alg=type. Stateful firewall foundation. OVS 2.5+.

  Example: `actions=ct(zone=1,commit,table=1)` tracks packet in zone 1, commits connection, continues to table 1.  
  Example: `actions=ct(nat(src=192.168.1.0/24),table=1)` applies source NAT.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: ct_clear (Nicira extension, OVS 2.5+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Clears connection tracking state (trk=0). Syntax: `ct_clear`. Forces packet to appear untracked. OVS 2.5+.

  Example: `actions=ct_clear` resets tracking.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: decap (Nicira extension, OVS 2.1+)**
- Bucket | Encapsulation | Purpose | Activity | Mechanism
  Removes innermost packet encapsulation (Ethernet, IP, NSH, GRE, Geneve). Syntax: `decap` or `decap(type:...)`. Reveals payload; used with NSH service chaining or generic encap/decap.

  Example: `actions=decap` removes NSH header; reveals inner packet.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: encap (Nicira extension, OVS 2.1+)**
- Bucket | Encapsulation | Purpose | Activity | Mechanism
  Adds packet encapsulation (NSH, Ethernet, IP). Syntax: `encap(type(args))` e.g., `encap(nsh(md_type=1,tlv(...)))`. Used for service chaining and tunneling. OVS 2.1+.

  Example: `actions=encap(nsh(md_type=1))` wraps packet in NSH header.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: controller (Nicira extension)**
- Bucket | Control | Purpose | Activity | Mechanism
  Sends packet to OpenFlow controller as PACKET_IN. Syntax: `controller` or `controller:max_len` or `controller(key=value,...)` with args: max_len, id (controller_id), reason (action,no_match,invalid_ttl), userdata. Extended with userdata for continuation-based programs (OVS 2.6+).

  Example: `actions=controller:65535` sends full packet; `actions=controller(reason=no_match,userdata=0x1234)`.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: note (Nicira extension)**
- Bucket | Annotation | Purpose | Activity | Mechanism
  Adds comment/metadata string to flow (no packet effect). Syntax: `note:text` or `note:hex`. Useful for flow annotations, debugging. OVS 1.8+.

  Example: `actions=output:1,note:hairpin-loop-prevention` annotates rule.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: sample (Nicira extension, OVS 2.5+)**
- Bucket | Monitoring | Purpose | Activity | Mechanism
  Probabilistic packet sampling (sFlow/NetFlow). Syntax: `sample(probability=P,actions=...,collector_set_id=...)`. Samples fraction P of packets and executes enclosed actions (e.g., output to sFlow agent). OVS 2.5+.

  Example: `actions=sample(probability=100,group=1)` samples 1-in-100 packets to sFlow group.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: exit (Nicira extension)**
- Bucket | Control | Purpose | Activity | Mechanism
  Halts pipeline immediately; executes action set at egress without further table processing. Syntax: `exit`. Similar to action set egress.

  Example: `actions=exit` stops pipeline; action set (from write_actions) executes.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: multipath (Nicira extension, OVS 1.11+)**
- Bucket | Load Balancing | Purpose | Activity | Mechanism
  Hash-based load balancing across N ports/buckets. Syntax: `multipath(fields,basis,algorithm,max_link,args)`. Algorithms: modulo_N, hash_threshold, symmetric_l3, symmetric_l3l4, symmetric_l4. Hashes selected fields and writes result to reg.

  Example: `actions=multipath(eth_src,0,hash_threshold,2,reg0)` load-balances across 2 ports, stores in reg0.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: bundle / bundle_load (Nicira extension, OVS 1.11+)**
- Bucket | Load Balancing | Purpose | Activity | Mechanism
  Similar to multipath; legacy alternatives. Syntax: `bundle(fields,basis,algorithm,max_link,members=[port1,port2,...])` or `bundle_load(fields,basis,algorithm,max_link,reg_dst,reg_off,reg_max)`. OVS 1.11+.

  Example: `actions=bundle(eth_src,0,hash_threshold,2,members=[1,2])` hashes to port 1 or 2.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: fin_timeout (Nicira extension, OVS 1.11+)**
- Bucket | Connection Tracking | Purpose | Activity | Mechanism
  Sets connection tracking timeout on TCP FIN. Syntax: `fin_timeout(idle_timeout=N,hard_timeout=N)`. Used in stateful rules to quickly expire after TCP close. OVS 1.11+.

  Example: `ct_state=+fin,actions=fin_timeout(idle_timeout=30,hard_timeout=300)` expires TCP conn 30sec after FIN.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: move (Nicira extension)**
- Bucket | Modification | Purpose | Activity | Mechanism
  Moves/copies bits from src field to dst field (bit-level granularity). Syntax: `move:src->dst` or `move(src[off:len],dst[off:len])`. Enables dynamic field population from registers.

  Example: `actions=move:reg0->ipv4_dst` copies reg0 to ipv4_dst; `actions=move:eth_src[0:24]->eth_dst[24:24]` copies 24-bit OUI.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: output:NXM (dynamic port)**
- Bucket | Forwarding | Purpose | Activity | Mechanism
  Outputs packet to port number stored in NXM field. Syntax: `output:NXM_NX_REG0[]` or `output:field`. Enables dynamic routing based on register/metadata.

  Example: `actions=output:NXM_NX_REG0[]` outputs to port in reg0; useful in multipath/bundle workflows.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: push:src (Nicira extension)**
- Bucket | Stack | Purpose | Activity | Mechanism
  Pushes field value onto OVS internal stack. Syntax: `push:field`. Stack used for temporary state during action execution. Paired with pop.

  Example: `actions=push:NXM_OF_IN_PORT[],load:0->NXM_OF_IN_PORT[],output:1,pop:NXM_OF_IN_PORT[]` swaps in_port temporarily.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html

**Action: pop:dst (Nicira extension)**
- Bucket | Stack | Purpose | Activity | Mechanism
  Pops value from stack into field. Syntax: `pop:field`. Restores prior value. Paired with push.

  Example: (see push example above) `pop:NXM_OF_IN_PORT[]` restores in_port.  
  Source: man7.org/linux/man-pages/man7/ovs-actions.7.html


### 2.3 Messages & state machine

**OFPT_HELLO (Type 0, OpenFlow 1.0+)**
- Bucket | Handshake | Purpose | Activity | Mechanism
  Version negotiation between controller and switch. Sent by both sides on TCP connect; versions field lists supported OpenFlow versions (bitmap: 1.0=0x01, 1.1=0x02, 1.2=0x04, 1.3=0x08, 1.4=0x10, 1.5=0x20). Switch/controller agree on highest common version; connection fails if no overlap.

  Example: Controller HELLO with versions 0x1E (1.1-1.5); switch HELLO with versions 0x04 (1.2); both use 1.2.  
  Source: OpenFlow Switch Specification 1.3

**OFPT_FEATURES_REQUEST (Type 5, OpenFlow 1.0+)**
- Bucket | Discovery | Purpose | Activity | Mechanism
  Controller requests switch capabilities (ports, tables, groups, meters, max_buffered_packets, etc.). No message body; switch responds with OFPT_FEATURES_REPLY listing all ports and capabilities. Typically sent after HELLO version agreement.

  Example: `ovs-ofctl show br0` sends FEATURES_REQUEST; receives port list and table count.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_FEATURES_REPLY (Type 6, OpenFlow 1.0+)**
- Bucket | Discovery | Purpose | Activity | Mechanism
  Switch response to FEATURES_REQUEST. Contains datapath_id (unique 64-bit switch ID), n_buffers (packet buffering), n_tables (number of flow tables), capabilities (FLOW_STATS, TABLE_STATS, PORT_STATS, GROUP_STATS, etc.), and port list with names, addresses, features.

  Example: Reply lists ports 1-4, datapath_id=0x0000000000000001, n_tables=254, capabilities=0x000000CF.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_PACKET_IN (Type 10, OpenFlow 1.0+)**
- Bucket | Event | Purpose | Activity | Mechanism
  Switch sends packet to controller when: (1) flow table miss and controller action configured, (2) explicit controller action, (3) invalid TTL in apply_actions. Contains packet body, in_port, reason (no_match/action/invalid_ttl), table_id, match fields (OXM), and optional userdata (Nicira extension). Allows controller to inspect/respond to exceptions.

  Example: Switch sends PACKET_IN when host on port 1 sends ARP for unknown IP; controller learns and installs flow.  
  Source: OpenFlow Switch Specification 1.0/1.3, openvswitch.org

**OFPT_PACKET_OUT (Type 13, OpenFlow 1.0+)**
- Bucket | Control | Purpose | Activity | Mechanism
  Controller sends packet to switch for immediate forwarding. Contains packet body, in_port (virtual ingress, often OFPP_CONTROLLER), and action list (output, set_field, etc.) to execute immediately. Used to respond to PACKET_IN or inject custom packets.

  Example: Controller responds to ARP PACKET_IN by sending ARP REPLY via PACKET_OUT with action=output:1.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_FLOW_MOD (Type 14, OpenFlow 1.0+)**
- Bucket | Configuration | Purpose | Activity | Mechanism
  Modifies flow table entries. Command: ADD (insert new), MODIFY (update existing, non-strict), MODIFY_STRICT (update exact match), DELETE (remove non-strict), DELETE_STRICT (remove exact match). Contains table_id, priority, match, instructions, timeout (idle/hard), flags (NO_PKT_COUNTS, NO_BYT_COUNTS, SEND_FLOW_REMOVED, RESET_COUNTS). Priority determines precedence (higher = checked first).

  Example: `ovs-ofctl add-flow br0 "table=0,priority=100,in_port=1,actions=output:2"` sends FLOW_MOD(ADD) with priority=100, table=0.  
  Source: OpenFlow Switch Specification 1.0/1.3, man7.org/linux/man-pages/man8/ovs-ofctl.8.html

**OFPT_BARRIER_REQUEST / OFPT_BARRIER_REPLY (Types 20/21, OpenFlow 1.0+)**
- Bucket | Synchronization | Purpose | Activity | Mechanism
  Request/reply pair for strict ordering guarantee. Controller sends BARRIER_REQUEST; switch processes all prior messages and responds with BARRIER_REPLY of matching xid. Ensures deterministic ordering of flow_mods, stats queries, etc.

  Example: Controller sends 3 FLOW_MOD messages then BARRIER_REQUEST; switch guarantees all flows applied before BARRIER_REPLY.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_ECHO_REQUEST / OFPT_ECHO_REPLY (Types 2/3, OpenFlow 1.0+)**
- Bucket | Liveness | Purpose | Activity | Mechanism
  Keep-alive heartbeat. Controller sends ECHO_REQUEST periodically; switch responds immediately with ECHO_REPLY (matching xid). If no response within timeout, controller assumes switch/connection dead and reconnects.

  Example: Controller sends ECHO_REQUEST every 5 seconds; 3 missed ECHOs trigger reconnection.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_MULTIPART_REQUEST (Type 18, OpenFlow 1.3+)**
- Bucket | Stats | Purpose | Activity | Mechanism
  Query switch state (flows, tables, ports, groups, meters). Type field specifies query: FLOW (matching flows), AGGREGATE (flow stats summary), TABLE (per-table info), PORT_STATS, GROUP, METER, METER_FEATURES, TABLE_FEATURES. Request includes match criteria and table_id; responses may fragment across multiple MULTIPART_REPLY messages.

  Example: MULTIPART_REQUEST(type=FLOW, table_id=0) queries table 0; MULTIPART_REQUEST(type=METER) queries meters.  
  Source: OpenFlow Switch Specification 1.3, man7.org/linux/man-pages/man8/ovs-ofctl.8.html

**OFPT_MULTIPART_REPLY (Type 19, OpenFlow 1.3+)**
- Bucket | Stats | Purpose | Activity | Mechanism
  Response to MULTIPART_REQUEST. Flags field: OFPMPF_REPLY_MORE (0x0001) indicates more replies follow. Multiple MULTIPART_REPLY messages assembled by controller using xid matching. Final reply has OFPMPF_REPLY_MORE=0.

  Example: 3 MULTIPART_REPLY(type=FLOW,flags=MORE) followed by MULTIPART_REPLY(type=FLOW,flags=0) for 100+ flows.  
  Source: OpenFlow Switch Specification 1.3

**OFPT_PORT_STATUS (Type 12, OpenFlow 1.0+)**
- Bucket | Event | Purpose | Activity | Mechanism
  Async notification when physical port state changes (up/down, add/remove). Reason: ADD (port appears), DELETE (port disappears), MODIFY (config/state change). Controller uses to update topology awareness. May be rate-limited by switch.

  Example: Switch sends PORT_STATUS(reason=MODIFY,port=1,state=LIVE_DOWN) when port 1 goes down; controller updates routing.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_FLOW_REMOVED (Type 11, OpenFlow 1.0+)**
- Bucket | Event | Purpose | Activity | Mechanism
  Async notification when flow entry removed (timeout, group delete, or explicitly via FLOW_MOD DELETE). Reason: IDLE_TIMEOUT, HARD_TIMEOUT, DELETE, GROUP_DELETE, METER_DELETE. Contains match, statistics (byte/packet count), duration (uptime), cookie (application identifier).

  Example: Switch sends FLOW_REMOVED(reason=IDLE_TIMEOUT) when flow inactive >300sec; controller recalculates routes if needed.  
  Source: OpenFlow Switch Specification 1.0/1.3

**OFPT_ROLE_REQUEST / OFPT_ROLE_REPLY (Types 24/25, OpenFlow 1.3+)**
- Bucket | Control | Purpose | Activity | Mechanism
  Controller role negotiation for redundancy. Roles: NOCHANGE, EQUAL (active, accept writes/reads), MASTER (exclusive writes, others become SLAVE), SLAVE (read-only). Used for controller failover; only MASTER/EQUAL controller can modify switch state. Generation_id (64-bit) prevents stale messages.

  Example: Primary controller sends ROLE_REQUEST(role=MASTER); secondary gets ROLE_REQUEST(role=SLAVE) and switches to read-only.  
  Source: OpenFlow Switch Specification 1.3

**OFPT_GROUP_MOD (Type 15, OpenFlow 1.2+)**
- Bucket | Configuration | Purpose | Activity | Mechanism
  Modifies group table entries. Command: ADD, MODIFY, DELETE. Contains group_id, type (all/select/indirect/fast_failover), buckets (list of actions and parameters per bucket). Failover buckets include watch_port/watch_group for health monitoring.

  Example: `ovs-ofctl add-group br0 "group_id=1,type=all,bucket=actions=output:1,bucket=actions=output:2"` sends GROUP_MOD(ADD).  
  Source: OpenFlow Switch Specification 1.2/1.3

**OFPT_METER_MOD (Type 29, OpenFlow 1.3+)**
- Bucket | QoS Configuration | Purpose | Activity | Mechanism
  Modifies meter table entries. Command: ADD, MODIFY, DELETE. Contains meter_id, flags (KBPS=rate in kilobits/sec, PKTPS=packets/sec, BURST=burst size, STATS), bands (type=drop/remark, rate, burst_size). Controls per-flow rate limiting.

  Example: `ovs-ofctl meter-mod br0 "meter_id=1,kbps,burst_size=1000,band=type=drop,rate=5000"` adds meter.  
  Source: OpenFlow Switch Specification 1.3

**OFPT_BUNDLE_OPEN / OFPT_BUNDLE_COMMIT / OFPT_BUNDLE_ADD_MESSAGE (Types 34/35/36, OpenFlow 1.4+)**
- Bucket | Transaction | Purpose | Activity | Mechanism
  Atomic flow modification transactions. BUNDLE_OPEN creates transaction context; BUNDLE_ADD_MESSAGE enqueues flow_mod/group_mod/meter_mod; BUNDLE_COMMIT applies all atomically (all-or-nothing). If any fails, entire bundle rolls back. Introduced OpenFlow 1.4 (OVS 2.4+). bundle_id (32-bit) identifies transaction.

  Example: Controller opens bundle, adds 10 flows, commits; switch applies all or none if error.  
  Source: OpenFlow Switch Specification 1.4, man7.org/linux/man-pages/man8/ovs-ofctl.8.html

**OFPT_REQUESTFORWARD (Type 32, OpenFlow 1.4+)**
- Bucket | Proxy | Purpose | Activity | Mechanism
  Auxiliary connection message relay (OpenFlow 1.4+). Allows controller to send messages via auxiliary connections; used for switch-to-switch message forwarding or controller discovery.

  Example: Switch forwards controller HELLO via REQUESTFORWARD on auxiliary connection to peer switch.  
  Source: OpenFlow Switch Specification 1.4

**OFPT_TABLE_STATUS (Type 30, OpenFlow 1.3+)**
- Bucket | Event | Purpose | Activity | Mechanism
  Async notification of table state changes (overflow, underflow, config changes). Reason: VACANCY_DOWN/UP (crossing vacancy threshold). Enables controller to monitor table pressure.

  Example: Switch sends TABLE_STATUS(reason=VACANCY_DOWN,table_id=0) when table 0 occupancy exceeds threshold.  
  Source: OpenFlow Switch Specification 1.3

**Connection State Machine: HELLO**
- Bucket | Protocol | Purpose | Activity | Mechanism
  Initial state after TCP/TLS establish. Both sides send OFPT_HELLO with supported versions. Highest common version negotiated; if no overlap, connection closes with error. All subsequent messages use negotiated version. Fails if no version agreement.

  Example: After TCP connect, controller sends HELLO(versions=0x1E); switch responds HELLO(versions=0x04); both use 1.2.  
  Source: OpenFlow Switch Specification 1.0/1.3

**Connection State Machine: FEATURES_REQUEST/REPLY**
- Bucket | Protocol | Purpose | Activity | Mechanism
  Follows HELLO. Controller requests switch capabilities/ports. Switch responds with datapath_id, port list, max_buffered_packets, n_tables, capabilities. Controller now has topology and resources.

  Example: Controller learns datapath_id=0x0000000000000001, ports={1,2,3,4}, n_tables=254.  
  Source: OpenFlow Switch Specification 1.0/1.3

**Connection State Machine: Steady State (ECHO keep-alive)**
- Bucket | Protocol | Purpose | Activity | Mechanism
  Stable operation. Controller and switch exchange ECHO_REQUEST/REPLY periodically (default 5-15 sec intervals) to detect connection loss. All FLOW_MOD, MULTIPART, PORT_STATUS, FLOW_REMOVED messages processed in steady state. If ECHO timeout occurs, connection drops and reconnect attempted.

  Example: Every 5 seconds, controller sends ECHO; if no ECHO_REPLY after 3 attempts (15 sec), reconnect.  
  Source: OpenFlow Switch Specification 1.0/1.3

**Auxiliary Connections (OpenFlow 1.3+)**
- Bucket | Protocol | Purpose | Activity | Mechanism
  Secondary TCP/TLS connections to same switch (datapath_id). All auxiliary connections share version negotiation from main connection. Used for: (1) parallel message transmission (avoid single connection bottleneck), (2) switch-to-switch forwarding (OFPT_REQUESTFORWARD), (3) role assignment (redundant controllers). Main connection remains primary.

  Example: Primary controller opens main connection; secondary controller opens auxiliary with same datapath_id, both can issue commands (with role constraints).  
  Source: OpenFlow Switch Specification 1.3

**OFPT_SET_ASYNC (Type 28, OpenFlow 1.4+)**
- Bucket | Control | Purpose | Activity | Mechanism
  Configures async notification behavior (PACKET_IN, PORT_STATUS, FLOW_REMOVED, TABLE_STATUS). Master vs Slave role can receive different notification masks. Controls which events are sent to controller and on which connection.

  Example: MASTER role receives all PACKET_IN; SLAVE role receives none (read-only controller gets no events).  
  Source: OpenFlow Switch Specification 1.4


### 2.4 Version differences (1.0 / 1.3 / 1.5)

**Single-Table vs Multi-Table Pipeline**
- Bucket | Architecture | Purpose | Activity | Mechanism
  OpenFlow 1.0: Single flow table (table 0 only), no goto_table, no other tables. Packets match once; if hit, execute action set immediately; if miss, drop or send to controller. Limited classification capability (simple forwarding only). OpenFlow 1.1+: Multi-table pipeline (254+ tables), goto_table instruction chains tables, metadata survives transitions, enables complex multi-stage processing (routing, ACL, QoS, stateful filtering).

  Example (OF 1.0): Single table with match=in_port,actions=output:port. (OF 1.3): table=0 match, goto_table:1; table=1 applies policies; table=2 applies QoS.  
  Source: OpenFlow Switch Specification 1.0 vs 1.3

**NXM vs OXM (Match Field Encoding)**
- Bucket | Encoding | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.1: Nicira eXtensible Match (NXM) uses type-length-value (TLV) format; each field has 16-bit class (NXM_OF=0, NXM_NX=1) and 8-bit type. OpenFlow 1.2+: OpenFlow eXtensible Match (OXM) standardized TLV format with 32-bit class (0x8000=OXM_OF, 0x0001=OXM_OF_PKT_REG, 0x8001=OXM_NX). OXM supports both standard and vendor extensions. NXM and OXM not interoperable in protocol (but OVS internally converts).

  Example (NXM): "NXM_OF_ETH_SRC[]=aa:bb:cc:dd:ee:ff"; (OXM): "OXM_OF_ETH_SRC[]=aa:bb:cc:dd:ee:ff" or shorthand "eth_src=aa:bb:cc:dd:ee:ff".  
  Source: OpenFlow Switch Specification 1.2, openvswitch.org

**Group Tables (OF 1.1+)**
- Bucket | Feature | Purpose | Activity | Mechanism
  OpenFlow 1.0: No group tables; multicast/load balancing requires duplicate flow entries (one per output port), wasteful. OpenFlow 1.1+: Group table (4 types: all, select, indirect, fast_failover) enables efficient multicast, load balancing, failover without flow explosion. Bucket-based actions replicate or hash-select. Introduced OF 1.1; enhanced with fast_failover in OF 1.2.

  Example (OF 1.0): 10 flows for 10 outputs; (OF 1.1): 1 group with 10 buckets, 10 flows reference group:1.  
  Source: OpenFlow Switch Specification 1.1/1.2/1.3

**Meters (OF 1.3+)**
- Bucket | QoS | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.2: No standard meter/rate-limit mechanism; rate limiting done via flow timeouts or external VLAN marking. OpenFlow 1.3+: Meter table with bands (drop, remark) applying per-packet rate limiting in kbps or pps with configurable burst. Meters referenced via meter instruction in flow. OpenFlow 1.4+: Meter features and additional band types.

  Example (OF 1.0): Static timeout idle=300; (OF 1.3): meter_id=1,kbps,rate=5000,band=type=drop.  
  Source: OpenFlow Switch Specification 1.3

**Bundles (OF 1.4+)**
- Bucket | Transaction | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.3: Flow_mod commands executed individually; partial failures leave switch in intermediate state. OpenFlow 1.4+: BUNDLE_OPEN/COMMIT/ADD_MESSAGE enable atomic multi-message transactions. All flow_mods in bundle applied atomically or entire bundle rolled back if any fail. Prevents split-brain during policy updates.

  Example (OF 1.3): 10 flow_mods; if 5th fails, flows 1-4 applied (split state). (OF 1.4): Same in bundle; if 5th fails, none applied (consistent).  
  Source: OpenFlow Switch Specification 1.4

**Egress Tables (OF 1.5+)**
- Bucket | Pipeline | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.4: Single ingress pipeline (table 0-254), action set executes at egress. OpenFlow 1.5+: Optional egress pipeline (table 0-254 again, conceptually after action set). Enables per-port output processing (e.g., remove VLAN tag when leaving certain ports without affecting other ports in same flow).

  Example (OF 1.5): Ingress tables add VLAN tag; egress table for port 1 removes it.  
  Source: OpenFlow Switch Specification 1.5

**copy_field (OF 1.5+)**
- Bucket | Action | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.4: move action (OVS extension) copies field bits; no OF standard. OpenFlow 1.5+: copy_field standardized with bit-offset support. Syntax: copy_field(src_offset:src_field, dst_offset:dst_field, nbits). Enables dynamic field population with sub-field granularity.

  Example (OF 1.5): copy_field(0:ipv4_src,0:reg0,32) copies ipv4_src to reg0.  
  Source: OpenFlow Switch Specification 1.5, man7.org/linux/man-pages/man7/ovs-actions.7.html

**Packet Type Aware Pipeline (OF 1.5+)**
- Bucket | Pipeline | Purpose | Activity | Mechanism
  OpenFlow 1.0-1.4: Assumes Ethernet encapsulation in all tables. OpenFlow 1.5+: packet_type field enables processing non-Ethernet encapsulations (NSH, bare IP, etc.) in pipeline. Allows service chaining and protocol-agnostic encapsulation handling.

  Example (OF 1.5): packet_type=1.2 (IPv4 bare), can match on ipv4_src without eth_type prerequisite.  
  Source: OpenFlow Switch Specification 1.5

**Version Support Summary**
- Bucket | Reference | Purpose | Activity | Mechanism
  OF 1.0: Single table, NXM/legacy actions, basic forwarding (port/flood/drop), PACKET_IN/PACKET_OUT, FLOW_MOD, no multi-stage filtering. OF 1.3: Multi-table pipeline (254 tables), goto_table, metadata, OXM fields, groups (all/select/indirect), meters, multipart queries, auxiliary connections, ROLE negotiation. OF 1.5: Egress tables, copy_field, packet_type-aware pipeline, additional actions/fields. OVS maintains backward compatibility and extends with Nicira NXM features.

  Example (OF 1.0 → 1.3 upgrade): Old flows must be rewritten (table ids added, OXM syntax); OF 1.3 switch accepts both.  
  Source: OpenFlow Switch Specification 1.0/1.3/1.5, openvswitch.org

---

## 3. OVN

### 3.1 Architecture & daemons

- **Daemon: ovn-northd** | Central Control Plane | Translates northbound logical config to southbound datapath flows | Active-standby leadership with OVSDB locking | Source: ovn-northd(8)
  - Leadership managed via SB_Global lock; multiple instances automatically elect one active daemon. When active instance fails, standby automatically takes over.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Northbound DB Management** | ovn-northd Configuration | Connects to OVN_Northbound via --ovnnb-db flag | Monitors all changes from NB DB | Source: ovn-northd(8)
  - Default database path is unix:@RUNDIR@/ovnnb_db.sock; can be overridden via OVN_NB_DB environment variable or --ovnnb-db option.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Southbound DB Management** | ovn-northd Datapath Publishing | Connects to OVN_Southbound via --ovnsb-db flag | Writes Logical_Flow, Multicast_Group, and other control tables | Source: ovn-northd(8)
  - Publishes logical flows to SB database for consumption by ovn-controller instances; default unix:@RUNDIR@/ovnsb_db.sock.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Daemon: ovn-controller** | Per-chassis Local Control Plane | Translates southbound logical flows to OpenFlow | Direct OVS integration via OpenFlow | Source: ovn-controller(8)
  - Runs on every hypervisor and software gateway; connects to OVN_Southbound DB and local OVS database; drives OpenFlow to ovs-vswitchd.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Chassis Configuration** | ovn-controller Local Identity | Sets via external_ids:system-id in Open_vSwitch table | Used in Chassis table registration | Source: ovn-controller(8)
  - Can be set via --system-id-override file or -n command-line option; precedence: CLI > file > OVS database.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Integration Bridge** | ovn-controller OVS Bridge | Default br-int, configurable via external_ids:ovn-bridge | Auto-created if missing on startup | Source: ovn-controller(8)
  - When multiple controllers run on same host, use external_ids:ovn-bridge-CHASSIS_NAME for unique bridges per controller.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Daemon: ovn-controller-vtep** | VTEP Gateway Controller | Manages hardware VTEP gateways to OVN | Interfaces with VTEP schema for port bindings | Source: OVN Architecture
  - Specializes in VTEP (VXLAN Tunnel Endpoint) hardware gateway integration; translates between OVN logical model and VTEP management.
  - SOURCE: ovn.org documentation

- **Daemon: ovn-ic** | Interconnection Control | Manages OVN deployments across regions/clouds | Coordinates IC_Northbound and IC_Southbound DBs | Source: OVN Inter-Connect Architecture
  - Enables federated OVN deployments; synchronizes logical routers and port information across OVN instances.
  - SOURCE: ovn.org documentation

- **Daemon: ovn-ic-northd** | Interconnection Central Control | Translates IC_Northbound to IC_Southbound | Coordinates route learning | Source: OVN Inter-Connect
  - Counterpart to ovn-northd for interconnection scenarios; publishes AvailabilityZone routes and traffic redirection.
  - SOURCE: ovn.org documentation

- **OVSDB Server Roles** | Persistent Storage | Three databases: OVN_Northbound, OVN_Southbound, OVN_IC (optional) | RAFT clustering for HA | Source: OVSDB Architecture
  - ovsdb-server instances can be standalone, replicated (active/passive), or clustered (RAFT); handles schema management and persistence.
  - SOURCE: ovn.org documentation

- **RAFT Clustering** | High Availability | Multi-server consensus for OVN databases | Leader-based writes, follower reads | Source: OVSDB Clustering
  - When ovsdb-server runs in RAFT cluster mode, only leader accepts writes; followers accept reads (subject to consistency policies).
  - SOURCE: ovn.org documentation

- **Relay Mode (ovsdb-server)** | Southbound DB Scale-Out | ovsdb-server in relay mode caches SB for many ovn-controller connections | Reduces load on primary SB server | Source: OVN Scale-Out Documentation
  - Relay servers proxy southbound database updates; reduces primary server connection count and improves overall system scalability.
  - SOURCE: ovn.org documentation

- **Inactivity Probes** | Connection Health Monitoring | Configurable per connection via --inactivity-probe or options | Detects dead connections | Source: OVN Database Options
  - ovn-controller uses external_ids:ovn-remote-probe-interval (milliseconds, min 1000ms if nonzero); disables with value 0.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Northd Probe Interval** | Leadership Heartbeat | northd_probe_interval in NB_Global controls leadership election timeout | HA failover timing | Source: OVN High Availability
  - Controls how quickly standby ovn-northd detects active instance failure and takes over OVSDB lock.
  - SOURCE: ovn.org documentation

- **Leader Election** | Distributed Consensus | Based on OVSDB lock acquisition in SB_Global | Active ovn-northd holds lock | Source: ovn-northd(8)
  - STATUS command returns 'active' (lock held), 'standby' (lock not held), or 'paused' (paused via ovn-appctl).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Daemon Threading** | ovn-northd Parallelization | --n-threads N (2-256 range) enables multi-threaded flow compilation | CPU scaling | Source: ovn-northd(8)
  - Controlled via -n-threads CLI flag or set-n-threads/get-n-threads ovn-appctl commands; defaults to 1 (single-threaded).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

### 3.2 Northbound / Southbound schemas

- **NB_Global Table** | Northbound Configuration | Persistent configuration for entire northbound database | Leader election state | Source: ovn-nb(5)
  - Contains global options, northbound configuration metadata, optionally northd_probe_interval for HA tuning.
  - SOURCE: ovn.org documentation

- **Logical_Switch Table (NB)** | Virtual L2 Domain | Defines logical layer 2 networks | Port binding target | Source: ovn-nb(5)
  - Each logical switch has name, ports (via Logical_Switch_Port), and optional DHCP/DNS configuration; multicast relay per switch.
  - SOURCE: ovn.org documentation

- **Logical_Switch_Port Table (NB)** | L2 Port Configuration | Parent/tag VLAN tagging support | Multiple port types | Source: ovn-nb(5)
  - Port types: router (to logical router), localport (local to chassis), localnet (physical network), l2gateway (bridged), vtep (hardware gateway), external (for external resources), virtual (redundancy), remote (inter-connect). Dynamic_addresses for DHCP/SLAAC allocation.
  - SOURCE: ovn.org documentation

- **Port Security (NB)** | Access Control | port_security column on Logical_Switch_Port | Per-port MAC/IP allowlist | Source: ovn-nb(5)
  - Ingress table 0 evaluates port security via check_in_port_sec() action; REGBIT_PORT_SEC_DROP register tracks failures.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **QoS Configuration (NB)** | Traffic Rate Limiting | qos_max_rate and qos_burst on Logical_Switch_Port | Per-port bandwidth limits | Source: ovn-nb(5)
  - ovn-controller installs OpenFlow queue configurations via set_queue() actions based on port QoS parameters.
  - SOURCE: ovn.org documentation

- **Requested Chassis (NB)** | Port Binding Hint | options:requested-chassis on Logical_Switch_Port | Preference for port location | Source: ovn-nb(5)
  - If set, ovn-controller prefers to bind this port to specified chassis if available; soft constraint (can be overridden).
  - SOURCE: ovn.org documentation

- **Reside-on-Redirect-Chassis (NB)** | Distributed Gateway Routing | options:reside-on-redirect-chassis on Logical_Router_Port | Gateway port location | Source: ovn-nb(5)
  - When true, allows distributed NAT and L3 gateway redirection across multiple chassis via cr- (chassisredirect) ports.
  - SOURCE: ovn.org documentation

- **Logical_Router Table (NB)** | Virtual L3 Device | Logical routing domain | Port aggregation and routing policies | Source: ovn-nb(5)
  - Contains logical router ports, static routes, NAT rules, load balancers, and policies; supports both centralized and distributed modes.
  - SOURCE: ovn.org documentation

- **Logical_Router_Port Table (NB)** | L3 Port Configuration | Peer reference for intra-OVN connectivity | HA and gateway configuration | Source: ovn-nb(5)
  - peer field creates logical patch port to another LR or LS; gateway_chassis and ha_chassis_group for redundancy; supports options:redirect-chassis for gateway redirection modes.
  - SOURCE: ovn.org documentation

- **Logical_Router_Static_Route (NB)** | Static Routing | nexthop and output_port fields | ECMP support | Source: ovn-nb(5)
  - Routes with same route_table and match criteria are treated as ECMP; LR uses load-balancing across equal-cost paths.
  - SOURCE: ovn.org documentation

- **Logical_Router_Policy (NB)** | Policy-Based Routing | Priority, match, action, nexthop columns | Per-route classification | Source: ovn-nb(5)
  - Matches flows against ACL-like expressions; actions direct traffic to specific nexthop or mark with pkt_mark for classification.
  - SOURCE: ovn.org documentation

- **NAT Table (NB)** | Network Address Translation | snat/dnat/dnat_and_snat types | Stateful translation | Source: ovn-nb(5)
  - allowed_ext_ips and exempted_ext_ips refine which external IPs are used; options:stateless disables connection tracking for fast-path NAT.
  - SOURCE: ovn.org documentation

- **Load_Balancer Table (NB)** | Service Load Balancing | VIP-to-backend mapping via vips column | Multiple protocols | Source: ovn-nb(5)
  - Supports TCP, UDP, SCTP; ip_port_mappings and selection_fields for consistent hashing; options:hairpin_snat_ip for hairpin return traffic.
  - SOURCE: ovn.org documentation

- **Load_Balancer_Group (NB)** | LB Aggregation | Combines multiple Load_Balancer entries | Applied to logical routers | Source: ovn-nb(5)
  - Allows LBs to be managed as unit; referenced by Logical_Router for uniform LB policy application.
  - SOURCE: ovn.org documentation

- **Load_Balancer_Health_Check (NB)** | LB Health Probing | Health status per backend | Active monitoring | Source: ovn-nb(5)
  - ovn-controller or external monitor checks backend status via HTTP/TCP probe; failed backends removed from forwarding.
  - SOURCE: ovn.org documentation

- **Address_Set Table (NB)** | Named MAC/IP Groups | Dynamic set membership | ACL/firewall rule targets | Source: ovn-nb(5)
  - Defines address_set with multiple addresses; used in ACL match expressions as $set_name for convenience and manageability.
  - SOURCE: ovn.org documentation

- **Port_Group Table (NB)** | Named Port Collections | Aggregates logical ports | ACL/policy enforcement | Source: ovn-nb(5)
  - Groups ports by name; used in ACL match expressions (inport and outport) as $pg_name; simplifies multi-port policy.
  - SOURCE: ovn.org documentation

- **ACL Table (NB)** | Firewall Policy | Direction (from-lport/to-lport), action, priority, match | Stateful inspection | Source: ovn-nb(5)
  - Actions: allow, allow-related (track connections), allow-stateless (skip tracking), drop, reject (send reset); log/severity for audit; sample_new/sample_est for telemetry; tier for grouping.
  - SOURCE: ovn.org documentation

- **Meter Table (NB)** | Rate Limiting | Bandwidth/packet-rate metering | Per-flow or per-table limits | Source: ovn-nb(5)
  - Meter_Band entries define rate (kbps) and burst; referenced by ACL or Logical_Flow for traffic shaping.
  - SOURCE: ovn.org documentation

- **QoS Table (NB)** | Quality of Service | Defines QoS policy per logical port | Rate, burst, priority | Source: ovn-nb(5)
  - Logical_Switch_Port can reference QoS entry for detailed traffic management; ovn-controller maps to OVS queue configuration.
  - SOURCE: ovn.org documentation

- **DHCP_Options Table (NB)** | DHCP Lease Configuration | Per-logical-switch DHCP parameters | Lease time, DNS, gateway | Source: ovn-nb(5)
  - Logical_Switch can point to DHCP_Options UUID; ovn-controller generates DHCP replies on switch ingress for VMs.
  - SOURCE: ovn.org documentation

- **Mirror Table (NB)** | Port Mirroring | Destination port for traffic copy | Egress/ingress/both selection | Source: ovn-nb(5)
  - Logical_Switch_Port can be mirroring source; packets copied to mirror_port in same LS for traffic analysis.
  - SOURCE: ovn.org documentation

- **Mirror_Rule (NB)** | Mirror Filtering | ACL-like match for mirror traffic | Per-rule enable/disable | Source: ovn-nb(5)
  - Allows selective mirroring based on packet fields; combined with Mirror configuration for granular traffic duplication.
  - SOURCE: ovn.org documentation

- **Forwarding_Group (NB)** | ECMP Redundancy | Defines failover ports for traffic | Liveness tracking | Source: ovn-nb(5)
  - Used with liveness checks to determine which ports in group are active; traffic redirected to healthy members.
  - SOURCE: ovn.org documentation

- **BFD Table (NB)** | Bidirectional Forwarding Detection | Health monitoring protocol | Sub-second failure detection | Source: ovn-nb(5)
  - Logical_Router_Port can enable BFD for gateway/HA monitoring; ovn-controller drives BFD via OVS BFD module.
  - SOURCE: ovn.org documentation

- **HA_Chassis Table (NB)** | Redundancy Configuration | Defines active/backup chassis | Ordered list of candidates | Source: ovn-nb(5)
  - Logical_Router_Port references HA_Chassis_Group; ovn-northd creates cr- (chassis redirect) port on active, routes via it.
  - SOURCE: ovn.org documentation

- **HA_Chassis_Group (NB)** | Grouped HA Chassis | Aggregates HA_Chassis entries | Reference by LRP | Source: ovn-nb(5)
  - Multiple LRPs can share same HA_Chassis_Group; priority field determines election order when active chassis fails.
  - SOURCE: ovn.org documentation

- **SB_Global Table** | Southbound Global State | Version tracking, chassis status | Leader election lock | Source: ovn-sb(5)
  - Stores nb_cfg (generation number of NB updates) for wait-for-update semantics; contains Connections for remote management.
  - SOURCE: ovn.org documentation

- **Chassis Table (SB)** | Datapath Binding | Physical or software gateway location | Encapsulation methods | Source: ovn-sb(5)
  - Each chassis row created by ovn-controller with: name (system-id), hostname, encaps (list of Encap references), other_config with bridge-mappings, ct-zone-limit.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Chassis_Private Table (SB)** | Per-Chassis State | Operational metadata | Not exposed to northbound | Source: ovn-sb(5)
  - Stores internal state per chassis; updated by ovn-controller and ovn-northd for operational coordination.
  - SOURCE: ovn.org documentation

- **Encap Table (SB)** | Tunnel Configuration | Type (geneve/vxlan/stt), ip, options | Tunnel metadata | Source: ovn-sb(5)
  - Each Chassis row references one or more Encap entries; geneve allows TLV metadata, vxlan limited; stt deprecated.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Datapath_Binding Table (SB)** | Logical Network Identity | Maps each LS/LR to tunnel_key | Flow context | Source: ovn-sb(5)
  - tunnel_key uniquely identifies logical datapath; used in OVN tunnel metadata (outer headers) for packet classification.
  - SOURCE: ovn.org documentation

- **Port_Binding Table (SB)** | Port Location | Binds logical port to chassis | Multiple port types | Source: ovn-sb(5)
  - chassis field set by ovn-controller when port becomes resident; tunnel_key identifies port within datapath; up flag indicates operational status.
  - SOURCE: ovn.org documentation

- **Port Binding Types (SB)** | Port Classification | VIF, container, patch, router, localnet, vtep, l3gateway, l2gateway, chassisredirect, virtual, external, remote | Type-specific behavior | Source: ovn-sb(5)
  - Different types trigger different datapath handling; patch ports connect two datapaths; chassisredirect for distributed gateways.
  - SOURCE: ovn.org documentation

- **Logical_Flow Table (SB)** | Datapath Program | Pipeline (ingress/egress), table_id, priority, match, actions | Executed per-packet | Source: ovn-sb(5)
  - Generated by ovn-northd; consumed by ovn-controller to create OpenFlow flows; hash field enables fast lookup.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Logical Flow Pipeline** | Ingress/Egress Stages | Standard table sequence per datapath type | Ordered processing | Source: ovn-architecture(7)
  - Ingress: LS_IN_PORT_SEC_L2 .. LS_IN_L2_LKUP; Egress: LS_OUT_*; LR_IN_* and LR_OUT_* for routers; tables numbered 0-33.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Multicast_Group Table (SB)** | BUM Flooding | Defines membership for unknown unicast/broadcast/multicast | Per-datapath groups | Source: ovn-sb(5)
  - ovn-northd creates multicast groups per LS; ovn-controller installs group actions in OpenFlow for replication.
  - SOURCE: ovn.org documentation

- **MAC_Binding Table (SB)** | ARP/ND Learning | Learned MAC-to-IP mappings | Generated by put_arp/put_nd actions | Source: ovn-sb(5)
  - Populated by ovn-controller ARP/ND learning; persists across restarts; used for traffic optimization.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **DNS Table (SB)** | DNS Responses | Mapping of DNS names to IPs | Per-datapath lookup table | Source: ovn-sb(5)
  - Logical_Switch can reference DNS entries; ovn-controller generates DNS replies on ingress for name resolution.
  - SOURCE: ovn.org documentation

- **RBAC_Role & RBAC_Permission (SB)** | Access Control | Role-based database access | Server-enforced | Source: ovn-sb(5)
  - Defines which roles can read/write which tables; enforced by ovsdb-server for client isolation.
  - SOURCE: ovn.org documentation

- **IGMP_Group Table (SB)** | Multicast Group Membership | IGMP snooping data | Per-datapath tracking | Source: ovn-sb(5)
  - Tracks which ports are members of multicast groups; used by multicast replication logic.
  - SOURCE: ovn.org documentation

- **Controller_Event Table (SB)** | Async Events | Fault/status notifications | For external monitoring | Source: ovn-sb(5)
  - ovn-controller writes event records for external consumption (e.g., health checks, failover notifications).
  - SOURCE: ovn.org documentation

- **Service_Monitor Table (SB)** | Health Status | LB backend health state | Per-service tracking | Source: ovn-sb(5)
  - Service_Monitor entries track health of each LB backend; updated by health check probes.
  - SOURCE: ovn.org documentation

- **Load_Balancer (SB)** | Resolved LB State | Datapath-specific LB configuration | Per-datapath instantiation | Source: ovn-sb(5)
  - SB Load_Balancer derived from NB Load_Balancer; includes resolved IP addresses and port mappings per datapath.
  - SOURCE: ovn.org documentation

- **Static_MAC_Binding (SB)** | Permanent ARP Entry | Administrator-configured MAC-IP binding | Overrides learned entries | Source: ovn-sb(5)
  - Can be manually created to pin specific MAC addresses to IPs; useful for static gateways or reserved addresses.
  - SOURCE: ovn.org documentation

- **FDB Table (SB)** | Forwarding Database | MAC-to-port mappings for L2 learning | Operational state | Source: ovn-sb(5)
  - Learned from datapath operations; used by L2 lookup stage to forward unicast frames within logical switch.
  - SOURCE: ovn.org documentation

- **Logical_DP_Group (SB)** | Datapath Set | Groups datapaths for multi-cast delivery | Logical_Flow optimization | Source: ovn-sb(5)
  - Used to efficiently represent flows that apply to multiple datapaths; reduces Logical_Flow table size.
  - SOURCE: ovn.org documentation

- **IP_Multicast (SB)** | IP Multicast Config | Per-datapath multicast forwarding settings | Replication mode, relay | Source: ovn-sb(5)
  - Configures how IP multicast traffic (224.0.0.0/4) is forwarded; mrouter ports, multicast relay options.
  - SOURCE: ovn.org documentation

### 3.3 Logical pipeline & datapath binding

- **Ingress vs Egress Pipeline** | Two-stage Processing | Separate pipeline stages for RX and TX | Stateful rule ordering | Source: ovn-architecture(7)
  - Ingress (P_IN) processes on port entry; egress (P_OUT) on port exit; match evaluation and actions depend on pipeline stage.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Logical Datapath Binding** | Flow Context Identity | tunnel_key maps each LS/LR to unique identifier | OVN tunnel encapsulation | Source: ovn-sb(5)
  - Tunnel outer packet carries datapath ID in metadata (geneve TLV or VXLAN VNI); ovn-controller uses to steer flows to correct datapath.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Tunnel Key Allocation** | Unique Identification | Per-logical-switch and per-logical-router unique tunnel_key | Global scope | Source: ovn-architecture(7)
  - Local keys (1 to ~16M), global keys (~16M to 24M) for distributed features; VXLAN uses 12-bit key space.
  - SOURCE: ovn-util.h

- **Logical Port Tunnel Key** | Port Identity in Tunnel | MLF (metadata lookup field) encodes source-chassis and logical-port | Tunnel metadata | Source: OVN Tunnel Specification
  - Outer tunnel metadata includes source chassis ID and source port ID; enables reverse classification for learning/response.
  - SOURCE: ovn.org documentation

- **Standard Switch Table Sequence** | Ingress Pipeline | LS_IN_PORT_SEC_L2, LS_IN_PORT_SEC_IP, LS_IN_LOOKUP, LS_IN_DHCP_OPTIONS, LS_IN_L2_LKUP | Ordered stages | Source: ovn-northd(8)
  - Ingress: port security -> ACLs -> DHCP -> L2 lookup. Each stage has fixed table_id; ovn-northd populates Logical_Flow per stage.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Standard Router Table Sequence** | Egress Pipeline | LR_IN_ADMISSION, LR_IN_IP_ROUTING, LR_IN_ARP_RESOLVE, LR_IN_GW_REDIRECT, LR_OUT_DELIVERY | Ordered stages | Source: ovn-northd(8)
  - Router ingress: admission -> IP routing -> ARP -> gateway redirect. Egress: delivery (to physical port or tunnel). Each with fixed table_id.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **Chassis Redirect Port (cr-*)** | Distributed Gateway | Special port type for gateway redundancy | Per-LR-port in distributed mode | Source: ovn-architecture(7)
  - ovn-northd creates cr-<lrp_name> port per distributed logical router port; bound to active chassis; flows via cr- enable stateless NAT/routing.
  - SOURCE: ovn.org documentation

- **VTEP Gateway Integration** | Hardware Gateway Bridging | VTEP encapsulation for HW appliances | Logical port type: vtep | Source: ovn-architecture(7)
  - ovn-controller-vtep binds VTEP port to hardware gateway; uses VXLAN for connectivity; MAC learning via VTEP bindings.
  - SOURCE: ovn.org documentation

- **Geneve TLV Encapsulation** | Metadata Carriage | TLV option 0x0102 for OVN metadata | Flexible encoding | Source: OVN Tunnel Spec
  - Geneve outer header carries 24-bit datapath key, source port, and flags in TLV; allows MLF (metadata lookup field) encoding.
  - SOURCE: ovn.org documentation

- **Encapsulation Precedence** | Tunnel Type Selection | geneve preferred, vxlan fallback, stt deprecated | Per-chassis capability | Source: ovn-controller(8)
  - When tunnel created between chassis, ovn-controller selects type based on Encap availability; geneve offers best performance.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Distributed Gateway Routing** | Stateless L3 GW | Gateway port on multiple chassis, NAT at source | ECMP-friendly | Source: ovn-architecture(7)
  - options:reside-on-redirect-chassis on LRP enables distributed mode; cr- port created on each chassis; traffic flow avoids centralized gateway bottleneck.
  - SOURCE: ovn.org documentation

- **Distributed NAT** | Per-Chassis Translation | NAT applied at source chassis for egress | Stateless path | Source: ovn-architecture(7)
  - Distributed NAT via external logical port; each chassis can perform NAT without central gateway; reduces latency.
  - SOURCE: ovn.org documentation

- **DVR-style Logical Patches** | Inter-datapath Connectivity | Logical patch ports connect LS-to-LR and LR-to-LR | Same-node forwarding | Source: ovn-architecture(7)
  - Peer field on LR_Port creates logical patch; traffic between connected datapaths stays on local ovn-controller until forwarding decision.
  - SOURCE: ovn.org documentation

- **MLF Local-Only Flag** | Traffic Steering | MLF_LOCAL_ONLY prevents inter-chassis tunneling | Same-chassis delivery | Source: OVN Tunnel Specification
  - Set by ovn-controller for local ARP learning, local DHCP responses; packets not tunneled if source and destination on same chassis.
  - SOURCE: ovn.org documentation

- **MLF Tunnel Metadata Encoding** | Packet Context Encoding | 24-bit datapath | 16-bit source port | Flags for local-only, etc. | Source: ovn-tunnel-spec
  - OVN encodes logical port and datapath into geneve TLV; allows reverse lookup for stateful inspection and connection tracking.
  - SOURCE: ovn.org documentation

- **OVN internal OVS register conventions** — Bucket: OVN | Context: OpenFlow flows generated by `ovn-controller` | Purpose: OVN reuses OVS `reg0`–`reg15` and `xreg0`–`xreg7` for pipeline-state variables; understanding the mapping is essential when correlating `ovs-ofctl dump-flows` output with OVN logical flows | Activity: debugging, flow correlation | Mechanism: conventions are defined in `lib/ovn-parallel-hdr.h` and `controller/lflow.c` in the OVN source tree.
  - Key register assignments (representative; exact offsets depend on OVN version):
    - `reg0` — scratch / general-purpose (e.g. NAT match state, ECMP selection result).
    - `reg1` — scratch / ECMP next-hop result, sometimes holds IPv4 address during ARP resolve.
    - `reg4`–`reg5` — logical flow registers for IPv4/IPv6 source address during SNAT.
    - `reg13` — `ct_zone` for the ingress port (written by port-security stage, read by ct() action).
    - `reg14` — `inport` tunnel key (16-bit logical port tunnel key of the ingress port).
    - `reg15` — `outport` tunnel key (16-bit logical port tunnel key of the egress port).
    - `xxreg0` (128-bit) — IPv6 address scratch register for ND/NA processing.
  - REGBIT conventions (bit-flag registers): OVN sets individual bits inside `reg0` for boolean pipeline flags, e.g.:
    - `REGBIT_PORT_SEC_DROP` (bit 0 of `reg0`) — set when port-security drops packet.
    - `REGBIT_ACL_HINT_ALLOW_NEW` (bit 1) — ACL allow-new hint for connection tracking.
    - `REGBIT_CONNTRACK_COMMIT` (bit 2) — instructs CT commit stage.
    - `REGBIT_SKIP_LOOKUP` (bit 7) — skip L2 lookup (e.g. after ARP reply injection).
  - Example: `ovs-ofctl dump-flows br-int table=44 | grep reg15` shows outport register use in egress delivery.
  - Source: https://github.com/ovn-org/ovn/blob/main/lib/ovn-parallel-hdr.h (OVN source); https://man7.org/linux/man-pages/man7/ovs-fields.7.html

- **OVN logical port pipeline table IDs** — Bucket: OVN | Context: OpenFlow table numbering on `br-int` | Purpose: map logical pipeline stages to physical OpenFlow table numbers so `ovs-ofctl dump-flows` output is readable | Activity: debugging, flow correlation | Mechanism: `ovn-controller` assigns fixed table IDs per pipeline stage; the mapping is stable within an OVN major version.
  - Representative ingress table sequence (LS ingress pipeline, tables 0–15):
    - Table 0: `LS_IN_PORT_SEC_L2` — inport port-security (L2 MAC check).
    - Table 1: `LS_IN_PORT_SEC_IP` — inport port-security (IP check).
    - Table 2: `LS_IN_PORT_SEC_ND` — ND/ARP port-security.
    - Table 3: `LS_IN_PRE_ACL` — pre-ACL stateful connector.
    - Table 4: `LS_IN_PRE_LB` — pre-load-balancer conntrack entry.
    - Table 5: `LS_IN_PRE_STATEFUL` — stateful pre-processing.
    - Table 6: `LS_IN_ACL_HINT` — ACL hint for allow/drop determination.
    - Table 7: `LS_IN_ACL_EVAL` — ACL evaluation (match ACLs).
    - Table 8: `LS_IN_ACL_ACTION` — ACL action execution (drop/allow/reject).
    - Table 9: `LS_IN_QOS_MARK` — QoS DSCP mark.
    - Table 10: `LS_IN_QOS_METER` — QoS rate-limit metering.
    - Table 11: `LS_IN_LB_AFF_CHECK` — LB affinity check.
    - Table 12: `LS_IN_LB` — load balancer DNAT.
    - Table 13: `LS_IN_LB_AFF_LEARN` — LB affinity learning.
    - Table 14: `LS_IN_PRE_HAIRPIN` — pre-hairpin.
    - Table 15: `LS_IN_NAT_HAIRPIN` — hairpin NAT.
    - Table 16: `LS_IN_HAIRPIN` — hairpin delivery.
    - Table 17: `LS_IN_ACL_AFTER_LB_EVAL` — post-LB ACL.
    - Table 18: `LS_IN_ACL_AFTER_LB_ACTION` — post-LB ACL action.
    - Table 19: `LS_IN_STATEFUL` — stateful commit.
    - Table 20: `LS_IN_ARP_ND_RSP` — ARP/ND responder.
    - Table 21: `LS_IN_DHCP_OPTIONS` — DHCP option construction.
    - Table 22: `LS_IN_DHCP_RESPONSE` — DHCP reply generation.
    - Table 23: `LS_IN_DNS_LOOKUP` — DNS name lookup.
    - Table 24: `LS_IN_DNS_RESPONSE` — DNS reply generation.
    - Table 25: `LS_IN_EXTERNAL_PORT` — external port handling.
    - Table 26: `LS_IN_L2_LKUP` — L2 unicast/multicast lookup (final forwarding decision).
    - Table 27: `LS_IN_L2_UNKNOWN` — unknown unicast flooding.
  - Egress LS pipeline (tables 32+) mirrors the ingress with `LS_OUT_*` stages; LR ingress and egress pipeline occupies another block.
  - Example: `ovs-ofctl dump-flows br-int table=26` shows the L2 forwarding decisions for all logical switches.
  - Source: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml (section "Logical Switch Ingress Table")

- **OVN logical port pipeline table IDs — LS_OUT stages** — Bucket: OVN | Context: OpenFlow table numbering on `br-int` for LS egress pipeline | Purpose: map LS egress logical stages to OpenFlow table numbers for reading `ovs-ofctl dump-flows br-int` output | Activity: debugging, ACL egress verification | Mechanism: `ovn-controller` assigns these table IDs per the OVN major version; the block starts after the LS ingress block (~table 32).
  - Representative egress table sequence (LS egress pipeline, tables 32–44 approximately):
    - Table 32: `LS_OUT_PRE_ACL` — egress pre-ACL stateful connector (same purpose as ingress pre-ACL but for departing packets).
    - Table 33: `LS_OUT_PRE_LB` — egress pre-load-balancer.
    - Table 34: `LS_OUT_PRE_STATEFUL` — egress stateful pre-processing.
    - Table 35: `LS_OUT_ACL_HINT` — egress ACL hint register.
    - Table 36: `LS_OUT_ACL_EVAL` — egress ACL evaluation (match rules applied to departing traffic).
    - Table 37: `LS_OUT_ACL_ACTION` — egress ACL action (drop / allow / reject outgoing packet).
    - Table 38: `LS_OUT_QOS_MARK` — egress QoS DSCP mark.
    - Table 39: `LS_OUT_QOS_METER` — egress QoS rate metering.
    - Table 40: `LS_OUT_STATEFUL` — egress stateful commit (conntrack).
    - Table 41: `LS_OUT_CHECK_PORT_SEC` — egress port-security check.
    - Table 42: `LS_OUT_APPLY_PORT_SEC` — egress port-security enforcement.
  - Note: exact table numbers are version-dependent; always confirm with `ovn-sbctl lflow-list <ls> | grep 'pipeline=egress'` and cross-check the `table_id` values.
  - Example: `ovs-ofctl dump-flows br-int table=36 | head` shows egress ACL evaluation flows.
  - Source: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml (section "Logical Switch Egress Table")

- **OVN logical port pipeline table IDs — LR ingress stages** — Bucket: OVN | Context: OpenFlow table numbering on `br-int` for Logical Router ingress pipeline | Purpose: identify which OpenFlow table corresponds to a given LR forwarding stage when debugging routing failures | Activity: debugging routing, NAT, gateway redirect | Mechanism: LR pipeline occupies a separate table block (typically starting at 48+ in the shared datapath on `br-int`; actual start offset depends on LS occupancy).
  - Representative LR ingress table sequence (LR_IN_* stages):
    - `LR_IN_ADMISSION` — ingress admission (check MAC, port-sec, discard unknown).
    - `LR_IN_LOOKUP_NEIGHBOR` — check if packet is a neighbor-learning candidate.
    - `LR_IN_LEARN_NEIGHBOR` — learn new ARP/ND neighbor into `MAC_Binding`.
    - `LR_IN_IP_INPUT` — handle ICMP echo to router IP, TTL-exceeded, fragmentation-needed.
    - `LR_IN_UNSNAT` — un-SNAT: reverse NAT lookup for reply packets entering the router.
    - `LR_IN_DNAT` — destination NAT for floating-IP / port-forwarding / LB DNAT.
    - `LR_IN_ECMP_STATEFUL` — ECMP per-connection state for symmetric reply.
    - `LR_IN_ND_RA_OPTIONS` — router advertisement option construction.
    - `LR_IN_ND_RA_RESPONSE` — RA response generation.
    - `LR_IN_IP_ROUTING_PRE` — pre-routing policy evaluation.
    - `LR_IN_IP_ROUTING` — IP routing table lookup (longest prefix match across static routes).
    - `LR_IN_IP_ROUTING_ECMP` — ECMP nexthop selection.
    - `LR_IN_POLICY` — policy-based routing (Logical_Router_Policy evaluation).
    - `LR_IN_POLICY_ECMP` — policy ECMP nexthop selection.
    - `LR_IN_ARP_RESOLVE` — resolve next-hop MAC from `MAC_Binding` / generate ARP/ND request.
    - `LR_IN_CHK_PKT_LEN` — check MTU / send ICMP frag-needed if oversized.
    - `LR_IN_LARGER_PKTS` — handle oversized packets (drop or buffer for fragmentation).
    - `LR_IN_GW_REDIRECT` — redirect centralized traffic to the gateway chassis (cr- port).
    - `LR_IN_ARP_REQUEST` — generate ARP/ND request for unresolved next-hop.
  - Example: `ovn-sbctl lflow-list <lr> | grep LR_IN_IP_ROUTING` lists routing decision flows with prefixes and nexthops.
  - Source: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml (section "Logical Router Ingress Table")

- **OVN logical port pipeline table IDs — LR egress stages** — Bucket: OVN | Context: OpenFlow table numbering for Logical Router egress pipeline | Purpose: understand final forwarding and NAT stages before packet leaves the logical router | Activity: debugging SNAT, delivery, egress port security | Mechanism: LR_OUT stages follow LR_IN in the shared table block.
  - Representative LR egress table sequence (LR_OUT_* stages):
    - `LR_OUT_UNDNAT` — reverse DNAT for reply traffic departing the router.
    - `LR_OUT_POST_UNDNAT` — post-un-DNAT processing.
    - `LR_OUT_SNAT` — source NAT for outgoing packets (floating IP / masquerade / SNAT pool).
    - `LR_OUT_POST_SNAT` — post-SNAT processing.
    - `LR_OUT_EGR_LOOP` — egress loop prevention (hairpin detection).
    - `LR_OUT_DELIVERY` — delivery: output to egress logical port or inter-datapath patch port.
  - Example: `ovn-sbctl lflow-list <lr> | grep LR_OUT_SNAT` shows SNAT rules for each NAT entry; compare with `ovs-ofctl dump-flows br-int | grep cookie=<lflow-uuid-prefix>`.
  - Source: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml (section "Logical Router Egress Table")

### 3.4 CLI tools & every option

- **ovn-nbctl: Northbound DB CLI** | Database Management | Command-line interface to OVN_Northbound database | Transactional updates | Source: ovn-nbctl(8)
  - Can execute multiple commands in single atomic transaction; supports daemon mode for performance on large databases.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --db** | Database Connection | Specify OVSDB remote | OVN_NB_DB environment variable or default | Source: ovn-nbctl(8)
  - Format: unix:@RUNDIR@/ovnnb_db.sock or active/passive OVSDB connection method; default unix:@RUNDIR@/ovnnb_db.sock.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --wait / --no-wait** | Synchronization Semantics | --wait=none (default), --wait=sb, --wait=hv | End-to-end latency control | Source: ovn-nbctl(8)
  - --wait=sb: waits for ovn-northd to update SB DB. --wait=hv: waits for all chassis (ovn-controller) to apply changes.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --print-wait-time** | Wait Time Reporting | Displays latency breakdown | Useful for performance measurement | Source: ovn-nbctl(8)
  - With --wait=sb, shows "ovn-northd delay before processing" and "ovn-northd completion". With --wait=hv, adds "ovn-controller(s) completion".
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --leader-only / --no-leader-only** | Cluster Consistency | Default: leader-only (reads from leader) | Stale-read trade-off | Source: ovn-nbctl(8)
  - With --leader-only, ensures consistent reads from RAFT cluster leader; --no-leader-only allows reads from any replica (may be stale).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --shuffle-remotes / --no-shuffle-remotes** | Load Distribution | Default: shuffle-remotes | Cluster load balancing | Source: ovn-nbctl(8)
  - Shuffles cluster member order before connection; prevents thundering herd on single replica; --no-shuffle-remotes preserves order.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --bare** | Minimal Output | Removes headers/borders from output | Script-friendly format | Source: ovn-nbctl(8)
  - Used in automation scripts; output only essential data without decorative borders.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --no-headings** | Column Suppression | Omits column headers from list output | Compact format | Source: ovn-nbctl(8)
  - Useful for parsing; shows only data rows without header row.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --columns** | Column Selection | --columns=name,type for show/list output | Selective display | Source: ovn-nbctl(8)
  - Filters output to specified columns only; reduces noise in large record sets.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --if-exists** | Conditional Deletion | Prevents error if record doesn't exist | Idempotent deletes | Source: ovn-nbctl(8)
  - Used with deletion commands; command succeeds even if target does not exist (useful for cleanup scripts).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --may-exist** | Conditional Creation | Prevents error if record already exists | Idempotent creates | Source: ovn-nbctl(8)
  - Used with creation commands; command succeeds even if target already exists (useful for provisioning scripts).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --dry-run** | Preview Mode | Validates syntax without committing | Testing transactions | Source: ovn-nbctl(8)
  - Parses commands, builds transaction, shows what would be done, but does not apply to database.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --oneline** | Single-Line Output | Converts newlines to \n | Single-line per-record format | Source: ovn-nbctl(8)
  - Useful for piping output; each command output on one line; newlines escaped.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --timeout** | Connection Timeout | -t secs or --timeout=secs | Default 0 (wait forever) | Source: ovn-nbctl(8)
  - Limits how long to wait for database response; exits with SIGALRM if exceeded.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl --detach** | Daemon Mode | Starts ovn-nbctl as background daemon | Persistent connection | Source: ovn-nbctl(8)
  - Improves performance on large databases; prints socket path; set OVN_NB_DAEMON environment variable to use.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl -u** | Unix Socket Path | Specify daemon socket path | Daemon mode I/O | Source: ovn-nbctl(8)
  - Use with --detach to create at specific path; use without --detach to connect to existing daemon at that path.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl logical switch subcommands** — Bucket: OVN | Context: NB DB | Purpose: create/delete/list logical switches and query their ports | Activity: provisioning | Source: ovn-nbctl(8).
  - `ls-add [LS]`, `ls-del LS`, `ls-list`, `ls-get LS`.
  - Example: `ovn-nbctl ls-add neutron-${NET_UUID}`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl logical switch port subcommands** — Bucket: OVN | Context: NB DB | Purpose: LSP lifecycle, port options, addresses, port security | Activity: provisioning | Source: ovn-nbctl(8).
  - `lsp-add LS PORT [PARENT TAG]`, `lsp-del PORT`, `lsp-list LS`, `lsp-get PORT`.
  - `lsp-set-addresses PORT [ADDRESS...]`, `lsp-get-addresses PORT`.
  - `lsp-set-port-security PORT [ADDR...]`, `lsp-get-port-security PORT`.
  - `lsp-set-options PORT KEY=VALUE...`, `lsp-get-options PORT`.
  - `lsp-set-type PORT TYPE`, `lsp-get-type PORT`.
  - `lsp-set-enabled PORT enabled|disabled`, `lsp-get-enabled PORT`.
  - `lsp-get-up PORT` — whether the port is bound and `up=true` in SB.
  - Example: `ovn-nbctl lsp-add net1 port1 && ovn-nbctl lsp-set-addresses port1 "fa:16:3e:01:02:03 10.0.0.5"`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl logical router subcommands** — Bucket: OVN | Context: NB DB | Purpose: LR lifecycle and port management | Activity: provisioning | Source: ovn-nbctl(8).
  - `lr-add [LR]`, `lr-del LR`, `lr-list`, `lr-get LR`.
  - `lrp-add LR PORT MAC NETWORK... [PEER PEER_PORT]`, `lrp-del PORT`, `lrp-list LR`, `lrp-get PORT`.
  - `lrp-set-gateway-chassis PORT CHASSIS [PRIORITY]`, `lrp-del-gateway-chassis PORT CHASSIS`, `lrp-get-gateway-chassis PORT`.
  - `lrp-set-enabled PORT enabled|disabled`, `lrp-get-enabled PORT`.
  - Example: `ovn-nbctl lrp-add router1 rp-net1 fa:16:3e:aa:bb:cc 10.0.0.1/24`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl ACL subcommands** — Bucket: OVN | Context: NB DB | Purpose: add/remove/list stateful and stateless firewall rules on LSes or Port Groups | Activity: provisioning, policy | Source: ovn-nbctl(8).
  - `acl-add ENTITY DIRECTION PRIORITY MATCH ACTION [log] [severity=LEVEL] [name=NAME] [meter=METER]`
  - `acl-del ENTITY [DIRECTION [PRIORITY MATCH]]`
  - `acl-list ENTITY`
  - ENTITY is a Logical_Switch name or Port_Group name (for `--type=port-group`).
  - DIRECTION: `from-lport` (ingress before leaving the LSP) or `to-lport` (egress toward the LSP).
  - ACTION: `allow`, `allow-related`, `allow-stateless`, `drop`, `reject`.
  - Example: `ovn-nbctl acl-add net1 to-lport 1000 "ip4 && tcp.dst == 22" allow-related`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl load balancer subcommands** — Bucket: OVN | Context: NB DB | Purpose: manage VIP-to-backend mappings for L4 load balancing | Activity: provisioning, service exposure | Source: ovn-nbctl(8).
  - `lb-add LB VIP[:PORT] BACKEND1[:PORT],BACKEND2[:PORT]... [PROTOCOL]`, `lb-del LB [VIP[:PORT]]`, `lb-list [LB]`.
  - `ls-lb-add LS LB [--may-exist]`, `ls-lb-del LS [LB] [--if-exists]`, `ls-lb-list LS`.
  - `lr-lb-add LR LB [--may-exist]`, `lr-lb-del LR [LB] [--if-exists]`, `lr-lb-list LR`.
  - Example: `ovn-nbctl lb-add lb-web 192.168.100.10:80 10.0.0.11:80,10.0.0.12:80 tcp`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl static route subcommands** — Bucket: OVN | Context: NB DB | Purpose: add/remove static routes on logical routers | Activity: provisioning, routing | Source: ovn-nbctl(8).
  - `lr-route-add LR PREFIX NEXTHOP [OUTPORT] [--ecmp] [--ecmp-symmetric-reply] [--may-exist]`
  - `lr-route-del LR [PREFIX [NEXTHOP [OUTPORT]]] [--if-exists]`
  - `lr-route-list LR`
  - `--ecmp-symmetric-reply` — install reverse ECMP flows so replies follow the same hash bucket (introduced OVN 21.03).
  - Example: `ovn-nbctl lr-route-add router1 0.0.0.0/0 10.0.0.254 --may-exist`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl NAT subcommands** — Bucket: OVN | Context: NB DB | Purpose: add/remove DNAT, SNAT, DNAT+SNAT rules on logical routers | Activity: provisioning, addressing | Source: ovn-nbctl(8).
  - `lr-nat-add LR TYPE EXTERNAL_IP LOGICAL_IP [LOGICAL_PORT EXTERNAL_MAC] [--may-exist] [--stateless]`
  - `lr-nat-del LR [TYPE [EXTERNAL_IP]] [--if-exists]`
  - `lr-nat-list LR`
  - TYPE: `snat`, `dnat`, `dnat_and_snat`.
  - Example: `ovn-nbctl lr-nat-add router1 snat 203.0.113.10 10.0.0.0/24`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl address set / port group subcommands** — Bucket: OVN | Context: NB DB | Purpose: manage reusable address/port sets for ACL expressions | Activity: provisioning, policy simplification | Source: ovn-nbctl(8).
  - `address-set-create NAME`, `address-set-delete NAME`, `address-set-list`, `address-set-add NAME ADDRESS...`, `address-set-remove NAME ADDRESS...`.
  - `pg-add PG [PORT...]`, `pg-del PG`, `pg-list`, `pg-set-ports PG PORT...`, `pg-add-ports PG PORT...`, `pg-del-ports PG PORT...`.
  - Example: `ovn-nbctl address-set-create allowed-ips && ovn-nbctl address-set-add allowed-ips 10.0.0.5 10.0.0.6`
  - Example: `ovn-nbctl acl-add net1 to-lport 900 "ip4.src == \$allowed-ips" allow-related`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-nbctl DHCP options subcommands** — Bucket: OVN | Context: NB DB | Purpose: create and manage DHCP option sets referenced by Logical_Switch_Port for native OVN DHCP reply generation | Activity: provisioning, tenant IP configuration | Source: ovn-nbctl(8).
  - `dhcp-options-create CIDR [EXTERNAL_IDS...]` — create a DHCP options record for a subnet CIDR.
  - `dhcp-options-del DHCP_OPTIONS_UUID` — delete a DHCP options record.
  - `dhcp-options-list` — list all DHCP options records with their UUIDs.
  - `dhcp-options-get-options DHCP_OPTIONS_UUID` — display the configured key-value options.
  - `dhcp-options-set-options DHCP_OPTIONS_UUID KEY=VALUE...` — write option values; common options: `lease_time`, `router`, `dns_server`, `server_id`, `server_mac`, `mtu`, `classless_static_route`.
  - Example (provision DHCP for subnet 10.0.0.0/24):
    ```
    UUID=$(ovn-nbctl dhcp-options-create 10.0.0.0/24)
    ovn-nbctl dhcp-options-set-options $UUID \
      lease_time=3600 router=10.0.0.1 \
      dns_server=8.8.8.8 server_id=10.0.0.1 \
      server_mac=fa:16:3e:00:00:01 mtu=1442
    ovn-nbctl lsp-set-dhcpv4-options port1 $UUID
    ```
  - SOURCE: https://man7.org/linux/man-pages/man8/ovn-nbctl.8.html

- **ovn-nbctl DNS subcommands** — Bucket: OVN | Context: NB DB | Purpose: manage DNS records for native OVN DNS resolution (VMs receive DNS replies directly from `ovn-controller` without needing an external DNS relay) | Activity: provisioning, VM name resolution | Source: ovn-nbctl(8).
  - `dns-add LS` — add a DNS entry attached to logical switch `LS`.
  - `dns-del UUID` — delete a DNS entry.
  - `dns-list LS` — list all DNS entries for a logical switch.
  - `dns-set-records UUID KEY=VALUE...` — set FQDN-to-IP mappings.
  - `dns-get-records UUID` — retrieve current mappings.
  - `dns-set-external-ids UUID KEY=VALUE...` — attach external metadata.
  - Example:
    ```
    DNS_UUID=$(ovn-nbctl dns-add net1)
    ovn-nbctl dns-set-records $DNS_UUID \
      vm1.example.com=10.0.0.5 \
      vm2.example.com=10.0.0.6
    ```
  - SOURCE: https://man7.org/linux/man-pages/man8/ovn-nbctl.8.html

- **ovn-nbctl BFD subcommands** — Bucket: OVN | Context: NB DB | Purpose: enable Bidirectional Forwarding Detection on logical router ports for sub-second next-hop liveness detection, especially for ECMP and static-route failover | Activity: HA routing, fast failover | Source: ovn-nbctl(8).
  - `bfd-add LRP DST_IP` — create a BFD record on logical router port `LRP` toward `DST_IP`.
  - `bfd-del BFD_UUID` — delete a BFD record.
  - `bfd-list LRP` — list all BFD sessions for `LRP`.
  - `bfd-get-option BFD_UUID KEY` — retrieve a BFD option value.
  - `bfd-set-options BFD_UUID KEY=VALUE...` — common options: `min_tx` (minimum TX interval ms, default 1000), `min_rx` (minimum RX interval ms), `detect_mult` (failure detection multiplier, default 3).
  - Example:
    ```
    BFD=$(ovn-nbctl bfd-add rp-ext 10.0.0.254)
    ovn-nbctl bfd-set-options $BFD min_tx=300 min_rx=300 detect_mult=3
    # Then reference BFD in a static route for auto-failover:
    ovn-nbctl lr-route-add router1 0.0.0.0/0 10.0.0.254 --bfd
    ```
  - SOURCE: https://man7.org/linux/man-pages/man8/ovn-nbctl.8.html

- **ovn-nbctl load-balancer health-check subcommands** — Bucket: OVN | Context: NB DB | Purpose: manage active health-check probes for individual VIP:port → backend:port entries on a Load_Balancer | Activity: provisioning, service reliability | Source: ovn-nbctl(8).
  - `lb-hc-add LB VIP[:PORT] PROTOCOL` — enable health-checking on a specific VIP endpoint.
  - `lb-hc-del LB [VIP[:PORT]]` — remove health-check entry.
  - `lb-hc-list LB` — list health-check configuration per VIP.
  - Options on `lb-hc-add`: `--health-check`, `--interval=N` (probe interval seconds), `--timeout=N`, `--success-count=N`, `--failure-count=N`.
  - `Service_Monitor` rows in SB DB reflect the resulting per-backend health state.
  - Example:
    ```
    ovn-nbctl lb-add lb-web 192.168.100.10:80 10.0.0.11:80,10.0.0.12:80 tcp
    ovn-nbctl lb-hc-add lb-web 192.168.100.10:80 tcp \
      -- set Load_Balancer_Health_Check . \
         options:interval=5 options:timeout=3 \
         options:success_count=2 options:failure_count=3
    ```
  - SOURCE: https://man7.org/linux/man-pages/man8/ovn-nbctl.8.html

- **ovn-nbctl generic DB subcommands** — Bucket: OVN | Context: NB DB | Purpose: raw table access identically to `ovs-vsctl` | Activity: advanced scripting, custom queries | Source: ovn-nbctl(8).
  - `show`, `list TABLE [RECORD...]`, `find TABLE [COLUMN=VALUE]...`, `get TABLE RECORD COLUMN`, `set TABLE RECORD COLUMN=VALUE`, `add TABLE RECORD COLUMN VALUE`, `remove TABLE RECORD COLUMN VALUE`, `create TABLE COLUMN=VALUE`, `destroy TABLE RECORD`, `wait-until TABLE RECORD [COLUMN=VALUE]`.
  - Example: `ovn-nbctl find Logical_Switch_Port type=router -- --columns=name list Logical_Switch_Port`
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml

- **ovn-sbctl: Southbound DB CLI** | Datapath Database Management | Command-line interface to OVN_Southbound database | Read-write configuration | Source: ovn-sbctl(8)
  - Similar interface to ovn-nbctl; used for manual datapath manipulation, chassis management, debugging.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl --db** | Database Connection | Specify OVN_Southbound remote | OVN_SB_DB environment variable or default | Source: ovn-sbctl(8)
  - Format: unix:@RUNDIR@/ovnsb_db.sock or OVSDB connection method; default unix:@RUNDIR@/ovnsb_db.sock.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl --leader-only** | Cluster Leader Binding | Ensures reads from RAFT leader | Consistency guarantee | Source: ovn-sbctl(8)
  - Same as ovn-nbctl; default true; use --no-leader-only for any-replica reads.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lflow-list** | Logical Flow Inspection | Lists logical flows by datapath | Debugging tool | Source: ovn-sbctl(8)
  - With --uuid: show flow UUIDs. With --ovs: retrieve corresponding OVS flows. With --stats: show OpenFlow counters.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lflow-list --uuid** | UUID Display | Shows first 32 bits of logical flow UUID | OVS flow lookup | Source: ovn-sbctl(8)
  - Matches OpenFlow flow cookie; enables correlation between OVN logical flows and OVS OpenFlow flows.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lflow-list --ovs** | OpenFlow Flow Correlation | Retrieves OVS flows corresponding to logical flows | Detailed flow inspection | Source: ovn-sbctl(8)
  - With optional remote parameter (default unix:@RUNDIR@/br-int.mgmt); requires active OpenFlow connection to switch.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lflow-list --vflows** | Related Records Display | Shows port-bindings, mac-bindings, multicast-groups, chassis | Full context | Source: ovn-sbctl(8)
  - Lists all southbound records used for generating the logical flows; useful for root-cause analysis.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl dump-flows** | Alias | Alias for lflow-list | Backward compatibility | Source: ovn-sbctl(8)
  - Same functionality as lflow-list; older naming convention.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl chassis-add** | Chassis Creation | Creates chassis with encap type and IP | Manual SB population | Source: ovn-sbctl(8)
  - Format: ovn-sbctl chassis-add NAME ENCAP_TYPE ENCAP_IP; --may-exist flag for idempotence.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl chassis-del** | Chassis Removal | Deletes chassis and associated encaps | SB cleanup | Source: ovn-sbctl(8)
  - Format: ovn-sbctl chassis-del NAME; --if-exists flag prevents error if chassis missing.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lsp-bind** | Port Binding | Binds logical port to chassis | Port location assignment | Source: ovn-sbctl(8)
  - Format: ovn-sbctl lsp-bind LOGICAL_PORT CHASSIS; --may-exist flag for idempotence.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-sbctl lsp-unbind** | Port Unbinding | Removes port-to-chassis binding | Decommissioning | Source: ovn-sbctl(8)
  - Format: ovn-sbctl lsp-unbind LOGICAL_PORT; --if-exists flag for safety.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **ovn-trace: Packet Tracing Tool** | Flow Simulation | Simulates packet forwarding through OVN | Debugging utility | Source: ovn-trace(8)
  - Takes microflow description and logical datapath; outputs expected forwarding decision and OpenFlow actions.
  - SOURCE: ovn.org documentation

- **ovn-trace --minimal** | Compact Trace | Minimal trace output | Quick overview | Source: ovn-trace(8)
  - Shows only essential forwarding decision and final actions; omits intermediate table processing details.
  - SOURCE: ovn.org documentation

- **ovn-trace --detailed** | Verbose Trace | Full table-by-table processing | Detailed debugging | Source: ovn-trace(8)
  - Shows all tables visited, actions applied per table, state changes; useful for ACL/policy debugging.
  - SOURCE: ovn.org documentation

- **ovn-trace --ovs** | OpenFlow Output | Shows equivalent OpenFlow flows | Implementation details | Source: ovn-trace(8)
  - Displays OVS OpenFlow flows that ovn-controller would install for the traced packet; useful for low-level debugging.
  - SOURCE: ovn.org documentation

- **ovn-detrace: OpenFlow-to-OVN Translation** | Reverse Lookup | Converts OVS OpenFlow flow/cookie to OVN logical flow | OVS flow investigation | Source: ovn-detrace(1)
  - Takes OpenFlow flow or cookie and outputs corresponding OVN logical flow; inverse of ovn-trace.
  - SOURCE: ovn.org documentation

- **ovn-appctl: Runtime Control** | Daemon Commands | Sends commands to running OVN daemons | Hot configuration | Source: ovn-appctl(8)
  - Syntax: ovn-appctl -t TARGET COMMAND [ARGS]; TARGET is daemon name or socket path.
  - SOURCE: ovn.org documentation

- **ovn-appctl exit** | Daemon Termination | Graceful shutdown of ovn-northd, ovn-controller | Clean stop | Source: ovn-northd(8), ovn-controller(8)
  - Exits daemon; cleans up database rows (e.g., Chassis for ovn-controller, OVSDB locks for ovn-northd).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl pause / resume** | Pause/Resume Processing | Pauses ovn-northd without exiting | High-availability control | Source: ovn-northd(8)
  - pause: stops processing, drops OVSDB lock (allows standby to take over). resume: resumes normal operation.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl is-paused / status** | State Inspection | Returns paused state and HA status | Operational monitoring | Source: ovn-northd(8)
  - is-paused: "true"/"false". status: "active"/"standby"/"paused". Used for orchestration and monitoring.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl set-n-threads / get-n-threads** | Thread Configuration | Changes/queries parallelization level | Runtime tuning | Source: ovn-northd(8)
  - set-n-threads N: enables/disables parallelization (1 = disabled, 2-256 = enabled); get-n-threads: returns current value.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl inc-engine/show-stats** | Engine Counters | Displays incremental engine statistics | Performance monitoring | Source: ovn-northd(8)
  - Shows recompute/compute/abort counters per engine node; used to detect performance issues.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl sb-cluster-state-reset / nb-cluster-state-reset** | Cluster Recovery | Resets cluster index | RAFT recovery | Source: ovn-northd(8), ovn-controller(8)
  - Used when all cluster members destroyed/rebuilt; resets stored cluster index so daemon can interact with rebuilt cluster.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml

- **ovn-appctl ct-zone-list** | Connection Tracking Zones | Lists local CT zones per port | Stateful inspection | Source: ovn-controller(8)
  - Maps logical port to CT zone ID; useful for understanding stateful ACL behavior.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl meter-table-list** | Meter Status | Lists meter table entries and local meter IDs | Rate limiting | Source: ovn-controller(8)
  - Maps NB meter to local OpenFlow meter; shows meter configuration for rate-limiting rules.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl group-table-list** | OpenFlow Group Status | Lists group table entries and local IDs | Multicast/redundancy | Source: ovn-controller(8)
  - Maps logical multicast groups to OpenFlow group IDs; shows group membership.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl inject-pkt** | Packet Injection | Injects microflow into local OVS | Datapath testing | Source: ovn-controller(8)
  - Syntax: inject-pkt MICROFLOW; must include inport matching resident port; uses OVN expression syntax.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl connection-status** | SBDB Connection | Shows OVN SBDB connection status | Connectivity monitoring | Source: ovn-controller(8)
  - Reports connection state to southbound database server; useful for troubleshooting connectivity issues.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl recompute** | Force Recompute | Triggers full compute iteration | Consistency workaround | Source: ovn-controller(8)
  - Used only for incremental engine bugs; performs full recompute of all flows (CPU-intensive).
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl lflow-cache/flush** | Cache Invalidation | Clears logical flow in-memory cache | Cache management | Source: ovn-controller(8)
  - Useful if cache becomes corrupted; normal operation does not require manual flush.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ovn-appctl lflow-cache/show-stats** | Cache Statistics | Displays LFlow cache enable/disable and hit rates | Performance analysis | Source: ovn-controller(8)
  - Shows per-cache-type entry counts; useful for understanding cache effectiveness.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

#### `ovn-ic-nbctl`

- **`ovn-ic-nbctl`** — Bucket: OVN | Context: CLI for the `OVN_IC_Northbound` database (OVN Interconnect) | Purpose: manage Availability Zones, Transit Logical Switches, and interconnect policies for multi-OVN-deployment federation | Activity: provisioning, AZ lifecycle, transit switch configuration | Mechanism: JSON-RPC to `ovn-ic-nbctl.db.sock`; same option model as `ovn-nbctl`.
  - Synopsis: `ovn-ic-nbctl [OPTIONS] COMMAND [ARG...]`
  - Common options (identical to `ovn-nbctl`): `--db=DATABASE`, `--timeout=SECS`, `--wait=none|sb|hv`, `--dry-run`, `--bare`, `--no-headings`, `--columns=COLS`, `--oneline`, `--format={table|html|csv|json}`, `-v`/`--verbose[=SPEC]`, `-h`/`--help`, `-V`/`--version`.
  - **Availability Zone subcommands**: `az-create NAME`, `az-del NAME`, `az-list`.
  - **Transit switch subcommands**: `ts-add TS`, `ts-del TS`, `ts-list`, `ts-lb-add TS LB [--may-exist]`, `ts-lb-del TS [LB] [--if-exists]`, `ts-lb-list TS`.
  - **Policy subcommands**: `ts-route-add`, `ts-route-del`, `ts-route-list` (version-dependent — consult `ovn-ic-nbctl --help`).
  - Example (create AZ and transit switch for two-region OVN deployment):
    ```
    ovn-ic-nbctl az-create us-west
    ovn-ic-nbctl ts-add transit-sw-1
    ```
  - Source: https://man7.org/linux/man-pages/man8/ovn-ic-nbctl.8.html

#### `ovn-ic-sbctl`

- **`ovn-ic-sbctl`** — Bucket: OVN | Context: CLI for the `OVN_IC_Southbound` database | Purpose: read-mostly inspection of the IC Southbound plane — Availability Zone state, learned routes, gateway associations, port bindings for transit switches | Activity: debugging, operational verification of inter-AZ traffic | Mechanism: same JSON-RPC interface; writes are normally done only by `ovn-ic` and `ovn-ic-northd`.
  - Synopsis: `ovn-ic-sbctl [OPTIONS] COMMAND [ARG...]`
  - Common options: same as `ovn-ic-nbctl` (`--db`, `--timeout`, `--bare`, `--no-headings`, etc.).
  - **Show subcommands**: `show` (topology summary), `list TABLE [RECORD]`, `find TABLE [COLUMN[:KEY]=VALUE]...`, `get TABLE RECORD COLUMN`.
  - **Gateway/route subcommands**: `gateway-list`, `route-list`, `port-binding-list` (consult `ovn-ic-sbctl --help` for version-specific names).
  - Example (inspect all IC SB state after federation setup):
    ```
    ovn-ic-sbctl show
    ovn-ic-sbctl list Availability_Zone
    ovn-ic-sbctl list Gateway
    ```
  - Source: https://man7.org/linux/man-pages/man8/ovn-ic-sbctl.8.html

#### `ovn-ic` daemon interaction

- **`ovn-ic` appctl commands** — Bucket: OVN | Context: runtime control of the `ovn-ic` daemon | Purpose: inspect/reset IC daemon state without restart | Activity: debugging federation, AZ route learning, gateway chassis coordination.
  - `ovn-appctl -t ovn-ic exit` — graceful shutdown.
  - `ovn-appctl -t ovn-ic vlog/set MODULE:DEST:LEVEL` — dynamic log level (same model as OVS).
  - `ovn-appctl -t ovn-ic coverage/show` — code-path counters.
  - Source: https://man7.org/linux/man-pages/man8/ovn-ic.8.html

### 3.5 Observability & troubleshooting

- **ovn-trace Simulation** | Packet Forwarding Analysis | Simulates packet path through logical networks | Predictive debugging | Source: ovn-trace(8)
  - Syntax: ovn-trace DB DATAPATH MICROFLOW; outputs logical flow table transitions and final forwarding decision.
  - SOURCE: ovn.org documentation

- **ovn-trace Output Format** | Trace Result Interpretation | Shows table transitions, actions, and final decision | Human-readable | Source: ovn-trace(8)
  - Each line shows table_name: actions; final line shows drop/output/tunnel/controller action.
  - SOURCE: ovn.org documentation

- **ovn-detrace Reverse Lookup** | OpenFlow-to-Logical Mapping | Maps OVS cookies to OVN logical flows | Low-level debugging | Source: ovn-detrace(1)
  - Useful for correlating OVS flow behavior with OVN configuration; helps trace packet behavior to source policy.
  - SOURCE: ovn.org documentation

- **ovn-controller Flow Installation Tracing** | Flow Creation Logging | debug/flush-conntrack for connection state | Stateful inspection | Source: ovn-controller(8)
  - Can enable verbose logging of flow installation; useful for debugging mismatches between expected and installed flows.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Connection Tracking Zone Limits** | CT Resource Management | other_config:ct-zone-limit on Chassis | Memory bounds | Source: ovn-sb(5)
  - Limits number of conntrack entries per chassis; prevents memory exhaustion from state explosion.
  - SOURCE: ovn.org documentation

- **SB Cluster State Monitoring** | Cluster Health | Monitor via ovn-appctl sb-cluster-state-reset and cluster logs | Consensus status | Source: OVN Clustering
  - Check RAFT log entries, leader election, follower sync lag to diagnose cluster issues.
  - SOURCE: ovn.org documentation

- **OVN Bug Tools** | Diagnostic Utilities | ovs-ctl, ovn-ctl for daemon inspection | System-level debugging | Source: OVN Troubleshooting
  - Scripts to manage and query OVN daemon status, restart, view logs.
  - SOURCE: ovn.org documentation

- **ovn-controller Flow Installation Metrics** | Performance Monitoring | Track flow install latency, recompute count | Operational health | Source: ovn-controller(8)
  - inc-engine/show-stats reports engine compute/recompute/cancel counters; high recompute indicates instability.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **OVN Logical Flow Cache** | Performance Optimization | In-memory cache of logical flows | Cache hit rate | Source: ovn-controller(8)
  - enabled via external_ids:ovn-enable-lflow-cache (default true); disabled on updates. lflow-cache/show-stats shows effectiveness.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Lflow Cache Size Limits** | Memory Management | ovn-limit-lflow-cache (max entries) and ovn-memlimit-lflow-cache-kb | Configurable bounds | Source: ovn-controller(8)
  - Prevent unbounded cache growth; automatic trimming triggered by ovn-trim-limit-lflow-cache and ovn-trim-wmark-perc-lflow-cache.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **OVN Database Monitoring** | Consistency Checking | SB_Global.nb_cfg and external_ids:ovn-nb-cfg on br-int | Configuration version tracking | Source: OVN Monitoring
  - nb_cfg incremented each time northbound database changes; ovn-northd updates SB, ovn-controller marks in OVS when applied.
  - SOURCE: ovn.org documentation

- **Southbound Connection State** | Database Reachability | connection-status command and OVSDB client state | Diagnostic probe | Source: ovn-controller(8)
  - Shows whether ovn-controller is connected to SB database, connection type, last activity timestamp.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Datapath Binding Verification** | Logical Network Mapping | Query Datapath_Binding table for tunnel_key assignments | Topology verification | Source: ovn-sb(5)
  - Confirm each logical switch/router has unique tunnel_key; check for key exhaustion on large deployments.
  - SOURCE: ovn.org documentation

- **Port Binding Status Inspection** | Port Operational State** | Check Port_Binding.up flag and chassis column | Port reachability | Source: ovn-sb(5)
  - up=true when port is operational; chassis column shows which chassis owns port; empty chassis = unbound.
  - SOURCE: ovn.org documentation

- **Logical Flow Debugging** | Flow Policy Verification | ovn-sbctl lflow-list with filters for table/datapath | Policy audit | Source: ovn-sbctl(8)
  - List flows by datapath UUID or logical switch name; correlate with northbound ACL/routing configuration.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **OpenFlow Flow Correlation** | OVS Behavior Analysis | lflow-list --ovs to match logical to installed flows | Implementation verification | Source: ovn-sbctl(8)
  - Confirm OVS installations match OVN intent; detect bugs in flow translation or OpenFlow device behavior.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml

- **Multicast Group Debugging** | BUM Flooding Verification | Query Multicast_Group table per logical switch | Broadcast behavior | Source: ovn-sb(5)
  - Lists ports in multicast group; verify broadcast flooding scope matches intended L2 domain.
  - SOURCE: ovn.org documentation

- **MAC Binding Inspection** | Learned Neighbor State | Query MAC_Binding table for ARP/ND entries | Neighbor cache | Source: ovn-sb(5)
  - Shows learned MAC-IP bindings per datapath; useful for understanding ARP behavior and failures.
  - SOURCE: ovn.org documentation

- **DNS Resolution Debugging** | Logical DNS Responses | Query DNS table for configured names and IPs | DNS service health | Source: ovn-sb(5)
  - Verify DNS entries exist and are correctly mapped; check ovn-controller applies DNS reply flows.
  - SOURCE: ovn.org documentation

- **Meter and Rate Limiting** | Traffic Policing Verification | meter-table-list for OpenFlow meter mapping | Policing behavior | Source: ovn-controller(8)
  - Confirms ACL-referenced meters are installed in OVS; check OpenFlow counters for meter drops/marks.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **ACL Logging** | Firewall Audit Trail | ACL log actions, severity in northbound; logs to ovn-controller module:acl_log | Security audit | Source: ovn-controller(8)
  - Set log=true on ACL; severity levels: alert/warning/notice/info/debug; filtered by verbosity settings.
  - SOURCE: https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml

- **Load Balancer Health Monitoring** | Backend Status** | Service_Monitor table tracks LB backend health | Availability tracking | Source: ovn-sb(5)
  - Health status per LB-backend pair; failed backends excluded from forwarding; status updated by periodic probes.
  - SOURCE: ovn.org documentation

- **BFD Health Detection** | Fast Failover** | BFD table for bidirectional monitoring | Sub-second detection | Source: ovn-sb(5)
  - Logical_Router_Port can enable BFD; ovn-controller drives OVS BFD module; detects peer failure in 300ms-3s.
  - SOURCE: ovn.org documentation

- **HA Chassis Failover Verification** | Redundancy Health** | Check HA_Chassis_Group priority and active chassis | Failover readiness | Source: ovn-nb(5)
  - Verify correct chassis is active (has cr- port); check priority ordering for failover behavior.
  - SOURCE: ovn.org documentation

- **Connector Inspection** | Flow Pattern Matching** | External flow matching for telemetry | Flow analytics | Source: OVN Monitoring
  - Tools can sample packets matching ovn-trace patterns; useful for verifying actual flow behavior vs. simulation.
  - SOURCE: ovn.org documentation

---


---

## 4. Cross-cutting troubleshooting playbook

These ten scenarios walk top-down from the OVN logical model down through OpenFlow flows, datapath megaflows, and packet capture. Every command shown here is a real, documented invocation; the playbook does not invent flags. Always begin a session with `ovn-nbctl show` / `ovn-sbctl show` to anchor your mental model of the topology before diving into OpenFlow or the datapath.

### 1. East-west traffic between two VMs on the same OVN logical switch fails

**Problem.** Packets between two VMs attached to the same logical switch are dropped or never arrive.

**Layered checklist.**

1. NB topology — confirm the switch and both ports exist:
   - `ovn-nbctl show`
   - `ovn-nbctl ls-list`
   - `ovn-nbctl lsp-list <switch>`
2. SB binding — both ports must be bound to the chassis where their VM lives:
   - `ovn-sbctl list Port_Binding | grep -E '<lsp-name>|chassis'`
3. Logical-flow inspection — look at L2_LOOKUP and OUTPUT stages on the LS datapath:
   - `ovn-sbctl lflow-list <ls-name>`
4. End-to-end simulation:
   - `ovn-trace <ls-name> 'inport == "<lspA>" && eth.src == <macA> && eth.dst == <macB>'`
   - Add `--ovs` to see the equivalent OVS flows.
5. OpenFlow on `br-int` — table 0 (port classification) and the L2 lookup tables:
   - `ovs-ofctl -O OpenFlow13 dump-flows br-int table=0`
   - `ovs-ofctl -O OpenFlow13 dump-flows br-int | grep <macB>`
6. Datapath megaflows:
   - `ovs-appctl dpctl/dump-flows | grep <macB>`
7. Counters and missed packets:
   - `ovs-appctl coverage/show | grep -E 'drop|miss|upcall'`
   - `ovs-appctl dpif/show`
8. Capture on `br-int` for ground truth:
   - `ovs-tcpdump -i br-int "ether host <macA> and ether host <macB>"`

**Likely root-cause categories.** Port not bound (`Port_Binding.chassis` empty); ACL drop in `LS_IN_ACL`/`LS_OUT_ACL`; FDB not yet populated and BUM flooding suppressed; wrong VLAN/QinQ on `localnet`; conntrack zone exhaustion on the chassis.

### 2. North-south egress through OVN distributed gateway port (DGP) blackholes

**Problem.** Egress to an external network reaches the gateway port but never leaves the chassis.

**Layered checklist.**

1. Gateway port and route configuration:
   - `ovn-nbctl lr-list`
   - `ovn-nbctl lrp-list <lr>`
   - `ovn-nbctl lr-route-list <lr>`
2. Gateway port residency:
   - `ovn-sbctl list Port_Binding | grep -E 'cr-|gateway_chassis'`
3. NAT and policies:
   - `ovn-nbctl lr-nat-list <lr>`
   - `ovn-nbctl lr-policy-list <lr>`
4. Trace through the LR ingress + egress pipelines:
   - `ovn-trace <lr-name> 'inport == "<lrp>" && ip4.src == <vm> && ip4.dst == <ext>'`
5. OpenFlow on `br-int` — confirm the chassisredirect flows are present and the patch port to `br-ex` is up:
   - `ovs-ofctl -O OpenFlow13 dump-flows br-int | grep -E 'cr-|patch'`
6. Datapath:
   - `ovs-appctl dpctl/dump-flows | grep <ext-ip>`
7. Capture on the patch and physical legs:
   - `ovs-tcpdump -i br-int "ip dst host <ext>"`
   - `tcpdump -i <uplink> "ip dst host <ext>"`

**Likely root-cause categories.** `gateway_chassis`/`ha_chassis_group` mismatch; missing or wrong-priority static route; SNAT entry absent so reply packets are unrouteable; `localnet`/`bridge-mappings` typo; uplink VLAN trunk missing; rp_filter on the host's external NIC.

### 3. OVN load balancer VIP drops new connections after a threshold

**Problem.** The VIP works for a while, then new connections start timing out while existing ones survive.

**Layered checklist.**

1. LB definition and where it is attached:
   - `ovn-nbctl list Load_Balancer`
   - `ovn-nbctl ls-lb-list <ls>` and `ovn-nbctl lr-lb-list <lr>`
2. Health check status:
   - `ovn-sbctl list Service_Monitor`
3. SB program for the LB datapath:
   - `ovn-sbctl lflow-list <dp> | grep -i 'lb\|ct_lb'`
4. Conntrack zone occupancy and limits — the most common cause:
   - `ovs-appctl dpctl/ct-get-limits`
   - `ovs-appctl dpctl/dump-conntrack | wc -l`
   - `ovs-appctl dpctl/dump-conntrack | awk -F'zone=' 'NF>1{split($2,a,",");print a[1]}' | sort | uniq -c | sort -rn`
5. ovs-vswitchd-side ephemeral port usage for SNAT:
   - `ovs-appctl coverage/show | grep -i ct`
6. Trace a new connection on the egress path:
   - `ovn-trace <lr> 'inport == "<lrp>" && ct.new && ip.proto == 6 && ip4.src == <client> && ip4.dst == <vip> && tcp.dst == <port>'`

**Likely root-cause categories.** Per-zone CT limit hit; all backends marked down by `Load_Balancer_Health_Check`; SNAT pool exhaustion when `hairpin_snat_ip` is configured; affinity timeout misconfigured on `selection_fields`; meter dropping new connections.

### 4. `ovn-controller` stuck in re-compute / high CPU

**Problem.** `ovn-controller` permanently above 80 % CPU; logs show repeated full recomputes; flow installation latency rises.

**Layered checklist.**

1. Confirm scale on the SB:
   - `ovn-sbctl --columns=_uuid list Logical_Flow | wc -l`
   - `ovn-sbctl --columns=_uuid list Port_Binding | wc -l`
2. Engine and cache stats:
   - `ovs-appctl -t ovn-controller inc-engine/show-stats`
   - `ovs-appctl -t ovn-controller lflow-cache/show-stats`
3. Logging — look for "Triggering recompute" messages:
   - `journalctl -u ovn-controller -n 200 | grep -iE 'recompute|trigger'`
4. Manual force, only as a diagnostic:
   - `ovs-appctl -t ovn-controller recompute`
5. Check whether SB monitoring conditions are correctly narrowing the data each chassis sees:
   - `ovs-appctl -t ovn-controller debug/dump-local-bindings` (if available in your version)

**Likely root-cause categories.** SB DB churn from MAC_Binding learning storms; very large `Address_Set`/`Port_Group` with frequent updates; NB write rate too high (orchestrator looping); incremental engine fallback to full recompute due to a code-path that does not handle a particular update incrementally; `lflow-cache` disabled or undersized.

### 5. SB DB connection flaps between `ovn-controller` and `ovsdb-server` cluster

**Problem.** ovn-controller log shows continuous "connecting to" / "connection dropped" cycles to the SB cluster.

**Layered checklist.**

1. Configured remote and current state on the chassis:
   - `ovs-vsctl get Open_vSwitch . external_ids:ovn-remote`
   - `ovs-vsctl get Open_vSwitch . external_ids:ovn-remote-probe-interval`
2. SB cluster health from any cluster member:
   - `ovs-appctl -t /var/run/openvswitch/ovnsb_db.ctl cluster/status OVN_Southbound`
3. Network reachability and TLS handshake:
   - `nc -zv <sb-ip> 6642`
   - `openssl s_client -connect <sb-ip>:6642 -CAfile /etc/ovn/ovn-ca.crt < /dev/null` (if SSL).
4. Inactivity-probe behaviour — value is in milliseconds, `0` disables:
   - `ovs-vsctl set Open_vSwitch . external_ids:ovn-remote-probe-interval=60000`
5. Server-side connection list:
   - `ovn-sbctl list Connection`

**Likely root-cause categories.** Probe interval shorter than RTT under load; firewall idle timeout closing TCP/6642; SB leader stepping down due to disk-full or fsync stalls; OVSDB RAFT leader election due to a flaky link between cluster members; certificate expiry.

### 6. Geneve tunnel down between two chassis (`br-int` → physical NIC)

**Problem.** Tunnel ports are present but east-west traffic between chassis fails.

**Layered checklist.**

1. Tunnels exist and remote IPs are correct:
   - `ovs-vsctl list-ports br-int | grep -E 'ovn-'`
   - `ovs-vsctl get Interface ovn-<remote-id> options`
2. Encap rows on the SB:
   - `ovn-sbctl list Encap`
3. Tunnel statistics and error counters:
   - `ovs-vsctl get Interface ovn-<remote-id> statistics`
4. Underlay reachability and MTU:
   - `ping -M do -s 1422 <remote-physical-ip>`
   - `ip -s link show <uplink>`
5. Capture Geneve on the underlay (UDP/6081):
   - `tcpdump -i <uplink> -nn 'udp port 6081' -c 20`
6. Trace forwarding into the tunnel:
   - `ovs-appctl ofproto/trace br-int "in_port=<lsp-ofport>,dl_dst=<mac-on-other-chassis>"`

**Likely root-cause categories.** Path MTU < 1500 + Geneve overhead → fragmentation drops; security group on the underlay blocking UDP/6081; mismatched encap type between chassis (one configured `geneve`, the other `vxlan`); chassis row stale after a hostname change so peers tunnel to a wrong IP.

### 7. Conntrack zone exhaustion / "ct_zone in use" errors

**Problem.** `ovs-vswitchd` logs "could not allocate ct_zone" or specific zones reach their limit.

**Layered checklist.**

1. Per-zone occupancy:
   - `ovs-appctl dpctl/ct-get-limits`
   - `ovs-appctl dpctl/dump-conntrack | awk -F'zone=' 'NF>1{split($2,a,",");print a[1]}' | sort | uniq -c | sort -rn | head`
2. Increase the per-zone or default limit (kernel datapath):
   - `ovs-appctl dpctl/ct-set-limits default=200000 zone=5,limit=50000`
3. Inspect chassis-level limit set via OVN:
   - `ovn-sbctl get Chassis <name> other_config:ct-zone-limit`
4. Identify offending OVN datapath / port via:
   - `ovs-appctl -t ovn-controller ct-zone-list`
5. Conntrack helpers (e.g. ALG=ftp) creating extra expectations:
   - `ovs-appctl dpctl/dump-conntrack | grep -i alg`

**Likely root-cause categories.** Workload exceeding per-zone budget; long TCP timeouts retaining `TIME_WAIT` entries; zombie zones from torn-down ports; ALG creating large numbers of `RELATED` expectations; misconfigured `CT_Timeout_Policy`.

### 8. `ovs-vswitchd` 100 % CPU with revalidator threads dominating

**Problem.** `top -H` shows revalidator threads pinning a CPU; flow installs lag the OpenFlow controller.

**Layered checklist.**

1. Flow churn rate:
   - `ovs-appctl coverage/show | grep -E 'rev_validate|flow_mod|upcall'` (compare two snapshots 5 s apart).
2. Megaflow size:
   - `ovs-appctl dpctl/dump-flows | wc -l`
3. Handler/revalidator counts:
   - `ovs-vsctl get Open_vSwitch . other_config:n-handler-threads`
   - `ovs-vsctl get Open_vSwitch . other_config:n-revalidator-threads`
4. Megaflow wildcarding quality — look for unmasked fields you did not expect:
   - `ovs-appctl dpctl/dump-flows | head`
5. Force a one-shot revalidation pass to confirm the queue drains:
   - `ovs-appctl revalidator/wait`

**Likely root-cause categories.** Flow churn from learn() actions installing thousands of microflows; pathological wildcarding caused by `set_field`/`move` actions touching too many fields; under-sized `n-revalidator-threads` for the megaflow count; OVN ACL with `log` causing controller-bound packets to keep re-installing flows.

### 9. OpenFlow bundle commit fails / partial flow install during `ovn-controller` restart

**Problem.** During restart, `ovn-controller` reports `OFPBFC_*` errors; some tables on `br-int` end up partially populated.

**Layered checklist.**

1. Identify the failing bundle:
   - `journalctl -u ovn-controller -n 500 | grep -i bundle`
2. Snapshot the present pipeline:
   - `ovs-ofctl -O OpenFlow15 dump-flows br-int | wc -l`
   - `ovs-ofctl -O OpenFlow15 dump-groups br-int`
3. Confirm OpenFlow protocols negotiated:
   - `ovs-vsctl get Bridge br-int protocols`
   - `ovs-ofctl show br-int`
4. Force a clean re-install:
   - `ovs-appctl -t ovn-controller recompute`
5. If groups/meters are referenced before installation, compare order with:
   - `ovs-ofctl -O OpenFlow15 monitor br-int watch:`

**Likely root-cause categories.** Group/meter referenced by a flow inside the same bundle but not yet committed; protocol mismatch (controller used 1.3 features but the bridge negotiated 1.0 only); large bundle exceeding switch buffer; `ovs-vswitchd` aborting the bundle because of an unsupported field on the negotiated version.

### 10. Asymmetric routing in OVN ECMP (return path takes the wrong chassis)

**Problem.** Forward path to an external destination works; the return packet enters via a different chassis and is dropped.

**Layered checklist.**

1. ECMP routes and policies:
   - `ovn-nbctl lr-route-list <lr>`
   - `ovn-nbctl get Logical_Router <lr> options:ecmp_symmetric_reply`
2. Trace both directions and compare the chosen nexthop:
   - `ovn-trace <lr> 'ip4.src == <vm> && ip4.dst == <ext>'`
   - `ovn-trace <lr> 'ip4.src == <ext> && ip4.dst == <vm>'`
3. Inspect the OpenFlow group used for ECMP selection on `br-int`:
   - `ovs-ofctl -O OpenFlow15 dump-groups br-int`
4. Conntrack continuity for symmetric reply (look for the `reg` carrying the chosen path):
   - `ovs-appctl dpctl/dump-conntrack | grep <ext>`
5. Capture on each candidate uplink to confirm path selection:
   - `tcpdump -i <uplink> "host <ext>"`

**Likely root-cause categories.** `ecmp_symmetric_reply` not enabled, so the reverse hash differs; ECMP nexthop count differs across chassis (one chassis sees a stale BGP route from FRR); SNAT moving the source port and changing the L4 hash; conntrack entry on the wrong chassis (no symmetry tracker).

### 11. Stale or missing MAC_Binding causes routing black-holes

**Problem.** Traffic between two subnets routed by an OVN logical router succeeds initially but intermittently drops, or never works after a VM's MAC address changes (migration, port replacement).

**Layered checklist.**

1. Confirm the router port and static route exist:
   - `ovn-nbctl lr-route-list <lr>`
   - `ovn-nbctl lrp-list <lr>`
2. Inspect MAC_Binding table for the nexthop / destination IP:
   - `ovn-sbctl list MAC_Binding | grep '<destination-ip>'`
   - Look for `mac=""` (empty) or a wrong MAC.
3. Trigger a fresh ARP/ND resolution — delete the stale entry and let traffic re-learn:
   - `ovn-sbctl destroy MAC_Binding $(ovn-sbctl --columns=_uuid find MAC_Binding ip="<destination-ip>" | awk 'NR%2==0')`
4. Trace the routing decision to see if it reaches `LR_IN_ARP_RESOLVE`:
   - `ovn-trace <lr-name> 'inport == "<lrp>" && eth.src == <vm-mac> && eth.dst == <router-mac> && ip4.src == <vm-ip> && ip4.dst == <dest-ip>'`
   - Look for `action=arp` (generates ARP request) vs `action=output` (MAC resolved).
5. Verify the ARP request is installed as an OVS flow on the originating chassis:
   - `ovs-ofctl -O OpenFlow15 dump-flows br-int | grep 'arp_op=1'`
6. Capture ARP on the relevant segment:
   - `ovs-tcpdump -i br-int "arp"`
7. Confirm `ovn-controller` is not throttling ARP resolution due to MAC_Binding table size:
   - `ovs-vsctl get Open_vSwitch . external_ids:ovn-mac-binding-limit`

**Likely root-cause categories.** VM migrated to new chassis but old MAC_Binding not flushed; router port MAC changed (`lrp-set-mac`); broadcast domain isolation prevents ARP from reaching the router (localnet ACL blocking arp); `ovn-northd` not processing updates because it is in standby mode; ARP response not reaching `br-int` (port binding on wrong chassis).

### 12. `ovn-northd` standby does not take over after active failure

**Problem.** Active `ovn-northd` is stopped or crashes; northbound config changes stop propagating to SB; OVN control plane is frozen despite a standby instance running.

**Layered checklist.**

1. Verify which instance holds the SB_Global lock (the active one):
   - `ovs-appctl -t /var/run/ovn/ovn-northd.ctl status` on each node — look for `active` vs `standby`.
2. Check the OVSDB lock state on the SB:
   - `ovn-sbctl get SB_Global . nb_cfg`  (changes should be incrementing as NB changes occur).
3. Confirm the standby instance's DB connectivity:
   - `ovs-appctl -t /var/run/ovn/ovn-northd.ctl is-paused`
4. Inspect `northd_probe_interval` — if it is too long, the standby takes time to detect failure:
   - `ovn-nbctl get NB_Global . options:northd_probe_interval`
5. Examine ovn-northd logs on both nodes:
   - `journalctl -u ovn-northd -n 200 | grep -iE 'lock|active|standby|elected|leading'`
6. Force failover by pausing the (misbehaving) active:
   - `ovs-appctl -t /var/run/ovn/ovn-northd.ctl pause` on the old active.
7. Resume processing on the desired instance:
   - `ovs-appctl -t /var/run/ovn/ovn-northd.ctl resume` on the new active.

**Likely root-cause categories.** `northd_probe_interval` too long relative to failure detection needs; OVSDB RAFT cluster leader step-down interrupting lock release; standby connected to a different (non-leader) OVSDB node so it cannot acquire the lock; both instances in `paused` state after an operator error; disk-full condition on the primary causing RAFT fsync stalls.

---

## 5. Source index

### Open vSwitch upstream

- Open vSwitch project home — https://www.openvswitch.org/
- "What Is Open vSwitch?" — https://docs.openvswitch.org/en/latest/intro/what-is-ovs/
- Conntrack tutorial — https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/
- DPDK install guide — https://docs.openvswitch.org/en/latest/intro/install/dpdk/
- DPDK PMD topics — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
- Datapath internals — https://docs.openvswitch.org/en/latest/topics/datapath/
- OpenFlow FAQ — https://docs.openvswitch.org/en/latest/faq/openflow/
- IPsec how-to — https://docs.openvswitch.org/en/latest/howto/ipsec/
- OVS NEWS / release notes — https://www.openvswitch.org/releases/

### OVS man pages (man7.org mirror)

- `ovs-vswitchd(8)` — https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html
- `ovs-vswitchd.conf.db(5)` — https://man7.org/linux/man-pages/man5/ovs-vswitchd.conf.db.5.html
- `ovs-vsctl(8)` — https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html
- `ovs-ofctl(8)` — https://man7.org/linux/man-pages/man8/ovs-ofctl.8.html
- `ovs-appctl(8)` — https://man7.org/linux/man-pages/man8/ovs-appctl.8.html
- `ovs-dpctl(8)` — https://man7.org/linux/man-pages/man8/ovs-dpctl.8.html
- `ovs-pcap(1)` / `ovs-tcpundump(1)` — https://man7.org/linux/man-pages/man1/ovs-pcap.1.html, https://man7.org/linux/man-pages/man1/ovs-tcpundump.1.html
- `ovs-tcpdump(8)` — https://man7.org/linux/man-pages/man8/ovs-tcpdump.8.html
- `ovs-pki(8)` — https://man7.org/linux/man-pages/man8/ovs-pki.8.html
- `ovs-testcontroller(8)` — https://man7.org/linux/man-pages/man8/ovs-testcontroller.8.html
- `vtep-ctl(8)` — https://man7.org/linux/man-pages/man8/vtep-ctl.8.html
- `ovs-fields(7)` — https://man7.org/linux/man-pages/man7/ovs-fields.7.html
- `ovs-actions(7)` — https://man7.org/linux/man-pages/man7/ovs-actions.7.html
- `ovsdb-server(1)` — https://man7.org/linux/man-pages/man1/ovsdb-server.1.html
- `ovsdb-tool(1)` — https://man7.org/linux/man-pages/man1/ovsdb-tool.1.html
- `ovsdb-client(1)` — https://man7.org/linux/man-pages/man1/ovsdb-client.1.html

### OVN upstream

- OVN project home — https://www.ovn.org/
- OVN documentation — https://docs.ovn.org/en/latest/
- OVN architecture — https://docs.ovn.org/en/latest/topics/architecture.html
- OVN HA — https://docs.ovn.org/en/latest/topics/high-availability.html
- OVN tutorials — https://docs.ovn.org/en/latest/tutorials/
- OVN man pages (upstream XML sources):
  - `ovn-northd(8)` — https://raw.githubusercontent.com/ovn-org/ovn/master/northd/ovn-northd.8.xml
  - `ovn-controller(8)` — https://raw.githubusercontent.com/ovn-org/ovn/master/controller/ovn-controller.8.xml
  - `ovn-nbctl(8)` — https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-nbctl.8.xml
  - `ovn-sbctl(8)` — https://raw.githubusercontent.com/ovn-org/ovn/master/utilities/ovn-sbctl.8.xml
- OVN man pages (man7.org mirror):
  - `ovn-architecture(7)` — https://man7.org/linux/man-pages/man7/ovn-architecture.7.html
  - `ovn-nb(5)` — https://man7.org/linux/man-pages/man5/ovn-nb.5.html
  - `ovn-sb(5)` — https://man7.org/linux/man-pages/man5/ovn-sb.5.html
  - `ovn-trace(8)` — https://man7.org/linux/man-pages/man8/ovn-trace.8.html
  - `ovn-detrace(1)` — https://man7.org/linux/man-pages/man1/ovn-detrace.1.html
  - `ovn-ic(8)` — https://man7.org/linux/man-pages/man8/ovn-ic.8.html
  - `ovn-ic-nbctl(8)` / `ovn-ic-sbctl(8)` — https://man7.org/linux/man-pages/man8/ovn-ic-nbctl.8.html, https://man7.org/linux/man-pages/man8/ovn-ic-sbctl.8.html

### ONF OpenFlow specifications

- Open Networking Foundation, *OpenFlow Switch Specification 1.0.0 (Wire Protocol 0x01)* — published Dec 2009.
- Open Networking Foundation, *OpenFlow Switch Specification 1.3.5 (Wire Protocol 0x04)* — published Mar 2015.
- Open Networking Foundation, *OpenFlow Switch Specification 1.5.1 (Wire Protocol 0x06)* — published Apr 2015.

(ONF distributes the PDFs through the Open Networking Project archive at https://opennetworking.org; specific documents are versioned attachments.)

### Vendor and distribution documentation

- Red Hat — *Networking with Open Virtual Network*, RHOSP — https://docs.redhat.com/en/documentation/red_hat_openstack_platform/16.0/html/networking_with_open_virtual_network/monitoring_ovn
- Red Hat Developer — *The revalidator process explained* — https://developers.redhat.com/articles/2022/10/19/open-vswitch-revalidator-process-explained
- Red Hat Developer — *Benchmarking improved conntrack performance in OvS 3.0.0* — https://developers.redhat.com/articles/2022/11/17/benchmarking-improved-conntrack-performance-ovs-300
- Canonical — *Charmed OpenStack OVN reference* — https://docs.openstack.org/charm-guide/latest/admin/networking/ovn.html
- OpenStack kolla-ansible — *OVN guide* — https://docs.openstack.org/kolla-ansible/latest/reference/networking/ovn.html
- OpenStack neutron / networking-ovn — *Troubleshooting* — https://docs.openstack.org/networking-ovn/ocata/troubleshooting.html

### IETF / RFC

- RFC 8300 — *Network Service Header (NSH)* — https://www.rfc-editor.org/rfc/rfc8300 (NSH encapsulation for service-function chaining; referenced by OVS NSH match fields `nsh_spi`, `nsh_si`, `nsh_c1`–`nsh_c4`).

### Engineer write-ups

- Russell Bryant — OVN architecture & northd internals (Red Hat blog and ovs-discuss postings).
- Numan Siddique — OVN load-balancer, ECMP symmetric reply, and incremental processing (Red Hat blog and ovn-org talks).
- Dan Williams — ovn-controller incremental engine work (Red Hat blog).
- Vikrant Aggarwal — *How to use ovn-trace for troubleshooting OpenFlows* — https://ervikrant06.github.io/ovn/openstack/OVN-openflow-trace/
- NVIDIA — *OVS-DOCA troubleshooting guide* — https://docs.nvidia.com/networking/display/bfswtroubleshooting/ovs-doca
- OVN source — register/pipeline table assignments — https://github.com/ovn-org/ovn/blob/main/lib/ovn-parallel-hdr.h

### 13. VM DNS queries dropped by OVN native DNS

**Problem.** VMs receive no DNS response; `dig` from the VM times out. OVN native DNS is configured (DNS records set via `ovn-nbctl dns-set-records`), but the packets are silently dropped.

**Layered checklist.**

1. Confirm DNS records exist on the logical switch:
   - `ovn-nbctl dns-list <ls>`
   - `ovn-nbctl dns-get-records <dns-uuid>`
2. Verify the logical switch has the DNS entry associated:
   - `ovn-nbctl get Logical_Switch <ls> dns_records`
3. Check OVN Northbound `DNS` table:
   - `ovn-nbctl list DNS`
4. Confirm `ovn-controller` generated the expected logical flow in the `lr_in_dns_lookup` / `ls_in_dns_lookup` pipeline stage:
   - `ovn-sbctl lflow-list | grep dns`
5. Check whether the DNS port binding is set (`type=localport`):
   - `ovn-sbctl list Port_Binding | grep -A5 dns`
6. Trace a DNS UDP packet end-to-end:
   - `ovn-trace <ls> 'udp,ip4.src==<vm-ip>,ip4.dst==<ovn-dns-vip>,udp.dst==53'`
7. Verify the chassis has `ovn-controller` running and is processing the DNS logical port:
   - `ovs-appctl -t ovn-controller connection-status`
8. On the hypervisor, capture DNS on `br-int`:
   - `ovs-tcpdump -i br-int "udp port 53"`

**Likely root-cause categories.** DNS record UUID not linked to the Logical_Switch `dns_records` column; `ovn-northd` not propagating DNS flows because it is in standby; DHCP option `dns_server` pointing to an external IP while OVN native DNS VIP is not configured in the VM's resolver; ACL blocking UDP/53 inbound on the logical switch; VM using the wrong gateway IP (which does not resolve OVN DNS).

---

### 14. Geneve/VXLAN MTU fragmentation causing intermittent large-packet drops

**Problem.** Small packets (ICMP echo, DNS) succeed; large TCP flows or file transfers stall or drop after a few kilobytes. The issue appears only between two hypervisors on different racks.

**Layered checklist.**

1. Confirm tunnel encapsulation type and underlay MTU:
   - `ovn-sbctl list Encap`
   - `ip link show <physical-NIC>` — note MTU.
2. Calculate the overhead:
   - Geneve: 50 bytes (Ethernet 14 + IP 20 + UDP 8 + Geneve header ≥ 8) on top of inner frame.
   - VXLAN: 50 bytes (Ethernet 14 + IP 20 + UDP 8 + VXLAN 8).
   - If physical MTU is 1500, maximum inner payload is 1450 bytes for Geneve.
3. Verify the OVS tunnel port MTU setting:
   - `ovs-vsctl list Interface | grep -A5 genev`
   - `ovs-appctl netdev-dummy/set-mtu <tun-port> <mtu>` (diagnostic only).
4. Check whether Path MTU Discovery (PMTUD) is working — look for ICMP Type 3 Code 4 (fragmentation needed) on the underlay:
   - `tcpdump -i <uplink> "icmp and icmp[0]=3"`
5. Verify `DF` bit handling on OVS tunnel ports:
   - `ovs-vsctl get Interface <genev-port> options:csum`
   - Geneve ports: `options:df_default` (if present).
6. Inspect whether GRO/GSO on the physical NIC is interacting badly with the tunnel:
   - `ethtool -k <physical-NIC> | grep -E 'generic-receive|generic-segmentation|tx-udp'`
7. Test with forced MTU clamp:
   - `ovs-vsctl set Interface <genev-port> options:df_default=false` (allow fragmentation as a diagnostic, not a permanent fix).
8. Check OVN chassis-specific MTU options:
   - `ovn-sbctl get Chassis <chassis> other_config:ovn-encap-df_default`
   - `ovn-nbctl set NB_Global . options:northd_probe_interval` (unrelated but often reviewed alongside).

**Likely root-cause categories.** Physical NIC MTU left at 1500 without accounting for tunnel overhead (correct fix: set underlay MTU to 1600+ or inner MTU to 1450); PMTUD broken because intermediate routers drop ICMP unreachables (common in datacenter iBGP fabrics with ACLs); NIC offload (GRO, LRO, TSO) reassembling large segments before OVS can apply the DF bit correctly; `df_default=true` (the OVS default) combined with a broken PMTUD path causing TCP to stall at the MSS renegotiation step; VXLAN chosen over Geneve but the underlay switch hardware does not offload VXLAN checksum, causing silent drops at line rate.

