import logging
import os

main_logger = None


def _get_logger() -> logging.Logger:
    """
    Get a logger instance.
    Returns:
        logging.Logger: Logger instance.
    """
    global main_logger

    if main_logger is not None:
        return main_logger

    main_logger = logging.getLogger("main_logger")
    return main_logger


def start_logger():
    """
    Start the logger with specified level
    """
    logger = _get_logger()

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, level, logging.INFO)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.info(f"Logger started with level: {level}")


def log_info(message: str):
    logger = _get_logger()
    logger.info(message)


def log_error(message: str):
    logger = _get_logger()
    logger.error(message)


def log_debug(message: str):
    logger = _get_logger()
    logger.debug(message)
