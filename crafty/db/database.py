from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from crafty.config import get_settings

# Create SQLAlchemy engine
engine = create_engine(
    get_settings().database_url,
    pool_size=150,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

# Base class for declarative models
Base = declarative_base()
