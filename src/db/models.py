import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="team")

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
    favorite_boards = relationship("Board", secondary="users_favorite_boards_association", back_populates="favorited_by")


    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id} email: {self.email}>"


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    icon_url = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_links")

    labels = relationship("Label", secondary="links_labels_association", back_populates="links")

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, created by: {self.created_by.email}>"

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_labels")

    links = relationship("Link", secondary="links_labels_association", back_populates="labels")
    boards_using_as_filter = relationship("Board", secondary="boards_labels_filters_association", back_populates="labels_filters")

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
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="created_boards", foreign_keys=[created_by_user_id])

    favorited_by = relationship("User", secondary="users_favorite_boards_association", back_populates="favorite_boards")
    labels_filters = relationship("Label", secondary="boards_labels_filters_association", back_populates="boards_using_as_filter")

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
