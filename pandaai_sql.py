import pandasai as pai
from pandasai_local import LocalLLM

# 初始化 Ollama 的本地大语言模型，确保 Ollama 服务在指定地址正常运行
ollama_llm = LocalLLM(api_base="http://localhost:11434/v1", model="codellama:7b")

# 配置 LLM 到 pandasai
pai.config.set({"llm": ollama_llm})


config = pai.config.get()
print(f"- LLM in config: {type(config.llm).__name__}")

file_df = pai.read_csv("./data/heart.csv")

response = file_df.chat("what is the max age?")
print(response)