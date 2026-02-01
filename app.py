from fastapi import FastAPI, Body
import requests

app = FastAPI()

# Home
@app.get("/")
def home():
    return {"message": "Welcome to Vyapar AI 🚀"}

# -------- AI BRAIN --------
@app.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question", "").lower()

    if "rahul" in question and ("বাকি" in question or "balance" in question):
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা"
        }

    return {
        "answer": "দুঃখিত, আমি প্রশ্নটা বুঝতে পারিনি 😅"
    }
