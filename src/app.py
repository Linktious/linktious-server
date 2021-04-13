from typing import List
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import base, models, schema, crud

models.Base.metadata.create_all(bind=base.engine)

DEBUG = True
DEV = 'DEV'
PROD = 'PROD'
PORT = 8000
ENV = DEV

app = FastAPI(debug=DEBUG,
              title='Linktious')


# Dependency
def get_db():
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: add validation to routes
# TODO: return status codes
@app.get("/")
def read_root():
    return {"status": "OK"}


@app.get("/health")
def health_check():
    return {"status": "Ok"}


@app.get("/teams", response_model=List[schema.Team])
def get_team(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@app.get("/users/{user_email}", response_model=schema.User)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db=db, user_email=user_email)


@app.get("/users/{user_id}", response_model=schema.UserBasicInfo)
def get_user_basic_info_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db=db, user_id=user_id)


@app.put("/users/{user_id}/set_main_board", response_model=schema.User)
def set_user_main_board(user_id: int, board_id: int, db: Session = Depends(get_db)):
    return crud.set_user_main_board(db=db, user_id=user_id, board_id=board_id)


@app.put("/users/{user_id}/set_favorite_boards", response_model=schema.User)
def set_user_favorite_boards(user_id: int, boards_ids: List[int], db: Session = Depends(get_db)):
    return crud.set_user_favorite_boards(db=db, user_id=user_id, boards_ids=boards_ids)


@app.get("/labels", response_model=List[schema.Label])
def get_labels(db: Session = Depends(get_db)):
    return crud.get_labels(db=db)


@app.post("/labels", response_model=schema.Label)
def create_label(label: schema.LabelCreate, db: Session = Depends(get_db)):
    return crud.create_label(db=db, label=label)


@app.get("/links", response_model=List[schema.Link])
def get_links(db: Session = Depends(get_db)):
    return crud.get_links(db=db)


@app.post("/links", response_model=schema.Link)
def create_link(link: schema.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db=db, link=link)


@app.get("/boards", response_model=List[schema.Board])
def get_boards(db: Session = Depends(get_db)):
    return crud.get_boards(db=db)


@app.post("/boards", response_model=schema.Board)
def create_board(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)


@app.post("/boards/{board_id}/set_labels_filters", response_model=schema.Board)
def set_board_labels_filters(board_id: int, labels_ids: List[int], db: Session = Depends(get_db)):
    return crud.set_board_labels_filters(db=db, board_id=board_id, labels_ids=labels_ids)


def start():
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level="info", reload=ENV == DEV)


if __name__ == "__main__":
    start()
