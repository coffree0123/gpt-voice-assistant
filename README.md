# gpt-voice-assistant

## frontend
### Prerequisite
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install 16
```

### Build
```{bash}
cd frontend
npm install
npm run build
```

## backend
### Prerequisite
1. Copy .env_templete to .env and add your openai api key.
2. Install the requirement package. (Recommend **python 3.9** above version)
    ```
    pip install -r requirements.txt
    ```
### Usage
```{bash}
cd backend
uvicorn server:app
```
### Common error
1. ERROR: Could not build wheels for PyAudio, which is required to install pyproject.toml-based projects
solution (**Test on m1 pro macbook**):
    ```
    brew update
    brew install portaudio
    pip install pyaudio
    ```