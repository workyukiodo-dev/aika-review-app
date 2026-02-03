import streamlit as st
import requests

# ページ設定
st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

st.title("💅 AIKA NAIL Review Concierge")
st.write("本日はご来店ありがとうございました。今の率直な想いをお聞かせください。")

# 入力フォーム
q1 = st.text_area("1. 最近のお爪の調子はいかがですか？", placeholder="トラブルなく過ごせている安心感など")
q2 = st.text_area("2. 本日のデザインや施術はいかがでしたか？", placeholder="お任せの心地よさや仕上がりの感想など")
q3 = st.text_area("3. 今、指先を見てどんなお気持ちですか？", placeholder="明日からの活力や自分への投資の喜びなど")

if st.button("クチコミ案を作成する"):
    if q1 and q2 and q3:
        with st.spinner("AIが品格のある文章を作成しています..."):
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
                
                # 出力ノード llm_output を取得
                review_all = result['data']['outputs']['llm_output']
                
                # --- UIの改善：Markdownとコード枠を分離 ---
                st.success("クチコミ案が完成しました！")
                
                # "```text" という文字を境目に上下に分割する
                if "```text" in review_all:
                    parts = review_all.split("```text")
                    header_part = parts[0] # リンク部分
                    body_part = parts[1].replace("```", "").strip() # 本文
                    
                    st.markdown(header_part) # リンクを青文字で表示
                    st.subheader("本文（コピーして貼り付けてください）")
                    st.code(body_part, language=None) # コピーしやすい枠
                else:
                    st.markdown(review_all)
                
                st.balloons() # 成功のお祝い
                
            except Exception as e:
                st.error(f"接続エラーが発生しました。時間を置いて再度お試しください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
