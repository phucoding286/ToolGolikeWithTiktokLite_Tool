from golike import check_tiktok_account_id
import multi_devices
multi_devices.GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
multi_devices.GOLIKE_HEADERS["t"] = open("t.txt", "r").read()
from multi_devices import GOLIKE_HEADERS
from modules import *

for character in "TOOL BY HOANG PHU : tool được viết bởi Phú":
    print(system_color(character), end="", flush=True)
    time.sleep(0.02)
print()

print(wait_color("[..] Đang dump list account tiktok trong golike."))
check_response = check_tiktok_account_id(None)
print(success_color(f"[*] Dump thành công, số tài khoản là -> {len(check_response)}"))
print(wait_color(f"[..] Đợi để chạy tool check dead/live account tiktok"))

for account in check_response:
    aid, auname = account[0], account[1]
    
    # try 2 times
    is_dead: bool = False
    for _ in range(2):
        response = scraper.get(f"https://www.tiktok.com/@{auname}")
        if len(response.text.split("followingCount\":")) <= 1:
            time.sleep(2)
            is_dead = True
            continue
        else:
            is_dead = False
            break

    if is_dead:
        print(error_color(f"[!] Username tiktok: {auname}, Đã dead!"))
    else:
        print(success_color(f"[*] Username tiktok: {auname}, Vẫn còn hoạt động."))

    time.sleep(2)

print()

input(system_color("[>] Enter để đóng\n-> "))
exit()