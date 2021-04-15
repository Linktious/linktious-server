from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_db
from db import crud, schema

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/login", response_model=schema.User, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Bad credentials"}})
def login(user_email: str, user_password: str, db: Session = Depends(get_db)):
    user = crud.user_authentication(db=db, user_email=user_email, user_password=user_password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials"
        )
    return user


@router.get("/{user_id}", response_model=schema.UserBasicInfo)
def get_user_basic_info_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user


@router.put("/{user_id}/set_main_board", response_model=schema.User)
def set_user_main_board(user_id: int, board_id: int, db: Session = Depends(get_db)):
    user = crud.set_user_main_board(db=db, user_id=user_id, board_id=board_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return user



@router.put("/{user_id}/set_favorite_boards", response_model=schema.User)
def set_user_favorite_boards(user_id: int, boards_ids: List[int], db: Session = Depends(get_db)):
    user = crud.set_user_favorite_boards(db=db, user_id=user_id, boards_ids=boards_ids)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
        )
    return user
