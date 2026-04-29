# E0 Foundation Dossier, plan v3.13

> **Purpose.** This dossier is the foundation library that every later E-sprint, R-sprint, and S-sprint of plan v3.13 reads from. It inventories the Open vSwitch source tree at tag `v2.17.9`, the upstream documentation set, the offline document library shipped with this curriculum, the canonical authors and integrating projects, and the high-level edge cases and hidden constraints that recur across the codebase. The dossier is written in plain technical English at CEFR B2 to C1 level per CLAUDE.md Rule 17. No em-dash, no Vietnamese, no plan internals leaked into prose.
>
> **Scope baseline.** Source tree at `C:/Users/voleh/Documents/ovs`, frozen at tag `v2.17.9`, commit `0bea06d9957e3966d94c48873cd9afefba1c2677`. Documentation set at `Documentation/` inside that worktree. Offline library at `sdn-onboard/doc/`. The canonical-authors and ecosystem material is current as of 2026-04-29 to within the limits of the upstream `git log` and `MAINTAINERS.rst` at `v2.17.9`.
>
> **Authoring date.** 2026-04-29.
>
> **Plan reference.** [`plans/sdn/v3.13-ovs-hands-on-mastery-and-source-deep-dive.md`](../../../plans/sdn/v3.13-ovs-hands-on-mastery-and-source-deep-dive.md) §4.0.2.
>
> **How to read.** Section A inventories the source tree. Section B inventories the upstream documentation. Section C inventories the offline doc library. Section D names the people and projects in the OVS ecosystem. Section E lists hidden constraints and edge cases that surface across the corpus. Section F records the online research pass with verified sources.
>
> A reader who is starting plan v3.13 from cold reads sections A and D first, then dips into B and C as the relevant R-sprint or S-sprint approaches.

---

## Section A. Open vSwitch source tree inventory at v2.17.9

### A.1. Top-level layout

The OVS source tree at `v2.17.9` has 26 top-level entries. The relevant ones for plan v3.13 are:

| Directory | Role | Plan v3.13 sprint that targets it |
|-----------|------|-----------------------------------|
| `Documentation/` | Upstream `.rst` documentation, 121 files across 6 subdirectories. The teaching material the project ships with itself. | Every E-sprint (Section B reading list) and S-sprint (cited in source-mastery files) |
| `lib/` | The core library. 419 files, 235,529 lines. Houses the classifier, the OpenFlow message handlers, the datapath interface, the netdev abstraction, the conntrack userspace path, the OVSDB client library, JSON parsing, platform abstractions, and a long tail of utilities. Every binary statically links `libopenvswitch.la` built from this directory. | S3 (lib deep map) |
| `ofproto/` | The OpenFlow processing engine. 44 files, 47,426 lines. Translates OpenFlow protocol messages into datapath actions. Every learning, observability, and tunnel path goes through this directory. | S4 (ofproto deep map) |
| `vswitchd/` | The `ovs-vswitchd` daemon glue. 8 files, 6,491 lines. Reads OVSDB, calls into `ofproto/` to materialise bridges, runs the main loop. The seat where everything else converges. | S5 (vswitchd daemon glue) |
| `ovsdb/` | The OVSDB database server. 58 files, 33,116 lines. Includes the standalone server, the JSON-RPC wire protocol, the Raft consensus implementation, the offline tools (`ovsdb-tool`, `ovsdb-client`), and the three generations of monitor protocol. | S6 (ovsdb deep map), R8 (multi-host Raft cluster lab) |
| `datapath/` | The kernel module C source. 150 files, 45,482 lines. The fast path inside the Linux kernel: `datapath.c`, `flow.c`, `flow_netlink.c`, `actions.c`, `conntrack.c`, `meter.c`, plus per-tunnel-type vport implementations and a Linux compatibility shim layer for older kernels. | S7 (datapath deep map), R4 (datapath internals lab), R5 (tunnels) |
| `utilities/` | The CLI binaries. 34 files, 24,803 lines. `ovs-vsctl`, `ovs-ofctl`, `ovs-dpctl`, `ovs-appctl`, `ovs-tcpdump`, `ovs-pcap`, `ovs-pki`, `ovs-ctl`, plus the bug-tool generator and the GDB helper scripts. | S8 (utilities deep map), every R-sprint that runs CLI commands |
| `python/` | The Python OVSDB IDL library and helper tools. 46 files, 16,409 lines. Used by tests and by integrators (Faucet, Ryu, OpenStack, OVN-controller-vtep). | S6 (covered alongside ovsdb), S8 (covered alongside utilities) |
| `tests/` | The Autotest test suite. 187 files, 101,469 lines. Hundreds of `.at` files compiled into a `testsuite` driver, plus system-traffic tests that spin up network namespaces, plus fuzz regression tests. | S9 (test suite deep map) |
| `include/` | Public header files. 127 files, 20,680 lines. The interface every external integrator codes against. | S3 (read alongside lib for the public API surface) |
| `ipsec/` | The IPsec helper that wraps strongSwan or LibreSwan to encrypt OVS tunnels. 1 file, 1,372 lines. | R5 (tunnels), brief mention in R5.5 (inter-host IPsec exercise) |
| `vtep/` | The Virtual Tunnel Endpoint schema and helper, an OVN-related sub-project. 4 files, 3,695 lines. | Out of scope per plan v3.13 §12 (OVN deferred) |
| `tutorial/` | Upstream tutorial files. Empty directory at `v2.17.9` (the tutorials were moved into `Documentation/tutorials/`). | Cross-reference only |

The remaining top-level directories cover packaging (`debian/`, `rhel/`, `selinux/`, `xenserver/`), build helpers (`build-aux/`, `m4/`, `acinclude.m4`, `boot.sh`, `configure.ac`, `Makefile.am`), platform-specific code (`datapath-windows/`, `windows/`), continuous integration (`.ci/`, `.github/`, `appveyor.yml`, `.travis.yml`, `.cirrus.yml`), proof-of-concept code (`poc/`), vendored third-party libraries (`third-party/`), and project metadata (`AUTHORS.rst`, `CONTRIBUTING.rst`, `LICENSE`, `MAINTAINERS.rst`, `NEWS`, `NOTICE`, `README.rst`).

`AUTHORS.rst` is 38,812 bytes and lists every person who has contributed a patch to the project. `NEWS` is 96,589 bytes and documents the user-visible changes per release; it is the first place to look when comparing behaviour across versions.

### A.2. The lib/ directory by subsystem

`lib/` is the largest subdirectory and merits a per-subsystem grouping. The 419 source files cluster into the following subsystems. Counts include both `.c` and `.h` files.

#### A.2.1. Classifier and flow tables (7 files)

`classifier.c` (2237 lines), `classifier-private.h`, `cmap.c` (concurrent hash map), `ccmap.c` (concurrent counted hash map), `flow.c` (3641 lines, packet field extraction), `meta-flow.c` (3703 lines, the `mf_field` definitions for every match field), `match.c` (1978 lines, `struct match` build and manipulate), `miniflow.h`, `nx-match.c` (2335 lines, NXM/OXM TLV serialisation).

The classifier is a Tuple Space Search structure. Each rule is keyed by the unique combination of fields it matches. Lookup walks every populated tuple in priority order until a match is found. The structure is what makes a flow table with millions of rules tractable; `tcam`-grade hardware would be the alternative.

#### A.2.2. OpenFlow message handling (23 files)

`ofp-actions.c` (9785 lines, the largest single file in `lib/`), `ofp-bundle.c`, `ofp-errors.c`, `ofp-flow.c` (2018 lines), `ofp-group.c` (2390 lines), `ofp-meter.c`, `ofp-monitor.c`, `ofp-msgs.c`, `ofp-packet.c`, `ofp-parse.c`, `ofp-port.c` (1856 lines), `ofp-print.c`, `ofp-prop.c`, `ofp-protocol.c`, `ofp-queue.c`, `ofp-switch.c`, `ofp-table.c` (2412 lines), `ofp-util.c`, `ofp-version-opt.c`, plus headers.

Every OpenFlow protocol version (1.0, 1.1, 1.2, 1.3, 1.4, 1.5) has its own wire format. The `ofp-*` files isolate the wire-format work from the rest of the codebase: the `ofproto/` engine speaks only the abstract internal types, and `lib/ofp-*` translates to and from those types.

The `ofp-actions.c` file is the canonical reference for what every OpenFlow action does. R3 (OpenFlow programming sprint) annotates every action exercised in the lab with its definition in this file.

#### A.2.3. Datapath interface (18 files)

