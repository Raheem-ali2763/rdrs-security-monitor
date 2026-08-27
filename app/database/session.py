from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "rdrs.db"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    """Create and return a new database session."""
    return SessionLocal()
