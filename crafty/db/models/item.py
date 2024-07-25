from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from crafty.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', description='{self.description}', price={self.price}, owner_id={self.owner_id})>"
