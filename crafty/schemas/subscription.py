from datetime import date

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    """
    Schema for creating a new subscription.
    """

    seller_id: int
    subscription_level: str
    start_date: date
    end_date: date


class Subscription(BaseModel):
    """
    Schema representing a subscription from the database.
    """

    id: int
    seller_id: int
    subscription_level: str
    start_date: date
    end_date: date

    class Config:
        from_attributes = True
