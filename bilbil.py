#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: jiajia
@file: bilbil.py
@time: 2020/8/22 18:48
"""
#!/usr/bin/env python
import re
import time
import base64

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import mode_one



def to_selenium(res):
    place = []
    title = [i['content'] for i in res if i['classes'] == "title"][0]
    for t in title:
        for item in res:
            if item['classes'] == "target":
                x1, y1, x2, y2 = item['crop']
                if item['content'] == t:
                    place.append(
                        {
                            "text": t,
                            "place": [(x1 + x2)/2, (y1 + y2)/2]
                        }
                    )
    return place


class BilBil(object):
    def __init__(self):
        chrome_options = self.options()
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 30)
        self.url = "https://passport.bilibili.com/login"
        self.ture = 0

    def __del__(self):
        self.browser.close()

    def options(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # mobile_emulation = {"deviceName": "iPhone 6"}
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return chrome_options

    def click(self, xpath):
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath))).click()

    def bibi(self):
        url = "https://passport.bilibili.com/login"
        self.browser.get(url)
        xpath = '//*[@id="login-username"]'
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath))).send_keys('Python')
        xpath = '//*[@id="login-passwd"]'
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath))).send_keys('Python')
        xpath = '//*[@id="geetest-wrap"]/div/div[5]/a[1]'
        self.click(xpath)

        xpath = '/html/body/div[2]/div[2]/div[6]/div/div/div[2]/div[1]/div/div[2]/img'
        logo = self.wait.until(EC.presence_of_element_located(
        (By.XPATH, xpath)))
        f = logo.get_attribute('src')
        if f:
            res = requests.get(f)
            res = res.content
            with open(f"bilbil.jpg", 'wb') as f:
                f.write(res)
        res = mode_one.run_click("bilbil.jpg")
        plan = to_selenium(res)
        X, Y = logo.location['x'], logo.location['y']
        print(X, Y)
        lan_x = 259/334
        lan_y = 290/384
        for p in plan:
            x, y = p['place']
            ActionChains(self.browser).move_by_offset(X-40 + x*lan_x, Y + y*lan_y).click().perform()
            ActionChains(self.browser).move_by_offset(-(X-40 + x*lan_x), -(Y + y*lan_y)).perform()  # 将鼠标位置恢复到移动前
            time.sleep(0.5)

        xpath = "/html/body/div[2]/div[2]/div[6]/div/div/div[3]/a/div"
        self.click(xpath)

        print(res)
        print(plan)
        print("".join([i['text']for i in plan]))
        time.sleep(100)


if __name__ == '__main__':
    import time
    start = time.time()
    jd = BilBil()
    jd.bibi()
    print(time.time() - start)