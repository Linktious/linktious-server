from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from dependencies import get_objects_managers
from db.schema import (
    Link as LinkSchema,
    LinkCreate as LinkCreateSchema
)
from db.models import (
    Link as LinkModel, 
    Label as LabelModel,
)
from db.managers import LinkManager, LabelManager


router = APIRouter(
    prefix="/links",
    tags=["links"],
)


link_manager_dependency = Depends(get_objects_managers(LinkModel))
link_and_label_managers_dependency = Depends(get_objects_managers(LinkModel, LabelModel))
LinkAndLabelManagers = Tuple[LinkManager, LabelManager]


@router.get("/", response_model=List[LinkSchema])
def get_links(link_manager: LinkManager = link_manager_dependency):
    return link_manager.all()


@router.get("/{link_id}", response_model=LinkSchema)
def get_link(link_id: int, link_manager: LinkManager = link_manager_dependency):
    return link_manager.get(link_id)


@router.post("/", response_model=LinkSchema, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreateSchema, link_manager: LinkManager = link_manager_dependency):
    return link_manager.create(model_schema=link)


@router.post("/{link_id}/set_labels", response_model=LinkSchema)
def set_link_labels(link_id: int, labels_ids: List[int], managers: LinkAndLabelManagers = link_and_label_managers_dependency):
    link_manager, label_manager = managers
    labels = label_manager.filter_by_ids(ids=labels_ids)
    return link_manager.set_labels(id=link_id, labels=labels)
