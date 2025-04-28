from modules import *
from golike import check_tiktok_account_id
import golike

for character in "TOOL BY HOANG PHU : tool được viết bởi Phú":
    print(system_color(character), end="", flush=True)
    time.sleep(0.02)
print()

golike.GOLIKE_HEADERS['authorization'] = open("auth.txt", "r").read()
golike.GOLIKE_HEADERS["t"] = open("t.txt", "r").read()

def check_follow_count(username, limit=1000):
    r = scraper.get(f"https://tiktok.com/@{username}")
    fl_count = r.text.split("followingCount\":")[1].split(",")[0]
    if int(fl_count) >= limit:
        return True, f"username {username} | {fl_count} following."
    else:
        return False, f"username {username} | {fl_count} following."

def main():
    limit = int(input(system_color("[?] Nhập vào số lượng limit following mà bạn muốn\n-> ")))
    print()
    print(system_color("[..] Đang xử lý"))
    rchk = check_tiktok_account_id(None)
    true_list, false_list = [], []
    for t in rchk:
        r = check_follow_count(t[1], limit)
        if r[0] is True:
            true_list.append(r[1])
        else:
            false_list.append(r[1])
    
    print(error_color(f"[#] Các username có số lượng following trên {limit}:"))
    for u in true_list:
        print(error_color("    "+u))
    print()
    print(success_color(f"[#] Các username có số lượng following dưới {limit}:"))
    for u in false_list:
        print(success_color("    "+u))
    
if __name__ == "__main__":
    main()