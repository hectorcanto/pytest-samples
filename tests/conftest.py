import sys

from loguru import logger

NEW_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
    "- <level>{message}</level>"
)


def configure_stdout_log():
    logger.remove()
    logger.configure(
        handlers=[dict(sink=sys.stdout, format=NEW_FORMAT, diagnose=False, level="DEBUG")]
    )


def pytest_configure(config):
    """Replace default logger and report configuration through stdout"""
    logger.remove()
    logger.add(sys.stdout, filter=__name__, format="<level>{message}</level>")
    logger.level("DEBUG", color="<cyan>")
    logger.level("INFO", color="<light-blue>")
    logger.debug("Running pytest pre-configuration")
    logger.critical(f"Current level is {logger._core.min_level}")  # pylint:disable=protected-access
    logger.info(config.inicfg["env"].replace("\n", " ") + "\n")

    configure_stdout_log()


def pytest_collection_modifyitems(items):
    """Adds marker to all tests in these submodules

    Use it with 'pytest -m unit'
    """
    for item in items:
        if "/integration/" in str(item.module):
            item.add_marker("integration")
        elif "/unit/" in str(item.module):
            item.add_marker("unit")
        elif "/smoke/" in str(item.module):
            item.add_marker("smoke")
        elif "/api/" in str(item.module):
            item.add_marker("api")
