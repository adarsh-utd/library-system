from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from db import users_collection
from model import UserBase, APIResponse, LoginResponse
from security import HashPassword, authenticate_user, create_access_token
from utils.time_utils import get_timestamp

router = APIRouter(prefix="/user",
                   tags=["Users"],
                   responses={
                       404: {"description": "Not Found"}
                   })


ACCESS_TOKEN_EXPIRE_MINUTES = 45


@router.post("/signup")
async def signup(request: UserBase):
    """
    This endpoint register user into the application
    :param request: A Pydantic model that validate the attributes based on annotation
    :return:
    """
    user=users_collection.find_one({"email":request.email})
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exist")
    hash_password_in=HashPassword(request.password)
    add_data={
        "name":request.name,
        "email":request.email,
        "role":request.role,
        "password":hash_password_in.hash_password()
    }
    users_collection.insert_one(add_data)
    response=APIResponse(status=True,message="User Registered successfully")
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=jsonable_encoder(response))

@router.post("/login")
async def login( form_data: OAuth2PasswordRequestForm = Depends()):
    user=authenticate_user(form_data.username,form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.get("email")},
                                       expires_delta=access_token_expires)
    expiry_time = get_timestamp() + ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000
    response=LoginResponse(access_token=access_token,expiry_time=expiry_time,email=form_data.username)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))