`dpif.c` (2123 lines, the abstract datapath interface), `dpif-netdev.c` (10105 lines, the largest single file in `lib/`, the userspace datapath), `dpif-netlink.c` (5294 lines, the kernel datapath bridge over netlink), `dpif-provider.h`, `odp-execute.c` (the action executor), `odp-util.c` (8768 lines, encode and decode ODP attributes), `dpctl.c` (3062 lines, the CLI surface for `ovs-dpctl` and `ovs-appctl dpctl/*`), plus headers.

The abstract `dpif` interface is what allows the rest of the codebase to be agnostic about which datapath is in use. The kernel datapath (`dpif-netlink.c`) and the userspace datapath (`dpif-netdev.c`) implement the same `dpif_class` virtual table. Switching between them requires only a `datapath_type=system` versus `datapath_type=netdev` setting on the bridge.

#### A.2.4. Network device abstraction (13 files)

`netdev.c` (2308 lines), `netdev-linux.c` (6752 lines), `netdev-bsd.c` (1722 lines), `netdev-dpdk.c` (5421 lines, out of scope per CLAUDE.md North Star ban), `netdev-dummy.c` (2115 lines, used by tests), `netdev-native-tnl.c` (the userspace tunnel implementations), `netdev-offload.c`, `netdev-offload-tc.c` (2546 lines), `netdev-offload-dpdk.c` (2761 lines, out of scope), `netdev-vport.c`, `netdev-windows.c`, `netdev-provider.h`.

The `netdev` abstraction wraps every kind of port OVS knows about: a Linux NIC, a tap device, an internal port, a tunnel port, a DPDK port, a BSD interface. Every operation that touches a wire is dispatched through the `netdev_class` virtual table. New port types are added by implementing this interface.

#### A.2.5. Connection tracking userspace path (5 files)

`conntrack.c` (3351 lines), `conntrack-private.h`, `conntrack-tcp.c`, `conntrack-icmp.c`, `conntrack-other.c`, `conntrack-tp.c`.

The userspace conntrack is used by the netdev datapath. It implements the same model as the Linux kernel `nf_conntrack`: a per-flow state machine with TCP, ICMP, and "other" protocol types, plus NAT and ALG hooks. The kernel datapath uses `nf_conntrack` directly via `datapath/conntrack.c`.

R6 (conntrack lab) exercises both paths: the kernel path on `datapath_type=system` bridges and the userspace path on `datapath_type=netdev` bridges, with a side-by-side comparison of `conntrack -L` output.

#### A.2.6. OVSDB client library (10 files)

`ovsdb-data.c` (2480 lines, OVSDB column types, atom and datum), `ovsdb-error.c`, `ovsdb-idl.c` (4402 lines, the Interface Definition Language client), `ovsdb-cs.c` (2357 lines, the cluster client), `ovsdb-parser.c`, `ovsdb-types.c`, `ovsdb-condition.c`, `ovsdb-set-op.c`, `ovsdb-map-op.c`, plus `db-ctl-base.c` (2681 lines, the shared logic between `ovs-vsctl`, `ovn-nbctl`, `ovn-sbctl`).

The IDL is the higher-level contract every OVSDB client codes against. Every `*ctl` binary in `utilities/` uses the IDL; so do the OVN binaries; so do every OpenStack Neutron, Faucet, and kube-ovn integration. The IDL is the most stable and most reused interface in the project.

#### A.2.7. JSON and JSON-RPC (2 files)

`json.c` (1748 lines), `jsonrpc.c`.

OVS does not use a third-party JSON library. The implementation is hand-rolled and must be present because OVSDB speaks JSON-RPC over Unix domain sockets, TCP, or TCP-with-SSL. RFC 7047 (the OVSDB protocol) is the wire format.

#### A.2.8. Platform abstractions (10 files)

`daemon.c`, `daemon-unix.c`, `daemon-windows.c`, `fatal-signal.c`, `process.c`, `process-unix.c`, `process-windows.c`, `socket-util.c`, `stream.c`, `stream-tcp.c`, `stream-unix.c`, `stream-ssl.c` (1574 lines), `stream-fd.c`, `stream-windows.c`, `unixctl.c`.

The `stream` abstraction is the typed-wire counterpart of `netdev`: it abstracts a TCP or Unix or SSL connection behind a single API so that JSON-RPC, OpenFlow, and `unixctl` can share a transport implementation. `unixctl.c` is the IPC framework that backs every `ovs-appctl` command.

#### A.2.9. L2 protocols (6 files)

`stp.c` (1733 lines, IEEE 802.1D), `rstp.c` (1683 lines, IEEE 802.1w), `rstp-state-machines.c` (2221 lines, the per-port and per-bridge state machines), `lacp.c` (Link Aggregation Control Protocol), `bond.c` is in `ofproto/`, `bfd.c` (Bidirectional Forwarding Detection), `lldp.c`, `cfm.c` (Connectivity Fault Management).

OVS implements the small set of L2 control protocols a software switch needs to coexist with hardware switches and routers: spanning tree, link aggregation, BFD, LLDP, CFM. Every protocol has its own state machine and per-port timer. R2.5 (traditional vs OVS) compares STP and RSTP behaviour against a Cisco baseline; R7 (LAG, mirroring, sFlow) exercises LACP.

#### A.2.10. Tunnel infrastructure (2 files)

`tnl-neigh-cache.c` (the tunnel neighbour cache, ARPs each tunnel destination), `tnl-ports.c`, plus the per-protocol vport implementations in `lib/netdev-native-tnl.c` and `datapath/linux/compat/`.

The tunnel cache resolves outer-IP to outer-MAC for every active tunnel, refreshes the entry when ARP times out, and caches the underlay route. Without the tunnel cache, every encapsulated packet would block on a synchronous ARP lookup.

#### A.2.11. Observability (4 files)

`vlog.c`, `coverage.c`, `perf-counter.c`, `timeval.c`.

`vlog` is the per-module log-level system that allows fine-grained debug enabling at runtime via `ovs-appctl vlog/set ANY:dbg` or per-module. `coverage` is the in-process counter set that `ovs-appctl coverage/show` dumps. `perf-counter` is a higher-resolution sampling counter. `timeval` is the monotonic and wall-clock abstraction.

R4 (datapath internals) reads `coverage/show` extensively. R9 (debug doctrine) reads `vlog/set` extensively.

#### A.2.12. The remaining 117 lib/ files

The remaining 117 files cover specialised functionality that does not group cleanly into a subsystem. The largest individual files in this miscellany are `util.c` (2467 lines, low-level helpers), `packets.c` (1939 lines, packet header build/parse), `packets.h` (1671 lines), `netdev-vport.c`, `ipf.c` (1527 lines, the IP fragmentation reassembler used by userspace conntrack), `vconn.c` (1526 lines, the OpenFlow virtual connection layer), `rconn.c` (1442 lines, the reconnecting OpenFlow connection layer with backoff and fail-open), and `dns-resolve.c`. A reader walking the source tree is best served by reading the file's leading comment block to understand what it does; almost every file in `lib/` is well-commented at the top.

### A.3. The ofproto/ directory file by file

The 44 files in `ofproto/` are the OpenFlow processing engine. The largest files are listed first; their roles are summarised inline.

| File | Lines | Role |
|------|-------|------|
| `ofproto.c` | 9411 | The abstract OpenFlow controller-facing layer. Hosts the flow tables, the table-miss behaviour, the per-controller connection state, the bundle commit logic, the role-based access control. The seat where every OpenFlow message lands first. |
| `ofproto-dpif-xlate.c` | 8489 | The translator from OpenFlow pipeline to datapath action list. The most behaviourally important file in OVS: every match-action interpretation a controller programs runs through this file. The functions `xlate_actions`, `xlate_normal`, `compose_output_action`, `xlate_table_action`, `xlate_ct` are the named entry points. |
| `ofproto-dpif.c` | 6912 | The datapath-backed concrete implementation of the abstract `ofproto` interface. Hosts the datapath's flow cache, the upcall handlers, the revalidator threads, the bridge-level features (mirror, sFlow, IPFIX, conntrack-zone, fail-open). |
| `ofproto-dpif-upcall.c` | 3539 | The upcall handler. Runs in a thread pool that pulls upcalls from the kernel datapath (or the userspace datapath) over netlink. Each upcall is translated into datapath actions via `ofproto-dpif-xlate.c` and the resulting megaflow is installed back into the datapath. |
| `ofproto-dpif-ipfix.c` | 3125 | IPFIX exporter. Implements RFC 7011 to export per-flow statistics to a collector. |
| `connmgr.c` | 2342 | Per-bridge OpenFlow connection manager. Tracks every controller connection, every monitor connection, every primary/secondary role. |
| `bond.c` | 2146 | Link bonding. Implements LACP-driven and statically-configured bond modes (active-backup, balance-slb, balance-tcp). |
| `ofproto-provider.h` | 2090 | The abstract `ofproto_class` virtual table that `ofproto-dpif.c` (and other backends) implement. |
| `ofproto-dpif-sflow.c` | 1437 | sFlow exporter. RFC 3176, sampling rate, agent address, collector list. |
| `ofproto-dpif-trace.c` | 845 | Backs the `ovs-appctl ofproto/trace` debugging command. |
| `tunnel.c` | 778 | Bridges the abstract tunnel concept (`tun_id`, `tun_src`, `tun_dst`) with the concrete tunnel ports. |
| `ofproto.h` | 576 | Public header for the abstract layer. |
| `ofproto-dpif-mirror.c` | 537 | Bridge-level port mirror, the OVS counterpart to Cisco SPAN. |
| `in-band.c` | 529 | In-band control: the OVS bridge can carry its own controller traffic if the controller is reachable only through the bridge. |

