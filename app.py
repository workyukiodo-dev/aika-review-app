import streamlit as st
import requests

# --- ページ設定（ここでサロンの色を出せます） ---
st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

st.title("💅 AIKA NAIL Review Concierge")
st.write("本日はご来店ありがとうございました。今の率直な想いをお聞かせください。")

# --- 入力フォーム（Difyの変数名と合わせます） ---
# image_aa31bb.png の変数名 answer_1, 2, 3 をそのまま使用
q1 = st.text_area("1. 最近のお爪の調子はいかがですか？", placeholder="トラブルなく過ごせている安心感など")
q2 = st.text_area("2. 本日のデザインや施術はいかがでしたか？", placeholder="お任せの心地よさや仕上がりの感想など")
q3 = st.text_area("3. 今、指先を見てどんなお気持ちですか？", placeholder="明日からの活力や自分への投資の喜びなど")

if st.button("クチコミ案を作成する"):
    if q1 and q2 and q3:
        with st.spinner("AIが品格のある文章を作成しています..."):
            # Dify APIの設定
            api_key = "app-Eeu81CvERvLEhcrwsmn4VMZ7"  # Difyで発行したAPIキー
            url = "https://api.dify.ai/v1/workflows/run" # DifyのAPIエンドポイント
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Difyへ送るデータ（image_aa31bb.pngの設定を流用）
            data = {
                "inputs": {
                    "answer_1": q1,
                    "answer_2": q2,
                    "answer_3": q3
                },
                "response_mode": "blocking",
                "user": "aika-nail-customer"
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                # 結果の表示（Difyの出力を表示）
                review_text = result['data']['outputs']['text'] # テンプレートノードの出力を取得
                st.success("クチコミ案が完成しました！")
                st.code(review_text, language=None) # コピーしやすい枠で表示
                st.info("右上のボタンでコピーして、Googleマップへ貼り付けてください。")
                
            except Exception as e:
                st.error(f"接続エラーが発生しました。オーナーにお知らせください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
