from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.subscription import (create_subscription, get_subscription,
                                      get_subscriptions)
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import (SubscriptionAlreadyExistsError,
                               SubscriptionNotFoundError)
from crafty.schemas.subscription import Subscription, SubscriptionCreate

router = APIRouter(tags=["subscriptions"], prefix="/subscriptions")


exception_mapping = {
    SubscriptionNotFoundError: 404,
    SubscriptionAlreadyExistsError: 400,
}


@router.post("/", response_model=Subscription)
@handle_http_exceptions(exception_mapping)
async def create_new_subscription(
    subscription: SubscriptionCreate, db: Session = Depends(get_db)
) -> Subscription:
    """
    Create a new subscription.

    Args:
        subscription (SubscriptionCreate): The subscription data to create. Must conform to the SubscriptionCreate schema.
        db (Session): The database session. Automatically injected by FastAPI's dependency injection.

    Returns:
        Subscription: The created subscription object.

    Raises:
        SubscriptionAlreadyExistsError: If a subscription with the same name already exists.
    """
    return await create_subscription(db=db, subscription=subscription)


@router.get("/{subscription_id}", response_model=Subscription)
@handle_http_exceptions(exception_mapping)
async def read_subscription(
    subscription_id: int, db: Session = Depends(get_db)
) -> Subscription:
    """
    Retrieve a subscription by ID.

    Args:
        subscription_id (int): The ID of the subscription to retrieve.
        db (Session): The database session. Automatically injected by FastAPI's dependency injection.

    Returns:
        Subscription: The retrieved subscription object.

    Raises:
        SubscriptionNotFoundError: If no subscription with the given ID exists.
    """
    return await get_subscription(db, subscription_id=subscription_id)


@router.get("/", response_model=List[Subscription])
@handle_http_exceptions(exception_mapping)
async def read_subscriptions(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[Subscription]:
    """
    Retrieve a list of subscriptions with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session): The database session. Automatically injected by FastAPI's dependency injection.

    Returns:
        List[Subscription]: List of subscription objects.

    Raises:
        HTTPException: If any unexpected errors occur (handled by the decorator).
    """
    return await get_subscriptions(db, skip=skip, limit=limit)
