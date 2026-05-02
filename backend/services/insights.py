from backend.llm import call
def generate_insights(context):
    prompt = f"""
You are an expert financial analyst.
Analyze the user's financial data below.
DATA:
{context}
Return STRICTLY in this JSON format:
{{
  "summary": "...",
  "problems": ["...", "..."],
  "patterns": ["...", "..."],
  "recommendations": ["...", "..."]
}}
Instructions:
- Identify spending trends across months
- Highlight overspending categories
- Detect unusual spikes
- Give actionable advice (specific, not generic)
- Keep answers concise and practical
"""
    response = call(prompt)
    return response