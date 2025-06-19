from modules import *

def upload_image(driver, adb_path, device_id, folderpath_img_upload="./img_for_upload_for_golike_tool_by_phu"):
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
            break
        except:
            print(error_color(f"[Device: {device_id}] [!] Push ảnh lên thiết bị thất bại, thử lại..."))
            continue

    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 100}")

        add_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[3]")
            )
        )
        add_btn.click()

        time.sleep(2)

        img_choose = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.GridView/android.widget.FrameLayout[1]/android.widget.ImageView")
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
    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.56:5555", appium_port="1000")
    # print(upload_image(None, adb_path, device_id="192.168.1.56:5555"))
    # input(">>> ")