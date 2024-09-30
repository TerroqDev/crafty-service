from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from crafty.db.database import Base
from crafty.db.models.join_tables import products_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    products = relationship("Product", secondary=products_tags, back_populates="tags")
