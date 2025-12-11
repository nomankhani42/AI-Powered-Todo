"""Database session configuration and setup.

Provides SQLAlchemy engine, session factory, and Base class for ORM models.
Includes connection pooling optimized for Neon Serverless PostgreSQL.

Neon Connection String Format:
    postgresql://[user]:[password]@[neon_hostname]/[dbname]?sslmode=require

The ?sslmode=require parameter is required for Neon connections.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from typing import Generator
from app.models.base import Base

# Database URL from environment or default
# Neon connection string should include ?sslmode=require parameter
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/todo_app?sslmode=require"
)

# Create SQLAlchemy engine optimized for Neon Serverless PostgreSQL
# Serverless databases handle pooling on their side, so we use smaller pools
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,              # Reduced from 10 for serverless architecture
    max_overflow=10,          # Reduced from 20 for serverless architecture
    pool_pre_ping=True,       # Essential: verify connections before using
    pool_recycle=300,         # Recycle connections after 5 minutes to prevent stale connections
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout for reliability
    },
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",  # Log SQL queries if enabled
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator:
    """Dependency injection for database session in FastAPI endpoints.

    Yields:
        Session: SQLAlchemy session object

    Example:
        @app.get("/tasks")
        def get_tasks(db: Session = Depends(get_db)):
            return db.query(Task).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables defined in models.

    This should be called once on application startup or during migration setup.
    For production, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


def check_db_connection():
    """Check if database connection is available.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
