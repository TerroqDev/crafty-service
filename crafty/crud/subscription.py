from sqlalchemy.orm import Session

from crafty.db.models.subscription import Subscription
from crafty.schemas.subscription import SubscriptionCreate


def create_subscription(db: Session, subscription: SubscriptionCreate) -> Subscription:
    """
    Create a new subscription in the database.

    Args:
        db (Session): The database session.
        subscription (SubscriptionCreate): The subscription data to create.

    Returns:
        Subscription: The created subscription object.
    """
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def get_subscription(db: Session, subscription_id: int) -> Subscription:
    """
    Retrieve a subscription by ID.

    Args:
        db (Session): The database session.
        subscription_id (int): The ID of the subscription to retrieve.

    Returns:
        Subscription: The retrieved subscription object or None if not found.
    """
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()


def get_subscriptions(
    db: Session, skip: int = 0, limit: int = 10
) -> list[Subscription]:
    """
    Retrieve a list of subscriptions with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[Subscription]: List of subscription objects.
    """
    return db.query(Subscription).offset(skip).limit(limit).all()
