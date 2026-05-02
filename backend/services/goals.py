def calculate_goal(target, months, df=None):
    if months <= 0:
        raise ValueError("Months must be greater than 0")
    monthly_required = target / months
    weekly_required = monthly_required / 4
    result = {
        "monthly_required": round(monthly_required, 2),
        "weekly_required": round(weekly_required, 2),
    }
    if df is not None and not df.empty:
        spend_df = df[df["type"] == "debit"]
        total_spent = spend_df["amount"].sum()
        avg_monthly_spend = total_spent / max(1, spend_df["date"].dt.to_period("M").nunique())
        category_spend = (
            spend_df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        top_category = category_spend.index[0] if not category_spend.empty else None
        feasibility = "easy"
        if monthly_required > avg_monthly_spend * 0.8:
            feasibility = "hard"
        elif monthly_required > avg_monthly_spend * 0.5:
            feasibility = "moderate"
        result.update({
            "avg_monthly_spend": round(avg_monthly_spend, 2),
            "top_spending_category": top_category,
            "feasibility": feasibility,
            "suggestion": f"Reduce spending in {top_category} to reach your goal"
            if top_category else "Monitor your expenses"
        })
    return result