import json, requests
from bs4 import BeautifulSoup

html = requests.get("https://mnrate.com/item/aid/B07X779ZK5")
soup = BeautifulSoup(html.text, "html.parser")

with open('soup.txt', 'w') as f:
    f.write(str(soup))

'''
for scriptdata in soup.find_all("script"):
    print('load {}\n\n'.format(str(scriptdata)[:100]))
    if "server_data" in str(scriptdata):
        mnrate = scriptdata.split(';')[0].split('\'')[1]
        break

mnrate_data = {}
mnrate_data = json.loads(mnrate)

print(mnrate_data["summary"]["data_name"])
'''