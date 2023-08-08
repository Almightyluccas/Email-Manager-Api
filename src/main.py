from fastapi import FastAPI
from .api_v1.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

origins = [
    "http://localhost:63343/ReactLaravelFirstProject/"
    "test.html?_ijt=g4pg8slgc9jjuj1ukf3i81fid8&_ij_reload=RELOAD_ON_SAVE",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
