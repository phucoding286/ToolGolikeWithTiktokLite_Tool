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
from get_device_id import get_devices
from upload_image import upload_image
from tuongtaccheo import ttc
from follow_via_open_link import follow_via_link
from change_profile_img import change_img_profile

from modules import *
import time
import os
import sys

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

def auto(driver, account_id, adb_path, time_scroll, device_id):
    account_id = str(account_id)
    error = True
    rj = None

    for _ in range(20):
        rj = get_job(account_id, device_id)

        if "error" in rj:
            print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi nhận job, thử lại..."))
            time.sleep(1)
            error = True
            continue

        elif isinstance(rj, tuple):
            print(success_color(f"[Device: {device_id}] [#] Đã nhận job thành công."))
            error = False
            break

        else:
            print(f"Trường hợp không xác định khi nhận job")
            print(rj)
    
    if error:
        return "error job"
    
    if rj[2] != "follow":
        print(error_color(f"[Device: {device_id}] [!] Không phải nhiệm vụ follow!"))

        r = drop_job(rj[1], rj[3], account_id, rj[2], device_id)
        if "error" in r:
            print(error_color(f"[Device: {device_id}] [!] Đã bỏ job thất bại."))
        else:
            print(success_color(f"[Device: {device_id}] [#] Đã bỏ job thành công!"))

        return "!=follow"


    if "error" in rj:
        print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi nhận job!"))
        
        r = drop_job(rj[1], rj[3], account_id, rj[2])
        if "error" in r:
            print(error_color(f"[Device: {device_id}] [!] Đã bỏ job thất bại."))
        else:
            print(success_color(f"[Device: {device_id}] [#] Đã bỏ job thành công!"))
        
        return "error job"
    
    else:
        desicion_follow_type = random.choice(
            ["via_link" for _ in range(10)] +\
            ["search" for _ in range(2)] +\
            ["via_link" for _ in range(10)]
        )
        if desicion_follow_type == "search": rf = follow(driver, adb_path, rj[0], time_scroll, device_id)
        elif desicion_follow_type == "via_link": rf = follow_via_link(adb_path, driver, device_id, rj[0], time_scroll)
        
        if "error" in rf:
            print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi follow!"))

            r = drop_job(rj[1], rj[3], account_id, rj[2], device_id)
            if "error" in r:
                print(error_color(f"[Device: {device_id}] [!] Đã bỏ job thất bại."))
            else:
                print(success_color(f"[Device: {device_id}] [#] Đã bỏ job thành công!"))

            return "error follow"
        
        elif "!=username" in rf:
            
            r = drop_job(rj[1], rj[3], account_id, rj[2], device_id)
            if "error" in r:
                print(error_color(f"[Device: {device_id}] [!] Đã bỏ job thất bại."))
            else:
                print(success_color(f"[Device: {device_id}] [#] Đã bỏ job thành công!"))

            return "diff username"
        
        else:
            rv = verify_complete_job(rj[1], account_id, device_id)

            if "error" in rv:
                print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi xác minh job."))

                r = drop_job(rj[1], rj[3], account_id, rj[2], device_id)
                if "error" in r:
                    print(error_color(f"[Device: {device_id}] [!] Đã bỏ job thất bại."))
                else:
                    print(success_color(f"[Device: {device_id}] [#] Đã bỏ job thành công!"))

                return "error verify job"
                
                # r = delete_cache(driver, adb_path)

                # if r == "error":
                #     return "delete cache error"
                # else:
                #     print(success_color("[#] đã xóa cache thành công."))
            
            else:
                print(success_color(f"[Device: {device_id}] [$] {rv[1]}"))
                print(success_color(f"[Device: {device_id}] [$] {rv[2]}"))
                from golike import prices
                print(success_color(f"[Device: {device_id}] [$] tổng thu nhập của tất cả phiên -> {prices}đ"))
                
                # print(system_color("[#] thực hiện xóa cache..."))
                # r = delete_cache(driver, adb_path)
                # if r == "error":
                #     return "delete cache error"
                # else:
                #     print(success_color("[#] đã xóa cache thành công."))
                
                return "success"


