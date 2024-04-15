from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from nomic.database.url import get_url

load_dotenv()

SQLALCHEMY_DATABASE_URL = get_url()

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DB_URL not found in environment variables")

# For PostgreSQL, the connect_args parameter is not required
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
