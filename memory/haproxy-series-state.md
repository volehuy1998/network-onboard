# HAProxy Onboard Series, State Tracker

> Status of every Part in the 29-Part series. Read this to know which Parts are written, in progress, or not started. **Part names should match `haproxy-onboard/README.md` (the source of truth).**

**Baseline:** HAProxy 2.0 on Ubuntu 20.04 (Canonical official repo).

**Version mapping:**

| Ubuntu LTS | HAProxy version | Kernel |
|------------|-----------------|--------|
| 20.04 | 2.0.x | 5.4 |
| 22.04 | 2.4.x | 5.15 |
| 24.04 | 2.8.x | 6.8 |

---

## Block I, Foundation architecture and operations (Parts 1-5)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 1 | Lịch sử hình thành và kiến trúc HAProxy | DONE | `1.0 - haproxy-history-and-architecture.md` | Professor-style reviewed, fact-checked (3 corrections), 10 URLs verified, Quiz added |
| 2 | Cài đặt và quản lý dịch vụ HAProxy | NOT STARTED | (none) | |
| 3 | Cấu trúc cấu hình và các khái niệm cốt lõi | NOT STARTED | (none) | |
| 4 | Mô hình kết nối và connection management | NOT STARTED | (none) | |
| 5 | Timeout và vòng đời kết nối | NOT STARTED | (none) | |

## Block II, Traffic processing language (Parts 6-10)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 6 | Fetches và Converters, hệ thống truy vấn dữ liệu của HAProxy | NOT STARTED | (none) | |
| 7 | ACL và content switching | NOT STARTED | (none) | |
| 8 | HTTP request/response rules | NOT STARTED | (none) | |
| 9 | TCP request/response rules | NOT STARTED | (none) | |
| 10 | Map files, pattern matching, và error handling | NOT STARTED | (none) | |

## Block III, Load balancing and session management (Parts 11-14)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 11 | Thuật toán cân bằng tải | NOT STARTED | (none) | |
| 12 | Health checks | NOT STARTED | (none) | |
| 13 | Stick tables, structure, tracking counters, peers | NOT STARTED | (none) | |
| 14 | Session persistence và rate limiting | NOT STARTED | (none) | |

## Block IV, Protocols and encryption (Parts 15-19)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 15 | SSL/TLS termination và certificate management | NOT STARTED | (none) | |
| 16 | Mutual TLS, OCSP, CRL, certificate automation | NOT STARTED | (none) | |
| 17 | HTTP/2, HTTP/3, WebSocket, gRPC | NOT STARTED | (none) | |
| 18 | Proxy Protocol | NOT STARTED | (none) | |
| 19 | Authentication, HTTP Basic Auth + JWT validation | NOT STARTED | (none) | |

## Block V, Advanced features and extensibility (Parts 20-24)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 20 | DNS resolvers và dynamic backends | NOT STARTED | (none) | |
| 21 | HTTP cache và compression | NOT STARTED | (none) | |
| 22 | Lua scripting và HAProxy extension | NOT STARTED | (none) | |
| 23 | Runtime API và dynamic admin | NOT STARTED | (none) | |
| 24 | Logging, monitoring, observability | NOT STARTED | (none) | |

## Block VI, Production operations (Parts 25-29)

| Part | Vietnamese title | Status | File | Notes |
|------|------------------|--------|------|-------|
| 25 | Performance tuning và kernel optimization | NOT STARTED | (none) | Prerequisites: P5, P12 |
| 26 | High availability, Keepalived, VRRP, seamless reload | NOT STARTED | (none) | Prerequisites: P2, P12 |
| 27 | Security hardening và DDoS mitigation | NOT STARTED | (none) | Prerequisites: P5, P14, P15 |
| 28 | Lab thực hành tổng hợp | NOT STARTED | (none) | Prerequisites: P25, P26, P27 |
| 29 | So sánh phiên bản HAProxy trên các Ubuntu LTS | NOT STARTED | (none) | Prerequisites: P1 |

---

## Statistics

- **Done:** 1/29 (3.4%).
- **In progress:** 0/29.
- **Not started:** 28/29.

---

## References

- `haproxy-onboard/README.md`: source of truth for Part titles + reading order.
- `haproxy-onboard/references/haproxy-version-evolution.md`: version evolution tracker (Rule 3).
- `CLAUDE.md`: project working memory + Rules.
