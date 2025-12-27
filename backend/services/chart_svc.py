"""Сервис работы с графикой."""
from collections import Counter
from typing import List, Dict
from io import BytesIO
import matplotlib.pyplot as plt


class ChartSVC:
    """Класс сервиса для работы с графиками."""


    def __init__(self, categories: Dict[int, str], title: str = "Распределение категорий сообщений"):
        self.categories = categories
        self.title = title

    def create_pie_chart(self, predictions: List[int]) -> BytesIO:
        """Создает круговую диаграмму с классификацией."""
        counter = Counter(predictions)

        total_categories = len(self.categories)
        counts = [counter.get(cat_id, 0) for cat_id in range(1, total_categories + 1)]
        labels = [self.categories[cat_id] for cat_id in range(1, total_categories + 1)]
        plt.figure(figsize=(8, 8))
        plt.pie(
            counts,
            labels=labels,
            autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
            startangle=90,
            textprops={'fontsize': 10}
        )

        plt.title(self.title, fontsize=14, pad=20)
        plt.axis('equal')

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches='tight')
        plt.close()
        buf.seek(0)

        plt.close()
        return buf