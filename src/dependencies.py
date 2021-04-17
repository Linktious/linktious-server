from typing import Union, List
from contextlib import contextmanager
from sqlalchemy.orm import Session
from db import base
from db.managers import ModelManager


@contextmanager
def db_session() -> Session:
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_objects_managers(*models: base.Base) -> Union[ModelManager, List[ModelManager]]:
    """Get models objects managers as dependencies.
    
    Args:
        *models(base.Base): class reference for models

    Returns:
        list. instances of ModelManager initialized with same db connection 
              if requested more than one manager.
        ModelManager. instance of model object manager initialized with db connection
                       if requested one manager.

    Usage example:
        team_manager, user_manager = fastapi.Depends(get_objects_managers(models.Team, models.User))
        team_manager.objects.all()
        user_manager.objects.create(schema.UserCreate(email="email@gmail.com", hashed_password="123456"))
    """
    def inner():
        with db_session() as db:
            managers_instances = tuple(model.get_objects_manager(db) for model in models)
            yield managers_instances[0] if len(managers_instances) == 1 else managers_instances
            
    return inner
