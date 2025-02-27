from modules import *

def manual_send_keys(adb_path, text: str, enter=False, device_id=None):
    os.system(f'{adb_path} -s {device_id}  shell input text "{text}"')
    time.sleep(1)
    if enter:
        os.system(f'{adb_path} -s {device_id}  shell input keyevent 66')


def follow(driver, adb_path="adb", target_link="https://tiktok.com/@example/", device_id=None):

    try:
        
        time.sleep(2)
        kham_pha_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView")
            )
        )
        kham_pha_btn.click()

        find_cell = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Tìm kiếm"]')
            )
        )
        find_cell.click()

        manual_send_keys(adb_path, target_link.split("/")[3], True, device_id)

        user_finded_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.bytedance.ies.xelement.viewpager.childitem.LynxTabbarItem[2]")
            )
        )
        user_finded_list.click()
        
        for _ in range(5):
            try:
                follow_btn = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '(//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Follow"])[1]')
                    )
                )
                break
            except:
                time.sleep(1)
                continue
        
        try:
            xml_src = driver.page_source
            top_username = xml_src.split("desc=\"")[39].split("\" checkable")[0]
            if top_username != target_link.split("/")[3].replace("@", ""):
                return "!=username"
        except:
            pass
        
        time.sleep(1)

        follow_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Follow"])[1]')
            )
        )
        time.sleep(1)
        follow_btn.click()
        
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')
        
        exit_btn2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/com.lynx.component.svg.UISvg")
            )
        )
        time.sleep(1)
        exit_btn2.click()
        
        time.sleep(1)
        os.system(f'{adb_path} -s {device_id} shell input keyevent 4')

        return {"success": "Follow thành công!"}
    
    except:
        return {"error": "Đã có lỗi khi follow"}
    
if __name__ == "__main__":
    # capabilities['udid'] = "R59R200B92N"
    driver = driver_init(r"E:\Android\Sdk\platform-tools\adb.exe", False)
    print(follow(driver, adb_path=r"E:\Android\Sdk\platform-tools\adb.exe", target_link="https://www.tiktok.com/@kekdjdjd"))
    time.sleep(5)