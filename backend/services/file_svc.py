"""Сервис работы с файлами."""
import json
import os
from typing import List

class FileSVC:
    """Класс сервиса для работы с файлами."""

    def __init__(self, filename: str):
        self.filename = filename


    def resolve_data(self) -> List[str]|None:
        """Парсит файл и возвращает список информативных сообщений."""
        result = []
        with open(self.filename, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return None

        if not isinstance(data, dict) or "messages" not in data:
            return None

        messages = data["messages"]
        if not isinstance(messages, list):
            return None

        for msg in messages:
            if isinstance(msg, dict) and "text" in msg:
                text = msg["text"]
                if isinstance(text, str) and text.strip():
                    result.append(text.strip())

        f.close()
        return result
    

    def clean_file(self) -> None:
        """Удаляет файл."""
        os.remove(self.filename)