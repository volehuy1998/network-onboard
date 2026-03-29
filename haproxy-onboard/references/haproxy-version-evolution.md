# Bảng theo dõi tiến hóa phiên bản HAProxy theo lộ trình Canonical

File này là **bảng tham chiếu trung tâm** (central tracking table) ghi nhận mọi thay đổi giữa các phiên bản HAProxy trên Ubuntu LTS. Mỗi khi viết một Part trong series và phát hiện behavior, directive, hoặc feature khác nhau giữa các phiên bản, thông tin đó được ghi vào đây với trỏ ngược (back-reference) đến Part đã nhắc đến nó.

Mục đích: khi đến Part 29 (So sánh phiên bản HAProxy trên các Ubuntu LTS), toàn bộ dữ liệu đã sẵn sàng — chỉ cần tổ chức, nghiên cứu chi tiết, và trình bày.

Phiên bản theo dõi:

| Ubuntu LTS | HAProxy (Canonical repo) | Trạng thái |
|---|---|---|
| 20.04 Focal | 2.0.x | **Baseline** (phiên bản gốc của series) |
| 22.04 Jammy | 2.4.x | So sánh với baseline |
| 24.04 Noble | 2.8.x | So sánh với baseline |
| (PPA/source) | 3.0+ / 3.2 | Ghi nhận cho lộ trình tương lai |

Quy ước trạng thái thay đổi:

| Ký hiệu | Ý nghĩa |
|---|---|
| `NEW` | Tính năng mới, không tồn tại ở phiên bản trước |
| `CHANGED` | Hành vi mặc định hoặc cú pháp thay đổi |
| `DEPRECATED` | Còn hoạt động nhưng được đánh dấu sẽ bị loại bỏ |
| `REMOVED` | Bị loại bỏ hoàn toàn, không còn hoạt động |
| `IMPROVED` | Tính năng cũ được cải thiện hiệu năng hoặc mở rộng |

---

## 1 — Process Model và Threading

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `master-worker` default | Không (cần `-W` hoặc directive) | Không | Mặc định | Mặc định | Part 1, §1.3 |
| `nbproc` | Fully supported | DEPRECATED | REMOVED (từ 2.5) | REMOVED | Part 1, §1.3 |
| `nbthread` default | 1 (manual set) | Auto-detect CPU cores | Auto-detect | Auto-detect | Part 1, §1.3 |
| `nbthread` + `nbproc` exclusive | Có (không dùng đồng thời) | N/A (nbproc deprecated) | N/A | N/A | Part 1, §1.3 |
| Thread groups | Không | Không | NEW (từ 2.7) | Có | — |
| `-W` master-worker flag | Có | Có | Có (nhưng là default) | Có | Part 1, §1.3 |
| `-sf` soft-finish reload | Có | Có | Có | Có | Part 1, §1.3 |

---

## 2 — Cấu hình cốt lõi (Global, Defaults, Sections)

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `http-reuse` default | `never` | CHANGED → `safe` | `safe` | `safe` | — |
| HTX engine (HTTP/2) | Có (mặc định từ 2.0) | Có | Có | Có | Part 1, §1.3 |
| `default-path` directive | Không | NEW | Có | Có | — |
| `strict-limits` | Không | NEW | Có | Có | — |
| Conditional blocks (`if`) | Không | NEW (từ 2.4) | Có | Có | — |
| `crt-store` section | Không | Không | Không | NEW (3.0) | — |

---

