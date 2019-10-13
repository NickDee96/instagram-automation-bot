from bs4 import BeautifulSoup as soup
from selenium import webdriver
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import pandas as pd
import random

df=pd.read_csv("furniturepalacedata.csv")
cookie="INSERT YOUR INSTAGRAM COOKIE HERE"
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")            
driver=webdriver.Firefox(executable_path = 'C:\\geckodriver\\geckodriver.exe',firefox_profile=profile)
driver.get('https://www.instagram.com/accounts/login')
driver.add_cookie({
    "name": "sessionid",
    "value": cookie,
    "domain":".instagram.com"
})
driver.get('https://www.instagram.com')


page=soup(driver.execute_script("return document.body.innerHTML"),'lxml')
cId=page.findAll("div",{"role":"dialog"})[-1].findAll("button")[1]["class"][0]
csSelector="button.{}:nth-child(2)".format(cId)
driver.find_element_by_css_selector(csSelector).click()


# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
def scroll(driver):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
            elif lastCount>21000:
                match=True
    return driver


def followBtn(driver):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "button"))
    )
    state=element.text
    if state=="Message":
        pass
    else:
        driver.find_elements_by_tag_name("button")[0].click()
        driver.find_element_by_tag_name("h1").click()
    return driver

driver.find_elements_by_tag_name("button")[0].text

j=0
length=3

def likeMessage(driver,length):
    elements = driver.find_elements_by_class_name("FFVAD")
    ac = ActionChains(driver)
    #ac.send_keys(Keys.SPACE).perform()
    for j in range(length):
        ac.move_to_element(elements[j]).move_by_offset(0, 0).click().perform()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "glyphsSpriteHeart__outline__24__grey_9"))
        )
        #driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span').click()
        element.click()
        driver.back()

def check_suggested(driver):
    if len(driver.find_elements_by_class_name("Rebts"))>=0:
        ac = ActionChains(driver)
        ac.send_keys(Keys.SPACE).perform()
    else:
        pass


        

def ranTime():
   t=random.choice(range(40,80))
   return t

for i in range(50,len(df.profileUrl)):
    try:
        driver.get(df.profileUrl[i])
        time.sleep(3)
        driver=followBtn(driver)
        time.sleep(1)
        check_suggested(driver)
        likeMessage(driver,3)
        time.sleep(20)
        print(df.profileUrl[i])
    except IndexError:
        time.sleep(20)
        pass

