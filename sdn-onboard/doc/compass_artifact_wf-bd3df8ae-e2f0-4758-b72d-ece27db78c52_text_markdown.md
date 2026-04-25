# Open vSwitch — A Senior Engineer's Training Curriculum

*A prose-first, command-verified textbook on OVS, OpenFlow, and OVN.*
*All commands below are traceable to the upstream Open vSwitch documentation at docs.openvswitch.org, the man pages at man7.org, and the tutorial source trees referenced at the end of each chapter. Commands are written to be copy-paste runnable on a current Linux distribution with Open vSwitch 2.17 or newer.*

---

## Table of contents

- **Phần I — Foundations** (Chapters 1–4)
- **Phần II — OVS Day-to-Day Operations** (Chapters A–W)
- **Phần III — OpenFlow in OVS** (Chapters 5–10)
- **Phần IV — Tunneling and Overlays** (Chapters 11–13)
- **Phần V — Performance and Scale** (Chapters 14–16)
- **Phần VI — OVN Topic Chapter** (Chapter 17)
- **Phần VII — Production Operations** (Chapters 18–20)
- **Appendices**

---

# Phần I — Foundations

## Chapter 1 — What Open vSwitch actually is

Open vSwitch (OVS) is a production-quality, multi-layer virtual switch designed to enable massive network automation through programmatic extension while still supporting standard management interfaces and protocols such as NetFlow, sFlow, IPFIX, RSPAN, CLI, LACP, and 802.1ag. It is the default vswitch in many KVM-based deployments and the data-plane of OVN. Architecturally, OVS is *not* a single binary. It is a cooperative set of processes:

- **`ovs-vswitchd`** — the chuyển tiếp daemon. It owns the OpenFlow pipeline, the megaflow cache, the userspace datapath (`netdev`), and the bond/LACP/STP/RSTP state machines.
- **`ovsdb-server`** — a lightweight JSON-RPC database server that serves the configuration schema for `ovs-vswitchd`. The on-disk file defaults to `/etc/openvswitch/conf.db`.
- **`openvswitch.ko`** (Linux kernel datapath) — the in-kernel flow cache that actually forwards packet when the datapath type is `system`. It is increasingly supplanted by the userspace `netdev` datapath with DPDK or AF_XDP.
- **Utilities** — `ovs-vsctl` (talks to `ovsdb-server`), `ovs-ofctl` (talks OpenFlow to a bridge), `ovs-appctl` (Unix-socket RPC to any OVS daemon), `ovs-dpctl` (raw datapath control, rarely needed), `ovsdb-tool` / `ovsdb-client` (DB maintenance).

The mental model you should carry through this book is a **four-layer stack**: the OVSDB configuration layer (what should exist), the OpenFlow flow-table layer (how packet should be treated), the datapath cache layer (what the fast path has learned), and the wire layer (what actually leaves the NIC). A great deal of operational troubleshooting amounts to comparing these four layers and finding where they disagree.

**Sources:** `https://docs.openvswitch.org/en/latest/intro/what-is-ovs/`, `https://docs.openvswitch.org/en/latest/intro/why-ovs/`.

## Chapter 2 — Installation across platforms

On Debian and Ubuntu, the canonical path is `apt-get install openvswitch-switch openvswitch-common`. On RHEL, CentOS Stream, and Fedora, it is `dnf install openvswitch`. The systemd units are `openvswitch-switch.service` (Debian family) or `openvswitch.service` (RHEL family); both ultimately launch `ovsdb-server` and `ovs-vswitchd`. The configuration database lives at `/etc/openvswitch/conf.db`, logs at `/var/log/openvswitch/`, and the control sockets at `/var/run/openvswitch/`.

A source build for when you need a specific feature or DPDK integration looks like this:

```bash
git clone https://github.com/openvswitch/ovs.git
cd ovs
./boot.sh
./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc \
            --with-dpdk=static     # optional
make -j$(nproc)
sudo make install
sudo make modules_install          # only if using the deprecated out-of-tree kmod
```

The first-time bootstrap is performed by `ovs-ctl`, which initializes the DB from the bundled schema:

```bash
sudo mkdir -p /etc/openvswitch /var/run/openvswitch /var/log/openvswitch
sudo ovsdb-tool create /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema
sudo ovs-ctl --system-id=random start
```

`--system-id=random` writes a UUID to the `Open_vSwitch.external_ids:system-id` column so that management tools can distinguish hosts. For DPDK, you additionally need hugepages (`echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages`), IOMMU enabled in the kernel command line (`intel_iommu=on iommu=pt`), and the VFIO driver bound to the target NIC via `dpdk-devbind.py`. Windows and BSD ports exist but are out of scope here except for brief notes in Chapter W.

**Sources:** `https://docs.openvswitch.org/en/latest/intro/install/general/`, `https://docs.openvswitch.org/en/latest/intro/install/distributions/`, `https://docs.openvswitch.org/en/latest/intro/install/dpdk/`.

## Chapter 3 — The first bridge, the first port, the first trace

The minimum viable session — which we will use as a baseline for the rest of the book — is three commands:

```bash
sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-port br0 eth1
sudo ovs-vsctl show
```

The output of `show` will list the bridge `br0` with an implicit internal port of the same name, plus the newly added `eth1`. Already at this point the switch is chuyển tiếp in **NORMAL** mode, i.e. behaving like an unmanaged L2 switch with MAC learning. To prove this without moving a single packet, run the built-in simulator:

```bash
sudo ovs-appctl ofproto/trace br0 "in_port=eth1,dl_src=aa:bb:cc:dd:ee:01,dl_dst=ff:ff:ff:ff:ff:ff"
```

The output walks the OpenFlow pipeline table-by-table and ends with a `Datapath actions:` line that tells you exactly what the kernel would do. `ofproto/trace` is the single most important OVS troubleshooting primitive and you should internalize it before reading Phần III.

## Chapter 4 — The OVSDB mental model in ten minutes

OVSDB is an *ordered, transactional, schema-bound* JSON-RPC database. For `vswitchd` the important tables, each of which gets a full chapter later, are: `Open_vSwitch` (singleton root), `Bridge`, `Port`, `Interface`, `Controller`, `Manager`, `QoS`, `Queue`, `Mirror`, `NetFlow`, `sFlow`, `IPFIX`, `Flow_Table`, `Flow_Sample_Collector_Set`, `SSL`, `AutoAttach`, `CT_Zone`, and `CT_Timeout_Policy`. Columns are typed: strings, integers, reals, booleans, UUIDs, and the two composite types `set<T>` and `map<K,V>`. Understanding map columns is essential because `other_config` and `external_ids` — the two escape hatches OVS uses for everything it did not promote to a first-class column — are both `map<string,string>`.

**Sources:** `https://docs.openvswitch.org/en/latest/ref/ovs-vswitchd.conf.db.5/`, `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`.

---

# Phần II — OVS Day-to-Day Operations

*This Phần is the heart of the rebuild. Each chapter opens with concept, then a thực hành lab with verified syntax, then verification and failure modes, then a self-check. Every command in this Phần is drawn from docs.openvswitch.org or the upstream man pages.*

