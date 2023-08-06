from typing import List
from fastapi import Body, HTTPException, status, APIRouter, Response
from bson import json_util
from fastapi.responses import JSONResponse
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import connect_db
from app.book_serializers import book_entity, book_list_entity
from bson.objectid import ObjectId

router = APIRouter()

Book = connect_db()

#Get all Records
@router.get('/', status_code=status.HTTP_200_OK, response_description="List all books")
async def get_books():
    books = await Book.find().to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Database is empty")
    return book_list_entity(books)

# Get a Single Record by isbn
@router.get('/bookByIsbn/{isbn}', status_code=status.HTTP_200_OK, response_description="List a book by isbn",
            response_model=schemas.BookSchema)
async def get_book(isbn: str):

    book = await Book.find_one({'ISBN': isbn})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this ISBN: {isbn} found")
    return book_entity(book)

# Get Record by its title
@router.get('/title/{title}', status_code=status.HTTP_200_OK, response_description="List a book by its title",
            response_model=schemas.BookSchema)
async def get_book_title(title: str):
    book = await Book.find_one({'title': title})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this title: {title} found")
    return book_entity(book)


# Get Record by author
@router.get('/author/{author}', status_code=status.HTTP_200_OK, response_description="List books for an author",
            response_model=List[schemas.BookSchema])
async def get_book_author(author: str):
    books = await Book.find({'author': author}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this author: {author} found")
    
    return book_list_entity(books)

# Get Record for a year
@router.get('/year/{year}', status_code=status.HTTP_200_OK, response_description="List books for a year",
            response_model=List[schemas.BookSchema])
async def get_book_year(year: int):
    year = str(year)
    books = await Book.find({"published_date": {"$regex": year, "$options": "i"}}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this year: {year} found")
    
    return book_list_entity(books)


# Get Record by a publisher
@router.get('/publisher/{publisher}', status_code=status.HTTP_200_OK, response_description="List books for a publisher",
            response_model=List[schemas.BookSchema])
async def get_book_publisher(publisher: str):
    books = await Book.find({'publisher': publisher}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this publisher: {publisher} found")
    return book_list_entity(books)

#Get all famous books
@router.get("/famous/", status_code=status.HTTP_200_OK, response_description="List books famous books(rating =5)",
            response_model=List[schemas.BookSchema])
async def get_books_famous():
    books = await Book.find({"rating": {"$gte": 5}}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No book found")
    return book_list_entity(books)


# Create a Record
@router.post('/', response_description="Add new book",
             response_model=schemas.BookSchema)
async def create_book(payload: schemas.BookSchema):
    try:
        result = await Book.insert_one(payload.model_dump(exclude_none=True))
        new_book = await Book.find_one({'_id': result.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=book_entity(new_book))
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Book with title: {payload.title} already exists")

#Update a Record
@router.put('/{isbn}', status_code=status.HTTP_200_OK, response_description="Update one book",
            response_model=schemas.BookSchema)
async def update_book(isbn: str, payload: schemas.BookSchema):       
    updated_book = await Book.find_one_and_update(
        {'ISBN': isbn}, {'$set': payload.model_dump(exclude_none=True)},
        return_document=ReturnDocument.AFTER)
    
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this ISBN: {isbn} found')
    return book_entity(updated_book)


@router.delete('/{isbn}', status_code=status.HTTP_200_OK, response_description="Delete one book")
async def delete_book(isbn: str):    
    book = await Book.find_one_and_delete({'ISBN': isbn})
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this isbn: {isbn} found')
    return {"message": "book deleted succeful!"}