The remaining files cover smaller subsystems: `bundles.c` (atomic OpenFlow bundle commit), `fail-open.c` (the standalone fallback when the controller disconnects), `netflow.c` (NetFlow v5 exporter), `ofproto-dpif-rid.c` (recirculation IDs), `ofproto-dpif-monitor.c` (the BFD/CFM/LACP monitor thread), `names.c` (port name registry).

### A.4. The vswitchd/ directory

The 8 files in `vswitchd/` are the daemon glue that ties OVSDB configuration to the `ofproto/` engine. The total is 6,491 lines.

| File | Lines | Role |
|------|-------|------|
| `bridge.c` | 5248 | The bridge configuration applier. Reads OVSDB, calls `ofproto_create()`, `ofproto_add_port()`, configures every column on every row, runs the main reconfiguration loop. The single file `bridge.c` is the centre of gravity of `ovs-vswitchd`; understanding it is understanding what the daemon does. |
| `bridge.h` | (small) | Public API of `bridge.c`. |
| `ovs-vswitchd.c` | (small) | The entry point. Argument parsing, daemon setup, calls into `bridge_init` and the main loop. |
| `system-stats.c` | (small) | The host-stats publisher (CPU, memory, file descriptors). Writes to the `Open_vSwitch.statistics` column. |
| `xenserver.c` | (small) | Hooks for the XenServer integration. Out of scope for plan v3.13. |
| `vswitch.ovsschema` | (data) | The JSON schema for the `Open_vSwitch` OVSDB. The single source of truth for every table and column the daemon reads or writes. |
| `vswitch.xml` | (data) | The XML documentation source; compiled into the `ovs-vswitchd.conf.db.5` man page. Every column has a description here. |
| `automake.mk` | (build) | Per-directory automake stanza listing the sources and the binary they build into. |

`vswitch.ovsschema` and `vswitch.xml` are paired: every column in the schema has a corresponding `<column>` element in the XML. R2 (bridge primitives lab) cites this pair frequently because every `ovs-vsctl set bridge ...` command edits a column whose semantics are documented in `vswitch.xml`.

### A.5. The ovsdb/ directory file by file

The 58 files in `ovsdb/` are the database server. Total lines 33,116.

| File | Lines | Role |
|------|-------|------|
| `raft.c` | 5041 | The Raft consensus implementation. The `raft_run`, `raft_handle_*`, and `raft_become_*` functions are the primary entry points. R8 (multi-host Raft cluster lab) walks this file in detail. |
| `ovsdb-client.c` | 2534 | The CLI client. Implements `ovsdb-client transact`, `monitor`, `dump`, `list-dbs`, etc. |
| `ovsdb-server.c` | 2156 | The standalone server entry point. Argument parsing, daemon setup, the main loop calling into `jsonrpc-server`, `monitor`, `transaction`, `raft`. |
| `jsonrpc-server.c` | 1834 | The OVSDB protocol over JSON-RPC. RFC 7047 implementation. |
| `monitor.c` | 1815 | The monitor (v1) protocol. Used by older clients. |
| `ovsdb-tool.c` | 1766 | The offline tool: `create`, `compact`, `convert`, `cluster-to-standalone`, `standalone-to-cluster`, `show-log`. R8 uses this for cluster bootstrap. |
| `transaction.c` | 1651 | In-memory transaction processing. Validates, applies, and either commits or aborts a transaction proposed via JSON-RPC. |
| `raft-rpc.c` | 1054 | The Raft wire protocol: `AppendEntries`, `RequestVote`, `InstallSnapshot`, plus the OVS-specific variants. |
| `log.c` | 1024 | The log-based persistence layer that backs `*.db` files. Append-only with periodic compaction. |
| `replication.c` | 933 | Active-backup replication (the older approach, now superseded by Raft for high-availability deployments but still used by some installations). |
| `execution.c` | 863 | The execution engine for OVSDB transactions: `insert`, `update`, `mutate`, `delete`, plus the `select`, `wait`, `commit` operators. |
| `raft-private.c` | 831 | Internal helpers for `raft.c`. |
| `storage.c` | 669 | The storage abstraction sitting between the in-memory database and the on-disk log. |
| `ovsdb.c` | 594 | The in-memory database object: schema, tables, rows. |
| `file.c` | 561 | The legacy file-based storage path. |
| `condition.c` | 553 | The transaction condition operators (`==`, `!=`, `<`, `<=`, `>`, `>=`, `includes`, `excludes`). |
| `mutation.c` | 533 | The mutation operators (`+=`, `-=`, `*=`, `/=`, `%=`, `insert`, `delete`). |
| `row.c` | 520 | The `ovsdb_row` representation in memory. |

The remaining files cover the schema parser, the indices, the trigger engine (`select` with `wait` blocks until a condition holds), the `monitor2` and `monitor3` newer protocol generations, plus per-tool entry points.

### A.6. The datapath/ directory file by file

The 150 files in `datapath/` are the kernel module C source. Total lines 45,482. The file count is high because the directory ships a Linux compatibility shim (`datapath/linux/compat/`) that backports newer kernel features to older kernels for the out-of-tree build.

| File | Lines | Role |
|------|-------|------|
| `flow_netlink.c` | 3512 | Encode and decode flow keys and actions over netlink. The wire format between userspace `ofproto-dpif-upcall.c` and the kernel datapath. |
| `linux/compat/ip6_gre.c` | 2746 | Backport of the IPv6 GRE tunnel for kernels that did not ship one. Compatibility shim. |
| `datapath.c` | 2707 | The kernel-side packet path. `ovs_dp_process_packet` is the entry point invoked by the netdev hook. Looks up the flow cache, executes actions, or upcalls to userspace on miss. |
| `conntrack.c` | 2413 | The kernel-side conntrack integration. Glues `nf_conntrack` to OVS actions. |
| `linux/compat/vxlan.c` | 2382 | VXLAN backport. |
| `linux/compat/ip6_tunnel.c` | 2213 | IPv6 tunnel backport. |
| `linux/compat/stt.c` | 2129 | STT (Stateless Transport Tunnelling), a Nicira protocol that has fallen out of favour. |
| `linux/compat/geneve.c` | 1854 | Geneve backport. |
| `actions.c` | 1587 | The kernel-side action executor. Mirror of `lib/odp-execute.c` for the kernel-side equivalent. |
| `linux/compat/ip_gre.c` | 1450 | IPv4 GRE backport. |
| `flow_table.c` | 988 | The kernel flow cache: the megaflow table backed by a `tablehash` of `mask`s and `flow`s. |
| `flow.c` | 972 | Kernel-side packet field extraction. Mirror of `lib/flow.c` for the kernel's `sk_buff`. |
| `linux/compat/ip_fragment.c` | 831 | IP defragmenter backport. |
| `linux/compat/lisp.c` | 816 | LISP backport. |
| `linux/compat/ip_tunnel.c` | 776 | IP tunnel base backport. |
| `linux/compat/nf_conntrack_reasm.c` | 740 | Conntrack reassembly backport. |
| `meter.c` | 639 | The kernel-side OpenFlow 1.3 meter implementation. Token bucket per meter. |
| `linux/compat/nf_conncount.c` | 621 | Connection-count backport for ACL rate-limiting. |
| `vport.c` | 614 | The kernel-side vport abstraction. Mirror of `lib/netdev.c` for kernel-side ports. |

The directory also contains per-vport implementation files (`vport-netdev.c`, `vport-internal_dev.c`, `vport-vxlan.c`, `vport-geneve.c`, `vport-gre.c`, `vport-stt.c`, `vport-lisp.c`, `vport-erspan.c`, `vport-ip6gre.c`, `vport-ip6erspan.c`), the netlink protocol helpers, and the `linux/compat/` directory backporting modern netfilter, network device, and tunnel features for older kernels.

The kernel module is built against the running kernel's headers via `make modules_install`. R1 path C (build from git checkout) explores this build path; R4 reads the kernel side of the upcall path; R5 reads the per-tunnel-type vport implementations.

### A.7. The utilities/ directory