## Chapter A — The ovs-vsctl language in depth

`ovs-vsctl` is not, despite first appearances, a shell around individual commands. It is a transactional compiler: a single invocation becomes a single OVSDB transaction, and the `--` separator is the statement separator inside that transaction. This matters because atomicity is how you avoid half-configured bridges, orphan `Queue` rows, and referential-integrity bugs.

### The universal verbs

Every OVSDB row, regardless of table, can be manipulated with eleven verbs. The first six operate on scalar or composite columns of existing rows: `list`, `find`, `get`, `set`, `add`, `remove`, `clear`. The remaining five operate on the row itself: `create`, `destroy`, and the idempotent variants `--may-exist`, `--if-exists`. Transactional *references* between new rows in the same transaction are expressed with the `--id=@name` token, which binds a symbolic name to the UUID of a row created in that transaction.

The canonical grammar:

```
ovs-vsctl [global-opts] command [-- command]...
global-opts : --db=socket | --no-wait | --timeout=N | --may-exist | --if-exists | --id=@name
command     : verb table [row] [column[:key][=value]]...
```

The `--no-wait` flag is particularly important on busy hypervisors: by default `ovs-vsctl` blocks until `ovs-vswitchd` has reloaded its configuration from the DB. Under automation you often do not need to wait, and the flag halves the độ trễ of bulk operations.

### Examples that exercise every column type

A string column: `ovs-vsctl set Bridge br0 fail_mode=secure`. An integer: `ovs-vsctl set Port p1 tag=100`. A boolean: `ovs-vsctl set Bridge br0 stp_enable=true`. A UUID reference, expressed by name: `ovs-vsctl set Port eth0 qos=@q -- --id=@q create QoS type=linux-htb`. A set: `ovs-vsctl set Port p1 trunks=10,20,30`; and to mutate it non-destructively, `ovs-vsctl add Port p1 trunks 40` or `ovs-vsctl remove Port p1 trunks 20`. A map: `ovs-vsctl set Bridge br0 other_config:mac-aging-time=600` writes one key; `ovs-vsctl remove Bridge br0 other_config mac-aging-time` deletes it; `ovs-vsctl clear Bridge br0 other_config` empties the whole map.

### Realistic multi-row atomic transaction

Creating a QoS hierarchy with two queues in one indivisible step is the classic test case:

```bash
ovs-vsctl -- set port eth0 qos=@newqos \
          -- --id=@newqos create qos type=linux-htb \
                          other-config:max-rate=1000000000 \
                          queues:0=@q0 queues:1=@q1 \
          -- --id=@q0 create queue other-config:min-rate=100000000 \
                                    other-config:max-rate=500000000 \
          -- --id=@q1 create queue other-config:min-rate=200000000
```

If any substep fails, the whole transaction aborts, which is precisely the behavior you want when programming queues that OpenFlow rules will later `set_queue:` into.

**Sources:** `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`, `https://docs.openvswitch.org/en/latest/faq/qos/`.

## Chapter B — Bridge lifecycle and properties

A bridge is the unit of OpenFlow chuyển tiếp. Create one with `ovs-vsctl add-br br0`; it comes up with `datapath_type=system` (kernel) by default. Specify `datapath_type=netdev` for the userspace datapath that DPDK and AF_XDP require; specify `datapath_type=dummy` for test beds that never touch real interfaces.

The **fail-mode** column decides what happens when all OpenFlow controllers are unreachable. With `fail_mode=standalone` (default), the bridge behaves as an unmanaged L2 switch running MAC learning and VLAN separation. With `fail_mode=secure`, the bridge stops chuyển tiếp except under flow explicitly programmed by the operator. In production with a controller, always set `secure`:

```bash
ovs-vsctl set-fail-mode br0 secure
ovs-vsctl set bridge br0 protocols=OpenFlow13,OpenFlow14,OpenFlow15
```

The `protocols` column is a `set<string>` that enables specific OpenFlow versions; if unset, only OpenFlow 1.0 is offered. Enable explicitly to khớp với your controller.

Spanning Tree uses two orthogonal switches. Classic STP (802.1D): `ovs-vsctl set bridge br0 stp_enable=true`; verify with `ovs-appctl stp/show br0`. RSTP (802.1w): `ovs-vsctl set bridge br0 rstp_enable=true`, then `ovs-appctl rstp/show br0`. Never enable both on the same bridge. Multicast snooping is enabled by `ovs-vsctl set bridge br0 mcast_snooping_enable=true` and tuned via `other_config:mcast-snooping-disable-flood-unregistered`.

The MAC table is capped at 2048 entries by default; raise it with `other_config:mac-table-size=8192`. Aging time defaults to 300s and is tuned with `other_config:mac-aging-time=600`. The datapath ID is derived from the bridge's internal port's MAC address unless overridden with `other_config:datapath-id`.

Remove a bridge safely by first disabling controllers (`ovs-vsctl del-controller br0`), draining traffic at the orchestration layer, then `ovs-vsctl --if-exists del-br br0`. Do not use `--if-exists` in CI pipeline where a missing bridge is itself a bug.

**Sources:** `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`, `https://docs.openvswitch.org/en/latest/ref/ovs-vswitchd.conf.db.5/`.

## Chapter C — Port lifecycle: access, trunk, bond, patch

A `Port` row in OVSDB binds one or more `Interface` rows to a `Bridge`. In most cases you will have one interface per port; bonds are the exception. Add a port with `ovs-vsctl add-port br0 eth1`; list with `ovs-vsctl list-ports br0`; find its bridge with `ovs-vsctl port-to-br eth1`; remove with `ovs-vsctl --if-exists del-port br0 eth1`.

VLAN semantics live in the `Port` row's `tag`, `trunks`, and `vlan_mode` columns. An **access port** has `tag=N` set and `vlan_mode=access`: untagged traffic enters VLAN N, and outgoing VLAN N traffic leaves untagged. A **trunk port** has `trunks=[set of VLAN IDs]` and no `tag`; tagged frames in those VLANs pass through unchanged. A **native-tagged** or **native-untagged** port combines a default VLAN (`tag=`) with a trunk list (`trunks=`), emitting the native VLAN either tagged or untagged depending on the mode. A **dot1q-tunnel** port implements Q-in-Q: set `vlan_mode=dot1q-tunnel`, `tag=N` for the outer VLAN, and frames entering the port are wrapped with an outer tag. To configure an access port after the fact:

```bash
ovs-vsctl set port eth1 tag=100 vlan_mode=access
```

**Patch ports** connect two OVS bridges in the same host at zero packet-cost: they are implemented as a pointer in the datapath, not by any send-and-receive path. Create them as a pair:

```bash
ovs-vsctl add-port br-int patch-to-ex -- \
  set Interface patch-to-ex type=patch options:peer=patch-to-int
ovs-vsctl add-port br-ex patch-to-int -- \
  set Interface patch-to-int type=patch options:peer=patch-to-ex
```

