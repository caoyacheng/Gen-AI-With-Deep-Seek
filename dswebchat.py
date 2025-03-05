import streamlit as st
from openai import OpenAI

# session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好，货币小助手有什么可以帮你的吗?"}
    ]

api_key = st.secrets["api_key"]


def deepseek_chat(api_key: str, messages: list) -> str:
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个货币助手，帮助用户回答货币问题，如果遇到投入拒收人民币的问题，请要求用户提供拒收的商户信息，并安抚用户"},
                *messages
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return ""


def main():
    st.title('💰 货币小助手')

    with st.sidebar:
        st.header("📚 用户手册")
        st.markdown("""
        ### 使用方法
        1. **开始聊天**：在聊天窗口底部的输入框中输入您的消息
        2. **继续对话**：聊天机器人会记住您的对话内容，因此您可以提出后续问题
        3. **查看历史记录**：向上滚动以查看您的聊天历史
        
        ### 提示
        - 提问时请尽量具体
        - 如有需要，请提出后续问题以进一步澄清
        - 使用重置按钮开始新的对话
        
        ### 需要帮助吗？
        如果您遇到任何问题，请尝试使用下方的按钮重置聊天。
        """)

        # 如果点击“重置聊天”按钮
        if st.button("重置聊天"):
            st.session_state.messages = [
                {"role": "assistant", "content": "你好，货币小助手有什么可以帮你的吗?"}
            ]
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("您在想什么呢？"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = deepseek_chat(api_key, st.session_state.messages)
                if response:
                    st.write(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()