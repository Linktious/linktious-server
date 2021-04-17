import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer

from .querysets import ModelQueryset


SQLALCHEMY_DATABASE_URL = os.getenv("LINKTIOUS_DATABASE_URL", "sqlite:///./linktious.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    id = Column(Integer, primary_key=True, index=True)

    ObjectsQueryset: ModelQueryset = NotImplemented

    @classmethod
    def get_objects_queryset(cls, db: Session) -> ModelQueryset:
        return cls.ObjectsQueryset(db=db, model=cls)