from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# local SQLite file
SQLALCHEMY_DATABASE_URL = "sqlite:///./water_workforce.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
