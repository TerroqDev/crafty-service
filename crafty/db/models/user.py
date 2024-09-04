from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from crafty.constants import UserType
from crafty.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    reviews_given = relationship(
        "Review", foreign_keys="Review.reviewer_id", back_populates="reviewer"
    )
    reviews_received = relationship(
        "Review", foreign_keys="Review.reviewed_user_id", back_populates="reviewed_user"
    )
    favorites = relationship("Favorite", back_populates="buyer")

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": user_type}


class Seller(User):
    __tablename__ = "sellers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    subscription_level = Column(Enum("basic", "premium", "pro"), nullable=False)

    products = relationship("Product", back_populates="seller")

    __mapper_args__ = {"polymorphic_identity": "seller"}


class Buyer(User):
    __tablename__ = "buyers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "buyer"}
