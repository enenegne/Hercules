import os
KEY = os.environ['KEY']

base_url = "https://api.telegram.org/bot"

from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

class sendMessage(BaseModel):
    update_id: int
    message: dict

def get_response(user_input):
    return user_input

@app.get("/")
def read_route():
    return "Chat Bot is UP"

@app.post("/")
def chatbot(in_message: sendMessage):
    value = in_message.message
    text = value['text']
    bot_says = get_response(text)
    id = value["from"]["id"]
    url = f"{base_url}{KEY}/sendMessage"
    requests.post(url, params={"chat_id": id, "text": bot_says})
    return None
    