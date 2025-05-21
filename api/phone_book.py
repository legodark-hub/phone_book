from fastapi import APIRouter, Depends, Query
from schemas.contact import DataItem, PhoneResponse
from services.contact_service import ContactService

router = APIRouter()

@router.post(
    "/write_data",
    summary="Запись или обновление данных",
    description="Сохраняет или обновляет адрес по указанному номеру телефона в Redis.",
)
async def write_data(
    item: DataItem, contact_service: ContactService = Depends(ContactService)
):
    """
    Записывает или обновляет данные (телефон-адрес) в Redis.
    Ключом в Redis является номер телефона.
    """
    return await contact_service.add_or_update_contact(item)


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
    contact_service: ContactService = Depends(ContactService),
):
    """
    Получает адрес из Redis по указанному номеру телефона.
    """
    return await contact_service.get_contact_by_phone(phone)
