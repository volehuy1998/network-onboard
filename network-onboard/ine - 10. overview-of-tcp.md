[INE - 10. Tổng quan TCP ( :heavy_plus_sign: UPDATED 22/07/2024)](#ine_10_overview_tcp)
- [10.1 - Giới thiệu TCP ( :heavy_plus_sign: UPDATED 22/07/2024)](#ine_10_intro_tcp)
- [10.2 - Khái niệm giao thức hướng kết nối ( :heavy_plus_sign: UPDATED 22/07/2024)](#ine_10_connection_oriented)
- [10.3 - Tổng quan về cờ PSH và URG](#ine_10_psh_n_urg)
- [10.4 - Tổng quan về Window Size vs Maximum Segment Size (MSS)](#ine_10_window_size_n_mss)
- [10.5 - Tổng quan bắt tay 3 bước](#ine_10_tcp_handshake)
- [10.6 - Tổng quan cơ chế truyền lại](#ine_10_tcp_retransmission)

# <a name="ine_10_intro_tcp"></a>10.1 - Giới thiệu TCP

Vào những thập niên 1970, với tư cách là trợ lý giáo sư tại Đại học Standford ở Vương Quốc Anh, [Vint Cerf](https://engineering.stanford.edu/about/heroes/2011-heroes/vint-cerf) cộng tác với các sinh viên ưu tú nhất của mình và kỹ sư người Mỹ tên [Robert Kahn](https://www.internethalloffame.org/inductee/robert-kahn/) (hay Bob Kahn) trực thuộc Cơ quan Dự án Nghiên cứu Nâng cao (DARPA) của Bộ Quốc phòng Hoa Kỳ cùng nhau tạo ra một chương trình có thể kiểm soát đường truyền Internet hay còn gọi là `Internet Transmission Control Program (TCP)`, đây là cách để xác định làm thế nào gói tin di chuyển trong Internet mà ngày nay trong trường học gọi là Bộ giao thức Internet. Trong những phiên bản đầu tiên của công nghệ này nó không hề có tên gọi hiện đại như ngày nay `Transmission Control Protocol` và được ghi lại ở tài liệu số [RFC 675](https://datatracker.ietf.org/doc/html/rfc675). Về mặt lịch sử `Transmission Control Protocol` hiện đại và `Internet Protocol` là đều có chung một nguồn gốc hay một phần trong tiêu chuẩn TCP, vào thời điểm đó các nhà khoa học không cố gắng phân biệt hay tách biệt chúng ra khỏi nhau. Ít lâu sau một thành phần trong chương trình này đã được tách ra và đặt tên là `Transmission Control Protocol` được định nghĩa ở tài liệu [RFC 793](https://datatracker.ietf.org/doc/html/rfc793), cái mà trường đại học phổ cập cho chúng ta ngày nay.

<div style="text-align:center"><img src="../images/ine_44_internet_protocol_suite.png" alt/></div>

Kể từ giờ trở đi khi nhắc đến `TCP` chúng ta không cần nhớ đến `Internet Transmission Control Program` nữa mà thay vào đó là tập trung vào `Transmission Control Protocol`. Trong `TCP/IP` sẽ có hai phần chính, `Transmission Control Protocol` là thành phần thu thập và tập hợp các gói dữ liệu thì `Internet Protocol` chịu trách nhiệm mô tả đích đến của gói tin. Vậy thì TCP và UDP có một số đặc điểm nào có thể phân biệt được? Gói tin UDP có thể bị rớt, nó không có cơ chế thông báo và phát lại gói tin. Ví dụ trường hợp rớt gói: định tuyến quá phức tạp, gói vô tình bị hủy bởi tường lửa, gói bị loại bỏ do tắc nghẽn ở gateway của router hoặc thiết bị cuối. Thêm vào đó nếu kích thước gói quá lớn thì sẽ cần phân mảnh, điều này càng làm tăng xác suất gói tin nguyên ban đầu không thể được nhận bởi đích đến. Ngược lại, TCP cung cấp cơ chế để đảm bảo người nhận thực sự nhận được gói tin nên có độ tin cậy cao hơn.

# <a name="ine_10_connection_oriented"></a>10.2 - Khai niệm giao thức hướng kết nối

Giao thức hưởng két nối có nghĩa là gì?
- Đầu tiên TCP xác minh sự tồn tại đích đến bạn muốn kết nối để trao đổi dữ liệu.
- Thực hiện đàm phán một số các tiêu chí để kiểm soát luồng dữ liệu trong lúc trao đổi.
- TCP là giao thức đáng tin cậy vì nó bảo đảm không mất gói tin nhờ vào cách thức đánh số thứ tự và xác minh đối tác đã nhận được gói (ack), nếu đối tác không nhận được sẽ truyền lại.
- TCP có phương pháp ngắt kết nối rất lịch sự, bài bản và dễ hiểu. Đối tác sẽ không bị bối rối trong tình huống họ nên chấm dứt kết nối hay nên tiếp tục chờ để nhận thêm gói tin.

<div style="text-align:center"><img src="../images/ine_45_tcp_header.png" alt/></div>

Chú thích:
- 2 trường port đầu tiên như đã giải thích ở bài trước.
- `Sequence number`: đánh số ngẫu nhiên 32 bit vào gói tin để đảm bảo dữ liệu được phân phối theo đúng thứ tự, thông báo mất mát và tránh trùng lặp. Gói kế tiếp bằng số ban đầu `+1`.
- `Acknownledgement number`: ví dụ đầu phát gửi gói tin đầu tiên có kích thước dữ liệu 200 bytes, gói tin phản hồi có giá trị ack là 201.
- `Data Offset` hay `Header length`: kích thước của gói TCP header.
- `Reserved`: dự phòng sử dụng cho tương lai.
- `Flags`: gồm 6 bit mỗi bit dùng để mô tả tính chất gói tin. Ví dụ đây là gói phản hồi ACK từ đầu nhận hay là gói của đầu phát, hoặc gói mang tín hiệu ngắt hoàn tất FIN (finish) để ngắt kết nối phiên TCP.
- `Window size`: đây là trường dùng để kiểm soát tải của luồng thông tin. Trước hết chúng ta phải biết quy tắc TCP không hoạt động theo cách đầu phát gửi 1 TCP segment thì đầu thu ack 1 TCP segment, mà TCP sẽ hoạt động theo cách đầu phát sẽ gửi nhiều TCP segment cùng lúc đến đầu thu. Chúng ta cũng có thể hiểu theo cách khác, nếu gửi 1 segment và ack 1 segment thì thời gian tiêu hao rất lớn và rồi sau đó `Window Size` được sinh ra để cải thiện hiệu suất. Ví dụ ban đầu chúng ta chỉ sử dụng ứng dụng Youtube và máy chủ Youtube sẽ gửi luồng dữ liệu đến thiết bị của chúng ta một cách đều đặn theo theo gian nhưng không lâu sau chúng ta sử dụng thêm các ứng dụng khác tương tự như iQiyi hoặc Netflix hoặc thậm chí đọc mail, tất cả dữ liệu sẽ đổ dồn về thiết bị chúng ta như một con lũ và khiến cho nó trì trệ do xử lý lượng tải quá cao. Hãy quay lại thời gian trước khi máy chủ Youtube đẩy luồng dữ liệu, thiết bị sẽ đàm phán với máy chủ Youtube về `window size` giả sư như 15 trước khi phiên TCP bắt đầu. Sau đó 15 TCP segment gửi về máy chúng ta cùng lúc như đã thỏa thuận nhưng một thời gian sau chúng ta mở song song thêm Netflix như kịch bản sắp đặt, lúc này thiết bị sẽ nói với máy chủ Youtube rằng nó đang quá tải hãy thu nhỏ `window size` xuống 5 hoặc 6 chẳng hạn và rồi một lúc nào đó thiết bị chúng ta nhàn rỗi thì nó có thể đàm phán tăng `window size` lên giả sử như 20.
- `TCP checksum`: dữ liệu được băm để bảo đảm không có sự thay đổi, nếu đầu thu băm ra kết quả khác với checksum thì có thể kết luận dữ liệu đã bị can thiệp và hủy gói tin.
- `Urgent pointer`: mô tả gói tin cần được ưu tiên xử lý. Giả sử chúng ta đang gõ chữ trên bàn phím rồi đột nhiên có vấn đề xuất hiện và chúng ta nhanh tay nhấn tổ hợp `Ctrl C` hoặc đại loại gì đó tương tự, tín hiệu đó sẽ gửi đến máy tính để ngắt tiến trình ngay lập tức nếu không xử lý thì các vấn đề lớn sẽ ùn ùn kéo theo sau ngay lập tức.

# <a name="ine_10_psh_n_urg"></a>10.3 - Tổng quan về cờ PSH và URG

<div style="text-align:center"><img src="../images/ine_46_tcp_psh_flag.png" alt/></div>

Lấy ví dụ khi chúng ta gõ phím trên ứng notepad của máy tính thì ký tự sẽ xuất hiện gần như là ngay lập tức nhưng khi gõ phím trên cửa sổ ứng dụng ssh (mobaxterm, putty) hoặc telnet thì ký tự sẽ xuất hiện chậm hơn. Để giả lập được trường hợp chậm hơn này có lẻ cần môi trường thực tế, trong công ty cloud mà tôi đang làm có lần gặp trường hợp máy chủ Compute (chứa VM) gặp trục trặc, trong đây chứa vài VM dịch vụ AI chiếm quá nhiều tài nguyên CPU dẫn đến giá trị biểu đồ của [CPU Steal Time](#https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-kvm_guest_timing_management-steal_time_accounting) cao lên ngất ngưỡng tính bằng 70-80% (bình thường luôn <0.5%) dẫn đến việc gõ phím trong ssh của những VM khác cũng vô cùng chậm chạp, đối với người lần đầu tiên gặp sẽ nghĩ là do mạng có vấn đề nhưng thực ra là do CPU không còn thời gian xử lý cho các VM khác. Như vậy cụ thể là việc này liên quan như thế nào đến việc gõ phím trên notepad và ssh? Bởi vì khi chúng ta gõ một phím trong ssh thì nó sẽ gửi TCP segment đến ssh server và trả ngược về ssh client, kết thúc hành trình này thì ký tự mới hiện diện trên màn hình ssh. Cờ `PSH` chỉ thị cho máy tính không cần phải đưa vào bộ đệm đến khi đủ `MSS (Maximum Segment Size)` như cách mà chúng ta gõ phím trên notepad, chờ nó tích lũy để đẩy đi mà hãy đẩy đi ngay lập tức. Như vậy chỉ khi kết nối TCP được thiết lập thì cờ `PSH` này mới hữu dụng.

(Ảnh 1: trước khi thiết lập kết nối TCP, gói tin vẫn chưa cài đặt cờ PSH.)

<div style="text-align:center"><img src="../images/ine_47_psh_flag_before_establish_tcp_connection.png" alt/></div>

(Ảnh 2: sau khi lập kết nối TCP, gói tin đã cài đặt cờ PSH.)

<div style="text-align:center"><img src="../images/ine_48_psh_flag_after_establish_tcp_connection.png" alt/></div>

(Ảnh 3: ví dụ gõ ký tự trên bàn phím, mỗi một phím được nhấn sẽ bắt được 3 gói tin Client, Server và ACK.)

<div style="text-align:center"><img src="../images/ine_49_psh_flag_after_establish_tcp_connection_ex2.png" alt/></div>

# <a name="ine_10_window_size_n_mss"></a>10.4 - Tổng quan về Window Size vs Maximum Segment Size (MSS)

Như phần trên đã đề cập, `Window Size` mô tả bao gồm nhiều TCP Segment có tổng số lượng byte phản ánh năng lực hiện tại có thể đảm nhận và `MSS` là kích thước cho mỗi TCP Segment. Ví dụ laptop mở vào trình duyệt và yêu cầu truy cập https://facebook.com (hiển nhiên chúng ta đều hiểu HTTP đều có nền là TCP), chúng ta có ví dụ sau:
- Khả năng của laptop có thể nhận được 5000 (bytes), nó gửi thông tin này đến máy chủ để thông báo khả năng chịu tải ở thời điểm hiện tại. Hình dưới mô tả đợt trao đổi dữ liệu thứ 2, laptop trống nhiều tài nguyên và thông báo đến máy chủ cập nhật mức độ chịu tải của nó lên 6000 (bytes).
- `MSS` chính là MTU, giả sử trong trường lý tưởng của máy chủ và laptop đều là 1000 (bytes).

<div style="text-align:center"><img src="../images/ine_50_tcp_window_size_n_mss.png" alt/></div>

Kích thước của `Window Size` là 16 bit tương đương giá trị lớn nhất có thể đạt được là 65535 (bytes) nhưng với thời buổi hiện nay năng lực phần cứng đã được hoàn thiện chúng ta có thể thấy được giá trị lớn hơn 65535 bằng cách cài đặt phép nhân giữa 2 giá trị.

<div style="text-align:center"><img src="../images/ine_51_window_size_larger_65535.png" alt/></div>

# <a name="ine_10_tcp_handshake"></a>10.5 - Tổng quan bắt tay 3 bước

# <a name="ine_10_tcp_retransmission"></a>10.6 - Tổng quan cơ chế truyền lại