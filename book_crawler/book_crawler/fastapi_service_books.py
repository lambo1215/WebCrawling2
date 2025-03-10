from http import HTTPStatus
from os import getenv
from typing import Any, Mapping
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import pymongo
from pymongo.asynchronous.collection import AsyncCollection


class Book(BaseModel):
    title: str
    author: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price_amount: int | None = Field(default=None)
    price_currency: str | None = Field(default=None)
    rating_value: float | None = Field(default=None)
    rating_count: int | None = Field(default=None)
    publication_year: int
    isbn: str
    pages_cnt: int | None = Field(default=None)
    publisher: str | None = Field(default=None)
    book_cover: str | None = Field(default=None)
    source_url: str


app = FastAPI(title="Book ISBN Search Service", description="Study Case Example")


async def get_mongo_db() -> AsyncCollection[Mapping[str, Any] | Any]:
    mongo_user = getenv("MONGO_USER")
    mongo_password = getenv("MONGO_PASSWORD")
    mongo_port = getenv("MONGO_PORT", 27017)
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@localhost:{mongo_port}/"
    mongo_db = getenv("MONGO_DATABASE", "items")
    mongo_db_collection = getenv("MONGO_DATABASE_COLLECTION", "scraped_books")
    client = pymongo.AsyncMongoClient(mongo_uri)
    return client[mongo_db][mongo_db_collection]


@app.get("/search_by_isbn", tags=["ISBN Searcher"])
async def get_book_by_isbn(
    mongo_db: Annotated[AsyncCollection[Mapping[str, Any] | Any], Depends(get_mongo_db)],
    isbn: str,
) -> Book:
    result = await mongo_db.find_one({"isbn": isbn})
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Can't find book with this ISBN",
        )
    return Book(**result)
