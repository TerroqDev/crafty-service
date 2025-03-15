from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    """
    Schema for creating a new favorite.
    """

    buyer_id: int
    product_id: int


class Favorite(BaseModel):
    """
    Schema representing a favorite from the database.
    """

    id: int
    buyer_id: int
    product_id: int

    class Config:
        from_attributes = True
