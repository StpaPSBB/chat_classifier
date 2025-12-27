"""Эндпоинты."""
import json
import os
import uuid
from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from services.chart_svc import ChartSVC
from services.file_svc import FileSVC
from services.llm_svc import LLMSVC
from config import API_URL, API_KEY, MODEL, CATEGORIES


router = APIRouter(
    prefix="/classifier",
    tags=["classifier"],
    responses={404: {"description": "Not found"}},
)


def save_upload_file(upload_file: UploadFile) -> str:
    """Сохраняет загруженный файл и возвращает путь к нему."""
    file_id = str(uuid.uuid4())
    file_path = f"temp/{file_id}_{upload_file.filename}"

    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as f:
        content = upload_file.file.read()
        f.write(content)

    return file_path


@router.post("/classify")
async def classify_chat(file: UploadFile = File(..., description="JSON файл с историей чата")) -> StreamingResponse:
    """
    Основной эндпоинт для классификации чата.
    Загружает JSON, классифицирует сообщения, создает визуализацию.
    """

    if not file.filename.endswith('.json'): # type: ignore
        raise HTTPException(status_code=400, detail="Файл должен быть в формате JSON")

    temp_file_path = save_upload_file(file)

    try:
        file_svc = FileSVC(temp_file_path)
        messages = file_svc.resolve_data()

        if not messages:
            raise HTTPException(status_code=400, detail="В файле не найдено подходящих сообщений")

        llm_svc = LLMSVC(
            api_url=API_URL,
            api_key=API_KEY,
            model=MODEL,
            categories=CATEGORIES,
        )

        if len(messages) > 45:
            messages = messages[:45]  # Ограничение для демо-версии

        predictions = llm_svc.classify_data(messages)

        chart_svc = ChartSVC(categories=CATEGORIES)
        task_id = temp_file_path.split("/")[1].split("_")[0]

        chart_buffer = chart_svc.create_pie_chart(predictions)

        distribution = {}
        for cat_id, cat_name in CATEGORIES.items():
            count = predictions.count(cat_id)
            distribution[cat_name] = count

        file_svc.clean_file()
        return StreamingResponse(
            chart_buffer,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=classification_{task_id}.png",
                "X-Task-ID": task_id,
                "X-Distribution": json.dumps(distribution)
            }
        )
   
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")
