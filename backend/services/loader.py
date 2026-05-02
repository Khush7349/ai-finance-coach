import pandas as pd
from pathlib import Path
REQUIRED_COLUMNS = {"date", "amount", "category", "merchant", "type"}
def load_transactions(path="backend/data/sample.csv"):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Error reading CSV: {str(e)}")
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    df = df.dropna(subset=["date", "amount"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    df["category"] = df["category"].astype(str).str.lower().str.strip()
    df["merchant"] = df["merchant"].astype(str).str.strip()
    df["type"] = df["type"].astype(str).str.lower().str.strip()
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    return df