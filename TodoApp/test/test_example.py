import pytest

from ..entities.user import User


def test_example() -> None:
    assert True

@pytest.fixture()
def regular_user() -> User:
    return User(
        email="habiba",
    )
#@pytest.mark.asyncio
def test_regular_user(regular_user: User) -> None:
    assert regular_user.email == "habiba"