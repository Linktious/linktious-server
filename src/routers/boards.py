from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from dependencies import get_objects_managers
from db.schema import (
    Board as BoardSchema,
    BoardCreate as BoardCreateSchema
)
from db.models import (
    Board as BoardModel, 
    Label as LabelModel,
)
from db.base import ManagerProxy

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)


board_manager_dependency = Depends(get_objects_managers(BoardModel))
board_and_label_managers_dependency = Depends(get_objects_managers(BoardModel, LabelModel))
BoardAndLabelManagers = Tuple[ManagerProxy]


@router.get("/", response_model=List[BoardSchema])
def get_boards(board_manager: ManagerProxy = board_manager_dependency):
    return board_manager.objects.all()


@router.get("/{board_id}", response_model=BoardSchema)
def get_board(board_id: int, board_manager: ManagerProxy = board_manager_dependency):
    return board_manager.objects.get(board_id)


@router.post("/", response_model=BoardSchema, status_code=status.HTTP_201_CREATED)
def create_board(board: BoardCreateSchema, board_manager: ManagerProxy = board_manager_dependency):
    return board_manager.objects.create(model_schema=board)


@router.post("/{board_id}/set_labels_filters", response_model=BoardSchema)
def set_board_labels_filters(board_id: int, labels_ids: List[int], managers: BoardAndLabelManagers = board_and_label_managers_dependency):
    board_manager, label_manager = managers
    labels = label_manager.objects.filter_by_ids(ids=labels_ids)
    return board_manager.objects.set_labels_filters(id=board_id, labels=labels)
