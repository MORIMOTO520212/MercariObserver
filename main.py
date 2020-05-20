import os, json, selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep

with open('setting.json', 'r') as f: # 設定ファイル読み込み
    setting = json.load(f)


#            初期設定            #

# chromeのプロファイルパス　※無い場合は空のファイルを作成
PROFILEPATH = 'userdata'
# メルカリデータパス　ここに監視する商品を登録する
MERCARIDATAPATH = setting['mercari_selling']



options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + PROFILEPATH)
driver = webdriver.Chrome(options=options)

def FIND_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute('class')

def FIND_TEXT_BY_CSS_SELECTOR(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, name)))
    return driver.find_element_by_css_selector(name).text

def MONORATE(asin):
    if len(asin) != 10:
        print('ASINが正しく指定されていません。')
        return False
    driver.get('https://mnrate.com/item/aid/'+asin)
    return FIND_TEXT_BY_CSS_SELECTOR('.price.used_price_color._btn_size_style.item_conditions_data_box')


def BOT(data):
    driver.get("https://www.mercari.com/jp/items/"+data)
    mer_slt_status   = FIND_CLASS_NAME('item-buy-btn')
    mer_slt_price    = FIND_CLASS_NAME('item-price')
    mer_slt_price    = mer_slt_price.replace('¥','').replace(',','')

    if 'disabled' in mer_slt_status: # 売り切れた場合
        return 'soldOut'

    mnrate_low_price = MONORATE(mer_slt_d['asin'])
    mnrate_low_price = mnrate_low_price.replace('￥','').replace(',','')

    if mer_slt_price > mnrate_low_price: # 金額がモノレート最低金額よりも高くなった場合
        return 'than{}'.format(int(mer_slt_price)-int(mnrate_low_price)) # この時点で削除
    
    if mer_slt_price < mnrate_low_price: # 金額がモノレート最低金額よりも低くなった場合
        return 'down{}'.format(int(mnrate_low_price)-int(mer_slt_price))

    if mer_slt_price == mnrate_low_price: # 金額が同じ場合
        return 0 # この時点で削除


if __name__=='__main__':
    with open(MERCARIDATAPATH, 'r') as f:
        mer_sel_d = json.load(f)

    for mer_slt_d in mer_sel_d:
        mercariId = mer_slt_d['mercariId'] # mercariId - DictData

        if mer_slt_d['status']!='soldout':
            bot_result = BOT(mercariId) # スクレイピングで商品の状態を確認する

            if bot_result == 'soldOut':
                print('MercariID:{} 売り切れ'.format(mercariId))

            elif 'than' in bot_result:
                than_amount = bot_result.replace('than','')
                print('MercariID:{} モノレートよりも{}円高い'.format(mercariId, than_amount))

            elif 'down' in bot_result:
                down_amount = bot_result.replace('down','')
                print('MercariID:{} モノレートよりも{}円低い'.format(mercariId, down_amount))

            elif not bot_result:
                print('MercariID:{} モノレートと同じ金額'.format(mercariId))
        else:
            print('MercariID:{} 売り切れ'.format(mercariId))

    driver.close()