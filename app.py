import streamlit as st
import requests

st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

st.title("💅 AIKA NAIL Review Concierge")
st.write("本日はご来店ありがとうございました。今の率直な想いをお聞かせください。")

q1 = st.text_area("1. 最近のお爪の調子はいかがですか？")
q2 = st.text_area("2. 本日のデザインや施術はいかがでしたか？")
q3 = st.text_area("3. 今、指先を見てどんなお気持ちですか？")

if st.button("クチコミ案を作成する"):
    if q1 and q2 and q3:
        with st.spinner("AIが品格のある文章を作成しています..."):
            api_key = "app-Eeu81CvERvLEhcrwsmn4VMZ7" # あなたのキーを入れる
            url = "[https://api.dify.ai/v1/workflows/run](https://api.dify.ai/v1/workflows/run)"
            
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "inputs": {"answer_1": q1, "answer_2": q2, "answer_3": q3},
                "response_mode": "blocking",
                "user": "aika-nail-customer"
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                # 終了ノードの変数名 llm_output を取得
                review_all = result['data']['outputs']['llm_output']
                
                # --- ここからUIの魔法 ---
                st.success("クチコミ案が完成しました！")
                
                # 1. リンクや説明文を「Markdown」として表示（これでリンクがクリック可能になります）
                # Dify側のテンプレートから「リンク部分」と「クチコミ部分」を分けて表示する工夫
                parts = review_all.split("```text")
                header_part = parts[0]
                content_part = parts[1].replace("```", "") if len(parts) > 1 else ""
                
                st.markdown(header_part) # リンクやタイトルを綺麗に表示
                
                if content_part:
                    st.subheader("本文（以下をコピーしてください）")
                    st.code(content_part, language=None) # クチコミ本文だけをコピー枠に入れる
                
                st.balloons() # 完成のお祝いバルーン
                
            except Exception as e:
                st.error(f"エラーが発生しました。時間を置いて再度お試しください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
