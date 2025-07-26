from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str
    code: str | None = None