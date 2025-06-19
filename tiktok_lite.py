from modules import *
from process_popup_via_screencap import screencap, popup_processing

def manual_send_keys(adb_path, text: str, enter=False, device_id=None):
    os.system(f'{adb_path} -s {device_id}  shell input text "{text}"')
    time.sleep(2)
    if enter:
        os.system(f'{adb_path} -s {device_id}  shell input keyevent 66')

def screen_cap_(adb_path, device_id):
    r = None
    max_times = 1
    count = 0
    while count < 1:
        try:
            r = screencap(adb_path, device_id)
            r = popup_processing(r)
            print(system_color(f"[Device: {device_id}] Kết quả detected -> {r}"))
            if r is None and count < max_times:
                count += 1
                print(system_color(f"[Device: {device_id}] [>] Kết quả là None, thử lại ({count}/{max_times})"))
                continue
            break
        except:
            print(error_color(f"[Device: {device_id}] [!] Lỗi không thể chụp ảnh màn hình và detect văn bản trong ảnh."))
            continue
    return r

def follow(driver, adb_path="adb", target_link="https://tiktok.com/@example/", time_scroll=3, device_id=None):
    try:

        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        r = screen_cap_(adb_path, device_id)
        if r == "Trạng thái tài khoản":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2)+150} {(height/2)+145}")
        elif r == "Follow bạn bè của bạn":
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        elif r == "Thêm bạn bè, dùng Tiktok t":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Thêm bạn bè, dùng TikTok":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Đồng bộ danh sách bạn bè":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "trên Tiktok, hãy cho phép tru":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Không cho phép":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Cập nhật Chính sách về":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Đã hiểu":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
            r = screen_cap_(adb_path, device_id)
            if r == "Đã hiểu": os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+420}")
        driver.activate_app(capabilities['appPackage'])
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {height/2}")
        
        time.sleep(2)
        kham_pha_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView")
            )
        )
        kham_pha_btn.click()

        find_cell = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Tìm kiếm"]')
            )
        )
        find_cell.click()

        manual_send_keys(adb_path, target_link.split("/")[3], True, device_id)

        time.sleep(2)

        user_finded_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.bytedance.ies.xelement.viewpager.childitem.LynxTabbarItem[2]")
            )
        )
        user_finded_list.click()
        
        for _ in range(5):
            try:
                follow_btn = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '(//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Follow"])[1]')
                    )
                )
                break
            except:
                time.sleep(1)
                continue
        
        # check username
        all_usernames = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, f'com.lynx.tasm.behavior.ui.text.FlattenUIText')
            )
        )
        top_username = ""
        try:
            for username in all_usernames:
                if username.text.strip() == target_link.split("/")[3].replace("@", ""):
                    top_username = username.text.strip()
                    break
            else:
                os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
                
                exit_btn2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.lynx.component.svg.UISvg")
                    )
                )
                time.sleep(1)
                exit_btn2.click()

                time.sleep(1)
                os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

                return "!=username"
        except: pass
        
        time.sleep(1)
        
        # xem video của mục tiêu cần follow trước khi follow
        top_username_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="{top_username}"]')
            )
        )
        top_username_btn.click()
        
        try:
            top_user_video_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.GridView/android.widget.FrameLayout[1]/android.view.View')
                )
            )
            top_user_video_btn.click()
        
            times_scrol_rdn = random.choice([i for i in range(time_scroll)])
            if times_scrol_rdn < 1:
                times_scrol_rdn = time_scroll
                
            r = waiting_scroll(
                driver, adb_path,
                times_scroll=times_scrol_rdn,
                text="Xem video của user trước khi follow",
                recreate_driver=False,
                device_id=device_id
            )
            if r == "lỗi khi scroll":
                raise ValueError("")
        
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
            time.sleep(1)

        except:
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
            time.sleep(1)
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
                
            exit_btn2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.lynx.component.svg.UISvg")
                )
            )
            time.sleep(1)
            exit_btn2.click()

            time.sleep(1)
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

            return "!=username"
        
        # follow và thoát
        follow_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//android.widget.Button[@text="Follow"]')
            )
        )
        time.sleep(1)
        follow_btn.click()
        
        # thoat
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        
        exit_btn2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.lynx.component.svg.UISvg")
            )
        )
        time.sleep(1)
        exit_btn2.click()
        
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

        return {"success": "Follow thành công!"}
    
    except:
        return {"error": "Đã có lỗi khi follow"}
    
if __name__ == "__main__":
    adb_path = open("adb_path.txt", "r").read()
    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.56:5555", appium_port="1000")
    print(follow(driver, adb_path, target_link="https://www.tiktok.com/@kekdjdjd7", device_id="192.168.1.56:5555"))
    time.sleep(5)