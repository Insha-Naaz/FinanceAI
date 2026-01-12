# main.py
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd

CURRENCY_RATES = {
    "INR": 1.0,
    "USD": 0.012,  # approx
    "EUR": 0.011   # approx
}

def convert_currency(amount, currency):
    rate = CURRENCY_RATES.get(currency, 1.0)
    return amount * rate


# --- Session initialization ---
if "user" not in st.session_state:
    st.session_state.user = None

from infra.database.queries import run_query
from infra.ai_logger import ai_logger
from services.auth_service import authenticate, require_permission
from config.settings import settings
from core.ai.intent_classifier import classify_intent, QueryIntent
from core.ai.sql_generator import generate_sql

def handle_user_query(user_text: str) -> str:
    """
    Safely process user queries for supported intents.
    Returns a human-readable result string.
    """
    try:
        intent = classify_intent(user_text)
        ai_logger.info(f"INTENT ROUTED TO EXECUTION: {intent}")

        # TOTAL
        if intent == QueryIntent.TOTAL:
            df = run_query("SELECT SUM(amount) AS total FROM transactions")
            if not df.empty and df.iat[0, 0] is not None:
                return f"Total Amount: {df.iat[0, 0]:.2f}"
            return "No transactions found."

        # COUNT
        elif intent == QueryIntent.COUNT:
            df = run_query("SELECT COUNT(*) AS count FROM transactions")
            if not df.empty:
                return f"Total Transactions: {int(df.iat[0, 0])}"
            return "No transactions found."

        # AVERAGE
        elif intent == QueryIntent.AVERAGE:
            df = run_query("SELECT AVG(amount) AS average FROM transactions")
            if not df.empty and df.iat[0, 0] is not None:
                return f"Average Amount: {df.iat[0, 0]:.2f}"
            return "No data available to calculate average."

        # MINIMUM
        elif intent == QueryIntent.MINIMUM:
            df = run_query("SELECT MIN(amount) AS minimum FROM transactions")
            if not df.empty and df.iat[0, 0] is not None:
                return f"Minimum Amount: {df.iat[0, 0]}"
            return "No data available."

        # MAXIMUM
        elif intent == QueryIntent.MAXIMUM:
            df = run_query("SELECT MAX(amount) AS maximum FROM transactions")
            if not df.empty and df.iat[0, 0] is not None:
                return f"Maximum Amount: {df.iat[0, 0]}"
            return "No data available."
        #time series
        elif intent == QueryIntent.TIME_SERIES:
            df = run_query(
        """
        SELECT DATE(date) AS day, SUM(amount) AS total
        FROM transactions
        GROUP BY DATE(date)
        ORDER BY DATE(date)
        """
                    )
            if not df.empty:
                return df.to_string(index=False)
            return "No time-series data available."
            # FILTERED LIST
        elif intent == QueryIntent.FILTERED_LIST:
            sql = generate_sql(user_text)
            if not sql:
                return "unable to generate valid query."
            df = run_query(sql)
            if not df.empty:
                return df.to_string(index=False)
            return "No matching transactions found."

        # RECENT TRANSACTIONS
        elif intent == QueryIntent.RECENT_TRANSACTIONS:
            df = run_query(
                """
                SELECT date, category, amount
                FROM transactions
                ORDER BY date DESC
                LIMIT 10
                """
            )   
            if not df.empty:
                return df.to_string(index=False)
            return "No recent transactions found."

        # TOP CATEGORY
        elif intent == QueryIntent.TOP_CATEGORY:
            df = run_query(
                """
                SELECT category, SUM(amount) AS total
                FROM transactions
                GROUP BY category
                ORDER BY total DESC
                LIMIT 1
                """
            )
            if not df.empty:
                category = df.iloc[0][0]
                total = df.iloc[0][1]
                return f"Top Category: {category} (Total: {total})"
            return "No transaction data available."

        # FALLBACK
        else:
            return f"Intent '{intent.value}' is recognized but not yet implemented."

    except Exception as e:
        ai_logger.exception(f"Failed to process query '{user_text}'")
        return "An internal error occurred while processing your query."

        
# --- Login UI ---
if st.session_state.user is None:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()


st.title("AI-Powered Finance SQL Analyst")
st.sidebar.title("Finance AI Assistant")
st.sidebar.caption(f"Environment: {settings.app_env}")
st.sidebar.subheader("Currency")
currency = st.sidebar.selectbox("Display amounts in", ["INR", "USD", "EUR"])

st.subheader("Finance Dashboard")
try:
    require_permission(st.session_state.user, "query")
except PermissionError as pe:
    st.error(str(pe))
    st.stop()

with st.spinner("Loading dashboard..."):
    total_expense_df = run_query("SELECT SUM(amount) AS total FROM transactions")
    count_df = run_query("SELECT COUNT(*) AS count FROM transactions")
    category_df = run_query(
        """
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
        """
    )
    # Category-wise spending for chart
    category_chart_df=run_query( 
         """
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
        """
    )

col1, col2, col3 = st.columns(3)

with col1:
    total_amount = total_expense_df.iloc[0]["total"]
    converted_total = convert_currency(total_amount, currency)
    symbol = "₹" if currency == "INR" else "$" if currency == "USD" else "€"

    st.metric(
        "Total Expense",
        f"{symbol} {converted_total:.2f}"
    )

with col2:
    st.metric("Transactions", int(count_df.iloc[0]['count']))

with col3:
    if not category_df.empty:
        # Safe access: use column names if columns exist, else numeric index
        if "category" in category_df.columns:
            top_category = category_df.iloc[0]["category"]
        else:
            top_category = category_df.iloc[0][0]  # fallback

        st.metric("Top Category", top_category)
    else:
        st.metric("Top Category", "No data")
st.subheader("Spending by Category")

if category_chart_df.empty:
    st.info("No category data available.")
elif "category" in category_chart_df.columns and "total" in category_chart_df.columns:
    st.bar_chart(
        category_chart_df.set_index("category")["total"]
    )
else:
    st.error("Category chart data is not in expected format.")

st.subheader("Daily Expense Trend")

time_series_df = run_query(
    """
    SELECT DATE(date) AS day, SUM(amount) AS total
    FROM transactions
    GROUP BY DATE(date)
    ORDER BY DATE(date)
    """
)

if not time_series_df.empty:
    st.line_chart(
        data=time_series_df.set_index("day")["total"]
    )
else:
    st.info("No time-series data available.")


st.divider()

st.sidebar.markdown(
    """
    **What this app does**
    - Ask questions in plain English  
    - Converts them into SQL  
    - Instantly analyzes your finance data  
    """
)

st.sidebar.divider()

st.sidebar.subheader("Example Questions")
st.sidebar.markdown(
    """
    - Total expenses  
    - Top spending categories  
    - Show all transactions  
    """
)

# Input natural language query
st.subheader("Ask a Question")

user_query = st.text_input(
    "What do you want to know about your finances?",
    placeholder="e.g. Total expenses this month"
)
if user_query:
    st.subheader("Generated SQL")
    try:
        # 1️⃣ Enforce RBAC FIRST
        require_permission(st.session_state.user, "query")

        result_text = handle_user_query(user_query)
        st.success(result_text)
        st.stop()
    except PermissionError as pe:
        st.error(str(pe))
        st.stop()
    except Exception as e:
        st.error(f"Failed to process your query: {e}")

