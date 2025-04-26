from modules import *
from urllib.parse import parse_qs

API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
hgf_headers = {"Authorization": "Bearer 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"}

headers = {
    "authority": "www.tiktok.com",
    "method": "GET",
    "scheme": "https",
    "accept": "*/*",
    "cookie": "tt_chain_token=X66lE4o0DpyCF1ibFTjGJg==; delay_guest_mode_vid=5; living_user_id=834047467792; _ga=GA1.1.1247099752.1738738263; FPID=FPID2.2.VZM%2Fgzvxh9nYVLwgqR8gxgxqn7HwViS54rm6LtN4hcw%3D.1738738263; FPAU=1.2.263400365.1738738063; _fbp=fb.1.1738738063327.1924554924; _ga_LWWPCY99PB=GS1.1.1738738263.1.1.1738738287.0.0.1076452525; _ttp=2sfbKr3VXCjbSbVmQNeq13Mwv98; passport_csrf_token=cb080fc5b8f9f99145a8b4d6f4ef022e; passport_csrf_token_default=cb080fc5b8f9f99145a8b4d6f4ef022e; last_login_method=google; tt_csrf_token=P8NUvrJA-DzHvj6Z6gSuHCk1mBXSJkPkqF50; s_v_web_id=verify_m887bmcx_0t1JnYgM_XpUK_48wt_9CwL_GaY5cnPJVRzA; multi_sids=6706066558852531202%3A4131798bcf0ce7b723d3fd9d20d3343d; cmpl_token=AgQQAPPdF-RO0o0uUqbAut07_Q12utDS_4MOYNlmqA; passport_auth_status=00ee38b08dc168d4c2613ee1c842cfe5%2C; passport_auth_status_ss=00ee38b08dc168d4c2613ee1c842cfe5%2C; uid_tt=cc015355204312d1c6c65501cc309d865a204fc8e409ab6ea3be23a2ad64dc74; uid_tt_ss=cc015355204312d1c6c65501cc309d865a204fc8e409ab6ea3be23a2ad64dc74; sid_tt=4131798bcf0ce7b723d3fd9d20d3343d; sessionid=4131798bcf0ce7b723d3fd9d20d3343d; sessionid_ss=4131798bcf0ce7b723d3fd9d20d3343d; store-idc=alisg; store-country-code=vn; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=sWJlKh8wRR-zGEt7CGAhW1ANspWPFK-TAXrSlW79eOuKw1JABI9XmZp5HHdQD6EfmhWyp4xgxiAnyRt8dhk2u6xyLoV4hOiySsUGSj-YN9quOveqUi2PThmaiOFXDipzuZ5wDkgPvTFSBLoUVCDYow3awCs_x6Dr7iT3THBPpCq9bWyoOPp3Ifx2iOIko7WRJzdw1nE_7LiaBcSiIjBji0X15d7VQ6vHxcbXx0lQMH_ZwObDcpSiOpfcI-UEvk1M-KbaK_8MWDxCGRKnml_aV7cjoFrsEdrsgBB7OXSYqj4k5-tRPf7w7kYfgC-YBHp8_8Aze0wx9t6X1feWMJI7hdV1ZNSgD-P8I6EMQdymQzOdAdSlN_OlGwQMNukTNx_F8-5OI1oyyrGo5Wb2s5Fih6STyUGpUXT6UTS1prvz8UXjd3WDTKIp9gbYyLBYG59BWfnKTrVKbCGZvIj2QL9LE0WVZtts-6zKtYGObIW5rWQJsNJr7njiPBxUh0ZqKjHn; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; sid_guard=4131798bcf0ce7b723d3fd9d20d3343d%7C1741921710%7C15551986%7CWed%2C+10-Sep-2025+03%3A08%3A16+GMT; sid_ucp_v1=1.0.0-KGY4NDEzZDUwODMzYWQzOTAxNGMwYTE3NGEzY2ExYThjODkxODVjOTMKGQiCiKDElICviF0QrrvOvgYYsws4CEASSAQQAxoCbXkiIDQxMzE3OThiY2YwY2U3YjcyM2QzZmQ5ZDIwZDMzNDNk; ssid_ucp_v1=1.0.0-KGY4NDEzZDUwODMzYWQzOTAxNGMwYTE3NGEzY2ExYThjODkxODVjOTMKGQiCiKDElICviF0QrrvOvgYYsws4CEASSAQQAxoCbXkiIDQxMzE3OThiY2YwY2U3YjcyM2QzZmQ5ZDIwZDMzNDNk; passport_fe_beating_status=true; ttwid=1%7C2wg4O3BHdbrcLd8RmPF5OY02fpqcXko9bS5rZ95xBII%7C1741927023%7C61b9f5c3bec454d980035853d1ad060d2885905902d783b2ed49263838d109d7; odin_tt=5045405c39ce7608d3b56fd04d583f3089f763846b3b968080bbfeb230caac2c5074bf0ba26a0f9a624224d73c0afdc62e964c872234b15c615fde8137d1e02d; perf_feed_cache={%22expireTimestamp%22:1741946400000%2C%22itemIds%22:[%227451032548781591826%22%2C%227474958652093369607%22%2C%227470967814237572360%22]}; csrf_session_id=5a0e799593428d590d5e6150347bb94d; msToken=Z06WaPDC-_Cso77UvGlu6JHopI8MHTO_OO-qxiwWGGqnrAfjkRQ_OC7_ajVGaYAzRnVDqbIw2LInu-TqIiAXlJE5t8K3l6S8dEtERMrRd5aI2LBu28Iz0bdxJ_xu0iK6JzZisIwhHw_SK7ZRi6C9FISC; msToken=z54ECPUksCaryFuhRo3XfNYIdJuK_8n0uk0UWKDXPOjHWBMQ76AUT_92ll1YD1-HF_s7MdwfFYgkyfrTJNY0FiuCaPA4PlZ9fAaun2PwZvw4K06j764-22C739KvVUN70si83piDmMGIWPfGHrUfC2Z3",
}

