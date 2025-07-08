from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from db.base import books_collection
from model import BookBase, APIResponse, UserRole, BookModel, BookActionEnum
from model.base import PyObjectId
from security import get_current_user, check_user_role

router = APIRouter(prefix="/book",
                   tags=["Users"],
                   responses={
                       404: {"description": "Not Found"}
                   })


@router.post("/")
async def create_book(request: BookBase, user: object = Depends(get_current_user)):
    if not check_user_role(user.get("role"), [UserRole.librarian]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised")
    book_re=jsonable_encoder(request)
    book_re["availability_status"]=True
    books_collection.insert_one(book_re)
    response = APIResponse(status=True, message="Book created successfully")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response))


@router.get("/")
async def get_book(title: Optional[str] = None,
                   author: Optional[str] = None,
                   skip: int = 0,
                   limit: int = 20,
                   user: object = Depends(get_current_user)):
    find_query = {}
    if title:
        find_query['title'] = title
    if author:
        find_query['author'] = author
    books = books_collection.find(find_query).skip(skip).limit(limit)
    books = [BookModel(**x).list_books() for x in books]
    return books

@router.put("/{book_id}")
async def create_book(book_id:PyObjectId,request: BookBase, user: object = Depends(get_current_user)):
    if not check_user_role(user.get("role"), [UserRole.librarian]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised")
    book=books_collection.find_one({"_id":book_id})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    books_collection.update_one({"_id":book_id},{"$set":jsonable_encoder(request)})
    response = APIResponse(status=True, message="Book updated successfully")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response))

@router.get("/{book_id}")
async def get_book(book_id:PyObjectId,user: object = Depends(get_current_user)):
    book = books_collection.find_one({"_id": book_id})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book=BookModel(**book).list_books()
    return book


@router.patch("/{book_id}/{action}")
async def get_book(book_id:PyObjectId,action:BookActionEnum,user: object = Depends(get_current_user)):
    book = books_collection.find_one({"_id": book_id})
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if action==BookActionEnum.return_book:
        if book.get("availability_status"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
        availability_status=True
        borrowed_on=0
    else:
        if not book.get("availability_status"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
        availability_status=False
        borrowed_on=datetime.now().timestamp()
    books_collection.update_one({"_id": book_id}, {"$set":{"availability_status":availability_status,
                                                           "borrowed_on":borrowed_on} })
    response = APIResponse(status=True, message=f"Book {action} successfully")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))









