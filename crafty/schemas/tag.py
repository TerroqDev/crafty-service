from pydantic import BaseModel


class TagCreate(BaseModel):
    """
    Schema for creating a new tag.
    """

    name: str


class Tag(BaseModel):
    """
    Schema representing a tag from the database.
    """

    id: int
    name: str

    class Config:
        from_attributes = True
