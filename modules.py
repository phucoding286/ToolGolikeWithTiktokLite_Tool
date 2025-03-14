from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
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

def waiting_scroll(driver, adb_path, times_scroll=0, text="", rdn_options=True, recreate_driver=True, device_id=None, appium_port=None):
    for i in range(1, times_scroll+1):

        if random.choice([True]+[False for _ in range(10)]) and rdn_options:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.ID, 'com.zhiliaoapp.musically.go:id/dm4')
                    )
                ).click()
                print(success_color(f"[Device: {device_id}] [#] Đã thực hiện tim video"))
            except:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.ID, 'com.zhiliaoapp.musically.go:id/dmb')
                        )
                    ).click()
                except:
                    print(error_color(f"[Device: {device_id}] [!] Đã có lỗi khi tim video"))
        else:
            if rdn_options:
                print(system_color(f"[Device: {device_id}] [00] Không chọn thực hiện tim"))

        if rdn_options:
            print(f"[Device: {device_id}] [...] Thực hiện thời gian xem ngẫu nhiên")
            
        while True and rdn_options:
            if random.choice([False]+[True for _ in range(2)]):
                print(system_color(f"[Device: {device_id}] [>] Xem tiếp 2s..."))
                time.sleep(2)
                continue
            else:
                print(system_color(f"[Device: {device_id}] [#] Lướt xem video mới."))
                break
        
        try:

            size = driver.get_window_size()
            width = size['width']
            height = size['height']
            driver.swipe(start_x=width/2, start_y=height/2, end_x=width/2, end_y=0, duration=500)

            print(colorama.Fore.YELLOW + f"[Device: {device_id}] [{i}-scroll] " + colorama.Style.RESET_ALL, end="")
            print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL)
            time.sleep(1)

        except:
            if recreate_driver:
                driver = driver_init(adb_path, False, device_id, appium_port)
                waiting_ui(5, "Lỗi driver, đợi 5s để tiếp tục scroll", device_id)
            else:
                return "lỗi khi scroll"
        
    return driver