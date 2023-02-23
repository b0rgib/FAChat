from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

front_router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


@front_router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@front_router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@front_router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@front_router.get("/chat/{group_id}", response_class=HTMLResponse)
def group(request: Request, group_id: int):
    return templates.TemplateResponse("group.html", {"request": request, "id": group_id})
