import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def cargar_flujo(path="flujo.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_model():
    return ChatOpenAI(
        model="gpt-4.1-mini-2025-04-14",
        temperature=0.3,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
