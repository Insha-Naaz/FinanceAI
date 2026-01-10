from infra.ai_logger import ai_logger
from core.ai.intent_classifier import classify_intent, QueryIntent
from core.ai.sql_templates import SQL_TEMPLATES

def generate_sql(user_text: str) -> str:
    ai_logger.info(f"User Query: {user_text}")

    intent = classify_intent(user_text)
    ai_logger.info(f"Detected Intent: {intent}")

    if intent in {QueryIntent.AGGREGATION, QueryIntent.TOP_CATEGORY}:
        if "category" in user_text.lower():
            sql = SQL_TEMPLATES["AGGREGATION"]["category_summary"]
        else:
            sql = SQL_TEMPLATES["AGGREGATION"]["total_expense"]

    elif intent == QueryIntent.LISTING:
        sql = SQL_TEMPLATES["LISTING"]["all_transactions"]

    else:
        ai_logger.warning(f"Rejected query due to unsupported intent: {intent}")
        raise ValueError("Query intent not allowed.")

    ai_logger.info(f"Generated SQL: {sql}")
    return sql