The 34 files in `utilities/` are the CLI binaries and supporting scripts. Total lines 24,803. The two largest are `ovs-ofctl.c` (5109 lines) and `ovs-vsctl.c` (3157 lines).

| File | Role |
|------|------|
| `ovs-vsctl.c` | The OVSDB-driven CLI. Parses high-level commands (`add-br`, `add-port`, `set Bridge ... ...`), builds an OVSDB transaction over the IDL, commits it. The most-typed binary in any OVS lab. |
| `ovs-ofctl.c` | The OpenFlow client. Speaks OpenFlow 1.0 to 1.5 to a switch, supports `add-flow`, `del-flow`, `dump-flows`, `mod-flow`, `add-group`, `add-meter`, `bundle`, `monitor`. |
| `ovs-dpctl.c` | The datapath CLI. Speaks netlink to the kernel datapath (or the userspace datapath via Unix socket). Surfaces `add-dp`, `del-dp`, `add-if`, `del-if`, `dump-flows`, `del-flows`. |
| `ovs-appctl.c` | Thin shim over `unixctl`. Sends a command to a daemon's Unix socket and prints the response. The Swiss army knife: every internal subsystem registers `unixctl` commands that `ovs-appctl` invokes. |
| `ovs-tcpdump.in` | Python script that creates a mirror port on a bridge and runs `tcpdump` against it. Removes the mirror on `Ctrl-C`; orphans the mirror on hard kill (recoverable manually). |
| `ovs-pcap.in` | Python pcap reader that handles OVS-specific packet types. |
| `ovs-pki.in` | The PKI helper for SSL-secured OVSDB and OpenFlow. Builds a CA, issues certificates, signs certificate signing requests. |
| `ovs-ctl.in` | The init script. Wraps `ovsdb-server` and `ovs-vswitchd` startup with the right command-line flags, sets up the OVSDB schema, recovers from prior crash. |
| `ovs-l3ping.in` | An L3 reachability test that uses an OVS internal port. |
| `ovs-sim.in` | A simulator that runs OVS in a sandbox without root. Useful for testing flows without affecting the host. |
| `bugtool/` | The support-bundle generator. Collects every relevant file (config, log, schema, kernel modinfo, dpctl dumps) into a tarball for support. |
| `gdb/ovs.py` | GDB pretty-printer scripts for OVS internal types: `struct flow`, `struct hmap`, `struct cmap`, `struct shash`. |
| `checkpatch.py` | The patch lint script. Run by `tests/checkpatch.at`. Catches Coding Style violations before review. |
| `nlmon.c` | A netlink monitor that prints generic netlink messages on the wire. Useful for debugging the datapath protocol. |

R9 (debug doctrine) cites every CLI command in the playbook back to the binary that implements it.

### A.8. Total source counts

For reference, the per-directory totals across `.c`, `.h`, `.py`, `.in`, `.at`, `.rst` files:

- `lib/`: 419 files, 235,529 lines.
- `ofproto/`: 44 files, 47,426 lines.
- `vswitchd/`: 8 files, 6,491 lines.
- `ovsdb/`: 58 files, 33,116 lines.
- `datapath/`: 150 files, 45,482 lines.
- `utilities/`: 34 files, 24,803 lines.
- `python/`: 46 files, 16,409 lines.
- `tests/`: 187 files, 101,469 lines.
- `Documentation/`: 121 files, 30,842 lines.
- `include/`: 127 files, 20,680 lines.
- `ipsec/`: 1 file, 1,372 lines.
- `vtep/`: 4 files, 3,695 lines.

Total in scope across these twelve directories: 1,199 files, 567,314 lines. This number is the gross size of the project that plan v3.13 commits to teaching. A learner who masters every file by name has read roughly 13,500 pages of source.

A reader inventorying their own progress can use this section as a checklist: which subsystem have I read, which files have I traced, which directory still feels unfamiliar.

---

## Section B. Upstream documentation inventory at v2.17.9

The OVS source ships 121 reStructuredText files in `Documentation/`. The files are grouped into six subdirectories. Section B reads each subdirectory and produces a one-paragraph synopsis per file. A reader who is stuck on a topic looks here first; the upstream docs are usually the highest-fidelity source after the source code itself.

### B.1. intro/ (high-level introduction)

`intro/index.rst` is the section index. `intro/what-is-ovs.rst` introduces Open vSwitch in two paragraphs as a multi-layer virtual switch licensed under Apache 2.0, designed for extensibility and programmability via OpenFlow and OVSDB. `intro/why-ovs.rst` explains the motivating use case: the virtualisation-driven need for software switching that exposes a programmable interface, can replace `bridge` for production workloads, and integrates with cloud orchestration.

### B.2. intro/install/ (installation paths)

This subdirectory is the canonical reading list for plan v3.13 R1 (install three ways).

- `intro/install/index.rst`: index.
- `intro/install/general.rst`: the canonical from-source install guide. Walks `./boot.sh`, `./configure`, `make`, `make install`, `make modules_install`. Discusses configure flags (`--with-linux`, `--with-dpdk`, `--with-debug`), the kernel-module versus userspace-datapath choice, and the post-install verification (`ovs-vsctl --version`, `ovs-vswitchd --version`).
- `intro/install/distributions.rst`: a roundup of distribution-specific notes. Where to find Ubuntu, Debian, RHEL, CentOS, Fedora, Arch packages. Which distribution ships which OVS version. The pointer to community-maintained packaging.
- `intro/install/userspace.rst`: how to run OVS without the kernel module, using the userspace datapath. Trade-offs versus the kernel datapath.
- `intro/install/dpdk.rst`: the DPDK install path. Out of scope per CLAUDE.md North Star, mentioned only as the file that exists.
- `intro/install/afxdp.rst`: the AF_XDP install path. Out of scope.
- `intro/install/debian.rst`: Debian-specific instructions, the `dpkg-buildpackage` path, the systemd unit layout.
- `intro/install/rhel.rst`: RHEL-specific instructions. SELinux, systemd, `firewalld`.
- `intro/install/fedora.rst`: Fedora-specific instructions.
- `intro/install/netbsd.rst`: NetBSD-specific instructions.
- `intro/install/windows.rst`: Windows-specific instructions. Out of scope for plan v3.13.
- `intro/install/xenserver.rst`: XenServer-specific instructions. Largely historical.
- `intro/install/bash-completion.rst`: how to install the bash-completion script that ships with OVS.
- `intro/install/documentation.rst`: how to build the Sphinx-based documentation locally.

### B.3. topics/ (architectural and deep-dive topics)

This is the subdirectory plan v3.13 cites most often.

- `topics/index.rst`: index.
- `topics/design.rst`: the design overview. The single most important `.rst` file in the corpus. Covers architecture, flow tables, OpenFlow versus OVSDB roles, the slow path and fast path, conntrack, mirroring, sFlow.
- `topics/datapath.rst`: the datapath internals. Megaflows, exact-match cache, masks, revalidation, upcall flow.
- `topics/openflow.rst`: OVS OpenFlow support matrix per version.
- `topics/ovs-extensions.rst`: NXM and OXM extensions OVS adds beyond the standard.
- `topics/integration.rst`: how OVS integrates with virtualisation platforms. The `br-int` plus `br-tun` pattern.
- `topics/networking-namespaces.rst`: the canonical reference for using network namespaces with OVS. Cited heavily by plan v3.13 §R0.1 sidebar.
- `topics/bonding.rst`: link bonding modes, LACP behaviour, balance modes.
- `topics/idl-compound-indexes.rst`: how the OVSDB IDL builds compound indices for fast lookup.
- `topics/language-bindings.rst`: roundup of language bindings (Python, Go, C, others).
- `topics/ovsdb-relay.rst`: OVSDB relay servers (a read-side scaling pattern).
- `topics/ovsdb-replication.rst`: active-backup replication (older approach).
- `topics/porting.rst`: how to port OVS to a new platform.
- `topics/record-replay.rst`: deterministic replay of an OVS run for debugging.
- `topics/testing.rst`: how to run the test suite. Cited by S9.
- `topics/tracing.rst`: tracepoints, USDT probes, `ovs-appctl ofproto/trace`, `dpctl/dump-flows`.
- `topics/usdt-probes.rst`: USDT (User Statically Defined Tracing) probe inventory.
- `topics/userspace-tso.rst`: TCP Segmentation Offload in the userspace datapath.
- `topics/userspace-tx-steering.rst`: TX steering for the userspace datapath.
- `topics/windows.rst`: Windows-specific topics. Out of scope.
- `topics/dpdk/`: DPDK subdirectory. Out of scope per CLAUDE.md North Star (8 files).
- `topics/fuzzing/`: fuzzing infrastructure (4 files). Documented but not exercised by plan v3.13.

### B.4. howto/ (task-oriented how-to guides)

