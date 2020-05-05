import os, json, selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep



#            初期設定            #

# chromeのプロファイルパス　※無い場合は空のファイルを作成
PROFILEPATH = 'userdata'
# メルカリデータパス　ここに監視する商品を登録する
MERCARIDATAPATH = 'data/mercari_selling.json'



options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + PROFILEPATH)
driver = webdriver.Chrome(options=options)

def FIND_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute('class')

def FIND_CSS_SELECTOR(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, name)))
    return driver.find_element_by_css_selector(name).text

def MONORATE(asin):
    if len(asin) != 10:
        print('ASINが正しく指定されていません。')
        return False
    driver.get('https://mnrate.com/item/aid/'+asin)
    return FIND_CSS_SELECTOR('.price.used_price_color._btn_size_style.item_conditions_data_box')

def BOT(data):
    driver.get(data)
    mer_slt_status   = FIND_CLASS_NAME('item-buy-btn')
    mer_slt_price    = FIND_CLASS_NAME('item-price')
    mer_slt_price    = mer_slt_price.replace('¥','').replace(',','')

    if 'disabled' in mer_slt_status:
        # 売り切れた場合
        return 'soldOut'

    mnrate_low_price = MONORATE(mer_slt_d['asin'])
    mnrate_low_price = mnrate_low_price.replace('￥','').replace(',','')

    if mer_slt_price > mnrate_low_price:
        # 金額がモノレート最低金額よりも高くなった場合
        return 'than{}'.format(int(mer_slt_price)-int(mnrate_low_price))
    
    if mer_slt_price < mnrate_low_price:
        # 金額がモノレート最低金額よりも低くなった場合
        return 'down{}'.format(int(mnrate_low_price)-int(mer_slt_price))

    if mer_slt_price == mnrate_low_price:
        # 金額が同じ場合
        return 0


if __name__=='__main__':
    with open(MERCARIDATAPATH, 'r') as f:
        mer_sel_d = json.load(f)

    for mer_slt_d in mer_sel_d:

        bot_result = BOT(mer_slt_d['href'])
        if bot_result == 'soldOut':
            print('売り切れ')
        elif 'than' in bot_result:
            than_amount = bot_result.replace('than','')
            print('モノレートよりも{}円高い'.format(than_amount))
        elif 'down' in bot_result:
            down_amount = bot_result.replace('down','')
            print('モノレートよりも{}円低い')
        elif not bot_result:
            print('モノレートと同じ金額')

    driver.close()