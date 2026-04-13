from fastapi import FastAPI, Request, staticfiles

from .context.database import init_db
from .routers import auth, todo, user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="TodoApp/templates")
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html",{"request": request})

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)

init_db()
