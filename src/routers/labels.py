from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from dependencies import get_objects_managers
from db.schema import (
    Label as LabelSchema,
    LabelCreate as LabelCreateSchema
)
from db.models import Label as LabelModel
from db.managers import LabelManager


router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)


label_manager_dependency = Depends(get_objects_managers(LabelModel))


@router.get("/", response_model=List[LabelSchema])
def get_labels(label_manager: LabelManager = label_manager_dependency):
    return label_manager.all()


@router.get("/{label_id}", response_model=LabelSchema)
def get_label(label_id: int, label_manager: LabelManager = label_manager_dependency):
    return label_manager.get(label_id)


@router.post("/", response_model=LabelSchema, status_code=status.HTTP_201_CREATED)
def create_label(label: LabelCreateSchema, label_manager: LabelManager = label_manager_dependency):
    return label_manager.create(model_schema=label)
