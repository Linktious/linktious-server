from typing import Union
from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session

from .base import Base
from . import querysets


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="team")

    ObjectsQueryset = querysets.TeamQueryset

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id} name: {self.name}>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team = relationship("Team", back_populates="users")

    main_board_id = Column(Integer, ForeignKey("boards.id", use_alter=True), nullable=True)
    main_board = relationship("Board", foreign_keys=[main_board_id])

    created_boards = relationship("Board", back_populates="created_by", foreign_keys='Board.created_by_user_id')
    created_links = relationship("Link", back_populates="created_by")
    created_labels = relationship("Label", back_populates="created_by")
    favorite_boards = relationship("Board", secondary="users_favorite_boards_association", back_populates="favorite_by")

    ObjectsQueryset = querysets.UserQueryset

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id} email: {self.email}>"


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    icon_url = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_links")

    labels = relationship("Label", secondary="links_labels_association", back_populates="links")

    ObjectsQueryset = querysets.LinkQueryset

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, created by: {self.created_by.email}>"


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_labels")

    links = relationship("Link", secondary="links_labels_association", back_populates="labels")
    boards_using_as_filter = relationship("Board", secondary="boards_labels_filters_association", back_populates="labels_filters")

    ObjectsQueryset = querysets.LabelQueryset

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, name: {self.name}, created by: {self.created_by.email}>"


class LinkLabelAssociation(Base):
    """Many to many relationship between links and labels to select labels for links and use
        those labels to filter links.
    """
    __tablename__ = "links_labels_association"

    link_id = Column(Integer, ForeignKey("links.id"), primary_key=True)
    lable_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_boards", foreign_keys=[created_by_user_id])

    favorite_by = relationship("User", secondary="users_favorite_boards_association", back_populates="favorite_boards")
    labels_filters = relationship("Label", secondary="boards_labels_filters_association", back_populates="boards_using_as_filter")

    ObjectsQueryset = querysets.BoardQueryset

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, name: {self.name}, created by: {self.created_by.email}>"


class UserFavoriteBoardsAssociation(Base):
    """Many to many relationship between users and boards to select favorite boards
        for users.
    """
    __tablename__ = "users_favorite_boards_association"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    board_id = Column(Integer, ForeignKey("boards.id"), primary_key=True)


class BoardLabelsFilterAssociation(Base):
    """Many to many relationship between boards and labels that will be used
        to filter links for board by the labels associated to board.
    """
    __tablename__ = "boards_labels_filters_association"

    board_id = Column(Integer, ForeignKey("boards.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)


class ModelsManager:
    """Models Manager for models.
    
    Models manager lets you use the same db session to query different model using their querysets.
    To use model queryset use the table name.

    Usage Example:
        models_manager = ModelsManager(db=db)
        teams = models_manager.teams.all()
        user = models_manager.users.create(model_schema=schema.UserCreate(username="user", hashed_password=12345678))
    """

    # Add models with queryset in here for better type hints
    teams: Team.ObjectsQueryset
    users: User.ObjectsQueryset
    links: Link.ObjectsQueryset
    labels: Label.ObjectsQueryset
    boards: Board.ObjectsQueryset
    
    def __init__(self, db: Session):
        self.db = db

    def __getattribute__(self, name):
        """Get attribute
        
        Checks first if requested attribute is model queryset and if so initialize
        instance of the relevant model queryset with the db session.
        """
        model = Base.get_model_by_table_name(name)
        if model is None:
            # Default behaviour
            return super().__getattribute__(name)
        
        return model.get_objects_queryset(db=self.db)