**Internal ports** are virtual L3 interfaces exposed to the host kernel. Every bridge comes with one of its own name; you can add more for management traffic: `ovs-vsctl add-port br0 mgmt -- set Interface mgmt type=internal`, then `ip addr add 10.0.0.1/24 dev mgmt && ip link set mgmt up`.

**Sources:** `https://docs.openvswitch.org/en/latest/faq/configuration/`, `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`.

## Chapter D — Interface lifecycle and types

The `Interface.type` column is the single most important typing decision in OVSDB. Recognized values include `system` (a Linux netdev), `internal` (an OVS-provided tap), `patch`, `tap`, `gre`, `vxlan`, `geneve`, `erspan`, `ip6erspan`, `ip6gre`, `stt`, `lisp`, `dpdk`, `dpdkvhostuser`, `dpdkvhostuserclient`, and `afxdp`. Each type consumes a distinct subset of the `options:` map.

For tunnels the near-universal options are `options:remote_ip=IP`, `options:local_ip=IP`, and `options:key=KEY-or-flow`. Setting `key=flow` defers the tunnel key selection to the OpenFlow action `set_tunnel:`, which is how multipoint flow-based tunneling works. Setting `options:dst_port=PORT` overrides the default L4 port (4789 for VXLAN, 6081 for Geneve).

`ofport_request` lets you pin OpenFlow port numbers deterministically, which is essential when your flow rules reference numeric `in_port=` matches: `ovs-vsctl set Interface eth1 ofport_request=5`. `mtu_request` sets the interface MTU independently of what the kernel reports. The `external_ids` map is by convention used for orchestrator metadata — `iface-id` and `attached-mac` being the two keys that OpenStack, OVN, and other cloud controllers expect.

Read per-interface statistics with `ovs-vsctl get Interface eth1 statistics`, which returns a map with keys like `rx_packets`, `tx_packets`, `rx_bytes`, `tx_bytes`, `rx_dropped`, `tx_dropped`, and `collisions`. For rate computation, sample twice and subtract.

**Sources:** `https://docs.openvswitch.org/en/latest/ref/ovs-vswitchd.conf.db.5/`.

## Chapter E — Bonding and link aggregation

OVS implements its own bonding independent of the Linux kernel bonding driver. Three modes exist: `active-backup` (one active member at a time), `balance-slb` (per-source-MAC hashing, rebalanced every `other_config:bond-rebalance-interval` ms, does not require switch cooperation), and `balance-tcp` (L2/L3/L4 hash; requires LACP and an MLAG-capable peer switch). Create a bond:

```bash
ovs-vsctl add-bond br0 bond0 eth1 eth2 \
  bond_mode=balance-slb \
  lacp=active other_config:lacp-time=fast \
  bond_updelay=100 bond_downdelay=100
```

`lacp=active|passive|off` toggles LACP; `active` sends PDUs proactively, `passive` only in response. Because some switches block all traffic while LACP negotiates, the fallback option `other_config:lacp-fallback-ab=true` lets OVS fall back to active-backup until negotiation succeeds — a configuration foot-gun-saver worth enabling by default.

Verify:

```bash
ovs-appctl bond/show bond0
ovs-appctl lacp/show bond0
```

The `bond/show` output lists `bond_mode`, `lacp_status`, active slave, each member's `may_enable` state, and the rebalance countdown. The `lacp/show` output dumps Actor and Partner system IDs, keys, priorities, and the LACP state bits (Active/Passive, Short/Long timeout, Aggregatable, IN_SYNC, Collecting, Distributing, Defaulted). The letter salad is worth memorizing: `ACEGIKNP` on both sides means a healthy bundled link.

Failure-test a bond by bringing one member down (`ip link set eth1 down`), running continuous pings, and watching `ovs-appctl bond/show`. Expect a sub-second reconvergence in `active-backup` and sub-100-millisecond in `balance-tcp` with LACP fast-timers.

**Sources:** `https://docs.openvswitch.org/en/latest/topics/bonding/`, `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`.

## Chapter F — Patch ports and the br-int / br-ex / br-tun pattern

The canonical multi-bridge pattern in real deployments is three bridges per host. `br-int` carries all VM/container-facing traffic and is where OpenFlow policy lives. `br-ex` peers with the physical uplink and handles VLAN translation, NAT, and provider-network plumbing. `br-tun` terminates overlay tunnels. The three are stitched together with **patch-port pairs**; in the kernel datapath, a patch port is a zero-copy tail-call, not a real queue, so the overhead of bridge crossing is effectively free.

```
      VMs                           Physical
       │                               │
   ┌───▼──────┐   patch   ┌────────────▼─┐
   │ br-int   ├──────────►│ br-ex         │
   └─┬────────┘           └───────────────┘
     │ patch
   ┌─▼────────┐
   │ br-tun   ├── VXLAN/Geneve to remote hosts
   └──────────┘
```

The zero-copy claim is visible in the theo dõi output: `ofproto/trace` shows the packet recirculating into the second bridge with no datapath hop, and `ovs-dpctl dump-flows` reveals that the kernel megaflow is a single entry spanning both bridges.

## Chapter G — Port mirroring (SPAN) and packet capture

The `Mirror` table in OVSDB is referenced from `Bridge.mirrors`. A mirror has up to three source selectors (`select_src_port`, `select_dst_port`, `select_vlan`, or the wildcard `select_all`) and one destination, which is either `output_port` (local SPAN) or `output_vlan` (RSPAN). The canonical atomic idiom:

```bash
ovs-vsctl -- set Bridge br0 mirrors=@m \
  -- --id=@eth0 get Port eth0 \
  -- --id=@eth1 get Port eth1 \
  -- --id=@eth2 get Port eth2 \
  -- --id=@m create Mirror name=mymirror \
         select-dst-port=@eth0,@eth1 \
         select-src-port=@eth0,@eth1 \
         output-port=@eth2
```

RSPAN uses `output-vlan=` instead of `output-port=` and strips the original tag in favor of the mirror tag. Point a local tcpdump at the output port — after `ip link set tap0 promisc on` if the port is a host-visible internal — to feed Wireshark or Suricata.

Cleanup is one line: `ovs-vsctl clear Bridge br0 mirrors`. Because the `Mirror` row is unreferenced after the clear, OVSDB garbage-collects it automatically; the same is **not** true for `QoS` or `Queue` rows, which you must `destroy` explicitly.

**Sources:** `https://docs.openvswitch.org/en/latest/faq/configuration/`, `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`.

## Chapter H — sFlow, NetFlow, and IPFIX export

Three separate protocols, three separate tables, one consistent idiom. sFlow samples a configurable fraction of packet (1-in-N) plus periodic counter polls; NetFlow emits flow records on timeout; IPFIX is NetFlow's standardized successor with template negotiation.

sFlow:

```bash
ovs-vsctl -- --id=@s create sFlow agent=eth1 \
             target=\"10.0.0.1:6343\" \
             header=128 sampling=64 polling=10 \
          -- set Bridge br0 sflow=@s
```

