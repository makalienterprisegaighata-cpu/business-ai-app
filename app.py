from fastapi import FastAPI, Body
import requests

app = FastAPI(title="Vyapar AI")

BASE_URL = "https://business-ai-app.onrender.com"

@app.get("/")
def home():
    return {"message": "Welcome to Vyapar AI 🚀"}

# ---------- EXISTING BUSINESS APIs ----------

@app.post("/customer/add")
def add_customer(name: str, phone: str):
    res = requests.post(f"{BASE_URL}/customer/add?name={name}&phone={phone}")
    return res.json()

@app.get("/customers")
def list_customers():
    res = requests.get(f"{BASE_URL}/customers")
    return res.json()

@app.get("/balance/{customer_id}")
def get_balance(customer_id: int):
    res = requests.get(f"{BASE_URL}/balance/{customer_id}")
    return res.json()

# ---------- AI BRAIN ----------

@app.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question", "").lower()

    # Very simple NLP logic (version 1)
    if "rahul" in question and ("balance" in question or "বাকি" in question):
        res = requests.get(f"{BASE_URL}/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা 💰"
        }

    if "customer" in question or "কাস্টমার" in question:
        res = requests.get(f"{BASE_URL}/customers")
        return {
            "answer": "এইগুলো আপনার সব কাস্টমার 👇",
            "data": res.json()
        }

    return {
        "answer": "দুঃখিত, আমি প্রশ্নটা বুঝতে পারিনি 🤔"
    }
