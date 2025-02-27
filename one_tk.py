from golike import (
    get_job,
    GOLIKE_HEADERS,
    check_tiktok_account_id,
    drop_job,
    verify_complete_job
)
from tiktok_lite import (
    driver_init,
    follow,
    go_to_my_page
)
from info_manager import (
    add_golike_auth,
    add_golike_t,
    add_device
)
from delete_tiktok_lite_cache import (
    delete_cache
)
from login_tiktok import login_tiktok_lite

from modules import *
import time
import os
import sys

more_wait_when_error = 1
mh_mode = input(system_color("[?] Nhập loại màn hình (old/new)\n-> ")).lower().strip()

def choose_id():
    inp, r = None, None

    while True:
        r = check_tiktok_account_id()

        print()
        for i in range(len(r)):
            print(success_color(f"[{i}] {r[i][0]} -> {r[i][1]}"))
        print()

        inp = int(input(system_color("[?] Chọn id và account bạn muốn chạy theo index\n-> ")))

        if isinstance(inp, int):
            break

        else:
            print()
            print(error_color("[!] Vui lòng nhập đúng index!"))
    
    return r[inp]

def auto(driver, account_id, adb_path):
    global more_wait_when_error
    account_id = str(account_id)
    
    error = True
    rj = None

    for _ in range(20):
        rj = get_job(account_id)

        if "error" in rj:
            print(error_color("[!] Đã có lỗi khi nhận job, thử lại..."))
            time.sleep(1)
            error = True
        else:
            print(success_color("[#] Đã nhận job thành công."))
            error = False
            break
    
    if error:
        return "error"
    
    if rj[2] != "follow":
        print(error_color("[!] Không phải nhiệm vụ follow!"))

        r = drop_job(rj[1], rj[3], account_id, rj[2])
        if "error" in r:
            print(error_color("[!] Đã bỏ job thất bại."))
        else:
            print(success_color("[#] Đã bỏ job thành công!"))

        return "!=follow"


    if "error" in rj:
        print(error_color("[!] Đã có lỗi khi nhận job!"))
        
        r = drop_job(rj[1], rj[3], account_id, rj[2])
        if "error" in r:
            print(error_color("[!] Đã bỏ job thất bại."))
        else:
            print(success_color("[#] Đã bỏ job thành công!"))
        
        return "error"
    
    else:
        rf = follow(driver, adb_path, rj[0], capabilities['udid'])
        
        if "error" in rf:
            print(error_color("[!] Đã có lỗi khi follow!"))

            r = drop_job(rj[1], rj[3], account_id, rj[2])
            if "error" in r:
                print(error_color("[!] Đã bỏ job thất bại."))
            else:
                print(success_color("[#] Đã bỏ job thành công!"))

            return "error follow"
        
        elif "!=username" in rf:
            
            r = drop_job(rj[1], rj[3], account_id, rj[2])
            if "error" in r:
                print(error_color("[!] Đã bỏ job thất bại."))
            else:
                print(success_color("[#] Đã bỏ job thành công!"))

            return "diff username"
        
        else:
            rv = verify_complete_job(rj[1], account_id)

            if "error" in rv:
                print(error_color("[!] Đã có lỗi khi xác minh job."))

                r = drop_job(rj[1], rj[3], account_id, rj[2])
                if "error" in r:
                    print(error_color("[!] Đã bỏ job thất bại."))
                else:
                    print(success_color("[#] Đã bỏ job thành công!"))

                more_wait_when_error += 1
                
                # r = delete_cache(driver, adb_path)

                # if r == "error":
                #     return "delete cache error"
                # else:
                #     print(success_color("[#] đã xóa cache thành công."))
            
            else:
                print(success_color(f"[$] {rv[1]}"))
                print(success_color(f"[$] {rv[2]}"))
                from golike import prices
                print(success_color(f"[$] tổng của phiên chạy này -> {prices}đ"))
                
                # print(system_color("[#] thực hiện xóa cache..."))
                # r = delete_cache(driver, adb_path)
                # if r == "error":
                #     return "delete cache error"
                # else:
                #     print(success_color("[#] đã xóa cache thành công."))
                
                more_wait_when_error = 1


def run(adb_path):
    global more_wait_when_error
    id_gl = choose_id()
    os.system(adb_path + " devices")
    udid_inp = input(system_color("[?] Nhập vào udid máy của bạn\n-> "))
    capabilities['udid'] = udid_inp
    wait = int(input(system_color("[?] Nhập số thời gian chờ\n-> ")))
    appium_port = input(system_color('[?] Nhập port appium của bạn\n-> '))
    print()

    driver = driver_init(adb_path, False, capabilities['udid'], appium_port=appium_port)
    driver = waiting_scroll(driver, adb_path, 5, "Đợi 5 scroll để bắt đầu...", mh_mode=mh_mode, device_id=capabilities['udid'])

    while True:
        r = auto(driver, id_gl[0], adb_path)
        
        if r == "!=follow":
            driver = waiting_scroll(driver, adb_path, 1, f"Vui lòng đợi 1 scroll để nhận job tiếp theo...",  mh_mode=mh_mode, device_id=capabilities['udid'])
            continue

        elif r == "error follow":
            print(system_color("[!] Lỗi follow, Khởi tạo lại driver..."))
            try:
                driver.quit()
            except:
                pass
            driver = driver_init(adb_path, False, appium_port)

            # r = delete_cache(driver, adb_path)
            # if r == "error":
            #     print(error_color("[!] đã xóa cache không thành công, khởi tạo lại driver.."))
            #     driver = driver_init(adb_path, False, appium_port)
            # else:
            #     print(success_color("[#] đã xóa cache thành công."))

            more_wait_when_error += 1

        elif r == "delete cache error":
            try:
                driver.quit()
            except:
                pass
            print(system_color("[!] Lỗi khi xóa cache, Khởi tạo lại driver..."))
            driver = driver_init(adb_path, False, appium_port)
            continue
        
        elif r == "diff username":
            print(system_color("[!] Lỗi khác username, Khởi tạo lại driver..."))
            try:
                driver.quit()
            except:
                pass
            driver = driver_init(adb_path, False, appium_port)
            continue

        try:
            driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", mh_mode=mh_mode, device_id=capabilities['udid'])
        except:
            pass

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
        print(system_color("| [2] Chạy tool                               |"))
        print(system_color(" -------------------------------------------------"))
        print()

        inp = int(input("[?] Nhập lựa chọn của bạn\n-> "))

        if inp == 0:
            add_golike_auth()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")

        elif inp == 1:
            add_golike_t()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")

        elif inp == 2:
            adb_path = open("adb_path.txt", "r").read()
            GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
            GOLIKE_HEADERS["t"] = open("t.txt", "r").read()

            print(error_color("[!] Bạn có thể Ctrl+C để thoát khi tool đang chạy"))
            print()
            
            try:
                run(adb_path)
            except KeyboardInterrupt:
                waiting_ui(4, "Bạn đã chọn thoát chương trình 4s")
                os.system("cls") if sys.platform.startswith("win") else os.system("clear")
                continue