NetFlow v5/v9:

```bash
ovs-vsctl -- set Bridge br0 netflow=@nf \
          -- --id=@nf create NetFlow targets=\"192.168.0.34:5566\" active-timeout=30
```

IPFIX:

```bash
ovs-vsctl -- set Bridge br0 ipfix=@i \
          -- --id=@i create IPFIX targets=\"192.168.0.34:4739\" \
                              obs_domain_id=123 obs_point_id=456 \
                              cache_active_timeout=60 cache_max_flows=13
```

Verify the agent is sending with `tcpdump -ni ethX udp port 6343` on the collector host. Rotate collectors by `ovs-vsctl set sFlow <uuid> target='"new:6343"'`; the change is atomic and no packet are lost during rotation. Clear with `ovs-vsctl clear Bridge br0 sflow` (or `netflow`, or `ipfix`).

**Sources:** `https://docs.openvswitch.org/en/latest/howto/sflow/`.

## Chapter I — QoS in depth

OVS configures, but does not implement, QoS — the actual queueing is done by Linux `tc` (for kernel datapaths) or the DPDK rte_sched library (for userspace). Two distinct QoS features matter: ingress policing and egress shaping.

**Ingress policing** is a simple token-bucket rate limiter on the `Interface` row:

```bash
ovs-vsctl set interface tap0 ingress_policing_rate=1000 \
                              ingress_policing_burst=100
```

Rate is in kbps, burst in kb. 0 disables the policer.

**Egress shaping** uses the `QoS` + `Queue` tables plus an OpenFlow action. The upstream `linux-htb` recipe — verbatim from the FAQ — is:

```bash
ovs-vsctl -- add-br br0 \
  -- add-port br0 eth0 \
  -- add-port br0 vif1.0 -- set interface vif1.0 ofport_request=5 \
  -- add-port br0 vif2.0 -- set interface vif2.0 ofport_request=6 \
  -- set port eth0 qos=@newqos \
  -- --id=@newqos create qos type=linux-htb \
        other-config:max-rate=1000000000 \
        queues:123=@vif10queue queues:234=@vif20queue \
  -- --id=@vif10queue create queue other-config:max-rate=10000000 \
  -- --id=@vif20queue create queue other-config:max-rate=20000000

ovs-ofctl add-flow br0 in_port=5,actions=set_queue:123,normal
ovs-ofctl add-flow br0 in_port=6,actions=set_queue:234,normal
```

The queue numbers (123, 234) are arbitrary OpenFlow queue IDs that `set_queue:` in the flow-table references. Without the OpenFlow rules, packet go to the default queue and nothing is shaped — this is the single most common QoS misconfiguration in the field.

`type=linux-hfsc` is the alternative for hierarchical fair service; `type=egress-policer` (DPDK) enforces a flat rate. Verify with `ovs-appctl qos/show eth0` and cross-check with `tc qdisc show dev eth0` and `tc class show dev eth0`. Clean up thoroughly, because unreferenced `QoS` and `Queue` rows are not garbage-collected:

```bash
ovs-vsctl -- destroy QoS eth0 -- clear Port eth0 qos
ovs-vsctl -- --all destroy Queue
```

**Sources:** `https://docs.openvswitch.org/en/latest/faq/qos/`, `https://docs.openvswitch.org/en/latest/howto/qos/`.

## Chapter J — Tunnel port CRUD

Create a VXLAN tunnel:

```bash
ovs-vsctl add-port br-tun vxlan0 -- \
  set Interface vxlan0 type=vxlan options:remote_ip=10.0.0.2 \
                                    options:key=flow \
                                    options:dst_port=4789
```

Swap `type=vxlan` for `geneve`, `gre`, `erspan`, or `ip6gre` as needed. For Geneve, `dst_port` defaults to 6081; for GRE, `options:key=N` maps to the GRE key; for ERSPAN, `options:erspan_ver`, `options:erspan_idx`, and `options:erspan_dir` control the mirror session ID. Use `options:tos=inherit` to copy the inner ToS to the outer header; `options:ttl=64` sets a fixed TTL; `options:df_default=true` sets DF in the outer IP header (recommended unless your PMTUD is broken).

Inspect tunnel neighbor tables with `ovs-appctl tnl/neigh/show`, `ovs-appctl tnl/arp/show`, `ovs-appctl tnl/ports/show`. The most common failure mode is "tunnel up but no traffic" — 95% of the time this is MTU. VXLAN adds 50 bytes, Geneve 50–66 bytes. Either shrink the tenant MTU to 1450 or raise the underlay MTU to 1600.

**Sources:** `https://docs.openvswitch.org/en/latest/howto/tunneling/`.

## Chapter K — SSL/TLS hardening of the control channel

`ptcp:` is convenient for labs, dangerous in production. Every `Controller` or `Manager` target should be `ssl:IP:PORT`. OVS ships a minimal PKI:

```bash
ovs-pki init                                    # root CA
ovs-pki req+sign ovsclient switch               # switch cert
ovs-pki req+sign ctl controller                 # controller cert
ovs-vsctl set-ssl /etc/openvswitch/key.pem \
                  /etc/openvswitch/cert.pem \
                  /etc/openvswitch/cacert.pem
ovs-vsctl set-controller br0 ssl:10.0.0.10:6653
```

Verify the handshake from the controller side with `openssl s_client -connect 10.0.0.10:6653 -CAfile cacert.pem`. Rotate CAs by adding the new root to `cacert.pem` before switching the client cert, never the reverse.

**Sources:** `https://man7.org/linux/man-pages/man8/ovs-pki.8.html`.

## Chapter L — Logging and debugging with ovs-appctl

`ovs-appctl` is a Unix-socket RPC to any OVS daemon. The vlog subsystem is modular: each source file is a module, each destination is a facility (`console`, `syslog`, `file`), and each combination has an independent level (`emer`, `err`, `warn`, `info`, `dbg`). List current levels with `ovs-appctl vlog/list`. Turn up a subsystem:

```bash
ovs-appctl vlog/set dpif:file:dbg
ovs-appctl vlog/set dpdk:file:dbg
ovs-appctl vlog/set vconn:file:dbg       # OpenFlow wire trace
```

Log rotation is handled by `ovs-appctl vlog/reopen` after moving the file. `ovs-appctl coverage/show` dumps every named counter in `ovs-vswitchd` with per-second, per-minute, and per-hour rates — start here when investigating unexpected behavior, because every allocation, netlink round-trip, upcall, and flow cài đặt is counted. `ovs-appctl memory/show` breaks down memory by component.

**Sources:** `https://man7.org/linux/man-pages/man8/ovs-appctl.8.html`.

## Chapter M — OVSDB operations: backup, restore, compact

The DB file at `/etc/openvswitch/conf.db` is append-only: every transaction is logged. Over time the file grows; `ovsdb-tool compact /etc/openvswitch/conf.db` rewrites it as a snapshot of current state. Do not compact while `ovsdb-server` is writing to the file; use `ovs-appctl -t ovsdb-server ovsdb-server/compact` instead, which performs a live compaction.