## 3 — SSL/TLS và Certificate Management

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| TLS 1.3 support | Có (OpenSSL 1.1.1) | Có | Có | Có | — |
| OCSP Stapling | Có (basic) | IMPROVED | IMPROVED (auto-update) | Có | README, Part 16 |
| ACME protocol (Let's Encrypt) | Không | Không | Không | NEW (3.2, experimental) | README, Part 16 |
| kTLS kernel offload | Không | NEW (kernel 5.15+) | Có | Có | README, Part 15 |
| `ssl-default-bind-ciphersuites` | Có (TLS 1.3 ciphers) | Có | Có | Có | — |
| Certificate hot-reload | Có (via Runtime API) | Có | IMPROVED | Có | — |

---

## 4 — HTTP/2, HTTP/3, và Modern Protocols

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| HTTP/2 frontend | Có (qua HTX) | Có | Có | Có | README, Part 17 |
| HTTP/2 backend (h2c/h2) | Có | IMPROVED | Có | Có | — |
| QUIC / HTTP/3 | Không | Không | NEW (experimental, từ 2.6) | Có (stable) | README, Part 17 |
| `bind quic4@`/`quic6@` | Không | Không | NEW | Có | README, Part 17 |
| WebSocket upgrade | Có | Có | Có | Có | — |
| gRPC proxying | Có | Có | Có | Có | — |

---

## 5 — Load Balancing và Health Checks

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `balance random` | Có | Có | Có | Có | — |
| Health check: agent-check | Có | Có | Có | Có | — |
| Passive health check | Có | Có | Có | Có | — |
| Health check TCP fast-open | Không | Không | NEW | Có | — |

---

## 6 — Stick Tables, Persistence, và Rate Limiting

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| Stick table peers | Có | Có | IMPROVED (peers v2.1) | Có | — |
| `gpt` (general purpose tag) | `gpt0` chỉ 1 tag | IMPROVED (multiple `gpt`) | Có | Có | — |
| `silent-drop` | Có | Có | Có | Có | — |

---

## 7 — ACL, Fetches, Converters, và Rules

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `jwt_verify()` | Không | NEW (từ 2.4) | Có | Có | — |
| `jwt_header_query` | Không | NEW | Có | Có | — |
| `http-after-response` | Có | Có | Có | Có | — |
| `set-var-fmt` | Không | NEW | Có | Có | — |

---

## 8 — Logging, Monitoring, và Observability

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| Prometheus exporter | Có (basic) | IMPROVED | IMPROVED | Có | — |
| `ring` section (ring buffer) | Có | Có | IMPROVED | Có | — |
| `log-forward` | Không | NEW (từ 2.3) | Có | Có | — |

---

## 9 — Performance, Kernel, và Advanced Features

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `splice()` zero-copy | Có | Có | Có | Có | — |
| `filter bwlim` (bandwidth limit) | Không | Không | NEW (từ 2.7) | Có | README, Part 21 |
| `mode spop` backend | Không | Không | Không | NEW (3.1) | README, Part 22 |
| CPU affinity per thread | Có (basic `cpu-map`) | IMPROVED | IMPROVED (thread groups) | Có | — |
| `tune.quic.*` directives | Không | Không | NEW | Có | — |

---

## 10 — Security

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| HTTP/2 Rapid Reset (CVE-2023-44487) | Không bị ảnh hưởng | Không bị ảnh hưởng | Patched | Patched | README, Part 27 |
| H2 SETTINGS_MAX_CONCURRENT_STREAMS | Có | Có | IMPROVED | Có | — |

---

## 11 — Lua, SPOE/SPOP, và Extensibility

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| Lua 4 extension points | Có (actions, fetches, converters, services) | Có | Có | Có | README, Part 22 |
| SPOE/SPOP | Có | Có | Có | IMPROVED (`mode spop` backend, 3.1+) | README, Part 22 |

---

## 12 — High Availability và Reload

| Thay đổi | 2.0 (20.04) | 2.4 (22.04) | 2.8 (24.04) | 3.0+ | Nguồn Part |
|---|---|---|---|---|---|
| `-x` fd passing reload | Có (master-worker mode) | Có | Có | Có | README, Part 26 |
| Seamless reload via master | Có (nếu master-worker bật) | Có | Có (default) | Có | Part 1, §1.3 |
| `hard-stop-after` | Có | Có | Có | Có | — |

---

## Quy ước inline annotation trong các Part

Khi viết nội dung một Part và phát hiện behavior khác nhau giữa phiên bản, sử dụng format sau trong thân bài:

**Khi tính năng không tồn tại ở 2.0 (baseline):**

```markdown
> **Lưu ý phiên bản:** Tính năng `jwt_verify()` chỉ khả dụng từ
> HAProxy 2.4+. Trên HAProxy 2.0 (Ubuntu 20.04), xác thực JWT
> cần thực hiện qua Lua scripting hoặc backend application.
```

**Khi default behavior thay đổi:**

```markdown
> **Lưu ý phiên bản:** Từ HAProxy 2.4, `http-reuse` mặc định
> chuyển từ `never` sang `safe` — nếu upgrade từ 2.0, cấu hình
> cũ có thể hoạt động khác mà không có dòng nào thay đổi trong
> file config.
```

**Khi directive bị loại bỏ:**

```markdown
> **Lưu ý phiên bản:** Directive `nbproc` fully supported ở 2.0,
> deprecated ở 2.4, và bị loại bỏ hoàn toàn từ 2.5. Multi-threading
> (`nbthread`) thay thế hoàn toàn multi-process.
```

Sau khi viết annotation trong Part, **bắt buộc** cập nhật bảng tương ứng trong file này với cột "Nguồn Part" trỏ đến Part và section đã nhắc. Quy trình hai bước này đảm bảo không mất thông tin.

---

## Thống kê tổng hợp (cập nhật khi viết thêm Part)

| Metric | Giá trị |
|---|---|
| Tổng số thay đổi đã ghi nhận | 52 |
| Từ 2.0 → 2.4 | ~15 thay đổi |
| Từ 2.4 → 2.8 | ~12 thay đổi |
| Từ 2.8 → 3.0+ | ~8 thay đổi |
| Parts đã đóng góp dữ liệu | Part 1, README |
| Parts chưa viết (cần bổ sung khi viết) | Part 2–28 |

---

## Tài liệu tham khảo cho nghiên cứu Part 29

Khi đến Part 29, tham khảo các nguồn chính thống sau để xác minh và bổ sung chi tiết cho từng entry:

1. [HAProxy 2.0 Release Notes](https://www.haproxy.org/download/2.0/src/CHANGELOG)
2. [HAProxy 2.4 Release Notes](https://www.haproxy.org/download/2.4/src/CHANGELOG)
3. [HAProxy 2.8 Release Notes](https://www.haproxy.org/download/2.8/src/CHANGELOG)
4. [HAProxy 3.0 Release Notes](https://www.haproxy.org/download/3.0/src/CHANGELOG)
5. [Announcing HAProxy 2.4 — haproxy.com](https://www.haproxy.com/blog/announcing-haproxy-2-4)
6. [Announcing HAProxy 2.8 — haproxy.com](https://www.haproxy.com/blog/announcing-haproxy-2-8)
7. [Announcing HAProxy 3.0 — haproxy.com](https://www.haproxy.com/blog/announcing-haproxy-3-0)
8. [Ubuntu Packages — HAProxy](https://packages.ubuntu.com/search?keywords=haproxy)
