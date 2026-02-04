# Classic Health Checks

[![PyPI version](https://badge.fury.io/py/classic-health-checks.svg)](https://badge.fury.io/py/classic-health-checks)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Простая реализация проверки работоспособности сервиса (liveness probe) через обновление временной метки файла.

Этот пакет предоставляет задачу, которая может быть запущена в отдельном потоке или гринлете для периодического обновления файла на диске. Внешние системы мониторинга, такие как Kubernetes или systemd, могут отслеживать время последнего изменения этого файла, чтобы убедиться, что сервис активен и не завис.

## Установка

```bash
pip install classic-health-checks
```

## Использование (Usage)

Вот минимальный пример использования `HealthCheckTask` в отдельном потоке.


### Использование с `gevent`

Для использования с `gevent` убедитесь, что он установлен:
```bash
pip install gevent
```

`HealthCheckTask` легко интегрируется с `gevent`. Инициализируем и запускаем run в гринлете.
```python
import gevent
from gevent.monkey import patch_all

patch_all()

import logging
from pydantic_settings import BaseSettings
from classic.health_checks import HealthCheckTask, HealthCheckSettingsMixin

# Настройте базовый логгер
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AppSettings(HealthCheckSettingsMixin, BaseSettings):
   ...

settings = AppSettings()

# 1. Создаем экземпляр

health_check = HealthCheckTask(
    logger=logger,
    settings=settings,
)

# 2. Запускаем HealthCheckTask и другие задачи в своих гринлетах

# Псевдо-задачи для примера
class LongRunningTask:
    def __init__(self, name: str):
        self.name = name
    def run(self):
        logger.info(f"Задача '{self.name}' запущена.")
        while True:
            gevent.sleep(60)

task1 = LongRunningTask("Обработчик сообщений")
task2 = LongRunningTask("Сборщик метрик")

all_greenlets = [
    gevent.spawn(health_check.run),
    gevent.spawn(task1.run),
    gevent.spawn(task2.run),
]

logger.info(f"Запущено {len(all_greenlets)} гринлетов, включая HealthCheck.")

# 3. Ожидаем завершения всех задач и обрабатываем остановку
try:
    gevent.joinall(all_greenlets, raise_error=True)
except (KeyboardInterrupt, SystemExit):
    logger.info("Получен сигнал остановки, завершаем все гринлеты...")
    gevent.killall(all_greenlets)
    logger.info("Приложение остановлено.")

```

> **Подсказка:** "Сигнал остановки" обычно отправляется нажатием `Ctrl+C` в терминале, где запущен скрипт.

### Интеграция с Kubernetes

Вы можете использовать этот механизм для настройки `livenessProbe` в вашем Helm-чарте:

```yaml
# ... внутри spec.template.spec.containers[]
# Добавляем переменную окружения, чтобы она была доступна в livenessProbe
env:
- name: HEALTHCHECK_FILE_PATH
  value: /tmp/my_app_healthy
  
  
envsFromSecret:
  secret-envs:
    ...
livenessProbe:
  exec:
    command:
    - /bin/sh
    - -c
    - "[ $(($(date +%s) - $(stat -c %Y $HEALTHCHECK_FILE_PATH))) -le 10 ]"
  periodSeconds: 10
  initialDelaySeconds: 30
  failureThreshold: 3
```
