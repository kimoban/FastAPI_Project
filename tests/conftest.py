import os
import pytest

from app.db.session import engine
from app.db.base import Base


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    test_url = os.getenv("TEST_DATABASE_URL")
    if test_url:
        # Ensure a clean schema for PostgreSQL tests
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
