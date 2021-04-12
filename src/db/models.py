import datetime as dt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    main_board_id = Column(Integer, ForeignKey("boards.id"), nullable=True)

    main_board = relationship("Board", foreign_keys=[main_board_id])
    created_boards = relationship("Board", back_populates="created_by", foreign_keys='Board.created_by_user_id')
    created_links = relationship("Link", back_populates="created_by")
    created_labels = relationship("Label", back_populates="created_by")
    favorite_boards = relationship("Board", secondary="users_favorite_boards", back_populates="favorited_by")


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
    labels = relationship("Label", secondary="links_labels", back_populates="links")

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, created by: {self.created_by.email}>"

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", back_populates="created_labels")
    links = relationship("Link", secondary="links_labels", back_populates="labels")
    boards_using_as_filter = relationship("Board", secondary="boards_labels_filters", back_populates="labels_filters")

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, name: {self.name}, created by: {self.created_by.email}>"


class LinkLable(Base):
    __tablename__ = "links_labels"

    link_id = Column(Integer, ForeignKey("links.id"), primary_key=True)
    lable_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)        
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", back_populates="created_boards", foreign_keys=[created_by_user_id])
    favorited_by = relationship("User", secondary="users_favorite_boards", back_populates="favorite_boards")
    labels_filters = relationship("Label", secondary="boards_labels_filters", back_populates="boards_using_as_filter")

    def __repr__(self):
        return f"<{self.__class__.__name__} id: {self.id}, name: {self.name}, created by: {self.created_by.email}>"


class UserFavoriteBoards(Base):
    __tablename__ = "users_favorite_boards"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    board_id = Column(Integer, ForeignKey("boards.id"), primary_key=True)


class BoardLabelsFilter(Base):
    __tablename__ = "boards_labels_filters"

    board_id = Column(Integer, ForeignKey("boards.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)
