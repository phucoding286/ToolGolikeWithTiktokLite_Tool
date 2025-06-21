from modules import *
from process_popup_via_screencap import screencap, popup_processing

diff_username_flag = list()

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

def follow_via_link(adb_path, driver, device_id, username_link, time_scroll=3):
    global diff_username_flag
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
    except:
        return {"error": "Đã có lỗi khi follow"}
    
    if device_id not in diff_username_flag and random.choice([False, True, False]):
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
    
    if device_id in diff_username_flag:
        diff_username_flag.remove(device_id)

    try:
        for retry in range(5):
            try:
                response = scraper.get(username_link, timeout=10)
                profile_id = response.text.split("\"user\":{\"id\":\"")[1].split("\",\"")[0]
                print(success_color(f"[Device: {device_id}] [#] Lấy profile id thành công"))
                break
            except:
                time.sleep(1)
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi lấy profile id, thử lại {retry+1}/5"))
                continue
        else:
            diff_username_flag.append(device_id)
            return "!=username"

        os.system(f"""{adb_path} -s {device_id} shell am start -n com.zhiliaoapp.musically.go/com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2 -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "snssdk1180://user/profile/{profile_id}?params_url=https://www.tiktok.com/{username_link.split("/")[3]}""")

        try:
            top_user_video_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.GridView/android.widget.FrameLayout[1]/android.view.View')
                )
            )
            top_user_video_btn.click()

            try:
                WebDriverWait(driver, 1.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//android.widget.Button[@text="Tin nhắn"]')
                    )
                )
                return "!=username"
            except: pass
        
            times_scrol_rdn = random.choice([i for i in range(time_scroll)])
            if times_scrol_rdn < 1:
                times_scrol_rdn = time_scroll

            time.sleep(2)
                
            r = waiting_scroll(
                driver, adb_path,
                times_scroll=times_scrol_rdn,
                text="Xem video của user trước khi follow",
                recreate_driver=False,
                device_id=device_id,
                watch_user_video=True
            )
            if r == "lỗi khi scroll":
                raise ValueError("")
        
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
            time.sleep(1)

        except:
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
            size = driver.get_window_size()
            width = size['width']
            height = size['height']
            driver.swipe(start_x=width/2, start_y=height/2, end_x=width/2, end_y=0, duration=500)
            diff_username_flag.append(device_id)
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

        return {"success": "Follow thành công!"}
    
    except:
        return {"error": "Đã có lỗi khi follow"}

if __name__ == "__main__":
    adb_path = open("adb_path.txt", "r").read()
    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.56:5555", appium_port="1000")
    out = follow_via_link(adb_path, driver, "192.168.1.56:5555", "https://www.tiktok.com/@phujstruong/", 3)
    print(out)