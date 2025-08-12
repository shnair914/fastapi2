# from fastapi.testclient import TestClient
# from app.main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import settings
# from app.database import get_db, engine
# from app import models
# import pytest

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# @pytest.fixture()
# def session():
#     models.Base.metadata.drop_all(bind=engine)
#     models.Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture()
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)