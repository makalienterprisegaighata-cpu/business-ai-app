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
