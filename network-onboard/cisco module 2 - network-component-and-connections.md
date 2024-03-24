[Cisco Module 2 - Các thành phần trong mạng, loại của chúng và các kết nối](#module2_intro)

- [2.0 - Vai trò máy khách và máy chủ (UPDATED 21/08/2023)](#server_client_role)
    - [2.0.1 - Giới thiệu](#server_client_intro)
    - [2.0.2 - Mạng P2P](#p2p_network)
    - [2.0.3 - Ứng dụng P2P](#p2p_app)
    - [2.0.4 - Các vai trò trong mạng](#multi_role)
- [2.1 - Các thành phần trong mạng (UPDATED 21/08/2023)](#network_component)
    - [2.1.1 - Hạ tầng mạng (UPDATED 21/08/2023)](#network_infra)
    - [2.1.2 - Thiết bị cuối (UPDATED 21/08/2023)](#end_dev)
- [2.2 - ISP (UPDATED 21/08/2023)](#isp)
    - [2.2.1 - Dịch vụ ISP (UPDATED 21/08/2023)](#isp_service)
    - [2.2.2 - Kết nối ISP (UPDATED 21/08/2023)](#isp_connection)
    - [2.2.3 - Cáp và kết nối DSL (UPDATED 21/08/2023)](#capble_dsl_connection)
    - [2.2.3 - Kết nối bổ sung (UPDATED 21/08/2023)](#add_connection)

# <a name="module2_intro"></a>Các thành phần trong mạng, loại của chúng và các kết nối

## <a name="server_client_role"></a>Vai trò máy khách và máy chủ

### <a name="server_client_intro"></a>Giới thiệu

Tất cả máy tính được kết nối trong mạng sẽ tham gia trực tiếp vào việc giao tiếp mạng, chúng được gọi là `host`. Các `host` đều có thể gửi và nhận thông tin trên mạng. Trong các mô hình mạng hiện nay thì `host` có thể là máy khách hoặc máy chủ hoặc đảm nhiệm cả hai. Dựa vào phần mềm được cài đặt trên `host` chúng ta có thể phân biệt nó là máy chủ hay máy khách.

Máy chủ là `host` mà có phần mềm được cài đặt để kích hoạt cung cấp thông tin (thư điện tử, nội dung web) tới một `host` khác trong mạng. Mỗi dịch vụ đều yêu cầu phần mềm máy chủ riêng. Ví dụ một máy chủ web yêu cầu cài đặt phần mềm dịch vụ web như apache, nginx, IIS (Windows). Mỗi một trang web trực tuyến mà bạn truy cập đều được cung cấp bởi máy chủ được đặt ở đâu đó trong mạng có kết nối Internet.

Máy khác là `host` cài đặt phần mềm để yêu cầu và hiển thị thông tin từ máy chủ. Ví dụ như phần mềm máy khách là trình duyệt như Internet Explorer, Safari, Chrome, Firefox, ... 

### <a name="p2p_network"></a>Mạng P2P

Phần mềm máy khách và máy chủ thường chạy tách biệt ở mức `host`, nhưng nó cũng có thể được cài đặt và chạy chung `host` một cách đồng thời. Loại mạng này được gọi là `peer-to-peer (P2P)`.

Mạng P2P đơn giản nhất sẽ chỉ bao gồm 2 máy tính kết nối trực tiếp với nhau có dây hoặc không dây. Nhiều máy tính cá nhân (PCs) đều có thể kết nối với nhau để tạo ra mạng P2P lớn nhưng có thể sẽ yêu cầu thiết bị chuyển mạch như switch để kết nối các máy tính.

Vấn đề lớn nhất của môi trường P2P là hiệu suất của một `host` có thể bị chậm lại nếu nó hoạt động trên cả hai nhiệm vụ khách và chủ cùng một thời điểm. Đối với doanh nghiệp lớn, bởi vì sẽ có lúc xảy ra tình huống lưu lượng mạng bị dâng cao nên thường sẽ triển khai máy chủ chuyên dụng để hỗ trợ các yêu cầu chuyển tới.

Ưu điểm của P2P:

- Dễ dàng thiết lặp.
- Chi phí thấp bởi vì các thiết bị chuyển mạch hoặc máy chủ chuyên dụng có thể sẽ không bị yêu cầu.

Nhược điểm:

- Không quản trị tập trung.
- Kém bảo mật.
- Không thể mở rộng.
- Hiệu suất khả năng cao sẽ thấp bởi vì một PC mang cả 2 vai trò máy khách lẫn máy chủ.

<div style="text-align:center"><img src="../images/p2p_network
.png" alt/></div>

### <a name="p2p_app"></a>Ứng dụng P2P

Ứng dụng P2P cho phép một thiết bị tương tác như thể nó vừa là máy khách vừa là máy chủ. Ứng dụng P2P được cài đặt trên PC sẽ có giao diện vai trò máy khách lẫn dịch vụ chạy nền. Một số ứng dụng P2P chạy ở dạng lai với mô hình Client-Server, tức là nó vẫn theo nguyên tắc không tập trung tài nguyên tại một PC nào đó nhưng vẫn có chỉ mục được lưu trữ tập trung - mỗi khi cần PC sẽ truy cập vào chỉ mục đó để lấy ra vị trí tài nguyên được lưu trữ ở PC khác.

<div style="text-align:center"><img src="../images/p2p_app
.png" alt/></div>

### <a name="multi_role"></a>Các vai trò trong mạng

Một máy tính có thể chạy nhiều phần mềm máy chủ. Trường hợp ở các doanh nghiệp nhỏ để tiết kiệm chi phí thì thường sẽ tích hợp nhiều dịch vụ khác nhau trên cùng một máy chủ như: File Server, Web Server, Mail Server, ...

Trường hợp phổ biến, một máy tính có thể chạy nhiều phần mềm máy khách. Với nhiều phần mềm được cài đặt như vậy thì máy tính này có thể kết nối nhiều máy chủ cùng lúc. Ví dụ bạn có thể đọc mail song song với việc lướt web trong khi đang nhắn tin, nghe nhạc trực tuyến.

<div style="text-align:center"><img src="../images/multi_role_in_host
.png" alt/></div>

## <a name="network_component"></a>Các thành phần trong mạng

### <a name="network_infra"></a>Hạ tầng mạng

Con đường để thông tin lấy từ nguồn đến nơi nhận có thể kết nối đơn giản bằng một sợi cáp giữa máy tính với bên còn lại. Hạ tầng mạng là nền tảng để hiểu về mạng máy tính. Nó cung cấp sự ổn định và quy tắc chặt chẽ đáng tin cậy để sự thông liên lạc của chúng ta diễn ra mượt mà.

<div style="text-align:center"><img src="../images/network_infra_categories.png" alt/></div>

Hạ tầng mạng chứa 3 loại thành phần phần cứng:

- `End device`: thiết bị cuối.
- `Intermediate device`: thiết bị trung gian.
- `Network media`: phương tiện truyền dẫn, môi trường truyền dẫn.

Các thiết bị và phương tiện đều là các yếu tố vật lý trong mạng. Phần cứng thường là các thành phần có thể thấy được như máy tính xách tay, PC, switch, router hoặc cáp mạng để kết nối. Thi thoảng sẽ có một số thành phần không nhìn thấy được như môi trường truyền dẫn không dây, các thông tin được truyền tải thông qua không khí sử dụng tần số vô tuyến hoặc sóng hồng ngoại.

### <a name="end_dev"></a>Thiết bị cuối

Các thiết bị mạng mà người dùng quen thuộc được gọi là `device` hoặc `host`. Những thiết bị này cung cấp giao diện tương tác giữa người dùng và mạng. Một số ví dụ về thiết bị cuối như sau:

- Máy trạm, máy tính xách tay, máy chủ web.
- Máy in.
- Điện thoại bàn.
- Camera.
- Thiết bị di động như điện thoại thông minh, máy tính bảng, thẻ tín dụng.

Thiết bị cuối có thể là nơi phát sinh hoặc nhận thông tin trong mạng. Sử dụng địa chỉ để nhận dạng các thiết bị. Khi một `host` khởi tạo một kênh liên lạc, nó cần có địa chỉ của `host` nhận để chỉ định cho thông tin biết nó cần gửi tới đâu.

## <a name="isp"></a>ISP

### <a name="isp_service"></a>Dịch vụ ISP

Nhà cung cấp dịch vụ Internet - Internet Service Provider cung cấp một kết nối giữa mạng nhà và internet. Rất nhiều ISP còn cung cấp thêm một số dịch vụ khác như email, web, backup, bảo mật. ISP rất quan trọng trong việc làm cầu nối liên lạc đến internet toàn cầu. Mỗi ISP sẽ liên kết với các ISP khác để tạo thành một mạng lưới kết nối người dùng toàn cầu. Để đảm bảo lưu lượng được di chuyển trên con đường ngắn nhất từ nguồn đến nơi nhận thì ISP được kết nối với nhau theo mô hình phân cấp.

<div style="text-align:center"><img src="../images/isp_services.png" alt/></div>

Trục internet giống một xa lộ thông tin khổng lộ cung cấp các liên kết dữ liệu tốc độ cao để kết giữa các mạng lưới ISP khác nhau. Phương tiện chính của trục internet là cáp quang. Cáp này thường được lắp đặt dưới lòng đất để kết nối các thành phố, quốc gia và châu lục.

### <a name="isp_connection"></a>Kết nối ISP

Sự kết nối của các ISP khác nhau tạo thành xương sống của internet là một mạng lưới cáp quang vô cùng phức tạo với các thiết bị chuyển mạch/định tuyến đắt tiền để kiểm soát luồng thông giữa các máy chủ. Thường thì người dùng cá nhân sẽ không quan tấm đến cơ sở hạ tầng bên ngoài. Đối với các hộ gia đình thì việc kết nối với ISP là một quá trình đơn giản.

Phần trên cùng của hình hiển thị kết nối ISP đơn giản nhất. Chỉ bao gồm `modem` kết nối trực tiếp giữa máy tính và ISP. Tuy nhiên tùy chọn này không nên được sử dụng vì máy tính không được bảo vệ trên internet. Phần phía dưới hành có `router` (bộ định tuyến) để kết nối máy tính với ISP một cách an toàn. Đây là tùy chọn kết nối phổ biến nhất. `router` bao gồm `switch` để kết nối các `host` có dây trong hộ gia đình và được tích hợp `Access Point` hỗ trợ cho các `host` có nhu cầu kết nối không dây.

<div style="text-align:center"><img src="../images/isp_connection.png" alt/></div>

### <a name="capble_dsl_connection"></a>Cáp và kết nối DSL

<div style="text-align:center"><img src="../images/cable_dsl_fiber.png" alt/></div>

Hầu hết mạng trong hộ gia định không kết nối tới ISP bằng cáp quang. Hai phương pháp phổ biến nhất là:

- `Cable`: tín hiệu dữ liệu internet được truyền trên cùng một cáp đồng trục của nhà cung cấp truyền hình cáp. Có một số loại đặc biệt hơn vì nó tách tín hiệu dữ liệu internet khỏi các tín hiệu khác.
- `DSL - Digital Subscriber Line`: yêu cầu một `modem` để tách tín hiệu DSL khỏi tín hiệu điện thoại và cung cấp kết nối Ethernet tới các `host`. Tuy DSL chạy trên đường dây điện thoại nhưng không bắt buộc người dùng phải có dịch vụ thoại để có DSL. Đường dây này được chia thành 3 kênh, đặc điểm này tạo nên cái gọi là `"always on"` - sự đột phá so với `Dial-up Telephone`. Một kênh được sử dụng cho gọi thoại, kênh này cho phép cá nhân nhận các cuộc gọi mà không cần ngắt kết nối internet. Kênh thứ hai được sử dụng để nhận thông tin từ internet. Kênh cuối được sử dụng để tải thông tin lên hoặc tải xuống. Chất lượng và tốc độ kết nối DSL phụ thuộc chủ yếu vào chất lượng đường dây điện thoại và khoảng cách địa lý. Tốc độ của DSL thấp hơn cáp đồng trục nhưng bù lại bảo mật hơn, quan trọng hơn hết là giá thành rẻ nên DSL phổ biến nhất thế giới. 

<div style="text-align:center"><img src="../images/connection_types.png" alt/></div>

### <a name="add_connection"></a>Kết nối bổ sung

Một số tùy chọn kết nối ISP khác dành cho hộ gia đình như:

- `Dial-up Telephone`: công nghệ cũ được sử dụng phổ biến vào những năm 1990. Để kết nối đến ISP bạn cần gọi đến ISP. Tốc độ rất chậm chỉ tầm 56(Kbps) và thậm chí chúng sử dụng chung kênh truyền thoại và internet, hậu quả là bạn không thể đồng thời sử dụng điện thoại và internet. Cho tới ngày nay vẫn còn một số người sử dụng loại hình này.
- `Cellular`: sử dụng mạng di động để kết nối. Bất cứ nơi nào bạn có thể nhận được tín hiệu di động thì đều có thể truy cập internet. Hiệu suất phụ thuộc vào điện thoại và tháp phát tín hiệu mà nó kết nối. Lợi ích của dịch vụ này dành cho những khu vực không thể kéo mạng đến được hoặc thường xuyên di chuyển. Nhược điểm là nhà mạng đo mức sử dụng để tính phí.
- `Satellite`: một tùy chọn tốt thay thế cho DSL hoặc cáp đồng trục. Yêu cầu môi trường ít bị cản trở bởi cây cối hoặc những nơi có vật cản trên cao. Chi phí lắp đặt khá cao nhưng giống như kết nối `cellular` nó mang lại lợi ích đặc biệt của truy cập không dây.

<div style="text-align:center"><img src="../images/satellite_connection.png" alt/></div>

Ở các khu vực đô thị, nhiều căn hộ và văn phòng được kết nối trực tiếp bằng cáp quang. Điều này cho phép ISP cung cấp tốc độ cao hơn, hỗ trợ dịch vụ tốt hơn và cung cấp nhiều dịch vụ hơn. Việc lựa chọn kết nối tùy thuộc vào vị trí địa lý và tính khả dụng của nhà cung cấp dịch vụ.