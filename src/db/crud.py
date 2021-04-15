from typing import List, Union
from sqlalchemy.orm import Session

from . import models, schema


UserOrNone = Union[models.User, None]
LabelOrNone = Union[models.Label, None]
LinkOrNone = Union[models.Link, None]
BoardOrNone = Union[models.User, None]


def get_teams(db: Session) -> List[models.Team]:
    return db.query(models.Team).all()


def create_team(db: Session, team: schema.TeamCreate) -> models.Team:
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# This method is temporary untill we add real authentication method
def user_authentication(db: Session, user_email: str, user_password: str) -> UserOrNone:
    return db.query(models.User).filter_by(email=user_email, hashed_password=user_password).one_or_none()


def get_user_by_id(db: Session, user_id: int) -> UserOrNone:
    return db.query(models.User).filter_by(id=user_id).one_or_none()


def set_user_main_board(db: Session, user_id: int, board_id: int) -> UserOrNone:
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        return None

    user.main_board_id = board_id
    db.commit()
    db.refresh(user)
    return user


def set_user_favorite_boards(db: Session, user_id: int, boards_ids: List[int]) -> UserOrNone:
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        return None

    boards = get_boards_by_ids(db=db, boards_ids=boards_ids)
    user.favorite_boards.clear()
    user.favorite_boards.extend(boards)
    db.commit() 
    db.refresh(user)
    return user


def get_labels(db: Session) -> List[models.Label]:
    return db.query(models.Label).all()


def get_label_by_id(db: Session, label_id: int) -> LabelOrNone:
    return db.query(models.Label).filter_by(id=label_id).one_or_none()


def get_labels_by_ids(db: Session, labels_ids: List[int]) -> List[models.Label]:
    return db.query(models.Label).filter(models.Label.id.in_(labels_ids))


def create_label(db: Session, label: schema.LabelCreate) -> models.Label:
    db_label = models.Label(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label


def get_links(db: Session) -> List[models.Link]:
    return db.query(models.Link).all()

def get_link_by_id(db: Session, link_id) -> LinkOrNone:
    return db.query(models.Link).filter_by(id=link_id).one_or_none()

def create_link(db: Session, link: schema.LinkCreate) -> models.Link:
    db_link = models.Link(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def set_link_labels(db: Session, link_id: int, labels_ids: List[int]) -> models.Link:
    link = get_link_by_id(db=db, link_id=link_id)
    if link is None:
        return None

    labels = get_labels_by_ids(db=db, labels_ids=labels_ids)
    link.labels.clear()
    link.labels.extend(labels)    
    db.commit()
    db.refresh(link)
    return link


def get_boards(db: Session) -> List[models.Board]:
    return db.query(models.Board).all()


def get_boards_by_ids(db: Session, boards_ids: List[int]) -> List[models.Board]:
    return db.query(models.Board).filter(models.Board.id.in_(boards_ids))


def get_board_by_id(db: Session, board_id: int) -> BoardOrNone:
    return db.query(models.Board).filter_by(id=board_id).one_or_none()

def create_board(db: Session, board: schema.BoardCreate) -> models.Board:
    db_board = models.Board(**board.dict())
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def set_board_labels_filters(db: Session, board_id: int, labels_ids: List[int]) -> BoardOrNone:
    board = get_board_by_id(db=db, board_id=board_id)
    if board is None:
        return None

    labels = get_labels_by_ids(db=db, labels_ids=labels_ids)
    board.labels_filters.clear()
    board.labels_filters.extend(labels)
    db.commit()
    db.refresh(board)
    return board