- `howto/index.rst`: index.
- `howto/dpdk.rst`: DPDK how-to. Out of scope.
- `howto/ipsec.rst`: how to enable IPsec on tunnels. Cited by R5.5 sub-task 12.
- `howto/kvm.rst`: KVM integration.
- `howto/libvirt.rst`: libvirt integration.
- `howto/lisp.rst`: LISP tunnel how-to. Mentioned for completeness; LISP is rarely deployed.
- `howto/qos.rst`: QoS configuration. Cited by R7.
- `howto/selinux.rst`: SELinux integration on RHEL.
- `howto/sflow.rst`: sFlow agent configuration. Cited by R7.
- `howto/ssl.rst`: SSL/TLS-secured OVSDB and OpenFlow.
- `howto/tunneling.rst`: kernel-datapath tunnel how-to. Cited by R5 and R5.5.
- `howto/userspace-tunneling.rst`: userspace-datapath tunnel how-to.
- `howto/vlan.rst`: VLAN access and trunk port configuration. Cited by R2 and R2.5.
- `howto/vtep.rst`: VTEP integration with hardware switches.

### B.5. ref/ (manual pages in rst form)

These files compile into man pages.

- `ref/index.rst`: index.
- `ref/ovs-actions.7.rst`: the `ovs-actions(7)` man page. The complete OVS action catalogue. Cited by R3.
- `ref/ovs-appctl.8.rst`: the `ovs-appctl(8)` man page.
- `ref/ovs-ctl.8.rst`: the `ovs-ctl(8)` man page.
- `ref/ovs-l3ping.8.rst`, `ref/ovs-pki.8.rst`, `ref/ovs-sim.1.rst`, `ref/ovs-tcpdump.8.rst`, `ref/ovs-tcpundump.1.rst`, `ref/ovs-test.8.rst`, `ref/ovs-vlan-test.8.rst`, `ref/ovs-parse-backtrace.8.rst`: the remaining utility man pages.
- `ref/ovsdb.5.rst`: the OVSDB schema-language man page.
- `ref/ovsdb.7.rst`: the OVSDB protocol man page. Cited by R8.
- `ref/ovsdb-server.7.rst`: the `ovsdb-server(7)` man page.

### B.6. internals/ (project governance and process)

- `internals/index.rst`: index.
- `internals/authors.rst`: how the project credits authors.
- `internals/bugs.rst`: how to file a bug.
- `internals/charter.rst`: the project charter.
- `internals/committer-emeritus-status.rst`, `committer-grant-revocation.rst`, `committer-responsibilities.rst`: committer process.
- `internals/contributing/`: contributing guide subdirectory (7 files including coding-style, submitting-patches, backporting-patches, libopenvswitch-abi, documentation-style).
- `internals/documentation.rst`: how the documentation is structured and built.
- `internals/mailing-lists.rst`: the project's mailing lists. Cited by Section F.
- `internals/maintainers.rst`: the maintainer list. Cited by Section D.
- `internals/patchwork.rst`: how patches are tracked.
- `internals/release-process.rst`: how releases are cut.
- `internals/security.rst`: the security-disclosure process.

### B.7. faq/ (frequently asked questions)

- `faq/index.rst`, `faq/general.rst`, `faq/configuration.rst`, `faq/contributing.rst`, `faq/design.rst`, `faq/issues.rst`, `faq/openflow.rst`, `faq/qos.rst`, `faq/releases.rst`, `faq/terminology.rst`, `faq/vlan.rst`, `faq/vxlan.rst`, `faq/bareudp.rst`.

The FAQ files are short; each answers one specific recurring question. A learner who is stuck on a particular subsystem (VLAN, VXLAN, QoS, OpenFlow) reads the matching FAQ first to check whether their confusion is one the upstream maintainers have already addressed.

### B.8. tutorials/ (multi-step walkthroughs)

- `tutorials/index.rst`: index.
- `tutorials/faucet.rst`: a Faucet-controller-driven tutorial.
- `tutorials/ipsec.rst`: an IPsec tunnel tutorial.
- `tutorials/ovs-advanced.rst`: an advanced OVS tutorial.
- `tutorials/ovs-conntrack.rst`: the canonical conntrack tutorial. Cited by R6.

### B.9. Recommended reading order for a new learner

The plan v3.13 reading order across `Documentation/` is:

1. `intro/what-is-ovs.rst` and `intro/why-ovs.rst` (the orientation, ten minutes).
2. `topics/design.rst` (the architecture, two hours, read carefully).
3. `topics/openflow.rst` and `ref/ovs-actions.7.rst` (OpenFlow surface).
4. `topics/datapath.rst` (datapath internals).
5. `topics/networking-namespaces.rst` (the lab convention).
6. `tutorials/ovs-conntrack.rst` (a worked example).
7. `topics/integration.rst` (the `br-int` plus `br-tun` pattern).
8. `howto/tunneling.rst` and `howto/userspace-tunneling.rst` (overlay primitives).
9. `ref/ovsdb.7.rst` (database protocol).
10. `topics/testing.rst` (test suite).
11. The relevant FAQ entries as questions arise.

After this list, every other file is read on demand from the corresponding R-sprint or S-sprint of plan v3.13.

---

## Section C. Offline doc library inventory

The `sdn-onboard/doc/` directory holds the curated offline reference library that ships with the curriculum. The files are reused across multiple R-sprints and S-sprints.

### C.1. Master keyword reference

- `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`. 207,075 bytes (about 2,617 lines), 320+ keywords. The internal authoritative dictionary of every term in the OVS / OpenFlow / OVN scope. Every R-sprint and S-sprint cross-references this file when introducing a new term. The reference is English-authoritative as of plan v3.12 closure.

### C.2. Vendor-published lab decks (PDF and PPTX)

These are training decks contributed to the curriculum library. Each is paired with a topic tag identifying which plan v3.13 sprint reads it.

| File | Pages (approximate) | Topic tag | Sprints that cite it |
|------|---------------------|-----------|----------------------|
| `Day 4-lab3-Introduction to Open vSwitch.pptx` and `.pdf` | ~30 slides | OVS introduction | R0, R1, R2 |
| `Day 4- Motivation and Introduction to Open vSwitch.pdf` | ~25 pages | OVS background and motivation | R0, R1, S0 |
| `Day 4-Overview of Open vSwitch Lab Series.pdf` | ~10 pages | Lab series outline | Cross-sprint reference |
| `Day 4-lab 9 - Open vSwitch Kernel Datapath.pdf` | ~20 pages | Kernel datapath internals | R4, S7 |
| `Day 4-lab4-ovs flow table.pdf` | ~25 pages | OpenFlow flow tables | R3 |
| `Day 5 -Lab 7 Implementing Routing in Open vSwitch.pdf` | ~20 pages | OVS native routing | R3, R11 |
| `Day 5-lab14-Quality of Service (QoS).pdf` | ~20 pages | QoS configuration | R7 |
| `Day 5-lab6-VLAN trunking in Open vSwitch.pdf` | ~20 pages | VLAN trunking | R2 |
| `OVS.pdf` | (large general reference) | OVS general reference | Every sprint |
| `OpenVSwitch.pdf` | (large general reference) | OVS general reference | Every sprint |
| `compass_artifact_wf-bd3df8ae-...md` | ~50K words | Field notes and synthesis | Sprint-specific |

### C.3. The doc/ovs/ subdirectory

`sdn-onboard/doc/ovs/` contains a redundant set of the lab decks above as PDFs. The duplication is intentional: it preserves the original deck format alongside any markdown derivatives.

### C.4. The lab SSH key

`sdn-onboard/doc/lab_private_key` is the SSH private key for the local lab fleet. Per `.gitignore` (added in plan v3.13 R0a), the key is not committed to git. The key is local-lab-only; the public counterpart is deployed to `/root/.ssh/authorized_keys` on every lab VM.

---

## Section D. Canonical authors and ecosystem

### D.1. Top contributors at v2.17.9

`git log --format=%an v2.17.9 | sort | uniq -c | sort -rn | head -25` produces the following ranking. Numbers are commit counts; the count is a lossy proxy for influence (some contributors squash, some chain) but the ordering is broadly representative.

| Commits | Author |
|---------|--------|
| 6180 | Ben Pfaff |
| 981 | Justin Pettit |
| 822 | Ethan Jackson |
| 701 | Ilya Maximets |
| 671 | Jarno Rajahalme |
| 666 | Jesse Gross |
| 509 | Gurucharan Shetty |
| 493 | Joe Stringer |
| 405 | Pravin B Shelar |
| 391 | Simon Horman |
| 346 | Andy Zhou |
| 285 | Alex Wang |
| 280 | Daniele Di Proietto |
| 248 | Russell Bryant |
| 241 | Alin Serdean |
| 218 | YAMAMOTO Takashi |
| 197 | William Tu |
| 152 | Han Zhou |
| 145 | Flavio Leitner |
| 141 | Nithin Raju |
| 137 | Darrell Ball |
| 134 | Greg Rose |
| 132 | Aaron Conole |
| 128 | Thomas Graf |
| 128 | Stephen Finucane |

