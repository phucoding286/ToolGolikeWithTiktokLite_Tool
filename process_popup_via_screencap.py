from modules import *

vocab = {
    "a": list("áàảãạăắằẳẵặâấầẩẫậ"),
    "e": list("éèẻẽẹêếềểễệ"),
    "i": list("íìỉĩị"),
    "o": list("óòỏõọôốồổỗộơớờởỡợ"),
    "u": list("úùủũụưứừửữự"),
    "y": list("ýỳỷỹỵ")
}

def detect_popup(img1, img2):
    str_detected = pytesseract.image_to_string(img1).splitlines()
    str_detected += pytesseract.image_to_string(img2).splitlines()
    for i in range(len(str_detected)):
        for key, value in vocab.items():
            for char in value:
                str_detected[i] = str_detected[i].replace(char, key)

    # print(str_detected)
    
    if "Dang xuat?" in str_detected:
        return "Đăng xuất?"
    
    elif 'Luu thong tin dang nhap?' in str_detected or 'Luu theng tin dang nhap?' in str_detected:
        return "Lưu thông tin đăng nhập?"
    
    elif "Follow ban be cua ban" in str_detected:
        return "Follow bạn bè của bạn"
    
    elif "Them ban be, dung TikTok t" in str_detected:
        return "Thêm bạn bè, dùng Tiktok t"
    
    elif "Deng be danh sach ban be" in str_detected:
        return "Đồng bộ danh sách bạn bè"

    elif "Them ban be, dung TikTok" in str_detected:
        return "Thêm bạn bè, dùng TikTok"
    
    elif "Trang thai tai knoan" in str_detected:
        return "Trạng thái tài khoản"
    
    elif "tren TikTok, hay cho phep tru" in str_detected:
        return "trên Tiktok, hãy cho phép tru"
    
    elif "Khdeng cho phep" in str_detected or "Kheng cho phep" in str_detected:
        return "Không cho phép"

def popup_processing(): 
    image = cv2.imread("./screenshot.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    image = Image.open("./screenshot.png")
    return detect_popup(gray, image)

def screencap(adb_path, device_id):
    os.system(f'{adb_path} -s {device_id} shell screencap /storage/emulated/0/Download/screenshot.png')
    os.system(f'{adb_path} -s {device_id} pull /storage/emulated/0/Download/screenshot.png ./screenshot.png')

if __name__ == "__main__":
    screencap(open("adb_path.txt").read(), "192.168.1.56:5555")
    print(popup_processing())