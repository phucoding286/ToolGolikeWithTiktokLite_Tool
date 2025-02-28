from modules import *

def get_devices(adb_path):
    result = subprocess.run(
        ["cmd", "/c", adb_path + " devices"],
        capture_output=True,
        text=True
    )
    device_list = result.stdout.split(
        "List of devices attached\n"
    )[1].split("\n\n")[0].splitlines()

    for i in range(len(device_list)):
        device_name_preprocessed = device_list[i].split()[0]
        device_list[i] = device_name_preprocessed

    return device_list

if __name__ == "__main__":
    print(get_devices(r"E:\Android\Sdk\platform-tools\adb.exe"))