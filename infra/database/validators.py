FORBIDDEN_KEYWORDS = {
    "DROP",
    "DELETE",
    "ALTER",
    "UPDATE",
    "INSERT",
    "TRUNCATE",
}

def validate_sql(sql: str) -> None:
    """
    Ensures only read-only SQL statements are executed.
    Raises ValueError if a forbidden keyword is detected.
    """
    sql_upper = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            raise ValueError(
                f"Forbidden SQL keyword detected: {keyword}. "
                "Only read-only queries are allowed."
            )