Backup and restore:

```bash
ovsdb-client backup > /tmp/conf.db.bak     # snapshot
ovsdb-client restore < /tmp/conf.db.bak    # restore (fresh DB)
```

`ovsdb-tool show-log` prints the transaction history. `ovsdb-tool db-version`, `db-cksum`, `db-name` answer schema questions. To upgrade across a schema change: `ovsdb-tool convert /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema`.

## Chapter N — High availability: clustered OVSDB with Raft

OVSDB gained Raft-based clustering in OVS 2.9. It is used in production for OVN's NB and SB databases; it is *not* used for per-host `conf.db`. Bootstrap a three-node cluster:

```bash
# node 1
ovsdb-tool create-cluster /etc/openvswitch/db OVN_Southbound tcp:10.0.0.1:6644

# node 2
ovsdb-tool join-cluster /etc/openvswitch/db OVN_Southbound \
           tcp:10.0.0.2:6644 tcp:10.0.0.1:6644

# node 3
ovsdb-tool join-cluster /etc/openvswitch/db OVN_Southbound \
           tcp:10.0.0.3:6644 tcp:10.0.0.1:6644 tcp:10.0.0.2:6644
```

Start `ovsdb-server` with the DB file on each node. Inspect cluster health:

```bash
ovs-appctl -t /var/run/openvswitch/ovsdb-server.ctl cluster/status OVN_Southbound
ovsdb-client list-dbs tcp:10.0.0.1:6642
```

Remove a running member with `ovs-appctl cluster/leave`; kick a failed member from a surviving node with `ovs-appctl cluster/kick`. Clients connect by specifying all cluster members in comma-separated form: `ovn-remote="tcp:10.0.0.1:6642,tcp:10.0.0.2:6642,tcp:10.0.0.3:6642"`. A three-node cluster tolerates one failure; a five-node cluster tolerates two. Once a server leaves a cluster it cannot rejoin — create a fresh member.

**Sources:** `https://docs.openvswitch.org/en/latest/ref/ovsdb.7/`, `https://docs.openvswitch.org/en/latest/tutorials/ovsdb-cluster/`.

## Chapter O — OVSDB role-based access control

Restricting which tables and columns a client can read or write is done by assigning a role in the `Manager` row: `ovs-vsctl set Manager ssl:10.0.0.10:6640 role=ovn-controller`. The RBAC permission model is defined in the OVN schema, and `ovn-controller` uses a restricted role that can only update its own `Chassis` row and the `Port_Binding` rows it owns. Verify with `ovsdb-client` from inside the restricted principal's identity — an attempt to write outside the role fails with a permission error.

## Chapter P — Upgrades, rolling restart, and graceful shutdown

Upgrading OVS without data-plane interruption is a five-step dance. First, install the new packages without restarting daemons. Second, `ovs-appctl -t ovsdb-server exit --cleanup` and start the new `ovsdb-server`. Third, run `ovsdb-tool needs-conversion` and `ovsdb-tool convert` if the schema changed. Fourth, restart `ovs-vswitchd` with `--bundle`-style atomic replacement: `systemctl reload-or-restart openvswitch-switch`. Fifth, for kernel-datapath hosts, reload `openvswitch.ko` — this briefly evicts the megaflow cache but does not drop existing connections because conntrack state lives separately.

## Chapter Q — Datapath introspection

`ovs-dpctl show` lists every datapath on the host with its port count and lookup hit/miss/lost counters. `ovs-dpctl dump-flows -m` dumps the current microflow and megaflow cache, including masked-out wildcards. `ovs-appctl upcall/show` reports the number of in-flight flow installs, the average, the maximum, and the configured limit (default 200,000). Too many upcall relative to packet rate means flow are being evicted too fast; raise with `ovs-appctl upcall/set-flow-limit 500000`. Tune handler and revalidator thread counts via `other_config:n-handler-threads` and `other_config:n-revalidator-threads`.

## Chapter R — ovs-appctl reference tour

A one-line recipe per target:

- `bridge/dump-flows br0` — every flow including hidden ones.
- `bond/show bond0`, `bond/show-stats`, `bond/migrate` — bond status, stats, manual hash migration.
- `lacp/show bond0` — LACP actor/partner state.
- `stp/show`, `rstp/show` — spanning-tree state.
- `fdb/show br0`, `fdb/flush br0` — MAC table and forced relearn.
- `mdb/show br0` — multicast snooping table.
- `ofproto/trace br0 "<flow>"` — simulate a packet through the pipeline.
- `dpctl/show`, `dpctl/dump-flows` — datapath equivalents of `ovs-dpctl`.
- `dpif/show`, `dpif/show-dp-features` — datapath feature flags.
- `dpif-netdev/pmd-stats-show`, `pmd-rxq-show`, `pmd-rxq-rebalance` — DPDK PMD telemetry.
- `tnl/neigh/show`, `tnl/arp/show`, `tnl/ports/show` — tunnel neighbor tables.
- `upcall/show`, `upcall/set-flow-limit N` — upcall pressure.
- `revalidator/wait`, `revalidator/purge` — flow-eviction plumbing.
- `coverage/show`, `memory/show`, `vlog/list`, `vlog/set m:d:l`, `vlog/reopen` — telemetry.

## Chapters S / T / U / V / W — Libvirt, Docker, security, sandbox, BSD/Windows (compressed)

**Libvirt + OVS**: set `<interface type='bridge'>` with `<virtualport type='openvswitch'/>` and `<source bridge='br-int'/>`. Libvirt inserts the interface into OVS and tags the `Interface.external_ids` with `attached-mac` and `iface-id` — the latter is how OVN finds the port. Troubleshoot VIF plug with `ovs-vsctl list Interface | grep -A2 vnet`.

**Docker + OVS**: the `ovs-docker` helper (`ovs-docker add-port br0 eth0 <container>` / `del-port` / `set-vlan` / `set-addr`) sets up netns-side veths. For production, plug containers manually with `ip link add ... type veth peer` and `ovs-vsctl add-port br0 veth0`, tagging `external_ids:container_id`.

**Security baseline**: `/etc/openvswitch` owned by `openvswitch:openvswitch` mode 0750; `/var/run/openvswitch` 0755; the key.pem 0400. Run the daemons as non-root where your distro supports it. SELinux/AppArmor profiles ship with the distro packages — do not disable them without replacement. Use TLS for every Manager and Controller; use IPsec (Chapter 12) for every tunnel traversing an untrusted network.

**Testing with ovs-sandbox**: the `tutorial/ovs-sandbox` script in the source tree boots a transient `ovsdb-server` + `ovs-vswitchd` pair in `/tmp` with `datapath_type=dummy`, allowing full flow-table development without a kernel module. `ovs-testcontroller` is a learning-switch controller useful for reproducing bug reports.

**Windows and OpenBSD ports**: OVS runs on Windows with a Hyper-V extensible-switch chuyển tiếp extension; on OpenBSD and NetBSD with userspace datapaths. Both ports lack DPDK and AF_XDP. Operationally they are managed with the same `ovs-vsctl` / `ovs-ofctl` tools.

