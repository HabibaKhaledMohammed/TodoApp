from fastapi import APIRouter, Path, HTTPException
from sqlalchemy.orm import Session

from ..dtos.todo_dto import TodoDto
from ..entities.todo import Todo
from ..dependencies import db_dependency, user_dependency

router = APIRouter(prefix="/todos", tags=["todos"])


def list_todos_for_user(db: Session, user: dict) -> list[Todo]:
    """Same rules as GET /todos/: admins see all; others see only their todos."""
    if user.get("role") == "admin":
        return db.query(Todo).all()
    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


def get_todo_for_user(db: Session, user: dict, todo_id: int) -> Todo | None:
    """Load one todo: admins by id; others only if they own it."""
    if user.get("role") == "admin":
        return db.query(Todo).filter(Todo.id == todo_id).first()
    return (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.owner_id == user.get("id"))
        .first()
    )


@router.get("/")
async def read_all(db: db_dependency, user: user_dependency):
    return list_todos_for_user(db, user)


@router.get("/{todo_id}", response_model=TodoDto)
def get_todo_by_id(
        db: db_dependency,
        user: user_dependency,
        todo_id: int = Path(gt=0)
):
    todo = get_todo_for_user(db, user, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@router.post("/", response_model=TodoDto, status_code=201)
def create_todo(todo: TodoDto, db: db_dependency, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed")
    new_todo = Todo(
        title=todo.title,
        description=str(todo.description),
        priority=todo.priority,
        complete=todo.complete,
        owner_id= int(user.get("id"))
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/{todo_id}", response_model=TodoDto)
def replace_todo(
    todo: TodoDto,
    db: db_dependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.get("id")).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.priority = todo.priority
    existing_todo.complete = todo.complete
    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@router.patch("/{todo_id}", response_model=TodoDto)
def update_todo(
    todo: TodoDto,
    db: db_dependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.get("id")).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    updates = todo.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(existing_todo, field_name, value)

    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@router.delete("/{todo_id}")
def delete_todo(
    db: db_dependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.get("id")).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(existing_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}


