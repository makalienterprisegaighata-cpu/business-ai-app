from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# CORS (HTML থেকে কল করার জন্য)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Vyapar AI Backend Running"}

@app.post("/ai/ask")
async def ask_ai(q: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "তুমি একজন ব্যবসায় সহায়ক বাংলা AI"},
                {"role": "user", "content": q.question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"answer": str(e)}
