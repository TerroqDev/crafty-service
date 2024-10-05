from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.tag import (create_tag, delete_tag, get_tag, get_tag_by_name,
                             get_tags)
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import TagAlreadyExistsError, TagNotFoundError
from crafty.schemas.tag import Tag, TagCreate

router = APIRouter(tags=["tags"], prefix="/tags")

exception_mapping = {
    TagNotFoundError: 404,
    TagAlreadyExistsError: 400,
}


@router.post("/", response_model=Tag)
@handle_http_exceptions(exception_mapping)
async def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)) -> Tag:
    """
    Create a new tag.

    Args:
        tag (TagCreate): The tag data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Tag: The created tag object.

    Raises:
        HTTPException: If a tag with the same name already exists or other internal errors occur.
    """
    return create_tag(db=db, tag=tag)


@router.get("/{tag_id}", response_model=Tag)
@handle_http_exceptions(exception_mapping)
async def read_tag(tag_id: int, db: Session = Depends(get_db)) -> Tag:
    """
    Retrieve a tag by ID.

    Args:
        tag_id (int): The ID of the tag to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Tag: The retrieved tag object.

    Raises:
        TagNotFoundError: If no tag with the specified ID exists.
        HTTPException: If other internal errors occur.
    """
    return get_tag(db, tag_id=tag_id)


@router.get("/name/{tag_name}", response_model=Tag)
@handle_http_exceptions(exception_mapping)
async def read_tag_by_name(tag_name: str, db: Session = Depends(get_db)) -> Tag:
    """
    Retrieve a tag by name.

    Args:
        tag_name (str): The name of the tag to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Tag: The retrieved tag object.

    Raises:
        TagNotFoundError: If no tag with the specified name exists.
        HTTPException: If other internal errors occur.
    """
    return get_tag_by_name(db, tag_name=tag_name)


@router.delete("/{tag_id}", response_model=dict)
@handle_http_exceptions(exception_mapping)
async def delete_existing_tag(tag_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a tag by ID.

    Args:
        tag_id (int): The ID of the tag to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A confirmation message indicating the tag has been deleted.

    Raises:
        TagNotFoundError: If no tag with the specified ID exists.
        HTTPException: If other internal errors occur.
    """
    delete_tag(db, tag_id=tag_id)
    return {"detail": "Tag deleted successfully."}


@router.get("/", response_model=List[Tag])
@handle_http_exceptions(exception_mapping)
async def read_tags(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Tag]:
    """
    Retrieve a list of tags with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Tag]: A list of tag objects.

    Raises:
        HTTPException: If other internal errors occur.
    """
    return get_tags(db, skip=skip, limit=limit)
