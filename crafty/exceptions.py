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


class ProductImageNotFoundError(Exception):
    """Exception raised when a product image is not found."""

    def __init__(self, image_id: int):
        self.message = f"Product image with ID {image_id} does not exist"
        super().__init__(self.message)
