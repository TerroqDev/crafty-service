from sqlalchemy.orm import Session

from crafty.db.models.favorite import Favorite
from crafty.schemas.favorite import FavoriteCreate


def create_favorite(db: Session, favorite: FavoriteCreate) -> Favorite:
    """
    Create a new favorite in the database.

    Args:
        db (Session): The database session.
        favorite (FavoriteCreate): The favorite data to create.

    Returns:
        Favorite: The created favorite object.
    """
    db_favorite = Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def get_favorite(db: Session, favorite_id: int) -> Favorite:
    """
    Retrieve a favorite by ID.

    Args:
        db (Session): The database session.
        favorite_id (int): The ID of the favorite to retrieve.

    Returns:
        Favorite: The retrieved favorite object or None if not found.
    """
    return db.query(Favorite).filter(Favorite.id == favorite_id).first()


def get_favorites(db: Session, skip: int = 0, limit: int = 10) -> list[Favorite]:
    """
    Retrieve a list of favorites with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Favorite]: List of favorite objects.
    """
    return db.query(Favorite).offset(skip).limit(limit).all()
