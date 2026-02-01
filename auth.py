from fastapi import APIRouter
import sqlite3
import hashlib

router = APIRouter()

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

@router.post("/auth/register")
def register(name: str, email: str, password: str):
    conn = sqlite3.connect("vyapar.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (NULL,?,?,?)",
              (name, email, hash_password(password)))
    conn.commit()
    conn.close()
    return {"status": "User registered successfully"}

@router.post("/auth/login")
def login(email: str, password: str):
    conn = sqlite3.connect("vyapar.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hash_password(password)))
    user = c.fetchone()
    conn.close()

    if user:
        return {"status": "Login success", "user_id": user[0]}
    else:
        return {"error": "Invalid credentials"}
