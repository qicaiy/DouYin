#coding=utf-8
import base64
import requests 
import json
from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_token(img):
    APP_ID = ''#百度云appid
    API_KEY = ''#百度云appkey
    SECRET_KEY = ''#百度云secret_key
    auth='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_KEY+'&client_secret='+SECRET_KEY
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        "Content-Type": "application/json"
    }
    try:
        res=requests.get(auth,headers=header)
        json_res=json.loads(res.text)
        access_token=json_res['access_token']
        url='https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+access_token
        header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        "Content-Type": "application/json"
        }
        data={
        'image':img,
        "face_field":"age,beauty,expression,face_shape,gender,glasses,emotion,face_type,spoofing",
        'image_type':'BASE64'
        }
        res=requests.post(url,data=data,headers=header)
        json_res=json.loads(res.text)
        res.close()
        try:
            颜值=json_res['result']['face_list'][0]['beauty']
            sex=json_res['result']['face_list'][0]['gender']['type']
            if(sex=='male'):
                return 'male'
            else:
                return 颜值
        except Exception:
            return False
    except Exception:
        return False
    
    

def start_chrome():
    #打开浏览器
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome('chromedriver.exe',options=option)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => false})"""})
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"}})
    browser.get("https://www.douyin.com/?enter=guide")
    sleep(3)
    print("请扫描登录")
    sleep(10)
    count=1
    while True:
        while True:
            ex=False
            颜值=get_token(browser.get_screenshot_as_base64())
            if(int(count)<=int(5)):
                print('开始第:'+str(count)+'/5次')
                if(颜值==False):
                    print("颜值检测失败")
                    browser.get_screenshot_as_file('error.png')
                    count+=1
                    continue
                elif(颜值=='male'):
                    print('检测为男性')
                    count+=1
                    continue
                elif(颜值 >=50):
                    print("颜值达标，分数:"+str(颜值))
                    browser.get_screenshot_as_file('success.png')
                    try:
                        browser.find_element(By.CLASS_NAME,value='HNBvVrcV').click()
                    except Exception:
                        print("点赞失败")
                    count=10
                else:
                    print("颜值不达标")
                    browser.get_screenshot_as_file('ban.png')
                    count+=1
                    continue
            else:
                try:
                    count=1
                    print("开始下一个视频检测")
                    browser.find_element(By.CSS_SELECTOR,value='#slidelist > div.swiper-container.swiper-container-initialized.swiper-container-vertical.swiper-container-autoheight.qRePWKBJ.fullscreen_capture_feedback > div.swiper-wrapper > div.swiper-slide.ARBi5fd6.swiper-slide-active > div > div.KXURcZ2l.playerContainer.P8fJYYpG > div > div > div.L1TH4HdO > div.xgplayer-playswitch.yCNzfa5z.immersive-player-switch-on-hide-interaction-area > div > div > div.xgplayer-playswitch-next').click()
                except Exception:
                    print("滑动下一个失败")

if '__main__' == __name__:
    start_chrome()
