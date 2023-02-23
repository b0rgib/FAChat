from pydantic import BaseModel
from datetime import datetime


class AddGroup(BaseModel):
    name: str


class GetGroup(BaseModel):
    id: int
    name: str
    admin: int

    class Config:
        orm_mode = True


class GetMessage(BaseModel):
    id: int
    user_id: int
    group_id: int
    text: str
    created_at: datetime
    
    class Config:
        orm_mode = True


class AddMessage(BaseModel):
    group_id: int
    text: str
