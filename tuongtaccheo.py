from modules import *

def manual_send_keys(adb_path, text: str, enter=False, device_id=None):
    time.sleep(4)
    text = "%s".join(text.split(" "))
    os.system(f'{adb_path} -s {device_id}  shell input text "{text}"')
    if enter:
        os.system(f'{adb_path} -s {device_id}  shell input keyevent 66')

def ttc(driver, adb_path, device_id, current_account, ttc_hist_username_filepath="ttc_hist.json"):
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 350}")
        
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
        
        time.sleep(1)
        random_find = ["Follow cheo", "Tuong tac cheo", "Cheo follow", "Cheo tuong tac", "Follow cheo moi nhat"]
        manual_send_keys(adb_path, random.choice(random_find), True, device_id)

        time.sleep(2)

        video_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.bytedance.ies.xelement.viewpager.childitem.LynxTabbarItem[3]")
            )
        )
        video_list.click()

        video_select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.lynx.tasm.ui.image.FlattenUIImage[3]")
            )
        )
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2)-20} {height/2}")
        time.sleep(1)
        
        for i in range(30):
            time.sleep(1)
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2) - 20} {(height / 2) - 350}")
        
            try:
                mini_follow = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//android.widget.ImageView[@resource-id='com.zhiliaoapp.musically.go:id/ds5']")
                    )
                )
                mini_follow.click()

                avatar = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//android.widget.ImageView[@resource-id='com.zhiliaoapp.musically.go:id/etq']")
                    )
                )
                avatar.click()
                
                username = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//android.widget.Button[@resource-id="com.zhiliaoapp.musically.go:id/etv"]')
                    )
                ).text
                
                # lưu username đã TTC để sau này unfollow
                if not os.path.exists(ttc_hist_username_filepath):
                    with open(ttc_hist_username_filepath, "w", encoding="utf8") as f:
                        obj = {current_account: [username]}
                        json.dump(obj, f, indent=4, ensure_ascii=False)
                else:
                    with open(ttc_hist_username_filepath, "r", encoding="utf8") as f:
                        obj = json.load(f)

                    if current_account not in obj:
                        obj[current_account] = [username]
                    else:
                        obj[current_account].append(username)

                    with open(ttc_hist_username_filepath, "w", encoding="utf8") as f:
                        json.dump(obj, f, indent=4, ensure_ascii=False)

                os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
                time.sleep(1)
                os.system(adb_path + f" -s {device_id}" + f" shell input tap {(width/2) - 20} {(height / 2) - 350}")

                break
            except:
                try: waiting_scroll(driver, adb_path, times_scroll=1, text="Scroll để tìm video TTC", rdn_options=False, recreate_driver=False, device_id=device_id)
                except: return {"error": "TTC thất bại"}
                continue

        comment_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.ImageView[@resource-id='com.zhiliaoapp.musically.go:id/djp']")
            )
        )
        comment_btn.click()
        
        try:
            cell_comment = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[@resource-id='com.zhiliaoapp.musically.go:id/dfk']")
                )
            )
            cell_comment.click()
        except:
            try:
                cell_comment = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//android.view.View[@resource-id='com.zhiliaoapp.musically.go:id/dbq']")
                    )
                )
                cell_comment.click()
            except: pass
        
        bot_comments = [
            "tt", "@tt", "Tuong tac cho minh di ban oi, minh follow roi do",
            "Tuong tac lai minh di, follow roi, cam on ban nhieu", "tt ne ban",
            "Minh rat thich kenh cua ban, follow lai minh di, minh da follow roi",
            "Hii, follow lai cho to nhe, to follow cau roi do", "Cheo follow nhe, minh follow roi a.",
            "Ban oi, nho follow lai minh nhe, minh follow roi a", "Ban tra cho minh lai tim duoc ko, minh follow roi",
            "Tra lai cho minh tim nha, minh follow ban roi", "To follow cau roi do, tra cho minh comment nha, tks cau",
            "Minh follow ban xong roi do, ban tra cho minh vai tim nhe, hay cmt cung duoc, cam on ban",
            "Follow xong roi nhe! nho tra lai cho minh do :3", "Da xong roi. dang doi nhan follow lai hehe...",
            "Follow roi nhe ban, minh cho ban fl lai."
        ]
        manual_send_keys(adb_path, random.choice(bot_comments), False, device_id)
        
        time.sleep(1)
        os.system(adb_path + f" -s {device_id}" + f" shell input tap {width-50} {(height/2)+50}")
        try:
            cell_comment = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[@resource-id='com.zhiliaoapp.musically.go:id/dfk']")
                )
            )
        except:
            os.system(adb_path + f" -s {device_id}" + f" shell input tap {width-50} {(height/2)}")

        # thoat
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

        return {"sucess": "TTC thành công"}
    except:
        return {"error": "TTC thất bại"}

if __name__ == "__main__":
    adb_path = open("adb_path.txt", "r").read()
    driver = driver_init(adb_path, ask_udid=False, device_id="192.168.1.4:5555", appium_port="1000")
    print(ttc(driver, adb_path, device_id="192.168.1.4:5555", current_account="pt12190"))
    input(">>> ")