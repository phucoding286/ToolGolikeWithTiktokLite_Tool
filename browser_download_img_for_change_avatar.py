from modules import *

print(system_color("[>] Thu thập ảnh cho change profile tự động tiktok lite"))
print(system_color("[?] Đây là công cụ khi bạn tải bất kỳ file nào, file đó sẽ đi vào trong folder chứa ảnh mà tôi dùng để up lên tiktok để nuôi acc."))
print(system_color("[!] Bạn lưu ý, hãy chỉ tải các file ảnh, tool đã gợi ý vào trang pinterest bạn có thể vào đó và khám phá, nếu bạn muốn acc tiktok mà tool chạy được bot xây như 1 kênh thật."))

download_folder = os.path.abspath("./img_for_change_avatar_for_golike_tool_by_phu")

options = selenium_webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,          # Không hỏi khi tải
    "download.directory_upgrade": True,             # Cho phép thay đổi thư mục
    "safebrowsing.enabled": True                    # Tránh Chrome chặn file
})
options.add_argument("--user-data-dir=" + open("./selenium_path.txt").read())

driver = selenium_webdriver.Chrome(options=options)
driver.get("https://www.pinterest.com/")
input(system_color("Nhấn vào đây để thoát chrome an toàn hơn\n-> "))
driver.quit()