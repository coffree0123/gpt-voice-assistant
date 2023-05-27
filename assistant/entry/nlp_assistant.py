from dotenv import load_dotenv
from assistant.agent import build_gpt_agent

load_dotenv()  # take environment variables from .env.


def listen():
    agent = build_gpt_agent()
    while (True):
        text = input("Please enter your question: ")
        # Test for nlp agent.
        response_text = agent.run(text)

        print(f"User: {text}")
        print(f"Response: {response_text}")


if __name__ == '__main__':
    listen()
