from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.tag import create_tag, get_tag, get_tags
from crafty.db.session import get_db
from crafty.schemas.tag import Tag, TagCreate

router = APIRouter(tags=["tags"], prefix="/tags")


@router.post("/", response_model=Tag)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)) -> Tag:
    """
    Create a new tag.

    Args:
        tag (TagCreate): The tag data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Tag: The created tag object.
    """
    return create_tag(db=db, tag=tag)


@router.get("/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)) -> Tag:
    """
    Retrieve a tag by ID.

    Args:
        tag_id (int): The ID of the tag to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Tag: The retrieved tag object.

    Raises:
        HTTPException: If the tag is not found.
    """
    db_tag = get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.get("/", response_model=List[Tag])
def read_tags(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Tag]:
    """
    Retrieve a list of tags with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Tag]: List of tag objects.
    """
    return get_tags(db, skip=skip, limit=limit)
