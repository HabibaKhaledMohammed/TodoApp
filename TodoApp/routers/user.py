from fastapi import APIRouter, HTTPException, Path
from starlette import status

from ..services.auth_service import password_context
from ..dependencies import db_dependency
from ..dtos.user_dto import  UserCreateDto, UserResponseDto, UserUpdateDto
from ..entities.user import User


router = APIRouter(prefix='/users', tags=['users'])
@router.get("/", response_model=list[UserResponseDto])
def read_all_users(db: db_dependency):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponseDto)
def read_user(db: db_dependency, user_id: int = Path(gt=0)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateDto, db: db_dependency):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        email=user.email,
        username=str(user.username),
        fullname=str(user.fullname),
        hashed_password=password_context.hash(user.password),
        role=str(user.role),
        phone_number=user.phone_number,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponseDto)
def update_user(user: UserUpdateDto, db: db_dependency, user_id: int = Path(gt=0)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email is not None:
        email_owner = db.query(User).filter(User.email == user.email, User.id != user_id).first()
        if email_owner is not None:
            raise HTTPException(status_code=409, detail="Email already exists")
        existing_user.email = user.email

    if user.username is not None:
        existing_user.username = user.username
    if user.fullname is not None:
        existing_user.fullname = user.fullname
    if user.password is not None:
        existing_user.hashed_password = password_context.hash(user.password)
    if user.role is not None:
        existing_user.role = user.role
    if user.is_active is not None:
        existing_user.is_active = user.is_active

    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.delete("/{user_id}")
def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}

