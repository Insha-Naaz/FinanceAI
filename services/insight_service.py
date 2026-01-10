import pandas as pd
from typing import List, Dict

def generate_insights(df) -> List[Dict]:
    insights = []
    if df.empty:
        return insights
    if "amount" in df.columns:
        avg_amount = df["amount"].mean()
        high_expenses = df[df["amount"] > avg_amount * 2]

        if not high_expenses.empty:
            insights.append({
                "type": "risk",
                "title": "High-Value Transactions Detected",
                "message": f"{len(high_expenses)} transactions exceed twice the average expense.",
                "recommendation": "Review these transactions for anomalies or approvals.",
            })
    if "category" in df.columns and "amount" in df.columns:
        category_totals = df.groupby("category")["amount"].sum()
        top_category = category_totals.idxmax()
        top_share = category_totals.max() / category_totals.sum()

        if top_share > 0.5:
            insights.append({
                "type": "warning",
                "title": "Spending Concentration Risk",
                "message": f"Over 50% of spending is in '{top_category}'.",
                "recommendation": "Evaluate vendor dependency and cost optimization opportunities.",
            })
    if "date" in df.columns and "amount" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        monthly = df.resample("M", on="date")["amount"].sum()

        if len(monthly) >= 2 and monthly.iloc[-1] > monthly.iloc[-2]:
            insights.append({
                "type": "info",
                "title": "Rising Expense Trend",
                "message": "Expenses increased compared to the previous month.",
                "recommendation": "Investigate drivers behind the increase and adjust budgets.",
            })

    return insights
