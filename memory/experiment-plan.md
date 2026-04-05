# Experiment Plan — FD Deep Dive & Beyond

> Kế hoạch chi tiết cho các thí nghiệm tiếp theo trên `huyvl-lab-fd`.
> Claude đọc file này khi cần biết experiment nào đã chạy, experiment nào cần chạy.
>
> **Cập nhật lần cuối:** 2026-04-04 (session 2)

---

## Inventory: Trạng thái 9 exercises hiện tại

| # | Heading | Section | Line | Lab Output | Status |
|---|---------|---------|------|-----------|--------|
| 1 | Guided Exercise 1: Quan sát ba FD tiêu chuẩn | 1.2 | 55 | Real (huyvl-lab-fd) | VERIFIED |
| 2 | Guided Exercise 2: So sánh open(), dup(), fork() trên cùng file | 1.3 | 164 | Real (PIDs 578, 587) | VERIFIED |
| 3 | Guided Exercise 3: Write-side proof — OFD sharing | 1.3 | 356 | Real (PID 558) | VERIFIED |
| 4 | Guided Exercise 4: Status flags chia sẻ qua OFD | 1.3 | 476 | Real (không có fork, output đúng sẵn) | VERIFIED |
| 5 | Guided Exercise 5: lseek xuyên process | 1.3 | 554 | Real (PID 566) | VERIFIED |
| 6 | Guided Exercise 6: Socket là file descriptor | 1.4 | 659 | Real (PID 558) | VERIFIED |
| 7 | Guided Exercise 7: strace TCP server | 1.9 | 900 | **"Output kỳ vọng"** — placeholder | NEEDS LAB |
| 8 | Lab 8: FD limit và kết nối tối đa | 1.9 | 941 | Self-directed (chỉ có instructions) | NEEDS LAB |
| 9 | Guided Exercise 9: CLOEXEC leak vs no leak | 1.10 | 1080 | Real (PIDs 527, 577) | VERIFIED |

**Ghi chú exercise 4 (Status flags):** Không cần redesign background child vì exercise này
không có fork() — chỉ thao tác trên shell hiện tại (mở 3 FD, fcntl qua python3, đọc
`/proc/$$/fdinfo`). Output trong tài liệu khớp thực tế từ trước khi redesign.

**Tổng:** 7/9 verified, 2/9 cần lab.

---

## PHASE A — Lab verification còn thiếu (ưu tiên 1, session tiếp theo)

> Mục tiêu: Thay toàn bộ placeholder/expected output bằng real output từ huyvl-lab-fd.
> Rule 7 (Terminal Output Fidelity) áp dụng: copy nguyên văn, không cắt bớt.

---

### A1. Guided Exercise 7: strace TCP server (line 900-937)

**Vấn đề:** Line 925 ghi "Output kỳ vọng (FD number có thể khác tùy hệ thống)" — 4 dòng
strace output là placeholder (FD 4, port 47968).

**Runbook — chạy trên huyvl-lab-fd:**

```bash
# ====== CHUẨN BỊ ======
# Đảm bảo không có process chiếm port 8080
ss -tlnp | grep 8080
# Nếu có → kill trước

# ====== BƯỚC 1: Khởi strace + Python server ======
strace -e trace=socket,bind,listen,accept4,close -f python3 -m http.server 8080 2>/tmp/strace_output.txt &
# → Ghi nhận: [N] PID — paste output lên chat

# Chờ server sẵn sàng
sleep 2

# ====== BƯỚC 2: Gửi request ======
curl -s http://localhost:8080/ > /dev/null

# ====== BƯỚC 3: Lấy strace output ======
grep -E 'socket|bind|listen|accept' /tmp/strace_output.txt
# → Paste TOÀN BỘ output lên chat (Rule 7: không cắt)

# ====== BƯỚC 4: Gửi thêm 1 request để thấy FD reuse ======
curl -s http://localhost:8080/ > /dev/null
grep -E 'accept' /tmp/strace_output.txt
# → Paste output lên chat

# ====== BƯỚC 5: Cleanup ======
kill %1 2>/dev/null; wait 2>/dev/null
kill %2 2>/dev/null; wait 2>/dev/null
rm -f /tmp/strace_output.txt
```

**Lines cần thay thế trong tài liệu:** 927-930 (4 dòng strace placeholder)
**Có thể cần thay thế thêm:** Line 934 (mô tả FD reuse) nếu FD number khác 5.

**Lưu ý kỹ thuật:**
- strace `-f` flag theo dõi cả child processes — Python http.server có thể fork worker
- FD number phụ thuộc vào Python internals (import modules mở FDs trước khi gọi socket)
- Port number trong accept4 output là ephemeral port của curl — sẽ khác mỗi lần
- `SOCK_CLOEXEC` flag phải xuất hiện trong cả `socket()` lẫn `accept4()` — đây là Python 3 best practice

