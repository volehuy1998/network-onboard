[INE - 7. Các trường trong tiêu đề IPv4](#ine_7_ipv4_header_fields)

- [7.1 - Tổng quan thông tin tiêu đề IPv4](#ine_7_header_field_overview)
- [7.2 - Ví dụ tìm vị trí fragment](#ine_7_example_determine_fragment_offset)

# <a name="ine_7_header_field_overview"></a>7.1 - Tổng quan thông tin tiêu đề IPv4

Trong phần này chúng ta tập trung vào việc tìm hiểu sơ lược các trường trong cấu trúc/tiêu đề của IPv4 và mục đích sử dụng của chúng.

<div style="text-align:center"><img src="../images/ine_33_ip_packet_structure.svg" alt/></div>

Trong mô hình OSI, bất kể loại dữ liệu của nó là TCP hay UDP thì đều truyền xuống `Network Layer`. IPv4 sẽ nhận tất cả mọi thứ được truyền xuống và thêm một tiêu đề mang tính không trùng lặp vào phần đầu của dữ liệu, phần tiêu đề này đã biến toàn bộ thành cái mà chúng ta gọi là `IP Packet` (gói tin IP). Tiêu đề này chứa trường địa chỉ cũng như nhiều thứ khác để cho phép router định tuyến.

<div style="text-align:center"><img src="../images/ine_32_wireshark_packet_strcture.png" alt/></div>

- `Version`: mô tả gói tin phiên bản 4 hoặc 6. Một byte được tách đôi thành 4 bits được sử dụng cho hai chức năng riêng biệt.
- `Header Length`: nơi kết thúc của tiêu đề IP và là nơi bắt đầu cửa dữ liệu. Nó không thực sự có ý nghĩa đối với người đọc thay vào đó được ứng dụng trong lập trình, thiết bị thu. Mặc dù kích thước không phải là giá trị tĩnh nhưng hầu hết (ví dụ như trong ảnh wireshark) thì đều mang giá trị `20 bytes` (32 bits x 5) là ít nhất. Nếu trường `Option` có tồn tại thì giá trị sẽ lớn hơn.
- `Differentiated Services` hoặc `Type of Service (TOS)`: giá trị càng lớn thì gói có độ ưu tiên càng cao, ví dụ trong ảnh toàn bộ giá trị `0` mô tả gói tin có độ ưu tiên thấp nhất hoặc nếu là gói IP Phone thì độ ưu tiên luôn luôn cao. Giá trị này bị thay đổi bởi chức năng `Quality of Service`.
- `Total Length`: tổng kích thước của gói tin bao gồm IP header và IP Payload (data), như hình trên gói ICMP có kích thước 60 (bytes) với `IP Payload` là `Internet control Message Protocol` phía dưới cùng.
- `Identification`: định danh gói tin được sinh một cách ngẫu nhiên. Trường này không có ý nghĩa nhiều trừ khi điều tra phân mảnh gói tin.
- `Fragment Offset`: vị trí của fragment sau khi phân mảnh hỗ trợ tái tạo lại gói tin theo đúng thứ tự.
- `Time to live (TTL)`: mô tả vòng đời của gói tin. Chỉ có ý nghĩa và được kiểm soát bởi router, mỗi khi đi qua một router thì giá trị sẽ giảm đi một đơn vị cho đến khi nó bị hủy khi về 0. Ví dụ ảnh trên thì gói tin ICMP có thể đi qua 112 router. Giá trị này hữu ích khi chống lại rủi ro nằm trong vòng lặp vô tận.
- `Protocol`: tên giao thức, con số cạnh bên gắn liền với giao thức đó. Ví dụ ICMP (1), IGMP (2) và UDP (17), ...
- `Header checksum`: khi một gói tin được tạo ra thì thiết bị sẽ sử dụng tham số là tất cả các trường của IP Header để tính toán và cho ra kết quả này. Điều này để đảm bảo rằng nội dung gói tin không bị thay đổi và tất nhiên mỗi trường này sẽ được tính toán lại mỗi khi thay đổi TTL hoặc thứ gì đó liên quan đến quy trình chuyển mạch. Ví dụ nếu thiết bị nhận gói tin trực tiếp thì nó sẽ có cùng checksum với thiết bị gửi, nếu gói tin cần chuyển tiếp thì thiết bị nhận sẽ tính toán lại checksum trước khi gửi.
- `Source` và `Destination`: thiết bị gửi và thiết bị nhận.

<div style="text-align:center"><img src="../images/ine_34_fragmen_and_id_packet.png" alt/></div>

`Flags`: giả sử khi dữ liệu được truyền trong network và kích thước của nó rất lớn thì lúc này nó cần phải có điểm dừng, thuật ngữ gọi là `Maximum Transmission Unit (MTU)`. Hầu hết các mạng mà chúng ta đang kết nối đều có MTU mặc định là 1500 (bytes), số còn lại đều có giá trị của riêng mình để sao cho tối ưu hệ thống. Ví dụ khi đi đến một router có MTU=500 (bytes) thì nó thực hiện phân mảnh 1500 bytes thành 3 fragment, các mảnh nhỏ này đều mang giá trị định danh của gói tin ban đầu, đôi khi vì một số lý do phát lại gói tin cho nên việc đầu thu nhận được trùng lặp gói là điều không thể tránh khỏi vì thế thông tin trong `Flags` rất hữu ích để xử lý việc này. Nơi nhận sẽ đảm nhiệm tái tạo lại gói tin ban đầu dựa trên nhiều yếu tố.

- `Reserved bit`: tài liệu RFC791 mô tả tính năng này sẽ được sử dụng trong tương lai, hiện tại giá trị của nó luôn là 0.
- `Don't fragment`: giá trị 1 yêu cầu thiết bị kế tiếp không phân mảnh và hủy gói tin đó đi nếu lớn hơn MTU. Lợi ích của việc này là tránh sử dụng tài nguyên CPU để phân mảnh và tái tạo lại gói tin, tối ưu thông lượng cho những dịch vụ khác. Thông thường chức năng này được sử dụng để xác định thông số MTU card mạng thông qua công cụ ping.
- `More fragments`: nếu mảnh không phải cuối cùng thì giá trị bằng 0.

# <a name="ine_7_example_determine_fragment_offset"></a>7.2 - Ví dụ tìm vị trí fragment

<div style="text-align:center"><img src="../images/ine_35_example_about_fragment.png" alt/></div>

[Lấy ví dụ của trang cisco](https://www.cisco.com/c/en/us/support/docs/ip/generic-routing-encapsulation-gre/25885-pmtud-ipfrag.html): một gói tin IP có `IP header` cố định 20 bytes, `IP payload` là 5120 bytes. Trung chuyển qua thiết bị có MTU là 1500, tìm vị trí của các fragment?

1) Tổng số lượng fragment: (5120 / 1480) + 1 = 3.45 + 1 = 4
2) Vị trí fragment đầu luôn là 0
3) Vị trí fragment thứ hai: (1480 / 8) * 1 = 185 <b>(trường hợp lý tưởng)</b>
4) Vị trí fragment thứ ba: 185 * 2 = 370
5) Vị trí fragment cuối: 185 * 3 = 555
6) Kích thước fragment cuối cùng: 5120 % 1480 = 680 (chưa bao gồm header)

<div style="text-align:center"><img src="../images/ine_36_example2_about_fragment.png" alt/></div>

[Lấy ví dụ của trang wiki](https://en.wikipedia.org/wiki/IP_fragmentation#): một gói tin IP có `IP header` cố định 20 bytes, `IP payload` là 10000 bytes. Trung chuyển qua thiết bị có MTU là 4000, tìm vị trí của các fragment?

1) Tổng số lượng fragment: (10000 / 3980) + 1 = 3
2) Vị trí fragment đầu luôn là 0
3) Vị trí fragment thứ hai: (3980 / 8) * 1 = 497.5 <b>(số lẻ)</b> vì thế làm tròn 497
4) Tính toán lại kích thước `IP Payload` của các fragment đầu là 497 * 8 = 3976 bytes, fragment cuối có độ dài 10000 % 3976 = 2048
4) Vị trí fragment thứ ba: 497 * 2 = 994