import logging
from typing import Dict, Any
from app.api.base import BaseYandexClient, YandexAPIError
from app.core.cache import cache_response
from app.core.config import settings

logger = logging.getLogger(__name__)


class YandexWeatherClient(BaseYandexClient):
    def __init__(self):
        super().__init__(
            api_key=settings.YANDEX_WEATHER_API_KEY,
            base_url="https://api.weather.yandex.ru/v2"
        )

    @cache_response(ttl=1800)  # Кэшируем на 30 минут
    async def get_forecast(self, lat: float, lon: float, limit: int = 24) -> Dict[str, Any]:
        """Получает прогноз погоды по координатам."""
        # Округляем координаты до 2 знаков для унификации ключей кэша
        lat_rounded = round(lat, 2)
        lon_rounded = round(lon, 2)

        logger.info(f"Fetching weather for lat={lat_rounded}, lon={lon_rounded}")

        params = {
            "lat": lat_rounded,
            "lon": lon_rounded,
            "limit": limit,
            "hours": "true",
            "extra": "false"  # Отключаем лишние данные для экономии трафика и лимитов
        }

        headers = {
            "X-Yandex-API-Key": self.api_key
        }

        try:
            return await self._request("GET", "/forecast", params=params, headers=headers)
        except YandexAPIError as e:
            logger.error(f"Yandex Weather API error: {e}")
            raise