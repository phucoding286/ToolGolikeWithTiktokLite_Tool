from modules import *

# make color for logs
def error_color(string: str):
    return colorama.Fore.RED + str(string) + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + str(string) + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + str(string) + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + str(string) + colorama.Style.RESET_ALL
def purple_color(string: str):
    return colorama.Fore.MAGENTA + str(string) + colorama.Style.RESET_ALL

# headers for golike account
GOLIKE_HEADERS = {
        "authority": "gateway.golike.net",
        "scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "", # authorization golike (add later)
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "gateway.golike.net",
        "Origin": "https://app.golike.net",
        "Referer": "https://app.golike.net/",
        "sec-ch-ua": "Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "t": "", # token golike (add later)
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)"
    }


# get job from golike
def get_job(account_id, device_id=None):
    try:

        # requests for get job
        get_job = scraper.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/tiktok/jobs?account_id={account_id}&data=null",
            headers=GOLIKE_HEADERS
        )
        gjj = get_job.json()

        # if status code is 400 inference it's end jobs
        if gjj['status'] == 400:
            raise ValueError(error_color(f"[Device: {device_id}] Đã hết job để làm, chờ load lại sau."))
        # else get needed data
        insta_link = gjj['data']['link']
        golike_user_id = gjj['data']['id']
        task_type = gjj['data']['type']
        object_id = gjj['data']['object_id']
        
        price_per_after_cost = gjj['data']['price_per_after_cost']
        if int(price_per_after_cost) < 42:
            return {"<42": "Thu nhập nhỏ hơn 42d"}
        else:
            print(success_color(f"[Device: {device_id}] Job hợp lê, thu nhập lớn hơn hoặc bằng 42d"))

        return insta_link, golike_user_id, task_type, object_id, {"status_code": gjj['status'], 'status': gjj['success']}
    
    except Exception as e:
        print(e)
        return {"error": "có lỗi khi nhận job, có thể do hết job"}



# drop job from golike when error
def drop_job(ads_id, object_id, account_id, task_type, device_id=None):
    for i in range(5):
        try:
            response = scraper.post(
                url="https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs",
                headers=GOLIKE_HEADERS,
                json={"account_id": account_id, "ads_id": ads_id, "object_id": object_id, "type": task_type}
            )

            if response.status_code == 200:
                return {"success": "đã bỏ job thành công"}
            else:
                print(error_color(f"[Device: {device_id}] [!] đã có lỗi khi bỏ job, thử lại..."))
                time.sleep(1)
                continue
        except:
            print(error_color(f"[Device: {device_id}] [!] đã có lỗi khi bỏ job, thử lại..."))
            time.sleep(1)
            continue
    return {"error": "đã có lỗi khi bỏ job"}



# verify job on golike when complete task for get money
def verify_complete_job(ads_id, account_id, device_id=None):
    global prices
    for i in range(5):
        try:
            complete_job = scraper.post(
                url="https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs",
                headers=GOLIKE_HEADERS,
                json={"async": True, "captcha": "recaptcha", "data": None, "account_id": account_id, "ads_id": ads_id, "data": None}
            )
            c = complete_job.json()
            prices += c['data']['prices']
            return (c['status'], f"trạng thái [{c['status']}] -> {'thành công' if c['success'] else 'không thành công'}", f"tiền công -> {c['data']['prices']}đ")
        except:
            print(error_color(f"[Device: {device_id}] [!] đã có lỗi khi xác minh job, thử lại..."))
            time.sleep(1)
            continue
    return {"error": f"đã có lỗi khi xác minh hoàn thành job"}
  


# check instagram accounts linking on golike
def check_tiktok_account_id(device_id=None):
    while True:
        try:
            response = scraper.get(
                url="https://gateway.golike.net/api/tiktok-account",
                headers=GOLIKE_HEADERS
            )
            resj = response.json()

            insta_id = [
                (insta_account_id['id'], insta_account_id['unique_username'])
                for insta_account_id in resj['data']
            ]
            return insta_id
        except Exception as e:
            print(e)
            print(error_color(f"[Device: {device_id}] lỗi không xác định đã xảy ra khi gửi yêu cầu nhận về list account id, thử lại"))
            continue