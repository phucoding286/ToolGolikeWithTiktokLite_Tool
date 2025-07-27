from get_device_id import get_devices
from modules import *

adb_path = open("adb_path.txt").read()
for device in get_devices(adb_path):
    os.system(f"{adb_path} -s {device} shell wm size reset")
    os.system(f"{adb_path} -s {device} shell wm density reset")