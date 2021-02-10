import urllib.request
import urllib.parse
import json
import requests

class A3RT:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def proofreading_API(self, text):
        API = "https://api.a3rt.recruit-tech.co.jp/proofreading/v2/typo"

        values = {
            'apikey': self.API_KEY,
            'sentence':text,
            'sensitivity':"medium", # チェック感度 low, medium, high の3つ
            }
        # パラメータをURLエンコード
        params = urllib.parse.urlencode(values)
        # リクエスト用のURLを生成
        url = API + "?" + params
        # リクエストを投げて結果を取得
        r = requests.get(url)
        # 辞書型に変換
        data = json.loads(r.text)
        # 結果を表示
        print(data)
        print()
        # 間違いの指摘箇所を表示（ <<"">> で示した場所）
        print(data['checkedSentence'])
        print()

        word_list = list(text)
        a = []
        if 'alerts' in data:    # 誤字を検出したとき['alerts']が返される
            for response_data in data['alerts']:  
                a.append(response_data['pos'])
                print("指摘箇所：{}、指摘文字：{}".format(response_data['pos'], response_data['word'])) 
                print()
                # 誤字の部分を正しいと思われる文字に置き換え
                word_list[response_data['pos']] = response_data['suggestions'][0]
        else:
            print("正しい文章です。")
            print()
        # リストにしたテキストを元に戻す
        correct_text = "".join(word_list)
        print(correct_text)
        return correct_text

    def text_suggest_API(self, text):
        API = "https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict"

        values = {
            'apikey': self.API_KEY,
            'previous_description':text,
            'style': 0, # 0:現代文 1:和歌 2:プログラミング言語(Go)
            'separation': 0 # 0:単語 1:フレーズ 2:センテンス
            }
        # パラメータをURLエンコード
        params = urllib.parse.urlencode(values)
        # リクエスト用のURLを生成
        url = API + "?" + params
        # リクエストを投げて結果を取得
        r = requests.get(url)
        # 辞書型に変換
        data = json.loads(r.text)
        # 結果を表示
        print(data)

        # リクエストがうまく動作しなかった場合のエラー一覧
        response_status_error = {
            1000: "AIPキーが指定されていません",
            1001: "APIキーが正しくありません",
            1010: "サーバーが見つかりません",
            1030: "アクセスが拒否されました",
            1400: "リクエストパラメーターが正しくありません",
            1405: "メソッドが正しくありません",
            1413: "リクエストパラメーターの値が長すぎます",
            1500: "API処理でエラーが発生しました"
            }
        
        # 結果を元のテキストにつなげて表示
        if data['status'] == 0:
            generate_text = "".join(data['suggestion'])
            result_text = text + generate_text
            print(result_text)
        else:
            print(response_status_error[data['status']])


kousei = A3RT("{発行したAPIキー}")
seisei = A3RT("{発行したAPIキー}")

text = "{任意のテキスト}"


seisei.text_suggest_API(kousei.proofreading_API(text))