import time
from logging import Logger
from pathlib import Path

from .settings import BaseHealthCheckSettings


class HealthCheckTask:
    """
    Задача для выполнения проверки работоспособности путем обновления
    временной метки файла.

    Этот класс реализует простую проверку жизнеспособности (liveness probe).
    При запуске метода `run` он периодически обновляет указанный файл
    в файловой системе. Внешняя система мониторинга может отслеживать
    время последнего изменения этого файла, чтобы убедиться, что сервис
    активен и не завис.

    Аргументы:
        logger: Экземпляр стандартного логгера для вывода отладочных сообщений.
        settings: Объект конфигурации с параметрами для проверки.
    """

    def __init__(
        self,
        logger: Logger,
        settings: BaseHealthCheckSettings,
    ) -> None:
        self.logger = logger
        self.filepath = Path(settings.HEALTHCHECK_FILE_PATH)
        self.interval = settings.HEALTHCHECK_INTERVAL
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """
        Запускает бесконечный цикл проверки работоспособности.

        Этот метод выполняет бесконечный цикл, в котором:
        1. Обновляет временную метку файла проверки.
        2. Приостанавливает выполнение на заданный интервал.
        3. Логирует отладочное сообщение.
        """
        while True:
            self.filepath.touch()
            time.sleep(self.interval)
            self.logger.debug('Healthcheck file written')
