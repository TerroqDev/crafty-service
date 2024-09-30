from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from crafty.db.database import Base
from crafty.db.models.join_tables import products_tags


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), index=True)

    seller = relationship("Seller", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    images = relationship("ProductImage", back_populates="product")

    tags = relationship("Tag", secondary=products_tags, back_populates="products")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)

    product = relationship("Product", back_populates="images")
