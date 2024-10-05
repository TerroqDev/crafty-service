from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.subscription import (create_subscription, get_subscription,
                                      get_subscriptions)
from crafty.db.session import get_db
from crafty.schemas.subscription import Subscription, SubscriptionCreate

router = APIRouter(tags=["subscriptions"], prefix="/subscriptions")


@router.post("/", response_model=Subscription)
def create_new_subscription(
    subscription: SubscriptionCreate, db: Session = Depends(get_db)
) -> Subscription:
    """
    Create a new subscription.

    Args:
        subscription (SubscriptionCreate): The subscription data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Subscription: The created subscription object.
    """
    return create_subscription(db=db, subscription=subscription)


@router.get("/{subscription_id}", response_model=Subscription)
def read_subscription(
    subscription_id: int, db: Session = Depends(get_db)
) -> Subscription:
    """
    Retrieve a subscription by ID.

    Args:
        subscription_id (int): The ID of the subscription to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Subscription: The retrieved subscription object.

    Raises:
        HTTPException: If the subscription is not found.
    """
    db_subscription = get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription


@router.get("/", response_model=List[Subscription])
def read_subscriptions(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Subscription]:
    """
    Retrieve a list of subscriptions with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Subscription]: List of subscription objects.
    """
    return get_subscriptions(db, skip=skip, limit=limit)
