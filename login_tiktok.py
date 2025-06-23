from modules import *
from process_popup_via_screencap import (
    popup_processing,
    screencap
)

google_account_elements = 0
next_count = {}
scroll_to_find_delete_btn = 20

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

def login_tiktok_lite(adb_path, driver: webdriver.Remote, device_id, appium_port):
    global google_account_elements
    global next_count
    global capabilities
    global scroll_to_find_delete_btn

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
    os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 110}")

    option_btns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
        )
    )
    option_btns[-1].click()

    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    
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
                waiting_scroll(driver, adb_path, 1, "tìm kiếm nút xóa cache...", False, False, device_id=device_id, appium_port=appium_port)
                continue

        waiting_scroll(driver, adb_path, 2, "tìm kiếm nút đăng xuất...", False, False, device_id=device_id, appium_port=appium_port)
        
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
                waiting_scroll(driver, adb_path, 1, "tìm kiếm nút đăng xuất...", False, False, device_id=device_id, appium_port=appium_port)
                continue

        # dùng toán học để xác định tọa độ của nút đăng xuất trong popup đăng xuất
        # lý do dùng tọa độ thay vì appium: Do appium không quét được popup tiktok lite
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        width_dx = (width / 2) + 150
        height_dx = (height / 2) + 145
        width_asdt = (width / 2) - 150
        height_asdt = (height / 2) + 230
        
        r = None
        max_times = 2
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

        if r == "Đăng xuất?":      
            time.sleep(1)
            print(system_color(f"[Device: {device_id}] [>] Tọa độ đã tính toán {width_dx}x{height_dx} nút đăng xuất."))
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width_dx} {height_dx}")
        elif r == "Trạng thái tài khoản":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2)+150} {(height/2)+145}")
        elif r == "Lưu thông tin đăng nhập?":
            time.sleep(1)
            print(system_color(f"[Device: {device_id}] [>] Tọa độ đã tính toán {width_asdt}x{height_asdt} nút 'để sau' cho popup lưu thông tin đăng nhập."))
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width_asdt} {height_asdt}")
            time.sleep(1)
            print(system_color(f"[Device: {device_id}] [>] Tọa độ đã tính toán {width_dx}x{height_dx} nút đăng xuất."))
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width_dx} {height_dx}")
        elif r == "Thêm bạn bè, dùng Tiktok t":
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height/2)+255}")
        elif r == "Thêm bạn bè, dùng TikTok":
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

    if device_id not in next_count:
        next_count[device_id] = 0
    
    _gaelms[next_count[device_id]].click()

    if next_count[device_id] >= google_account_elements:
        next_count[device_id] = 0
    else:
        next_count[device_id] += 1

    r = None
    max_times = 2
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

    print(system_color(f"[Device: {device_id}] [>] lấy username..."))
    os.system(adb_path + f" -s {device_id}" + f" shell input tap {720/2} {(1424 / 2) - 350}")
    option_btns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout")
        )
    )
    option_btns[-1].click()

    r = None
    max_times = 2
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
    
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.Button")
        )
    )
    username = username[0].text
    os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

    return {"username": username}

if __name__ == "__main__": 
    pass
    # capabilities['udid'] = "192.168.1.56:5555"
    # adb_path = open("adb_path.txt", "r").read()

    # driver = driver_init(adb_path, ask_udid=False, device_id="351a9fc", appium_port="1000")
    # size = driver.get_window_size()
    # input(size)
    # r = login_tiktok_lite(adb_path, driver, device_id="351a9fc", appium_port="1000")
    # print(r)
    # input(">>> ")
    # r = login_tiktok_lite(adb_path, driver, device_id="192.168.1.56:5555", appium_port="1000")
    # print(r)