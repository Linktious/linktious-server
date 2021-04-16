from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from db import crud, schema
from dependencies import get_db


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/", response_model=List[schema.Team])
def get_team(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@router.post("/", response_model=schema.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schema.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)
