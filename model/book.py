from enum import Enum
from typing import Optional

from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator
from starlette import status

from db.base import books_collection
from model.base import PyObjectId


class BookBase(BaseModel):
    title:str
    author:str
    genre:str



    # @model_validator(mode="before")
    # def check_duplicate_entry(cls,values):
    #     book = books_collection.find_one({"title": values['title']})
    #     if book:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised")



class BookModel(BookBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    borrowed_on:Optional[float]=0
    availability_status: bool


    def list_books(self):

        return {
            "id":str(self.id),
            "title":self.title,
            "author":self.author,
            "genre":self.genre,
            "availability_status":self.availability_status
        }

class BookActionEnum(str,Enum):
    borrow="borrow"
    return_book="return"



