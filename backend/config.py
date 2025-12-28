import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_NAME", "deepseek/deepseek-r1-distill-qwen-32b:free")

CATEGORIES = {
    1: "Организация",
    2: "Учёба",
    3: "Техническое",
    4: "Неформальное",
    5: "Вакансии",
    6: "Другое"
}
