from typing import Generic, TypeVar, Union, List, TYPE_CHECKING
import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Session, relationship, Query

if TYPE_CHECKING:
    from .base import Base
    from . import models, schema

T_Model = TypeVar("T_Model", bound='Base')
T_SchemaCreate = TypeVar("T_SchemaCreate", bound='schema.BaseModel')
UserOrNone = Union['models.User', None]
LinkOrNone = Union['models.Link', None]
BoardOrNone = Union['models.Board', None]


class ModelQueryset(Generic[T_Model, T_SchemaCreate]):
    """Model queryset to extend sqlalchemy queryset functionality."""
    def __init__(self, db: Session, model: T_Model):
        self.db = db
        self.model = model
        self.queryset = self.db.query(self.model)

    def __getattr__(self, name: str) -> Query:
        queryset = super().__getattribute__('queryset')
        return getattr(queryset, name)

    def filter_by_ids(self, ids) -> List[T_Model]:
        return self.filter(self.model.id.in_(ids))

    def create(self, model_schema: T_SchemaCreate) -> T_Model:
        print(self.model, type(self.model))
        db_model = self.model(**model_schema.dict())
        return self.save(model=db_model)

    def save(self, model: T_Model) -> T_Model:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model


class TeamQueryset(ModelQueryset['models.Team', 'schema.TeamCreate']):
    """Team model queryset allow to extend ModelQueryset with
        methods that only relevant to Team model.
    """
    pass


class UserQueryset(ModelQueryset['models.User', 'schema.UserCreate']):
    """User model queryset allow to extend ModelQueryset with
        methods that only relevant to User model.
    """
    
    # This method is temporary untill we add real authentication method
    def authentication(self, email: str, password: str) -> UserOrNone:
        return self.filter_by(email=email, hashed_password=password).one_or_none()

    def set_main_board(self, id: int, board_id) -> UserOrNone:
        user = self.get(id)
        if user is None:
            return None

        user.main_board_id = board_id
        return self.save(model=user)
    
    def set_favorite_boards(self, id: int, boards: List['models.Board']) -> UserOrNone:
        user = self.get(id)
        if user is None:
            return None
        
        user.favorite_boards.clear()
        user.favorite_boards.extend(boards)
        return self.save(model=user)


class LabelQueryset(ModelQueryset['models.Label', 'schema.LabelCreate']):
    """Label model queryset allow to extend ModelQueryset with
        methods that only relevant to Label model.
    """
    pass


class LinkQueryset(ModelQueryset['models.Link', 'schema.LinkCreate']):
    """Link model queryset allow to extend ModelQueryset with
        methods that only relevant to Link model.
    """
    
    def set_labels(self, id: int, labels: List['models.Label']) -> LinkOrNone:
        link = self.get(id)
        if link is None:
            return None

        link.labels.clear()
        link.labels.extend(labels)
        return self.save(model=link)


class BoardQueryset(ModelQueryset['models.Board', 'schema.BoardCreate']):
    """Board model queryset allow to extend ModelQueryset with
        methods that only relevant to Board model.
    """
    
    def set_labels_filters(self, id: int, labels: List['models.Label']) -> BoardOrNone:
        board = self.get(id)
        if board is None:
            return None

        board.labels_filters.clear()
        board.labels_filters.extend(labels)
        return self.save(model=board)


class ModelsManager:
    """Models Manager for models.
    
    Models manager lets you use the same db session to query different model using their querysets.

    Usage Example"
        models_manager = ModelsManager(db=db)
        teams = models_manager.teams.all()
        user = models_manager.users.create(model_schema=schema.UserCreate(username="user", hashed_password=12345678))
    """

    teams: TeamQueryset
    users: UserQueryset
    links: LinkQueryset
    labels: LabelQueryset
    boards: BoardQueryset
    
    def __init__(self, db: Session):
        self.db = db

    def __getattribute__(self, name):
        """Get attribute
        
        Checks first if requested attribute is model queryset and if so initialize
        instance of the relevant model queryset with the db session.
        """
        from . import models
        property_to_model = {
            "teams": models.Team,
            "users": models.User,
            "links": models.Link,
            "labels": models.Label,
            "boards": models.Board,
        }
        model = property_to_model.get(name)
        if model is None:
            # Default behaviour
            return super().__getattribute__(name)
        
        return model.get_objects_queryset(db=self.db)
