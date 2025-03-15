from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from crafty.crud.review import (create_review, delete_review, get_review,
                                get_reviews)
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import ReviewAlreadyExistsError, ReviewNotFoundError
from crafty.schemas.review import Review, ReviewCreate

router = APIRouter(tags=["reviews"], prefix="/reviews")

exception_mapping = {
    ReviewNotFoundError: 404,
    ReviewAlreadyExistsError: 400,
}


@router.post("/", response_model=Review)
@handle_http_exceptions(exception_mapping)
async def create_new_review(
    review: ReviewCreate, db: Session = Depends(get_db)
) -> Review:
    """
    Create a new review.

    Args:
        review (ReviewCreate): The review data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Review: The created review object.

    Raises:
        ReviewAlreadyExistsError: If a review already exists for the given reviewer, reviewed user, and product.
    """
    return create_review(db=db, review=review)


@router.get("/{review_id}", response_model=Review)
@handle_http_exceptions(exception_mapping)
async def read_review(review_id: int, db: Session = Depends(get_db)) -> Review:
    """
    Retrieve a review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Review: The retrieved review object.

    Raises:
        ReviewNotFoundError: If the review with the given ID does not exist.
    """
    return get_review(db, review_id=review_id)


@router.delete("/{review_id}", status_code=204)
@handle_http_exceptions(exception_mapping)
async def delete_review_by_id(review_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a review by its ID.

    Args:
        review_id (int): The ID of the review to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        ReviewNotFoundError: If the review with the given ID does not exist.
    """
    delete_review(db, review_id=review_id)


@router.get("/", response_model=List[Review])
async def read_reviews(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Review]:
    """
    Retrieve a list of reviews with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Review]: A list of review objects.
    """
    return get_reviews(db, skip=skip, limit=limit)
