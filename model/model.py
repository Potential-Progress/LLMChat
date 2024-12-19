from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage,SystemMessage

class Model:
    def __init__(self,provider="openai"):
        """
        初始化模型支持多模型切换
        :param provider: 模型提供方 (openai, claude, deepseek)
        :param model_name: 模型名称
        :param base_url: 如果是第三方模型 (如 Deepseek) 则需要指定
        """
        # 根据 provider 初始化不同模型
        self.provider = provider
        if provider.lower() == "openai":
            #api_key = os.getenv("OPENAI_API_KEY")
            openai_api_key = ""
            self._llm = ChatOpenAI(
                api_key=openai_api_key,
                model="gpt-4o-2024-11-20",
                temperature=0.7,
                max_tokens=1000,
                streaming=True,
                base_url="https://api.openai.com/v1"
            )
            # return self._llm
            
        elif provider.lower() == "deepseek":
            #deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            depseek_api_key = ""
            self._llm = ChatOpenAI(
                api_key=depseek_api_key,
                model = "deepseek-chat",
                temperature=0.7,
                max_tokens=1000,
                streaming=True,
                base_url="https://api.deepseek.com"
            )
        elif provider.lower() == "claude":
            #claude_api_key = os.getenv("CLAUDE_API_KEY")
            claude_api_key = ""
            self._llm = ChatAnthropic(
                api_key=claude_api_key,
                model="claude-3-5-sonnet-20240620",
                temperature=0.7,
                max_tokens=1000,
                base_url="https://api.anthropic.com"
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
    def __call__(self,user_input):
        messages = [
            SystemMessage(content="You are a helpful and knowledgeable assistant. Answer questions clearly and concisely, providing examples when needed.And please answer in Chinese"),
            HumanMessage(content=user_input)
            ]
        
        responses = self._llm.invoke(messages)
        return responses.content
if __name__ == "__main__":
    model = Model(provider="claude")
    response = model("你好")
    print(response)
