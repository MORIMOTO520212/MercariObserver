# MERCARI OBSERVER 1.0
メルカリの商品状態を監視します。  

chromedriver.exe はお使いのChromeブラウザのバージョンを確認して適切なファイルを以下のリンクからダウンロードし置き換えてください。  
[ChromeDriver Download](https://chromedriver.chromium.org/downloads)

**バージョン情報の確認方法**  
Chromeのアドレスバーで以下のリンクにアクセスします。
```
chrome://version
```

**各実行ファイルの使用方法**
- AddItem.py
商品を監視下に配置します。
モノレートより価格が高くなった場合や商品自体が売り切れた場合は監視対象から自動的に外れます。

- main.py
常時監視ファイルです。
このファイルを実行している間は商品を常に巡回し監視します。