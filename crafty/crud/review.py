import logging
from typing import List

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from crafty.db.models.review import Review
from crafty.exceptions import ReviewAlreadyExistsError, ReviewNotFoundError
from crafty.schemas.review import ReviewCreate

logger = logging.getLogger(__name__)


def create_review(db: Session, review: ReviewCreate) -> Review:
    """
    Create a new review in the database.

    This function checks if a review already exists for the specified reviewer,
    reviewed user, and product. If it exists, a ReviewAlreadyExistsError is raised.

    Args:
        db (Session): The database session used for the operation.
        review (ReviewCreate): The review data to be created.

    Returns:
        Review: The created review object.

    Raises:
        ReviewAlreadyExistsError: If a review already exists for the user
        on the specified product.
        Exception: If any unexpected error occurs during the operation.
    """
    try:
        existing_review = (
            db.query(Review)
            .filter(
                Review.reviewer_id == review.reviewer_id,
                Review.reviewed_user_id == review.reviewed_user_id,
                Review.product_id == review.product_id,
            )
            .one_or_none()
        )
        if existing_review:
            raise ReviewAlreadyExistsError(
                f"Review already exists for user {review.reviewer_id} on product {review.product_id}."
            )

        db_review = Review(**review.model_dump())
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    except IntegrityError as e:
        logger.error(f"IntegrityError while creating review: {e}")
        db.rollback()
        raise ReviewAlreadyExistsError(
            f"Review already exists for user {review.reviewer_id} on product {review.product_id}."
        )
    except Exception as e:
        breakpoint()
        logger.error(f"Unexpected error while creating review: {e}")
        db.rollback()
        raise


def get_review(db: Session, review_id: int) -> Review:
    """
    Retrieve a review from the database by its ID.

    Args:
        db (Session): The database session used for the operation.
        review_id (int): The ID of the review to be retrieved.

    Returns:
        Review: The retrieved review object.

    Raises:
        ReviewNotFoundError: If no review with the specified ID is found.
    """
    try:
        return db.query(Review).filter(Review.id == review_id).one()
    except NoResultFound:
        raise ReviewNotFoundError(review_id)


def get_reviews(db: Session, skip: int = 0, limit: int = 10) -> List[Review]:
    """
    Retrieve a list of reviews from the database with optional pagination.

    Args:
        db (Session): The database session used for the operation.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.

    Returns:
        List[Review]: A list of review objects.
    """
    return db.query(Review).offset(skip).limit(limit).all()


def delete_review(db: Session, review_id: int) -> None:
    """
    Delete a review from the database by its ID.

    Args:
        db (Session): The database session used for the operation.
        review_id (int): The ID of the review to be deleted.

    Raises:
        ReviewNotFoundError: If no review with the specified ID is found.
        Exception: If any unexpected error occurs during the operation.
    """
    try:
        review = db.query(Review).filter(Review.id == review_id).one()
        db.delete(review)
        db.commit()
    except NoResultFound:
        raise ReviewNotFoundError(review_id)
    except Exception as e:
        logger.error(f"Unexpected error while deleting review: {e}")
        db.rollback()
        raise
