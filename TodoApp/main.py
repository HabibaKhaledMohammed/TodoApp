from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from .context.database import init_db
from .dependencies import db_dependency
from .routers import auth, todo, user
from .routers.todo import get_todo_for_user, list_todos_for_user
from .services.auth_service import decode_access_token_from_cookie_or_none


app = FastAPI()
app.add_middleware(ProxyHeadersMiddleware)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def template_context(request: Request, **extra: Any) -> dict[str, Any]:
    user = decode_access_token_from_cookie_or_none(request.cookies.get("access_token"))
    ctx: dict[str, Any] = {"request": request, "current_user": user}
    ctx.update(extra)
    return ctx


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=template_context(request),
    )


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=template_context(request),
    )


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=template_context(request),
    )


@app.get("/todos/todo-page")
def todos_page(request: Request, db: db_dependency):
    user = decode_access_token_from_cookie_or_none(request.cookies.get("access_token"))
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    todos = list_todos_for_user(db, user)
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context=template_context(request, todos=todos),
    )


@app.get("/todos/add")
def todo_add_page(request: Request):
    if decode_access_token_from_cookie_or_none(request.cookies.get("access_token")) is None:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="todo_add.html",
        context=template_context(request),
    )


@app.get("/todos/edit/{todo_id}")
def todo_edit_page(request: Request, todo_id: int, db: db_dependency):
    user = decode_access_token_from_cookie_or_none(request.cookies.get("access_token"))
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    todo = get_todo_for_user(db, user, todo_id)
    if todo is None:
        return RedirectResponse(url="/todos/todo-page", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="todo_edit.html",
        context=template_context(request, todo=todo),
    )


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)

init_db()
