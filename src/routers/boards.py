from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from db import crud, schema
from dependencies import get_db


router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)


@router.get("/", response_model=List[schema.Board])
def get_boards(db: Session = Depends(get_db)):
    return crud.get_boards(db=db)


@router.post("/", response_model=schema.Board, status_code=status.HTTP_201_CREATED)
def create_board(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)


@router.post("/{board_id}/set_labels_filters", response_model=schema.Board)
def set_board_labels_filters(board_id: int, labels_ids: List[int], db: Session = Depends(get_db)):
    return crud.set_board_labels_filters(db=db, board_id=board_id, labels_ids=labels_ids)
