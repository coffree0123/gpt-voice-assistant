from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_initial_promit, load_assistant_prompt


class Agent():
    def __init__(self) -> None:
        # Prepare agent chain for ai-assistant.
        self.initial_agent = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_initial_promit("initial_stage"),
            verbose=False,
        )

        self.chat_agent = LLMChain(
            llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
            prompt=load_assistant_prompt("en_assistant"),
            verbose=False,
            memory=ConversationBufferWindowMemory(k=2),
        )

    def run(self, text: str):
        # 1st stage: Intent classification.
        intent = self.initial_agent.run(text)

        # 2nd stage: Decide to use different agent based on intention.
        result = None
        if 'schedule' in intent.lower():
            print(f"Intention is schedule plan: {intent}")
        else:
            print(f"Intention is chat only: {intent}")
            result = self.chat_agent.run(text)

        return result


def build_gpt_agent():
    agent = Agent()
    return agent
