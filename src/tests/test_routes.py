from src.emailManager import app
from fastapi import FastAPI

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)