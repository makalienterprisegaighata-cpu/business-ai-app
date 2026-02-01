from fastapi import FastAPI
import sqlite3
from auth import router as auth_router
app = FastAPI(title="Vyapar AI")
app.include_router(auth_router)
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
# ---------- Add Transaction ----------
@app.post("/transaction/add")
def add_transaction(customer_id: int, amount: float, note: str = ""):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            amount REAL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT INTO transactions (customer_id, amount, note) VALUES (?, ?, ?)",
        (customer_id, amount, note)
    )

    db.commit()
    return {"status": "Transaction added successfully 💸"}
# ---------- List Transactions by Customer ----------
@app.get("/transactions/{customer_id}")
def get_transactions(customer_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, amount, note, created_at FROM transactions WHERE customer_id = ?",
        (customer_id,)
    )
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "amount": row[1],
            "note": row[2],
            "date": row[3]
        })

    return {
        "customer_id": customer_id,
        "transactions": data
    }
# ---------- List Transactions by Customer ----------
@app.get("/transactions/{customer_id}")
def get_transactions(customer_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, amount, note, created_at FROM transactions WHERE customer_id = ?",
        (customer_id,)
    )
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "amount": row[1],
            "note": row[2],
            "date": row[3]
        })

    return {
        "customer_id": customer_id,
        "transactions": data
    }
from fastapi.responses import FileResponse
from fpdf import FPDF
import os

# ===== OPTION A: BALANCE API =====
@app.get("/balance/{customer_id}")
def get_balance(customer_id: int):
    conn = sqlite3.connect("vyapar.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM customers WHERE id=?", (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        return {"error": "Customer not found"}

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE customer_id=?",
        (customer_id,)
    )
    total = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "customer_id": customer_id,
        "customer_name": customer[0],
        "total_balance": total
    }


# ===== OPTION B: PDF STATEMENT =====
@app.get("/statement/pdf/{customer_id}")
def generate_pdf(customer_id: int):
    conn = sqlite3.connect("vyapar.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM customers WHERE id=?", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        return {"error": "Customer not found"}

    cursor.execute(
        "SELECT amount, note, date FROM transactions WHERE customer_id=?",
        (customer_id,)
    )
    transactions = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Vyapar AI Statement", ln=True)
    pdf.cell(200, 10, txt=f"Customer: {customer[0]}", ln=True)
    pdf.ln(10)

    total = 0
    for t in transactions:
        amount, note, date = t
        total += amount
        pdf.cell(200, 10, txt=f"{date} | {amount} | {note}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Balance: {total}", ln=True)

    filename = f"statement_{customer_id}.pdf"
    pdf.output(filename)

    return FileResponse(filename, media_type="application/pdf", filename=filename)
