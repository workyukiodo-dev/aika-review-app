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
                
                # --- 表示の整形（折り返し対応版） ---
                st.success("クチコミ案が完成しました！")
                
                if "```text" in review_all:
                    parts = review_all.split("```text")
                    header = parts[0]
                    body = parts[1].replace("```", "").strip()
                    
                    # 1. リンク部分をMarkdownで表示（青いリンクになります）
                    st.markdown(header) 
                    
                    st.subheader("本文（以下をコピーして貼り付けてください）")
                    
                    # 2. 本文を「テキストエリア」で表示（自動で折り返され、コピーも簡単です）
                    # heightで高さを調整できます。disabled=Trueで編集不可にしています。
                    st.text_area(label="コピー用ボックス", value=body, height=200, disabled=False)
                    
                    st.info("↑ 枠内の文章を長押し（またはドラッグ）してコピーしてください。")
                else:
                    # 万が一分割に失敗した時のためのバックアップ表示
                    st.text_area(label="クチコミ案", value=review_all, height=300)
                
                st.balloons() # 成功のお祝い
                
            except Exception as e:
                st.error(f"接続エラーが発生しました。時間を置いて再度お試しください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")
