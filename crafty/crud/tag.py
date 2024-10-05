from sqlalchemy.orm import Session

from crafty.db.models.tag import Tag
from crafty.schemas.tag import TagCreate


def create_tag(db: Session, tag: TagCreate) -> Tag:
    """
    Create a new tag in the database.

    Args:
        db (Session): The database session.
        tag (TagCreate): The tag data to create.

    Returns:
        Tag: The created tag object.
    """
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int) -> Tag:
    """
    Retrieve a tag by ID.

    Args:
        db (Session): The database session.
        tag_id (int): The ID of the tag to retrieve.

    Returns:
        Tag: The retrieved tag object or None if not found.
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 10) -> list[Tag]:
    """
    Retrieve a list of tags with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Tag]: List of tag objects.
    """
    return db.query(Tag).offset(skip).limit(limit).all()
