from typing import Union
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, Session

from .querysets import ModelQueryset


SQLALCHEMY_DATABASE_URL = os.getenv("LINKTIOUS_DATABASE_URL", "sqlite:///./linktious.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    ObjectsQueryset: ModelQueryset = NotImplemented

    @classmethod
    def get_objects_queryset(cls, db: Session) -> ModelQueryset:
        return cls.ObjectsQueryset(db=db, model=cls)

    @classmethod
    def get_model_by_table_name(cls, table_name: str) -> Union["Base", None]:
        return next((model for model in cls.__subclasses__()
                     if model.__tablename__ == table_name), None)
