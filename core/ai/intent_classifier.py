from enum import Enum


class QueryIntent(Enum):
    TOTAL = "total"
    COUNT = "count"
    TOP_CATEGORY = "top_category"
    AVERAGE = "average"
    MINIMUM  ="minimum"
    MAXIMUM = "maximum"
    CATEGORY_BREAKDOWN = "category_breakdown" #group by category
    TIME_SERIES = "time_series" #trend over time
    FILTERED_LIST = "filtered_list" #filtered transactions
    RECENT_TRANSACTIONS = "recent_transactions"
    COMPARISON = "comparison" #compare two periods
    PREDICTION = "prediction"
    BUDGET_ALERTS = "budget_alerts" # budget exceeds check
    SUMMARY = "summary" #general overview
    LISTING = "listing" #show all records 
    AGGREGATION = "aggregation" #generic aggregation
    UNKNOWN = "unknown" 
 

# --- Keyword dictionaries (industry-style routing) ---
AGG_TOTAL_KEYWORDS = {"total", "sum", "overall", "spent", "expense", "expenses"}
AGG_COUNT_KEYWORDS = {"count", "number", "how many", "transactions"}
AGG_TOP_CATEGORY_KEYWORDS = {"top", "highest", "most", "category", "categories"}
AGG_AVERAGE_KEYWORDS = {"average", "mean"}
AGG_MINIMUM_KEYWORDS = {"minimum", "least", "smallest", "lowest"}
AGG_MAXIMUM_KEYWORDS = {"maximum", "largest", "highest"}
CATEGORY_BREAKDOWN_KEYWORDS = {"breakdown", "by category", "category-wise", "group by category"}
TIME_SERIES_KEYWORDS = {"trend", "over time", "daily", "weekly", "monthly", "time series"}
FILTERED_LIST_KEYWORDS = {"above", "below", "specific",}
RECENT_TRANSACTIONS_KEYWORDS = {"recent", "last", "latest", "most recent"}
COMPARISON_KEYWORDS = {"compare", "vs", "versus"}
BUDGET_ALERTS_KEYWORDS = {"budget", "limit", "exceed", "overspent"}
PREDICTION_KEYWORDS = {"forecast", "predict", "projection"}
AGGREGATION_KEYWORDS = { "aggregation", "group", "group"}
LISTING_KEYWORDS = {"show", "list", "all", "transactions", "records", "entries", "details"}
SUMMARY_KEYWORDS = {"summary", "overview", "insights", "analysis", "report"}

def classify_intent(user_text: str) -> QueryIntent:
    if not user_text or not user_text.strip():
        return QueryIntent.UNKNOWN

    text = user_text.lower()

    # 1️⃣ Business logic first
    if any(k in text for k in BUDGET_ALERTS_KEYWORDS):
        return QueryIntent.BUDGET_ALERTS

    if any(k in text for k in PREDICTION_KEYWORDS):
        return QueryIntent.PREDICTION

    # 2️⃣ Comparison & time-based
    if any(k in text for k in COMPARISON_KEYWORDS):
        return QueryIntent.COMPARISON

    if any(k in text for k in RECENT_TRANSACTIONS_KEYWORDS):
        return QueryIntent.RECENT_TRANSACTIONS

    if any(k in text for k in TIME_SERIES_KEYWORDS):
        return QueryIntent.TIME_SERIES

    # 3️⃣ Grouped aggregations
    if any(k in text for k in CATEGORY_BREAKDOWN_KEYWORDS):
        return QueryIntent.CATEGORY_BREAKDOWN

    # 4️⃣ Mathematical aggregations
    if any(k in text for k in AGG_AVERAGE_KEYWORDS):
        return QueryIntent.AVERAGE

    if any(k in text for k in AGG_MINIMUM_KEYWORDS):
        return QueryIntent.MINIMUM

    if any(k in text for k in AGG_MAXIMUM_KEYWORDS):
        return QueryIntent.MAXIMUM

    if any(k in text for k in AGG_COUNT_KEYWORDS):
        return QueryIntent.COUNT

    if any(k in text for k in AGG_TOTAL_KEYWORDS):
        return QueryIntent.TOTAL

    # 5️⃣ Category-based ranking
    if any(k in text for k in AGG_TOP_CATEGORY_KEYWORDS):
        return QueryIntent.TOP_CATEGORY

    # 6️⃣ Generic fallback aggregation
    if any(k in text for k in AGGREGATION_KEYWORDS):
        return QueryIntent.AGGREGATION
    # 7️⃣ Filtered list (important: before listing)
    if any(k in text for k in FILTERED_LIST_KEYWORDS):
        return QueryIntent.FILTERED_LIST

    # 7️⃣ Display intents
    if any(k in text for k in LISTING_KEYWORDS):
        return QueryIntent.LISTING

    if any(k in text for k in SUMMARY_KEYWORDS):
        return QueryIntent.SUMMARY

    return QueryIntent.UNKNOWN

    