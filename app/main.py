from fastapi import FastAPI
from app.routes.url import router as url_router

app = FastAPI(title="URL Shortener API", description="A simple URL shortening service", version="1.0.0")

app.include_router(url_router, prefix="/api", tags=["URL Shortener"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API!"}