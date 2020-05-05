# メルカリの商品を監視に登録します。

import os, json, random, string, selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
jsonData = {}

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


print('- 入力に困った場合はhelpでヒントを閲覧できます。 -')


def randomId():
       return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def FIND_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute('class')

def FIND_TEXT_BY_CLASS_NAME(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
    return driver.find_element_by_class_name(name).get_attribute("textContent")

def FIND_TEXT_BY_CSS_SELECTOR(name):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, name)))
    return driver.find_element_by_css_selector(name).text

def MONORATE(asin):
    if len(asin) != 10:
        print('ASINが正しく指定されていません。')
        return False
    driver.get('https://mnrate.com/item/aid/'+asin)
    return FIND_TEXT_BY_CSS_SELECTOR('.price.used_price_color._btn_size_style.item_conditions_data_box')

def main():
    with open(setting['mercari_selling'], 'r') as f:
        MERCARIDATA = json.load(f)

    while True: # ASIN #
        asin = input('ASIN >').replace('\n','')
        if asin == 'help': print('<ANS> ASINの確認方法はモノレートから商品を検索してください。')
        elif len(asin) != 10: print('不正な入力です。')
        else: break
    
    while True: # mercari ID #
        mercariId = input('mercari ID >').replace('\n','')
        if mercariId == 'help': print('<ANS> mercariIdの確認方法はメルカリの商品ページのリンクにあります。')
        elif len(mercariId) != 12: print('不正な入力です。')
        else: break
    
    driver.get("https://www.mercari.com/jp/items/"+mercariId)

    mer_slt_status   = FIND_CLASS_NAME('item-buy-btn')       # メルカリ商品状態を確認
    mer_slt_price    = FIND_TEXT_BY_CLASS_NAME('item-price') # メルカリ商品価格を取得
    mer_slt_price    = mer_slt_price.replace('¥','').replace(',','') # # データ加工

    if not 'disabled' in mer_slt_status: status = "selling"
    else: 
        print('この商品は売り切れています。')
        return

    mnrate_low_price = MONORATE(asin)
    mnrate_low_price = mnrate_low_price.replace('￥','').replace(',','')

    if mer_slt_price > mnrate_low_price: # 金額がモノレート最低金額よりも高くなった場合
        print('メルカリの商品はモノレートの中古品最安値より{}円高いです。'.format(str(int(mer_slt_price)-int(mnrate_low_price))))
    
    if mer_slt_price < mnrate_low_price: # 金額がモノレート最低金額よりも低くなった場合
        print('メルカリの商品はモノレートの中古品最安値より{}円安いです。'.format(str(int(mnrate_low_price)-int(mer_slt_price))))

    if mer_slt_price == mnrate_low_price: # 金額が同じ場合
        print('メルカリの商品とモノレートの中古品最安値の価格が同じです。')

    # データ整理
    jsonData = MERCARIDATA
    newData = {
        "id": randomId(),
        "asin": asin,
        "status": status,
        "mercariPrice": int(mer_slt_price),
        "mercariId": mercariId
    }
    jsonData.append(newData)

    # json書き出し
    with open(setting['mercari_selling'], 'w') as f:
        json.dump(jsonData, f, indent=4)
    
if __name__=='__main__':
    
    while True:
        print('load')
        main()