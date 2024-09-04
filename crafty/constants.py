import enum


class UserType(enum.Enum):
    buyer = "buyer"
    seller = "seller"


class Rating(enum.Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"


class SubscriptionLevel(enum.Enum):
    basic = "basic"
    premium = "premium"
    pro = "pro"
