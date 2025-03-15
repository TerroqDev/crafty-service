import logging
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crafty.constants import SubscriptionLevel, UserType
from crafty.db.models.user import Buyer, Seller, User
from crafty.exceptions import (InvalidUserTypeError, UserAlreadyExistsError,
                               UserNotFoundError)
from crafty.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database."""
    try:
        if db.query(User).filter(User.username == user.username).first():
            raise UserAlreadyExistsError(user.username, "username")
        if db.query(User).filter(User.email == user.email).first():
            raise UserAlreadyExistsError(user.email, "email")

        db_user = (
            Buyer(**user.model_dump())
            if user.user_type == UserType.buyer
            else Seller(**user.model_dump())
        )
        if user.user_type == UserType.seller:
            db_user.subscription_level = SubscriptionLevel.basic

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
    """Retrieve a user based on a dynamic identifier (ID, username, or email)."""
    filters = {
        "id": db.query(User).filter(User.id == int(identifier)).one_or_none,
        "username": db.query(User).filter(User.username == identifier).one_or_none,
        "email": db.query(User).filter(User.email == identifier).one_or_none,
    }

    if identifier_type not in filters:
        raise ValueError("Invalid identifier type")

    user = filters[identifier_type]()

    if not user:
        raise UserNotFoundError(identifier, identifier_type)

    return user


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    """Retrieve a list of users with optional pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, identifier: str, identifier_type: str) -> User:
    """Delete a user from the database based on a dynamic identifier."""
    try:
        user = get_user(db, identifier, identifier_type)
        db.delete(user)
        db.commit()
        return user
    except UserNotFoundError:
        logger.warning(f"User not found for deletion: {identifier} ({identifier_type})")
        raise
    except IntegrityError as e:
        logger.error(f"IntegrityError while trying to delete user: {e}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting user: {e}")
        db.rollback()
        raise
