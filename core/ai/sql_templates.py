SQL_TEMPLATES = {
    "AGGREGATION": {
        "total_expense": "SELECT SUM(amount) AS total_expense FROM transactions;",
        "category_summary": """
            SELECT category, SUM(amount) AS total
            FROM transactions
            GROUP BY category
            ORDER BY total DESC;
        """
    },
    "LISTING": {
        "all_transactions": "SELECT * FROM transactions LIMIT 100;"
    }
}
