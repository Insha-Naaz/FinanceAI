import pandas as pd
from infra.database.connection import get_db_connection
from infra.database.logger import db_logger
from infra.database.validators import validate_sql

def run_query(sql: str) -> pd.DataFrame:
    validate_sql(sql)
    db_logger.info(f"Executing SQL: {sql}")

    try:
        with get_db_connection() as conn:
            df = pd.read_sql_query(sql, conn)
            db_logger.info("Query executed successfully")
            return df

    except Exception as e:
        db_logger.error(f"Query failed: {e}")
        raise
