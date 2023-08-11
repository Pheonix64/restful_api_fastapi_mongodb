from app import book, user
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI()

app.include_router(user.routerUser, tags=['User authentication'], prefix='/api/v1/auth')
app.include_router(book.router, tags=['Books Management system API'], prefix='/api/v1/books')

@app.get("/api/v1/healthchecker")
async def root():
    return {"message": "Welcome to book management's RESTFUL API bult with FastAPI and Mongodb atlas!"}
