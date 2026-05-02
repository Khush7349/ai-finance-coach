from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.loader import load_transactions
from backend.services.rag import build_index, query_rag
from backend.llm import call
router = APIRouter(prefix="/chat")
class ChatRequest(BaseModel):
    question: str
df = load_transactions()
build_index(df)
@router.post("/")
def chat(req: ChatRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        retrieved = query_rag(q)
        context = "\n".join(retrieved) if retrieved else "No relevant data found."
        prompt = f"""
You are a personal finance assistant.
Use the user's financial data below to answer the question.
Data:
{context}
Question:
{q}
Instructions:
- Be specific
- Mention patterns (months, categories)
- Give actionable advice
"""
        answer = call(prompt)
        return {
            "question": q,
            "context_used": retrieved[:3],  # preview
            "response": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))