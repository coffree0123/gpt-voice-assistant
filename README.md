# gpt-voice-assistant

## Prerequisite
1. Copy .env_templete to .env and add your openai api key.
2. Install the requirement package. (Recommend **python 3.9** above version)
    ```
    pip install -r requirements.txt
    ```
## Usage
```{bash}
python -m assistant.entry.voice_assistant
```
## Common error
1. ERROR: Could not build wheels for PyAudio, which is required to install pyproject.toml-based projects
solution (**Test on m1 pro macbook**):
    ```
    brew update
    brew install portaudio
    pip install pyaudio
    ```