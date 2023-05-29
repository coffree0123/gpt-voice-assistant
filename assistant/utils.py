import subprocess
from sys import platform
from langchain.tools import YouTubeSearchTool


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


class VideoSearchTool():
    def __init__(self) -> None:
        self.tool = YouTubeSearchTool()

    def run(self, search_name: str) -> str:
        result = self.tool.run(f"{search_name},{1}").replace(
            '"', '').replace('\'', '')
        result = result.replace('[', '').replace(']', '')
        result = result.split(', ')
        urls = [f"https://www.youtube.com/{res}" for res in result]

        return urls[0]
