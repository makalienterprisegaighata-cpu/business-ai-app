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
from fastapi import Body
import requests
import os

AI_API_KEY = os.getenv("OPENAI_API_KEY")  # Render env থেকে আসবে

@api.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question")

    # খুব simple NLP logic (first version)
    if "Rahul" in question and "বাকি" in question:
        # Backend থেকে balance আনো
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা।"
        }

    return {
        "answer": "দুঃখিত, আমি প্রশ্নটা বুঝতে পারিনি।"
    }
from fastapi import Body
import requests

@api.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question")

    # First version simple AI logic
    if "Rahul" in question and "বাকি" in question:
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা।"
        }

    return {
        "answer": "দুঃখিত, আমি প্রশ্নটা বুঝতে পারিনি।"
    }
