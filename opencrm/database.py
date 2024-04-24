from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from opencrm.utils.utils import get_logger

LOGGER = get_logger(__name__)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1/crm"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
default_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def get_database():
    db = default_session()
    try:
        return db
    finally:
        db.close()


def do_commit(db: Session):
    try:
        db.commit()
    except Exception as e:
        LOGGER.error(f"Error committing transaction: {e}")
        db.rollback()
        raise e
