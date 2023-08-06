from app import book
from fastapi import FastAPI

app = FastAPI()

app.include_router(book.router, tags=['Books'], prefix='/api/books')

@app.get("/api/healthchecker")
async def root():
    return {"message": "Welcome to book management's RESTFUL API bult with FastAPI and Mongodb atlas!"}