dump_following_params = input(system_color("[!] Truy cập vào tiktok, vào inspector, nhấn vào following, tìm gói \"tiktok.com/api/user/list/...\", nhấn vào query, nhấn vào view source, rồi copy vào đây\n-> "))
def params_raw_to_dict(query_string):
    parsed = parse_qs(query_string)
    # Chuyển từ dict có dạng {key: [value]} về {key: value}
    cleaned_dict = {k: v[0] for k, v in parsed.items()}
    return cleaned_dict

dump_following_params = params_raw_to_dict(dump_following_params)
url = "https://www.tiktok.com/api/user/list/"

def dump_following_list():
    min_cursor = 0
    users = []
    while True:
        dump_following_params['minCursor'] = min_cursor
        r = requests.get(url=url, headers=headers, params=dump_following_params)
        min_cursor = r.json()['minCursor']
        try:
            for user_list in r.json()['userList']:
                users.append(user_list['user']['uniqueId'])
        except:
            break
        
        input(users)
        
        print(success_color(f"[..] Đang dump following list, username cuối list: {users[-1]}, tổng số index: {len(users)}"))

    return users

def main():
    if not os.path.exists("hist_data.json"):
        with open("hist_data.json", "w") as file:
            json.dump({"data":[]}, file)

    cookie = input(system_color("[?] Nhập cookie của bạn\n-> "))
    limit = int(input(system_color("[?] Nhập vào giới hạn lần unfollow\n-> ")))
    print()
    
    headers['cookie'] = cookie
    cookie_name_val = []
    for ck in cookie.split("; "):
        cookie_name_val.append(ck.split("="))

    if str(json.load(open("hist_data.json", "r"))['data']) != "[]":
        inp = input(system_color("[?] Bạn muốn dùng dữ liệu cũ?(Y/n)\n-> "))
        if inp.lower().strip() == "n":
            users = dump_following_list()
            with open("hist_data.json", "w") as file:
                json.dump({"data":users}, file)
        else:
            users = json.load(open("hist_data.json", "r"))['data']
    else:
        users = dump_following_list()
        with open("hist_data.json", "w") as file:
            with open("hist_data.json", "w") as file:
                json.dump({"data":users}, file)

    options = undetected_chromedriver.ChromeOptions()
    chrome_user_data = open("selenium_path.txt").read()
    # options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-popup-blocking")
    options.add_argument(f"--user-data-dir={chrome_user_data}")
    options.add_argument("--mute-audio")
    driver = undetected_chromedriver.Chrome(options=options)
    driver.set_window_size(50, 500)
    driver.set_page_load_timeout(10000)
    
    driver.get("https://www.tiktok.com/")
    for ck in cookie_name_val:
        driver.add_cookie({"name": ck[0], "value": ck[1], "domain": ".tiktok.com", "path": "/"})
    driver.refresh()

    i = 0
    for username in reversed(users):
        driver.get(f"https://www.tiktok.com/@{username}")
        try:
            captcha_audio_btn = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='TUXButton TUXButton--borderless TUXButton--xsmall TUXButton--secondary cap-flex ']")
            ))
            captcha_audio_btn.click()
            
            print(system_color("[>] Phát hiện captcha, tiến hành giải captcha..."))

            audio_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="captcha-verify-container-main-page"]/div[2]/div[1]/audio')
            ))
            audio_url = audio_element.get_attribute("src")

            data = requests.get(audio_url).content
            response = requests.post(API_URL, headers=hgf_headers, data=data)

            text_captcha = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//input[@class="TUXTextInputCore-input"]')
            ))
            text_captcha.send_keys(response.json()['text'])
            
            verify_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//button[@class="TUXButton TUXButton--default TUXButton--medium TUXButton--primary cap-w-full sm:cap-w-auto sm:cap-ml-8 cap-ml-0"]')
            ))
            verify_btn.click()
        except:
            pass

        try:
            unfl_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='TUXButton TUXButton--default TUXButton--medium TUXButton--secondary']")
            ))
            unfl_btn.click()
        except:
            print(error_color("[!] Lỗi khi unfollow, tiếp tục"))
            pass

        if i >= limit:
            break
        else:
            i += 1

        driver.execute_script("window.open();")
        time.sleep(1)
        driver.close()
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        
        try:
            if i % 2 == 0:
                with open("hist_data.json", "w") as file:
                    json.dump({"data":users[:-i]}, file)
        except:
            pass
        print(success_color(f"[#] Đã unfollow {username} ở lần thứ {i}/{limit}"))
    
    input(success_color("[#] Đã hoàn tất\n-> "))

if __name__ == "__main__":
    main()