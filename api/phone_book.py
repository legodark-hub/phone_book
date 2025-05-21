from fastapi import APIRouter, HTTPException, Query
import redis.asyncio as aioredis
from config import REDIS_URL
from schemas.contact import DataItem, PhoneResponse

router = APIRouter()

redis_client = aioredis.from_url(REDIS_URL)


@router.post(
    "/write_data",
    summary="Запись или обновление данных",
    description="Сохраняет или обновляет адрес по указанному номеру телефона в Redis.",
)
async def write_data(item: DataItem):
    """
    Записывает или обновляет данные (телефон-адрес) в Redis.
    Ключом в Redis является номер телефона.
    """
    if not redis_client:
        raise HTTPException(status_code=503, detail="Сервис Redis недоступен.")
    try:
        await redis_client.set(item.phone, item.address)
        return {
            "message": "Данные успешно записаны/обновлены",
            "phone": item.phone,
            "address": item.address,
        }
    except Exception as e:
        print(f"Ошибка при записи данных в Redis: {e}")
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера при записи данных."
        )


@router.get(
    "/check_data",
    response_model=PhoneResponse,
    summary="Получение данных по номеру телефона",
    description="Ищет адрес по номеру телефона в Redis и возвращает его.",
)
async def check_data(
    phone: str = Query(
        ..., description="Номер телефона для поиска", example="89090000000"
    ),
):
    """
    Получает адрес из Redis по указанному номеру телефона.
    """
    if not redis_client:
        raise HTTPException(status_code=503, detail="Сервис Redis недоступен.")
    try:
        address = await redis_client.get(phone)
        if address is None:
            return PhoneResponse(phone=phone, address=None)
        return PhoneResponse(phone=phone, address=address)
    except Exception as e:
        print(f"Ошибка при чтении данных из Redis: {e}")
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера при чтении данных."
        )
