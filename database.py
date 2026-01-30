
from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Vyapar AI")

# ---------- Database ----------
def get_db():
    conn = sqlite3.connect("vyapar.db")
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
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    db.commit()
    return {"status": "Customer added successfully 💚"}

# ---------- List Customers ----------
@app.get("/customers")
def list_customers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    return {"customers": [dict(row) for row in rows]}
