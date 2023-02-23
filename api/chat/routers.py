from fastapi import (APIRouter,
                     Depends,
                     WebSocket,
                     WebSocketDisconnect)
from .schemas import GetGroup, GetMessage
from api.auth.models import User
from api.auth.routers import fastapi_users
from typing import List
from .utils import ConnectionManager, websocket_auth
from .services import MessageService, GroupService

message_router = APIRouter(tags=["message"], prefix="/message")
group_router = APIRouter(tags=["group"], prefix="/group")
current_user = fastapi_users.current_user()


manager = ConnectionManager()


@message_router.get("/{group_id}", response_model=List[GetMessage])
async def get_messages(group_id: int,
                       service: MessageService = Depends()):
    return await service.get(group_id)


@message_router.websocket("/ws")
async def add_message(websocket: WebSocket,
                      service: MessageService = Depends(),
                      user=Depends(websocket_auth)):
    await manager.connect(websocket)
    try:
        while True:
            try:
                message = await service.create(websocket, user)
                await manager.broadcast(message)
            except AttributeError:
                await manager.send_personal_message("You are not authorized to create groups", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@message_router.delete("/{message_id}")
async def delete_message(message_id: int,
                         service: MessageService = Depends(),
                         user: User = Depends(current_user)):
    return await service.delete(message_id, user)


@group_router.websocket("/ws/")
async def create_group(websocket: WebSocket,
                       service: GroupService = Depends(),
                       user=Depends(websocket_auth)):
    await manager.connect(websocket)
    try:
        while True:
            try:
                group = await service.create(websocket, user)
                await manager.broadcast(group)
            except AttributeError:
                await manager.send_personal_message("You are not authorized to create groups", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@group_router.get("/", response_model=List[GetGroup])
async def get_group(service: GroupService = Depends()):
    return await service.get()


@group_router.delete("/{group_id}")
async def delete_group(group_id: int,
                       service: GroupService = Depends(),
                       user: User = Depends(current_user)):
    return await service.delete(group_id, user)
