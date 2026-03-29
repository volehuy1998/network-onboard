# network-onboard

:pushpin: Lưu ý bài viết sau sử dụng môi trường thực hành lý tưởng là bản phân phối [Red Hat Enterprise Linux 9](https://access.redhat.com/downloads/content/479/ver=/rhel---9/9.3/x86_64/product-software), có thể sử dụng [CentOS 9](https://cloud.centos.org/centos/9-stream/x86_64/images/) để thay thế nhưng không khuyến khích. Ngoài ra có thể tạo tài khoản Red Hat để đọc tài liệu chính hãng miễn phí, tham gia thảo luận tại [cộng đồng học viên](https://learn.redhat.com/) hoặc [tại đây](https://access.redhat.com/discussions) (dành cho khách hàng sử dụng sản phẩm RHEL).

[Phần 1 - Lịch sử hình thành và phát triển Linux](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/1.0%20-%20linux-history-onboard.md)

- 1.1 - Những thập niên 1969 (UPDATED 21/08/2023)
- 1.2 - Những thập niên 1980 (UPDATED 21/08/2023)
- 1.3 - Những thập niên 1990 (UPDATED 21/08/2023)
- 1.4 - Năm 2015 (UPDATED 21/08/2023)
- 1.5 - Khái niệm phân phối (UPDATED 21/08/2023)
- 1.6 - Giấy phép lưu hành (UPDATED 21/08/2023)

[Phần 2 - Kiến trúc Linux](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.0%20-%20linux-arch-onboard.md)

- [2.1 - Linux Kernel (UPDATED 21/01/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.1%20-%20linux-arch-onboard.md#linux_kernel)
  - 2.1.1 - Vai trò của Linux Kernel (UPDATED 21/01/2024)
  - 2.1.2 - Tổng quan về Interrupt - Ngắt (UPDATED 05/09/2023)
- [2.2 - Quản lý người dùng và nhóm ( :arrow_up: UPDATED 15/04/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.2%20-%20linux-user-management.md#user_and_group)
  - 2.2.1 - Khái niệm `User` (UPDATED 17/09/2023)
  - 2.2.2 - Khái niệm về nhóm, chính và phụ (UPDATED 12/09/2023)
  - 2.2.3 - Thay đổi tài khoản người dùng (UPDATED 13/09/2023)
  - 2.2.4 - Các thao tác quản lý trên người dùng và nhóm(UPDATED 11/09/2023)
  - 2.2.5 - Hạn chế quyền truy cập người dùng (UPDATED 13/09/2023)
  - 2.2.6 - Cấp quyền `sudo` cho nhóm `wheel` ( :arrow_up: UPDATED 15/04/2024)
  - 2.2.7 - Cấp quyền `sudo` cụ thể ( :arrow_up: UPDATED 15/04/2024)
- [2.3 - Hệ thống tệp tin (UPDATED 07/01/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.3%20-%20linux-file-system-overview.md#fs)
  - 2.3.1 - Phân cấp hệ thống tệp tin (UPDATED 26/08/2023)
  - 2.3.2 - RPM Package và phân loại (UPDATED 24/08/2023)
  - 2.3.3 - Kernel RPM Package (UPDATED 24/08/2023)
  - 2.3.4 - Tổng quan về quyền trên tệp tin (UPDATED 07/01/2024)
    - 2.3.4.1 - Quản lý quyền tệp tin (UPDATED 13/09/2023)
    - 2.3.4.2 - Quyền đặc biệt dành cho chủ sở hữu (SUID) và lỗ hổng leo thang đặc quyền (UPDATED 10/09/2023)
    - 2.3.4.3 - Quyền đặc biệt dành cho nhóm (UPDATED 10/09/2023)
    - 2.3.4.4 - Quyền đặc biệt Sticky bit (UPDATED 04/09/2023)
  - 2.3.5 - Xác định hệ thống tệp tin và thiết bị (UPDATED 07/11/2023)
- [2.4 - Tổng quan tiến trình Linux (UPDATED 04/10/2023)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.4%20-%20linux-process-overview.md#linux_process)
  - 2.4.1 - Trạng thái của tiến trình Linux (UPDATED 17/09/2023)
  - 2.4.2 - Kiểm soát các `Job` (UPDATED 04/10/2023)
  - 2.4.3 - Kết thúc tiến trình (UPDATED 18/09/2023)
  - 2.4.4 - Dịch vụ hạ tầng (UPDATED 21/09/2023)
  - 2.4.5 - Tổng quan về `systemd` (UPDATED 30/09/2023)
  - 2.4.6 - Kiểm soát dịch vụ hệ thống (UPDATED 04/10/2023)
  - 2.4.7 - Mẫu `unit` với ký hiệu `@` (UPDATED 04/10/2023)
  - 2.4.8 - Chi tiết tệp `unit` (UPDATED 04/10/2023)
    - 2.4.8.1 - Loại `unit` phổ biến `*.service` (UPDATED 03/10/2023)
    - 2.4.8.2 - Loại `unit` về `*.socket` (UPDATED 30/09/2023)
    - 2.4.8.3 - Loại `unit` về `*.path` (UPDATED 30/09/2023)
- [2.5 - Điều khiển an toàn từ xa (UPDATED 31/12/2023)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.5%20-%20linux-secure-remote-overview.md#remote_connection)
  - 2.5.1 - Tổng quan về kiến trúc giao thức `SSH` (UPDATED 31/12/2023)
    - 2.5.1.1 - Kiến trúc giao thức `SSH` (UPDATED 22/10/2023)
    - 2.5.1.2 - Những xem xét bảo mật về khía cạnh truyền dẫn (UPDATED 19/10/2023)
    - 2.5.1.3 - Những xem xét bảo mật về khía cạnh xác thực (UPDATED 19/10/2023)
    - 2.5.1.4 - Giao thức `SSH-1`, `SSH-2` và sự cải tiến (UPDATED 22/10/2023)
  - 2.5.2 - Cài đặt `OpenSSH`, kết nối và cấu hình (UPDATED 23/10/2023)
    - 2.5.2.1 - Sử dụng công cụ cơ bản (UPDATED 19/10/2023)
    - 2.5.2.2 - Thông tin về `finger print` tại máy khách và máy chủ (UPDATED 19/10/2023)
    - 2.5.2.3 - Hành vi xử lý chuẩn kết nối đến máy chủ (UPDATED 19/10/2023)
    - 2.5.2.4 - Cấu hình `ssh client` (UPDATED 21/10/2023)
    - 2.5.2.5 - Sử dụng `X11 Forwarding` và `Port Forwarding` (UPDATED 23/10/2023)
- [2.6 - Tổng quan về quản lý mạng (UPDATED 05/11/2023)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.6%20-%20linux-network-overview.md#network_manage)
  - 2.6.1 - Mô hình `TCP/IP` (UPDATED 25/10/2023)
  - 2.6.2 - Mô tả về `Network Interface` (UPDATED 01/11/2023)
  - 2.6.3 - Địa chỉ `v4` (UPDATED 25/10/2023)
  - 2.6.4 - Địa chỉ `v6` (UPDATED 25/10/2023)
  - 2.6.5 - Thông tin về `network interface`(UPDATED 25/10/2023)
  - 2.6.6 - Công cụ quản lý `nmcli`(UPDATED 05/11/2023)
  - 2.6.7 - Cấu hình và quản lý `hostname`(UPDATED 05/11/2023)
- [2.7 - Kiến trúc nhật ký hệ thống (UPDATED 17/12/2023)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.7%20-%20linux-system-log-architecture-overview.md#sys_log_arch)
  - 2.7.1 - Tổng quan (UPDATED 03/12/2023)
  - 2.7.2 - Cách sử dụng `rsyslog` (UPDATED 06/12/2023)
  - 2.7.3 - Cách sử dụng `systemd-journald` (UPDATED 10/12/2023)
  - 2.7.4 - Đồng bộ thời gian (UPDATED 17/12/2023)
    - 2.7.4.1 - Tổng quan `Network Time Protocol` (UPDATED 17/12/2023)
    - 2.7.4.2 - Công cụ `datetimectl` (UPDATED 10/12/2023)
    - 2.7.4.3 - Cấu hình `NTP` sử dụng `chrony` (UPDATED 17/12/2023)
    - 2.7.4.4 - Cấu hình `NTP` sử dụng `ntpd` (UPDATED 10/12/2023)
- [2.8 - Lập lịch chạy cho tác vụ tương lai (UPDATED 01/01/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.8%20-%20linux-job-scheduler.md#schedule_job)
  - 2.8.1 - Tổng quan (UPDATED 24/12/2023)
  - 2.8.2 - Cách sử dụng công cụ `at` (UPDATED 24/12/2023)
  - 2.8.3 - Cách sử dụng công cụ `cron` (UPDATED 24/12/2023)
  - 2.8.4 - Ứng dụng `systemd timer` (UPDATED 01/01/2024)
    - 2.8.4.1 - Cách sử dụng công cụ `systemd timer` (UPDATED 01/01/2024)
    - 2.8.4.2 - Quản lý loại tệp tạm thời (UPDATED 01/01/2024)
      - 2.8.4.2.1 - Cách sử dụng `systemd-tmpfiles --create` (UPDATED 01/01/2024)
      - 2.8.4.2.2 - Cách sử dụng `systemd-tmpfiles --clean` (UPDATED 01/01/2024)
      - 2.8.4.2.3 - Cách sử dụng `systemd-tmpfiles --remove` (UPDATED 01/01/2024)
- [2.9 - Quản lý tệp đóng gói và nén với công cụ `tar` (UPDATED 09/02/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.9%20-%20linux-manage-compressed-tar-archives.md#manage_compress_tar_archive)
    - 2.9.1 - Tạo và quản lý tệp đóng gói (UPDATED 09/02/2024)
    - 2.9.2 - Tạo và quản lý tệp nén đóng gói (UPDATED 15/01/2024)
    - 2.9.3 - Quản lý tệp sao lưu gia tăng `incremental backup` (UPDATED 15/01/2024)
    - 2.9.4 - Chuyển tệp giữa các hệ thống một cách an toàn (UPDATED 15/01/2024)
    - 2.9.5 - Đồng bộ giữa các hệ thống một cách an toàn (UPDATED 15/01/2024)
- [2.10 - Quản lý `SELinux` (UPDATED 28/01/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.10%20-%20linux-se-mode.md#selinux_manage)
    - 2.10.1 - Kiến trúc `SELinux` (UPDATED 27/01/2024)
    - 2.10.2 - Sử dụng `SELinux` cơ bản với chính sách `targeted` (UPDATED 28/01/2024)
      - 2.10.2.1 - Xem nhãn, kích hoạt và vô hiệu hóa `SELinux` (UPDATED 28/01/2024)
      - 2.10.2.2 - Xem định nghĩa chính sách `SELinux` (UPDATED 27/01/2024)
      - 2.10.2.3 - Auditing hành vi hệ thống (UPDATED 28/01/2024)
      - 2.10.2.4 - Kiểm soát `fcontext` với nhãn sẵn có (UPDATED 27/01/2024)
      - 2.10.2.5 - Kiểm soát `port` với nhãn sẵn có (UPDATED 27/01/2024)
      - 2.10.2.6 - Kiểm soát chính sách với  `boolean` (UPDATED 27/01/2024)
- [2.11 - Quản lý lưu trữ cơ bản (UPDATED 07/02/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.11%20-%20linux-manage-basic-storage.md#manage_basic_storage)
    - 2.11.1 - Khái niệm phân vùng ổ cứng (UPDATED 05/01/2024)
    - 2.11.2 - Quản lý phân vùng theo định dạng (UPDATED 05/01/2024)
      - 2.11.2.1 - Quản lý phân vùng định dạng MBR (UPDATED 07/02/2024)
      - 2.11.2.2 - Quản lý phân vùng định dạng GPT (UPDATED 05/01/2024)
      - 2.11.2.3 - So sanh giữa tạo phân vùng GPT và MBR (UPDATED 07/02/2024)
    - 2.11.3 - Tạo tệp hệ thống (UPDATED 05/01/2024)
    - 2.11.4 - Mount tệp hệ thống (UPDATED 05/01/2024)
      - 2.11.4.1 - Mount thủ công tệp hệ thống (UPDATED 05/01/2024)
      - 2.11.4.2 - Mount tự vĩnh viễn tệp hệ thống (UPDATED 05/01/2024)
    - 2.11.5 - Quản lý không gian `Swap` (UPDATED 05/01/2024)
      - 2.11.5.1 - Khái niệm không gian `Swap` (UPDATED 05/01/2024)
      - 2.11.5.2 - Tạo phân vùng `swap` (UPDATED 05/01/2024)
    - 2.11.6 - Tăng giảm kích thước phân vùng (UPDATED 07/02/2024)
- [2.12 - Quản lý lưu trữ nâng cao (UPDATED 09/02/2024)](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/2.12%20-%20linux-manage-advance-storage.md#manage_advance_storage)
  - 2.12.1 - Tổng quan Logical Volume Manager (LVM) (UPDATED 09/02/2024)
  - 2.12.2 - Xây dựng hệ thống lưu trữ LVM (UPDATED 09/02/2024)
  - 2.12.3 - Tạo Logical Volume tính năng nén và chống trùng lặp (UPDATED 09/02/2024)

---

# Cisco - Mạng cơ bản

[Cisco Module 1 - Liên lạc trong thế giới kết nối](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/cisco%20module%201%20-%20network-basic-communication-in-connected-world.md)
  - 1.0 - Loại mạng
    - 1.0.1 - Mọi thứ đều trực tuyến
    - 1.0.2 - Mạng cục bộ
    - 1.0.3 - Thiết bị di dộng
    - 1.0.4 - Các kết nối trong thiết bị gia đình
    - 1.0.5 - Các thiết bị kết nối khác
  - 1.1 - Truyền dữ liệu
      - 1.1.1 - Các loại dữ liệu cá nhân
      - 1.1.2 - Bit
      - 1.1.3 - Phương pháp phổ biến truyền tải dữ liệu
  - 1.2 - Băng thông và thông lượng
      - 1.2.1 - Băng thông
      - 1.2.2 - Thông lượng
  - 1.3 - Thông tin liên lạc trong thế giới kết nối lẫn nhau

[Cisco Module 2 - Các thành phần trong mạng, loại của chúng và các kết nối](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/cisco%20module%202%20-%20network-component-and-connections.md)
  - 2.0 - Vai trò máy khách và máy chủ
    - 2.0.1 - Giới thiệu
    - 2.0.2 - Mạng P2P
    - 2.0.3 - Ứng dụng P2P
    - 2.0.4 - Các vai trò trong mạng
  - 2.1 - Các thành phần trong mạng
      - 2.1.1 - Hạ tầng mạng
      - 2.1.2 - Thiết bị cuối
      - 2.1.3 - Thiết bị trung gian
  - 2.2 - LAN và WAN
  - 2.3 - Internet
  - 2.4 - ISP
      - 2.4.1 - Dịch vụ ISP
      - 2.4.2 - Kết nối ISP
      - 2.4.3 - Công nghệ truy cập Internet
      - 2.4.3 - Kết nối bổ sung

[INE - 1. Mạng máy tính là gì?](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%201.%20what-is-computer-network.md)

[INE - 2. Các thành phần trong mạng máy tính?](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%202.%20components-of-computer-networks.md)

[INE - 3. Các vị trí trong nghành mạng máy tính?](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%203.%20network-job-roles.md)
  - 3.1 - Kiến trúc sư, kỹ sư và quản trị viên
  - 3.2 - Chuyên môn

[INE - 4. Kiến trúc topo](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%204.%20network-topology-architectures.md)
  - 4.1 - Tổng quan kiến trúc mạng
  - 4.2 - Kiến trúc 2-Tier và 3-Tier
  - 4.3 - Kiến trúc Spine-Leaf
  - 4.4 - Kiến trúc WAN
  - 4.5 - Kiến trúc SOHO
  - 4.6 - Kiến trúc On-Premise và Cloud-Based

[INE - 5. Power Over Ethernet](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%205.%20power-over-ethernet.md)
  - 5.1 - Khái niệm PoE
  - 5.2 - Lợi ích của việc sử dụng PoE
  - 5.3 - PSE và PD

[INE - 6. Lịch sử và mục đích của Internet Protocol](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%206.%20history-and-purpose-of-ip.md)
  - 6.1 - Lịch sử phát triển chuyển mạch gói tin
  - 6.2 - Khái niệm chuyển mạch gói
  - 6.3 - Tổng quan về Internet Protocol

[INE - 7. Các trường trong tiêu đề IPv4](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%207.%20ipv4-header-fields.md)
  - 7.1 - Tổng quan thông tin tiêu đề IPv4
  - 7.2 - Ví dụ tìm vị trí fragment

[INE - 8. Xác định các bit thuộc phần Network ( UPDATED 15/07/2024)](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%208.%20identifying-the-network-bits.md)
  - 8.1 - Các lớp địa chỉ IPv4 (UPDATED 07/07/2024)
  - 8.2 - Khái niệm về `subnet mask` (UPDATED 07/07/2024)
  - 8.3 - Các loại địa chỉ IPv4 (UPDATED 07/07/2024)
      - 8.3.1 - Unicast (UPDATED 13/07/2024)
      - 8.3.2 - Multicast (UPDATED 14/07/2024)
      - 8.3.3 - Broadcast (UPDATED 15/07/2024)

[INE - 9. Tổng quan UDP (UPDATED 18/07/2024)](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%209.%20overview-of-udp.md)
  - 9.1 - Giới thiệu UDP (UPDATED 18/07/2024)
  - 9.2 - Các cổng ở tầng transport (UPDATED 18/07/2024)

[INE - 10. Tổng quan TCP ( :arrow_up: UPDATED 25/10/2024)](https://github.com/volehuy1998/network-onboard/blob/master/network-onboard/ine%20-%2010.%20overview-of-tcp.md)
  - 10.1 - Giới thiệu TCP ( :arrow_up: UPDATED 25/10/2024)
  - 10.2 - Khái niệm giao thức hướng kết nối ( :arrow_up: UPDATED 25/10/2024)
  - 10.3 - Tổng quan về cờ PSH và URG ( :arrow_up: UPDATED 25/10/2024)
  - 10.4 - Tổng quan kỹ thuật kiểm soát luồng ( :arrow_up: UPDATED 25/10/2024)
      - 10.4.1 - Tổng quan về Window Size vs Maximum Segment Size (MSS) ( :arrow_up: UPDATED 25/10/2024)
      - 10.4.2 - Phân biệt các loại kỹ thuật kiểm soát luồng ( :arrow_up: UPDATED 25/10/2024)
  - 10.5 - Tổng quan bắt tay 3 bước ( :arrow_up: UPDATED 25/10/2024)
  - 10.6 - Tổng quan kỹ thuật kiểm soát nghẽn ( :arrow_up: UPDATED 25/10/2024)

---

# HAProxy - Cân bằng tải chuyên sâu

:pushpin: Môi trường thực hành: Ubuntu Server 20.04 LTS, HAProxy 2.0.x (Canonical official repository, cài đặt qua `apt install haproxy`). Sau đó phân tích những thay đổi ở HAProxy 2.4 (Ubuntu 22.04) và HAProxy 2.8 (Ubuntu 24.04). Tài liệu tham khảo chính thống: [HAProxy Configuration Manual 2.0](https://www.haproxy.org/download/2.0/doc/configuration.txt), [HAProxy Starter Guide 2.0](https://www.haproxy.org/download/2.0/doc/intro.txt), và [HAProxy Management Guide 2.0](https://www.haproxy.org/download/2.0/doc/management.txt).

> **Lưu ý về phiên bản:** Ubuntu 20.04 chỉ cung cấp HAProxy 2.0.x từ Canonical official repo. Ubuntu 22.04 cung cấp HAProxy 2.4.x, Ubuntu 24.04 cung cấp HAProxy 2.8.x. Cài đặt phiên bản cao hơn (ví dụ: 3.2) yêu cầu PPA hoặc biên dịch từ mã nguồn — nằm ngoài hệ sinh thái chính thức của Canonical và không được khuyến nghị cho production. Phần 29 so sánh chi tiết các phiên bản.

## Khối I — Nền tảng kiến trúc và vận hành

[Phần 1 - Lịch sử hình thành và kiến trúc HAProxy](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/1.0%20-%20haproxy-history-and-architecture.md)

- 1.1 - Bối cảnh ra đời: bài toán C10K và giới hạn của mô hình thread-per-connection
- 1.2 - Willy Tarreau và sự ra đời của HAProxy
- 1.3 - Kiến trúc event-driven: epoll, single-process và multi-threading
- 1.4 - Vòng đời xử lý một kết nối trong HAProxy
- 1.5 - So sánh kiến trúc HAProxy với Nginx và LVS

[Phần 2 - Cài đặt và quản lý dịch vụ HAProxy](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/2.0%20-%20haproxy-installation-and-service-management.md)

- 2.1 - Cài đặt HAProxy 2.0 từ Canonical repo trên Ubuntu 20.04 (`apt install haproxy`)
- 2.2 - Master-worker process model: kiến trúc quản lý tiến trình hiện đại
- 2.3 - Phân tích tệp `haproxy.service` của systemd và mối quan hệ với master-worker
- 2.4 - Quản lý dịch vụ: khởi động, dừng, seamless reload (`-x`, `-sf`) và kiểm tra cấu hình
- 2.5 - Cấu trúc thư mục, phân quyền, system user `haproxy` và cơ chế chroot

[Phần 3 - Cấu trúc cấu hình và các khái niệm cốt lõi](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/3.0%20-%20haproxy-core-concepts.md)

- 3.1 - Năm section cấu hình: `global`, `defaults`, `frontend`, `backend`, `listen`
- 3.2 - Directive `bind`: lắng nghe trên địa chỉ:cổng, Unix socket, IPv4/IPv6 dual-stack
- 3.3 - Mode `tcp` và mode `http`: tầng hoạt động, hạn chế, và quyết định kiến trúc
- 3.4 - Directive `server`: định nghĩa backend, weight, và server states
- 3.5 - Biến môi trường và conditional configuration blocks

[Phần 4 - Mô hình kết nối và connection management](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/4.0%20-%20haproxy-connection-model.md)

- 4.1 - Hai kết nối TCP riêng biệt: client-side và server-side
- 4.2 - HTTP keep-alive: persistent connections và tác động đến performance
- 4.3 - HTTP/1.1 connection reuse và connection pooling giữa HAProxy và backend
- 4.4 - HTTP/2 multiplexing: nhiều stream trên một kết nối TCP
- 4.5 - Ảnh hưởng của mô hình kết nối đến logging, ACL, và troubleshooting

[Phần 5 - Timeout và vòng đời kết nối](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/5.0%20-%20haproxy-timeouts-and-connection-lifecycle.md)

- 5.1 - Tại sao timeout là cấu hình quan trọng nhất trong production
- 5.2 - `timeout connect`: thời gian chờ TCP handshake đến backend
- 5.3 - `timeout client` và `timeout server`: kiểm soát hai phía kết nối
- 5.4 - `timeout http-request`, `timeout http-keep-alive`, `timeout tunnel` và `timeout queue`
- 5.5 - Phân tích hiệu ứng domino khi timeout sai: từ một giá trị đến sự cố toàn hệ thống

## Khối II — Ngôn ngữ xử lý traffic

[Phần 6 - Fetches và Converters — hệ thống truy vấn dữ liệu của HAProxy](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/6.0%20-%20haproxy-fetches-and-converters.md)

- 6.1 - Tại sao cần hiểu fetches/converters trước khi học ACL và rules
- 6.2 - Sample fetches: trích xuất dữ liệu từ request, response, connection, và nội bộ HAProxy
- 6.3 - Converters: biến đổi dữ liệu (chuỗi, IP, số, mã hóa, hash, base64)
- 6.4 - Chuỗi fetch-convert: `hdr(host),lower,map(/etc/haproxy/hosts.map)`
- 6.5 - Danh mục fetches quan trọng: `src`, `dst`, `path`, `hdr()`, `ssl_fc`, `req.body`, `sc_http_req_rate()`

[Phần 7 - ACL và content switching](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/7.0%20-%20haproxy-acl-and-content-switching.md)

- 7.1 - Cú pháp ACL: `acl <name> <fetch> <flags> <operator> <value>`
- 7.2 - Matching types: boolean, string, IP, integer, regex
- 7.3 - Routing traffic: `use_backend`, `default_backend`, và SNI-based routing trong mode tcp
- 7.4 - Kết hợp ACL: toán tử `AND` (ngầm định), `OR` (`||`), `NOT` (`!`)
- 7.5 - ACL files: tách pattern ra file ngoài cho quản lý quy mô lớn

[Phần 8 - HTTP request/response rules](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/8.0%20-%20haproxy-http-rules.md)

- 8.1 - Vòng đời xử lý request: thứ tự thực thi `http-request` → routing → `http-response`
- 8.2 - `http-request`: deny, reject, tarpit, silent-drop, redirect, set-header, del-header, add-header
- 8.3 - `http-response`: chỉnh sửa response trước khi gửi về client
- 8.4 - `http-after-response`: xử lý response sau khi đã qua bộ lọc (cache, compression)
- 8.5 - HTTP rewriting: thay đổi path, query string, và redirect 301/302/303

[Phần 9 - TCP request/response rules](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/9.0%20-%20haproxy-tcp-rules.md)

- 9.1 - `tcp-request connection`: hành động ngay khi TCP handshake hoàn tất, trước khi đọc dữ liệu
- 9.2 - `tcp-request content`: hành động sau khi đọc dữ liệu từ client (TLS SNI, payload inspection)
- 9.3 - `tcp-response content`: can thiệp dữ liệu trả về từ backend
- 9.4 - Kết hợp TCP rules với stick tables để rate limiting ở tầng kết nối

[Phần 10 - Map files, pattern matching, và error handling](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/10.0%20-%20haproxy-maps-and-error-handling.md)

- 10.1 - Map files: tra cứu key-value cho routing, rewriting, và response
- 10.2 - Runtime API: cập nhật map files mà không cần reload (`set map`, `add map`)
- 10.3 - Error handling: `errorfile`, `errorloc`, section `http-errors`, custom error pages
- 10.4 - Retry mechanism: `retry-on`, cấu hình retry cho connection failure và HTTP errors

## Khối III — Cân bằng tải và session management

[Phần 11 - Thuật toán cân bằng tải](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/11.0%20-%20haproxy-load-balancing-algorithms.md)

- 11.1 - `roundrobin` và `static-rr`: trọng số, dynamic weight adjustment
- 11.2 - `leastconn`: phân phối theo số kết nối hiện tại và trường hợp sử dụng
- 11.3 - Hash-based: `source`, `uri`, `hdr()`, `rdp-cookie` — consistent hashing và hash-type
- 11.4 - `random` và `first`: các trường hợp đặc biệt
- 11.5 - Thay đổi thuật toán và weight tại runtime qua Runtime API

[Phần 12 - Health checks](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/12.0%20-%20haproxy-health-checks.md)

- 12.1 - Layer 4 health check: TCP SYN, cơ chế `fall`/`rise`/`inter`/`fastinter`/`downinter`
- 12.2 - Layer 7 health check: HTTP/HTTPS request, kiểm tra status code và body content
- 12.3 - `agent-check`: health check thông minh điều khiển từ phía backend (drain, maint, weight)
- 12.4 - Passive health check: `observe layer4`/`observe layer7`, phát hiện lỗi từ traffic thực tế
- 12.5 - Email alerts: cấu hình `mailers` thông báo khi backend thay đổi trạng thái

[Phần 13 - Stick tables: cấu trúc, tracking counters, và peers](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/13.0%20-%20haproxy-stick-tables.md)

- 13.1 - Cấu trúc stick table: `type`, `size`, `expire`, `store`
- 13.2 - Key types: `ip`, `ipv6`, `integer`, `string`, `binary`
- 13.3 - Tracking counters: `gpc0`, `gpt0`, `http_req_rate`, `conn_rate`, `conn_cur`, `bytes_in_rate`
- 13.4 - Tương tác stick table với ACL: `sc_http_req_rate()`, `sc_conn_cur()`, `sc_gpc0_rate()`
- 13.5 - Peers protocol: đồng bộ stick table giữa nhiều HAProxy nodes

[Phần 14 - Session persistence và rate limiting](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/14.0%20-%20haproxy-persistence-and-rate-limiting.md)

- 14.1 - Cookie-based persistence: `cookie insert`, `cookie prefix`, `cookie rewrite`
- 14.2 - Stick table-based persistence: `stick on src`, `stick match`, `stick store-request`
- 14.3 - Rate limiting bằng stick table: giới hạn request/giây, connection/giây theo IP
- 14.4 - Tarpit và silent-drop: phản ứng với client vi phạm rate limit
- 14.5 - So sánh trade-off: cookie persistence vs stick table persistence

## Khối IV — Giao thức và mã hóa

[Phần 15 - SSL/TLS termination và certificate management](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/15.0%20-%20haproxy-ssl-tls.md)

- 15.1 - SSL offloading: giải mã TLS tại HAProxy, plaintext đến backend
- 15.2 - Cấu hình certificate: `crt`, `ca-file`, `crt-list`, và section `crt-store`
- 15.3 - Cipher suites: `ssl-default-bind-ciphers` (TLS 1.2) vs `ssl-default-bind-ciphersuites` (TLS 1.3)
- 15.4 - SNI và ALPN: phân biệt domain và giao thức trên cùng IP:port
- 15.5 - Certificate hot-reload: cập nhật certificate không cần restart
- 15.6 - kTLS: tăng tốc mã hóa thông qua kernel TLS offload (Ubuntu 22.04+)

[Phần 16 - Mutual TLS, OCSP, CRL, và tự động hóa certificate](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/16.0%20-%20haproxy-mtls-ocsp-acme.md)

- 16.1 - Mutual TLS (mTLS): `verify required`, `ca-file`, trích xuất thông tin certificate client
- 16.2 - OCSP Stapling: kiểm tra trạng thái thu hồi certificate, auto-update (HAProxy 2.8+)
- 16.3 - CRL (Certificate Revocation List): `crl-file` và quản lý danh sách thu hồi
- 16.4 - ACME protocol: tự động xin và renew certificate Let's Encrypt/ZeroSSL (HAProxy 3.2, experimental)

[Phần 17 - HTTP/2, HTTP/3, WebSocket và gRPC](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/17.0%20-%20haproxy-modern-protocols.md)

- 17.1 - HTTP/2 frontend và backend: `alpn h2`, multiplexing, stream prioritization
- 17.2 - HTTP/3 và QUIC: UDP transport, `quic-bind`, `tune.quic.frontend.max-tx-mem`
- 17.3 - WebSocket proxying: upgrade mechanism, `timeout tunnel`, và mode tcp fallback
- 17.4 - gRPC proxying: bidirectional streaming qua HTTP/2 backend
- 17.5 - Trade-off: HTTP/1.1 vs HTTP/2 vs HTTP/3 cho từng loại workload

[Phần 18 - Proxy Protocol](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/18.0%20-%20haproxy-proxy-protocol.md)

- 18.1 - Vấn đề mất địa chỉ IP client sau khi qua proxy: tại sao X-Forwarded-For không đủ
- 18.2 - Proxy Protocol v1 (text) và v2 (binary): cấu trúc header và khi nào dùng v2
- 18.3 - Directive `send-proxy`, `send-proxy-v2`, `accept-proxy` trên frontend và backend
- 18.4 - TLV extensions trong Proxy Protocol v2: truyền thêm metadata (SSL info, unique ID)
- 18.5 - Tích hợp với Nginx, Apache, và các backend khác

[Phần 19 - Authentication: HTTP Basic Auth và JWT validation](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/19.0%20-%20haproxy-authentication.md)

- 19.1 - HTTP Basic Authentication: section `userlist`, `http_auth()`, `http_auth_group()`
- 19.2 - JWT validation: `jwt_verify()`, trích xuất claims với `jwt_header_query`, `jwt_payload_query`
- 19.3 - Kết hợp authentication với ACL để bảo vệ backend theo role
- 19.4 - So sánh: xác thực tại HAProxy vs xác thực tại application — khi nào làm gì

## Khối V — Tính năng nâng cao và mở rộng

[Phần 20 - DNS resolvers và dynamic backends](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/20.0%20-%20haproxy-dns-and-dynamic-backends.md)

- 20.1 - Section `resolvers`: cấu hình DNS resolver riêng cho HAProxy
- 20.2 - `server-template`: tự động tạo backend servers từ DNS SRV records
- 20.3 - `init-addr`: khởi động HAProxy trước khi DNS sẵn sàng
- 20.4 - Dynamic server management: thêm/xóa server qua Runtime API
- 20.5 - Tích hợp với Consul, Kubernetes DNS, và service discovery

[Phần 21 - HTTP cache và compression](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/21.0%20-%20haproxy-cache-and-compression.md)

- 21.1 - HTTP cache tích hợp: section `cache`, `http-request cache-use`, `http-response cache-store`
- 21.2 - Cache tuning: `total-max-size`, `max-object-size`, `max-age`
- 21.3 - HTTP compression: `compression algo gzip`, `compression type`, filter architecture
- 21.4 - Bandwidth limiting: `filter bwlim-in`, `filter bwlim-out` (HAProxy 2.7+)

[Phần 22 - Lua scripting và mở rộng HAProxy](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/22.0%20-%20haproxy-lua-scripting.md)

- 22.1 - Tại sao Lua: khi ACL và map files không đủ linh hoạt
- 22.2 - Lua actions, fetches, converters, và services: bốn điểm mở rộng
- 22.3 - Ví dụ thực tế: custom health check, dynamic routing, request transformation
- 22.4 - Lua performance: coroutine model, non-blocking I/O, và giới hạn cần biết
- 22.5 - SPOE (Stream Processing Offload Engine): xử lý ngoài process cho tác vụ nặng

[Phần 23 - Runtime API và quản trị động](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/23.0%20-%20haproxy-runtime-api.md)

- 23.1 - Stats socket: cấu hình `stats socket`, permission levels (admin/operator/user)
- 23.2 - Lệnh quản trị: `show stat`, `show info`, `show servers state`, `show table`
- 23.3 - Thao tác runtime: `set server`, `set weight`, `disable server`, `enable server`
- 23.4 - Cập nhật map và ACL files: `set map`, `add map`, `del map`, `show map`
- 23.5 - Master CLI: quản lý tất cả workers từ master process (`@@`)

[Phần 24 - Logging, monitoring, và observability](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/24.0%20-%20haproxy-logging-and-monitoring.md)

- 24.1 - Cấu hình `rsyslog` cho HAProxy: facility, severity, và log tách riêng
- 24.2 - Log format: `option httplog`, `option tcplog`, `log-format` tùy chỉnh, timing fields
- 24.3 - Ring buffer logging: `ring` section, ghi log vào bộ nhớ thay vì syslog
- 24.4 - Stats page: `stats enable`, `stats uri`, ý nghĩa từng trường và cột
- 24.5 - Prometheus exporter: endpoint `/metrics`, tích hợp Grafana

## Khối VI — Production operations

[Phần 25 - Performance tuning và kernel optimization](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/25.0%20-%20haproxy-performance-tuning.md)

- 25.1 - `nbthread`, thread groups, và CPU binding: tận dụng multi-core
- 25.2 - `maxconn` và mối quan hệ với `LimitNOFILE`, `sysctl fs.nr_open`
- 25.3 - Kernel tuning: `sysctl` cho TCP stack (`net.core.somaxconn`, `net.ipv4.tcp_tw_reuse`, `net.ipv4.ip_local_port_range`)
- 25.4 - `splice()`: zero-copy data forwarding giữa socket file descriptors
- 25.5 - Buffer tuning: `tune.bufsize`, `tune.maxrewrite`, `tune.recv_enough`
- 25.6 - Benchmarking: phương pháp đo lường chính xác với `wrk`, `hey`, và `h2load`

[Phần 26 - High availability: Keepalived, VRRP, và seamless reload](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/26.0%20-%20haproxy-high-availability.md)

- 26.1 - Keepalived và VRRP protocol: chuyển đổi VIP giữa hai HAProxy nodes
- 26.2 - Seamless reload: cờ `-x` (fd passing qua Unix socket) và `-sf` (graceful stop)
- 26.3 - Hitless upgrade: nâng cấp HAProxy phiên bản không downtime
- 26.4 - Master-worker và fd passing: cơ chế truyền file descriptor giữa old/new worker
- 26.5 - Connection draining: `set server drain` và graceful server removal

[Phần 27 - Security hardening và DDoS mitigation](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/27.0%20-%20haproxy-security-hardening.md)

- 27.1 - Defense in depth: chroot, drop privileges, `CapabilityBoundingSet`, AppArmor trên Ubuntu
- 27.2 - HTTP Request Smuggling: nguyên lý CL/TE desync và cách HAProxy phòng chống
- 27.3 - Slowloris và slow POST: `timeout http-request`, `timeout client`
- 27.4 - DDoS mitigation: connection rate limiting với stick tables, `silent-drop`, `tarpit`
- 27.5 - HTTP/2 Rapid Reset (CVE-2023-44487): tại sao HAProxy không bị ảnh hưởng

[Phần 28 - Lab thực hành tổng hợp](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/28.0%20-%20haproxy-real-world-labs.md)

- 28.1 - Lab: Kiến trúc web application multi-tier (HAProxy + Nginx + App + Database)
- 28.2 - Lab: TCP proxy cho MySQL/PostgreSQL cluster với health check và failover
- 28.3 - Lab: API Gateway với ACL, JWT validation, rate limiting và SSL termination
- 28.4 - Lab: HTTP/2 frontend với gRPC backend và Prometheus monitoring
- 28.5 - Lab: High availability với Keepalived VRRP và seamless reload dưới tải

[Phần 29 - So sánh phiên bản HAProxy trên các Ubuntu LTS](https://github.com/volehuy1998/network-onboard/blob/master/haproxy-onboard/29.0%20-%20haproxy-version-comparison.md)

- 29.1 - HAProxy 2.0 (Ubuntu 20.04 default): đặc điểm và giới hạn
- 29.2 - HAProxy 2.4 (Ubuntu 22.04 default): tính năng mới và thay đổi hành vi
- 29.3 - HAProxy 2.8 (Ubuntu 24.04 default): cải tiến hiệu suất, OCSP auto-update
- 29.4 - HAProxy 3.2 (LTS mới nhất): QUIC, HTTP/3, ACME, thread groups
- 29.5 - Benchmark so sánh định lượng trên cùng workload và phần cứng