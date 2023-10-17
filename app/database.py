from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL =   '<url>'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker( bind=engine , autoflush=False )

Base = declarative_base()


def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()
