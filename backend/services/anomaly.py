def detect_anomalies(df):
    anomalies = []
    df = df[df["type"] == "debit"].copy()
    df["month"] = df["date"].dt.to_period("M")
    baseline = (
        df.groupby(["month", "category"])["amount"]
        .mean()
        .reset_index()
    )
    df = df.merge(baseline, on=["month", "category"], suffixes=("", "_avg"))
    for _, row in df.iterrows():
        avg = row["amount_avg"]
        if avg == 0:
            continue
        ratio = row["amount"] / avg
        if ratio > 2:
            severity = (
                "critical" if ratio > 4 else
                "high" if ratio > 3 else
                "medium"
            )
            anomalies.append({
                "type": "spike",
                "category": row["category"],
                "amount": row["amount"],
                "average": round(avg, 2),
                "ratio": round(ratio, 2),
                "date": str(row["date"]),
                "severity": severity,
                "message": f"{severity.upper()}: {row['category']} spending spike"
            })
    return anomalies