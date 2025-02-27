from modules import *

google_account_elements = 0
next_count = 0
scroll_to_find_delete_btn = 20

def login_tiktok_lite(adb_path, driver, device_id, mh_mode, appium_port):
    global google_account_elements
    global next_count
    global capabilities
    global scroll_to_find_delete_btn

    option_btns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
        )
    )
    option_btns[-1].click()
    
    logined_previous = False
    try:
        ba_cham = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.widget.ImageView')
            )
        )
        ba_cham.click()

        setting = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//android.widget.FrameLayout[@content-desc="Trang tính dưới cùng"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView')
            )
        )
        setting.click()
        
        for _ in range(scroll_to_find_delete_btn):
            try:
                delete_cache_btn = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Xóa bộ nhớ đệm"]')
                    )
                )
                delete_cache_btn.click()
                break
            except:
                waiting_scroll(driver, adb_path, 1, "tìm kiếm nút xóa cache...", False, mh_mode, False, device_id=device_id, appium_port=appium_port)
                continue

        waiting_scroll(driver, adb_path, 2, "tìm kiếm nút đăng xuất...", False, mh_mode, False, device_id=device_id, appium_port=appium_port)
        
        for _ in range(scroll_to_find_delete_btn):
            try:
                logout = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.ss.android.ugc.aweme.spark.xelements.ui.LynxRipple[last()]')
                    )
                )
                logout.click()
                break
            except:
                waiting_scroll(driver, adb_path, 1, "tìm kiếm nút đăng xuất...", False, mh_mode, False, device_id=device_id, appium_port=appium_port)
                continue

        # dùng toán học để xác định tọa độ của nút đăng xuất trong popup đăng xuất
        # lý do dùng tọa độ thay vì appium: Do appium không quét được popup tiktok lite
        size = driver.get_window_size()

        width = size['width']
        height = size['height']

        width = (width / 2) + 150
        height = (height / 2) + 145
        
        time.sleep(1)
        print(system_color(f"[Device: {device_id}] [>] Tọa độ đã tính toán {width}x{height}"))
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width} {height}")
        logined_previous = True

    except:
        logined_previous = False
    
    if logined_previous:
        option_btns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
            )
        )
        option_btns[-1].click()
    
    option_logins = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/X.02h")
        )
    )
    options_xpath_path = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/X.02h"
    for i in range(len(option_logins)):
        __get = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, options_xpath_path+f"[{i+1}]/android.widget.TextView")
            )
        )
        print(system_color(f"[Device: {device_id}] [>] Đang detect ô cần đăng nhập, text output: {__get.text}"))
        if __get.text == "Tiếp tục với Google":
            option_logins[i].click()
            break
    
    _gaelms = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout")
        )
    )
    google_account_elements = len(_gaelms) -2
    
    _gaelms[next_count].click()
    if next_count >= google_account_elements:
        next_count = 0
    else:
        next_count += 1
    
    print(system_color(f"[Device: {device_id}] [>] lấy username..."))
    option_btns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
        )
    )
    option_btns[-1].click()
    os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
    option_btns[-1].click()

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.Button")
        )
    )
    username = username[0].text
    os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
    return {"username": username}

if __name__ == "__main__":
    capabilities['udid'] = "192.168.1.56:5555"
    adb_path = open("adb_path.txt", "r").read()

    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.56:5555", appium_port="1000")
    r = login_tiktok_lite(adb_path, driver, mh_mode="old", device_id="192.168.1.56:5555", appium_port="1000")
    print(r)
    input(">>> ")
    r = login_tiktok_lite(adb_path, driver, mh_mode="old", device_id="192.168.1.56:5555", appium_port="1000")
    print(r)