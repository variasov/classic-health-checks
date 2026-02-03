import logging
import threading
import time
from pathlib import Path

from classic.health_checks import HealthCheckTask, BaseHealthCheckSettings

logger = logging.getLogger('test')


class TestSettings(BaseHealthCheckSettings):
    HEALTHCHECK_FILE_PATH: str
    HEALTHCHECK_INTERVAL: float = 0.1


def test_health_check_creates_directory(tmp_path: Path):
    """Тест: HealthCheckTask должен создавать родительскую директорию, если ее нет."""
    health_dir = tmp_path / "sub"
    health_file = health_dir / "healthy"
    settings = TestSettings(HEALTHCHECK_FILE_PATH=str(health_file))

    assert not health_dir.exists()

    HealthCheckTask(logger=logger, settings=settings)

    assert health_dir.exists()
    assert health_dir.is_dir()


def test_health_check_updates_file_timestamp(tmp_path: Path):
    """
    Тест: HealthCheckTask должен обновлять временную метку файла в цикле.
    """ 
    # Arrange
    settings = TestSettings(
        HEALTHCHECK_FILE_PATH=str(tmp_path / "healthy"),
        HEALTHCHECK_INTERVAL=0.05,
    )
    task = HealthCheckTask(logger=logger, settings=settings)

    thread = threading.Thread(target=task.run, daemon=True)
    thread.start()

    time.sleep(settings.HEALTHCHECK_INTERVAL * 1.5)
    first_mtime = task.filepath.stat().st_mtime

    time.sleep(settings.HEALTHCHECK_INTERVAL * 1.5)
    second_mtime = task.filepath.stat().st_mtime

    assert task.filepath.exists()
    assert second_mtime > first_mtime
