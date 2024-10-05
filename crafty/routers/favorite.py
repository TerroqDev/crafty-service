from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.favorite import create_favorite, get_favorite, get_favorites
from crafty.db.session import get_db
from crafty.schemas.favorite import Favorite, FavoriteCreate

router = APIRouter(tags=["favorites"], prefix="/favorites")


@router.post("/", response_model=Favorite)
def create_new_favorite(
    favorite: FavoriteCreate, db: Session = Depends(get_db)
) -> Favorite:
    """
    Create a new favorite.

    Args:
        favorite (FavoriteCreate): The favorite data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Favorite: The created favorite object.
    """
    return create_favorite(db=db, favorite=favorite)


@router.get("/{favorite_id}", response_model=Favorite)
def read_favorite(favorite_id: int, db: Session = Depends(get_db)) -> Favorite:
    """
    Retrieve a favorite by ID.

    Args:
        favorite_id (int): The ID of the favorite to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Favorite: The retrieved favorite object.

    Raises:
        HTTPException: If the favorite is not found.
    """
    db_favorite = get_favorite(db, favorite_id=favorite_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite


@router.get("/", response_model=List[Favorite])
def read_favorites(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Favorite]:
    """
    Retrieve a list of favorites with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Favorite]: List of favorite objects.
    """
    return get_favorites(db, skip=skip, limit=limit)
