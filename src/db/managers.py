from typing import Generic, TypeVar, Union, List
import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Session, relationship

from .base import Base
from . import models, schema


T_Model = TypeVar("T_Model", bound=Base)
T_SchemaCreate = TypeVar("T_SchemaCreate", bound=schema.BaseModel)
UserOrNone = Union[models.User, None]
LinkOrNone = Union[models.Link, None]
BoardOrNone = Union[models.Board, None]


class ModelQueryset(Generic[T_Model, T_SchemaCreate]):

    def __init__(self, db: Session, model: T_Model):
        self.db = db
        self.model = model
        self.queryset = self.db.query(self.model)

    def __getattr__(self, name: str):
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


class TeamQueryset(ModelQueryset[models.Team, schema.TeamCreate]):
    """Team Model Manager allow to extend ModelManager with
        methods that only relevant to Team model.
    """
    pass


class TeamObjectsManager(models.Team):
    __tablename__ = "teams"
    __table_args__ = {'extend_existing': True} 

    def __init__(self, db: Session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = TeamQueryset(db=db, model=models.Team)


class UserQueryset(ModelQueryset[models.User, schema.UserCreate]):
    """User Model Manager allow to extend ModelManager with
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
    
    def set_favorite_boards(self, id: int, boards: List[models.Board]) -> UserOrNone:
        user = self.get(id)
        if user is None:
            return None
        
        user.favorite_boards.clear()
        user.favorite_boards.extend(boards)
        return self.save(model=user)

class UserObjectsManager(models.User):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = UserQueryset(db=db, model=models.User)


class LabelQueryset(ModelQueryset[models.Label, schema.LabelCreate]):
    """Label Model Manager allow to extend ModelManager with
        methods that only relevant to Label model.
    """
    pass


class LabelObjectsManager(models.Label):
    __tablename__ = "labels"
    __table_args__ = {'extend_existing': True} 

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = LabelQueryset(db=db, model=models.Label)


class LinkQueryset(ModelQueryset[models.Link, schema.LinkCreate]):
    """Link Model Manager allow to extend ModelManager with
        methods that only relevant to Link model.
    """
    
    def set_labels(self, id: int, labels: List[models.Label]) -> LinkOrNone:
        link = self.get(id)
        if link is None:
            return None

        link.labels.clear()
        link.labels.extend(labels)
        return self.save(model=link)


class LinkObjectsManager(models.Link):
    __tablename__ = "links"
    __table_args__ = {'extend_existing': True} 

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = LinkQueryset(db=db, model=models.Link)


class BoardQueryset(ModelQueryset[models.Board, schema.BoardCreate]):
    """Board Model Manager allow to extend ModelManager with
        methods that only relevant to Board model.
    """
    
    def set_labels_filters(self, id: int, labels: List[models.Label]) -> BoardOrNone:
        board = self.get(id)
        if board is None:
            return None

        board.labels_filters.clear()
        board.labels_filters.extend(labels)
        return self.save(model=board)


class BoardObjectsManager(models.Board):
    __tablename__ = "boards"
    __table_args__ = {'extend_existing': True} 

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = BoardQueryset(db=db, model=models.Board)