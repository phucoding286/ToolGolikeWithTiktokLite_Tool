# Hướng dẫn cài đặt các phụ thuộc cần thiết
1. bạn cần cài đặt ```python``` với phiên bản ```3.11```
- [link tải python, hãy kéo xuống cùng trang bạn sẽ thấy các bản cài đặt](https://www.python.org/downloads/release/python-3110/)

2. bạn cần cài đặt ```android-studio```
- [link tải android-studio (bạn có thể tải thủ công nếu link lỗi)](https://developer.android.com/studio?gad_source=1&gclid=CjwKCAiA5Ka9BhB5EiwA1ZVtvG3pfLygEY-iGi0KHeQFqXem0MrQMpZ5JksOcjQt8eDMFLx8SwDjbBoC7oAQAvD_BwE&gclsrc=aw.ds)

3. bạn cần cài đặt ```appium```
- [link cài đặt appium](https://github.com/appium/appium-desktop/releases/tag/v1.22.3-4)

# Link video hướng dẫn chi tiết setup appium và android studio
[Link Video](https://youtu.be/oqaJvdIQ7JQ?si=Zc_kqeJcMMiULRZ8)

4. bạn cần cài đặt ```tiktok lik```e phiên bản phù hợp với tool ```(37.8.4)``` cho điện thoại
- [link tải tệp tiktok lite apk tương thích cho tool](https://apkpure.com/vn/tiktok-lite-2024/com.zhiliaoapp.musically.go/downloading)

5. bạn cần cài đặt ```tesseract```
- [link đến trang web tải tesseract](https://sourceforge.net/projects/tesseract-ocr.mirror/)

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
