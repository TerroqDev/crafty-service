from typing import Optional

from pydantic import BaseModel

from crafty.constants import Rating


class ReviewCreate(BaseModel):
    """
    Schema for creating a new review.
    """

    rating: Rating
    comment: Optional[str]
    reviewer_id: int
    reviewed_user_id: Optional[int]
    product_id: Optional[int]


class Review(BaseModel):
    """
    Schema representing a review from the database.
    """

    id: int
    rating: int
    comment: Optional[str]
    reviewer_id: int
    reviewed_user_id: Optional[int]
    product_id: Optional[int]

    class Config:
        from_attributes = True
