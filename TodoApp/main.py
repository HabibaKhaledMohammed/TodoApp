from fastapi import FastAPI

from context.database import init_db
from routers import auth, todo, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)

init_db()