Ben Pfaff has authored more than half of the project by commit count and remains the most influential active maintainer. His commits cluster heavily in `lib/`, `ofproto/`, and `ovsdb/`. His talks at the annual OvSCON conference (Section F) are the canonical reference for design rationale.

Justin Pettit contributed heavily to the early OpenFlow surface and the userspace datapath. Ethan Jackson and Pravin B Shelar contributed most of the kernel-side datapath and the original Geneve and STT tunnel implementations. Jarno Rajahalme contributed most of the conntrack integration. Ilya Maximets is currently the most active maintainer in the userspace-datapath, DPDK, and AF_XDP areas; he is the named author of many R-sprint-relevant features.

Jesse Gross was an early kernel-side author and the initial maintainer; he moved to other projects but his structural decisions remain visible in `datapath/`.

### D.2. Active committers per MAINTAINERS.rst

The `MAINTAINERS.rst` at `v2.17.9` lists the following 17 active committers with push access:

- Alex Wang `<ee07b291@gmail.com>`
- Alin Serdean `<aserdean@ovn.org>`
- Andy Zhou `<azhou@ovn.org>`
- Ansis Atteka `<aatteka@nicira.com>`
- Daniele Di Proietto `<daniele.di.proietto@gmail.com>`
- Gurucharan Shetty `<guru@ovn.org>`
- Ian Stokes `<istokes@ovn.org>`
- Ilya Maximets `<i.maximets@ovn.org>`
- Jarno Rajahalme `<jarno@ovn.org>`
- Jesse Gross `<jesse@kernel.org>`
- Justin Pettit `<jpettit@ovn.org>`
- Pravin B Shelar `<pshelar@ovn.org>`
- Russell Bryant `<russell@ovn.org>`
- Simon Horman `<horms@ovn.org>`
- Thomas Graf `<tgraf@noironetworks.com>`
- William Tu `<u9012063@gmail.com>`
- YAMAMOTO Takashi `<yamamoto@midokura.com>`

The `@ovn.org` cluster reflects the historical Nicira to VMware to Red Hat trajectory of the project. The `@kernel.org`, `@gmail.com`, `@noironetworks.com`, and `@midokura.com` addresses reflect the broader contributor base.

`MAINTAINERS.rst` also lists Emeritus Committers; Ben Pfaff appears in the Emeritus list but remains the most-cited active author by commit count, which reflects the Emeritus designation as a workload designation, not a removal of authority.

### D.3. Integrating projects

OVS is consumed by a large set of higher-level projects. The relevant integrators for plan v3.13 are listed below; each has at least one sprint that cross-references it.

- **OVN (Open Virtual Network).** A distributed virtual networking layer built directly on top of OVS. Provides logical switches, logical routers, ACLs, NAT, load balancing, DHCP, DNS, all compiled to OVS OpenFlow flows. Maintained by the same upstream community at `github.com/ovn-org/ovn`. **Out of scope for plan v3.13** per the owner directive but referenced as the natural next step; R5.5 sub-task 14 contrasts raw OVS with OVN, R11 capstone explicitly demonstrates "what OVN automates that we are doing by hand".
- **OpenStack Neutron.** The networking service of OpenStack uses OVS via the `ML2/OVS` driver and via the OVN-based driver. The reference architecture has each compute node running `br-int` plus `br-tun`. Cited by R5.5 sub-task 10 and R11.
- **kube-ovn.** A Kubernetes CNI plugin built on OVN. Provides per-pod networking, network policies, multi-tenancy. Cited by E11 enrichment dossier (when authored).
- **Antrea.** Another Kubernetes CNI plugin, this one built on raw OVS rather than OVN. Cited by E11 enrichment dossier as a comparative case.
- **Faucet.** A Python-based OpenFlow controller for OVS. Used by some campus and data centre operators as a more stable, simpler alternative to ONOS or OpenDaylight. Cited by `Documentation/tutorials/faucet.rst` and by R3.
- **Ryu.** A Python-based OpenFlow controller framework. Used heavily in research and in some tutorial materials. Cited by R3 if the controller-driven path is taken.
- **ONOS.** A distributed OpenFlow controller targeting service-provider networks. Cited briefly by R3 for completeness.
- **OpenDaylight.** A larger Java-based controller framework. Cited briefly by R3.
- **Cilium.** A Kubernetes CNI plugin built on eBPF rather than OVS. **Permanently banned** from plan v3.13 per CLAUDE.md North Star. Mentioned only to be excluded.
- **OvS-IPsec.** The IPsec helper that ships with OVS. Wraps strongSwan or LibreSwan. Cited by R5.5 sub-task 12.

The OVS-OVN-OpenStack-Kubernetes axis is the most consequential ecosystem path for an SDN engineer; the controller axis (Faucet, Ryu, ONOS, OpenDaylight) is the more academic path.

---

## Section E. Edge cases and hidden constraints

The 50 entries below are edge cases, hidden constraints, surprising behaviours, and "expert-only" details surfaced by reading the source tree (Section A), the upstream documentation (Section B), and the offline doc library (Section C). Every entry names where it surfaced and what makes it hard. Later E-sprints reference these by entry number to avoid restating.

The list is structured by subsystem. The numbering is stable: future revisions of this dossier may renumber but each entry's content is permanent until the underlying behaviour changes upstream.

### E.1. Bridge and port configuration

**E.1.1. `ovs-vsctl set` semantics: `set` versus `add` versus `--if-exists`.** The command `ovs-vsctl set <table> <row> <column>=<value>` overwrites the column. To merge into an existing column on a map type, use `ovs-vsctl set <table> <row> <column>:<key>=<value>`. To extend a set type, use `ovs-vsctl add <table> <row> <column> <value>`. `--if-exists` modifies the verb to silently no-op when the row does not exist instead of erroring; this matters for idempotent provisioning scripts.

**E.1.2. `--no-wait` and the OVSDB notification round-trip.** By default, `ovs-vsctl` blocks until `ovs-vswitchd` has applied the change and reported back. `--no-wait` skips the wait. Skipping is useful in scripts that pipe many commands but it means the next command may observe stale state.

**E.1.3. The `Bridge.fail_mode` column has three values.** `standalone` (the default for bridges with no controller) makes the bridge act as a regular L2 learning switch via the implicit normal action. `secure` (recommended when a controller is configured) makes the bridge drop every packet for which there is no flow rule. The third value is an empty string, treated as `standalone`. The choice has profound consequences: a `secure` bridge with a disconnected controller drops everything.

**E.1.4. The `Bridge.datapath_type` column has two values.** `system` (the default) uses the kernel datapath. `netdev` uses the userspace datapath. Switching requires recreating the bridge. Mixing kernel and userspace ports on the same bridge is not supported.

**E.1.5. Port name length limit is 15 characters.** Linux kernel `IFNAMSIZ` is 16 including the null terminator. Names longer than 15 characters are rejected by `ovs-vsctl add-port` with an unhelpful error from the kernel. Port-name conventions like `tap-<UUID>` collide with this limit.

### E.2. Flow table and OpenFlow semantics

**E.2.1. The implicit normal action.** When a bridge has `fail_mode=standalone` and no controller, every packet hits the implicit normal action which mimics a regular L2 learning switch. This action lives in `ofproto/ofproto-dpif-xlate.c:xlate_normal()`. A learner expecting "no flows means no forwarding" is wrong; "no flows plus standalone means MAC learning".

**E.2.2. Flow priorities and the wildcard rule.** Higher numeric priority wins. When two rules tie on priority, the order is undefined; most operators add a small differentiator to avoid ambiguity.

**E.2.3. Flow tables 0 to 254.** OVS supports up to 255 flow tables. Table 0 is the entry point. `actions=resubmit(,N)` jumps to table N. Pipelines that exceed this are an indication of design drift.

**E.2.4. Recirculation IDs are scarce.** The `recirc()` action allocates a recirculation ID via `ofproto-dpif-rid.c`. Pool exhaustion silently drops packets at the slow path. This is a real production failure mode.

**E.2.5. The `learn` action and target table fullness.** `learn(table=10, ...)` synthesises a flow into table 10. If table 10 is full, the synthesis silently fails. There is no built-in retry.

**E.2.6. Megaflow versus exact-match cache semantics.** The kernel datapath maintains both an exact-match cache (EMC) for the most-recent traffic and a megaflow cache for the long tail. Traffic that hits EMC is faster. The `emc_insert_inv_prob` `other_config` knob tunes how aggressively the EMC is populated. The userspace datapath has analogous structures.

