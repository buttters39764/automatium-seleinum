import logging
from datetime import datetime
from pathlib import Path

from automation.config.config import EnableDebugLogging, LogDirectory

_LOGGER_NAME = "automation"
_CONFIGURED = False


def _build_log_file_path() -> Path:
    log_dir = Path(LogDirectory)
    log_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    return log_dir / f"{date_str}.log"


def setup_logging():
    global _CONFIGURED
    if _CONFIGURED:
        return logging.getLogger(_LOGGER_NAME)

    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.handlers.clear()

    console_level = logging.DEBUG if EnableDebugLogging else logging.INFO

    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(logging.Formatter("%(message)s"))

    fh = logging.FileHandler(_build_log_file_path(), encoding="utf-8")
    fh.setLevel(logging.DEBUG if EnableDebugLogging else logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    logger.addHandler(ch)
    logger.addHandler(fh)

    _CONFIGURED = True
    logger.info("[INFO] Logging inicializálva.")
    if EnableDebugLogging:
        logger.debug("[DEBUG] Debug logging engedélyezve.")
    return logger


def get_logger():
    return logging.getLogger(_LOGGER_NAME)


def info(msg: str):
    get_logger().info(msg)


def debug(msg: str):
    get_logger().debug(msg)


def warning(msg: str):
    get_logger().warning(msg)


def error(msg: str):
    get_logger().error(msg)


def exception(msg: str):
    get_logger().exception(msg)