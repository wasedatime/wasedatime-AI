import openai

import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from decouple import config
import re

from dotenv import load_dotenv
load_dotenv() # loading .env file


OPENAI_API_KEY = config('OPENAI_API_KEY', default='default_value_if_not_found')
openai.api_key = OPENAI_API_KEY

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index(request: Request, topic: str= Form(...)):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful university student who suggest the responses of the topic only. Write in informal way like students, and not academic. Give out concise THREE responses based on the GIVEN_TOPIC. Do not repeat the examples."},
        {"role": "user", "content": "Example Topic: Academic"},
        {"role": "assistant", "content": "Examples: Which profs are the best for teaching Intro to Statistics? | Any easy classes I should register in the class course revision? | Why is it hard to join english-speaking Waseda circles?"},
       {"role": "user", "content": "Topic asked: " + generate_prompt(topic)}
            ])
    result = format_string(response['choices'][0]['message']['content'])

    return templates.TemplateResponse("index.html", {"request": request, "result": result})


def format_string(s: str) -> str:
    questions = re.split(r'\s?\|\s?', s)
    return '\n'.join(f"{i+1}. {question}" for i, question in enumerate(questions))


def generate_prompt(topic: str) -> str:
    return """
Topic: {}""".format(
        topic.capitalize()
    )

if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)