---

### A2. Lab 8: FD limit (line 941-967)

**Vấn đề:** Exercise hiện là self-directed (chỉ instructions, không có output mẫu). Cần quyết
định: giữ self-directed hay thêm reference output.

**Đề xuất:** Thêm reference output section (giống RHCSA exam: instructions → student chạy →
có "Answer Key" section ở cuối để tự kiểm tra). Giữ instructions nguyên, thêm output bên dưới.

**Runbook — chạy trên huyvl-lab-fd:**

```bash
# ====== BƯỚC 1: Kiểm tra limits ======
ulimit -Sn
# → Paste output (thường 1024)
ulimit -Hn
# → Paste output (thường 1048576 hoặc 524288)

# ====== BƯỚC 2: Giảm soft limit ======
ulimit -n 20
ulimit -Sn
# → Paste output (phải là 20)

# ====== BƯỚC 3: Start server trong shell bị giới hạn ======
python3 -m http.server 8080 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Đếm FD ban đầu
ls /proc/$SERVER_PID/fd/ | wc -l
ls -la /proc/$SERVER_PID/fd/
# → Paste output — cho thấy baseline FD count

# ====== BƯỚC 4: Stress test từ TERMINAL KHÁC ======
# (MỞ TERMINAL MỚI — terminal mới có ulimit mặc định, không bị giới hạn 20)

# Terminal 2: tạo nhiều concurrent connections giữ lâu (keep-alive)
for i in $(seq 1 25); do
  curl -s --keepalive-time 30 http://localhost:8080/ > /dev/null &
done
wait

# Hoặc dùng ab (Apache Benchmark) nếu có:
# ab -n 100 -c 20 http://localhost:8080/

# ====== BƯỚC 5: Observe "Too many open files" ======
# Quay lại terminal 1:
# → Xem stderr của Python server — sẽ có OSError: [Errno 24] Too many open files
# → Paste error output lên chat

# Đếm FD tại thời điểm peak:
ls /proc/$SERVER_PID/fd/ | wc -l
# → Paste output

# ====== BƯỚC 6: Tính toán ======
# 20 (limit) - 3 (stdin/out/err) - 1 (listen socket) = 16 FDs cho connections
# Nhưng Python nội bộ mở thêm FDs (modules, __pycache__) → thực tế ít hơn
# → Kiểm tra: ls /proc/$SERVER_PID/fd/ khi CHƯA có connection nào → đếm baseline

# ====== CLEANUP ======
kill $SERVER_PID 2>/dev/null
# Mở terminal mới để lấy lại ulimit mặc định
```

**Lines cần thay đổi trong tài liệu:**
- Giữ nguyên instructions (line 949-961)
- Thêm section "Reference Output" SAU "Evaluation" (line 963) với real output
- Hoặc: thêm output inline vào mỗi bước (giống exercises 1-6)

**Quyết định cần từ user:** Inline output hay reference section riêng?

---

## PHASE B — WCAG spacing fixes (ưu tiên 2, cùng session hoặc session riêng)

> 3 pre-existing SVGs có minor text spacing violations.
> Sửa nhanh, không ảnh hưởng content.

| SVG | Figure | Vấn đề |
|-----|--------|--------|
| `images/fd-fork-exec-cloexec.svg` | Fig 1-13 | Text spacing 0.5-2.5px shortfall |
| `images/fd-kernel-3-table-model.svg` | Fig 1-1 | Text spacing 0.5-2.5px shortfall |
| `images/fd-select-poll-vs-epoll.svg` | Fig 1-12 | Text spacing 0.5-2.5px shortfall |

**Action:**
1. Chạy svg-audit.py trên 3 file → xác định violations cụ thể
2. Sửa spacing (tăng font-size hoặc giảm nội dung text)
3. Chạy diacritics-audit.py → verify Vietnamese diacritics
4. svg-caption-consistency.py → verify captions
5. Null byte check

---

## PHASE C — Mở rộng FD document (ưu tiên 3, sessions riêng)

### C1. epoll practical exercise (thêm vào section 1.7 hoặc 1.9)

**Mục tiêu:** Hands-on với epoll — hiện section 1.7 chỉ có lý thuyết + benchmark.

**Concept — 2 versions so sánh:**

```
Version 1: Python select() echo server
  - socket() → bind() → listen()
  - select([server_fd, *client_fds], ..., timeout=1)
  - Loop: mỗi iteration scan TẤT CẢ FDs

Version 2: Python selectors (epoll backend) echo server
  - Cùng logic, nhưng dùng selectors.DefaultSelector (→ epoll trên Linux)
  - epoll_ctl(ADD) khi client mới
  - epoll_wait() chỉ trả FDs có events

Verification bằng strace:
  strace -e select,epoll_ctl,epoll_wait -f python3 server_select.py
  strace -e select,epoll_ctl,epoll_wait -f python3 server_epoll.py
  → So sánh syscall patterns: O(n) scan vs O(1) notification
```

