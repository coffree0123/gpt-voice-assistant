import time
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_assistant_prompt

load_dotenv()  # take environment variables from .env.


def listen():
    # Prepare prompt for chatgpt agent. You can add any prompt templete as you wish.
    # Chek prompts folder for more information.
    prompt = load_assistant_prompt('en_assistant')

    # Prepare agent chain for ai-assistant.
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2),
    )

    r = sr.Recognizer()
    engine = pyttsx3.init()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print('Okay, go...')
        while (True):
            text = ''
            print('listening now...')
            try:
                audio = r.listen(source, timeout=6, phrase_time_limit=5)
                print('Recognizing...')
                text = r.recognize_google(audio)
            except Exception as e:
                unrecognized_speech_text = f'Sorry, I didn\'t catch that. Exception was: {e}s'
                text = unrecognized_speech_text

            response_text = chatgpt_chain.predict(human_input=text)

            print(f"User: {text}")
            print(f"Response: {response_text}")

            time.sleep(1)

            engine.say(response_text)
            engine.runAndWait()


if __name__ == '__main__':
    listen()
