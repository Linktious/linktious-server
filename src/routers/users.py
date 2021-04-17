from typing import List, Union, Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_objects_managers
from db.schema import (
    User as UserSchema,
    UserBasicInfo as UserBasicInfoSchema
)
from db.managers import UserObjectsManager, BoardObjectsManager


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


user_manager_dependency = Depends(get_objects_managers(UserObjectsManager))
user_and_board_managers_dependency = Depends(get_objects_managers(UserObjectsManager, BoardObjectsManager))
UserAndBoardManagers = Tuple[Union[UserObjectsManager, BoardObjectsManager]]



@router.post("/login", response_model=UserSchema, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Bad credentials"}})
def login(user_email: str, user_password: str, user_manager: UserObjectsManager = user_manager_dependency):
    user = user_manager.objects.authentication(email=user_email, password=user_password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials"
        )
    return user


@router.get("/{user_id}", response_model=UserBasicInfoSchema)
def get_user_basic_info_by_id(user_id: int, user_manager: UserObjectsManager = user_manager_dependency):
    user = user_manager.objects.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user


@router.put("/{user_id}/set_main_board", response_model=UserSchema)
def set_user_main_board(user_id: int, board_id: int, user_manager: UserObjectsManager = user_manager_dependency):
    user = user_manager.objects.set_main_board(id=user_id, board_id=board_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user


@router.put("/{user_id}/set_favorite_boards", response_model=UserSchema)
def set_user_favorite_boards(user_id: int, boards_ids: List[int], managers: UserAndBoardManagers = user_and_board_managers_dependency):
    user_manager, board_manager = managers
    boards = board_manager.objects.filter_by_ids(ids=boards_ids)
    user = user_manager.objects.set_favorite_boards(id=user_id, boards=boards)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
        )
    return user
