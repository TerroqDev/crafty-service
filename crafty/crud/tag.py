import logging
from typing import List

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from crafty.db.models.tag import Tag
from crafty.exceptions import TagAlreadyExistsError, TagNotFoundError
from crafty.schemas.tag import TagCreate

logger = logging.getLogger(__name__)


def create_tag(db: Session, tag: TagCreate) -> Tag:
    """Create a new tag in the database."""
    try:
        existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
        if existing_tag:
            raise TagAlreadyExistsError(tag.name)

        db_tag = Tag(**tag.model_dump())
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError as e:
        logger.error(f"IntegrityError while creating tag: {e}")
        db.rollback()
        raise TagAlreadyExistsError(tag.name)
    except Exception as e:
        logger.error(f"Unexpected error while creating tag: {e}")
        db.rollback()
        raise


def get_tag(db: Session, tag_id: int) -> Tag:
    """Retrieve a tag by ID."""
    try:
        return db.query(Tag).filter(Tag.id == tag_id).one()
    except NoResultFound:
        raise TagNotFoundError(tag_id)


def get_tag_by_name(db: Session, tag_name: str) -> Tag:
    """Retrieve a tag by name."""
    try:
        return db.query(Tag).filter(Tag.name == tag_name).one()
    except NoResultFound:
        raise TagNotFoundError(tag_name)


def delete_tag(db: Session, tag_id: int) -> None:
    """Delete a tag by ID."""
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).one()
        db.delete(tag)
        db.commit()
    except NoResultFound:
        raise TagNotFoundError(tag_id)
    except Exception as e:
        logger.error(f"Unexpected error while deleting tag: {e}")
        db.rollback()
        raise


def get_tags(db: Session, skip: int = 0, limit: int = 10) -> List[Tag]:
    """Retrieve a list of tags with optional pagination."""
    return db.query(Tag).offset(skip).limit(limit).all()
