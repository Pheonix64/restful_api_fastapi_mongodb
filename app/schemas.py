from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class BookModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')
    ISBN: str
    author: str
    currency: str
    description: str
    language: str
    page_count: int
    price: float
    published_date: str
    publisher: str
    rating: Optional[float]
    title: str
    voters:Optional[int]
    
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "ISBN": "",
                "author": "Jane Doe",
                "currency": "XOF",
                "description": "book description here",
                "language": "zarma",
                "page_count": 100,
                "price": 6.5,
                "published_date": "jul, 2021",
                "publisher": "Edition africaine",
                "rating": 4.0,
                "title": "Experiments, Science, and Fashion in Nanophotonics",
                "voters": 200
            }
        }

class BookSchema(BaseModel):
    ISBN: Optional[str]
    author: Optional[str]
    currency: Optional[str]
    description: Optional[str]
    language: Optional[str]
    page_count: Optional[int]
    price: Optional[float]
    published_date: Optional[str]
    publisher: Optional[str]
    rating: Optional[float]
    title: Optional[str]
    voters: Optional[int]
    
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "ISBN": "",
                "author": "Jane Doe",
                "currency": "XOF",
                "description": "book description here",
                "language": "zarma",
                "page_count": 100,
                "price": 6.5,
                "published_date": "jul, 2021",
                "publisher": "Edition africaine",
                "rating": 4.0,
                "title": "Experiments, Science, and Fashion in Nanophotonics",
                "voters": 200
            }
        }

class ResponseModel(BookSchema):
    book: List[BookSchema]