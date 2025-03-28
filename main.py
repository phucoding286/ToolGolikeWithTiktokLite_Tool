import one_tk
from modules import *
import multi_devices

if __name__ == "__main__":
    while True:
        print(system_color(" -------------------------------------------------"))
        print(system_color("| Tool Golike Tiktok By PhuTech (Programing-Sama) |"))
        print(system_color("|     Công cụ được xây dựng dựa trên APPIUM       |"))
        print(system_color(" -------------------------------------------------"))
        print(system_color("| # Các nguồn tài nguyên phụ thuộc                |"))
        print(system_color("|  $ Android Studio                               |"))
        print(system_color("|  $ appium-python-client (python package)        |"))
        print(system_color("|  $ appium (app)                                 |"))
        print(system_color(" -------------------------------------------------"))
        print(system_color("| ? Các lựa chọn theo index                       |"))
        print(system_color("| [0] Thêm golike authorization                   |"))
        print(system_color("| [1] Thêm golike t                               |"))
        print(system_color("| [2] Chạy tool với 1 device và 1 TK              |"))
        print(system_color("| [3] Chạy tool song song TK và Devices           |"))
        print(system_color(" -------------------------------------------------"))
        print()

        inp = int(input("[?] Nhập lựa chọn của bạn\n-> "))

        if inp == 0:
            multi_devices.add_golike_auth()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")

        elif inp == 1:
            multi_devices.add_golike_t()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")

        elif inp == 2:
            adb_path = open("adb_path.txt", "r").read()
            multi_devices.GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
            multi_devices.GOLIKE_HEADERS["t"] = open("t.txt", "r").read()

            print(error_color("[!] Bạn có thể Ctrl+C để thoát khi tool đang chạy"))
            print()
            
            try:
                one_tk.run(adb_path)
            except KeyboardInterrupt:
                waiting_ui(4, "Bạn đã chọn thoát chương trình 4s")
                os.system("cls") if sys.platform.startswith("win") else os.system("clear")
                continue
        
        elif inp == 3:
            adb_path = open("adb_path.txt", "r").read()
            multi_devices.GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
            multi_devices.GOLIKE_HEADERS["t"] = open("t.txt", "r").read()

            print(error_color(f"[!] Bạn có thể Ctrl+C để thoát khi tool đang chạy"))
            print()

            appium_port = input(system_color('[?] Nhập port appium của bạn\n-> '))
            devices = multi_devices.get_devices(adb_path)
            wait = int(input(system_color(f"[?] Nhập số thời gian chờ\n-> ")))
            times_scroll = int(input(system_color(f"[?] Nhập số scroll video user\n-> ")))
            wait_device_setup = int(input(system_color("[?] Nhận vào số thời gian chờ mỗi thiết bị setup xong\n-> ")))
            ask = input(system_color("[?] Bạn có muốn thêm mã device tách biệt?\n(y/N)-> "))
            
            out_device_list = []
            if ask.lower().strip() == "y":

                max_len = max([len(str(device)) for device in devices])
                print(success_color(" " + "-" * (max_len + 2)))
                for device in devices:
                    print(success_color("| " + device + (" " * (max_len - len(str(device)))) + " |"))
                print(success_color(" " + "-" * (max_len + 2)))
                
                print(error_color("[!] Bạn có thể gõ 'exit' để thoát."))
                while True:

                    if str(out_device_list) != "[]":
                        print(error_color("[!] Danh sách device tách biệt hiện tại bên dưới"))
                        max_len = max([len(str(device)) for device in out_device_list])
                        print(success_color(" " + "-" * (max_len + 2)))
                        for device in out_device_list:
                            print(success_color("| " + device + (" " * (max_len - len(str(device)))) + " |"))
                        print(success_color(" " + "-" * (max_len + 2)))
                    else:
                        print(error_color("[!] Danh sách device tách biệt hiện tại rỗng"))
                    
                    device_inp = input(system_color("[?] Nhập mã device mà bạn muốn tool tách biệt nó\n-> "))
                    if device_inp.strip().lower() == "exit":
                        break
                    else:
                        out_device_list.append(device_inp)
                        continue
            
            print()
            for device in devices:
                if device in out_device_list:
                    continue
                try:
                    thread = threading.Thread(
                        target=multi_devices.run, args=[adb_path, device, wait, appium_port, times_scroll],
                        daemon=True
                    )
                    thread.start()
                    waiting_ui(wait_device_setup, f"Đợi {wait_device_setup}s để chạy tất cả\n", device)
                    continue
                except KeyboardInterrupt:
                    waiting_ui(4, "Bạn đã chọn thoát chương trình 4s")
                    os.system("cls") if sys.platform.startswith("win") else os.system("clear")
                    break

            input(success_color("[#] Đã chạy xong tất cả thiết bị\n"))