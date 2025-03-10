from http import HTTPStatus
from os import getenv
from typing import Any, Mapping, List, Optional
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.collection import Collection


class Book(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[List[str]] = None
    price_amount: Optional[str] = None
    price_currency: Optional[str] = None
    rating_value: Optional[float] = None
    rating_count: Optional[int] = None
    publication_year: str
    isbn: str
    pages_cnt: Optional[str] = None
    publisher: Optional[str] = None
    book_cover: Optional[str] = None
    source_url: str


app = FastAPI(title="Book ISBN Search Service", description="Study Case Example for chitai-gorod.ru Web Crawler")


def get_mongo_db() -> Collection:
    # Use environment variables if set, otherwise use defaults that match the crawler setup
    mongo_user = getenv("MONGO_USER", "")
    mongo_password = getenv("MONGO_PASSWORD", "")
    mongo_port = getenv("MONGO_PORT", "27017")
    
    # Build connection URI based on whether auth is needed
    if mongo_user and mongo_password:
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@localhost:{mongo_port}/"
    else:
        mongo_uri = f"mongodb://localhost:{mongo_port}/"
    
    mongo_db = getenv("MONGO_DATABASE", "books_db")
    mongo_db_collection = getenv("MONGO_DATABASE_COLLECTION", "books")
    
    client = MongoClient(mongo_uri)
    return client[mongo_db][mongo_db_collection]


@app.get("/books/isbn/{isbn}", tags=["Books"])
def get_book_by_isbn(
    isbn: str,
    mongo_db: Annotated[Collection, Depends(get_mongo_db)],
) -> Book:
    # Add strip to clean the ISBN input and use regex for partial matching
    cleaned_isbn = isbn.strip()
    result = mongo_db.find_one({"isbn": {"$regex": cleaned_isbn}})
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Can't find book with ISBN: {cleaned_isbn}",
        )
    
    # Convert ObjectId to string for JSON serialization
    if "_id" in result:
        result["_id"] = str(result["_id"])
    
    # Clean up any whitespace in string fields
    for field in ["title", "isbn"]:
        if field in result and isinstance(result[field], str):
            result[field] = result[field].strip()
        
    return Book(**result)
