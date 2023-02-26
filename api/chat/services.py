from fastapi import Depends, HTTPException, status
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Message, Group
from sqlalchemy import select, delete
from .schemas import GetMessage, GetGroup


class MessageService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, message, user):
        new_message = Message(user_id=user.id, **message)
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return GetMessage.from_orm(new_message).json()

    async def delete(self, message_id, user):
        query_admin = select(Group.admin).join(
            Message.group).where(Message.id == message_id)
        query_creator = select(Message.user_id).where(Message.id == message_id)
        admin = await self.session.execute(query_admin)
        creator = await self.session.execute(query_creator)
        if admin.first()[0] != user.id and creator.first()[0] != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no permission to perform this action")
        stmt = delete(Message).where(Message.id == message_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return message_id

    async def get(self, group_id):
        query = select(Message).where(Message.group_id == group_id)
        result = await self.session.execute(query)
        return [GetMessage.from_orm(message) for
                message in
                result.scalars().all()]


class GroupService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get(self):
        query = select(Group).order_by(Group.edited_at)
        result = await self.session.execute(query)
        return [GetGroup.from_orm(group) for group in result.scalars().all()]

    async def create(self, group, user):
        new_group = Group(admin=user.id, **group)
        self.session.add(new_group)
        await self.session.commit()
        await self.session.refresh(new_group)
        return GetGroup.from_orm(new_group).dict()

    async def delete(self, group_id, user):
        query = select(Group).where(Group.id == group_id)
        result = await self.session.execute(query)
        try:
            group_admin = result.first()[0].admin
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="No such group!")
        if group_admin != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no permission to perform this action")
        stmt = delete(Group).where(Group.id == group_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return group_id

    async def get_one(self, group_id):
        query = select(Group).where(Group.id == group_id)
        result = await self.session.execute(query)
        return GetGroup.from_orm(result.first()[0])
