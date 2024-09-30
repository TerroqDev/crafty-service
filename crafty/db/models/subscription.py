from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from crafty.constants import SubscriptionLevel
from crafty.db.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("users.id"), index=True)
    subscription_level = Column(Enum(SubscriptionLevel), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    seller = relationship("Seller")
