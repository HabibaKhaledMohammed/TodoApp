from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user as resolve_current_user,
    oauth2_bearer,
    password_context,
    verify_password,
)
from dependencies import db_dependency, user_dependency
from dtos.auth_dto import ChangePasswordDto, LoginDto, TokenDto
from entities.user import User

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/login", response_model=TokenDto)
def login(login_request: LoginDto, db: db_dependency):
    user = authenticate_user(login_request.username, login_request.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {"access_token": create_access_token(user), "token_type": "bearer"}


@router.post("/token", response_model=TokenDto)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {"access_token": create_access_token(user), "token_type": "bearer"}


@router.get("/get_current_user")
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    return resolve_current_user(token)


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    password_request: ChangePasswordDto,
    db: db_dependency,
    current_user: user_dependency
):
    user = db.query(User).filter(User.id == current_user.get("id")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.hashed_password is None or not verify_password(
        password_request.current_password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    user.hashed_password = password_context.hash(password_request.new_password)
    db.commit()
