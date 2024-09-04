from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from crafty.db.database import Base
from crafty.db.models.user import User


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)

    buyer = relationship("User", back_populates="favorites")
    product = relationship("Product")
