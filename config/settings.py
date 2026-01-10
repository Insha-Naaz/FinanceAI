import os

ENV = os.getenv("FINANCEAI_ENV", "dev")

if ENV == "prod":
    from .prod_settings import *
else:
    from .dev_settings import *
# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Database configuration
DB_NAME = "finance.db"
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# Environment
APP_ENV = os.getenv("APP_ENV", "development")
class Settings:
    env = ENV
    base_dir = BASE_DIR
    data_dir = DATA_DIR
    db_name = DB_NAME
    db_path = DB_PATH
    app_env = APP_ENV

settings = Settings()
