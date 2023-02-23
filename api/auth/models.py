from fastapi_users.db import SQLAlchemyBaseUserTable
import sqlalchemy as sa
from ..chat.models import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "User"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username: str = sa.Column(sa.String, nullable=False, unique=True)
