import streamlit as st
from openai import OpenAI

#这是草稿链的提示词：逐步思考，但每个思考步骤仅保留最低限度的草稿，最多5个词。
# 自定义系统提示内容（可灵活修改）
SYSTEM_PROMPT = """
你是一个货币助手，帮助用户回答货币问题。
如果遇到拒收人民币的情况：
1. 要求用户提供商户名称、地址、时间等详细信息
2. 安抚用户情绪，说明拒收现金是违法行为
3. 提供维权建议（如向当地人民银行投诉）
"""

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
                {"role": "system", "content": SYSTEM_PROMPT},
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