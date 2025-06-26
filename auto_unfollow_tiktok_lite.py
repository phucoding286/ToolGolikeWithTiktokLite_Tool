from modules import *
from golike import check_tiktok_account_id, GOLIKE_HEADERS
from following_checker import check_follow_count

def select_id_from_username(username, device_id):
    for check in check_tiktok_account_id(device_id):
        if check[1] == username: return check[0]

def get_user_da_duyet_tien(device_id, account_id, limit, page):
    url = f"https://gateway.golike.net/api/advertising/publishers/tiktok/logs?limit={limit}&log_type=success&page={page}&_t=1750926867&account_id={account_id}"
    for i in range(5):
        try:
            r = scraper.get(url, headers=GOLIKE_HEADERS)
            users_da_duyet_tien = list()
            for object_user in r.json()['data']:
                users_da_duyet_tien.append((object_user['advertising']['link'], object_user['advertising']['object_id']))
            return {"success": users_da_duyet_tien}
        except:
            print(error_color(f"[Device: {device_id}] [!] Lỗi khi lấy list user đã duyệt tiền, thử lại.."))
    else:
        return {"error": "Đã có lỗi khi lấy list user đã duyệt tiền"}

def unfollow(driver: webdriver.Remote, adb_path, device_id, object_target_id):
    os.system(f"""{adb_path} -s {device_id} shell am start -n com.zhiliaoapp.musically.go/com.ss.android.ugc.aweme.deeplink.DeepLinkActivityV2 -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "snssdk1180://user/profile/{object_target_id}""")
    try:
        unfollow_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.ImageView[@resource-id='com.zhiliaoapp.musically.go:id/dsb']")
        ))
        unfollow_btn.click()
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        return {"success": "Đã follow thành công"}
    except:
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        return {"error": "Đã có lỗi khi unfollow"}
    
def auto_unfollow_tiktok_lite(driver, adb_path, device_id, account_username, limit_check_follow):
    r = check_follow_count(account_username, limit_check_follow)
    if not r[0]: return
    print(error_color(f"[Device: {device_id}] [!] Phát hiện số lượng follwing của account '{account_username}' lớn hơn mức '{limit_check_follow}', tiến hành unfollow tự động."))
    
    tiktok_acc_id = select_id_from_username(account_username, device_id=device_id)
    error_count, idx_page_log, length_sequence_log = 1, 1, 30
    states = [f"{idx_page_log}_{length_sequence_log}"]

    while error_count < 10:
        list_da_duyet = get_user_da_duyet_tien(device_id, tiktok_acc_id, length_sequence_log, idx_page_log)
        if "success" in list_da_duyet: list_da_duyet = list_da_duyet['success']
        else: return
        if str(list_da_duyet).strip() == "[]": return

        for obj_target_user in list_da_duyet:
            if error_count >= 10: return
            r = unfollow(driver, adb_path, device_id, obj_target_user[1])
            if "error" in r:
                print(error_color(f"[Device: {device_id}] [!] Unfollow user {obj_target_user[0]} thất bại."))
                error_count += 1

                if (error_count - 1) % 2 == 0:
                    idx_page_log = random.randint(1, 100)
                    length_sequence_log = random.randint(1, 100)
                    curr_state = f"{idx_page_log}_{length_sequence_log}"
                     
                    max_count = 1
                    while curr_state in states and max_count < 1000:
                        idx_page_log = random.randint(1, 100)
                        length_sequence_log = random.randint(1, 100)
                        curr_state = f"{idx_page_log}_{length_sequence_log}"
                        max_count += 1
                    states.append(curr_state)

                    break
            else:
                print(success_color(f"[Device: {device_id}] [#] Unfollow user {obj_target_user[0]} thành công."))
                error_count = 1

        idx_page_log += 1

if __name__ == "__main__":
    GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
    GOLIKE_HEADERS["t"] = open("t.txt", "r").read()
    adb_path = open("adb_path.txt").read()
    device_id = "192.168.1.56:5555"

    driver = driver_init(adb_path, ask_udid=False, device_id=device_id, appium_port="1000")
    auto_unfollow_tiktok_lite(driver, adb_path, device_id, "ngi.tnh.xa", limit_check_follow=10000)
