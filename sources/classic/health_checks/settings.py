from pydantic_settings import BaseSettings


class HealthCheckSettingsMixin:
    """
    Настройки конфигурации для задачи проверки работоспособности.

    Эти настройки могут быть загружены из переменных окружения или .env файла.
    """
    HEALTHCHECK_FILE_PATH: str = '/tmp/healthcheck'
    """Путь к файлу, используемому для проверки работоспособности."""

    HEALTHCHECK_INTERVAL: float = 10.0
    """Интервал в секундах между обновлениями файла проверки."""


class HealthCheckSettings(HealthCheckSettingsMixin, BaseSettings):
    ...
