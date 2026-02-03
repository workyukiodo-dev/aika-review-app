import streamlit as st
import requests

# ページ設定
st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

st.title("💅 AIKA NAIL Review Concierge")
st.write("本日はご来店ありがとうございました。指先の変化とともに、今の想いをお聞かせください。")

# 入力欄
q1 = st.text_area("1. 最近のお爪の調子はいかがですか？", placeholder="例：トラブルなく過ごせている安心感など")
q2 = st.text_area("2. 本日のデザインや施術はいかがでしたか？", placeholder="例：お任せの心地よさや仕上がりの感想など")
q3 = st.text_area("3. 今、指先を見てどんなお気持ちですか？", placeholder="例：明日からの活力になる喜びなど")

if st.button("クチコミ案を作成する"):
    if q1 and q2 and q3:
        with st.spinner("AIが心を込めて文章を作成しています..."):
            # --- ここにご自身のAPIキーを入れてください ---
            api_key = "app-Eeu81CvERvLEhcrwsmn4VMZ7" 
            url = "https://api.dify.ai/v1/workflows/run"
            
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "inputs": {"answer_1": q1, "answer_2": q2, "answer_3": q3},
                "response_mode": "blocking",
                "user": "aika-nail-customer"
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                # エラーチェック
                if response.status_code != 200:
                    st.error("現在、AIが少しお休みしています。時間をおいて再度お試しください。")
                    st.write(result) # 開発中のみ表示
                    st.stop()

                # 出力ノード llm_output を取得
                review_all = result['data']['outputs']['llm_output']
                
                # --- 表示の整形（Markdownリンクと本文を分ける） ---
                st.success("クチコミ案が完成しました！")
                
                # "```text" という文字で分割して、上半分をリンク、下半分をコピー枠にする
                if "```text" in review_all:
                    parts = review_all.split("```text")
                    header = parts[0]
                    body = parts[1].replace("```", "").strip()
                    
                    st.markdown(header) # リンクを有効化して表示
                    st.subheader("本文（以下をコピーして貼り付けてください）")
                    st.code(body, language=None) # コピーしやすい枠
                else:
                    st.markdown(review_all)
                
                st.balloons() # 成功のお祝い

            except Exception as e:
                st.error(f"接続エラーが発生しました。オーナーにお知らせください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