**Sources:** `https://docs.openvswitch.org/en/latest/howto/libvirt/`, `https://docs.openvswitch.org/en/latest/howto/docker/`, `https://docs.openvswitch.org/en/latest/topics/selinux/`, `https://docs.openvswitch.org/en/latest/topics/windows/`.

---

# Phần III — OpenFlow in OVS

## Chapter 5 — Flow syntax grammar

Every `ovs-ofctl add-flow` takes a flow spec: a comma-separated list of khớp với fields, a literal `actions=`, and a comma-separated action list. Selectors that apply to the flow itself live alongside the matches: `table=N`, `priority=N` (0–65535, default 32768), `cookie=HEX`, `idle_timeout=N`, `hard_timeout=N`, `importance=N`, `send_flow_rem`, `check_overlap`. Always pass `-O OpenFlow13` (or higher) when you use multi-table pipeline, groups, or meters, because OVS defaults to OpenFlow 1.0.

```bash
ovs-ofctl -O OpenFlow13 add-flow br0 \
  "table=0,priority=100,in_port=1,dl_type=0x0800,actions=goto_table:10"
```

## Chapter 6 — Match fields

Layer 2: `in_port`, `dl_src`, `dl_dst`, `dl_type`, `dl_vlan`, `dl_vlan_pcp`. Layer 3 IPv4: `nw_src`, `nw_dst`, `nw_proto`, `nw_tos`, `nw_ttl`. Layer 4: `tp_src`, `tp_dst`, `tcp_flags`, `icmp_type`, `icmp_code`. IPv6: `ipv6_src`, `ipv6_dst`. Tunnel metadata: `tun_id`, `tun_src`, `tun_dst`, `tun_flags`. Conntrack: `ct_state`, `ct_zone`, `ct_mark`, `ct_label`, `ct_nw_src`, `ct_nw_dst`, `ct_tp_src`, `ct_tp_dst`. Registers: `reg0`..`reg15`, `xreg0`..`xreg7`, `xxreg0`..`xxreg3`, plus the OpenFlow-standard `metadata`. Masked matches use CIDR or `/mask` for IPs and slash-mask for MACs: `nw_src=10.0.0.0/8`, `dl_src=00:11:22:00:00:00/ff:ff:ff:00:00:00`.

`ct_state` is a bitfield: `+trk` (tracked), `+new` (packet đầu tiên of a new conn), `+est` (established), `+rel` (related, e.g. ICMP error), `+inv` (invalid), `+rpl` (reply direction), `+snat`, `+dnat`. Combine with `+` and `-`: `ct_state=+trk+new-inv`.

## Chapter 7 — Actions

Output variants: `output:N`, `NORMAL`, `FLOOD`, `ALL`, `LOCAL`, `IN_PORT`, `CONTROLLER[:max_len]`, `drop`. Header modification: `mod_vlan_vid:N`, `mod_vlan_pcp:N`, `strip_vlan`, `push_vlan:0x8100`, `pop_vlan`, `mod_dl_src`, `mod_dl_dst`, `mod_nw_src`, `mod_nw_dst`, `mod_nw_tos`, `mod_nw_ttl`, `dec_ttl`, `mod_tp_src`, `mod_tp_dst`. General field ops: `set_field:VALUE->FIELD`, `load:VALUE->FIELD`, `move:SRC->DST`. Pipeline: `resubmit([PORT],[TABLE])`, `goto_table:N`, `group:N`, `meter:N`. Stateful: `learn(...)`, `ct(commit,zone=N,nat(src=IP),table=N,exec(...))`, `ct_clear`. Queue: `set_queue:N`, `pop_queue`. MPLS: `push_mpls:0x8847`, `pop_mpls:0x0800`, `dec_mpls_ttl`. Advanced: `multipath`, `hash`, `bundle`, `sample`, `conjunction(id,k/n)`, `note:`, `exit`, `clone(...)`, `encap(...)`/`decap()`, `check_pkt_larger`, `truncate`.

Groups: `ovs-ofctl -O OpenFlow13 add-group br0 "group_id=1,type=select,bucket=weight=50,output:1,bucket=weight=50,output:2"`. Types are `all` (multicast), `select` (ECMP), `indirect` (a pointer), `fast_failover` (live/dead link failover).

Meters: `ovs-ofctl -O OpenFlow13 add-meter br0 "meter=1,kbps,band=type=drop,rate=1000,burst_size=100"`, then `actions=meter:1,NORMAL`.

## Chapter 8 — Multi-table pipeline and the advanced 5-table tutorial

The upstream advanced tutorial builds a VLAN-aware MAC-learning switch in five stages: (0) admission control — drop multicast-source MACs and BPDU range `01:80:c2:00:00:00/ff:ff:ff:ff:ff:f0`; (1) VLAN input processing — push the access VLAN for untagged ingress, validate trunk VLAN membership for tagged ingress; (2) MAC+VLAN learning — the `learn(...)` action writes a flow into table 10 that remembers the `(VLAN, source MAC) → ingress port` mapping; (3) destination lookup — match `(VLAN, dst MAC)` in table 10 and load the output port into `reg0`; (4) output processing — read `reg0`, flood if unknown, strip the tag for access egress, preserve for trunk egress. The `learn(...)` syntax is verbatim:

```
learn(table=10, hard_timeout=300, NXM_OF_VLAN_TCI[0..11],
      NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],
      load:NXM_OF_IN_PORT[]->NXM_NX_REG0[0..15])
```

Run `ovs-appctl ofproto/trace br0 "in_port=1,dl_vlan=20,dl_src=50:00:00:00:00:01,dl_dst=ff:ff:ff:ff:ff:ff" -generate` to execute side effects, then `ovs-ofctl -O OpenFlow13 dump-flows br0 table=10` to see the learned flow:

```
table=10, vlan_tci=0x0014/0x0fff,dl_dst=50:00:00:00:00:01 actions=load:0x1->NXM_NX_REG0[0..15]
```

This is the single most pedagogically valuable exercise in the entire OVS curriculum.

**Sources:** `https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/`.

## Chapter 9 — Connection tracking

`ct()` sends a packet into the Linux (or userspace) conntrack module and optionally reinjects it. Without `commit` it is a read; with `commit` it writes an entry that outlives the packet. The five-flow canonical stateful firewall — verbatim from the tutorial — allows new outbound TCP from `veth_l0` and admits only established traffic back:

```
ovs-ofctl add-flow br0 "table=0,priority=50,ct_state=-trk,tcp,in_port=veth_l0,actions=ct(table=0)"
ovs-ofctl add-flow br0 "table=0,priority=50,ct_state=+trk+new,tcp,in_port=veth_l0,actions=ct(commit),veth_r0"
ovs-ofctl add-flow br0 "table=0,priority=50,ct_state=-trk,tcp,in_port=veth_r0,actions=ct(table=0)"
ovs-ofctl add-flow br0 "table=0,priority=50,ct_state=+trk+est,tcp,in_port=veth_r0,actions=veth_l0"
ovs-ofctl add-flow br0 "table=0,priority=50,ct_state=+trk+est,tcp,in_port=veth_l0,actions=veth_r0"
```

