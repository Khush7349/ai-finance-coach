from fastapi import APIRouter, HTTPException
from backend.services.loader import load_transactions
from backend.services.anomaly import detect_anomalies
from backend.llm import call
import pandas as pd
router = APIRouter(prefix="/insights")
@router.get("/")
def insights():
    try:
        df = load_transactions()
        total_spent = df[df["type"] == "debit"]["amount"].sum()
        category_spend = (
            df[df["type"] == "debit"]
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )
        monthly_spend = (
            df[df["type"] == "debit"]
            .groupby(df["date"].dt.to_period("M"))["amount"]
            .sum()
            .to_dict()
        )
        anomalies = detect_anomalies(df)
        context = f"""
Total Spend: {total_spent}
Category Breakdown:
{category_spend}
Monthly Spend:
{monthly_spend}
Anomalies:
{anomalies}
"""
        prompt = f"""
You are a financial analyst.
Analyze the user's financial data below:
{context}
Provide:
1. Key insights (patterns)
2. Problem areas
3. Actionable recommendations
4. Month-wise observations
"""
        analysis = call(prompt)
        return {
            "summary": {
                "total_spent": total_spent,
                "top_categories": list(category_spend.keys())[:3]
            },
            "anomalies": anomalies,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))