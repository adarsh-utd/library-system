from pydantic import BaseModel


class APIResponse(BaseModel):
    status:bool
    message:str


class LoginResponse(BaseModel):
    access_token:str
    expiry_time:float
    email:str