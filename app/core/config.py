from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    YANDEX_WEATHER_API_KEY: str
    YANDEX_GPT_API_KEY: str
    YANDEX_FOLDER_ID: str

    # Настройки подключения к Redis (по умолчанию для локального Docker)
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()