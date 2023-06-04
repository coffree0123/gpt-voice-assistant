from fastapi import FastAPI
from assistant.agent import build_gpt_agent
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from fastapi import File, UploadFile
from starlette.responses import JSONResponse
import os
import json


class Text(BaseModel):
    text: str


load_dotenv()

app = FastAPI()

gpt_agent = build_gpt_agent()


@app.post("/api/text")
def chat(text: Text):
    response_text = gpt_agent.run(text.text)
    return {"response": response_text}


@app.post("/api/audio")
async def upload_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()

    try:
        # Save the file
        with open(f"{file.filename}", "wb") as buffer:
            buffer.write(await file.read())
        text = recognizer.recognize_google(buffer)
        print(text)
        # Return a response
        return JSONResponse(
            status_code=200, content={"detail": "Audio successfully uploaded!"}
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


@app.get("/api/tasks")
def get_tasks():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isfile('data/schedule.json'):
        return {
            "Mon": {},
            "Tue": {},
            "Wed": {},
            "Thu": {},
            "Fri": {},
            "Sat": {},
            "Sun": {},
        }
    with open('data/schedule.json', 'r') as f:
        schedule = json.load(f)
    return schedule


if os.environ.get("ENV") == "prod":
    app.mount("/", StaticFiles(directory="dist", html=True))
