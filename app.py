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

    # Simple AI Logic v1
    if "rahul" in question and "balance" in question:
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট ব্যালেন্স হলো {balance} টাকা 💰"
        }

    if "customers" in question:
        res = requests.get("https://business-ai-app.onrender.com/customers")
        customers = res.json()
        return {
            "answer": f"মোট {len(customers)} জন কাস্টমার আছে 👥"
        }

    return {
        "answer": "দুঃখিত 😅, আমি প্রশ্নটা বুঝতে পারিনি"
    }
