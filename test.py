import os, json, random, string, selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep

PROFILEPATH = 'userdata'

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + PROFILEPATH)
driver = webdriver.Chrome(options=options)

def FIND_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute('class')

def FIND_TEXT_BY_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute("textContent")

def FIND_TEXT_BY_CSS_SELECTOR(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, name)))
    return driver.find_element_by_css_selector(name).get_attribute("textContent")


driver.get("https://www.mercari.com/jp/items/"+'m43995817534')

mer_slt_status   = FIND_CLASS_NAME('item-buy-btn')
mer_slt_price    = FIND_TEXT_BY_CLASS_NAME('item-price')
mer_slt_price    = mer_slt_price.replace('¥','').replace(',','')
print(mer_slt_price)