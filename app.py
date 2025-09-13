from dotenv import load_dotenv
load_dotenv()


#画面に入力フォームを1つ用意し、入力フォームから送信したテキストをLangChainを使ってLLMにプロンプトとして渡し、回答結果が画面上に表示されるようにしてください。ラジオボタンでLLMに振る舞わせる専門家の種類を選択できるようにし、Aを選択した場合はAの領域の専門家として、またBを選択した場合はBの領域の専門家としてLLMに振る舞わせるよう、選択値に応じてLLMに渡すプロンプトのシステムメッセージを変えてください。また用意する専門家の種類はご自身で考えてください。「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り、LLMからの回答を戻り値として返す関数を定義し、利用してください。Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示してください。
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.schema import (HumanMessage, SystemMessage)
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
st.title("専門家アドバイスアプリ")
st.write("""
このアプリは、選択した専門家の視点からアドバイスを
提供します。以下の入力フォームに質問を入力し、専門家の種類を選択して「送信」ボタンを押してください。
""")
def get_advice(input_text, expert_type):
    if expert_type == "医療専門家":
        system_message = "あなたは医療の専門家です。健康に関する質問に対して、正確で信頼できるアドバイスを提供してください。"
    elif expert_type == "法律専門家":
        system_message = "あなたは法律の専門家です。法律に関する質問に対して、正確で信頼できるアドバイスを提供してください。"
    elif expert_type == "キャリアカウンセラー":
        system_message = "あなたはキャリアカウンセラーです。キャリアに関する質問に対して、建設的で実用的なアドバイスを提供してください。"
    else:
        system_message = "あなたは多分野の専門家です。質問に対して、適切なアドバイスを提供してください。"
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    response = llm(messages)
    return response.content
input_text = st.text_area("質問を入力してください")
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("医療専門家", "法律専門家", "キャリアカウンセラー")
)
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

