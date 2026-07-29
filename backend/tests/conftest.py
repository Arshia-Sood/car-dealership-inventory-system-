import sys
from pathlib import Path

import pytest
from sqlalchemy import text

from app.core.database import Base, SessionLocal, engine

# Ensure the backend root directory is on Python's import path so tests can
# import modules like `from app.main import app`.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


@pytest.fixture(autouse=True)
def prepare_database():
    """Ensure tables exist and start each test with empty database tables."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        session.execute(text("TRUNCATE TABLE users, vehicles RESTART IDENTITY CASCADE"))
        session.commit()

    yield