Observe the resulting conntrack entry with `ovs-appctl dpctl/dump-conntrack`. Zones (`ct(zone=N)`) isolate overlapping address ranges. NAT is `ct(commit,nat(src=192.168.1.1))` or `nat(dst=10.0.0.1:80)`. The `force` option terminates any existing connection in the current direction and starts a new one.

**Sources:** `https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/`.

## Chapter 10 — Flow-table hygiene: monitor, replace-flow, diff-flow

`ovs-ofctl monitor br0 watch:` streams live flow modifications to stdout — leave it running during application debugging. `ovs-ofctl replace-flows br0 new.flows` atomically swaps the entire flow table (versus `add-flows` which just appends). `ovs-ofctl diff-flows br0 new.flows` shows what would change without applying it — always run this in production before `replace-flows`.

---

# Phần IV — Tunneling and Overlays

## Chapter 11 — VXLAN, Geneve, GRE walkthrough

Already covered syntactically in Chapter J. What matters operationally is the interplay with `set_tunnel:` when `options:key=flow`: a single tunnel port can reach any remote endpoint, with the OpenFlow pipeline selecting the VNI and the underlay picking the destination via ARP/ND resolution through the kernel routing table. This is the OVN model.

## Chapter 12 — IPsec for tunnels

`ovs-monitor-ipsec` watches the `Interface.options:psk` or `Interface.options:remote_cert` columns and programs strongSwan or Libreswan accordingly. Enable IPsec on a VXLAN port:

```bash
ovs-vsctl add-port br0 vxlan-ipsec -- set Interface vxlan-ipsec \
  type=vxlan options:remote_ip=10.0.0.2 options:key=flow options:psk=mysecret
systemctl enable --now openvswitch-ipsec
```

Verify with `ipsec statusall` on both ends. Always rotate the PSK, or better still use the PKI path with `options:remote_cert=...`.

## Chapter 13 — Tunnel troubleshooting flowchart

Tunnel comes up but no traffic: check MTU first (`ip link show`, shrink inner MTU). Traffic in one direction only: check underlay routing, reverse path filter (`sysctl net.ipv4.conf.all.rp_filter`). Intermittent drops: check firewall state on an intermediate NAT. OVS shows the tunnel down: check `ovs-appctl tnl/neigh/show` and underlay ARP.

---

# Phần V — Performance and Scale

## Chapter 14 — DPDK

Enable with `ovs-vsctl set Open_vSwitch . other_config:dpdk-init=true`, restart `ovs-vswitchd`, then create a `datapath_type=netdev` bridge and `type=dpdk` ports:

```bash
ovs-vsctl add-br br-dpdk -- set Bridge br-dpdk datapath_type=netdev
ovs-vsctl add-port br-dpdk p0 -- set Interface p0 type=dpdk \
                                    options:dpdk-devargs=0000:01:00.0
```

Tune with `other_config:dpdk-socket-mem=1024,1024`, `dpdk-lcore-mask=0x2`, `pmd-cpu-mask=0x3c`. Monitor with `ovs-appctl dpif-netdev/pmd-stats-show` and `dpif-netdev/pmd-rxq-show`. Enable detailed perf metrics (`other_config:pmd-perf-metrics=true`) and read with `dpif-netdev/pmd-perf-show`. Pin RX queues with `ovs-vsctl set Interface p0 other_config:pmd-rxq-affinity="0:2,1:4"`. The EMC insertion probability knob (`emc-insert-inv-prob`) controls how aggressively flow populate the exact-match cache — set to 0 for many-parallel-flow workloads to force reliance on megaflow.

## Chapter 15 — AF_XDP

`type=afxdp` with `options:xdp-mode=native` (or `skb`/`hw`) gives DPDK-class chuyển tiếp using the kernel's XDP infrastructure without userspace drivers. Requires a recent kernel and libbpf. The administrative tradeoff is portability and kernel integration versus the raw băng thông thực tế ceiling of DPDK.

## Chapter 16 — Hardware offload via tc-flower

`ovs-vsctl set Open_vSwitch . other_config:hw-offload=true` (then restart) directs OVS to cài đặt megaflows into the NIC's tc-flower chain. Verify with `tc -s filter show dev ethX ingress` and `ovs-appctl dpctl/dump-flows -m type=offloaded`. Mellanox ConnectX-5/6 and the Netronome Agilio are the canonical offload-capable NICs. The `dpctl/offload-stats-show` target reports enqueued, inserted, and in-flight offload counts plus per-insertion độ trễ histograms.

---

# Phần VI — OVN Topic Chapter

## Chapter 17 — OVN as a topic

OVN sits above OVS as a logical networking controller. Its architecture is three tiers: `ovn-nbctl` on operators' desks writes logical ý đồ cấu hình into the Northbound DB; `ovn-northd` translates logical ý đồ cấu hình into logical flow in the Southbound DB; `ovn-controller` on each hypervisor reads the SB, translates relevant logical flow into OpenFlow for the local `br-int`, and programs local port bindings. Key NB tables: `Logical_Switch`, `Logical_Switch_Port`, `Logical_Router`, `Logical_Router_Port`, `Logical_Router_Static_Route`, `ACL`, `NAT`, `Load_Balancer`. Key SB tables: `Chassis`, `Port_Binding`, `MAC_Binding`, `Datapath_Binding`, `Logical_Flow`.

Essential `ovn-nbctl` subcommands: `ls-add`, `lsp-add`, `lsp-set-addresses`, `lsp-set-port-security`, `lr-add`, `lrp-add`, `lr-route-add`, `lr-nat-add`, `acl-add`, `lb-add`. Essential `ovn-sbctl`: `show`, `lflow-list`, `chassis-list`. Always run NB and SB as Raft clusters (Chapter N).

---

# Phần VII — Production Operations

## Chapter 18 — Observability stack

Feed sFlow into goflow2 or ntopng for traffic analytics; scrape `ovs_exporter` for Prometheus metrics on interface stats, flow counts, and PMD utilization; run `ovs-appctl coverage/show` on a cron and log deltas to phát hiện abnormal upcall or netlink rates.

## Chapter 19 — Upgrade choreography

Revisited from Chapter P. Three golden rules: schema first (convert DB before starting the new binary), one daemon at a time, never simultaneously upgrade OVS and the kernel on the same host.

## Chapter 20 — Incident response decision tree

1. Packet loss → `ovs-dpctl show` → check `lost` counter → `upcall/show` → raise flow limit or n-handler-threads.
2. Unexpected drops → `ovs-appctl ofproto/trace` with the offending flow → identify which table is dropping.
3. Tunnel down → `tnl/neigh/show` → underlay connectivity → MTU.
4. Bond flap → `bond/show` + `lacp/show` → physical switch LACP config.
5. OVSDB unavailable → `cluster/status` on each member → bring quorum back.

---

# Appendices

