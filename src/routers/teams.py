from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from db.schema import (
    Team as TeamSchema,
    TeamCreate as TeamCreateSchema
)
from db.managers import TeamObjectsManager
from dependencies import get_objects_managers


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


team_manager_dependency = Depends(get_objects_managers(TeamObjectsManager))


@router.get("/", response_model=List[TeamSchema])
def get_team(team_manager: TeamObjectsManager = team_manager_dependency):
    return team_manager.objects.all()


@router.post("/", response_model=TeamSchema, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreateSchema, team_manager: TeamObjectsManager = team_manager_dependency):
    return team_manager.objects.create(model_schema=team)
