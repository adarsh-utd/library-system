from enum import Enum

from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator, EmailStr
from starlette import status

from model.base import PyObjectId


class UserBase(BaseModel):
    name: str
    password: str
    email: EmailStr
    role: str

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "",
                "role": "user"
            }
        }

    # @model_validator(mode="before")
    # def check_password_strength(cls,values):
    #     if len(values["password"]) <=8:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Provide stronger password")




class UserModel(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class UserRole(str,Enum):
    user="user"
    librarian="librarian"
