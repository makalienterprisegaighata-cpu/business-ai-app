from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# ===== CORS (MOST IMPORTANT) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== OpenAI Key =====
openai.api_key = os.getenv("OPENAI_API_KEY")

# ===== Home =====
@app.get("/")
def home():
    return {"message": "Welcome to Vyapar AI 🚀"}

# ===== AI Schema =====
class Question(BaseModel):
    question: str

# ===== AI Ask =====
@app.post("/ai/ask")
def ask_ai(data: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Vyapar AI, a helpful business assistant in Bengali."},
                {"role": "user", "content": data.question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
