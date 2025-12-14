from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# Detect test mode
TESTING = os.getenv("TESTING") == "1"

# Read DB credentials (production)
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "calculator")
DB_PASS = os.getenv("DB_PASSWORD", "calculator")
DB_NAME = os.getenv("DB_NAME", "calculator")

# Switch database between SQLite (tests) and PostgreSQL (prod)
if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
else:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Special arguments for SQLite only
connect_args = {"check_same_thread": False} if TESTING else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    operator = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)
