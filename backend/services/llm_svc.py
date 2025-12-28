"""Сервис работы с нейросетью."""
from typing import List, Dict
import json
import requests


class LLMSVC:
    """Класс сервиса для работы с нейросетью."""

    def __init__(self, api_url: str, api_key: str, model: str, categories: Dict[int, str]):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.categories = categories

    def _create_promt(self) -> str:
        """Создает основу для запроса в нейросеть."""
        categories_list = [f"{key}: {value}" for key, value in self.categories.items()]
        categories_string = """\n""".join(categories_list)
        return f"""Ты классификатор текста. Отвечай ТОЛЬКО одной цифрой от 1 до 6.

        Категории:
        {categories_string}

        Твоя задача: определить категорию сообщения.
        Ответ только цифрой (1-6), без объяснений. Даже если не уверен, все равно ответь одной цифрой."""
    

    def classify_data(self, data: List[str]) -> List[int]:
        """Проводит классификацию сообщений из списка и возвращает список классификации."""
        result = []
        promt_start = self._create_promt()
        for message in data:
            response = requests.post(
            url=f"{self.api_url}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            data=json.dumps({
                "model": f"{self.model}",
                "messages": [
                {
                    "role": "user",
                    "content": promt_start + "\n" + f"Текст для классификации: {message}"
                }
                ]
            })
            )
            if response.status_code != 200:
                print(response.text)
            answer_text = response.json()["choices"][0]["message"]["content"].strip()
            category = None
            for char in answer_text:
                if char.isdigit():
                    num = int(char)
                    category = num
                    break
            result.append(category)
        
        return result
