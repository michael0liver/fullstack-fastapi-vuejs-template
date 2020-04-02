from datetime import datetime
from typing import Optional

from pydantic import EmailStr, validator
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.enums.userenums import UserStatus

from .meta.pydanticbase import PydanticBase
from .meta.pydanticmixins import PydanticTS
from .meta.sqlalchemybase import SQLAlchemyBase
from .meta.sqlalchemymixins import SQLAlchemyIntPK, SQLAlchemyTS


# SQLAlchemy models
class User(SQLAlchemyTS, SQLAlchemyIntPK, SQLAlchemyBase):
    __tablename__ = "user"
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    status = Column(String, default=UserStatus.inactive)

    # Relationships
    roles = relationship("Role", secondary="user_roles")


# Pydantic models
class UserBase(PydanticBase):
    """Base schema defines common field metadata and validators."""

    @validator("first_name", "last_name", "email", check_fields=False)
    def lower(cls, v: str):
        return v.lower()

    class Config:
        orm_mode = True
        validate_assignment = True


class UserRegister(UserBase):
    """Properties to receive via API on creation via register endpoint."""

    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserCreate(UserRegister):
    """Properties to receive via API on user creation."""

    status: Optional[UserStatus] = UserStatus.inactive


class UserUpdate(UserBase):
    """Properties to receive via API on update."""

    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    status: Optional[UserStatus]


class UserUpdateMe(UserBase):
    """Properties to receive via API on update of current user."""

    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]


class UserRead(PydanticTS, UserBase):
    """Properties to return via API."""

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    status: UserStatus
