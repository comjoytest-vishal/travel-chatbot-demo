import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from company_knowledge import COMPANY_KNOWLEDGE


load_dotenv()

app = FastAPI()


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://travel-chatbot-demo-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Travel Chatbot Backend is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    prompt = f"""
{COMPANY_KNOWLEDGE}

Customer question:
{request.question}

Answer the customer politely.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return {
        "answer": interaction.output_text
    }