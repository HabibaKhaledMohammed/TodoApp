from pydantic import BaseModel


class UserCreateDto(BaseModel):
    email: str
    username: str | None = None
    fullname: str | None = None
    password: str
    phone_number: str | None = None
    is_active: bool | None = None
    role: str | None = None


class UserUpdateDto(BaseModel):
    email: str | None = None
    username: str | None = None
    fullname: str | None = None
    password: str | None = None
    phone_number: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponseDto(BaseModel):
    id: int
    email: str
    username: str | None = None
    fullname: str | None = None
    phone_number: str | None = None
    is_active: bool
    role: str | None = None

    model_config = {"from_attributes": True}

