import streamlit as st
import requests

# ページ設定
st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

st.title("💅 AIKA NAIL Review Concierge")
st.write("本日はご来店ありがとうございました。今の率直な想いをお聞かせください。")

# 入力フォーム
q1 = st.text_area("1. 最近のお爪の調子はいかがですか？")
q2 = st.text_area("2. 本日のデザインや施術はいかがでしたか？")
q3 = st.text_area("3. 今、指先を見てどんなお気持ちですか？")

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
                
                st.success("クチコミ案が完成しました！")
                
                if "```text" in review_all:
                    parts = review_all.split("```text")
                    header_part = parts[0]
                    body_content = parts[1].replace("```", "").strip()
                    
                    # 1. リンクをMarkdownで表示（青文字でクリック可能）
                    st.markdown(header_part)
                    
                    # 2. 本文をコピーボタン付きで表示
                    st.subheader("本文（右上のボタンでコピー！）")
                    # st.codeに language=None を指定するとコピーボタンが出現します
                    st.code(body_content, language=None)
                    
                    # 💡スマホでの「折り返し」を強制するスタイル設定
                    st.markdown("""
                        <style>
                        code {
                            white-space : pre-wrap !important;
                            word-break: break-all !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                else:
                    st.code(review_all, language=None)
                
                st.balloons()
                
            except Exception as e:
                st.error("接続エラーが発生しました。時間を置いて再度お試しください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
