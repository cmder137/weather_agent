# test_api.py
import asyncio
from app.api.weather import YandexWeatherClient

async def main():
    client = YandexWeatherClient()
    try:
        # Тестовые координаты (Москва)
        data = await client.get_forecast(lat=55.7558, lon=37.6173)
        print("Успех! Получены данные:", data.get("fact", {}).get("temp"))
    except Exception as e:
        print("Ошибка (ожидаемо, если ключ тестовый):", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())