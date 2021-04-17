from typing import Union, List
from contextlib import contextmanager
from sqlalchemy.orm import Session
from db import base, managers


@contextmanager
def db_session() -> Session:
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()

ModelManagers = Union[
    managers.TeamObjectsManager,
    managers.UserObjectsManager,
    managers.LabelObjectsManager,
    managers.LinkObjectsManager,
    managers.BoardObjectsManager,
]


def get_objects_managers(*managers: ModelManagers) -> Union[ModelManagers, List[ModelManagers]]:
    """Get models objects managers as dpendencies.
    
    Args:
        *managers(ModelManagers): class reference for model manager

    Returns:
        list. instances of model objects managers initialized with same db connection 
              if requested more than one manager.
        ModelManagers. instance of model object manager initialized with db connection
                       if requested one manager.

    Usage example:
        team_manager, user_manager = fastapi.Depends(get_objects_managers(managers.TeamObjectsManager, managers.UserObjectsManager))
    """
    def inner():
        with db_session() as db:
            managers_instances = tuple(manager(db) for manager in managers)
            yield managers_instances[0] if len(managers_instances) == 1 else managers_instances
    return inner
