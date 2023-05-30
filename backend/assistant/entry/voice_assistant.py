import time
import speech_recognition as sr
from dotenv import load_dotenv
from assistant.utils import TTS
from assistant.agent import build_gpt_agent

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


def listen():
    agent = build_gpt_agent()
    # Prepare text-to-speech(TTS) model and ASR model.
    tts = TTS()
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
            tts.say(response_text)
            tts.runAndWait()


if __name__ == '__main__':
    listen()
