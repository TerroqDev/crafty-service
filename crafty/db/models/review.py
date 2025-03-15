from sqlalchemy import (Column, Enum, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from crafty.constants import Rating
from crafty.db.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    rating = Column(Enum(Rating), nullable=False)
    comment = Column(String(500))
    reviewer_id = Column(Integer, ForeignKey("users.id"), index=True)
    reviewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    reviewer = relationship(
        "User", foreign_keys=[reviewer_id], back_populates="reviews_given"
    )
    reviewed_user = relationship(
        "User", foreign_keys=[reviewed_user_id], back_populates="reviews_received"
    )
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (
        UniqueConstraint(
            "reviewer_id",
            "reviewed_user_id",
            "product_id",
            name="unique_reviewer_reviewed_user_product",
        ),
    )
