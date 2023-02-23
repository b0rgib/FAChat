from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str = Field(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description='Password must contain minimum eight characters, at least one letter and one number')


class UserUpdate(schemas.BaseUserUpdate):
    pass
