<!doctype html>
<html>
    <head>
        <title>mercari add Item</title>
        <link rel="stylesheet" type="text/css" href="assets/style.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script src="http://code.jquery.com/jquery.min.js"></script>
    </head>
    <body>
        <div class="header">
            <div class="a"></div>
            <div class="b"></div>
            <div class="c"></div>
        </div>
        <div class="main">
            <div class="left"></div>
            <div class="center">
                <form method="post" action="">
                    <div class="asin_input">
                        <label class="ef">
                                <input type="text" placeholder="Amazon ASIN ID">
                        </label>
                    </div>
                    <div class="asin_input">
                        <label class="ef">
                                <input type="text" placeholder="mercari ID">
                        </label>
                    </div>
                    <div class="submit">
                        <input id="button" type="submit" value="追加">
                    </div>
                    <div class="note">
                        トランザクションの表示数をブラウザから変更できるようにする。<br>
                        そのとき変更した内容をセッションに保存する。
                    </div>
                </form>
            </div>
            <div class="transaction">
                <!-- ここにトランザクションをどんどん追加していく -->
                <div class="btn">
                    <button id="button" class="remove-btn">削除</button>
                    <select id="select" name="view">
                        <option value="5">5</option>
                        <option value="8">8</option>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                </div>
                <div class="block">
                    <div class="type">商品が追加されました。</div>
                    <div class="product_name">Nintendo Switch 本体 (ニンテンドースイッチ) Joy-Con(L) ネオンブルー/(R) ネオンレッド(バッテリー持続時間が長くなったモデル)</div>
                    <div class="id">
                        <div class="system_id"><span>ASIN ID：</span>B0T7IOP44MNBJ0E</div>
                        <div class="system_id"><span>mercari ID：</span>m384975935</div>
                    </div>
                    <div class="price"><span>メルカリ価格：</span>¥5,000</div>
                    <div class="price"><span>モノレート最安価格：</span>¥3,200</div>
                    <div class="profit"><span>利益：</span>¥1,900</div>
                    <div class="date">2020/05/23 16:22</div>
                </div>
                <div class="block">
                    <div class="type a">メルカリの商品の価格が変更されました。</div>
                    <div class="product_name">Nintendo Switch 本体 (ニンテンドースイッチ) Joy-Con(L) ネオンブルー/(R) ネオンレッド(バッテリー持続時間が長くなったモデル)</div>
                    <div class="id">
                        <div class="system_id"><span>ASIN ID：</span>B0T7IOP44MNBJ0E</div>
                        <div class="system_id"><span>mercari ID：</span>m384975935</div>
                    </div>
                    <div class="price"><span>価格：</span>¥3,200</div>
                    <div class="price"><span>変更前：</span>¥5,000</div>
                    
                    <div class="date">2020/05/23 16:22</div>
                </div>
            </div>
        </div>
    </body>
    <script>
        var selected = $("#select").children("option:selected");
        var selectedValue = selected.val();
        console.log("トランザクション表示件数："+selectedValue);
        transaction_count = selectedValue; // 履歴表示数
        
        function past(transaction, mercari_selling){
            for(var i = Object.keys(transaction).length-1; i >= (Object.keys(transaction).length-1)-transaction_count; i--){ // 表示数分ループ
                id = transaction[i].id;
                m_s_element = mercari_selling.find((element) => { // mercari_selling.jsonからidを探す
                    return (element.id == id)
                });
                //------------------------------//
                product_name = m_s_element.name; // ここで発生するエラーは”jsonのデータがループ数より少ない”場合に発生するので正常な挙動です。
                console.log(product_name);
                //------------------------------//
            }
        }

        var _size = 0;
        var _size2= 0;
        var _transactionData = '';
        var transactionData;
        var mercari_sellingData;

        function t_d(data){
            transactionData = data;
        }
        function m_s_d(data){
            mercari_sellingData = data;
        }

        function interval(){
            $.post('response.php?mode=transaction', {}, function(data){ // jQuery POST
                jsonData = JSON.parse(data);
                if (_size != jsonData.length){
                    _size = jsonData.length;
                    t_d(jsonData);
                }
            });
            $.post('response.php?mode=mercari_selling', {}, function(data){
                jsonData = JSON.parse(data);
                if (_size2 != jsonData.length){
                    _size2 = jsonData.length;
                    m_s_d(jsonData);
                }
            });
            if (_transactionData != Object.keys(transactionData).length){
                past(transactionData, mercari_sellingData);
                _transactionData = Object.keys(transactionData).length;
            }
        }
        setInterval(interval, 1000);
    </script>
</html>