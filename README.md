# Hướng dẫn cài đặt các phụ thuộc cần thiết
1. bạn cần cài đặt ```python``` với phiên bản ```3.11```
- [link tải python, hãy kéo xuống cùng trang bạn sẽ thấy các bản cài đặt](https://www.python.org/downloads/release/python-3110/)

2. bạn cần cài đặt ```android-studio```
- [link tải android-studio (bạn có thể tải thủ công nếu link lỗi)](https://drive.google.com/file/d/1eG1hifNHqvXMb4IPuJaVNGBeaPo--Dkl/view?usp=drive_link)

3. bạn cần cài đặt ```appium```
- [link cài đặt appium](https://github.com/appium/appium-desktop/releases/tag/v1.21.0)

- Link video hướng dẫn chi tiết setup appium và android studio [Link Video 1](https://youtu.be/oqaJvdIQ7JQ?si=Zc_kqeJcMMiULRZ8) [Link video 2](https://youtu.be/AExZRlVznQs?si=nLJexMYi4abqWKB4)

4. Bạn cần cài đặt ```Java```
- [link cài đặt java](https://download.oracle.com/java/23/archive/jdk-23.0.2_windows-x64_bin.exe)

5. bạn cần cài đặt ```tiktok like``` phiên bản phù hợp với tool ```(37.8.4)``` cho điện thoại
- [link tải tệp tiktok lite apk tương thích cho tool](https://drive.google.com/file/d/1a0riuIloZ2aWNNRnIkF75pvCOZ8mbs4d/view?usp=drive_link)

6. bạn cần cài đặt ```tesseract```
- [link tải tesseract](https://drive.google.com/file/d/1PUsrhBLqjYi2eubnH_H-e8erdGOF7ENL/view?usp=drive_link)

# Hướng dẫn setup các file quan trọng trong tool
1. file ```adb_path.txt```
- bạn có thể thêm vào đường dẫn của tệp ```adb.exe``` vào đây, hoặc nếu bạn đã thêm ```adb.exe``` vào biến môi trường thì chỉ cần để ```adb``` là được
2. file ```tesseract_path.txt```
- bạn có thể thêm đường dẫn của tệp ```tesseract.exe vào``` file này hoặc bạn có thể để ```tesseract``` nếu đã thiết lập biến môi trường

# Hướng dẫn phụ và các lưu ý nhỏ
1. Trong ứng dụng ```tiktok lite``` trên android của bạn nên cấp các quyền sau
- Quyền bộ nhớ
- Quyền danh bạ
- Quyền vị trí
2. Đảm bảo rằng ứng dụng ```tiktok lite``` của bạn trong quá trình hoạt động không có popup gì khác trong script, để đảm bảo tool chạy ổn định!
3. trên tài khoản ```tiktok``` của bạn, để đảm bảo tool chạy đúng hãy cập nhật ```tên hồ sơ``` (nếu chưa có) và đăng ít nhất ```một ảnh``` nếu chưa đăng ảnh nào.
4. hãy dùng app vpn ```1.1.1.1``` nếu bạn auto nhiều thiết bị cùng lúc (Hoặc không cũng được, dựa trên việc chạy thực tế, tool này hoạt động ít nhả follow khi không fake VPN)
5. Lưu Ý quan trọng!! Vì tool có auto post ảnh, nên bạn cần chuẩn bị 1 hoặc 2 ảnh trở lên trong thư viện ảnh, và hạn chế các ảnh cá nhân để tránh post ảnh không mong muốn.
6. Lưu ý quan trọng!! Bạn vui lòng vào ứng dụng google play để tải về ứng dụng bàn phím ```Gboard``` để đảm bảo tương thích với tool.
7. Lưu ý quan trọng!! Bạn vui lòng không thêm email hoặc số điện thoại vào tài khoản facebook để tránh 2fa phá hỏng luồng làm việc của tool
8. Lưu ý quan trọng!! Sau khi mọi thiết lập hoàn tất, bạn hãy tắt hoặc hạn chế google play đi, để tránh tự động cập nhật (dù đã bật không tự động cập nhật, nhưng đôi lúc nó khó hiểu lắm :> ..)

