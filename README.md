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

# SDN — Software Defined Networking (OVN/OVS/OpenFlow)

**Release:** `v3.1-OperatorMaster` (2026-04-24). 116 file, ~52.6K dòng. Phase G Operator Mastery 5/5 area COMPLETE. Xem [`CHANGELOG.md`](CHANGELOG.md) cho release notes đầy đủ.

Chương trình đào tạo Software Defined Networking tập trung thuần vào **OpenvSwitch, OpenFlow, và OVN** như các nền tảng portable. Xây dựng từ lịch sử Stanford Clean Slate 2006 đến production forensic analysis OVN multichassis 2026 + operator daily playbook. Xem chi tiết roadmap: [`sdn-onboard/README.md`](sdn-onboard/README.md).

**5 trụ cột kỹ năng cần đạt được**: (1) nền tảng kiến thức OVS/OpenFlow/OVN vững chắc + chi tiết, (2) am hiểu tường tận tools OVS/OVN cung cấp, (3) hiểu sâu output của tools (anatomy từng field), (4) debug + troubleshoot skill, (5) kiến trúc + cơ chế hoạt động.

**Cấu trúc 20 Block (rev 5, 2026-04-24)**:
- **Foundation (Block 0-XIII)**: 14 block với 78 file — từ "Why SDN" (Part 1) qua OpenFlow evolution (Part 3-4 đầy đủ match+action catalog), alternative SDN paradigms (Part 5-6), controller ecosystem (Part 7), Linux primer (Part 8), OVS internals + ops (Part 9 tier 1 complete), OVSDB (Part 10), overlay + tunnel labs (Part 11), DC topology (Part 12), đến OVN foundation (Part 13 full LS/LR pipeline exhaustive).
- **Expert Extension (Block XIV-XVI, optional, deprioritized)**: 3 block với 9 file — P4 programmable pipeline (Part 14), service mesh partial (Part 15.0), kernel+DPDK performance (Part 16). Block XV K8S/Service Mesh + Block XVI DPDK/XDP deprioritized theo user directive để focus OVS/OpenFlow/OVN core.
- **Advanced case studies (Block XVII-XIX)**: 3 Part forensic analysis production OVN multichassis (FDB poisoning + ARP responder + PMTUD multichassis binding).
- **Operations (Block XX, new Phase G)**: 7 Part daily operator workflow — systematic debugging (20.0), security hardening + audit trail (20.1), OVN troubleshooting deep-dive (20.2), OVN daily operator playbook (20.3), OVS daily operator playbook (20.4), OVN forensic case studies (20.5), retrospective 2007-2024 (20.6).

Trọng tâm flagship:

[Part 17 - OVN L2 Forwarding và FDB Poisoning](sdn-onboard/17.0%20-%20ovn-l2-forwarding-and-fdb-poisoning.md)

- 17.1 - Tại sao OVN tồn tại: bài toán gốc và hành trình giải quyết
- 17.2 - Localnet port: cầu nối giữa thế giới ảo và VLAN vật lý
- 17.3 - MC_FLOOD và MC_UNKNOWN: broadcast và unknown destination trong distributed control plane
- 17.4 - FDB table và dynamic MAC learning: từ bài toán flooding đến caching
- 17.5 - MAC_Binding table: IP-to-MAC resolution trên logical router
- 17.6 - Case study: FDB poisoning trên provider network VLAN 3808
- 17.7 - Bài học thiết kế: trade-off và tiến hóa incremental

[Part 18 - OVN ARP Responder và BUM Suppression](sdn-onboard/18.0%20-%20ovn-arp-responder-and-bum-suppression.md)

- 18.1 - Bối cảnh: ARP trên mạng vật lý và hiệu ứng khuếch đại trong overlay
- 18.2 - Dòng chảy lịch sử: từ l2population đến ARP Responder tích hợp trong OVN
- 18.3 - Cơ chế ARP Responder: Ingress Table 26 và hệ thống bốn tầng priority
- 18.4 - Port_security: gate trung tâm quyết định ARP Responder có hoạt động hay không
- 18.5 - ARP Responder và FDB: hai cơ chế độc lập cho hai bài toán
- 18.6 - Khi ARP Responder vắng mặt: incidents thực tế và đánh giá triển khai
- 18.7 - Bốn kiến trúc ARP suppression và arp_proxy

[Part 19 - OVN Multichassis Binding, PMTUD và activation-strategy](sdn-onboard/19.0%20-%20ovn-multichassis-binding-and-pmtud.md)

