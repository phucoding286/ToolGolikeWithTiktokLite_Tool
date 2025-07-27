from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
import cloudscraper
import json
import os
import colorama
import time
import random
import subprocess
import threading
import pytesseract
from PIL import Image
import sys
import cv2
import requests
from selenium import webdriver as selenium_webdriver
import undetected_chromedriver

colorama.init()
pytesseract.pytesseract.tesseract_cmd = open("./tesseract_path.txt").read()
scraper = cloudscraper.create_scraper()
prices = 0

# make color for logs
def error_color(string: str):
    return colorama.Fore.RED + str(string) + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + str(string) + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + str(string) + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + str(string) + colorama.Style.RESET_ALL
def purple_color(string: str):
    return colorama.Fore.MAGENTA + str(string) + colorama.Style.RESET_ALL


capabilities = {
  "udid": "351a9fc",
  "platformName": "Android",
  "appPackage": "com.zhiliaoapp.musically.go",
  "appActivity": "com.ss.android.ugc.aweme.main.homepage.MainActivity",
  "noReset": True
}


def driver_init(adb_path, ask_udid=True, device_id=None, appium_port=None):
    for retry in range(5):
        try:
            requests.get("https://www.google.com/", timeout=2)
            break
        except:
            time.sleep(1)
            continue
    else:
        input("[!] Lỗi mạng >>> ")

    appium_server_url = f"http://localhost:{appium_port}/wd/hub"

    if ask_udid:
        os.system(adb_path + " devices")
        udid_inp = input(system_color("[?] Nhập vào udid máy của bạn\n-> "))
        capabilities['udid'] = udid_inp

    elif device_id is not None:
        capabilities['udid'] = device_id
    
    error = False
    while True:
        try:

            if len(capabilities['udid'].split(".")) >= 3 and error:
                os.system(adb_path + " connect " + capabilities['udid'])

            driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
            time.sleep(2)
            waiting_scroll(driver, adb_path, 1, f"scroll sau khi tạo lại driver", False, device_id=device_id, appium_port=appium_port)
            
            error = False
            break

        except Exception as e:
            # print(e)
            try:
                driver.quit()
            except:
                pass
            print(error_color(f"[Device: {device_id}] [!] Lỗi khi tạo driver, thử lại..."))
            error = True
    
    driver.execute_script('mobile: shell', {
        'command': 'wm',
        'args': ['size', '720x1280']
    })

    driver.execute_script('mobile: shell', {
        'command': 'wm',
        'args': ['density', '320']
    })
    return driver

def go_to_my_page(username, adb_path):
    try:
        os.system(f'{adb_path} -s {capabilities["udid"]} shell am start -a android.intent.action.VIEW -d "https://www.tiktok.com/@{username}" com.zhiliaoapp.musically.go')
        return {"success": "Đã đến trang cá nhân thành công"}
    except:
        return {"error": "đã có lỗi khi đi đến trang cá nhân"}


# make waiting animation theme
def waiting_ui(timeout=5, text="", device_id=None):
    for i in range(1, timeout+1):
        print(colorama.Fore.YELLOW + f"\r[Device: {device_id}] [{i}s] " + colorama.Style.RESET_ALL, end="")
        print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0

def waiting_scroll(driver: webdriver.Remote, adb_path, times_scroll=0, text="", rdn_options=True, recreate_driver=True, device_id=None, appium_port=None, watch_user_video=False):
    width, height = 0, 0
    for i in range(1, times_scroll+1):

        tim_desicion = random.choice([False for _ in range(20)] + [True] + [False for _ in range(20)])
        if tim_desicion and rdn_options:
            try:
                os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 350}")
                
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.ID, 'com.zhiliaoapp.musically.go:id/dm4')
                    )
                ).click()
                print(success_color(f"[Device: {device_id}] [#] Đã thực hiện tim video"))
                os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 350}")
            except:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.ID, 'com.zhiliaoapp.musically.go:id/dmb')
                        )
                    ).click()
                    print(success_color(f"[Device: {device_id}] [#] Đã thực hiện tim video"))
                    os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 350}")
                except:
                    print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi tim video"))
        else:
            if rdn_options:
                print(system_color(f"[Device: {device_id}] [00] Không chọn thực hiện tim"))

        if rdn_options:
            print(f"[Device: {device_id}] [...] Thực hiện thời gian xem ngẫu nhiên")
        
        wait_times_ = 0
        while True and rdn_options:
            n_false, n_true = random.randint(1, 2), random.randint(1, 2)
            false_list = [False for _ in range(n_false)]
            true_list = [True for _ in range(n_true)]
            low_val_for_randn = random.uniform(0.5, 0.8)
            high_val_for_randn = random.uniform(0.9, 1.2)
            if random.choice(false_list + true_list):
                time_wait_beforce_scroll = random.choice([low_val_for_randn, high_val_for_randn])
                print(system_color(f"[Device: {device_id}] [>] Xem tiếp {time_wait_beforce_scroll}s..."))
                time.sleep(time_wait_beforce_scroll)
                wait_times_ += 1
                continue
            else:
                if wait_times_ < 2: continue
                print(system_color(f"[Device: {device_id}] [#] Lướt xem video mới."))
                break
        
        try:
            driver.activate_app(capabilities['appPackage'])
            
            size = driver.get_window_size()
            width = size['width']
            height = size['height']
            
            driver.swipe(start_x=width/2, start_y=height/2, end_x=width/2, end_y=0, duration=500)
            print(colorama.Fore.YELLOW + f"[Device: {device_id}] [{i}-scroll] " + colorama.Style.RESET_ALL, end="")
            print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL)

        except:
            if recreate_driver:
                driver = driver_init(adb_path, False, device_id, appium_port)
                waiting_ui(5, "Lỗi driver, đợi 5s để tiếp tục scroll", device_id)
            else:
                return "lỗi khi scroll"
            
    if watch_user_video: os.system(adb_path + f" -s {device_id}" + f" shell input tap {width/2} {(height / 2) - 350}")
    return driver