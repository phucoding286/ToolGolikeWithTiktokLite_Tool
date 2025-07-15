from modules import *
from get_device_id import get_devices

adb_path = open("adb_path.txt", "r").read()

print("*Lưu ý: Vui lòng đăng nhập trước tài khoản của bạn trên thiết bị.")
for device in get_devices(adb_path):
    print(device)

print()
device_id = input("Nhập device phía trên mà bạn muốn: ")
appium_port = input("Nhập appium port: ")

driver = driver_init(
    adb_path,
    ask_udid=False,
    device_id=device_id,
    appium_port=appium_port
)

while True:
    driver = waiting_scroll(
        driver, adb_path, times_scroll=10, text="Scroll 10 lần",
        device_id=device_id, appium_port=appium_port
    )