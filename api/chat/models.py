import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "Group"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String, nullable=False)
    admin: int = sa.Column(sa.Integer, sa.ForeignKey("User.id"), nullable=False)


class Message(Base):
    __tablename__ = "Message"
    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("User.id"))
    group_id: int = sa.Column(sa.Integer, sa.ForeignKey(
        "Group.id", ondelete="CASCADE"))
    text: str = sa.Column(sa.String, nullable=False)
    created_at: datetime = sa.Column(sa.TIMESTAMP, default=datetime.utcnow)

    group = relationship("Group")
