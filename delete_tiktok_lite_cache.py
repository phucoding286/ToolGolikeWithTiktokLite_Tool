from modules import (
    driver_init,
    capabilities,
    waiting_scroll,
    go_to_my_page,
    error_color,
    success_color
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def delete_cache(driver, adb_path, scroll_to_find_delete_btn=5):
    try:
        profile = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[5]/android.widget.TextView')
            )
        )
        profile.click()

        ba_cham = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.widget.ImageView')
            )
        )
        ba_cham.click()

        setting = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//android.widget.FrameLayout[@content-desc="Trang tính dưới cùng"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView')
            )
        )
        setting.click()
        
        for _ in range(scroll_to_find_delete_btn):
            try:
                delete_cache_btn = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Xóa bộ nhớ đệm"]')
                    )
                )
                delete_cache_btn.click()
                break
            except:
                waiting_scroll(driver, adb_path, 1, "tìm kiếm nút xóa cache...", False)
                continue
        
        time.sleep(1)

        os.system(f'{adb_path} -s {capabilities["udid"]} shell input keyevent 4')

        time.sleep(1)

        os.system(f'{adb_path} -s {capabilities["udid"]} shell input keyevent 4')

        return "success"
    
    except:
        return "error"

if __name__ == "__main__":
    # capabilities['udid'] = "R59R200B92N"
    adb_path = open("adb_path.txt", "r").read()
    driver = driver_init(adb_path, ask_udid=False)
    print(delete_cache(driver, adb_path))