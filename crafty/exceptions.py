class UserAlreadyExistsError(Exception):
    """Exception raised when trying to create a user that already exists."""

    def __init__(self, identifier: str, identifier_type: str):
        self.message = f"User with {identifier_type} '{identifier}' already exists"
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, identifier: str, identifier_type: str):
        self.message = f"User with {identifier_type} '{identifier}' does not exist"
        super().__init__(self.message)


class InvalidUserTypeError(Exception):
    """Exception raised when trying to create a user that already exists."""

    def __init__(self, user_type: int):
        self.message = f"Invaid user type {user_type}"
        super().__init__(self.message)


class ProductNotFoundError(Exception):
    """Exception raised when a product is not found."""

    def __init__(self, product_id: int):
        self.message = f"Product with ID {product_id} does not exist"
        super().__init__(self.message)


class ProductAlreadyExistsError(Exception):
    """Exception raised when a product already exists."""

    def __init__(self, name: str):
        self.message = f"Product with name '{name}' already exists"
        super().__init__(self.message)


class NoProductsFoundError(Exception):
    """Raised when no products are found for a given seller."""

    def __init__(self, seller_id: int):
        self.seller_id = seller_id
        self.message = f"No products found for seller with ID {seller_id}"
        super().__init__(self.message)


class ProductImageNotFoundError(Exception):
    """Exception raised when a product image is not found."""

    def __init__(self, image_id: int):
        self.message = f"Product image with ID {image_id} does not exist"
        super().__init__(self.message)


class TagNotFoundError(Exception):
    """Custom exception raised when a tag is not found."""

    def __init__(self, tag_id: int):
        self.message = f"Tag with ID {tag_id} not found."
        super().__init__(self.message)


class TagAlreadyExistsError(Exception):
    """Custom exception raised when trying to create a tag that already exists."""

    def __init__(self, tag_name: str):
        self.message = f"A tag with the name '{tag_name}' already exists."
        super().__init__(self.message)


class ReviewNotFoundError(Exception):
    """Exception raised when a review is not found."""

    def __init__(self, review_id: int):
        super().__init__(f"Review with ID {review_id} not found.")


class ReviewAlreadyExistsError(Exception):
    """Exception raised when a review already exists."""

    def __init__(self, review_id: int):
        super().__init__(f"Review with ID {review_id} already exists.")


class FavoriteNotFoundError(Exception):
    """Exception raised when a favorite is not found."""

    def __init__(self, favorite_id: int):
        super().__init__(f"Favorite with ID {favorite_id} not found.")


class FavoriteAlreadyExistsError(Exception):
    """Exception raised when a favorite already exists."""

    def __init__(self, user_id: int, product_id: int):
        super().__init__(
            f"Favorite already exists for user {user_id} on product {product_id}."
        )


class SubscriptionNotFoundError(Exception):
    """Raised when a subscription is not found in the database."""

    def __init__(self, subscription_id: int):
        self.subscription_id = subscription_id
        super().__init__(f"Subscription with ID {subscription_id} not found.")


class SubscriptionAlreadyExistsError(Exception):
    """Raised when trying to create a subscription that already exists."""

    def __init__(self):
        super().__init__("A subscription with this name already exists.")
