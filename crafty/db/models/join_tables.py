from sqlalchemy import Column, ForeignKey, Integer, Table

from crafty.db.database import Base

products_tags = Table(
    "products_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
