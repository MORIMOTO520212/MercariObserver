import os, json, selenium, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep

# 設定ファイル読み込み
with open('setting.json', 'r') as f: 
    setting = json.load(f)

#            初期設定            #

# chromeのプロファイルパス　※無い場合は空のファイルを作成
PROFILEPATH = 'userdata'
# メルカリデータパス　ここに監視する商品を登録する
MERCARIDATAPATH = setting['mercari_selling']
TRANSACTIONPATH = setting['transaction']


options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + PROFILEPATH)

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

def TRANSACTION(id, asin, mercariId, type, merPrice, mnPrice, be, af, profit):
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y/%m/%d %H:%M')
    transaction = {
        "id": id,
        "asin": asin,
        "mercariId": mercariId,
        "date": date,
        "changeDetails":{}
    }
    if type == "soldout":
        transaction["changeDetails"] = {
            "soldout": True,
            "add": False,
            "mercariChange": False,
            "mnrateChange": False
        }
    elif type == "add":
        transaction["changeDetails"] = {
            "soldout": False,
            "add": {
                "mercariPrice": merPrice,
                "mnratePrice": mnPrice,
                "Profit": profit
            },
            "mercariChange": False,
            "mnrateChange": False
        }
    else:
        if type == "mercariChange":
            transaction["changeDetails"] = {
                "soldout": False,
                "add": False,
                "mercariChange": {
                    "before": be,
                    "after": af
                },
                "mnrateChange": False
            }
        if type == "mnrateChange":
            transaction["changeDetails"] = {
                "soldout": False,
                "add": False,
                "mercariChange": False,
                "mnrateChange": {
                    "before": be,
                    "after": af
                }
            }

    transaction_d.append(transaction)

    with open(TRANSACTIONPATH, 'w') as f:
        json.dump(transaction_d, f, indent=4)

def BOT(data):
    driver.get("https://www.mercari.com/jp/items/"+data)
    mer_slt_status   = FIND_CLASS_NAME('item-buy-btn')
    mer_slt_price    = FIND_TEXT_BY_CLASS_NAME('item-price')
    mer_slt_price    = mer_slt_price.replace('¥','').replace(',','')

    if 'disabled' in mer_slt_status: # 売り切れた場合
        return 'soldOut'

    mnrate_low_price = MONORATE(mer_slt_d['asin'])
    mnrate_low_price = mnrate_low_price.replace('￥','').replace(',','')

    if mer_slt_price > mnrate_low_price: # 金額がモノレート最低金額よりも高くなった場合
        return 'than{}'.format(int(mer_slt_price)-int(mnrate_low_price)), int(mer_slt_price), int(mnrate_low_price)
    
    if mer_slt_price < mnrate_low_price: # 金額がモノレート最低金額よりも低くなった場合
        return 'down{}'.format(int(mnrate_low_price)-int(mer_slt_price)), int(mer_slt_price), int(mnrate_low_price)

    if mer_slt_price == mnrate_low_price: # 金額が同じ場合
        return 0, int(mer_slt_price), int(mnrate_low_price)


if __name__=='__main__':
    while True:
        driver = webdriver.Chrome(options=options)
        
        with open(MERCARIDATAPATH, 'r') as f:
            mer_sel_d = json.load(f)
        
        with open(TRANSACTIONPATH, 'r') as f:
            transaction_d = json.load(f)

        for mer_slt_d in mer_sel_d:
            mercariId = mer_slt_d['mercariId']

            if mer_slt_d['status'] != 'soldout': # soldout判定した商品は飛ばす
                bot_result, mer_slt_price, mnrate_low_price = BOT(mercariId) # スクレイピングで商品の状態を確認する
                mer_json_price    = mer_slt_d['mercariPrice'][len(mer_slt_d['mercariPrice'])-1] # jsonからメルカリの最後の価格を取得
                mnrate_json_price = mer_slt_d['mnratePrice'][len(mer_slt_d['mnratePrice'])-1]   # jsonからモノレートの最後の価格を取得

                if mer_slt_price != mer_json_price: # jsonに保存していた価格と違っていたら
                    mer_ch_rlt = mer_slt_price - mer_json_price
                    if   mer_ch_rlt > 0: # 値上がりした場合
                        print("メルカリの値段が変更されました。\n変更前：{}\n変更後：[{}]".format(str(mer_json_price), str(mer_slt_price)))
                    elif mer_ch_rlt < 0: # 値下がりした場合
                        print("メルカリの値段が変更されました。\n変更前：{}\n変更後：{}".format(str(mer_json_price), str(mer_slt_price)))

                    # transaction.jsonに変更を保存
                    TRANSACTION(mer_slt_d["id"], mer_slt_d["asin"], mercariId, "mercariChange", False, False, mer_json_price, mer_slt_price, False)

                    # mercari_selling.jsonに変更を保存
                    mer_slt_d['mercariPrice'].append(mer_slt_price)
                    with open(MERCARIDATAPATH,'w') as f: 
                        json.dump(mer_sel_d, f, indent=4)
                
                if mnrate_low_price != mnrate_json_price: # jsonに保存していた価格と違っていたら
                    mnrate_ch_rlt = mnrate_low_price - mnrate_json_price
                    if   mnrate_ch_rlt > 0: # 値上がりした場合
                        print("モノレートの値段が変更されました。\n変更前：{}\n変更後：{}".format(str(mnrate_json_price), str(mnrate_low_price)))
                    elif mnrate_ch_rlt < 0: # 値下がりした場合
                        print("モノレートの値段が変更されました。\n変更前：{}\n変更後：[{}]".format(str(mnrate_json_price), str(mnrate_low_price)))
                
                    # transaction.jsonに変更を保存
                    TRANSACTION(mer_slt_d["id"], mer_slt_d["asin"], mercariId, "mnrateChange", False, False, mnrate_json_price, mnrate_low_price, False)

                    # mercari_selling.jsonに変更を保存
                    mer_slt_d['mnratePrice'].append(mnrate_low_price)
                    with open(MERCARIDATAPATH,'w') as f: 
                        json.dump(mer_sel_d, f, indent=4)

                if bot_result == 'soldOut':
                    print('MercariID:{} 売り切れ'.format(mercariId))
                    TRANSACTION(mer_slt_d["id"], mer_slt_d["asin"], mercariId, "soldout", False, False, False, False, False)

                elif 'than' in bot_result:
                    than_amount = bot_result.replace('than','')
                    print('MercariID:{} モノレートの中古品最安値より{}円高いです。'.format(mercariId, than_amount))

                elif 'down' in bot_result:
                    down_amount = bot_result.replace('down','')
                    print('MercariID:{} モノレートの中古品最安値より{}円安いです。'.format(mercariId, down_amount))

                elif not bot_result:
                    print('MercariID:{} モノレートと同じ金額'.format(mercariId))
            else:
                print('MercariID:{} 売り切れ'.format(mercariId))

        driver.close()