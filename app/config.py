# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    VERTEX_API_KEY = os.getenv('VERTEX_API_KEY')