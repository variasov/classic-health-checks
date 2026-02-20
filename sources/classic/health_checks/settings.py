from pydantic_settings import BaseSettings, SettingsConfigDict


class HealthCheckSettingsMixin:
    """
    Настройки конфигурации для задачи проверки работоспособности.

    Эти настройки могут быть загружены из переменных окружения или .env файла.
    """
    HEALTHCHECK_FILE_PATH: str
    """Путь к файлу, используемому для проверки работоспособности."""

    HEALTHCHECK_INTERVAL: float = 10.0
    """Интервал в секундах между обновлениями файла проверки."""


class HealthCheckSettings(HealthCheckSettingsMixin, BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )
