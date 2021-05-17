from typing import List
from fastapi import APIRouter, status
from dependencies import models_manager_dependency
from db.models import ModelsManager
from db.schema import (
    Board as BoardSchema,
    BoardCreate as BoardCreateSchema
)


router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)


@router.get("/", response_model=List[BoardSchema])
def get_boards(models_manager: ModelsManager = models_manager_dependency):
    return models_manager.boards.all()


@router.get("/{board_id}", response_model=BoardSchema)
def get_board(board_id: int, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.boards.get(board_id)


@router.post("/", response_model=BoardSchema, status_code=status.HTTP_201_CREATED)
def create_board(board: BoardCreateSchema, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.boards.create(model_schema=board)


@router.post("/{board_id}/set_labels_filters", response_model=BoardSchema)
def set_board_labels_filters(board_id: int, labels_ids: List[int], models_manager: ModelsManager = models_manager_dependency):
    labels = models_manager.labels.filter_by_ids(ids=labels_ids)
    return models_manager.boards.set_labels_filters(board_id=board_id, labels=labels)
