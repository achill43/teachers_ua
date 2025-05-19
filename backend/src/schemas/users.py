from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole

    class Config:
        from_attributes = True


class SessionReponce(BaseModel):
    access_token: str
    refresh_token: str
