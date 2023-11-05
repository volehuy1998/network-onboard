# network-onboard
[Phần 1 - Lịch sử hình thành và phát triển Linux](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/linux-history-onboard.md)

- 1.1 - Những thập niên 1969 (UPDATED 21/08/2023)
- 1.2 - Những thập niên 1980 (UPDATED 21/08/2023)
- 1.3 - Những thập niên 1990 (UPDATED 21/08/2023)
- 1.4 - Năm 2015 (UPDATED 21/08/2023)
- 1.5 - Khái niệm phân phối (UPDATED 21/08/2023)
- 1.6 - Giấy phép lưu hành (UPDATED 21/08/2023)

[Phần 2 - Kiến trúc Linux](https://github.com/volehuy1998/network-onboard/blob/master/linux-onboard/linux-arch-onboard.md)

- 2.1 - Linux Kernel (UPDATED 27/08/2023)
- 2.2 - Vai trò của Linux Kernel (UPDATED 24/08/2023)
- 2.3 - Tổng quan về Interrupt - Ngắt (UPDATED 05/09/2023)
- 2.4 - Quản lý người dùng và nhóm (UPDATED 17/09/2023)
    - 2.4.1 - Khái niệm `User` (UPDATED 17/09/2023)
    - 2.4.2 - Khái niệm về nhóm, chính và phụ (UPDATED 12/09/2023)
    - 2.4.3 - Thay đổi tài khoản người dùng (UPDATED 13/09/2023)
    - 2.4.4 - Các thao tác quản lý trên người dùng và nhóm(UPDATED 11/09/2023)
    - 2.4.5 - Hạn chế quyền truy cập người dùng (UPDATED 13/09/2023)
    - 2.4.6 - Cấp quyền `sudo` tự do (UPDATED 11/09/2023)
    - 2.4.7 - Cấp quyền `sudo` với lệnh cụ thể (UPDATED 11/09/2023)
- 2.5 - Hệ thống tệp tin (UPDATED 04/10/2023)
    - 2.5.1 - Phân cấp hệ thống tệp tin (UPDATED 26/08/2023)
    - 2.5.2 - Tổng quan về quyền trên tệp tin (UPDATED 09/09/2023)
    - 2.5.3 - RPM Package và phân loại (UPDATED 24/08/2023)
    - 2.5.4 - Kernel RPM Package (UPDATED 24/08/2023)
    - 2.5.4 - Tổng quan về quyền trên tệp tin (UPDATED 04/10/2023)
        - 2.5.4.1 - Quản lý quyền tệp tin (UPDATED 13/09/2023)
        - 2.5.4.2 - Quyền đặc biệt dành cho chủ sở hữu (SUID) và lỗ hổng leo thang đặc quyền (UPDATED 10/09/2023)
        - 2.5.4.3 - Quyền đặc biệt dành cho nhóm(UPDATED 10/09/2023)
        - 2.5.4.4 - Quyền đặc biệt Sticky bit(UPDATED 04/09/2023)
- 2.6 - Tổng quan tiến trình Linux (UPDATED 04/10/2023)
    - 2.6.1 - Trạng thái của tiến trình Linux (UPDATED 17/09/2023)
    - 2.6.2 - Kiểm soát các `Job` (UPDATED 04/10/2023)
    - 2.6.3 - Kết thúc tiến trình (UPDATED 18/09/2023)
    - 2.6.4 - Dịch vụ hạ tầng (UPDATED 21/09/2023)
    - 2.6.5 - Tổng quan về `systemd` (UPDATED 30/09/2023)
    - 2.6.6 - Kiểm soát dịch vụ hệ thống (UPDATED 04/10/2023)
    - 2.6.7 - Mẫu `unit` với ký hiệu `@` (UPDATED 04/10/2023)
    - 2.6.8 - Chi tiết tệp `unit` (UPDATED 04/10/2023)
        - 2.6.8.1 - Loại `unit` phổ biến `*.service` (UPDATED 03/10/2023)
        - 2.6.8.2 - Loại `unit` về `*.socket` (UPDATED 30/09/2023)
        - 2.6.8.3 - Loại `unit` về `*.path` (UPDATED 30/09/2023)
- 2.7 - Điều khiển an toàn từ xa (UPDATED 23/10/2023)
  - 2.7.1 - Tổng quan về kiến trúc giao thức `SSH` (:UPDATED 22/10/2023)
    - 2.7.1.1 - Kiến trúc giao thức `SSH` (UPDATED 22/10/2023)
    - 2.7.1.2 - Những xem xét bảo mật về khía cạnh truyền dẫn (UPDATED 19/10/2023)
    - 2.7.1.3 - Những xem xét bảo mật về khía cạnh xác thực (UPDATED 19/10/2023)
    - 2.7.1.4 - Giao thức `SSH-1`, `SSH-2` và sự cải tiến (UPDATED 22/10/2023)
  - 2.7.2 - Cài đặt `OpenSSH`, kết nối và cấu hình (UPDATED 23/10/2023)
    - 2.7.2.1 - Sử dụng công cụ cơ bản (UPDATED 19/10/2023)
    - 2.7.2.2 - Thông tin về `finger print` tại máy khách và máy chủ (UPDATED 19/10/2023)
    - 2.7.2.3 - Hành vi xử lý chuẩn kết nối đến máy chủ (UPDATED 19/10/2023)
    - 2.7.2.4 - Cấu hình `ssh client` (UPDATED 21/10/2023)
    - 2.7.2.5 - Sử dụng `X11-Forwarding` và `Port-Forwarding` (UPDATED 23/10/2023)
- 2.8 - Tổng quan về quản lý mạng (:heavy_plus_sign:UPDATED 05/11/2023)
  - 2.8.1 - Mô hình `TCP/IP` (:heavy_plus_sign:UPDATED 25/10/2023)
  - 2.8.2 - Mô tả về `Network Interface` (:heavy_plus_sign:UPDATED 01/11/2023)
  - 2.8.3 - Địa chỉ `v4` (:heavy_plus_sign:UPDATED 25/10/2023)
  - 2.8.4 - Địa chỉ `v6` (:heavy_plus_sign:UPDATED 25/10/2023)
  - 2.8.5 - Thông tin về `network interface`(:heavy_plus_sign:UPDATED 25/10/2023)
  - 2.8.6 - Công cụ quản lý `nmcli`(:heavy_plus_sign:UPDATED 05/11/2023)
  - 2.8.7 - Cấu hình và quản lý `hostname`(:heavy_plus_sign:UPDATED 05/11/2023)