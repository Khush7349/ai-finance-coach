from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.routes import transactions, chat, insights, goals
from backend.services.loader import load_transactions
from backend.services.rag import build_index
app = FastAPI(
    title="AI Finance Coach",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def startup_event():
    df = load_transactions()
    build_index(df)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")
app.include_router(goals.router, prefix="/api/v1")
@app.get("/")
def root():
    return {"status": "running"}
@app.get("/health")
def health():
    return {"status": "ok"}