from fastapi import FastAPI
from app.api.ai_api_controller import ai_router

# FastAPI 인스턴스 생성
app = FastAPI()

# AI 라우터 등록
app.include_router(ai_router, prefix="/ai", tags=["AI Processing"])