## Appendix A — Command cheat-sheet

```
ovs-vsctl show / list-br / list-ports BR / add-br / del-br / add-port / del-port
         set-controller BR TARGET / set-fail-mode BR secure|standalone
         set / get / add / remove / clear / create / destroy TABLE ROW COL[:KEY]=VAL
ovs-ofctl -O OpenFlow13 show BR / dump-ports BR / dump-flows BR [MATCH]
         add-flow / mod-flows / del-flows / replace-flows / diff-flows / monitor
         add-group / add-meter / dump-groups / dump-meters
ovs-appctl vlog/list | vlog/set M:D:L | vlog/reopen
          coverage/show | memory/show | upcall/show | fdb/show BR
          bond/show | lacp/show | stp/show | rstp/show
          ofproto/trace BR "FLOW" [-generate]
          dpctl/show | dpctl/dump-flows -m | dpctl/dump-conntrack
          dpif-netdev/pmd-stats-show | pmd-rxq-show | pmd-rxq-rebalance
          tnl/neigh/show | tnl/arp/show | tnl/ports/show
          cluster/status DB | cluster/leave DB | cluster/kick DB SID
ovs-dpctl show | dump-flows -m
ovsdb-tool create | create-cluster | join-cluster | compact | convert | show-log
ovsdb-client list-dbs | get-schema | dump | transact | monitor | backup | restore
```

## Appendix B — OVSDB schema quick reference (vswitchd)

`Open_vSwitch` (singleton): `bridges`, `manager_options`, `ssl`, `other_config`, `external_ids`, `db_version`, `ovs_version`, `system_type`. `Bridge`: `name`, `ports`, `controller`, `fail_mode`, `protocols`, `datapath_type`, `datapath_id`, `mirrors`, `netflow`, `sflow`, `ipfix`, `flow_tables`, `stp_enable`, `rstp_enable`, `mcast_snooping_enable`, `other_config` (keys: `mac-aging-time`, `mac-table-size`, `hwaddr`, `forward-bpdu`, `datapath-id`, `disable-in-band`). `Port`: `name`, `interfaces`, `tag`, `trunks`, `vlan_mode`, `bond_mode`, `lacp`, `bond_updelay`, `bond_downdelay`, `qos`, `mac`, `other_config` (`bond-rebalance-interval`, `lacp-time`, `lacp-fallback-ab`). `Interface`: `name`, `type`, `options` (tunnel and DPDK options), `ofport`, `ofport_request`, `mtu`, `mtu_request`, `admin_state`, `link_state`, `mac_in_use`, `statistics`, `ingress_policing_rate`, `ingress_policing_burst`, `external_ids` (`iface-id`, `attached-mac`). `QoS`: `type`, `queues` (map of queue-id → Queue UUID), `other_config` (`max-rate`, `cir`, `cbs`, `eir`, `ebs`). `Queue`: `dscp`, `other_config` (`min-rate`, `max-rate`, `priority`, `burst`). `Mirror`: `name`, `select_all`, `select_src_port`, `select_dst_port`, `select_vlan`, `output_port`, `output_vlan`, `snaplen`, `statistics`. `sFlow`: `agent`, `targets`, `header`, `sampling`, `polling`. `NetFlow`: `targets`, `active_timeout`, `engine_id`, `engine_type`, `add_id_to_interface`. `IPFIX`: `targets`, `obs_domain_id`, `obs_point_id`, `cache_active_timeout`, `cache_max_flows`, `sampling`. `Controller` / `Manager`: `target`, `connection_mode`, `role`, `is_connected`, `inactivity_probe`, `max_backoff`, `other_config`. `SSL`: `private_key`, `certificate`, `ca_cert`, `bootstrap_ca_cert`.

## Appendix C — Troubleshooting decision tree

Compressed form: *Are packet arriving? → tcpdump on physical NIC. Are they entering OVS? → `dpctl/dump-flows -m` hit counters. Are the right flow matching? → `ofproto/trace`. Is the action correct? → read the Datapath actions line. Does the datapath agree? → `dpctl/dump-flows` on the actual kernel/netdev. Does the wire agree? → tcpdump on egress NIC. When all four agree and packet still drop → upstream switch.*

## Appendix D — Bibliography and verified source URLs

- `https://docs.openvswitch.org/en/latest/intro/install/` (installation index and sub-pages for Fedora, RHEL, Debian, DPDK, userspace, Windows, OpenBSD, NetBSD)
- `https://docs.openvswitch.org/en/latest/howto/` (kvm, libvirt, qos, sflow, tunneling, userspace-tunneling, lisp, ssl, firewalld, selinux, docker, windows)
- `https://docs.openvswitch.org/en/latest/topics/` (bonding, datapath, dpdk/*, high-availability, ovsdb-replication, role-based-access-control, userspace-tso, userspace-checksum-offloading, selinux, tracing, windows, language-bindings, openflow, ovs-extensions, porting, integration)
- `https://docs.openvswitch.org/en/latest/ref/ovs-vsctl.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-vswitchd.conf.db.5/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-ofctl.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-appctl.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-dpctl.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-fields.7/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-vswitchd.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-pki.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovs-testcontroller.8/`
- `https://docs.openvswitch.org/en/latest/ref/ovsdb.7/`
- `https://docs.openvswitch.org/en/latest/ref/ovsdb-server.7/`
- `https://docs.openvswitch.org/en/latest/ref/ovsdb-tool.1/`
- `https://docs.openvswitch.org/en/latest/ref/ovsdb-client.1/`
- `https://docs.openvswitch.org/en/latest/faq/` (general, configuration, vlan, qos, openflow, vxlan, issues, releases)
- `https://docs.openvswitch.org/en/latest/tutorials/faucet/`
- `https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/`
- `https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/`
- `https://docs.openvswitch.org/en/latest/tutorials/ovsdb-cluster/`
- `https://docs.openvswitch.org/en/latest/tutorials/ipsec/`
- `https://man7.org/linux/man-pages/man8/ovs-vsctl.8.html`
- `https://man7.org/linux/man-pages/man8/ovs-ofctl.8.html`
- `https://man7.org/linux/man-pages/man8/ovs-appctl.8.html`
- `https://man7.org/linux/man-pages/man8/ovs-vswitchd.8.html`
- `https://www.openvswitch.org/support/dist-docs/ovsdb-tool.1.html`
- `https://docs.ovn.org/en/latest/` (OVN Northbound, Southbound, nbctl, sbctl references)

---

## Closing note to the reader

You now have a single reference from which you can bring up OVS from packages, configure bridges, ports, bonds, mirrors, QoS, tunnels, and monitoring from `ovs-vsctl` alone; program any OpenFlow pipeline that OVS supports with `ovs-ofctl`; diagnose any production incident with `ovs-appctl`; cluster OVSDB for HA; offload to DPDK, AF_XDP, or tc-flower; and operate OVN on top. Every command in this book is traceable to the upstream docs. When in doubt, return to the URLs in Appendix D: they are, and will remain, the ground truth.

*End of curriculum.*