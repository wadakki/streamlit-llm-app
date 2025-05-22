from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
st.write("APIキーの取得チェック")
st.write("OPENAI_API_KEY is set:", os.getenv("OPENAI_API_KEY") is not None)
# --- タイトルと説明 ---
st.title("提出課題: 回答専門家の選択")

st.write("##### 専門家A: ペットの専門家")
st.write("入力フォームに質問を入力し、「実行」ボタンを押すことでペットの質問に答えてくれます。")
st.write("##### 専門家B: 機械設備の整備の専門家")
st.write("入力フォームに質問を入力し、「実行」ボタンを押すことで機械設備の整備について質問に答えてくれます。")

# --- ラジオボタン ---
selected_item = st.radio(
    "動作モードを選択してください。",
    ["ペットの専門家", "機械設備の整備"]
)

# --- テキスト入力フォーム ---
user_input = st.text_input("質問を入力してください:")

# --- 実行ボタン ---
if st.button("実行"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        # LangChainでLLMを呼び出す処理
        def get_expert_response(text: str, expert_type: str) -> str:
            system_prompt = {
                "ペットの専門家": "あなたは優しいペットの専門家です。飼い方や病気について詳しく説明してください。",
                "機械設備の整備": "あなたは経験豊富な機械設備の整備士です。機械の保守や故障診断に関して専門的に答えてください。"
            }.get(expert_type, "あなたは親切なアシスタントです。")

            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=text)
            ]

            result = llm(messages)
            return result.content

        # 回答取得と表示
        answer = get_expert_response(user_input, selected_item)
        st.subheader("回答:")
        st.write(answer)