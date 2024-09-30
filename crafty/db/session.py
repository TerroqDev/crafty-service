from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from .database import engine

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Provides a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Db session which can be used outside of FastAPI routes.

    Usage example:
        with db_session() as db:
        db.query(.....)
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
