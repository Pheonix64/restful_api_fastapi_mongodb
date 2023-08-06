def book_entity(book) -> dict:
    return {
        "ISBN": book.get("ISBN", ""),
        "author": book.get("author", ""),
        "currency": book.get("currency", ""),
        "description": book.get("description", ""),
        "language": book.get("language", ""),
        "page_count": book.get("page_count", 0),
        "price": book.get("price", 0.0),
        "published_date": book.get("published_date", ""),
        "publisher": book.get("publisher", ""),
        "rating": book.get("rating", 0.0),
        "title": book.get("title", ""),
        "voters": book.get("voters", [])
    }

   
def book_list_entity(books) -> list:
    return [book_entity(book) for book in books]
