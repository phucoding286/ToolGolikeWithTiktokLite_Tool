from modules import *

def detect_popup(img):
    str_detected = pytesseract.image_to_string(img).splitlines()
    print(str_detected)
    if "Dang xuat?" in str_detected:
        return "Đăng xuất?"
    
    elif 'Luu thong tin dang nhap?' in str_detected:
        return "Lưu thông tin đăng nhập?"
    
    elif "Follow ban be cua ban" in str_detected:
        return "Follow bạn bè của bạn"
    
    elif "Thém ban bé, dung TikTok t" in str_detected:
        return "Thêm bạn bè, dùng Tiktok t"

def popup_processing(): 
    img = Image.open(r"./screenshot.png")
    return detect_popup(img)

def screencap(adb_path, device_id):
    os.system(f'{adb_path} -s {device_id} shell screencap /storage/emulated/0/Download/screenshot.png')
    os.system(f'{adb_path} -s {device_id} pull /storage/emulated/0/Download/screenshot.png ./screenshot.png')

if __name__ == "__main__":
    screencap(open("adb_path.txt").read(), "192.168.1.4:5555")
    print(popup_processing())