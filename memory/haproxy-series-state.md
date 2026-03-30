# HAProxy Onboard Series — State Tracker

> Trạng thái từng Part trong series 29 phần. Claude đọc file này để biết
> Part nào đã viết, Part nào đang viết, Part nào chưa bắt đầu.
> **Tên Part phải khớp 100% với `haproxy-onboard/README.md` (source of truth).**

**Baseline:** HAProxy 2.0 trên Ubuntu 20.04 (Canonical official repo)

**Version mapping:**
| Ubuntu LTS | HAProxy version | Kernel |
|------------|----------------|--------|
| 20.04 | 2.0.x | 5.4 |
| 22.04 | 2.4.x | 5.15 |
| 24.04 | 2.8.x | 6.8 |

---

## Block I — Nền tảng kiến trúc và vận hành (Parts 1-5)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 1 | Lịch sử hình thành và kiến trúc HAProxy | DONE | `1.0 - haproxy-history-and-architecture.md` | Professor-style reviewed, fact-checked (3 corrections applied), 10 URLs verified, Quiz added |
| 2 | Cài đặt và quản lý dịch vụ HAProxy | NOT STARTED | — | |
| 3 | Cấu trúc cấu hình và các khái niệm cốt lõi | NOT STARTED | — | |
| 4 | Mô hình kết nối và connection management | NOT STARTED | — | |
| 5 | Timeout và vòng đời kết nối | NOT STARTED | — | |

## Block II — Ngôn ngữ xử lý traffic (Parts 6-10)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 6 | Fetches và Converters — hệ thống truy vấn dữ liệu của HAProxy | NOT STARTED | — | |
| 7 | ACL và content switching | NOT STARTED | — | |
| 8 | HTTP request/response rules | NOT STARTED | — | |
| 9 | TCP request/response rules | NOT STARTED | — | |
| 10 | Map files, pattern matching, và error handling | NOT STARTED | — | |

## Block III — Cân bằng tải và session management (Parts 11-14)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 11 | Thuật toán cân bằng tải | NOT STARTED | — | |
| 12 | Health checks | NOT STARTED | — | |
| 13 | Stick tables: cấu trúc, tracking counters, và peers | NOT STARTED | — | |
| 14 | Session persistence và rate limiting | NOT STARTED | — | |

## Block IV — Giao thức và mã hóa (Parts 15-19)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 15 | SSL/TLS termination và certificate management | NOT STARTED | — | |
| 16 | Mutual TLS, OCSP, CRL, và tự động hóa certificate | NOT STARTED | — | |
| 17 | HTTP/2, HTTP/3, WebSocket và gRPC | NOT STARTED | — | |
| 18 | Proxy Protocol | NOT STARTED | — | |
| 19 | Authentication: HTTP Basic Auth và JWT validation | NOT STARTED | — | |

## Block V — Tính năng nâng cao và mở rộng (Parts 20-24)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 20 | DNS resolvers và dynamic backends | NOT STARTED | — | |
| 21 | HTTP cache và compression | NOT STARTED | — | |
| 22 | Lua scripting và mở rộng HAProxy | NOT STARTED | — | |
| 23 | Runtime API và quản trị động | NOT STARTED | — | |
| 24 | Logging, monitoring, và observability | NOT STARTED | — | |

## Block VI — Production operations (Parts 25-29)

| Part | Tên | Status | File | Notes |
|------|-----|--------|------|-------|
| 25 | Performance tuning và kernel optimization | NOT STARTED | — | Prerequisites: P5, P12 |
| 26 | High availability: Keepalived, VRRP, và seamless reload | NOT STARTED | — | Prerequisites: P2, P12 |
| 27 | Security hardening và DDoS mitigation | NOT STARTED | — | Prerequisites: P5, P14, P15 |
| 28 | Lab thực hành tổng hợp | NOT STARTED | — | Prerequisites: P25, P26, P27 |
| 29 | So sánh phiên bản HAProxy trên các Ubuntu LTS | NOT STARTED | — | Prerequisites: P1 |

---

## Thống kê

- **Đã hoàn thành:** 1/29 (3.4%)
- **Đang viết:** 0/29
- **Chưa bắt đầu:** 28/29
