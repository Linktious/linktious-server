from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from db import crud, schema
from dependencies import get_db


router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)


@router.get("/", response_model=List[schema.Label])
def get_labels(db: Session = Depends(get_db)):
    return crud.get_labels(db=db)


@router.post("/", response_model=schema.Label, status_code=status.HTTP_201_CREATED)
def create_label(label: schema.LabelCreate, db: Session = Depends(get_db)):
    return crud.create_label(db=db, label=label)
