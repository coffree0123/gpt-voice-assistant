import time
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_assistant_prompt

load_dotenv()  # take environment variables from .env.


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


def listen():
    agent = build_gpt_agent()
    while (True):
        text = input("Please enter your question: ")
        # Test for nlp agent.
        response_text = agent.run(human_input=text)

        print(f"User: {text}")
        print(f"Response: {response_text}")


if __name__ == '__main__':
    listen()
