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
