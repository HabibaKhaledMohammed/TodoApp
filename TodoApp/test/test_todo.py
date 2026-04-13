import pytest
from fastapi import HTTPException
from fastapi import status

from ..entities.todo import Todo
from ..routers.todo import get_todo_by_id


def test_read_all_returns_only_current_user_todos(
    authenticated_client,
    seeded_todos,
):
    response = authenticated_client.get("/todos/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 2,
            "title": "User task",
            "description": "visible to owner",
            "priority": 2,
            "complete": False,
            "owner_id": 2,
        }
    ]


def test_create_todo_uses_fixture_user_as_owner(authenticated_client, db_session):
    payload = {
        "title": "Fixture created task",
        "description": "created in test",
        "priority": 3,
        "complete": False,
    }

    response = authenticated_client.post("/todos", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == payload

    todos = db_session.query(Todo).all()
    assert len(todos) == 1
    assert todos[0].title == "Fixture created task"
    assert todos[0].owner_id == 2
def test_get(authenticated_client):
    response = authenticated_client.get("/todos")
    assert response.status_code == 200


def test_get_todo_by_id_raises_not_found(db_session, current_user):
    with pytest.raises(HTTPException) as exc_info:
        get_todo_by_id(db=db_session, user=current_user, todo_id=999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Todo not found"
