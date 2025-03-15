import re
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from crafty.constants import UserType


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The username of the user. Must be unique.
        email (EmailStr): The email of the user. Must be unique.
        password_hash (str): The hashed password of the user.
        user_type (UserType): The type of the user (either 'buyer' or 'seller').

    Config:
        use_enum_values (bool): Ensures that enum values are used when parsing and serializing.
    """

    username: str = Field(
        ...,
        description="The username of the user. Must be unique, at least 3 characters long, and only contain alphanumeric characters and allowed symbols (., _, -).",
    )
    email: EmailStr = Field(..., description="The email of the user.")
    password_hash: str = Field(..., description="The hashed password of the user.")
    user_type: UserType = Field(
        ..., description="The type of the user (either 'buyer' or 'seller')."
    )

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Username must be between 3 and 50 characters long.")
        if not re.match(r"^[a-zA-Z0-9._-]+$", value):
            raise ValueError(
                "Username must only contain alphanumeric characters and symbols: . _ -"
            )
        return value

    class Config:
        use_enum_values = True
        str_min_length = 1
        str_strip_whitespace = True


class UserBase(BaseModel):
    """
    Base schema for representing a user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (EmailStr): The email of the user.
        user_type (UserType): The type of the user (either 'buyer' or 'seller').

    Config:
        use_enum_values (bool): Ensures that enum values are used when parsing and serializing.
    """

    id: int
    username: str
    email: EmailStr
    user_type: UserType

    class Config:
        use_enum_values = True


class SellerCreate(UserCreate):
    """
    Schema for creating a new seller.

    Inherits from:
        UserCreate: The base schema for creating a user, with all its attributes.

    Additional attributes can be added specific to sellers if needed.
    """

    pass


class BuyerCreate(UserCreate):
    """
    Schema for creating a new buyer.

    Inherits from:
        UserCreate: The base schema for creating a user, with all its attributes.

    Additional attributes can be added specific to buyers if needed.
    """

    pass


class UserResponse(UserBase):
    """
    Schema for the response model of a user.

    Inherits from:
        UserBase: The base schema for representing a user, with all its attributes.

    This schema is used for returning user data in API responses.
    """

    pass
