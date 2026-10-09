import json
import hashlib
import logging
from functools import wraps
from typing import Any, Callable
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# Глобальный клиент Redis (переиспользуем соединение)
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def cache_response(ttl: int = 1800):
    """Декоратор для кэширования результатов асинхронных функций."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Формируем уникальный ключ кэша из имени функции и аргументов
            cache_key = f"{func.__name__}:{hashlib.md5(json.dumps(kwargs, sort_keys=True).encode()).hexdigest()}"

            try:
                # Проверяем кэш
                cached_data = await redis_client.get(cache_key)
                if cached_data:
                    logger.debug(f"Cache HIT: {cache_key}")
                    return json.loads(cached_data)
            except redis.RedisError as e:
                logger.warning(f"Redis connection error, bypassing cache: {e}")

            # Если кэша нет, выполняем функцию
            result = await func(*args, **kwargs)

            # Сохраняем результат в кэш
            try:
                await redis_client.setex(cache_key, ttl, json.dumps(result))
                logger.debug(f"Cache SET: {cache_key} (TTL: {ttl}s)")
            except redis.RedisError as e:
                logger.warning(f"Failed to set cache: {e}")

            return result

        return wrapper

    return decorator