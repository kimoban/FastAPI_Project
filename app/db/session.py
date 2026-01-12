import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

database_url = settings.database_url
if (os.getenv("PYTEST_CURRENT_TEST") is not None) or ("pytest" in sys.modules):
	# Use an isolated test database file and reset it each run
	database_url = "sqlite:///./test.db"
	try:
		os.remove("test.db")
	except FileNotFoundError:
		pass

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
