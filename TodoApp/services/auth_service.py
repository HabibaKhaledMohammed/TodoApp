from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..entities.user import User

password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = "ab0f37f2add75c15dbfae3a27ef7935b4d838cd07fd351e3ad806c4fdd19e168"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if user is None or user.hashed_password is None:
        return None
    if not verify_password(password, str(user.hashed_password)):
        return None
    return user


def create_access_token(user: User) -> str:
    payload = {"sub": user.username, "id": user.id, "role": user.role}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def decode_access_token_from_cookie_or_none(token: str | None) -> dict | None:
    """Return JWT payload if valid; None if missing, invalid, or expired."""
    if not token:
        return None
    try:
        return decode_token(token)
    except JWTError:
        return None


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    return decode_token(token)
