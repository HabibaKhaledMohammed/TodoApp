from pydantic import BaseModel

class LoginDto(BaseModel):
    username: str
    password: str


class TokenDto(BaseModel):
    access_token: str
    token_type: str


class ChangePasswordDto(BaseModel):
    current_password: str
    new_password: str
