from modules import *
from get_device_id import get_devices

adb_path = open("adb_path.txt", "r").read()

while True:
    devices = get_devices(adb_path)
    for device in devices:
        output = subprocess.check_output(f"{adb_path} -s {device} shell dumpsys battery", shell=True, text=True)
        temp = output.split("temperature: ")[1].split()[0]
        float_part = temp[-1]
        temp = temp[:-1]
        temp += "." + float_part
        print(f"Thiết bị: {device}, Nhiệt độ pin: {temp}°C")
    time.sleep(15)
    os.system("cls") if sys.platform.startswith("win") else os.system("clear")