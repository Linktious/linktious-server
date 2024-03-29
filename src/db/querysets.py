from typing import Generic, TypeVar, Union, List, TYPE_CHECKING
from sqlalchemy.orm import Session, Query

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
    
    # This method is temporary until we add real authentication method
    def authentication(self, email: str, password: str) -> UserOrNone:
        return self.filter_by(email=email, hashed_password=password).one_or_none()

    def set_main_board(self, user_id: int, board_id) -> UserOrNone:
        user = self.get(user_id)
        if user is None:
            return None

        user.main_board_id = board_id
        return self.save(model=user)
    
    def set_favorite_boards(self, user_id: int, boards: List['models.Board']) -> UserOrNone:
        user = self.get(user_id)
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
    
    def set_labels(self, link_id: int, labels: List['models.Label']) -> LinkOrNone:
        link = self.get(link_id)
        if link is None:
            return None

        link.labels.clear()
        link.labels.extend(labels)
        return self.save(model=link)


class BoardQueryset(ModelQueryset['models.Board', 'schema.BoardCreate']):
    """Board model queryset allow to extend ModelQueryset with
        methods that only relevant to Board model.
    """
    
    def set_links(self, board_id: int, links: List['models.Link']) -> BoardOrNone:
        board = self.get(board_id)
        if board is None:
            return None

        board.links.clear()
        board.links.extend(links)
        return self.save(model=board)