- 19.1 - Lịch sử ba thời kỳ live migration trong OVN (pre-22.09 → 22.09 → 24.03+)
- 19.2 - Multichassis port binding lifecycle (CAN_BIND_AS_MAIN/ADDITIONAL/CANNOT_BIND)
- 19.3 - `enforce_tunneling_for_multichassis_ports` + sáu kịch bản packet path
- 19.4 - Geneve 58-byte overhead + PMTUD pipeline + bug FDP-620 root cause
- 19.5 - activation-strategy=rarp: tín hiệu đồng bộ ba tầng
- 19.6 - Operational tuning: Jumbo frame + MTU cache recovery
- 19.7 - Design lessons + Khuyến nghị vận hành
- Lab 1: Verification playbook sáu lớp (POE framework)
- Lab 2: Reproduce bug FDP-620 với `ping -s 6000`
- Lab 3: Đo Geneve overhead trên wire bằng tcpdump + wireshark

**Operations flagship (Block XX, Phase G 2026-04):**

[Part 20.0 - OVS+OVN Systematic Debugging](sdn-onboard/20.0%20-%20ovs-ovn-systematic-debugging.md) — isolation-first philosophy + 5-layer model + 3 production case study (VM no network race, upgrade schema drift, partition thundering herd).

[Part 20.1 - OVS+OVN Security Hardening + Audit Trail](sdn-onboard/20.1%20-%20ovs-ovn-security-hardening.md) — 4-layer defense-in-depth (control/management/data plane) + port_security + ACL default-deny + audit trail + cert rotation zero-downtime + 2 GE + Capstone POE.

[Part 20.2 - OVN Troubleshooting Deep-dive](sdn-onboard/20.2%20-%20ovn-troubleshooting-deep-dive.md) — `ovn-trace` 11 option + `ovn-detrace` chain + Port_Binding 8 type forensic + ovn-appctl 21 command + 16-symptom diagnostic matrix + 3 GE + Capstone POE.

[Part 20.3 - OVN Daily Operator Playbook](sdn-onboard/20.3%20-%20ovn-daily-operator-playbook.md) — 10 task category (health check + inventory + port lifecycle + ACL + LB+NAT + DHCP+DNS + gateway+HA + conntrack + performance + backup) + 2 workflow end-to-end (new-tenant + tenant-teardown script).

[Part 20.4 - OVS Daily Operator Playbook](sdn-onboard/20.4%20-%20ovs-daily-operator-playbook.md) — sister của 20.3 nhưng OVS pure-datapath. 10 task category + 2 workflow (new-bridge.sh + bridge-decommission.sh) + 4 CLI layer distinguish (vsctl / ofctl / dpctl / appctl).

[Part 20.5 - OVN Forensic Case Studies](sdn-onboard/20.5%20-%20ovn-forensic-case-studies.md) — 3 distributed control plane case study (Port_Binding migration race + northd bulk tenant deletion memory cascade + MAC_Binding ARP scan exploit) + 3 design lesson.

[Part 20.6 - OVS/OpenFlow/OVN Retrospective 2007-2024](sdn-onboard/20.6%20-%20ovs-openflow-ovn-retrospective-2007-2024.md) — 5 thời kỳ (sơ khai / reality đối mặt / hypervisor overlays thắng / OVN era / production hardening) + 10 meta-lesson universal + 6 frontier 2024-2030.

**OVS deep internals forensic (Block IX):**

- [Part 9.25 - OVS flow debugging + ofproto/trace](sdn-onboard/9.25%20-%20ovs-flow-debugging-ofproto-trace.md) — 10 GE + 4 POE, `ofproto/trace` grammar end-to-end.
- [Part 9.26 - OVS Revalidator Storm Forensic](sdn-onboard/9.26%20-%20ovs-revalidator-storm-forensic.md) — 3 case study (megaflow invalidation + LACP bond flap cascade + conntrack zone collision cross-chassis migration) + 4 GE + 1 Capstone POE.
- [Part 9.27 - OVS+OVN Packet Journey End-to-end](sdn-onboard/9.27%20-%20ovs-ovn-packet-journey-end-to-end.md) — 3-tier parallel diagnostic framework + Geneve TLV deep-dive + MTU forensic + 10 fault catalog pattern.

**Expert Extension (Block XIV-XVI, optional):**

- [Part 14.0-14.2 - P4 Programmable Pipeline](sdn-onboard/14.0%20-%20p4-language-fundamentals.md) — P4_16 + PSA + PISA + Tofino silicon + P4Runtime gRPC + Stratum.
- [Part 15.0 - Service Mesh Integration](sdn-onboard/15.0%20-%20service-mesh-integration.md) — Istio + Envoy + Linkerd + Cilium eBPF + OVN-Kubernetes CNI.
- [Part 16.0-16.2 - Kernel + DPDK Performance](sdn-onboard/16.0%20-%20dpdk-afxdp-kernel-tuning.md) — DPDK EAL + AF_XDP zero-copy + hugepage + NUMA affinity + perf + bpftrace profiling.

---

# HAProxy — Cân bằng tải chuyên sâu

29 phần, 6 khối — từ kiến trúc event-driven đến production operations. Baseline: HAProxy 2.0 trên Ubuntu 20.04 (Canonical official repo).

[Xem mục lục chi tiết, sơ đồ phụ thuộc kiến thức, và lộ trình đọc](haproxy-onboard/README.md)