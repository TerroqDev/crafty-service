import logging
from importlib.metadata import metadata

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy_utils import create_database, database_exists

from crafty.routers import favorite, product, review, subscription, tag, user
from crafty.config import get_settings
from crafty.db.database import Base, engine
from crafty.middleware import LoggingMiddleware


# Clear settings cache to ensure fresh configuration loading
get_settings.cache_clear()

# Initialize the FastAPI app
app = FastAPI(
    title=metadata(__package__)["Name"],
    description=metadata(__package__)["Summary"],
    version=metadata(__package__)["Version"],
    contact={"name": "Mare i Vare", "email": "development@crafty.hr"},
)

app.add_middleware(LoggingMiddleware)
app.include_router(favorite.router)
app.include_router(product.router)
app.include_router(review.router)
app.include_router(subscription.router)
app.include_router(tag.router)
app.include_router(user.router)

# Configure the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.get("/")
def redirect_to_docs():
    """Redirect root URL to FastAPI documentation."""
    return RedirectResponse(url="/docs")


def main():
    """Start the FastAPI application.

    This function initializes the Uvicorn server to run the FastAPI application.
    It is used in conjunction with Poetry, which has an entry point set in the
    pyproject.toml file. This way, the application can be started as a script
    from the command line with the command 'crafty'.

    Uvicorn will run the app, listening on all available IP addresses (0.0.0.0)
    and port 4000. The server will also restart on code changes (reload=True).
    """

    logger.info(f"Starting application {app.title}.")

    alembic_cfg = Config("alembic.ini")

    logger.info(get_settings().database_url)

    if not database_exists(get_settings().database_url):
        create_database(get_settings().database_url)
        logger.info("Database created, applying migrations.")
        command.upgrade(alembic_cfg, "head")
    else:
        logger.info("Applying any pending migrations.")
        command.upgrade(alembic_cfg, "head")

    uvicorn.run(
        "crafty.main:app",
        host="0.0.0.0",
        port=4000,
        loop="asyncio",
    )


if __name__ == "__main__":
    main()
