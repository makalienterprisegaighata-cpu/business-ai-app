import sqlite3
from datetime import datetime

DB_NAME = "business.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        balance REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount REAL,
        note TEXT,
        date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    conn.commit()
    conn.close()

def get_customers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_customer(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO customers (name, phone, balance) VALUES (?, ?, 0)",
        (name, phone)
    )
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    cur.execute("DELETE FROM transactions WHERE customer_id=?", (customer_id,))
    conn.commit()
    conn.close()

def add_transaction(customer_id, amount, note):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions (customer_id, amount, note, date) VALUES (?, ?, ?, ?)",
        (customer_id, amount, note, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )

    cur.execute(
        "UPDATE customers SET balance = balance + ? WHERE id=?",
        (amount, customer_id)
    )

    conn.commit()
    conn.close()

def get_transactions_by_customer(customer_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT amount, note, date FROM transactions WHERE customer_id=?",
        (customer_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
