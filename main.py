from openai import OpenAI
from keys import API_KEY
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import Annotated
import uvicorn

app = FastAPI()

openai = OpenAI(
    api_key = API_KEY
)

templates = Jinja2Templates(directory='templates')

@app.get("/", response_class = HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



#----------------------------------------------------------------------------------------
chat_log = []

chat_responses = []

@app.post("/", response_class = HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = chat_log,
        temperature = 0.6
    )

    gpt_response = response.choices[0].message.content
    chat_log.append({'role':'assistant', 'content': gpt_response})
    chat_responses.append(gpt_response)
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
































# while True:

#     user_input = input()

#     if user_input.lower() == 'stop':
#         break

#     chat_log.append({'role': 'user', 'content': user_input})

#     response = openai.chat.completions.create(
#     model = 'gpt-3.5-turbo',
#     messages = chat_log,
#     temperature = 0.6
#     )
#     bot_response = response.choices[0].message.content
#     chat_log.append({'role': 'assistant', 'content': bot_response})
#     print(bot_response)