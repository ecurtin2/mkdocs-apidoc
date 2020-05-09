from os import getenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s] %(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
)
log_level = getenv("MKDOCS_APIDOC_LOG_LEVEL", "WARN")

logger = logging.getLogger("mkdocs-apidoc")
logger.setLevel(log_level)

logger.debug("Set log level")
