from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from db import crud, schema
from dependencies import get_db


router = APIRouter(
    prefix="/links",
    tags=["links"],
)


@router.get("/", response_model=List[schema.Link])
def get_links(db: Session = Depends(get_db)):
    return crud.get_links(db=db)


@router.post("/", response_model=schema.Link, status_code=status.HTTP_201_CREATED)
def create_link(link: schema.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db=db, link=link)


@router.post("/{link_id}/set_labels", response_model=schema.Link)
def set_link_labels(link_id: int, labels_ids: List[int], db: Session = Depends(get_db)):
    return crud.set_link_labels(db=db, link_id=link_id, labels_ids=labels_ids)