**Giá trị:** Bridge lý thuyết → thực hành. Người đọc THẤY sự khác biệt qua strace output.

**Files cần tạo:**
- `linux-onboard/examples/echo_select.py` (10-15 dòng)
- `linux-onboard/examples/echo_epoll.py` (10-15 dòng)
- 1 SVG diagram so sánh (hoặc dùng lại Fig 1-12 đã có)

### C2. signalfd / eventfd / timerfd (section mới 1.11 hoặc phụ lục)

**Mục tiêu:** Mở rộng "everything is a file" sang non-traditional FD types.

```
Exercise signalfd:
  - python3: import signalfd (hoặc C snippet)
  - Tạo signalfd cho SIGUSR1
  - kill -USR1 $PID → read() trên signalfd FD → nhận signal data
  - ls /proc/$PID/fd/ → thấy FD mới (anon_inode:[signalfd])
  - Liên hệ: thay thế signal handler (async-unsafe) bằng synchronous FD read

Exercise timerfd:
  - python3: ctypes wrapper cho timerfd_create
  - Set interval 1 giây → epoll_wait → tick
  - strace: timerfd_create, timerfd_settime, read(timerfd)
  - Liên hệ: HAProxy dùng timerfd cho timeout management

Exercise eventfd:
  - python3: os.eventfd() (Python 3.10+) hoặc ctypes
  - Producer write(eventfd, 1) → consumer read(eventfd) → wakeup
  - Liên hệ: Nginx thread pool notification
```

**Prerequisite:** Kiểm tra Python version trên huyvl-lab-fd (`python3 --version`).
Python 3.10+ có `os.eventfd()`. Nếu < 3.10 → dùng ctypes hoặc viết C.

### C3. /proc/sys/fs/file-nr + system-wide monitoring (thêm vào section 1.9)

```
Bước 1: cat /proc/sys/fs/file-nr
  → 3 số: allocated | unused-but-allocated | max
  Ví dụ: 1280    0       9223372036854775807

Bước 2: So sánh per-process limit vs system-wide
  ulimit -n     → per-process soft limit (thường 1024)
  sysctl fs.file-max   → system-wide max
  cat /proc/sys/fs/file-nr → system-wide hiện tại

Bước 3: Monitoring script
  watch -n 1 'cat /proc/sys/fs/file-nr; echo "---"; ls /proc/$$/fd | wc -l'

Bước 4: Liên hệ HAProxy
  - global maxconn tính toán: maxconn × 2 (frontend + backend) + overhead
  - HAProxy tự gọi setrlimit(RLIMIT_NOFILE, maxconn*2+...margin)
  - haproxy -vv → dòng "Total" cho thấy FD budget tính toán
```

---

## PHASE D — HAProxy series labs: Parts 2-5 (Block I)

> Prerequisite: Part 1 DONE. VM cần: Ubuntu 20.04, HAProxy 2.0.x
> Mỗi Part = 1-2 sessions.

### D1. Part 2: Cài đặt và quản lý dịch vụ HAProxy

```
Lab 2.1: Installation
  apt install haproxy
  haproxy -vv                          # version + build options
  dpkg -L haproxy                      # file list
  systemctl status haproxy             # systemd unit
  cat /etc/haproxy/haproxy.cfg         # default config

Lab 2.2: Config validation
  haproxy -c -f /etc/haproxy/haproxy.cfg         # syntax check
  # Cố tình viết sai → xem error message format

Lab 2.3: Reload vs restart
  systemctl reload haproxy             # graceful — giữ connections
  systemctl restart haproxy            # hard — drop connections
  ss -tlnp | grep haproxy             # quan sát listener trước/sau
  # strace -e kill,sendto -p $(pidof haproxy) → thấy signal sequence

Lab 2.4: Master-worker mode
  # HAProxy 2.0+: master process + worker processes
  ps auxf | grep haproxy              # thấy process tree
  cat /proc/$(pidof -s haproxy)/status | grep Threads
```

### D2. Part 3: Cấu trúc cấu hình

