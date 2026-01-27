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
