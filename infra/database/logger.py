import os
from loguru import logger

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "../../logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "db.log")

# Configure loguru sink (only once per process)
logger.add(
    LOG_FILE,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[component]} | {message}",
    rotation="5 MB",
)

# Database-scoped logger
db_logger = logger.bind(component="database")
