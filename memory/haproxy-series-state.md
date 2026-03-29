# HAProxy Onboard Series — State Tracker

> Trạng thái từng Part trong series 29 phần. Claude đọc file này để biết
> Part nào đã viết, Part nào đang viết, Part nào chưa bắt đầu.

**Baseline:** HAProxy 2.0 trên Ubuntu 20.04 (Canonical official repo)

**Version mapping:**
| Ubuntu LTS | HAProxy version | Kernel |
|------------|----------------|--------|
| 20.04 | 2.0.x | 5.4 |
| 22.04 | 2.4.x | 5.15 |
| 24.04 | 2.8.x | 6.8 |

---

## Block I — Nền tảng kiến trúc (Parts 1-5)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 1 | Lịch sử và kiến trúc HAProxy | DONE | `1.0 - haproxy-history-and-architecture.md` | Professor-style reviewed, fact-checked, 9 URLs verified |
| 2 | Cài đặt HAProxy 2.0 từ Canonical repo | NOT STARTED | — | |
| 3 | Frontend, Backend, Listen — Mô hình proxy hai phía | NOT STARTED | — | |
| 4 | Connection Model — HTTP keep-alive, tunnel, close | NOT STARTED | — | |
| 5 | Timeout — Hiểu đúng để tránh sự cố | NOT STARTED | — | |

## Block II — Ngôn ngữ cấu hình (Parts 6-10)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 6 | Fetches và Converters | NOT STARTED | — | |
| 7 | ACL — Điều kiện định tuyến | NOT STARTED | — | |
| 8 | HTTP Rules — Hành động trên request/response | NOT STARTED | — | |
| 9 | Maps — Dynamic routing | NOT STARTED | — | |
| 10 | Stick Tables (cơ bản) — Session tracking | NOT STARTED | — | |

## Block III — Phân phối tải (Parts 11-14)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 11 | Thuật toán Load Balancing | NOT STARTED | — | |
| 12 | Health Checks — L4, L7, agent | NOT STARTED | — | |
| 13 | Stick Tables (nâng cao) — Rate limiting, abuse detection | NOT STARTED | — | |
| 14 | Connection và Rate Limiting | NOT STARTED | — | |

## Block IV — Bảo mật và giao thức (Parts 15-19)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 15 | SSL/TLS Termination | NOT STARTED | — | |
| 16 | SSL/TLS Passthrough và Re-encryption | NOT STARTED | — | |
| 17 | HTTP/2 và WebSocket | NOT STARTED | — | |
| 18 | Proxy Protocol | NOT STARTED | — | |
| 19 | Authentication — Basic, JWT, client cert | NOT STARTED | — | |

## Block V — Vận hành (Parts 20-24)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 20 | DNS Resolution và Service Discovery | NOT STARTED | — | |
| 21 | HTTP Caching | NOT STARTED | — | |
| 22 | Compression | NOT STARTED | — | |
| 23 | Runtime API và Stats | NOT STARTED | — | |
| 24 | Logging — Format, syslog, tracing | NOT STARTED | — | |

## Block VI — Production (Parts 25-29)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 25 | Performance Tuning | NOT STARTED | — | Prerequisites: P5, P12 |
| 26 | HA với Keepalived/VRRP | NOT STARTED | — | Prerequisites: P2, P12 |
| 27 | Security Hardening | NOT STARTED | — | Prerequisites: P5, P14, P15 |
| 28 | Lab tổng hợp | NOT STARTED | — | Prerequisites: P25, P26, P27 |
| 29 | So sánh phiên bản HAProxy | NOT STARTED | — | Prerequisites: P1 (đọc bất kỳ lúc nào sau P1) |

---

## Thống kê

- **Đã hoàn thành:** 1/29 (3.4%)
- **Đang viết:** 0/29
- **Chưa bắt đầu:** 28/29

## Version Evolution Tracker

File: `haproxy-onboard/references/haproxy-version-evolution.md`
- **Entries:** 52
- **Categories:** 12
- **Cập nhật lần cuối:** 2026-03-29 (commit `919341b`)
