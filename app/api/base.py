import logging
from typing import Any, Dict
import aiohttp
from aiohttp import ClientTimeout

logger = logging.getLogger(__name__)


class YandexAPIError(Exception):
    """Базовое исключение для ошибок Yandex API."""
    pass


class BaseYandexClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = ClientTimeout(total=10)
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None,
                       headers: Dict[str, str] = None) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"

        # Объединяем заголовки
        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        try:
            async with session.request(method, url, params=params, headers=request_headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    raise YandexAPIError("Неверные параметры запроса или локация не найдена (400)")
                elif response.status == 401:
                    raise YandexAPIError("Недействительный API-ключ (401)")
                elif response.status in (403, 429):
                    raise YandexAPIError("Превышен лимит запросов Yandex API (403/429)")
                else:
                    response.raise_for_status()
        except aiohttp.ClientError as e:
            logger.error(f"Network error during Yandex API request: {e}")
            raise YandexAPIError(f"Ошибка сети при запросе к Yandex API: {e}")