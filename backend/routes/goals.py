from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.services.goals import calculate_goal
from backend.services.loader import load_transactions
from backend.llm import call
router = APIRouter(prefix="/goals")
class GoalRequest(BaseModel):
    target: float = Field(..., gt=0)
    months: int = Field(..., gt=0, le=60)
@router.post("/")
def goal(req: GoalRequest):
    try:
        target = req.target
        months = req.months
        plan = calculate_goal(target, months)
        df = load_transactions()
        total_spent = df["amount"].sum()
        prompt = f"""
You are a financial advisor.
User wants to save {target} in {months} months.
Their spending data total:
{total_spent}
Plan:
Monthly saving: {plan['monthly_required']}
Weekly saving: {plan['weekly_required']}
Give:
- feasibility
- suggestions to cut costs
- realistic advice
"""
        advice = call(prompt)
        return {
            "goal": {
                "target": target,
                "months": months
            },
            "plan": plan,
            "advice": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))