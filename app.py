from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_NAME = "business.db"

@app.get("/")
def home():
    return {"status": "Business AI App is running 🚀✅"}

@app.get("/customers")
def get_customers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, phone FROM customers")
        rows = cursor.fetchall()
        return {"customers": rows}
    except:
        return {"customers": []}
    finally:
        conn.close()
@app.get("/ping")
def ping():
    return {"message": "pong 🏓"}
from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    phone: str

@app.post("/customers")
def add_customer(customer: Customer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)",
        (customer.name, customer.phone)
    )
    conn.commit()
    conn.close()
    return {"message": "Customer added successfully"}
