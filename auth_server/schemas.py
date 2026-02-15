from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        phone_pattern = r"^[\d\s\-\+\(\)]+$"
        if not re.match(phone_pattern, v):
            raise ValueError("Invalid phone number format")
        return v


class UserLogin(BaseModel):
    username_or_email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
