from typing import List
from sqlalchemy.orm import Session

from . import models, schema

# TODO: create class for every model and implement there the logic
# TODO: add validations....

def get_teams(db: Session):
    return db.query(models.Team).all()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def set_user_main_board(db: Session, user_id: int, board_id: int):
    user = get_user_by_id(db=db, user_id=user_id)
    user.main_board_id = board_id
    db.commit()
    db.refresh(user)
    return user


def set_user_favorite_boards(db: Session, user_id: int, boards_ids: List[int]):
    user = get_user_by_id(db=db, user_id=user_id)
    boards = get_boards_by_ids(db=db, boards_ids=boards_ids)
    user.favorite_boards.clear()
    user.favorite_boards.extend(boards)
    db.commit()
    db.refresh(user)
    return user


def get_labels(db: Session):
    return db.query(models.Label).all()


def get_labels_by_ids(db: Session, labels_ids: List[int]):
    return db.query(models.Label).filter(models.Label.id.in_(labels_ids))


def create_label(db: Session, label: schema.LabelCreate):
    db_label = models.Label(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label


def get_links(db: Session):
    return db.query(models.Link).all()


def create_link(db: Session, link: schema.LinkCreate):
    db_link = models.Link(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_boards(db: Session):
    return db.query(models.Board).all()


def get_boards_by_ids(db: Session, boards_ids: List[int]):
    return db.query(models.Board).filter(models.Board.id.in_(boards_ids))


def get_board_by_id(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()

def create_board(db: Session, board: schema.BoardCreate):
    db_board = models.Board(**board.dict())
    db.add(board)
    db.commit()
    db.refresh(db_board)
    return db_board


def set_board_labels_filters(db: Session, board_id: int, labels_ids: List[int]):
    board = get_board_by_id(db=db, board_id=board_id)
    labels = get_labels_by_ids(db=db, labels_ids=labels_ids)
    board.labels_filters.clear()
    board.labels_filters.extend(labels)
    db.commit()
    db.refresh(board)
    return board
