from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, status
from dependencies import models_manager_dependency
from db.models import ModelsManager
from db.schema import (
    Label as LabelSchema,
    LabelCreate as LabelCreateSchema
)


router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)


@router.get("/", response_model=List[LabelSchema])
def get_labels(models_manager: ModelsManager = models_manager_dependency):
    return models_manager.labels.all()


@router.get("/{label_id}", response_model=LabelSchema)
def get_label(label_id: int, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.labels.get(label_id)


@router.post("/", response_model=LabelSchema, status_code=status.HTTP_201_CREATED)
def create_label(label: LabelCreateSchema, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.labels.create(model_schema=label)
