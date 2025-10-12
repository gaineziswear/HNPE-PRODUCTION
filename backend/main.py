from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(title="HNPE Signals API")

app.include_router(api_router, prefix='/api')

@app.get('/')
async def root():
    return {"status": "ok", "service": "hnpe-signals"}
