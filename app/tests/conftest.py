import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.main import app
from app.dependencies import get_db

TEST_DATASETS_DIR = 'tests/test_datasets'

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def db():
    session = TestingSessionLocal()
    yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db) -> TestClient:
    def _get_db_override():
        return db

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)
