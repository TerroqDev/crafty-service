import logging
from typing import List

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from crafty.db.models.favorite import Favorite
from crafty.db.models.user import User
from crafty.exceptions import FavoriteAlreadyExistsError, FavoriteNotFoundError
from crafty.schemas.favorite import FavoriteCreate

logger = logging.getLogger(__name__)


def create_favorite(db: Session, favorite: FavoriteCreate) -> Favorite:
    """Create a new favorite in the database.

    Args:
        db (Session): The database session.
        favorite (FavoriteCreate): The favorite data to create.

    Returns:
        Favorite: The created favorite object.

    Raises:
        FavoriteAlreadyExistsError: If a favorite already exists for the given user and product.
        IntegrityError: If there is an integrity error during the database operation.
    """
    try:
        existing_favorite = (
            db.query(Favorite)
            .filter(
                Favorite.buyer_id == favorite.buyer_id,
                Favorite.product_id == favorite.product_id,
            )
            .one_or_none()
        )

        if existing_favorite:
            raise FavoriteAlreadyExistsError(favorite.buyer_id, favorite.product_id)

        db_favorite = Favorite(**favorite.model_dump())
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return db_favorite
    except IntegrityError as e:
        logger.error(f"IntegrityError while creating favorite: {e}")
        db.rollback()
        raise FavoriteAlreadyExistsError(favorite.buyer_id, favorite.product_id)
    except Exception as e:
        logger.error(f"Unexpected error while creating favorite: {e}")
        db.rollback()
        raise


def get_favorite(db: Session, favorite_id: int) -> Favorite:
    """Retrieve a favorite by ID.

    Args:
        db (Session): The database session.
        favorite_id (int): The ID of the favorite to retrieve.

    Returns:
        Favorite: The retrieved favorite object.

    Raises:
        FavoriteNotFoundError: If the favorite with the given ID is not found.
        Exception: If any unexpected error occurs during retrieval.
    """
    try:
        favorite = db.query(Favorite).filter(Favorite.id == favorite_id).one()
        return favorite
    except NoResultFound:
        raise FavoriteNotFoundError(favorite_id)
    except Exception as e:
        logger.error(f"Unexpected error while retrieving favorite: {e}")
        raise


def delete_favorite(db: Session, favorite_id: int) -> None:
    """Delete a favorite by ID.

    Args:
        db (Session): The database session.
        favorite_id (int): The ID of the favorite to delete.

    Raises:
        FavoriteNotFoundError: If the favorite with the given ID is not found.
        Exception: If any unexpected error occurs during deletion.
    """
    try:
        favorite = db.query(Favorite).filter(Favorite.id == favorite_id).one()
        db.delete(favorite)
        db.commit()
    except NoResultFound:
        raise FavoriteNotFoundError(favorite_id)
    except Exception as e:
        logger.error(f"Unexpected error while deleting favorite: {e}")
        db.rollback()
        raise


def get_favorites(db: Session, skip: int = 0, limit: int = 10) -> List[Favorite]:
    """Retrieve a list of favorites with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[Favorite]: List of favorite objects.
    """
    return db.query(Favorite).offset(skip).limit(limit).all()


def get_favorites_by_buyer_id(db: Session, buyer_id: int) -> List[Favorite]:
    """Retrieve all favorites for a specific buyer by buyer_id.

    Args:
        db (Session): The database session.
        buyer_id (int): The ID of the buyer.

    Returns:
        List[Favorite]: List of favorite objects for the specified buyer.
    """
    try:
        return db.query(Favorite).filter(Favorite.buyer_id == buyer_id).all()
    except Exception as e:
        logger.error(
            f"Unexpected error while retrieving favorites for buyer_id {buyer_id}: {e}"
        )
        raise


def get_favorites_by_username(db: Session, username: str) -> List[Favorite]:
    """Retrieve all favorites for a specific buyer by username.

    Args:
        db (Session): The database session.
        username (str): The username of the buyer.

    Returns:
        List[Favorite]: List of favorite objects for the specified buyer.
    """
    try:
        return (
            db.query(Favorite)
            .join(Favorite.buyer)
            .filter(User.username == username)
            .all()
        )
    except Exception as e:
        logger.error(
            f"Unexpected error while retrieving favorites for username {username}: {e}"
        )
        raise
