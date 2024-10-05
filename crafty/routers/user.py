from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from crafty.crud.user import create_user, get_user, get_users
from crafty.db.session import get_db
from crafty.exceptions import (InvalidUserTypeError, UserAlreadyExistsError,
                               UserNotFoundError)
from crafty.schemas.user import UserCreate, UserResponse

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Create a new user.

    Args:
        user (UserCreate): The user data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If a user with the same username or email already exists, or if the user type is invalid.
    """
    try:
        return create_user(db=db, user=user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidUserTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Retrieve a list of users with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[UserResponse]: List of user objects.
    """
    return get_users(db, skip=skip, limit=limit)


@router.get("/email/{email}", response_model=UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get a user by their email.

    Args:
        email (str): The email of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The user object.

    Raises:
        HTTPException: If the user with the given email does not exist.
    """
    try:
        user = get_user(db, email, "email")
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail="User not found with the given email"
        )


@router.get("/username/{username}", response_model=UserResponse)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a user by their username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The user object.

    Raises:
        HTTPException: If the user with the given username does not exist.
    """
    try:
        user = get_user(db, username, "username")
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail="User not found with the given username"
        )


@router.get("/id/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The user object.

    Raises:
        HTTPException: If the user with the given ID does not exist.
    """
    try:
        user = get_user(db, user_id, "id")
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}", status_code=204)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user.

    Args:
        user_id (int): The ID of the ser to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user is not found or other internal errors occur.
    """
    try:
        delete_user(db, user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
