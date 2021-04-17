from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import models_manager_dependency
from db.schema import (
    User as UserSchema,
    UserBasicInfo as UserBasicInfoSchema
)
from db.models import ModelsManager


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/login", response_model=UserSchema, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Bad credentials"}})
def login(user_email: str, user_password: str, models_manager: ModelsManager = models_manager_dependency):
    user = models_manager.users.authentication(email=user_email, password=user_password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials"
        )
    return user


@router.get("/{user_id}", response_model=UserBasicInfoSchema)
def get_user_basic_info_by_id(user_id: int, models_manager: ModelsManager = models_manager_dependency):
    user = models_manager.users.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user


@router.put("/{user_id}/set_main_board", response_model=UserSchema)
def set_user_main_board(user_id: int, board_id: int, models_manager: ModelsManager = models_manager_dependency):
    user = models_manager.users.set_main_board(id=user_id, board_id=board_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user


@router.put("/{user_id}/set_favorite_boards", response_model=UserSchema)
def set_user_favorite_boards(user_id: int, boards_ids: List[int], models_manager: ModelsManager = models_manager_dependency):
    boards = models_manager.boards.filter_by_ids(ids=boards_ids)
    user = models_manager.users.set_favorite_boards(id=user_id, boards=boards)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
        )
    return user
