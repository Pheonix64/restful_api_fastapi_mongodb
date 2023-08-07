from typing import List
from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import connect_db
from app.book_serializers import book_entity, book_list_entity

router = APIRouter()

Book = connect_db()

#Get all Records
@router.get('/', status_code=status.HTTP_200_OK, response_description="List all books")
async def get_books():
    """
    Get all books in the database.

    Returns:
        List[dict]: A list of dictionaries representing books in the database.

    Raises:
        HTTPException: If the database is empty, a 404 status code will be returned.

    Example:
        If the database contains books, the response will be a JSON list with book details.
        Otherwise, an HTTP 404 response will be returned with the message "Database is empty."
    """
    books = await Book.find().to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Database is empty")
    return book_list_entity(books)


# Get a Single Record by isbn
@router.get('/bookByIsbn/{isbn}', status_code=status.HTTP_200_OK, response_description="List a book by isbn",
            response_model=schemas.BookSchema)
async def get_book(isbn: str):
    """
    Get a book record from the database based on its ISBN.

    Args:
        isbn (str): The ISBN (International Standard Book Number) of the book.

    Returns:
        dict: A dictionary representing the book record in the database.

    Raises:
        HTTPException: If no book with the provided ISBN is found, a 404 status code will be returned.

    Example:
        If a book with the provided ISBN exists in the database, the response will be a JSON object with
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book
        with this ISBN: {isbn} found."
    """
    book = await Book.find_one({'ISBN': isbn})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this ISBN: {isbn} found")
    return book_entity(book)


# Get Record by its title
@router.get('/title/{title}', status_code=status.HTTP_200_OK, response_description="List a book by its title",
            response_model=schemas.BookSchema)
async def get_book_title(title: str):
    """
    Get a book record from the database based on its title.

    Args:
        title (str): The title of the book.

    Returns:
        dict: A dictionary representing the book record in the database.

    Raises:
        HTTPException: If no book with the provided title is found, a 404 status code will be returned.

    Example:
        If a book with the provided title exists in the database, the response will be a JSON object with
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book
        with this title: {title} found."
    """    
    book = await Book.find_one({'title': title})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this title: {title} found")
    return book_entity(book)


# Get Record by author
@router.get('/author/{author}', status_code=status.HTTP_200_OK, response_description="List books for an author",
            response_model=List[schemas.BookSchema])
async def get_book_author(author: str):
    """
    Get a list of book records from the database based on the author's name.

    Args:
        author (str): The name of the author.

    Returns:
        List[dict]: A list of dictionaries representing book records in the database.

    Raises:
        HTTPException: If no books by the specified author are found, a 404 status code will be returned.

    Example:
        If books by the specified author exist in the database, the response will be a JSON list containing
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book
        with this author: {author} found."
    """
    books = await Book.find({'author': author}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this author: {author} found")
    
    return book_list_entity(books)


# Get Record for a year
@router.get('/year/{year}', status_code=status.HTTP_200_OK, response_description="List books for a year",
            response_model=List[schemas.BookSchema])
async def get_book_year(year: int):   
    """
    Get a list of book records from the database based on the published year.

    Args:
        year (int): The year of publication.

    Returns:
        List[dict]: A list of dictionaries representing book records in the database.

    Raises:
        HTTPException: If no books published in the specified year are found, a 404 status code will be returned.

    Example:
        If books published in the specified year exist in the database, the response will be a JSON list containing
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book
        with this year: {year} found."
    """    
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
    """
    Get a list of book records from the database based on the publisher's name.

    Args:
        publisher (str): The name of the publisher.

    Returns:
        List[dict]: A list of dictionaries representing book records in the database.

    Raises:
        HTTPException: If no books published by the specified publisher are found, a 404 status code will be returned.

    Example:
        If books published by the specified publisher exist in the database, the response will be a JSON list containing
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book
        with this publisher: {publisher} found."
    """
    books = await Book.find({'publisher': publisher}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this publisher: {publisher} found")
    return book_list_entity(books)


#Get all famous books
@router.get("/famous/", status_code=status.HTTP_200_OK, response_description="List books famous books(rating =5)",
            response_model=List[schemas.BookSchema])
async def get_books_famous():
    """
    Get a list of famous books from the database, where famous books have a rating of 5 or higher.

    Returns:
        List[dict]: A list of dictionaries representing famous book records in the database.

    Raises:
        HTTPException: If no famous books (rating >= 5) are found, a 404 status code will be returned.

    Example:
        If famous books (rating >= 5) exist in the database, the response will be a JSON list containing
        the book details. Otherwise, an HTTP 404 response will be returned with the message "No book found."
    """
    books = await Book.find({"rating": {"$gte": 5}}).to_list(length=None)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No book found")
    return book_list_entity(books)


# Create a Record
@router.post('/', response_description="Add new book",
             response_model=schemas.BookSchema)
async def create_book(payload: schemas.BookSchema):
    """
    Create a new book record in the database.

    Args:
        payload (schemas.BookSchema): The request payload containing book information.

    Returns:
        JSONResponse: A JSON response containing the created book details.

    Raises:
        HTTPException: If a book with the same title already exists in the database, a 409 status code will be returned.

    Example:
        If the book is successfully created, the response will be a JSON object with the newly added book details.
        If a book with the same title already exists in the database, an HTTP 409 response will be returned with
        the message "Book with title: {payload.title} already exists."
    """
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
    """
    Update an existing book record in the database based on its ISBN (International Standard Book Number).

    Args:
        isbn (str): The ISBN of the book to be updated.
        payload (schemas.BookSchema): The request payload containing updated book information.

    Returns:
        dict: A dictionary representing the updated book details.

    Raises:
        HTTPException: If no book with the specified ISBN is found, a 404 status code will be returned.

    Example:
        If the book with the specified ISBN is successfully updated, the response will be a JSON object with
        the updated book details.
        If no book with the specified ISBN is found, an HTTP 404 response will be returned with the message
        "No book with this ISBN: {isbn} found."
    """    
    updated_book = await Book.find_one_and_update(
        {'ISBN': isbn}, {'$set': payload.model_dump(exclude_none=True)},
        return_document=ReturnDocument.AFTER)
    
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this ISBN: {isbn} found')
    return book_entity(updated_book)


@router.delete('/{isbn}', status_code=status.HTTP_200_OK, response_description="Delete one book")
async def delete_book(isbn: str):    
    """
    Delete an existing book record from the database based on its ISBN (International Standard Book Number).

    Args:
        isbn (str): The ISBN of the book to be deleted.

    Returns:
        string: A message indicating the successful deletion.

    Raises:
        HTTPException: If no book with the specified ISBN is found, a 404 status code will be returned.

    Example:
        If the book with the specified ISBN is successfully deleted, the response will be a JSON object with
        the message "book deleted successfully!"
        If no book with the specified ISBN is found, an HTTP 404 response will be returned with the message
        "No book with this ISBN: {isbn} found."
    """
    book = await Book.find_one_and_delete({'ISBN': isbn})
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this isbn: {isbn} found')
    return {"message": "book deleted succefully!"}

