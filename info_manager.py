from modules import *

def add_golike_auth(filename="auth.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào auth golike của bạn\n-> "))

        if len(inp) < 10:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập auth hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu auth golike thành công!"))
        waiting_ui(4, "4s...")
        break

def add_golike_t(filename="t.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào t golike của bạn\n-> "))

        if len(inp) < 4:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập t hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu t golike thành công!"))
        waiting_ui(4, "4s...")
        break

def add_device(filename="device.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào tên device của bạn\n-> "))

        if len(inp) < 2:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập tên device hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu tên device thành công!"))
        waiting_ui(4, "4s...")
        break