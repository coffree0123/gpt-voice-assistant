from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_assistant_prompt

def build_gpt_agent(prompt: str = 'en_assistant'):
    # Prepare prompt for chatgpt agent. You can add any prompt templete as you wish.
    # Chek prompts folder for more information.
    prompt = load_assistant_prompt(prompt)

    # Prepare agent chain for ai-assistant.
    agent = LLMChain(
        # You can change model to gpt-4 as well.
        llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2),
    )

    return agent

# class GPTAgent():
#     def __init__(self) -> None:
#         self.agent = build_gpt_agent()
        