from typing import List, Optional

from pydantic import BaseModel, Field, conint


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """

    name: str = Field(..., description="The name of the product.")
    description: Optional[str] = Field(
        None, description="The description of the product."
    )
    price: conint(ge=0) = Field(
        ..., description="The price of the product. Must be a positive integer."
    )
    seller_id: int = Field(
        ..., description="The ID of the seller associated with the product."
    )


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    """

    name: Optional[str] = Field(None, description="The name of the product.")
    description: Optional[str] = Field(
        None, description="The description of the product."
    )
    price: Optional[conint(ge=0)] = Field(None, description="The price of the product.")
    seller_id: Optional[int] = Field(
        None, description="The ID of the seller associated with the product."
    )


class ProductImageCreate(BaseModel):
    """
    Schema for creating a new product image.
    """

    image_url: str = Field(..., description="The URL of the product image.")
    product_id: int = Field(
        ..., description="The ID of the product associated with the image."
    )


class Product(BaseModel):
    """
    Schema representing a product from the database.
    """

    id: int
    name: str
    description: Optional[str]
    price: int
    seller_id: int
    images: List[ProductImageCreate] = []

    class Config:
        from_attributes = True  # Ensure Pydantic can work with SQLAlchemy models.


class ProductImage(BaseModel):
    """
    Schema representing a product image from the database.
    """

    id: int
    image_url: str
    product_id: int

    class Config:
        from_attributes = True  # Ensure Pydantic can work with SQLAlchemy models.