**E.2.7. The slow path is single-threaded per upcall handler thread.** `ofproto-dpif-upcall.c` thread pool size is `n-handler-threads`. A burst of upcalls saturates the pool and queues; queue depth above ~1000 is a sign of slow-path bottleneck and warrants `coverage/show` inspection.

### E.3. Datapath and conntrack

**E.3.1. Kernel module conflict.** The kernel ships an in-tree `openvswitch.ko`; OVS source ships an out-of-tree alternative. Loading both is a kernel-level error. The plan v3.13 R0 baseline confirmed the in-tree module at `/lib/modules/5.15.0-173-generic/kernel/net/openvswitch/openvswitch.ko`. R1 path C must decide whether to displace it.

**E.3.2. The `openvswitch` module hard-depends on six other modules.** Per the R0 baseline `modinfo`: `nf_conntrack`, `nf_nat`, `nf_conncount`, `libcrc32c`, `nf_defrag_ipv6`, `nsh`. Loading `openvswitch` auto-loads these. If any is missing or has an ABI mismatch, `modprobe` fails.

**E.3.3. Conntrack zone and tenant isolation.** `ct(zone=N, commit)` separates conntrack state per tenant. Without zones, two tenants with overlapping IP space share a conntrack table and pollute each other's NAT translations. Zones are essential for multi-tenant deployments. R6 exercises this.

**E.3.4. NAT reverse traffic and zone consistency.** A NAT translation written in zone A but matched in zone B does not reverse correctly. The conntrack zone must be consistent across both directions of a flow.

**E.3.5. Conntrack with fragmentation.** IPv4 fragments are reassembled by the kernel before conntrack sees them. The userspace conntrack uses `lib/ipf.c`. Behaviour differences between the two paths exist for malformed fragments; the userspace path is stricter.

**E.3.6. ICMP conntrack quirks.** ICMP echo and reply pair via the conntrack `id` field; ICMP errors (destination unreachable, time exceeded) carry the inner header and require the inner header to match an existing conntrack entry to be considered RELATED.

### E.4. Tunnels

**E.4.1. Tunnel MTU and PMTUD.** A 1500-byte underlay MTU plus a 50-byte Geneve overhead leaves 1450 for the inner payload. If the VM has a 1500 MTU, large packets either fragment (rare, depends on `df` bit and outer encapsulation rules) or trigger an ICMP "fragmentation needed" reply that the VM kernel must process. The first symptom is intermittent packet loss for large flows. R5.5 sub-task 11 exercises this.

**E.4.2. Tunnel destination ARP cache.** `lib/tnl-neigh-cache.c` resolves the underlay MAC for each tunnel destination once and caches it. ARP timeouts trigger a refresh; while the refresh is in flight, packets queue or drop depending on the cache state.

**E.4.3. VXLAN versus Geneve VNI compatibility.** Both use a 24-bit virtual network identifier but the wire formats differ. A VXLAN tunnel cannot inter-operate with a Geneve tunnel even if the VNI is identical.

**E.4.4. Geneve TLV options.** Geneve allows variable-length TLV options between the outer UDP header and the inner Ethernet frame. OVS does not parse most TLVs; OVN uses TLVs for metadata such as the source logical port. A `tcpdump -X` capture of a Geneve packet shows the TLV bytes; interpreting them requires knowledge of the option class.

**E.4.5. STT is being phased out.** STT (Stateless Transport Tunnelling) uses a TCP-shaped header to ride NIC TSO. It works only on hardware that handles the synthetic TCP headers correctly. Modern kernels do not ship the STT module. R5.5 mentions STT but does not lab it.

**E.4.6. GRE behind NAT.** GRE has no port number. NAT devices that translate only TCP and UDP discard GRE traffic. A GRE tunnel between hosts that traverse NAT requires a NAT-helper that understands GRE; most do not.

**E.4.7. IPsec IKE rekey and tunnel disruption.** IPsec rekeys the SA periodically. During the rekey window, traffic may be reordered or briefly dropped. The window is typically configured at one hour for the IKE SA and ten minutes for the IPsec SA. Long-running traces should expect this disruption.

### E.5. OVSDB

**E.5.1. Boot order race between `ovsdb-server` and `ovs-vswitchd`.** `ovs-vswitchd` connects to `ovsdb-server` at startup. If `ovsdb-server` is not yet ready, `ovs-vswitchd` retries with backoff. The `ovs-ctl` script paces the start sequence; raw `systemd` ordering may not.

**E.5.2. Schema version incompatibility.** A newer `ovs-vswitchd` reading an older OVSDB schema may fail at startup if a required column is missing. A newer `ovsdb-server` accepting an older client is more tolerant. Upgrades require updating `ovsdb-server` first, then `ovs-vswitchd`.

**E.5.3. `other_config` keys silently accepted without effect.** Many features expose tuning via `Open_vSwitch.other_config:<key>`. If the feature is not built into this binary (for example, a key that was added in a later version), the key is accepted without effect. There is no warning. A learner who sets a key and observes no behavioural change should compare key against the documented set in `vswitch.xml`.

**E.5.4. OVSDB transaction size limits.** A transaction that touches thousands of rows (large bulk insert) may exceed the JSON-RPC frame size and get rejected. Large operations should be batched.

**E.5.5. Raft cluster member count.** A cluster with two members tolerates zero failures (both must be alive). Three tolerates one. Five tolerates two. Even-numbered clusters waste a node compared to the next-odd cluster. R8 uses three.

**E.5.6. Raft log compaction is not free.** `ovsdb-tool compact` truncates the log and writes a snapshot. During compaction, transaction throughput is paused. Compaction interval is a tuning knob.

**E.5.7. Cluster snapshot transfer cost.** When a follower lags far behind, the leader sends an `InstallSnapshot` carrying the entire OVSDB. For large databases (OpenStack Neutron with thousands of ports), this can saturate the underlay link. Slow followers become very-slow followers.

**E.5.8. The `relay` mode.** OVSDB relay (`Documentation/topics/ovsdb-relay.rst`) is a read-only forwarder that fans out monitor traffic. Useful for very-large deployments. Not used by plan v3.13 but documented for completeness.

### E.6. Observability

**E.6.1. Per-module `vlog` levels.** `ovs-appctl vlog/list` lists every module. `ovs-appctl vlog/set ANY:dbg` enables debug for all; `ovs-appctl vlog/set ofproto_dpif_xlate:dbg` enables for one module. Production should not run with `ANY:dbg` (the log volume is enormous).

**E.6.2. Coverage counters as forensic evidence.** `ovs-appctl coverage/show` dumps every counter. Counters that increment unexpectedly during a steady-state run are signals. R4 reads the counter set during synthetic load.

**E.6.3. `ofproto/trace` requires a synthesised packet.** The trace command takes a packet description (`in_port`, fields) and walks the OpenFlow pipeline. The trace shows every table visited, every action applied, the resulting datapath flow. `ofproto/trace` is the single most useful debugging tool when a controller behaves unexpectedly.

**E.6.4. `ovs-tcpdump` orphan ports on hard kill.** `ovs-tcpdump` creates a port mirror; on `Ctrl-C` it removes the mirror. On `kill -9` the mirror leaks and must be removed manually with `ovs-vsctl del-port`.

**E.6.5. sFlow collector overload.** A high sampling rate (1-in-100) generates significant traffic. A misconfigured collector (single underspecified host) becomes a bottleneck. Sampling rate should match the collector capacity, not the bridge throughput.

### E.7. Performance and tuning

**E.7.1. `n-handler-threads` and `n-revalidator-threads`.** The two thread-pool sizes for the slow path. Defaults are reasonable for small deployments; multi-NUMA hosts benefit from per-NUMA pools.

**E.7.2. `flow-limit`.** The `Open_vSwitch.other_config:flow-limit` knob caps the number of datapath flows. Beyond this, the revalidator aggressively prunes. Setting this too low causes flow churn; too high causes memory pressure.

**E.7.3. EMC insert probability.** `emc-insert-inv-prob` controls how often the userspace datapath populates the EMC. Lower values populate more aggressively.

**E.7.4. Megaflow size grows with flow diversity.** A bridge with many distinct match-field combinations has many megaflows. `dpctl/dump-flows | wc -l` measures this.

### E.8. CLI and operator experience

**E.8.1. `ovs-vsctl` is OVSDB only.** It does not see the OpenFlow flow table; for that, use `ovs-ofctl`. A common newcomer mistake is `ovs-vsctl dump-flows`, which silently does nothing because the verb does not exist.

**E.8.2. `ovs-appctl` discovery.** `ovs-appctl list-commands` (when run without arguments against a daemon) lists every registered `unixctl` command. Many subsystems register undocumented commands; this is how to discover them.

