from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from assistant.utils import VideoSearchTool
from langchain.utilities import ArxivAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_simple_prompt, load_assistant_prompt


class Agent():
    def __init__(self) -> None:
        # Prepare agent chain for ai-assistant.
        self.initial_agent = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_simple_prompt("initial_stage"),
            verbose=False,
        )

        self.chat_agent = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_assistant_prompt("en_assistant"),
            verbose=False,
            memory=ConversationBufferWindowMemory(k=2),
        )

        self.paper_analyzer = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_simple_prompt("paper_analyze"),
            verbose=False,
        )

        self.video_agent = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=load_simple_prompt("video_search"),
            verbose=False
        )

        self.paper_keyword = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_simple_prompt("paper_search"),
            verbose=False
        )
        
        # Tool collection.
        self.paper_search = ArxivAPIWrapper()
        self.search_engine = DuckDuckGoSearchRun()
        self.video_search = VideoSearchTool()

    def run(self, text: str):
        # 1st stage: Intent classification.
        intent = self.initial_agent.run(text)

        # 2nd stage: Decide to use different agent based on intention.
        result = None
        if 'schedule' in intent.lower():
            print(f"Intention is schedule plan: {intent}")
        elif 'video' in intent.lower():
            print(f"Intention is searching video: {intent}")
            search_name = self.video_agent.run(text).replace('"', '').replace('\n', '')
            print(f"Search name: {search_name}")
            result = f"Here are some video about {search_name}.\n{self.video_search.run(search_name)}"
        elif 'paper' in intent.lower():
            print(f"Intention is paper search: {intent}")
            keyword = self.paper_keyword.run(text).replace('\n', '')
            print(f"Keyword: {keyword}")
            search_result = self.paper_search.run(keyword)
            result = self.paper_analyzer.run(search_result)

            result = f"Here are some paper that you should take it a look.\n{result}"
        else:
            print(f"Intention is chat only: {intent}")
            result = self.chat_agent.run(text)

        return result


def build_gpt_agent():
    agent = Agent()
    return agent
