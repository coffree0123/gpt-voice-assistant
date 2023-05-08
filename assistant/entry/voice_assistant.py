import time
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from assistant.prompt.conversation import load_assistant_prompt

load_dotenv()  # take environment variables from .env.


def text_from_speech(recognizer, source):
    print('listening now...')
    try:
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
        print('Recognizing...')
        text = recognizer.recognize_google(audio)
    except Exception as e:
        unrecognized_speech_text = f'Sorry, I didn\'t catch that. Exception was: {e}s'
        text = unrecognized_speech_text

    return text


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
    # Prepare text-to-speech(TTS) model and ASR model.
    tts = pyttsx3.init()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while (True):
            # Step 1: Speech to text.
            text = text_from_speech(recognizer, source)

            # Step 2: Chatgpt response consider input text.
            response_text = agent.run(human_input=text)

            print(f"User: {text}")
            print(f"Response: {response_text}")

            # Step 3: Text to speech.
            time.sleep(1)
            tts.say(response_text)
            tts.runAndWait()


if __name__ == '__main__':
    listen()
