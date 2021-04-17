from typing import Union, List
from contextlib import contextmanager
from fastapi import Depends
from sqlalchemy.orm import Session
from db import base
from db.querysets import ModelsManager


@contextmanager
def db_session() -> Session:
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_models_manager() -> ModelsManager:
    """Get models manager."""
    with db_session() as db:
        yield ModelsManager(db=db)


models_manager_dependency = Depends(get_models_manager)
