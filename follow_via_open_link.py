from modules import *

def follow_via_link(adb_path, driver, device_id, username_link, time_scroll=3):
    try:
        for retry in range(5):
            try:
                response = scraper.get(username_link)
                profile_id = response.text.split("\"user\":{\"id\":\"")[1].split("\",\"")[0]
                print(success_color(f"[Device: {device_id}] [#] Lấy profile id thành công"))
                break
            except:
                time.sleep(1)
                print(error_color(f"[Device: {device_id}] [!] Lỗi khi lấy profile id, thử lại {retry+1}/5"))
                continue
        else:
            return "!=username"

        os.system(f"""{adb_path} -s {device_id} shell am start -n com.zhiliaoapp.musically.go/com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2 -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "snssdk1180://user/profile/{profile_id}?params_url=https://www.tiktok.com/{username_link.split("/")[3]}""")

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

            time.sleep(2)
                
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
    # driver = driver_init(adb_path, ask_udid=False, device_id="351a9fc", appium_port="1000")
    out = follow_via_link(adb_path, None, "351a9fc", "https://www.tiktok.com/@phujstruong/", 3)
    print(out)