from fastapi import FastAPI, Request
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"message": "Welcome to Vyapar AI 🚀"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    response = client.responses.create(
        model="gpt-5.2",
        input=f"You are Vyapar AI, a smart business assistant. Answer in simple Bengali.\nUser: {user_message}"
    )

    return {
        "reply": response.output_text
    }
