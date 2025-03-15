from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.favorite import (create_favorite, delete_favorite,
                                  get_favorite, get_favorites,
                                  get_favorites_by_buyer_id,
                                  get_favorites_by_username)
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import FavoriteAlreadyExistsError, FavoriteNotFoundError
from crafty.schemas.favorite import Favorite, FavoriteCreate

router = APIRouter(tags=["favorites"], prefix="/favorites")


exception_mapping = {
    FavoriteNotFoundError: 404,
    FavoriteAlreadyExistsError: 400,
}


@router.post("/", response_model=Favorite)
@handle_http_exceptions(exception_mapping)
async def create_new_favorite(
    favorite: FavoriteCreate, db: Session = Depends(get_db)
) -> Favorite:
    """
    Create a new favorite for a user.

    Args:
        favorite (FavoriteCreate): The favorite data to create.

    Returns:
        Favorite: The created favorite object.
    """
    return create_favorite(db=db, favorite=favorite)


@router.get("/{favorite_id}", response_model=Favorite)
@handle_http_exceptions(exception_mapping)
async def read_favorite(favorite_id: int, db: Session = Depends(get_db)) -> Favorite:
    """
    Retrieve a favorite by ID.

    Args:
        favorite_id (int): The ID of the favorite to retrieve.

    Returns:
        Favorite: The retrieved favorite object.
    """
    return get_favorite(db, favorite_id=favorite_id)


@router.delete("/{favorite_id}", status_code=204)
@handle_http_exceptions(exception_mapping)
async def delete_favorite_by_id(
    favorite_id: int, db: Session = Depends(get_db)
) -> None:
    """
    Delete a favorite by ID.

    Args:
        favorite_id (int): The ID of the favorite to delete.

    Returns:
        None: No content on successful deletion.
    """
    delete_favorite(db, favorite_id=favorite_id)


@router.get("/", response_model=List[Favorite])
async def read_favorites(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Favorite]:
    """
    Retrieve a list of favorites with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        List[Favorite]: List of favorite objects.
    """
    return get_favorites(db, skip=skip, limit=limit)


@router.get("/buyer/{buyer_id}", response_model=List[Favorite])
async def read_favorites_by_buyer_id(
    buyer_id: int, db: Session = Depends(get_db)
) -> List[Favorite]:
    """Get all favorites for a specific buyer by buyer_id.

    Args:
        buyer_id (int): The ID of the buyer.
        db (Session, optional): The database session.

    Returns:
        List[Favorite]: List of favorite objects for the specified buyer.
    """
    favorites = get_favorites_by_buyer_id(db, buyer_id)
    if not favorites:
        raise HTTPException(
            status_code=404, detail="No favorites found for this buyer."
        )
    return favorites


@router.get("/buyer/username/{username}", response_model=List[Favorite])
async def read_favorites_by_username(
    username: str, db: Session = Depends(get_db)
) -> List[Favorite]:
    """Get all favorites for a specific buyer by username.

    Args:
        username (str): The username of the buyer.
        db (Session, optional): The database session.

    Returns:
        List[Favorite]: List of favorite objects for the specified buyer.
    """
    favorites = get_favorites_by_username(db, username)
    if not favorites:
        raise HTTPException(
            status_code=404, detail="No favorites found for this username."
        )
    return favorites
