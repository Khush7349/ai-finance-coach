from fastapi import APIRouter, Query, HTTPException
from backend.services.loader import load_transactions
router = APIRouter(prefix="/transactions")
@router.get("/")
def get_transactions(
    month: int = Query(None, ge=1, le=12),
    category: str = None,
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0)
):
    try:
        df = load_transactions()
        if month:
            df = df[df["date"].dt.month == month]
        if category:
            df = df[df["category"] == category]
        total_records = len(df)
        df = df.iloc[offset: offset + limit]
        total_spent = df[df["type"] == "debit"]["amount"].sum()
        return {
            "meta": {
                "total_records": total_records,
                "limit": limit,
                "offset": offset
            },
            "summary": {
                "total_spent": total_spent
            },
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))