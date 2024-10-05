from sqlalchemy.orm import Session

from crafty.db.models.review import Review
from crafty.schemas.review import ReviewCreate


def create_review(db: Session, review: ReviewCreate) -> Review:
    """
    Create a new review in the database.

    Args:
        db (Session): The database session.
        review (ReviewCreate): The review data to create.

    Returns:
        Review: The created review object.
    """
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int) -> Review:
    """
    Retrieve a review by ID.

    Args:
        db (Session): The database session.
        review_id (int): The ID of the review to retrieve.

    Returns:
        Review: The retrieved review object or None if not found.
    """
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews(db: Session, skip: int = 0, limit: int = 10) -> list[Review]:
    """
    Retrieve a list of reviews with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Review]: List of review objects.
    """
    return db.query(Review).offset(skip).limit(limit).all()
