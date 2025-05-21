from schemas.contact import DataItem, PhoneResponse
from repositories.contact_repository import ContactRepository, get_contact_repository
from fastapi import Depends, HTTPException

class ContactService:
    def __init__(self, repository: ContactRepository = Depends(get_contact_repository)):
        self.repository = repository

    async def add_or_update_contact(self, item: DataItem) -> dict:
        """
        Записывает или обновляет данные (телефон-адрес).
        """
        try:
            await self.repository.set_contact(item.phone, item.address)
            return {
                "message": "Данные успешно записаны/обновлены",
                "phone": item.phone,
                "address": item.address,
            }
        except ConnectionError as e: 
            print(f"Ошибка соединения с Redis в сервисе при записи: {e}")
            raise HTTPException(status_code=503, detail="Сервис Redis недоступен.")
        except Exception as e:
            print(f"Ошибка при записи данных в сервисе: {e}")
            raise HTTPException(
                status_code=500, detail="Внутренняя ошибка сервера при записи данных."
            )

    async def get_contact_by_phone(self, phone: str) -> PhoneResponse:
        """
        Получает адрес по указанному номеру телефона.
        """
        try:
            address = await self.repository.get_contact_address(phone)
            return PhoneResponse(phone=phone, address=address)
        except ConnectionError as e: 
            print(f"Ошибка соединения с Redis в сервисе при чтении: {e}")
            raise HTTPException(status_code=503, detail="Сервис Redis недоступен.")
        except Exception as e:
            print(f"Ошибка при чтении данных в сервисе: {e}")
            raise HTTPException(
                status_code=500, detail="Внутренняя ошибка сервера при чтении данных."
            )