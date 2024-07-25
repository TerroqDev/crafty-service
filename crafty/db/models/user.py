from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from crafty.db.database import Base


class UserType(PyEnum):
    BUYER = "buyer"
    SELLER = "seller"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', user_type='{self.user_type}')>"
