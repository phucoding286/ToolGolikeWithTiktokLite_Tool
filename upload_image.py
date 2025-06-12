from modules import *

def upload_image(driver, adb_path, device_id):
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {height/2}")

        add_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[3]")
            )
        )
        add_btn.click()

        time.sleep(2)

        img_choose = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.GridView/android.widget.FrameLayout[2]/android.widget.ImageView")
                )
            )
        img_choose.click()

        post_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.Button[@text='Đăng']")
            )
        )
        post_btn.click()
        
        print(success_color(f"[Device: {device_id}] [..] UP Ảnh thành công, đợi 10s để tiếp tục!"))
        time.sleep(10)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

        return {"success": "Upload image thành công"}
    except:
        return {"error": "Upload image thất bại."}

if __name__ == "__main__":
    adb_path = open("adb_path.txt", "r").read()
    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.4:5555", appium_port="1000")
    print(upload_image(driver, adb_path, device_id="192.168.1.4:5555"))
    input(">>> ")