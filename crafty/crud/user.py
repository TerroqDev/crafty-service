import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crafty.constants import SubscriptionLevel, UserType
from crafty.db.models.user import Buyer, Seller, User
from crafty.exceptions import (InvalidUserTypeError, UserAlreadyExistsError,
                               UserNotFoundError)
from crafty.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user object.
    """
    try:
        if db.query(User).filter(User.username == user.username).first():
            raise UserAlreadyExistsError(user.username, "username")
        if db.query(User).filter(User.email == user.email).first():
            raise UserAlreadyExistsError(user.email, "email")

        if user.user_type == UserType.buyer:
            db_user = Buyer(**user.model_dump())
        elif user.user_type == UserType.seller:
            db_user = Seller(**user.model_dump())
            db_user.subscription_level = SubscriptionLevel.basic
        else:
            raise InvalidUserTypeError(user.user_type)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise


def get_user(db: Session, identifier: str, identifier_type: str) -> User:
    """
    Retrieve a user based on a dynamic identifier (ID, username, or email).

    Args:
        db (Session): The database session.
        identifier (str): The value of the identifier (ID, username, or email).
        identifier_type (str): The type of the identifier ('id', 'username', 'email').

    Returns:
        User: The retrieved user object.

    Raises:
        UserNotFoundError: If no user with the given identifier exists.
    """
    if identifier_type == "id":
        user = db.query(User).filter(User.id == int(identifier)).one_or_none()
    elif identifier_type == "username":
        user = db.query(User).filter(User.username == identifier).one_or_none()
    elif identifier_type == "email":
        user = db.query(User).filter(User.email == identifier).one_or_none()
    else:
        raise ValueError("Invalid identifier type")

    if not user:
        raise UserNotFoundError(identifier, identifier_type)

    return user


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """
    Retrieve a list of users with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[User]: List of user objects.
    """
    return db.query(User).offset(skip).limit(limit).all()
