import streamlit as st
import requests

# 1. ページ設定とアイコン等の非表示設定
st.set_page_config(page_title="AIKA NAIL クチコミコンシェルジュ", page_icon="💅")

# CSSでデザインを微調整（GitHubアイコン非表示、クラウンマーク非表示、文字の折り返し対応）
st.markdown(
    """
    <style>
    /* 右上のメニューとGitHubアイコンを非表示 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 右下のStreamlitロゴ（フッター）を非表示 */
    footer {visibility: hidden;}
    
    /* クチコミ本文（code部分）の自動折り返し設定 */
    code {
        white-space : pre-wrap !important;
        word-break: break-all !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. タイトルと案内
st.title("💅 AIKA NAIL Review Concierge")
st.subheader("クチコミ作成 3ステップ")
st.write("1. **こたえる**（一言でOK！） → 2. **コピーする** → 3. **はる**")

# 3. 入力フォーム（一言で答えやすい st.text_input に変更し、具体的なヒントを表示）
#
q1 = st.text_input(
    "1. これまでの爪の悩みや、他店との違いは？", 
    placeholder="例：他店で傷んでしまった、形がコンプレックスだった"
)
q2 = st.text_input(
    "2. 今日のデザインや施術で『ここが好き！』な点は？", 
    placeholder="例：丁寧な甘皮ケア、絶妙なニュアンスカラー"
)
q3 = st.text_input(
    "3. 明日から、どんな気分で過ごせそうですか？", 
    placeholder="例：仕事中も眺めて癒やされる、自分に自信が持てる"
)

# 4. 実行ボタン
if st.button("クチコミ案を作成する"):
    if q1 and q2 and q3:
        with st.spinner("AIが心を込めて文章を作成しています..."):
            # Dify APIの設定
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
                
                # Difyの出力ノード llm_output を取得
                review_all = result['data']['outputs']['llm_output']
                
                st.success("クチコミ案が完成しました！")
                
                # --- 表示の整形（Markdownリンクとコピー枠を分離） ---
                if "```text" in review_all:
                    parts = review_all.split("```text")
                    header_part = parts[0]
                    body_content = parts[1].replace("```", "").strip()
                    
                    # リンクを表示（青文字でクリック可能）
                    st.markdown(header_part)
                    
                    # 本文をコピーボタン付きで表示
                    st.subheader("本文（右上のボタンでコピー！）")
                    st.code(body_content, language=None)
                else:
                    st.code(review_all, language=None)
                
                st.balloons() # お祝いのバルーン
                
            except Exception as e:
                st.error("接続エラーが発生しました。時間を置いて再度お試しください。")
    else:
        st.warning("すべてのご質問にお答えいただけますと幸いです。")