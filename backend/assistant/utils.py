import subprocess
from sys import platform


class MacTTS():
    def say(self, text: str):
        subprocess.call(['say', text])

    def runAndWait(self):
        pass


class TTS():
    def __init__(self) -> None:
        if platform == 'darwin':
            # Mac OS
            self.tts = MacTTS()
        else:
            import pyttsx3
            # Linux or windows
            self.tts = pyttsx3.init()

    def say(self, text: str):
        self.tts.say(text)

    def runAndWait(self):
        self.tts.runAndWait()