def run(adb_path, device_id, wait, appium_port, times_scroll=3, wait_for_when_error=5):
    more_wait_when_error = 1
    max_times_for_switch_account = 3
    max_times_for_error_verify_job = 2
    switch_account_counter = 0
    error_verify_job_counter = 0
    error_get_job_counter = 0
    max_times_for_error_get_job = 2
    max_times_for_error_follow = 2
    error_follow_counter = 0
    const_wait = wait

    driver = driver_init(adb_path, False, device_id, appium_port)
    accounts_id = check_tiktok_account_id(device_id)

    # wait = int(input(system_color(f"[Device: {device_id}] [?] Nhập số thời gian chờ\n-> ")))
    # mh_mode = input(system_color("[?] Nhập loại màn hình (old/new)\n-> ")).lower().strip()
    # print()
    
    print(system_color(f"[Device: {device_id}] [>] tiến hành đăng nhập tài khoản để bắt đầu chạy..."))
    id_gl = None
    success = False
    while True:
        
        try:
            username = login_tiktok_lite(adb_path, driver, device_id, appium_port)
        except:
            print(error_color(f"[Device: {device_id}] [!] Lỗi khi chuyển acc, khởi tạo lại driver..."))
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
            try:
                driver.quit()
            except:
                pass
            driver = driver_init(adb_path, False, device_id, appium_port)
            continue

        username = username['username']
        username = username.replace("@", "")

        for id_username in accounts_id:
            if username == id_username[1]:
                id_gl = id_username[0]
                print(success_color(f"[Device: {device_id}] [#] username '{username}' có tồn tại trong account golike"))
                success = True
                break

        if not success:
            print(error_color(f"[Device: {device_id}] [!] username '{username}' không tồn tại trong account golike"))
            continue
        else:
            break

    driver = waiting_scroll(driver, adb_path, 5, f"Đợi 5 scroll để bắt đầu...", device_id=device_id, appium_port=appium_port)

    while True:
        decision = random.choice(
            ["run" for _ in range(40)] +\
            ['ttc' for _ in range(18)] +\
            ['up' for _ in range(1)] +\
            ['change' for _ in range(1)] +\
            ["run" for _ in range(40)]
        )

        if decision == "ttc":
            r = ttc(driver, adb_path, device_id)
            if "error" in r:
                try:
                    driver.quit()
                except: pass
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi TTC khởi lại tại driver..."))
                driver = driver_init(adb_path, False, device_id, appium_port)
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
            else:
                print(success_color(f"[Device: {device_id}] [#] TTC thành công"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue

        if decision == "up":
            r = upload_image(driver, adb_path, device_id)
            if "error" in r:
                try:
                    driver.quit()
                except: pass
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi UP Ảnh khởi lại tại driver..."))
                driver = driver_init(adb_path, False, device_id, appium_port)
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
            else:
                print(success_color(f"[Device: {device_id}] [#] UP Ảnh thành công"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue

        if decision == "change":
            r = change_img_profile(driver, adb_path, device_id)
            if "error" in r:
                try:
                    driver.quit()
                except: pass
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi Đổi ảnh đại diện khởi lại tại driver..."))
                driver = driver_init(adb_path, False, device_id, appium_port)
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
            else:
                print(success_color(f"[Device: {device_id}] [#] Đổi ảnh đại diện thành công"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
                
        r = auto(driver, id_gl, adb_path, times_scroll, device_id)

        if r == "success":
            more_wait_when_error = 1
            error_verify_job_counter = 0
            error_get_job_counter = 0
            error_follow_counter = 0
        
        if r == "!=follow":
            driver = waiting_scroll(driver, adb_path, 1, f"Vui lòng đợi 1 scroll để nhận job tiếp theo...", device_id=device_id, appium_port=appium_port)
            continue
        
        elif r == "error verify job" or r == "error job" or r == "error follow":
            if r == "error verify job":
                error_verify_job_counter += 1
                switch_account_counter += 1
                more_wait_when_error += 1
            elif r == "error job":
                error_get_job_counter += 1
            elif r == "error follow":
                switch_account_counter += 1
                error_follow_counter += 1
                more_wait_when_error += 1
                print(system_color(f"[Device: {device_id}] [!] Lỗi follow, Khởi tạo lại driver..."))
                try:
                    driver.quit()
                except:
                    pass
                driver = driver_init(adb_path, False, device_id, appium_port)

            if error_verify_job_counter >= max_times_for_error_verify_job and r == "error verify job":
                print(error_color(f"[Device: {device_id}] [!] Lỗi xác minh job vượt qua số lần giới hạn, đổi account.."))
                pass
            elif error_get_job_counter >= max_times_for_error_get_job and r == "error job":
                print(error_color(f"[Device: {device_id}] [!] Lỗi nhận job vượt qua số lần giới hạn, đổi account.."))
                pass
            elif error_follow_counter >= max_times_for_error_follow and r == "error follow":
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi follow vượt qua số lần giới hạn, đổi account.."))
                pass

            elif error_verify_job_counter < max_times_for_error_verify_job and r == "error verify job":
                print(system_color(f"[Device: {device_id}] [!] Thử lại follow trên account '{username}' lần thử {error_verify_job_counter}/{max_times_for_error_verify_job}"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait_for_when_error * more_wait_when_error, f"Vui lòng đợi {wait_for_when_error * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
            elif error_get_job_counter < max_times_for_error_get_job and r == "error job":
                print(system_color(f"[Device: {device_id}] [!] Thử lại nhận job trên account '{username}' lần thử {error_get_job_counter}/{max_times_for_error_get_job}"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait_for_when_error * more_wait_when_error, f"Vui lòng đợi {wait_for_when_error * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
            elif error_follow_counter < max_times_for_error_follow and r == "error follow":
                print(system_color(f"[Device: {device_id}] [!] Thử lại follow trên account '{username}' lần thử {error_follow_counter}/{max_times_for_error_follow}"))
                try:
                    driver = waiting_scroll(driver, adb_path, wait_for_when_error * more_wait_when_error, f"Vui lòng đợi {wait_for_when_error * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                continue
             
            if switch_account_counter >= max_times_for_switch_account:
                print(system_color(f"[Device: {device_id}] [>] Số lần đổi account đã lớn hơn mức quy định, tiến hành scroll..."))
                try:
                    driver = waiting_scroll(driver, adb_path, wait_for_when_error * more_wait_when_error, f"Vui lòng đợi {wait_for_when_error * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
                switch_account_counter = 0
            
            if r == "error job":
                print(system_color(f"[Device: {device_id}] [!] Lỗi nhận job, tiến hành đổi tài khoản khác..."))
            else:
                print(system_color(f"[Device: {device_id}] [!] Lỗi xác minh job, tiến hành đổi tài khoản khác..."))
            
            id_gl = None
            success = False
            while True:
                
                try:
                    username = login_tiktok_lite(adb_path, driver, device_id, appium_port)
                except:
                    print(error_color(f"[Device: {device_id}] [!] Lỗi khi chuyển acc, khởi tạo lại driver..."))
                    os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = driver_init(adb_path, False, device_id, appium_port)
                    continue

                username = username['username']
                username = username.replace("@", "")

                for id_username in accounts_id:
                    if username == id_username[1]:
                        id_gl = id_username[0]
                        print(success_color(f"[Device: {device_id}] [#] username '{username}' có tồn tại trong account golike"))
                        success = True
                        break

                if not success:
                    print(error_color(f"[Device: {device_id}] [!] username '{username}' không tồn tại trong account golike"))
                    continue
                else:
                    break
            
            decision = random.choice(["UP Ảnh", "Đổi ảnh đại diện"])
            print(system_color(f"[Device: {device_id}] [>] {decision} sau khi đổi tài khoản để tăng trust..."))
            r = upload_image(driver, adb_path, device_id) if decision == "UP Ảnh" else change_img_profile(driver, adb_path, device_id)
            if "error" in r:
                try:
                    driver.quit()
                except: pass
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi {decision} khởi lại tại driver..."))
                driver = driver_init(adb_path, False, device_id, appium_port)
                try:
                    driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
                except:
                    pass
            else:
                print(success_color(f"[Device: {device_id}] [#] {decision} thành công"))
            continue

        elif r == "error follow":
            print(system_color(f"[Device: {device_id}] [!] Lỗi follow, Khởi tạo lại driver..."))
            try:
                driver.quit()
            except:
                pass
            driver = driver_init(adb_path, False, device_id, appium_port)

            # r = delete_cache(driver, adb_path)
            # if r == "error":
            #     print(error_color("[!] đã xóa cache không thành công, khởi tạo lại driver.."))
            #     driver = driver_init(adb_path, False)
            # else:
            #     print(success_color("[#] đã xóa cache thành công."))

            more_wait_when_error += 1

        elif r == "delete cache error":
            try:
                driver.quit()
            except:
                pass
            print(system_color(f"[Device: {device_id}] [!] Lỗi khi xóa cache, Khởi tạo lại driver..."))
            driver = driver_init(adb_path, False, device_id, appium_port)
            continue
        
        elif r == "diff username":
            print(system_color(f"[Device: {device_id}] [!] Lỗi khác username."))
            continue

        try:
            driver = waiting_scroll(driver, adb_path, wait * more_wait_when_error, f"Vui lòng đợi {wait * more_wait_when_error} scroll để follow tiếp theo...", device_id=device_id, appium_port=appium_port)
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
        print(system_color("| [2] Chạy tool                                   |"))
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

            print(error_color(f"[!] Bạn có thể Ctrl+C để thoát khi tool đang chạy"))
            print()

            appium_port = input(system_color('[?] Nhập port appium của bạn\n-> '))
            
            devices = get_devices(adb_path)
            device_with_options = {}
            print(system_color("[!] Bạn có thể gõ 'skip' để bỏ qua thiết bị mà bạn không muốn nó chạy."))
            
            for device_id in devices:
                wait = input(system_color(f"[Device: {device_id}] [?] Nhập số thời gian chờ\n-> "))
                if wait.strip().lower() == "skip":
                    device_with_options[device_id] = False
                    continue
                device_with_options[device_id] = (int(wait))
            print()
            
            for key, value in device_with_options.items():
                if not value:
                    continue
                try:
                    thread = threading.Thread(target=run, args=[adb_path, key, value[0], appium_port])
                    thread.start()
                    waiting_ui(10, "Đợi 4s để chạy tất cả", key)
                    continue
                except KeyboardInterrupt:
                    waiting_ui(4, "Bạn đã chọn thoát chương trình 4s")
                    os.system("cls") if sys.platform.startswith("win") else os.system("clear")
                    break
            input(success_color("[#] Đã chạy xong tất cả thiết bị\n"))