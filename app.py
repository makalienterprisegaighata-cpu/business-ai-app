from fastapi import FastAPI, Body
import requests

app = FastAPI(title="Vyapar AI")

# -------------------------
# BASIC TEST ROUTE
# -------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Vyapar AI 🚀"}


# -------------------------
# CUSTOMER API (DUMMY)
# -------------------------
@app.post("/customer/add")
def add_customer(name: str, phone: str):
    return {"status": "Customer added successfully ✅"}


@app.get("/balance/{customer_id}")
def get_balance(customer_id: int):
    # Dummy data (later DB হবে)
    if customer_id == 1:
        return {
            "customer_id": 1,
            "customer_name": "Rahul",
            "total_balance": 2000
        }
    return {"error": "Customer not found"}


# -------------------------
# AI BRAIN (MAIN PART)
# -------------------------
@app.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question", "").lower()

    # Simple AI logic v1
    if "rahul" in question and ("বাকি" in question or "balance" in question):
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info["total_balance"]

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা।"
        }

    return {
        "answer": "দুঃখিত, আমি প্রশ্নটা বুঝতে পারিনি 😅"
    }
