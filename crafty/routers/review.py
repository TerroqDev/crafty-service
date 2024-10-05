from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.review import create_review, get_review, get_reviews
from crafty.db.session import get_db
from crafty.schemas.review import Review, ReviewCreate

router = APIRouter(tags=["reviews"], prefix="/reviews")


@router.post("/", response_model=Review)
def create_new_review(review: ReviewCreate, db: Session = Depends(get_db)) -> Review:
    """
    Create a new review.

    Args:
        review (ReviewCreate): The review data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Review: The created review object.
    """
    return create_review(db=db, review=review)


@router.get("/{review_id}", response_model=Review)
def read_review(review_id: int, db: Session = Depends(get_db)) -> Review:
    """
    Retrieve a review by ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Review: The retrieved review object.

    Raises:
        HTTPException: If the review is not found.
    """
    db_review = get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@router.get("/", response_model=List[Review])
def read_reviews(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Review]:
    """
    Retrieve a list of reviews with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Review]: List of review objects.
    """
    return get_reviews(db, skip=skip, limit=limit)
