from fastapi import FastAPI
from api.auth.routers import router as auth_router
from api.chat.routers import message_router, group_router
from frontend.routers import front_router

app = FastAPI()

app.include_router(message_router)
app.include_router(group_router)
app.include_router(auth_router)
app.include_router(front_router)
