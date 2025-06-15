from modules import *
from process_popup_via_screencap import screencap, popup_processing

def screen_cap_(adb_path, device_id):
    r = None
    max_times = 1
    count = 0
    while True:
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

def upload_avatar_img(device_id, adb_path, folderpath_img_upload):
    folderpath_img_upload = os.path.abspath(folderpath_img_upload)
    while True:
        try:
            list_img = os.listdir(folderpath_img_upload)
            random_img = random.choice(list_img)
            list_img.remove(random_img)
            path_come_img = folderpath_img_upload + "/" + random_img
    
            for char in list(" `~!@#$%^&*()-+=[]{}:;'\"<>?,./|\\"):
                if len(random_img.split(char)) > 1:
                    new_img = Image.open(path_come_img)
                    for char in list(" `~!@#$%^&*()-+=[]{}:;'\"<>?,/|\\"): random_img = random_img.replace(char, "")
                    
                    if random_img in list_img:
                        random_sent = list("qwertyuiopasdfghjklzxcvbnm"*4)
                        random.shuffle(random_sent)
                        random_sent = "".join(random_sent[:int(len(random_sent)/4)])
                        random_img = random_sent + random_img
                        
                    new_path = folderpath_img_upload + "/" + random_img
                    new_img.save(new_path)
                    if new_path != path_come_img: os.remove(path_come_img)
                    path_come_img = new_path
                    break
    
            if path_come_img.split(".")[-1] not in ["jpeg"]:
                new_img = Image.open(path_come_img)
                random_img = random_img.replace(".","") + ".jpeg"
                new_img_path = folderpath_img_upload + "/" + random_img
                new_img.save(new_img_path, format="JPEG")
                os.remove(path_come_img)
                path_come_img = new_img_path

            path_for_save = "/storage/emulated/0/Download/" + random_img
            os.system(adb_path + f" -s {device_id}" + f" shell rm {path_for_save}")
            time.sleep(1)
            os.system(adb_path + f" -s {device_id}" + f" shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/{random_img}")
            time.sleep(1)
            os.system(adb_path + f" -s {device_id}" + f" push {path_come_img} {path_for_save}")
            time.sleep(2)
            os.system(adb_path + f" -s {device_id}" + f" shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/{random_img}")
            return random_img, path_for_save
        except:
            print(error_color(f"[Device: {device_id}] [!] Push ảnh lên thiết bị thất bại, thử lại..."))
            continue

def change_img_profile(driver: webdriver.Remote, adb_path, device_id, folderpath_img_upload="./img_for_change_avatar_for_golike_tool_by_phu"):
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {height/2}")

        option_btns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
            )
        )
        option_btns[-1].click()
    
        r = screen_cap_(adb_path, device_id)
        if r == "Follow bạn bè của bạn":
            os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        elif r == "Trạng thái tài khoản":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2)+150} {(height/2)+145}")
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

        random_img, path_for_save = upload_avatar_img(device_id, adb_path, folderpath_img_upload)

        avatar_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.ImageView[@resource-id='com.zhiliaoapp.musically.go:id/dxe']"))
        )
        avatar_btn.click()

        edit_img_profile_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "com.lynx.component.svg.UISvg"))
        )
        edit_img_profile_btn[1].click()

        select_first_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.ImageView[1]'))
        )
        select_first_img.click()

        save_img_profile_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='Lưu']"))
        )
        save_img_profile_btn.click()

        print(success_color(f"[Device: {device_id}] [..] Đã đổi ảnh đại diện thành công, đợi 10s để tiếp tục!"))
        time.sleep(10)

        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        return {"success": "Đã change profile image thành công!"}
    except:
        return {"error": "Đã có lỗi khi change profile image!"}
        
if __name__ == "__main__":
    adb_path = open("adb_path.txt", "r").read()
    # driver = driver_init(adb_path, ask_udid=False, device_id="351a9fc", appium_port="1000")
    # print(change_img_profile(driver, adb_path, device_id="351a9fc"))
    upload_avatar_img("192.168.1.56:5555", adb_path, r"E:\MySRC\golike-tools\golike_tiktok_lite_adb_api\img_for_change_avatar_for_golike_tool_by_phu")
    input(">>> ")