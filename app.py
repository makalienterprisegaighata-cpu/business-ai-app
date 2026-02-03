from fastapi.middleware.cors import CORSMiddlewarefrom fastapi import FastAPI, Body
import requests
import sqlite3

app = FastAPI(title="Vyapar AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------- Database ----------
def get_db():
    conn = sqlite3.connect("business.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Home ----------
@app.get("/")
def home():
    return {"message": "Welcome to Vyapar AI 🚀"}

# ---------- Add Customer ----------
@app.post("/customer/add")
def add_customer(name: str, phone: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
    db.commit()
    return {"status": "Customer added successfully ✅"}

# ---------- List Customers ----------
@app.get("/customers")
def list_customers():
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT * FROM customers").fetchall()
    return [dict(row) for row in rows]

# ---------- Get Balance ----------
@app.get("/balance/{customer_id}")
def get_balance(customer_id: int):
    db = get_db()
    cur = db.cursor()
    row = cur.execute(
        "SELECT name, balance FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()

    if not row:
        return {"error": "Customer not found"}

    return {
        "customer_id": customer_id,
        "customer_name": row["name"],
        "total_balance": row["balance"]
    }

# ---------- AI Brain ----------
@app.post("/ai/ask")
def ai_ask(data: dict = Body(...)):
    question = data.get("question", "").lower()

    # simple logic
    if "rahul" in question and "বাকি" in question:
        res = requests.get("https://business-ai-app.onrender.com/balance/1")
        info = res.json()
        balance = info.get("total_balance", 0)

        return {
            "answer": f"Rahul এর মোট বাকি আছে {balance} টাকা 💰"
        }

    return {
        "answer": "দুঃখিত 😅 আমি এখনো এই প্রশ্নটা বুঝতে পারিনি"
    }
