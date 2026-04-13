from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

import TodoApp.main as main
from ..context.database import Base, get_db
from ..entities.todo import Todo
from ..entities.user import User
from ..services.auth_service import create_access_token, get_current_user, password_context


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    db_file = tmp_path / "test_todos.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main.app) as test_client:
        yield test_client
    main.app.dependency_overrides.clear()


@pytest.fixture()
def seeded_users(db_session: Session) -> dict[str, User]:
    admin_user = User(
        email="admin@example.com",
        username="admin",
        fullname="Admin User",
        hashed_password=password_context.hash("admin-pass"),
        role="admin",
        is_active=True,
    )
    regular_user = User(
        email="user@example.com",
        username="user",
        fullname="Regular User",
        hashed_password=password_context.hash("user-pass"),
        role="user",
        is_active=True,
    )
    db_session.add_all([admin_user, regular_user])
    db_session.commit()
    db_session.refresh(admin_user)
    db_session.refresh(regular_user)
    return {"admin": admin_user, "user": regular_user}


@pytest.fixture()
def current_user(seeded_users: dict[str, User]) -> dict[str, int | str]:
    user = seeded_users["user"]
    return {"sub": str(user.username), "id": int(user.id), "role": str(user.role)}


@pytest.fixture()
def authenticated_client(
    client: TestClient,
    current_user: dict[str, int | str],
) -> Generator[TestClient, None, None]:
    main.app.dependency_overrides[get_current_user] = lambda: current_user
    try:
        yield client
    finally:
        main.app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture()
def auth_headers(seeded_users: dict[str, User]) -> dict[str, dict[str, str]]:
    admin_token = create_access_token(seeded_users["admin"])
    user_token = create_access_token(seeded_users["user"])
    return {
        "admin": {"Authorization": f"Bearer {admin_token}"},
        "user": {"Authorization": f"Bearer {user_token}"},
    }


@pytest.fixture()
def seeded_todos(db_session: Session, seeded_users: dict[str, User]) -> list[Todo]:
    todos = [
        Todo(
            title="Admin task",
            description="visible to admin",
            priority=1,
            complete=False,
            owner_id=seeded_users["admin"].id,
        ),
        Todo(
            title="User task",
            description="visible to owner",
            priority=2,
            complete=False,
            owner_id=seeded_users["user"].id,
        ),
    ]
    db_session.add_all(todos)
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

