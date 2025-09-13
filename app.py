import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging
from dotenv import load_dotenv
import os

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ローカル用 .env 読み込み
load_dotenv()

# Streamlit Secrets から取得、なければローカル環境変数を利用
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# LLMの準備
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# タイトルと説明
st.title("専門家アドバイスアプリ")
st.write("""
このアプリは、選択した専門家の視点からアドバイスを
提供します。以下の入力フォームに質問を入力し、専門家の種類を選択して「送信」ボタンを押してください。
""")

# 専門家アドバイス取得関数
def get_advice(input_text, expert_type):
    system_messages = {
        "医療専門家": "あなたは医療の専門家です。健康に関する質問に対して、正確で信頼できるアドバイスを提供してください。",
        "法律専門家": "あなたは法律の専門家です。法律に関する質問に対して、正確で信頼できるアドバイスを提供してください。",
        "キャリアカウンセラー": "あなたはキャリアカウンセラーです。キャリアに関する質問に対して、建設的で実用的なアドバイスを提供してください。",
        "教育専門家": "あなたは教育の専門家です。学習や教育に関する質問に対して、適切で実用的なアドバイスを提供してください。"
    }
    
    system_message = system_messages.get(expert_type, "あなたは多分野の専門家です。質問に対して、適切で実用的なアドバイスを提供してください。")
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    
    response = llm(messages)
    return response.content

# 入力フォーム
input_text = st.text_area("質問を入力してください")
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("医療専門家", "法律専門家", "キャリアカウンセラー", "教育専門家")
)

# 送信ボタン
if st.button("送信"):
    if input_text.strip() == "":
        st.warning("質問を入力してください。")
    else:
        try:
            advice = get_advice(input_text, expert_type)
            st.subheader("専門家からのアドバイス:")
            st.write(advice)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            st.error("アドバイスの取得中にエラーが発生しました。もう一度お試しください。")
