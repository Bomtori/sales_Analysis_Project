from fastapi import FastAPI
from app.api import analytics

app = FastAPI(title="Dashboard API")

# 라우터 등록
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Dashboard API is running!"}
