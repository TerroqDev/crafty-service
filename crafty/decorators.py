from functools import wraps

from fastapi import HTTPException


def handle_http_exceptions(exception_mapping: dict):
    """
    Decorator to handle HTTP exceptions based on a mapping.

    This decorator wraps a FastAPI route handler and intercepts exceptions that occur during the execution
    of the handler function. It raises an appropriate HTTPException based on the exception type, using a
    provided mapping of exception types to HTTP status codes. If the exception type is not found in the
    mapping, a generic 500 Internal Server Error is raised.

    Args:
        exception_mapping (dict): A dictionary mapping exception types to HTTP status codes.
            Example:
            {
                ValueError: 400,
                NotFoundError: 404,
                DatabaseError: 500,
                # Add more mappings as needed
            }

    Returns:
        function: The wrapped function that raises HTTP exceptions based on the exception mapping.

    Raises:
        HTTPException: If an exception occurs, it raises HTTPException with the appropriate status code
        from the mapping or a default 500 status code.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if type(e) in exception_mapping:
                    raise HTTPException(
                        status_code=exception_mapping[type(e)], detail=str(e)
                    )
                raise HTTPException(status_code=500, detail="Internal server error")

        return wrapper

    return decorator
