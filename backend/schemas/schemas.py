#Add the pydantic models for the schemas here

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)