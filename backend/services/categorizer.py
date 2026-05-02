import re
RULES = {
    "zomato": "food",
    "swiggy": "food",
    "uber": "transport",
    "ola": "transport",
    "amazon": "shopping",
    "flipkart": "shopping",
    "netflix": "entertainment",
    "spotify": "entertainment",
    "electricity": "utilities",
    "rent": "rent",
    "salary": "income"
}
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)  
    return text.strip()
def categorize(row):
    merchant = clean_text(str(row.get("merchant", "")))
    existing = row.get("category")
    for key, value in RULES.items():
        if key in merchant:
            return value
    if existing:
        return existing.lower()
    amount = row.get("amount", 0)
    if amount > 20000:
        return "income"
    elif amount < 500:
        return "misc"
    return "other"