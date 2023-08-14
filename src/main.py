from fastapi import FastAPI
from api_v1.routes import router

app = FastAPI(debug=True)

app.include_router(router, prefix="/api/v1")
