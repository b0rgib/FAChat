from typing import List, Optional
from fastapi import WebSocket, Depends
from fastapi_users.db.base import BaseUserDatabase
import jwt
from config import SECRET
from database import get_user_db


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


async def cookie_authentication(
    credentials: Optional[str], user_db: BaseUserDatabase,
):
    if credentials is None:
        return None

    try:
        data = jwt.decode(
            credentials,
            SECRET,
            audience="fastapi-users:auth",
            algorithms=["HS256"],
        )
        user_id = int(data.get("sub"))
        if user_id is None:
            return None
    except jwt.PyJWTError:
        return None

    try:
        return await user_db.get(user_id)
    except ValueError:
        return None


async def websocket_auth(websocket: WebSocket, user_db=Depends(get_user_db)):
    try:
        cookie = websocket._cookies['fastapiusersauth']
        user = await cookie_authentication(cookie, user_db)
        # User is authenticated, you can also check if he is active
        if user and user.is_active:
            return user

        return None
    except KeyError:
        return None
