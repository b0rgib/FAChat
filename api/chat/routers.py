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


group_manager = ConnectionManager()
message_manager = ConnectionManager()


@message_router.get("/{group_id}", response_model=List[GetMessage])
async def get_messages(group_id: int,
                       service: MessageService = Depends()):
    return await service.get(group_id)


@message_router.websocket("/")
async def add_message(websocket: WebSocket,
                      service: MessageService = Depends(),
                      user: User = Depends(websocket_auth)):
    await message_manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                if not data.get("id"):
                    message = await service.create(data, user)
                else:
                    message = await service.delete(data["id"], user)
                await message_manager.broadcast(message)
            except AttributeError:
                await message_manager.send_personal_message(
                    "You are not authorized to create or delete messages",
                    websocket)
    except WebSocketDisconnect:
        message_manager.disconnect(websocket)


@group_router.websocket("/")
async def create_delete_group(websocket: WebSocket,
                              service: GroupService = Depends(),
                              user: User = Depends(websocket_auth)):
    await group_manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                if not data.get("id"):
                    group = await service.create(data, user)
                else:
                    group = await service.delete(data["id"], user)
                await group_manager.broadcast(group)
            except AttributeError:
                await group_manager.send_personal_message(
                    "You are not authorized to create or delete groups",
                    websocket)
    except WebSocketDisconnect:
        group_manager.disconnect(websocket)


@group_router.get("/", response_model=List[GetGroup])
async def get_groups(service: GroupService = Depends()):
    return await service.get()


@group_router.get("/{group_id}", response_model=GetGroup)
async def get_group(group_id: int,
                    service: GroupService = Depends()):
    return await service.get_one(group_id)
