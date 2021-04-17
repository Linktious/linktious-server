from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, status
from dependencies import models_manager_dependency
from db.schema import (
    Link as LinkSchema,
    LinkCreate as LinkCreateSchema
)
from db.models import ModelsManager


router = APIRouter(
    prefix="/links",
    tags=["links"],
)


@router.get("/", response_model=List[LinkSchema])
def get_links(models_manager: ModelsManager = models_manager_dependency):
    return models_manager.links.all()


@router.get("/{link_id}", response_model=LinkSchema)
def get_link(link_id: int, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.links.get(link_id)


@router.post("/", response_model=LinkSchema, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreateSchema, models_manager: ModelsManager = models_manager_dependency):
    return models_manager.links.create(model_schema=link)


@router.post("/{link_id}/set_labels", response_model=LinkSchema)
def set_link_labels(link_id: int, labels_ids: List[int], models_manager: ModelsManager = models_manager_dependency):
    labels = models_manager.labels.filter_by_ids(ids=labels_ids)
    return models_manager.links.set_labels(id=link_id, labels=labels)
