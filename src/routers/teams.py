from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, status

from dependencies import models_manager_dependency
from db.schema import (
    Team as TeamSchema,
    TeamCreate as TeamCreateSchema
)
from db.querysets import ModelsManager


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/", response_model=List[TeamSchema])
def get_team(models_manager: ModelsManager = models_manager_dependency):
    return models_manager.teams.all()


@router.post("/", response_model=TeamSchema, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreateSchema, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.teams.create(model_schema=team)