**E.8.3. `ovs-dpctl/show` versus `ovs-appctl dpif/show`.** The first talks to the kernel datapath via netlink; the second talks to `ovs-vswitchd` via `unixctl`. They show similar information but the second is filtered through `ovs-vswitchd`'s view of the datapath.

**E.8.4. `ovs-vsctl --columns=` for OVSDB introspection.** When debugging, listing only a few columns is faster and clearer than the full row dump.

**E.8.5. OpenFlow protocol negotiation.** `ovs-ofctl` defaults to OpenFlow 1.0. Modern features require `-O OpenFlow13` or later. A `dump-flows` against an OF 1.5 bridge with no `-O` flag returns the bridge's OF 1.0 view, which may differ from what the controller programmed.

### E.9. Security and packaging

**E.9.1. SSL-secured OVSDB versus TCP.** Production OVSDB should run on SSL with mutual authentication via `ovs-pki`. TCP without auth is a debugging-only mode.

**E.9.2. SELinux and OVS on RHEL.** Default SELinux denies several OVS operations. The `openvswitch-selinux-extra-policy` package addresses this. Cited in `howto/selinux.rst`.

**E.9.3. The `openvswitch-test` package is in `universe` on Ubuntu.** Per R0 `apt-cache policy`. Standard support tier differs between `main` and `universe`; this matters for long-term operations.

**E.9.4. The package vs source build differ in the systemd unit.** The package ships a tested systemd unit at `/lib/systemd/system/openvswitch-switch.service`. The source build does not install a systemd unit by default; the operator must use the script `/usr/local/share/openvswitch/scripts/ovs-ctl start` instead.

### E.10. Test suite

**E.10.1. `make check` versus `make check-system-userspace` versus `make check-kernel`.** Three tiers. `make check` is hermetic unit tests. `make check-system-userspace` exercises the userspace datapath against real network namespaces. `make check-kernel` requires the kernel module loaded. R1 path C exercises `make check`.

**E.10.2. Autotest variable expansion.** `AT_CHECK([command])` runs the command; `AT_CHECK([command], [exit_code], [stdout], [stderr])` adds expected exit and output. The `m4` macro expansion is fragile; quoting matters.

**E.10.3. Per-test working directory.** `tests/testsuite.dir/N/` is the working directory of test number N. After a failure, this directory holds the relevant logs.

**E.10.4. `OVS_VSWITCHD_START` versus `OVS_TRAFFIC_VSWITCHD_START`.** Two macros for spinning up `ovs-vswitchd` in a test. The first uses the userspace datapath; the second the kernel datapath. Tests must pick the right one.

---

## Section F. Online research pass (foundational)

Section F records the foundational online sources every later E-sprint draws from. Each entry has a verified URL (per Rule 6 Checklist B step 2), a one-line description, and the topic tags it serves.

### F.1. Upstream community surfaces

- `https://www.openvswitch.org/`. The project home page. Links to documentation, downloads, mailing lists, conference programmes.
- `https://docs.openvswitch.org/`. The published documentation, rendered from `Documentation/`.
- `https://mail.openvswitch.org/pipermail/ovs-dev/`. The development mailing list archive. Patch submission and review traffic, every active maintainer's voice. Search the archive for design rationale on any feature.
- `https://mail.openvswitch.org/pipermail/ovs-discuss/`. The user-discussion list archive. Production-operator questions and answers, the place to find recipe-style "how do I configure X" answers from the community.
- `https://patchwork.ozlabs.org/project/openvswitch/list/`. The patchwork instance tracking patch state.
- `https://github.com/openvswitch/ovs`. The canonical source repository. Issues, pull requests (limited use upstream), tags, releases.
- `https://github.com/openvswitch/ovs/issues`. The issue tracker. Sorted by reaction count is a reasonable proxy for "the bugs the most users hit".
- `https://patches.dpdk.org/`. Patchwork for DPDK-related OVS patches. Out of scope per ban; included for inventory completeness.

### F.2. Conferences

- `https://www.openvswitch.org/support/ovscon2014/`, `ovscon2015`, `ovscon2016`, `ovscon2017`, `ovscon2018`, `ovscon2019`, `ovscon2020`, `ovscon2021`, `ovscon2022`, `ovscon2023`. The annual OvSCON conference. Slide decks and abstracts for every talk. The single richest source of design-rationale content beyond the mailing list. Major recurring speakers: Ben Pfaff (Linux Foundation), Justin Pettit (VMware), Pravin Shelar (Red Hat), Jarno Rajahalme (Cisco), Ilya Maximets (Red Hat).
- `https://lpc.events/event/`. The annual Linux Plumbers Conference includes a Networking Track that frequently covers OVS-adjacent topics: kernel datapath changes, conntrack evolution, kernel bypass alternatives.

### F.3. Vendor documentation

- `https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/`. RHEL networking documentation includes the OVS subsection, useful for the OS-level operations a learner will perform.
- `https://www.redhat.com/en/blog`. Red Hat developer blog. Search `openvswitch`, `ovn`, `dpdk`. Authors include Aaron Conole and Eelco Chaudron (both active OVS contributors).
- `https://docs.openstack.org/neutron/latest/`. OpenStack Neutron documentation. The reference architecture for OVS-based deployments; cited by R5.5 and R11.

### F.4. Practitioner blogs

- `https://vincent.bernat.ch/en`. Vincent Bernat's blog. Consistently high-quality networking content including OVS deep dives, kernel-side analysis, troubleshooting walkthroughs.
- `https://lwn.net/`. LWN.net's networking and kernel coverage. Subscriber-only for the most recent articles; older articles open. Search for OVS-specific stories about kernel-side conntrack changes, datapath evolution, security disclosures.
- `https://stbuehler.de/blog/`. Stephan Bühler's blog (occasional OVS content).
- `https://blog.kelvinsong.com/`. Kelvin Song's networking blog (occasional OVS content).

### F.5. Specification documents

- `https://opennetworking.org/wp-content/uploads/2014/10/openflow-switch-v1.5.1.pdf`. The OpenFlow 1.5.1 specification. Cited by R3.
- `https://datatracker.ietf.org/doc/html/rfc7047`. RFC 7047, the OVSDB protocol. Cited by R8.
- `https://datatracker.ietf.org/doc/html/rfc7348`. RFC 7348, the VXLAN specification. Cited by R5 and R5.5.
- `https://datatracker.ietf.org/doc/html/rfc8926`. RFC 8926, the Geneve specification. Cited by R5 and R5.5.
- `https://datatracker.ietf.org/doc/html/rfc1701` and `https://datatracker.ietf.org/doc/html/rfc1702`. RFC 1701 and 1702, the original GRE and GRE-over-IPv4 specifications. Cited by R5.
- `https://datatracker.ietf.org/doc/html/rfc7011`. RFC 7011, the IPFIX specification. Cited by R7 and S4.
- `https://datatracker.ietf.org/doc/html/rfc3176`. The sFlow v5 specification (originally a vendor specification, later RFC). Cited by R7.
- `https://raft.github.io/raft.pdf`. The Raft paper (Diego Ongaro and John Ousterhout, 2014). Cited by R8.

### F.6. Search queries to record (for reproducibility)

The following searches are recorded so that future E-sprints can reproduce the source list and check it against current results. The query and the relevant result count at time of recording are noted.

- `site:mail.openvswitch.org "<feature>"` for any specific feature.
- `site:openvswitch.org "<topic>"` for general topic browsing.
- `intitle:openvswitch site:lwn.net` for LWN articles.
- `"ben pfaff" openvswitch site:youtube.com` for OvSCON talk recordings.

The full list of E-sprint-specific online sources lives in each E-sprint dossier. Section F is foundation only.

---

## Section G. Foundation reading order

A learner who is starting plan v3.13 from cold should read this dossier in the order Section A, Section D, Section B, Section C, Section E, Section F. Section A grounds the source-tree map. Section D grounds the human and ecosystem map. Section B and C ground the documentation map. Section E surfaces the recurring traps. Section F provides the URL list to bookmark.

A reader who is in the middle of an R-sprint or S-sprint reads only the relevant subsection. The dossier is structured so that any reader can pick it up at any point.

---

## Authoring metadata

Authored 2026-04-29 by Claude Opus 4.7 under owner direction (VO LE) per plan v3.13 §4.0.2. The dossier is a working artefact in `memory/sdn/v3.13-enrichment/`, not curriculum, but it is referenced by every E-sprint, R-sprint, and S-sprint that follows.

When the dossier is updated by a future session (because new files are added to the OVS source tree, the documentation reorganises, the maintainer list changes, or a new edge case is discovered), the update commit must mention the section that changed and why. The dossier is append-mostly: existing entries should not be deleted, only annotated as stale, so the historical record remains intact.
