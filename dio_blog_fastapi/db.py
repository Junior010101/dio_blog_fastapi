from os import getenv

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = getenv("DATABASE_URL", "sqlite+pysqlite:///./blog.sqlite")
metadata = MetaData()

class Base(DeclarativeBase):
    metadata = metadata

if getenv("RENDER"):
    engine = create_engine(
        DATABASE_URL,
        echo=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
    )

database = Database(DATABASE_URL)