```
Lab 3.1: Minimal working config
  # Viết config tối thiểu: global + defaults + frontend + backend
  # frontend bind :80 → default_backend
  # backend: 2 Python http.server trên port 8081, 8082
  python3 -m http.server 8081 &
  python3 -m http.server 8082 &
  systemctl reload haproxy
  curl -v http://localhost/              # → round-robin giữa 2 backends

Lab 3.2: Stats page
  # Thêm: stats enable, stats uri /stats, stats auth admin:admin
  # Mở browser: http://server:80/stats
  # Hoặc: curl -u admin:admin http://localhost/stats

Lab 3.3: listen shorthand
  # Viết cùng config bằng listen vs frontend+backend
  # haproxy -c → cả hai đều valid
  # So sánh: listen = syntactic sugar

Lab 3.4: Log setup
  # global: log /dev/log local0
  # defaults: log global, option httplog
  # Kiểm tra: journalctl -u haproxy hoặc /var/log/haproxy.log
  curl http://localhost/ → xem log entry format
```

### D3. Part 4: Connection management

```
Lab 4.1: HTTP mode vs TCP mode
  # Config 1: mode http → HAProxy parse HTTP, thêm X-Forwarded-For
  # Config 2: mode tcp → HAProxy transparent, không parse
  # tcpdump -i lo -A port 8081 → thấy header injection trong HTTP mode

Lab 4.2: maxconn cascading
  # frontend maxconn 100
  # backend maxconn 50
  # server srv1 maxconn 10
  # Stress test: ab -n 100 -c 20 http://localhost/
  # show stat (Unix socket) → quan sát qcur, scur, slim

Lab 4.3: Connection reuse
  # option http-reuse always
  # tcpdump → quan sát TCP connections (ít hơn requests nếu reuse hoạt động)
  # stats page: conn_rate, req_rate
```

### D4. Part 5: Timeout

```
Lab 5.1: timeout server
  # Backend: python3 script sleep 5 giây trước khi respond
  # Config: timeout server 2s
  # curl → nhận 504 Gateway Timeout
  # Log: termination code "sD" (server timeout during data)

Lab 5.2: timeout http-request (slowloris protection)
  # Config: timeout http-request 5s
  # nc localhost 80 → gõ chậm, không gửi \r\n\r\n → bị disconnect sau 5s
  # Log: termination code "cR" (client timeout during request)

Lab 5.3: timeout queue
  # server maxconn 1 + timeout queue 3s
  # Gửi 5 concurrent requests → 1 served, 4 queued → sau 3s queue timeout
  # Log: termination code "cQ" (client timeout in queue)

Lab 5.4: Timeout diagnosis exercise
  # Đưa log line có termination code → student phân tích timeout nào trigger
  # Ví dụ: "... 2000/0/-1/0/2001 504 ..." → timeout server (sD)
```

---

## PHASE E — Network onboard series (tương lai, sau Block I HAProxy)

> Chờ sau khi HAProxy Block I (Parts 1-5) hoàn thành.
> Chưa có content — chỉ là placeholder cho roadmap.

- CCNA-level: IP subnetting, VLAN config, static routing
- OVN/OVS lab: logical switch, logical router, ACLs
- BGP/OSPF lab: containerlab hoặc GNS3
- Wireshark exercises: TCP handshake analysis, TLS 1.3

---

## Execution Priority & Effort Estimate

```
Phase A  (A1 + A2)        → 1 session     → NEXT
Phase B  (WCAG fixes)     → 30 phút       → cùng session hoặc session sau
Phase D1 (HAProxy Part 2) → 1-2 sessions  → sau khi merge PR hiện tại
Phase C1 (epoll hands-on) → 1 session     → xen kẽ HAProxy nếu cần thay đổi topic
Phase D2 (HAProxy Part 3) → 1-2 sessions
Phase D3 (HAProxy Part 4) → 1-2 sessions
Phase D4 (HAProxy Part 5) → 1-2 sessions
Phase C2 (signalfd/...)   → 1-2 sessions  → sau Block I
Phase C3 (/proc/sys/...)  → 30 phút       → gộp với C1 hoặc C2
Phase E  (Network)        → TBD
```

**Tổng Block I HAProxy:** ~6-8 sessions (Parts 2-5, mỗi Part 1-2 sessions)
**Tổng FD expansion:** ~3-4 sessions (C1 + C2 + C3)

---

## Lab Environment

| Lab | VM/Host | Software | Status |
|-----|---------|----------|--------|
| FD exercises (Phase A, C) | `huyvl-lab-fd` | bash, python3, strace, ss, curl, gcc | Existing |
| HAProxy labs (Phase D) | Cần setup | Ubuntu 20.04, HAProxy 2.0.x, python3 (backends) | TBD |
| Network labs (Phase E) | Cần setup | containerlab hoặc GNS3, OVN/OVS | TBD |

**HAProxy lab topology đề xuất:**
```
                    ┌──────────────┐
  Client ──────────►│  HAProxy LB  │──────────► Backend 1 (python3 :8081)
                    │  :80 / :443  │──────────► Backend 2 (python3 :8082)
                    └──────────────┘
  Có thể chạy tất cả trên 1 VM nếu dùng loopback (127.0.0.1)
```
